# static/udzbenik/ — мотор интерактивног уџбеника

Bundle долази из репоа **mis-udzbenik** (`scripts/izgradi-u-mis.sh` тамо гради
Vite/Three.js мотор и копира `udzbenik.js`, chunk-ове `udzbenik-jezgro-<хеш>.js`,
`udzbenik-three-<хеш>.js`, `udzbenik-dijagrami-<хеш>.js`, `udzbenik.css`,
`rezerve/*.png` и `VERZIJA.txt` овде; старе `udzbenik-*.js` брише).
Све то иде у git (изузеци у .gitignore). **Не уређивати ручно** — свака ручна
измена нестаје при следећој изградњи.

Chunk-ове `udzbenik.js` увози релативно од `import.meta.url` и **без `?v=`** —
зато носе хеш садржаја у имену (од мотора 07dc3ea, 09.11.2026). Пре тога су
имена била фиксна и кеширани стари chunk уз нов `udzbenik.js` је заустављао
уџбеник на „Учитавање…“. Улаз `udzbenik.js` и даље не сме бити immutable
(видети `location ~ ^/static/udzbenik/.*\.js$` у `nginx_museum.conf`).

Док мотор није изграђен, `udzbenik.js` је привремени чувар места који у
`#udzbenik-app` испише да мотор још није изграђен, а `VERZIJA.txt` садржи
`nema`. Уговор између мотора и сервера: `/tmp/udzbenik/BRIF-ANTIGRAVITY.md`
(§3 монтирање, §4 API), шема садржаја: `udzbenik/schema/lekcija.schema.json`.
