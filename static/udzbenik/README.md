# static/udzbenik/ — мотор интерактивног уџбеника

Bundle долази из репоа **mis-udzbenik** (`scripts/izgradi-u-mis.sh` тамо гради
Vite/Three.js мотор и копира `udzbenik.js`, `udzbenik.css`, `rezerve/*.png` и
`VERZIJA.txt` овде). **Не уређивати ручно** — свака ручна измена нестаје при
следећој изградњи.

Док мотор није изграђен, `udzbenik.js` је привремени чувар места који у
`#udzbenik-app` испише да мотор још није изграђен, а `VERZIJA.txt` садржи
`nema`. Уговор између мотора и сервера: `/tmp/udzbenik/BRIF-ANTIGRAVITY.md`
(§3 монтирање, §4 API), шема садржаја: `udzbenik/schema/lekcija.schema.json`.
