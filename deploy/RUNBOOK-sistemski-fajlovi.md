# Усклађивање системских фајлова на проду са репоом

Стање 17.08.2026. `deploy.sh` при сваком деплоју испише 8 упозорења да се
системски фајлови на проду разликују од репо копија и да их **не преписује**.
То понашање је исправно и остаје. Овај документ каже шта се са тим ради.

## Шта је ту заправо

Репо копије **нису опис продукције** него непримењена августовска прерада.
Прод ради јулске оригинале:

| фајл | прод | репо | разлика |
|---|---|---|---|
| `/etc/systemd/system/backup-nhmb.service` | 2. јул, 102 B | 10. авг, 643 B | репо додаје `OnFailure=`, `After/Wants=postgresql`, `Nice`, `IOSchedulingClass` |
| `/etc/systemd/system/backup-nhmb.timer` | 2. јул, 130 B | 10. авг, 207 B | само коментар |
| `/etc/systemd/system/restore-proba.service` | 22. јул, 178 B | 10. авг, 584 B | репо додаје `OnFailure=` и зависности |
| `/etc/systemd/system/restore-proba.timer` | 22. јул, 134 B | 10. авг, 235 B | само коментар |
| `/etc/systemd/system/mis-fototeka-worker.service` | 9. јул, 799 B | 10. авг, 758 B | **само коментар** — понашање идентично |
| `/etc/nginx/conf.d/mis.conf` | 16. јул, 1269 B | 10. авг, 6274 B | репо додаје ограничење приступа, rate limiting, забрану `.env`/`.py` |
| `/usr/local/bin/backup-nhmb.sh` | 9. јул, 1486 B | 12. авг, 5040 B | нечитљиво без root-а — **упоредити пре одлуке** |
| `/usr/local/bin/restore-proba.sh` | 22. јул, 2255 B | 12. авг, 3070 B | 131 линија разлике |

## Мине проверене 17.08.2026

1. **Репо nginx конф је показивао на непостојеће сертификате**
   (`/etc/pki/tls/certs/museum_cert.pem`). Прод користи `/etc/pki/nginx/mis.crt`.
   Копирање старе верзије оборило би `nginx -t`, дакле и reload. **Исправљено
   у репоу**, али то значи да ниједна од ових копија није испробана на проду.
2. **`mis-alarm@.service` је слао мејл, а на проду нема MTA** — нема `mail`,
   `mailx` ни `s-nail`, postfix неактиван. `OnFailure=mis-alarm@%n.service`
   без тога само ствара утисак да неко гледа. Јединица је зато преправљена
   да **пише маркер** у `/var/lib/mis/alarm/`, а мејл шаље само ако `mail`
   постоји. Маркере чита дневна провера са dev-а
   (`scripts/nadzor/provera_proda.py`).

## Провера која НЕ чека ово

Дневни надзор са dev машине већ ради (тајмер `mis-nadzor.timer`, 08:00) и
покрива свежину бекапа, пале јединице, простор и здравље апликације — без
иједне измене на проду. Инсталација јединица испод додаје једино хватање
пада који је у међувремену ручно поправљен.

## Корак 1 — systemd јединице (безопасно)

`sudo` без лозинке имам само за `deploy.sh` и `psql`, па ово покреће
Александар. Прво снимак постојећег стања:

```bash
sudo mkdir -p /root/pre-usklađivanja-2026-08-17
sudo cp -a /etc/systemd/system/backup-nhmb.{service,timer} \
           /etc/systemd/system/restore-proba.{service,timer} \
           /etc/systemd/system/mis-alarm@.service \
           /root/pre-usklađivanja-2026-08-17/
```

Затим инсталација и провера:

```bash
cd /opt/mis/app
sudo cp deploy/backup-nhmb.service deploy/backup-nhmb.timer \
        deploy/restore-proba.service deploy/restore-proba.timer \
        deploy/mis-alarm@.service /etc/systemd/system/
sudo systemd-analyze verify /etc/systemd/system/backup-nhmb.service \
                            /etc/systemd/system/restore-proba.service \
                            /etc/systemd/system/mis-alarm@.service
sudo systemctl daemon-reload
systemctl list-timers backup-nhmb.timer restore-proba.timer --no-pager
```

Доказ да аларм стварно ради (намерно обори јединицу):

```bash
sudo systemctl start mis-alarm@proba.service
ls -l /var/lib/mis/alarm/
```

Мора да се појави фајл. Ако га нема — јединица је намерно направљена да
падне, па ће `systemctl is-failed mis-alarm@proba.service` рећи `failed`,
и следећа јутарња провера са dev-а то пријави.

**Повратак**, ако нешто не ваља:

```bash
sudo cp -a /root/pre-usklađivanja-2026-08-17/. /etc/systemd/system/
sudo systemctl daemon-reload
```

## Корак 2 — nginx (посебан термин, не уз деплој)

Ово мења ко сме да приђе апликацији: репо конф пушта само `127.0.0.1`,
`192.168.144.0/24` и `100.64.0.0/10` (Tailscale), све остало одбија. Пре
примене проверити да ниједан корисник не долази са неке треће адресе.

```bash
sudo cp -a /etc/nginx/conf.d/mis.conf /root/pre-usklađivanja-2026-08-17/
sudo cp /opt/mis/app/deploy/nginx_museum_prod.conf /etc/nginx/conf.d/mis.conf
sudo nginx -t                     # МОРА да прође; ако не — врати и стани
sudo systemctl reload nginx
curl -sk https://127.0.0.1/healthz
```

Повратак:

```bash
sudo cp -a /root/pre-usklađivanja-2026-08-17/mis.conf /etc/nginx/conf.d/mis.conf
sudo nginx -t && sudo systemctl reload nginx
```

## Корак 3 — две скрипте у /usr/local/bin

`backup-nhmb.sh` се не може ни прочитати без root-а (`-rwxr-x--- root root`),
па поређење ради Александар:

```bash
sudo diff -u /opt/mis/app/deploy/backup-nhmb.sh /usr/local/bin/backup-nhmb.sh
sudo diff -u /opt/mis/app/deploy/restore-proba.sh /usr/local/bin/restore-proba.sh
```

Ово је једини од три корака где **прод примерак може бити тачнији** — репо
верзије су по опису „реконструисане по понашању". Бекап ради и његов излаз је
проверен, па нема разлога да се дира док се разлика не прочита ред по ред.

## Корак 4 — да се ово више не понавља

`deploy.sh` треба да задржи правило „никад тихо не преписуј", али упозорење
да постане прави `diff`, а примена системских фајлова засебна изричита
наредба. Деплој кода не сме успут да мења инфраструктуру.
