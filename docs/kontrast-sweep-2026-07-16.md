# Контраст — систематски обилазак (2026-07-16)

Пети пријављени контраст-баг (текст око слике у Фототеци) био је повод да се
уместо још једне појединачне поправке уради **мерење целе површине**.

## Шта је мерено

`playwright/tests/kontrast-sweep.spec.js` + `playwright/tests/helpers/kontrast.js`:
18 страна × {тамна, висок контраст} × 4 стила = **8 комбинација**, укључујући
overlay елементе (модали преко својих тригера, dropdown-и).

## Зашто axe није био довољан (кључни налаз)

`axe-core` **не пријављује** текст на градијент-позадини: не уме да израчуна
боју, па чвор заврши у `incomplete` корпи (`messageKey: "bgGradient"`,
`contrastRatio: 0`) — **не** у `violations`. На детаљном приказу фотографије
било је **45** таквих чворова, а сам баг који је корисник пријавио био је међу
њима. Зато статичке провере и претходне четири поправке нису ово ухватиле.

Мерач овде зато не погађа боју из CSS-а него **чита стварни пиксел**: сакрије
сав текст, сними страну, врати снимак кроз canvas и очита боју тачно испод
текста. Ради и за градијенте, слике и полупровидне слојеве.

> Два погрешна приступа су успут одбачена, да се не понављају: (1) „најгора
> станица градијента" и (2) „најгори узорак у кутији" — оба дају лажне пријаве
> (навигација и подножје испадну као бело-на-белом иако су читљиви). Исправно
> је: **доминантна** боја узорка испод текста.

## Стање

- **Укупно нађено:** 103 корена испод AA (2201 појава кроз 8 комбинација).
- **Поправљено:** 14 корена — цела класа „хардкодована бела плоча" (`.fototeka-card`,
  `.dokumenti-card`, `.search-card`, space/docs плоче — 8 шаблона, један блок у
  `main.css`). Покривено тестом `kontrast-fototeka-detalj.spec.js` (8/8).
- **ОСТАЈЕ: ~58 корена** — пописано доле, НИЈЕ поправљено.

### Пролаз 3 (`/zahtevi/*` + збирка) — `prod-2026-07-16-6`

Поправљено још 16 корена (тест: `kontrast-zahtevi-zbirke.spec.js`, 5 страна × 4 стила):

1. **`.document-preview` — фиксно бели папир.** Преглед молбе је документ који се
   штампа и остаје бео у свакој теми, а текст је наслеђивао токен теме → крем на
   белом, 1.18–1.31:1. Иста замка као навигација, само обрнута: тамно мастило на
   ТРАЈНО светлој подлози. Уведен `--paper-text` (вредност = затечено heritage
   мастило #4a311f, да светла остане пиксел-идентична). Исти шаблон користе
   4 стране захтева.
2. **Исти образац изван прегледа** — `.highlight-field` (#fff3cd), `.integration-status`,
   `.selected-locations-summary` (#f8f9fa): фиксно светле површине, 1.18–2.92:1.
   Битно: правило мора да покрије и ПОТОМКЕ (`.integration-status *`) јер груби
   `[data-theme="dark"] p, span, label` гађа дете директно и туче наслеђивање.
3. **`.bg-light .text-muted`** — `.bg-light` је у тамној `--gray-100` (#374151),
   светлије од картице, па `--text-muted` пада на 3.35:1 → корак на `--text-secondary`.
4. **`.btn-outline-secondary`** — задржавао Bootstrap сиву (#6c757d) на тамној: 3.4:1.

Мерач: гашење CSS прелаза пре мерења. Промена теме покреће transition на боји; на
тешким странама (збирка, 2700 редова) мерење је хватало боју УСРЕД прелаза
(#987f61 — ни стара ни нова) па је тест падао насумично, зависно од оптерећења.

### Пролаз 2 (образац „црно/тамно на тамном") — `prod-2026-07-16-5`

Поправљено још 15 корена на `/admin/timesheet_reports` и `/vehicle_reservations`
(тест: `kontrast-crno-na-tamnom.spec.js`, тамна × 4 стила):

1. **Контекстуалне врсте табеле** (`.table-success` и род) — Bootstrap на врсти
   хардкодује `--bs-table-color: #000`; подлога у тамној постаје тамна, текст
   остаје црн (1.23:1). Шаблони их користе 42 пута → решено једним блоком.
2. **`.text-success`** — `--success` (#059669) је боја позадине, као текст даје
   2.28:1. Уведен засебан токен `--success-text` (не дира се `--success`, јер би
   се померила позадина беџева).
3. **`.dropdown-toggle-submenu`** (мега-мени, overlay, на СВАКОЈ страни) — ранија
   поправка 5615ce5 ослонила се на светлији `--primary-dark`, али
   `body.heritage-shell` га враћа на тамнозелену (#3c7561) → 2.61:1. Та поправка
   је практично била мртва свуда.

### ВАЖНО: део налаза НИЈЕ баг тамне теме

Преосталих 6 корена на те две стране (браон heritage површине + крем текст:
`badge bg-light/bg-warning/bg-secondary`, `btn-secondary`, `h5.mb-0`,
`small.text-muted`) **падају и у СВЕТЛОЈ теми** — измерено: `badge bg-light`
2.59:1, `bg-warning` 2.98:1, `btn-secondary` 4.48:1 (исто као у тамној).
Извор је `body.heritage-shell .badge` (L1840) и род — хардкодоване боје које не
прате тему.

Дакле то нису баг тамне теме него **глобални**, а светла је ПОДРАЗУМЕВАНА тема.
Поправка мења изглед светле теме свим корисницима, што досадашња конвенција
(„светла остаје пиксел-идентична") избегава — зато је свесно остављено за
одлуку, а не тихо поправљено само у тамној (то би била половична поправка).

## Обрасци у ономе што остаје

1. **Бутстрап подразумевано на тамној подлози** — `td`/`strong` црно на тамној
   (`/admin/timesheet_reports`, 1.23:1), `small.text-success`, `small.text-muted`.
2. **Бела „папирна" подлога прегледа** — `/zahtevi/godisnji-odmor` (образац молбе
   је бела страница, текст наслеђује токен теме): `.highlight-field` 1.18:1.
3. **Overlay** — `a.dropdown-item` црно на бордо у мега-менију
   (`/admin/mineral_collection`, 1.53:1).

## Списак (најгори прво, по страни)

### `/zahtevi/godisnji-odmor` — 16 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **1.18:1** | strana | `#previewBrojDana` | rgb(236, 224, 201) → rgb(255,243,205) | __ |
| **1.18:1** | strana | `span.highlight-field` | rgb(236, 224, 201) → rgb(255,243,205) | ________________ |
| **1.31:1** | strana | `#previewPeriod` | rgb(236, 224, 201) → rgb(255,255,255) | __-__.__.____ |
| **1.31:1** | strana | `#previewDatum` | rgb(236, 224, 201) → rgb(255,255,255) | 16.07.2026. |
| **1.68:1** | strana | `h1.h3.mb-1` | rgb(236, 224, 201) → rgb(241,139,231) | Захтев за годишњи одмор |
| **1.7:1** | strana | `p.mb-0.opacity-75` | rgb(236, 224, 201) → rgb(240,136,226) | Креирање молбе за годишњи од |
| **2.07:1** | strana | `div.header-to` | rgb(173, 181, 189) → rgb(255,255,255) | Директору Природњачког музеј |
| … | | још 8 | | |

### `/admin/timesheet_reports` — 13 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **1.23:1** | strana | `strong` | rgb(0, 0, 0) → rgb(37,29,21) | Александар Луковић |
| **1.23:1** | strana | `td` | rgb(0, 0, 0) → rgb(37,29,21) | December 2027 |
| **1.23:1** | strana | `td.col-org` | rgb(0, 0, 0) → rgb(37,29,21) | ГЕОЛОШКО ОДЕЉЕЊЕ |
| **1.23:1** | strana | `td.text-end.col-number` | rgb(0, 0, 0) → rgb(37,29,21) | 8.00 |
| **1.24:1** | strana | `td.text-end.col-number.fw-semibold` | rgb(0, 0, 0) → rgb(37,29,21) | 8.00 |
| **2.47:1** | strana | `span.badge.bg-light.text-dark` | rgb(33, 37, 41) → rgb(126,95,54) | Рад у музеју |
| **2.61:1** | dropdown | `a.dropdown-item.dropdown-toggle-submenu` | rgb(60, 117, 97) → rgb(53,41,29) | Биологија |
| … | | још 5 | | |

### `/admin/mineral_collection` — 12 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **1.53:1** | dropdown | `a.dropdown-item` | rgb(0, 0, 0) → rgb(86,23,25) | 3D Депо |
| **2.17:1** | strana | `span.badge.bg-success.ms-1` | rgb(255, 255, 255) → rgb(107,163,138) | 2709 |
| **2.6:1** | strana | `span.badge.bg-white.text-dark` | rgb(33, 37, 41) → rgb(126,94,54) | 1/55 • 2709 укупно |
| **2.61:1** | dropdown | `a.dropdown-item.dropdown-toggle-submenu` | rgb(60, 117, 97) → rgb(53,41,29) | Биологија |
| **3.35:1** | strana | `a.nav-link.active` | rgb(255, 255, 255) → rgb(6,154,107) | Музејска збирка |
| **3.35:1** | strana | `small.text-muted.fw-medium` | rgb(165, 144, 111) → rgb(55,65,81) | Приказ по страни: |
| **4.07:1** | strana | `span.page-link` | rgb(165, 140, 107) → rgb(54,48,42) | ... |
| … | | још 4 | | |

### `/vehicle_reservations` — 8 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **1:1** | modal #reservationModal | `button.btn.btn-primary` | rgb(255, 255, 255) → rgb(255,255,255) | Резервиши |
| **1:1** | strana | `small.text-muted` | rgb(165, 144, 111) → rgb(127,95,65) | - |
| **1.13:1** | strana | `small.text-success` | rgb(4, 97, 63) → rgb(39,85,71) | Слободно |
| **1.2:1** | modal #reservationModal | `button.btn.btn-secondary` | rgb(246, 233, 207) → rgb(133,101,69) | Откажи |
| **2.01:1** | strana | `small.text-muted` | rgba(33, 37, 41, 0.75) → rgb(130,97,66) | - |
| **2.28:1** | strana | `small.text-success` | rgb(5, 150, 105) → rgb(39,84,70) | Слободно |
| **2.61:1** | dropdown | `a.dropdown-item.dropdown-toggle-submenu` | rgb(60, 117, 97) → rgb(53,41,29) | Биологија |

### `/terenska-aktivnost` — 8 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **1.67:1** | strana | `h1.h3.mb-1` | rgb(236, 224, 201) → rgb(244,143,23) | Теренска активност |
| **1.88:1** | strana | `p.mb-0.opacity-75` | rgb(236, 224, 201) → rgb(244,138,22) | Преглед теренских активности |
| **1.89:1** | strana | `small.text-muted` | rgb(165, 144, 111) → rgb(55,65,81) | Завршене |
| **2.26:1** | strana | `p.mb-0.opacity-75` | rgb(255, 255, 255) → rgb(244,151,23) | Преглед теренских активности |
| **2.39:1** | strana | `h1.h3.mb-1` | rgb(255, 255, 255) → rgb(244,143,23) | Теренска активност |
| **2.61:1** | dropdown | `a.dropdown-item.dropdown-toggle-submenu` | rgb(60, 117, 97) → rgb(53,41,29) | Биологија |
| **4.45:1** | strana | `span.badge.bg-secondary` | rgb(247, 234, 208) → rgb(134,101,69) | Завршена |

### `/fototeka` — 4 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **2.33:1** | strana | `#fototekaSelCount` | rgb(236, 224, 201) → rgb(93,161,131) | 0 |
| **2.61:1** | dropdown | `a.dropdown-item.dropdown-toggle-submenu` | rgb(60, 117, 97) → rgb(53,41,29) | Биологија |
| **3.92:1** | strana | `span.foto-format` | rgb(236, 224, 201) → rgb(105,110,119) | JPG |

### `/fototeka/uvoz` — 4 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **1.46:1** | strana | `code` | rgb(214, 51, 132) → rgb(27,66,48) | data/fototeka_import |
| **2.61:1** | dropdown | `a.dropdown-item.dropdown-toggle-submenu` | rgb(60, 117, 97) → rgb(53,41,29) | Биологија |
| **2.62:1** | strana | `code` | rgb(230, 133, 181) → rgb(27,66,48) | data/fototeka_import |

### `/admin/manage_access` — 4 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **2.56:1** | strana | `span.badge.bg-light.text-dark` | rgb(33, 37, 41) → rgb(125,94,54) | Бело |
| **2.61:1** | dropdown | `a.dropdown-item.dropdown-toggle-submenu` | rgb(60, 117, 97) → rgb(53,41,29) | Биологија |
| **4.25:1** | strana | `h6.mb-0.small` | rgb(236, 224, 201) → rgb(130,98,67) | Модули |

### `/vehicle_management` — 4 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **1:1** | modal #addVehicleModal | `button.btn.btn-primary` | rgb(255, 255, 255) → rgb(255,255,255) | Додај возило |
| **1.2:1** | modal #addVehicleModal | `button.btn.btn-secondary` | rgb(246, 233, 207) → rgb(133,100,69) | Откажи |
| **2.61:1** | dropdown | `a.dropdown-item.dropdown-toggle-submenu` | rgb(60, 117, 97) → rgb(53,41,29) | Биологија |

### `/dashboard` — 4 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **2.61:1** | dropdown | `a.dropdown-item.dropdown-toggle-submenu` | rgb(60, 117, 97) → rgb(53,41,29) | Биологија |
| **2.64:1** | strana | `span.weather-location` | rgba(243, 226, 188, 0.4) → rgb(103,43,45) | Београд · клик за детаље |
| **3.32:1** | strana | `span.weather-wind` | rgba(243, 226, 188, 0.5) → rgb(101,42,43) | RHMZ дневна провера |

### `/fototeka/upload` — 3 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **2.61:1** | dropdown | `a.dropdown-item.dropdown-toggle-submenu` | rgb(60, 117, 97) → rgb(53,41,29) | Биологија |
| **3.88:1** | strana | `div.form-text` | rgb(138, 125, 99) → rgb(254,253,252) | JPG, PNG, TIFF, WebP, BMP и  |

### `/admin/virtual_depot` — 3 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **2.03:1** | strana | `small.text-warning` | rgb(122, 60, 0) → rgb(25,25,44) | Кликни на екран да почнеш |
| **2.61:1** | dropdown | `a.dropdown-item.dropdown-toggle-submenu` | rgb(60, 117, 97) → rgb(53,41,29) | Биологија |

### `/dokumenti` — 2 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **2.61:1** | dropdown | `a.dropdown-item.dropdown-toggle-submenu` | rgb(60, 117, 97) → rgb(53,41,29) | Биологија |

### `/dokumenti/odobravanje` — 2 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **2.61:1** | dropdown | `a.dropdown-item.dropdown-toggle-submenu` | rgb(60, 117, 97) → rgb(53,41,29) | Биологија |

### `/zahtevi/odobravanje` — 2 корена

| однос | где | селектор | fg → bg | текст |
|---|---|---|---|---|
| **1:1** | strana | `#navbarDropdown` | rgb(255, 255, 255) → rgb(255,255,255) | System Administrator |
| **2.61:1** | dropdown | `a.dropdown-item.dropdown-toggle-submenu` | rgb(60, 117, 97) → rgb(53,41,29) | Биологија |
