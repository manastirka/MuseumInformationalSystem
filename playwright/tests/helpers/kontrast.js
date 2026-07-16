// Мерење контраста које ХВАТА оно што axe пропушта.
//
// Зашто постоји: axe не уме да израчуна контраст кад је позадина градијент —
// такав чвор заврши у `incomplete` корпи (messageKey `bgGradient`,
// contrastRatio 0), НЕ у `violations`. Управо тако је продукцијски баг на
// детаљном приказу фотографије прошао испод радара: `.fototeka-card` је имао
// хардкодован бели градијент, а текст је наслеђивао светли токен теме —
// 1.26:1, а axe је ћутао.
//
// Како мери: не погађа позадину из CSS-а (градијент има више станица, па се из
// стила не зна КОЈА је тачно испод текста — то даје лажне пријаве). Уместо
// тога узима СТВАРНЕ пикселе: сакрије сав текст, сними страну, врати снимак у
// страницу преко canvas-а и очита боју тачно испод сваког текста. То ради и за
// градијенте, и за слике, и за преклопљене полупровидне слојеве.

const REZIMI = ['dark', 'contrast'];
const STILOVI = ['institucionalna', 'moderna', 'arhivska', 'terenska'];

async function postaviTemu(page, rezim, stil) {
  await page.evaluate(([r, s]) => {
    document.documentElement.setAttribute('data-theme', r);
    document.documentElement.setAttribute('data-bs-theme', r === 'dark' ? 'dark' : 'light');
    if (s === 'institucionalna') document.documentElement.removeAttribute('data-style');
    else document.documentElement.setAttribute('data-style', s);
  }, [rezim, stil]);
  await page.waitForTimeout(200);
}

const SAKRIJ_ID = '__kontrast_sakrij__';

// Враћа падове: [{selektor, tekst, fg, bg, odnos, prag}]
async function izmeriKontrast(page, korenSelektor) {
  // 1) покупи кандидате (елементи са сопственим видљивим текстом)
  const kandidati = await page.evaluate((koren) => {
    // querySelectorAll, не querySelector: селектор попут `.fototeka-card` гађа
    // ВИШЕ плоча, а текст који пада може бити у било којој — мерење само прве
    // (она са сликом, без текста) лажно прође.
    const koreni = koren ? [...document.querySelectorAll(koren)] : [document.body];
    if (!koreni.length) return [];
    const selektorZa = (el) => {
      if (el.id) return '#' + el.id;
      const cls = (el.className && typeof el.className === 'string')
        ? '.' + el.className.trim().split(/\s+/).slice(0, 3).join('.') : '';
      return el.tagName.toLowerCase() + cls;
    };
    const out = [];
    const svi = [...new Set(koreni.flatMap((k) => [k, ...k.querySelectorAll('*')]))];
    for (const el of svi) {
      const tekst = [...el.childNodes]
        .filter((n) => n.nodeType === 3).map((n) => n.textContent.trim()).join(' ').trim();
      if (!tekst) continue;
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) < 0.05) continue;
      const r = el.getBoundingClientRect();
      if (r.width < 4 || r.height < 4) continue;
      // ван екрана — не мери се
      if (r.bottom < 0 || r.top > (window.scrollY + window.innerHeight + 4000)) continue;
      const px = parseFloat(cs.fontSize);
      const bold = (parseInt(cs.fontWeight, 10) || 400) >= 700;
      out.push({
        selektor: selektorZa(el),
        tekst: tekst.slice(0, 40),
        fg: cs.color,
        px,
        veliki: px >= 24 || (bold && px >= 18.66),
        x: r.left + window.scrollX,
        y: r.top + window.scrollY,
        w: r.width,
        h: r.height,
      });
    }
    return out;
  }, korenSelektor);

  if (!kandidati.length) return [];

  // 2) сакриј СВЕ текстове па сними — остаје чиста позадина
  await page.addStyleTag({
    content: `#${SAKRIJ_ID}{}
      *, *::before, *::after {
        color: transparent !important;
        text-shadow: none !important;
        text-decoration-color: transparent !important;
        caret-color: transparent !important;
      }`,
  }).then((h) => h.evaluate((el, id) => el.setAttribute('id', id), SAKRIJ_ID));

  const snimak = (await page.screenshot({ fullPage: true })).toString('base64');

  // 3) врати снимак у страницу и очитај пикселе испод сваког текста
  const padovi = await page.evaluate(async ([b64, kand]) => {
    const img = new Image();
    img.src = 'data:image/png;base64,' + b64;
    await img.decode();
    const c = document.createElement('canvas');
    c.width = img.naturalWidth; c.height = img.naturalHeight;
    const ctx = c.getContext('2d', { willReadFrequently: true });
    ctx.drawImage(img, 0, 0);

    // снимак може бити у другој скали од CSS пиксела
    const skala = img.naturalWidth / Math.max(document.documentElement.scrollWidth, 1);

    const parseRgb = (s) => {
      const m = s.match(/rgba?\(([^)]+)\)/);
      if (!m) return null;
      const d = m[1].split(',').map((x) => parseFloat(x.trim()));
      return { r: d[0], g: d[1], b: d[2], a: d.length > 3 ? d[3] : 1 };
    };
    const lum = (c2) => {
      const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
      return 0.2126 * f(c2.r) + 0.7152 * f(c2.g) + 0.0722 * f(c2.b);
    };
    const odnos = (a, b) => {
      const l1 = lum(a), l2 = lum(b);
      return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    };
    const spoji = (fg, bg) => ({
      r: fg.r * fg.a + bg.r * (1 - fg.a),
      g: fg.g * fg.a + bg.g * (1 - fg.a),
      b: fg.b * fg.a + bg.b * (1 - fg.a),
      a: 1,
    });

    const out = [];
    for (const k of kand) {
      const fg0 = parseRgb(k.fg);
      if (!fg0) continue;
      // узорак: неколико тачака унутар кутије текста
      const tacke = [];
      const nx = 5, ny = 3;
      for (let i = 1; i <= nx; i++) {
        for (let j = 1; j <= ny; j++) {
          tacke.push([k.x + (k.w * i) / (nx + 1), k.y + (k.h * j) / (ny + 1)]);
        }
      }
      // ДОМИНАНТНА боја узорка, не најгора: текст лежи на својој позадини, а
      // понеки узорак може да падне на ивицу или суседни елемент — то би дало
      // лажну пријаву. Боје се групишу грубо (корак 8) па се узима најчешћа.
      const brojac = new Map();
      for (const [px0, py0] of tacke) {
        const px = Math.round(px0 * skala), py = Math.round(py0 * skala);
        if (px < 0 || py < 0 || px >= c.width || py >= c.height) continue;
        const d = ctx.getImageData(px, py, 1, 1).data;
        const kljuc = `${d[0] >> 3},${d[1] >> 3},${d[2] >> 3}`;
        const rec = brojac.get(kljuc) || { n: 0, r: d[0], g: d[1], b: d[2] };
        rec.n++;
        brojac.set(kljuc, rec);
      }
      if (!brojac.size) continue;
      const dom = [...brojac.values()].sort((a, b) => b.n - a.n)[0];
      const najgoriBg = { r: dom.r, g: dom.g, b: dom.b, a: 1 };
      const fg = fg0.a < 1 ? spoji(fg0, najgoriBg) : fg0;
      const najgori = odnos(fg, najgoriBg);
      const prag = k.veliki ? 3.0 : 4.5;
      if (najgori !== null && najgori < prag) {
        out.push({
          selektor: k.selektor,
          tekst: k.tekst,
          fg: k.fg,
          bg: `rgb(${najgoriBg.r},${najgoriBg.g},${najgoriBg.b})`,
          odnos: Math.round(najgori * 100) / 100,
          prag,
        });
      }
    }
    return out;
  }, [snimak, kandidati]);

  // 4) врати текст
  await page.evaluate((id) => { const el = document.getElementById(id); if (el) el.remove(); }, SAKRIJ_ID);

  return padovi;
}

module.exports = { REZIMI, STILOVI, postaviTemu, izmeriKontrast };
