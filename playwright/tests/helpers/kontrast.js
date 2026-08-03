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

// Ранији тестови су мерили само режиме који ОДСТУПАЈУ од подразумеваног, јер је
// светла тема тада важила за неприкосновену („светла остаје пиксел-идентична").
// Од поправке heritage тонова то више не важи — светла се мери као и остале.
const REZIMI = ['dark', 'contrast'];
const SVI_REZIMI = ['light', 'dark', 'contrast'];
const STILOVI = ['institucionalna', 'moderna', 'arhivska', 'terenska'];
// Именоване равне теме: фаза 1 (plava-*) + фаза 2 (неутралне/институционалне).
// Мери се у комфорној и компактној густини (густина мења паддинг/оквире) и у
// светлом и тамном режиму (фаза 2: равна палета поштује mode кроз dark-flat слој).
const PALETE = ['plava-klasicna', 'plava-windows', 'plava-tamna', 'plava-ledena',
  'plava-muzejska', 'siva-poslovna', 'zelena-institucionalna', 'bordo-muzejska',
  'crno-bela'];
const GUSTINE = ['komforno', 'kompakt'];
const PALETE_REZIMI = ['light', 'dark'];
// Акцентна оса (фаза 2). 'podrazumevano' (идентитет палете) се покрива
// подразумеваним пролазом палете, па се овде мере 9 експлицитних боја.
const ACCENTI = ['klasicna-plava', 'svetloplava', 'tamnoplava', 'tirkizna',
  'zelena', 'ljubicasta', 'bordo', 'narandzasta', 'grafitnosiva'];

async function postaviTemu(page, rezim, stil) {
  // Промена теме покреће CSS transition на боји. На тешким странама (нпр.
  // збирка са 2700 редова) мерење ухвати боју УСРЕД прелаза — ни стару ни нову
  // — па тест пада насумично, зависно од оптерећења. Прелази се гасе пре мерења.
  await page.addStyleTag({
    content: `*, *::before, *::after {
      transition: none !important;
      animation: none !important;
    }`,
  });
  await page.evaluate(([r, s]) => {
    document.documentElement.setAttribute('data-theme', r);
    document.documentElement.setAttribute('data-bs-theme', r === 'dark' ? 'dark' : 'light');
    if (s === 'institucionalna') document.documentElement.removeAttribute('data-style');
    else document.documentElement.setAttribute('data-style', s);
  }, [rezim, stil]);
  await page.waitForTimeout(200);
}

// Примени именовану равну палету исто како то ради base.html скрипт: постави
// data-palette, скини style осу, и разреши режим (light → без data-theme;
// dark → data-theme=dark + dark data-bs-theme, што пали заједнички dark-flat
// слој). Акценат се посебно поставља кроз postaviAkcenat.
async function postaviPaletu(page, paleta, gustina, rezim) {
  rezim = rezim || 'light';
  await page.addStyleTag({
    content: `*, *::before, *::after {
      transition: none !important;
      animation: none !important;
    }`,
  });
  await page.evaluate(([p, g, r]) => {
    const root = document.documentElement;
    root.removeAttribute('data-accent');
    root.removeAttribute('data-style');
    root.setAttribute('data-palette', p);
    if (r === 'dark') {
      root.setAttribute('data-theme', 'dark');
      root.setAttribute('data-bs-theme', 'dark');
    } else {
      root.removeAttribute('data-theme');
      root.setAttribute('data-bs-theme', 'light');
    }
    if (g === 'komforno') root.removeAttribute('data-density');
    else root.setAttribute('data-density', g);
  }, [paleta, gustina, rezim]);
  await page.waitForTimeout(200);
}

// Постави/скини акцентну осу (фаза 2). 'podrazumevano' → скини (идентитет палете).
async function postaviAkcenat(page, akcenat) {
  await page.evaluate((a) => {
    const root = document.documentElement;
    if (!a || a === 'podrazumevano') root.removeAttribute('data-accent');
    else root.setAttribute('data-accent', a);
  }, akcenat);
  await page.waitForTimeout(120);
}

// Враћа падове: [{selektor, tekst, fg, bg, odnos, prag}]
async function izmeriKontrast(page, korenSelektor) {
  // 0) Мери се и снима у ИСТОМ стању распореда.
  //
  // `screenshot({fullPage:true})` привремено развуче прозор на целу висину
  // документа. Ако се правоугаоници покупе при висини 720, а снимак направи при
  // висини нпр. 3780, распоред се помери (`min-height: 100vh` и сродно) па
  // координате гађају погрешне пикселе — насумично, зависно од стране и стила
  // (навигација је испадала „злато на крему", розе заглавље „крем на крему").
  // Зато се прозор прво развуче, па се тек онда мери и снима.
  const stariProzor = page.viewportSize();
  const visinaDok = await page.evaluate(() => document.documentElement.scrollHeight);
  const punaVisina = Math.min(Math.max(visinaDok, stariProzor ? stariProzor.height : 720), 8000);
  await page.setViewportSize({ width: stariProzor ? stariProzor.width : 1280, height: punaVisina });
  await page.waitForTimeout(150);

  try {
    return await izmeriUStanju(page, korenSelektor);
  } finally {
    if (stariProzor) await page.setViewportSize(stariProzor);
  }
}

async function izmeriUStanju(page, korenSelektor) {
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
    // Емоџи носи сопствене боје и не прати `color` — мерење контраста над њим
    // је лажна пријава (нпр. застава 🇷🇸 у бирачу језика).
    const samoEmoji = (s) => /^[\p{Extended_Pictographic}\p{Emoji_Presentation}️‍\s]+$/u.test(s);

    // ОГРАНИЧЕЊЕ: `position: fixed|sticky` се на снимку целе стране не поклапа
    // са својим правоугаоником — снимак се прави са развученим прозором, а
    // лепљиви елемент остаје „закачен" другде, па се очита погрешан пиксел
    // (навигација је испадала „злато на крему" 1.15:1, иако је стварно злато на
    // бордо ≈ 5.5:1). Такви се овде прескачу; навигацију покрива
    // `kontrast-menija.spec.js`, који мери отворене меније директно.
    const uLepljivom = (el) => {
      for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
        const p = getComputedStyle(n).position;
        if (p === 'fixed' || p === 'sticky') return true;
      }
      return false;
    };

    // Хоризонтално исечени елементи: десне колоне широке табеле у
    // `.table-responsive` (overflow-x:auto) излазе ван видљивог оквира
    // контејнера. `screenshot({fullPage})` хвата само висину документа, не и
    // хоризонтални скрол унутар контејнера — па се за исечену ћелију очита
    // пиксел ПОРЕД ње (позадина стране). Бело мастило на тамноплавом заглављу
    // тако лажно испадне „бело на светлом". Досад је пролазило само зато што
    // heritage заглавља имају ТАМАН текст, који и на погрешно очитаној светлој
    // позадини задовољава AA. Исти разлог за прескакање као код lepljivih.
    const isecenHscroll = (el) => {
      const r = el.getBoundingClientRect();
      for (let n = el.parentElement; n && n.nodeType === 1; n = n.parentElement) {
        const cs = getComputedStyle(n);
        if (/(auto|scroll)/.test(cs.overflowX)) {
          const nr = n.getBoundingClientRect();
          if (r.right > nr.left + n.clientWidth + 1 || r.left < nr.left - 1) return true;
        }
      }
      return false;
    };

    const out = [];
    const svi = [...new Set(koreni.flatMap((k) => [k, ...k.querySelectorAll('*')]))];
    for (const el of svi) {
      const tekst = [...el.childNodes]
        .filter((n) => n.nodeType === 3).map((n) => n.textContent.trim()).join(' ').trim();
      if (!tekst || samoEmoji(tekst) || uLepljivom(el) || isecenHscroll(el)) continue;
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

  // 2) сакриј СВЕ текстове па сними — остаје чиста позадина.
  //
  // Мора ИНЛАЈН, не преко <style>: `* { color: transparent !important }` има
  // специфичност (0,0,0), па га туче свако друго `!important` правило са јачим
  // селектором (нпр. `--navbar-text` на навигацији). Такав текст остане видљив,
  // мери се ГЛИФ уместо позадине и испадне „злато на злату" ≈ 1.15:1 — лажна
  // пријава. Декларација у style атрибуту бије сваки селектор, па хвата и њих.
  const vraceno = await page.evaluate(() => {
    const stari = [];
    for (const el of document.querySelectorAll('*')) {
      stari.push([el, el.style.getPropertyValue('color'), el.style.getPropertyPriority('color'),
        el.style.getPropertyValue('text-shadow')]);
      el.style.setProperty('color', 'transparent', 'important');
      el.style.setProperty('text-shadow', 'none', 'important');
    }
    window.__kontrastVrati = () => {
      for (const [el, boja, prio, senka] of stari) {
        if (boja) el.style.setProperty('color', boja, prio); else el.style.removeProperty('color');
        if (senka) el.style.setProperty('text-shadow', senka); else el.style.removeProperty('text-shadow');
      }
    };
    return document.querySelectorAll('*').length;
  });

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
  await page.evaluate(() => { if (window.__kontrastVrati) window.__kontrastVrati(); });

  return padovi;
}

module.exports = {
  REZIMI, SVI_REZIMI, STILOVI, PALETE, GUSTINE, PALETE_REZIMI, ACCENTI,
  postaviTemu, postaviPaletu, postaviAkcenat, izmeriKontrast,
};
