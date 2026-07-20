"""Pure (Flask-free) helpers for the Конзерваторско-рестаураторски досије module.

Kept separate from `kr_dosije_views.py` so the CLI importer and the unit tests
can import the parsing/format logic without pulling in Flask or a request
context. Anything here is either pure Python or takes an open DB cursor.
"""

import re
import unicodedata
from datetime import date


# ---------------------------------------------------------------------------
# Labels / enums
# ---------------------------------------------------------------------------
ODELJENJE_LABELS = {
    'geo': 'Геолошко одељење',
    'bio': 'Биолошко одељење',
}

# Фаза фотографије (стара конвенција: сл. а/б/в).
FAZA_LABELS = {
    'pre': 'Пре радова',
    'tokom': 'Током радова',
    'posle': 'После радова',
}
FAZA_REDOSLED = {'pre': 0, 'tokom': 1, 'posle': 2}

# Врста предлошка = које поље описа попуњава.
VRSTA_LABELS = {
    'pre': 'Опис стања пре радова',
    'postupak': 'Опис поступка и материјала',
    'posle': 'Опис стања након радова',
}

# Слово у имену датотеке → фаза. Ћирилица и латиница (уноси мешају писма).
_SLOVO_U_FAZU = {
    'а': 'pre', 'a': 'pre',
    'б': 'tokom', 'b': 'tokom',
    'в': 'posle', 'v': 'posle',
}


# ---------------------------------------------------------------------------
# Одељење
# ---------------------------------------------------------------------------
def department_to_odeljenje(department):
    """Мапирај текст одељења из сесије/директоријума на 'geo'/'bio'.

    Прима нпр. 'ГЕОЛОШКО ОДЕЉЕЊЕ' или 'Биолошко одељење'. Враћа None ако се
    не препознаје (нпр. администрација) — позивалац одлучује шта тада.
    """
    if not department:
        return None
    d = department.strip().lower()
    if d.startswith('геол') or 'геолош' in d:
        return 'geo'
    if d.startswith('биол') or 'биолош' in d:
        return 'bio'
    return None


# ---------------------------------------------------------------------------
# Инвентарни / колекторски бројеви (за поклапање слика са досијеом)
# ---------------------------------------------------------------------------
def normalize_broj(value):
    """Сведи број предмета на канонски облик за поклапање.

    Уклања ознаке ('сл.', 'Col.', 'Кол.', 'М'/'M', 'Инв.бр.'), размаке и
    сепараторе. '/' и '-' се БРИШУ јер их извори мешају ('УШ 85/643' у Excel-у
    ↔ 'УШ 85-643' у имену датотеке). Празно → ''.
    """
    if value is None:
        return ''
    s = str(value)
    # Уклони очигледне ознаке које нису део самог броја.
    s = re.sub(r'(?i)\b(сл\.?|col\.?|кол\.?|инв\.?\s*бр\.?|ред\.?\s*број|радни\s*број(?:еви)?)',
               ' ', s)
    s = s.replace('.', ' ')
    # Ћирилично М (U+041C/U+043C) и латинично M на почетку броја су иста ствар.
    s = s.strip()
    s = re.sub(r'(?i)^[МMмm]\s*(?=\d)', '', s)
    # Задржи слова (УШ, A) и цифре; сепаратори (/, -) и остало отпадају.
    s = re.sub(r'[^0-9A-Za-zА-Яа-я]', '', s)
    return s.upper()


# ---------------------------------------------------------------------------
# Период извршења (колона I — неуједначена проза)
# ---------------------------------------------------------------------------
_DATUM_RE = re.compile(r'(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})')


def parse_period(text):
    """Извуци (period_od, period_do) из прозе типа
    'у периоду од 23.12.2022. године до 07.01.2023. године' или 'дана 06.09.2023'.

    Први датум = од, последњи = до. Ако је само један, од==до. Ако нема ниједног,
    (None, None). Неисправни датуми се прескачу. Не покушава да исправи логички
    обрнуте опсеге (у изворним подацима их има) — само их пренесе.
    """
    if not text:
        return None, None
    datumi = []
    for d, m, y in _DATUM_RE.findall(str(text)):
        try:
            datumi.append(date(int(y), int(m), int(d)))
        except ValueError:
            continue
    if not datumi:
        return None, None
    return datumi[0], datumi[-1]


# ---------------------------------------------------------------------------
# Извршиоци (колона H — проза, понекад више особа)
# ---------------------------------------------------------------------------
def parse_izvrsioci(text, known_users):
    """Из прозе о лицу које је вршило радове извуци листу извршилаца.

    `known_users` = листа (email, full_name). Свако познато пуно име нађено у
    тексту постаје извршилац са email-ом. Ако ниједан налог није поклопљен,
    враћа једног извршиоца са сировим (скраћеним) текстом и без email-а —
    да се податак не изгуби. Резултат: листа {'user_email', 'ime_tekst'}.
    """
    result = []
    seen_emails = set()
    if text:
        haystack = _strip_accents_lower(text)
        for email, full_name in known_users:
            if not full_name:
                continue
            if _strip_accents_lower(full_name) in haystack and email not in seen_emails:
                result.append({'user_email': email, 'ime_tekst': full_name})
                seen_emails.add(email)
    if not result and text:
        result.append({'user_email': None, 'ime_tekst': _sazmi_ime(text)})
    return result


def _sazmi_ime(text):
    """Скрати прозу о извршиоцу на нешто налик имену за приказ (fallback кад
    нема поклопљеног налога): узми део пре прве запете, без уводне фразе."""
    s = ' '.join(str(text).split())
    s = re.sub(r'(?i)^.*?изврш(?:ио|ила|или)\s+(?:је\s+)?', '', s)
    s = re.sub(r'(?i)^.*?извршен[оа]?\s+(?:је\s+)?', '', s)
    s = s.split(',')[0].strip(' .-')
    return s[:200] if s else ' '.join(str(text).split())[:200]


def _strip_accents_lower(s):
    nfkd = unicodedata.normalize('NFKD', str(s))
    return ''.join(c for c in nfkd if not unicodedata.combining(c)).lower()


# ---------------------------------------------------------------------------
# Имена датотека фотографија (parser сл. а/б/в = pre/tokom/posle)
# ---------------------------------------------------------------------------
# Изолован маркер фазе: једно слово а/б/в (ћир) или a/b/v (лат), окружено
# не-словима (тачка, размак, заграда, цифра, крај). Тиме се избегавају слова
# унутар речи ('бизона', 'Врчин').
_FAZA_MARKER_RE = re.compile(
    r'(?<![0-9A-Za-zА-Яа-я])\d{0,2}([абвАБВabvABV])(?![A-Za-zА-Яа-я0-9])'
)


def parse_image_filename(filename):
    """Рашчлани име датотеке фотографије из старог система.

    Враћа {'broj_norm', 'broj_raw', 'faza'} ако се могу извући и број предмета
    и фаза; иначе None (позивалац то пријави као непоклопљено — не погађа се).

    Примери:
      'сл. 771.в.jpg'                  -> 771 / posle
      '(Сл.Col.072022. a).png'         -> 072022 / pre
      '(сл.М1989 .а).jpeg'             -> М1989 / pre
      '(Сл.Col.A 168 в) рог бизона).jpg' -> A168 / posle
      'Доделиће се касније 1.jpg'      -> None (нема фазе)
    """
    if not filename:
        return None
    stem = re.sub(r'\.[A-Za-z]{2,4}$', '', filename).strip()
    faza = _extract_faza(stem)
    if faza is None:
        return None
    broj_raw = _extract_broj_from_name(stem)
    broj_norm = normalize_broj(broj_raw)
    if not broj_norm:
        return None
    return {'broj_norm': broj_norm, 'broj_raw': broj_raw.strip(), 'faza': faza}


def _extract_faza(stem):
    """Нађи маркер фазе. Бирамо ПОСЛЕДЊИ изолован а/б/в — код ових имена он
    стоји иза броја предмета ('Col.A 168 а'), где би прво 'A' био део броја."""
    faza = None
    for m in _FAZA_MARKER_RE.finditer(stem):
        slovo = m.group(1).lower()
        # 'в' се преклапа ћир/лат; мапа то решава. 'A' велико латинично унутар
        # броја ('A 168') неће проћи јер иза њега иде размак па цифра — али
        # _FAZA_MARKER_RE тражи да иза НЕ иде слово; иза 'A' иде размак → пролази.
        # Зато памтимо последњи маркер: стварни маркер фазе је на крају.
        if slovo in _SLOVO_U_FAZU:
            faza = _SLOVO_U_FAZU[slovo]
    return faza


def _extract_broj_from_name(stem):
    """Извуци сирови део са бројем предмета из имена (пре маркера фазе)."""
    # Одсеци део од последњег маркера фазе надаље — број је пре њега.
    markers = list(_FAZA_MARKER_RE.finditer(stem))
    head = stem[:markers[-1].start()] if markers else stem
    return _first_broj_token(head)


def _first_broj_token(text):
    """Први „број предмета" из произвољног текста: 'Col.XXX', 'М XXXX',
    'УШ 85/643', 'A 168' или голи број. Празно ако нема цифре."""
    # 'Col.XXX' / 'Кол.XXX' / 'Инв.бр.XXX' праћено бројем (уз опц. слова префикс).
    m = re.search(
        r'(?i)(?:col\.?|кол\.?|инв\.?\s*бр\.?)\s*([A-Za-zА-Яа-я]{0,3}\s?\d[\d/\-\s]*)',
        text,
    )
    if m:
        return m.group(1)
    m = re.search(r'(?i)([МMмm]\s?\d[\d/\-]*)', text)
    if m:
        return m.group(1)
    m = re.search(r'([A-Za-zА-Яа-я]{0,3}\s?\d[\d/\-]{1,})', text)
    if m:
        return m.group(1)
    return ''


def broj_key_from_text(text):
    """Нормализовани кључ броја предмета из неуредне Excel ћелије (B/C).

    Извлачи водећи број-токен (игноришући пратећу прозу типа
    'Col.898 Фосилни материјал…') па га нормализује. Празно кад нема броја
    (нпр. 'Овај примерак не поседује колекторски број…')."""
    return normalize_broj(_first_broj_token(str(text))) if text else ''


# ---------------------------------------------------------------------------
# Евиденциони број (КР-ГЕО-2026-001) — узима отворен курсор
# ---------------------------------------------------------------------------
ODELJENJE_PREFIX = {'geo': 'ГЕО', 'bio': 'БИО'}


def next_evidencioni_broj(cur, odeljenje, year):
    """Следећи слободан евиденциони број за одељење и годину.

    Формат КР-<ГЕО|БИО>-<година>-<NNN>, редни број се ресетује сваке године.
    Рачуна се као max(постојећи суфикс)+1 за дати префикс, па је отпоран на
    обрисане редове. Позива се унутар трансакције која одмах уписује ред;
    UNIQUE(evidencioni_broj) хвата евентуалну трку.
    """
    prefix = f'КР-{ODELJENJE_PREFIX[odeljenje]}-{year}-'
    cur.execute(
        """
        SELECT evidencioni_broj FROM kr_dosije
        WHERE evidencioni_broj LIKE %s
        """,
        (prefix + '%',),
    )
    max_n = 0
    for (broj,) in cur.fetchall():
        suf = broj[len(prefix):]
        if suf.isdigit():
            max_n = max(max_n, int(suf))
    return f'{prefix}{max_n + 1:03d}'
