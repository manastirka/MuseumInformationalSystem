"""Shared curator collection bootstrap data and lazy loader helpers."""

import logging


logger = logging.getLogger(__name__)


_PHASE3A_COLLECTION_LOADERS = {
    'botany': 'get_botany_collection',
    'ichthyology': 'get_ichthyology_collection',
    'entomology': 'get_entomology_collection',
    'mycology': 'get_mycology_collection',
    'herpetology': 'get_herpetology_collection',
    'ornithology': 'get_ornithology_collection',
    'paleozoology': 'get_paleozoology_collection',
    'paleobotany': 'get_paleobotany_collection',
    'petrology': 'get_petrology_collection',
}


BOTANY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'BOT-2024-001',
            'scientific_name': 'Pančić Omorika (Picea omorika)',
            'common_name_sr': 'Панчићева оморика',
            'family': 'Pinaceae',
            'location_found': 'Тара, Србија',
            'altitude': '800-1600m',
            'date_collected': '2023-06-15',
            'collector': 'Др М. Никетић',
            'herbarium_number': 'BEOU-40001',
            'condition': 'Одлично',
            'endemic_status': 'Ендемична врста Србије',
            'conservation_status': 'Угрожена (EN)',
            'description': 'Ендемична четинарска врста Србије. Реликтна врста из терцијара.',
            'curator': 'mniketic@nhmbeo.rs'
        },
        {
            'catalog_number': 'BOT-2024-002',
            'scientific_name': 'Ramonda serbica',
            'common_name_sr': 'Српска рамонда (Наталијина рамонда)',
            'family': 'Gesneriaceae',
            'location_found': 'Сува планина, Србија',
            'altitude': '400-1800m',
            'date_collected': '2023-05-10',
            'collector': 'Др А. Савић',
            'herbarium_number': 'BEOU-40002',
            'condition': 'Одлично',
            'endemic_status': 'Балкански ендем',
            'conservation_status': 'Ретка',
            'description': 'Реликтна биљка способна за анабиозу. Национални симбол Србије.',
            'curator': 'aleksandra.savic@nhmbeo.rs'
        },
        {
            'catalog_number': 'BOT-2024-003',
            'scientific_name': 'Lilium bosniacum',
            'common_name_sr': 'Босански љиљан',
            'family': 'Liliaceae',
            'location_found': 'Копаоник, Србија',
            'altitude': '1200-2000m',
            'date_collected': '2022-07-20',
            'collector': 'В. Стојановић',
            'herbarium_number': 'BEOU-38547',
            'condition': 'Добро',
            'endemic_status': 'Балкански ендем',
            'conservation_status': 'Заштићена',
            'description': 'Ретка врста планинског љиљана са Балкана.',
            'curator': 'verica.stojanovic@nhmbeo.rs'
        },
        {
            'catalog_number': 'BOT-2024-004',
            'scientific_name': 'Acer heldreichii',
            'common_name_sr': 'Хелдрајхов јавор',
            'family': 'Sapindaceae',
            'location_found': 'Проклетије, Србија',
            'altitude': '1000-1800m',
            'date_collected': '2023-09-12',
            'collector': 'Др М. Несторовић',
            'herbarium_number': 'BEOU-39221',
            'condition': 'Одлично',
            'endemic_status': 'Балкански ендем',
            'conservation_status': 'Ретка',
            'description': 'Врста јавора карактеристична за Балканско полуострво.',
            'curator': 'marko.nestorovic@nhmbeo.rs'
        },
        {
            'catalog_number': 'BOT-2024-005',
            'scientific_name': 'Paeonia tenuifolia',
            'common_name_sr': 'Божур',
            'family': 'Paeoniaceae',
            'location_found': 'Фрушка гора, Србија',
            'altitude': '200-400m',
            'date_collected': '2023-04-28',
            'collector': 'Др М. Никетић',
            'herbarium_number': 'BEOU-39845',
            'condition': 'Одлично',
            'endemic_status': 'Аутохтона',
            'conservation_status': 'Строго заштићена',
            'description': 'Ретка степска биљка са црвеним цветовима.',
            'curator': 'mniketic@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 5,
        'endemic_species': 4,
        'threatened_species': 3,
        'herbarium_size': '>40,000'
    }
}

ICHTHYOLOGY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'ICH-2024-001',
            'scientific_name': 'Acipenser ruthenus',
            'common_name_sr': 'Кечига',
            'family': 'Acipenseridae',
            'location_found': 'Дунав, Србија',
            'habitat': 'Слатководна',
            'date_collected': '2022-08-15',
            'length_cm': 85,
            'weight_kg': 4.5,
            'age_estimated': '12 година',
            'condition': 'Одличан препарат',
            'conservation_status': 'Критично угрожена (CR)',
            'description': 'Јесетра из породице Acipenseridae. Извор кавијара. Део изложбе "Kavijar".',
            'curator': 'dubravka.vucic@nhmbeo.rs'
        },
        {
            'catalog_number': 'ICH-2024-002',
            'scientific_name': 'Hucho hucho',
            'common_name_sr': 'Младица',
            'family': 'Salmonidae',
            'location_found': 'Лим, Србија',
            'habitat': 'Брзе планинске реке',
            'date_collected': '2023-05-22',
            'length_cm': 120,
            'weight_kg': 18,
            'age_estimated': '8 година',
            'condition': 'Добар препарат',
            'conservation_status': 'Угрожена (EN)',
            'description': 'Највећа врста пастрмке у Европи. Ендемична за дунавски слив.',
            'curator': 'dubravka.vucic@nhmbeo.rs'
        },
        {
            'catalog_number': 'ICH-2024-003',
            'scientific_name': 'Zingel balcanicus',
            'common_name_sr': 'Вретенар',
            'family': 'Percidae',
            'location_found': 'Вардар, Србија',
            'habitat': 'Брзотекуће воде',
            'date_collected': '2021-09-10',
            'length_cm': 18,
            'weight_kg': 0.15,
            'age_estimated': '3 године',
            'condition': 'Одличан препарат',
            'conservation_status': 'Угрожена (EN)',
            'description': 'Балкански ендем. Карактеристичне зебрасте пруге.',
            'curator': 'dubravka.vucic@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 3,
        'endangered_species': 3,
        'endemic_species': 2
    }
}

ENTOMOLOGY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'ENT-OD-001',
            'scientific_name': 'Calopteryx virgo',
            'common_name_sr': 'Девојачка виленица',
            'order': 'Odonata',
            'family': 'Calopterygidae',
            'location_found': 'Ђердап, Србија',
            'date_collected': '2023-06-18',
            'sex': 'мужјак',
            'wingspan_mm': 65,
            'condition': 'Одличан препарат',
            'part_of_collection': 'Balkan OdoBase',
            'description': 'Модра виленица са металним сјајем. Индикатор чистих вода.',
            'curator': 'milos.jovic@nhmbeo.rs'
        },
        {
            'catalog_number': 'ENT-LEP-001',
            'scientific_name': 'Parnassius apollo',
            'common_name_sr': 'Аполонов лептир',
            'order': 'Lepidoptera',
            'family': 'Papilionidae',
            'location_found': 'Стара планина, Србија',
            'date_collected': '2022-07-05',
            'sex': 'женка',
            'wingspan_mm': 75,
            'condition': 'Одличан препарат',
            'conservation_status': 'Строго заштићена',
            'description': 'Ретка планинска врста лептира. Заштићена на нивоу Европе.',
            'curator': 'aleksandar@nhmbeo.rs'
        },
        {
            'catalog_number': 'ENT-COL-001',
            'scientific_name': 'Rosalia alpina',
            'common_name_sr': 'Алпски стрижибуба',
            'order': 'Coleoptera',
            'family': 'Cerambycidae',
            'location_found': 'Шар планина, Србија',
            'date_collected': '2023-08-14',
            'sex': 'мужјак',
            'length_mm': 38,
            'condition': 'Одличан препарат',
            'conservation_status': 'Заштићена',
            'description': 'Велика плаво-црна буба дугорог. Живи на старим буквама.',
            'curator': 'milos.jovic@nhmbeo.rs'
        },
        {
            'catalog_number': 'ENT-HYM-001',
            'scientific_name': 'Bombus terrestris',
            'common_name_sr': 'Земни бумбар',
            'order': 'Hymenoptera',
            'family': 'Apidae',
            'location_found': 'Авала, Србија',
            'date_collected': '2023-05-20',
            'sex': 'радилица',
            'length_mm': 22,
            'condition': 'Добар препарат',
            'conservation_status': 'Није угрожена',
            'description': 'Најчешћа врста бумбара у Србији. Важан опрашивач.',
            'curator': 'aleksandar@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 4,
        'odonata_collection': 1,
        'total_species_exhibited': '1,710+'
    }
}

MYCOLOGY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'MYC-2024-001',
            'scientific_name': 'Tuber petrophilum',
            'common_name_sr': 'Српски тартуф',
            'family': 'Tuberaceae',
            'location_found': 'Источна Србија',
            'habitat': 'Кречњачко тло, храстове шуме',
            'date_collected': '2014-10-12',
            'diameter_cm': 4.5,
            'weight_g': 35,
            'condition': 'Конзервиран',
            'type_status': 'Холотип',
            'description': 'Нова врста тартуфа описана од др Б. Иванчевића. Објављена у Mycotaxon 2014.',
            'curator': 'boris@nhmbeo.rs'
        },
        {
            'catalog_number': 'MYC-2024-002',
            'scientific_name': 'Amanita muscaria',
            'common_name_sr': 'Мухомор',
            'family': 'Amanitaceae',
            'location_found': 'Златибор, Србија',
            'habitat': 'Четинарске шуме',
            'date_collected': '2023-09-18',
            'diameter_cm': 12,
            'condition': 'Добар препарат',
            'toxicity': 'Отровна',
            'description': 'Класичан црвени мухомор са белим тачкама. Симбионт четинара.',
            'curator': 'boris@nhmbeo.rs'
        },
        {
            'catalog_number': 'MYC-2024-003',
            'scientific_name': 'Boletus edulis',
            'common_name_sr': 'Вргањ',
            'family': 'Boletaceae',
            'location_found': 'Голија, Србија',
            'habitat': 'Мешовите шуме',
            'date_collected': '2023-10-05',
            'diameter_cm': 18,
            'weight_g': 450,
            'condition': 'Одличан препарат',
            'edibility': 'Јестива',
            'description': 'Јестива гљива високог квалитета. Симбионт храста и четинара.',
            'curator': 'boris@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 3,
        'new_species_described': 1,
        'research_years': '30+'
    }
}

HERPETOLOGY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'HERP-AMP-001',
            'scientific_name': 'Salamandra salamandra',
            'common_name_sr': 'Обична саламандерица',
            'class': 'Amphibia',
            'order': 'Caudata',
            'family': 'Salamandridae',
            'location_found': 'Фрушка гора, Србија',
            'habitat': 'Влажне листопадне шуме',
            'date_collected': '2022-04-15',
            'length_cm': 18,
            'sex': 'женка',
            'condition': 'Одличан препарат',
            'conservation_status': 'Заштићена',
            'description': 'Црно-жута саламандерица. Индикатор здравих шумских екосистема.',
            'curator': 'ana.paunovic@nhmbeo.rs'
        },
        {
            'catalog_number': 'HERP-REP-001',
            'scientific_name': 'Vipera ammodytes',
            'common_name_sr': 'Поскок',
            'class': 'Reptilia',
            'order': 'Squamata',
            'family': 'Viperidae',
            'location_found': 'Суве планине, Србија',
            'habitat': 'Камењари, сунчани терени',
            'date_collected': '2021-06-22',
            'length_cm': 72,
            'sex': 'мужјак',
            'condition': 'Одличан препарат',
            'venomous': 'Да - отровна',
            'conservation_status': 'Заштићена',
            'description': 'Најотровнија европска змија. Карактеристични рог на њушци.',
            'curator': 'ana.paunovic@nhmbeo.rs'
        },
        {
            'catalog_number': 'HERP-AMP-002',
            'scientific_name': 'Bombina variegata',
            'common_name_sr': 'Жутотрба бумбарка',
            'class': 'Amphibia',
            'order': 'Anura',
            'family': 'Bombinatoridae',
            'location_found': 'Вршачке планине, Србија',
            'habitat': 'Планинске баре и потоци',
            'date_collected': '2023-05-10',
            'length_cm': 4.5,
            'sex': 'женка',
            'condition': 'Добар препарат',
            'conservation_status': 'Осетљива',
            'description': 'Мала жаба са жутим трбухом. Живи у чистим планинским водама.',
            'curator': 'ana.paunovic@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 3,
        'amphibians': 2,
        'reptiles': 1,
        'field_research_years': '20+'
    }
}

ORNITHOLOGY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'ORN-2024-001',
            'scientific_name': 'Aquila chrysaetos',
            'common_name_sr': 'Крсташ (Сури орао)',
            'order': 'Accipitriformes',
            'family': 'Accipitridae',
            'location_found': 'Увац, Србија',
            'habitat': 'Планинске стене',
            'date_collected': '2020-11-08',
            'wingspan_cm': 220,
            'weight_kg': 4.8,
            'sex': 'женка',
            'ring_number': 'EURING-SRB-12458',
            'condition': 'Одличан препарат',
            'conservation_status': 'Строго заштићена',
            'description': 'Највећа грабљивица Србије. Симбол планинских предела.',
            'curator': 'vuk.popic@nhmbeo.rs'
        },
        {
            'catalog_number': 'ORN-2024-002',
            'scientific_name': 'Ciconia nigra',
            'common_name_sr': 'Црна рода',
            'order': 'Ciconiiformes',
            'family': 'Ciconiidae',
            'location_found': 'Обедска бара, Србија',
            'habitat': 'Мочваре и влажне шуме',
            'date_collected': '2021-07-14',
            'wingspan_cm': 185,
            'weight_kg': 3.2,
            'sex': 'мужјак',
            'ring_number': 'EURING-SRB-13201',
            'condition': 'Добар препарат',
            'conservation_status': 'Заштићена',
            'description': 'Ретка врста роде. Гнезди у старим шумама.',
            'curator': 'vuk.popic@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 2,
        'ringed_birds': 2,
        'euring_program': 'Активан'
    }
}

PALEOZOOLOGY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'PALEO-DINO-001',
            'scientific_name': 'Theropoda indet.',
            'common_name_sr': 'Зуб теропода',
            'taxon_group': 'Dinosauria',
            'geological_period': 'Горња креда',
            'age_million_years': 70,
            'location_found': 'Пирот, Србија',
            'date_discovered': '2019-08-12',
            'discoverers': 'Др З. Марковић, М. Миливојевић',
            'specimen_type': 'Зуб',
            'length_cm': 4.2,
            'condition': 'Добро очуван',
            'significance': 'Први фосил диносауруса у Србији',
            'description': 'Зуб месоједног диносауруса. Историјско откриће за српску палеонтологију.',
            'publication': 'Објављен у међународном часопису 2020',
            'curator': 'zoran.markovic@nhmbeo.rs'
        },
        {
            'catalog_number': 'PALEO-PROB-001',
            'scientific_name': 'Deinotherium giganteum',
            'common_name_sr': 'Деинотеријум (праисторијски слон)',
            'taxon_group': 'Proboscidea',
            'geological_period': 'Миоцен',
            'age_million_years': 10,
            'location_found': 'Белград, Србија',
            'date_discovered': '2015-03-20',
            'discoverers': 'С. Алабурић',
            'specimen_type': 'Кљова',
            'length_cm': 95,
            'condition': 'Одлично очуван',
            'exhibition': 'Surlaši - divovi prošlosti',
            'description': 'Кљова праисторијског слона. Део изложбе о сурлашима.',
            'curator': 'sanja.pavic@nhmbeo.rs'
        },
        {
            'catalog_number': 'PALEO-MOLL-001',
            'scientific_name': 'Viviparus serbicus',
            'common_name_sr': 'Српски живороднi пуж',
            'taxon_group': 'Mollusca',
            'geological_period': 'Миоцен',
            'age_million_years': 15,
            'location_found': 'Алексинац, Србија',
            'date_discovered': '2018-09-05',
            'discoverers': 'Др Б. Митровић',
            'specimen_type': 'Љушт ура',
            'length_cm': 3.5,
            'condition': 'Одлично очуван',
            'type_status': 'Нова врста за науку',
            'description': 'Фосилни слатководни пуж из миоцена. Описан од др Б. Митровић.',
            'curator': 'biljana.mitrovic@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 3,
        'dinosaur_fossils': 1,
        'exhibitions': 'Evolucija, Surlaši, Ledeno doba, Fosilizacija'
    }
}

PALEOBOTANY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'PBOT-2024-001',
            'scientific_name': 'Pteridium aquilinum (fossil)',
            'common_name_sr': 'Окамењена папрат',
            'geological_period': 'Карбон',
            'age_million_years': 300,
            'location_found': 'Алексинац, Србија',
            'date_discovered': '2019-06-10',
            'specimen_type': 'Лист (отисак)',
            'length_cm': 18,
            'width_cm': 12,
            'condition': 'Одлично очуван',
            'description': 'Окамењени лист древне папрати из каменоугљеног периода.',
            'curator': 'desadjm@nhmbeo.rs'
        },
        {
            'catalog_number': 'PBOT-2024-002',
            'scientific_name': 'Quercus sp. (fossil)',
            'common_name_sr': 'Фосилни храст',
            'geological_period': 'Неоген',
            'age_million_years': 8,
            'location_found': 'Мељак, Србија',
            'date_discovered': '2020-08-22',
            'specimen_type': 'Лист и жир',
            'length_cm': 14,
            'width_cm': 8,
            'condition': 'Добро очуван',
            'description': 'Фосилни лист и жир храста из неогена. Део истраживања праисторијске вегетације.',
            'curator': 'desadjm@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 2,
        'curator_since': 1993,
        'role': 'Профессор палеоекологије'
    }
}

PETROLOGY_FALLBACK = {
    'specimens': [
        {
            'catalog_number': 'PETR-2024-001',
            'rock_name': 'Гранит',
            'scientific_name': 'Granite',
            'rock_type': 'Магматска стена',
            'location_found': 'Букуља, Србија',
            'geological_age': 'Палеоген',
            'date_collected': '2021-05-18',
            'minerals_present': 'Кварц, фелдспат, слуда',
            'texture': 'Грубозрна',
            'color': 'Светло сива',
            'weight_kg': 2.5,
            'dimensions_cm': '15x12x8',
            'condition': 'Одличан узорак',
            'description': 'Типичан гранит са великим кристалима. Користи се у градњи.',
            'curator': 'tatjana.milicbabic@nhmbeo.rs'
        },
        {
            'catalog_number': 'PETR-2024-002',
            'rock_name': 'Базалт',
            'scientific_name': 'Basalt',
            'rock_type': 'Вулканска стена',
            'location_found': 'Авала, Србија',
            'geological_age': 'Неоген',
            'date_collected': '2022-09-10',
            'minerals_present': 'Пироксен, плагиоклас',
            'texture': 'Ситнозрна',
            'color': 'Тамно сива до црна',
            'weight_kg': 1.8,
            'dimensions_cm': '12x10x7',
            'condition': 'Одличан узорак',
            'description': 'Вулканска стена настала брзим хлађењем лаве.',
            'curator': 'tatjana.milicbabic@nhmbeo.rs'
        }
    ],
    'statistics': {
        'total_specimens': 2,
        'exhibitions': 'I bi svetlost, Mozaik prirode'
    }
}


COLLECTION_FALLBACKS = {
    'botany': BOTANY_FALLBACK,
    'ichthyology': ICHTHYOLOGY_FALLBACK,
    'entomology': ENTOMOLOGY_FALLBACK,
    'mycology': MYCOLOGY_FALLBACK,
    'herpetology': HERPETOLOGY_FALLBACK,
    'ornithology': ORNITHOLOGY_FALLBACK,
    'paleozoology': PALEOZOOLOGY_FALLBACK,
    'paleobotany': PALEOBOTANY_FALLBACK,
    'petrology': PETROLOGY_FALLBACK,
}


METEORITE_COLLECTION_DATABASE = {
    'specimens': [
        {
            'catalog_number': 'MET-001',
            'meteorite_name': 'Soko-Banja (Сокобања)',
            'classification': 'LL4 (Обични хондрит, брекча)',
            'fall_type': 'Пад (посматран)',
            'fall_date': '13. октобар 1877.',
            'total_mass_kg': 80.0,
            'specimen_mass': 16.286,
            'quantity': 1,
            'location_found': 'Сокобања, Заječарски округ, Централна Србија',
            'acquisition_date': 'Историјска колекција',
            'source': 'Оригинални налаз - 10 камена (највећи 38 kg)',
            'description': 'Најзначајнији српски метеорит. Пао 13.10.1877. Укупна маса свих камена 80 kg. Полиміктна брекча са различитим нивоима шока (S3-5). Садржи честице величине до 2 mm.',
            'meteorite_bulletin_number': '23661',
            'shock_stage': 'S3-5 (варијабилан шок)',
            'weathering_grade': 'W0 (без оксидације)',
            'chemical_composition': 'Оливин Fa26-32 mol%, Fe 19-22%, метално Fe 0.3-3%',
            'mineralogy': 'Оливин, ортопироксен, албитни плагиоклас, троилит, Fe-Ni метал',
            'parent_body': 'LL астероид из главног астероидног појаса',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': True
        },
        {
            'catalog_number': 'MET-002',
            'meteorite_name': 'Jelica (Јелица)',
            'classification': 'LL6 (Обични хондрит, брекча)',
            'fall_type': 'Пад (посматран)',
            'fall_date': '1. децембар 1889.',
            'total_mass_kg': 34.0,
            'specimen_mass': 8.5,
            'quantity': 1,
            'location_found': 'Јелица (Виљуша), Чачак, Моравички округ, Централна Србија (43.83°N, 20.44°E)',
            'acquisition_date': 'Историјска колекција',
            'source': 'Оригинални налаз - подручје пада 8x5 km',
            'description': 'Српски метеорит пао код планине Јелице 1.12.1889. Укупна маса 34 kg. Садржи еухедрални тетратаенит (65x107 μm) са импакт-растопљеним клaстом. Космички експозициони век ~26.2 милиона година.',
            'meteorite_bulletin_number': '12078',
            'shock_stage': 'S3 (слаб шок, ~15-20 GPa)',
            'weathering_grade': 'W0 (минимална еволуција)',
            'chemical_composition': 'Оливин Fa32.3 mol%, Fe 19-22%, метално Fe 0.3-3%, Ni≥50% у тетратаениту, Co 30% у вaирауиту',
            'mineralogy': 'Оливин, ортопироксен, албитни плагиоклас, троилит, Fe-Ni метал (тетратаенит, вaираuit, камацит, таенит), хромит, илменит, фосфати',
            'parent_body': 'LL астероид из главног астероидног појаса',
            'cosmic_ray_exposure': '~26.2 милиона година',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': True
        },
        {
            'catalog_number': 'MET-003',
            'meteorite_name': 'Dimitrovgrad (Димитровград)',
            'classification': 'Iron IIIAB (Гвоздени метеорит, средње октаедрит)',
            'fall_type': 'Налаз',
            'fall_date': 'Пронађен 1955.',
            'total_mass_kg': 'Није доступно',
            'specimen_mass': 100.0,
            'quantity': 1,
            'location_found': 'Димитровград, Пиротски округ, Централна Србија (43°2\'47"N, 22°51\'50"E)',
            'acquisition_date': '1955',
            'source': 'Документован налаз',
            'description': 'Српски гвоздени метеорит из Димитровграда. Пронађен 1955. Средње октаедрит са Widmanstätten структуром. Садржи камацит и таенит фазе.',
            'meteorite_bulletin_number': '7644',
            'shock_stage': 'Средњи до јак шок (типично за IIIAB)',
            'weathering_grade': 'Није наведено (налаз)',
            'chemical_composition': 'Ni 7.1-10.5%, Ga 16-23 ppm, Ge 27-47 ppm, Ir 0.01-19 ppm, Co ~0.5%, P 0.1-0.5%, S 0.1-1%',
            'mineralogy': 'Камацит и таенит (Fe-Ni фазе)',
            'widmanstatten_pattern': 'Присутан, ширина камацита 0.5-1.3 mm',
            'parent_body': 'Диференцирано језгро астероида из унутрашњег Сунчевог система',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': True
        },
        {
            'catalog_number': 'MET-004',
            'meteorite_name': 'Henbury (Pe section)',
            'classification': 'Iron IIIAB (Гвоздени метеорит, средње октаедрит)',
            'fall_type': 'Налаз',
            'fall_date': 'Откривен 1931., пао пре ~4,200±1,900 година',
            'total_mass_kg': 1.0,
            'specimen_mass': 0.1595,
            'quantity': 1,
            'location_found': 'Henbury Meteorite Conservation Reserve, Northern Territory, Аустралија (24°34\'S, 133°10\'E)',
            'acquisition_date': '1964-01-01',
            'source': 'Kyaneutta Museum, Kyaneutta, South Australia',
            'description': 'Пресек гвозденог метеорита из Хенбурија. Метеорит је створио ~13 ударних кратера (највећи 130m). Део међународне размене. Укупно пронађено преко 1000 kg.',
            'meteorite_bulletin_number': '11872',
            'shock_stage': 'Средњи до јак шок',
            'weathering_grade': 'Умерено до високо (хиљаде година изложености)',
            'chemical_composition': 'Ni 7.47%, Ga 17.7 ppm, Ge 33.7 ppm, Ir 13 ppm',
            'mineralogy': 'Камацит, таенит, коенит',
            'widmanstatten_pattern': 'Присутан (ширина камацита 0.9 mm), фине ламеле камацита и таенита',
            'parent_body': 'Диференцирано метално језгро астероида',
            'fusion_crust': 'Присутна на неким фрагментима',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-005',
            'meteorite_name': 'Silica Glass (Henbury)',
            'classification': 'Импактно стакло',
            'total_mass_g': 3.0,
            'quantity': 2,
            'location_found': 'Henbury Meteorite Craters, 1/2 mile East of main Crater',
            'acquisition_date': '1964-01-01',
            'source': 'Kyaneutta Museum, Kyaneutta, South Australia',
            'description': 'Црно силикатно стакло из кратера Хенбури. Импактно стакло настало ударом.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-006',
            'meteorite_name': 'Wolf Creek (Wolfe Creek)',
            'classification': 'Iron IIIAB (Гвоздени метеорит, средње октаедрит)',
            'fall_type': 'Налаз',
            'fall_date': 'Кратер откривен 1947., пао пре 120,000-137,000 година',
            'total_mass_kg': 'Није прецизно квантификовано',
            'specimen_mass': 0.692,
            'quantity': 1,
            'location_found': 'Wolfe Creek Crater, Western Australia, Аустралија (Tanami Road, 150 km јужно од Halls Creek)',
            'acquisition_date': '1964-01-01',
            'source': 'Smithsonian Museum, USA',
            'description': 'Гвоздени метеорит из другог по величини кратера на свету са пронађеним метеоритом. Веома еродиран - фрагменти претворени у "гвоздене шкриљце" масе до 250 kg. Садржи 3.5-4.5% Ni у оксидованим фрагментима.',
            'meteorite_bulletin_number': '24326',
            'shock_stage': 'Није наведено',
            'weathering_grade': 'Високо (екстензивна оксидација у гвоздене шкриљце)',
            'chemical_composition': 'Ni 3.5-4.5% у оксидованим фрагментима (типично IIIAB: Ni 7.1-10.5%, Ga 16-23 ppm, Ge 27-47 ppm)',
            'mineralogy': 'Оксидовани метеоритски фрагменти, гвожђе-оксид, неки фрагменти садрже неалтерисани метал',
            'parent_body': 'Диференцирано метално језгро астероида',
            'terrestrial_age': 'Мање од 120,000 година (касни плеистоцен)',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-007',
            'meteorite_name': 'Dalgaranga',
            'classification': 'Mesosiderite-A (Каменито-гвоздени метеорит)',
            'fall_type': 'Налаз',
            'fall_date': 'Откривен 1921.',
            'total_mass_kg': 12.2,
            'specimen_mass': 0.1328,
            'quantity': 1,
            'location_found': 'Dalgaranga Crater, Western Australia, Аустралија (75 km NW од Mount Magnet)',
            'acquisition_date': '1964-01-01',
            'source': 'Smithsonian Museum, USA (оригинално Gerard Wellard, 1921)',
            'description': 'ЈЕДИНСТВЕН метеорит - једини кратер на свету створен месосидеритом! Месосидерит са подједнаким деловима Ni-Fe метала и силиката. Формиранударом између кора и језгра астероида Весте пре ~4,525 милиона година.',
            'meteorite_bulletin_number': '5506',
            'shock_stage': 'S1-S2 (веома слаб шок, <10 GPa)',
            'weathering_grade': 'Умерено (налаз из 1921)',
            'chemical_composition': 'Оливин Fo58-92 (Fa8-42), Пироксен Fs20-40, Плагиоклас An>80 (анортит до битовнит)',
            'mineralogy': 'Ортопироксен, калциумски плагиоклас (доминантни), пигионит, оливин, тридимит, Ni-Fe метал (камацит, таенит)',
            'parent_body': 'Астероид 4 Vesta или сличан диференциран астероид',
            'fragment_type': 'Петролошка класа A (висок садржај плагиокласа)',
            'dating_method': 'U-Pb датирање: формирање коре 4,558.5±2.1 Ma, мешање метал-силикат 4,525.39±0.85 Ma',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-008',
            'meteorite_name': 'Plainview',
            'classification': 'H5 (Обични хондрит, високо гвожђе, брекча)',
            'fall_type': 'Налаз',
            'fall_date': 'Пронађен 1917.',
            'total_mass_kg': 700.0,
            'specimen_mass': 0.132,
            'quantity': 1,
            'location_found': 'Plainview, Hale County, Texas, USA (8 km SW од Plainview)',
            'acquisition_date': '1964-01-01',
            'source': 'Smithsonian Museum, USA',
            'description': 'ТРЕЋИ најмасивнији H5 хондрит на свету (после Јилин 4 тоне и Куња-Ургенч 1.1 тона). Полиміктна брекча са реголитним материјалом. Подручје пада 6x26 km. Преко 700 kg сакупљено захваљујући Harvey Nininger-у.',
            'meteorite_bulletin_number': '54437',
            'shock_stage': 'S3 (слаб шок, ~15-20 GPa)',
            'weathering_grade': 'W2 (мања оксидација метала и сулфида, рђа)',
            'chemical_composition': 'Оливин Fa16-20 mol%, Fe 25-31%, метално Fe 15-19%, просечна величина хондрула ~0.3 mm',
            'mineralogy': 'Оливин, пироксен, плагиоклас, троилит, Fe-Ni метал; садржи неравнотежене силикатне зрна и хондруле',
            'parent_body': 'H хондритски астероид из главног астероидног појаса',
            'fragment_type': 'Комплексна реголитна брекча формирана поновљеним ударима на површини родитељског тела',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-009',
            'meteorite_name': 'Toluca (Xiquipilco)',
            'classification': 'Гвоздени метеорит',
            'total_mass_g': 59.0,
            'quantity': 1,
            'location_found': 'Xiquipilco, Toluca, Mexico',
            'acquisition_date': '1964-01-01',
            'source': 'Smithsonian Museum, USA',
            'description': 'Гвоздени метеорит из Мексика. Познати метеорит Толука.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-010',
            'meteorite_name': 'Canyon Diablo',
            'classification': 'Гвоздени метеорит',
            'total_mass_g': 231.0,
            'quantity': 2,
            'location_found': 'Canyon Diablo, Arizona, USA',
            'acquisition_date': '1964-01-01',
            'source': 'Smithsonian Museum, USA',
            'description': 'Чувени метеорит из Каниона Ђаволо, креатора Meteor Cratera у Аризони.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-011',
            'meteorite_name': 'Звор нички хондрит',
            'classification': 'Хондрит',
            'total_mass_g': 66.5,
            'quantity': 1,
            'location_found': 'Зворник, Завидовићи, Босна и Херцеговина',
            'acquisition_date': 'Историјска колекција',
            'source': 'Мехо Рамовић',
            'description': 'Хондрит са подручја бивше Југославије. Донација М. Рамовића.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-012',
            'meteorite_name': 'Влтавин - Молдавит',
            'classification': 'Тектит (импактно стакло)',
            'total_mass_g': 'N/A',
            'quantity': 8,
            'location_found': 'Врабце код Ч. Будејовица, Чехословачка',
            'acquisition_date': 'Историјска колекција',
            'source': 'F.S. Tvrdel',
            'description': 'Влтавин (молдавит) - зелено тектитно стакло из Чешке. 8 примерака.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-013',
            'meteorite_name': 'Тектит (Индокинит)',
            'classification': 'Тектит (импактно стакло)',
            'total_mass_g': 7.2,
            'quantity': 1,
            'location_found': 'Лева обала реке Меконг, Лаос',
            'acquisition_date': 'Историјска колекција',
            'source': 'Др Ранко Рушић',
            'description': 'Индокинитски тектит из Лаоса. Донација др Р. Рушића.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-014',
            'meteorite_name': 'Mundrabila',
            'classification': 'Метеорит',
            'total_mass_kg': 1.965,
            'quantity': 1,
            'location_found': 'Пруга Перт - Аделаида (30°45\'S 127°30\'E), Аустралија',
            'acquisition_date': 'Историјска колекција',
            'source': 'Paul Ramdohr',
            'description': 'Метеорит Мундрабила из западне Аустралије. Донација P. Ramdohra.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-015',
            'meteorite_name': 'Henbury Iron #2',
            'classification': 'Гвоздени метеорит',
            'total_mass_g': 120.5,
            'quantity': 4,
            'location_found': 'Henbury, Central Australia',
            'acquisition_date': '1964-01-01',
            'source': 'Kyaneutta Museum, Kyaneutta, South Australia',
            'description': 'Додатни узорци гвозденог метеорита из Хенбурија. 4 примерка.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-016',
            'meteorite_name': 'Шљакасте бомбе (Henbury)',
            'classification': 'Импактни материјал',
            'total_mass_g': 28.35,
            'quantity': 3,
            'location_found': 'Henbury главни кратер, Central Australia',
            'acquisition_date': '1964-01-01',
            'source': 'Kyaneutta Museum, Kyaneutta, South Australia',
            'description': 'Шљакасте бомбе из главног кратера Хенбури. Импактни материјал.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-017',
            'meteorite_name': 'Henbury Iron #3',
            'classification': 'Гвоздени метеорит',
            'total_mass_g': 191.0,
            'quantity': 3,
            'location_found': 'Henbury, Central Australia',
            'acquisition_date': '1964-01-01',
            'source': 'Kyaneutta Museum, Kyaneutta, South Australia',
            'description': 'Гвоздени метеорит из Хенбурија. 3 примерка. Део аустралијске колекције.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        },
        {
            'catalog_number': 'MET-018',
            'meteorite_name': 'Bjurbole',
            'classification': 'Хиперстен хондрит',
            'total_mass_g': 55.2,
            'quantity': 1,
            'location_found': 'Bjurbole, Borge, Finland',
            'acquisition_date': 'Историјска колекција',
            'source': 'Minerals Engineering S.A, Geneva, Швајцарска',
            'description': 'Хиперстен хондрит из Финске. Класичан L/LL хондрит, пао 1899.',
            'curator': 'aca.lukovic@nhmbeo.rs',
            'serbian_meteorite': False
        }
    ],
}


def _compute_meteorite_statistics(specimens):
    """Derive meteorite collection statistics from the specimen list so the
    displayed aggregates stay consistent with the records (no hand drift)."""
    serbian = sum(1 for specimen in specimens if specimen.get('serbian_meteorite'))
    return {
        'total_specimens': len(specimens),
        'serbian_meteorites': serbian,
        'international_specimens': len(specimens) - serbian,
    }


METEORITE_COLLECTION_DATABASE['statistics'] = _compute_meteorite_statistics(
    METEORITE_COLLECTION_DATABASE['specimens']
)


CONSERVATION_BIOLOGY_DATABASE = {
    'records': [
        {
            'record_number': 'CONS-2024-001',
            'specimen_id': 'ENT-LEP-001',
            'specimen_name': 'Parnassius apollo',
            'conservation_type': 'Препарација',
            'conservator': 'Г. Петковски',
            'date_started': '2024-01-15',
            'date_completed': '2024-02-20',
            'condition_before': 'Оштећен',
            'condition_after': 'Одличан',
            'treatment_applied': 'Чишћење, стабилизација, монтирање на игли',
            'materials_used': 'Ентомолошке иглице, памук, дрво',
            'notes': 'Успешно препариран примерак за изложбу инсеката.',
            'storage_location': 'Ентомолошка збирка - фиока 12'
        },
        {
            'record_number': 'CONS-2024-002',
            'specimen_id': 'HERP-AMP-001',
            'specimen_name': 'Salamandra salamandra',
            'conservation_type': 'Конзервација',
            'conservator': 'М. Мрваљевић',
            'date_started': '2024-03-10',
            'date_completed': '2024-03-25',
            'condition_before': 'Добар',
            'condition_after': 'Одличан',
            'treatment_applied': 'Формалин конзервација, стаклена боца',
            'materials_used': 'Формалин 4%, стаклена боца',
            'notes': 'Влажна препарација за научну колекцију.',
            'storage_location': 'Херпетолошка збирка - полица А-15'
        }
    ],
    'statistics': {
        'total_records': 2,
        'conservators': 3,
        'specimens_treated_2024': 2
    }
}


CULTURAL_HERITAGE_DATABASE = {
    'heritage_items': [
        {
            'id': 1,
            'name': 'Скелет тираносауруса рекса',
            'registry_number': 'КД-ПМ-001/2015',
            'type': 'Покретно културно добро',
            'category': 'Природњачко наслеђе',
            'subcategory': 'Палеонтолошки узорак',
            'significance': 'Културно добро од великог значаја',
            'location': 'Сала 1 - Витрина 3',
            'condition': 'Одлично',
            'protection_date': '2015-06-20',
            'acquisition_date': '2015-03-15',
            'description': 'Комплетан скелет младог тираносауруса рекса, стар око 65 милиона година. Јединствен експонат са територије Североамеричког континента.',
            'legal_basis': 'Решење Министарства културе РС бр. 612-00-00403/2015-05',
            'cultural_value': 'Научно и едукативно наслеђе изузетне вредности',
            'period': 'Креда (65 милиона година)',
            'origin': 'Монтана, САД',
            'dimensions': '4.5m × 2.1m × 1.8m',
            'material': 'Окамењене кости',
            'weight': '450 kg',
            'protection_status': 'заштићено'
        },
        {
            'id': 2,
            'name': 'Кристал кварца са Копаоника',
            'registry_number': 'КД-ПМ-002/2018',
            'type': 'Покретно културно добро',
            'category': 'Природњачко наслеђе',
            'subcategory': 'Минералошки узорак',
            'significance': 'Културно добро',
            'location': 'Сала 2 - Витрина 1',
            'condition': 'Добро',
            'protection_date': '2018-09-15',
            'acquisition_date': '2018-07-22',
            'description': 'Велики кристал кварца са планине Копаоник, представља геолошко наслеђе Србије',
            'legal_basis': 'Решење Завода за заштиту споменика културе бр. 1247/18',
            'cultural_value': 'Геолошко наслеђе националног значаја',
            'period': 'Мезозоик',
            'origin': 'Копаоник, Србија',
            'dimensions': '45cm × 30cm × 25cm',
            'material': 'Кварц',
            'weight': '15 kg',
            'protection_status': 'заштићено'
        },
        {
            'id': 3,
            'name': 'Окамењени лист древне папрати',
            'registry_number': 'КД-ПМ-003/2020',
            'type': 'Покретно културно добро',
            'category': 'Природњачко наслеђе',
            'subcategory': 'Палеоботанички узорак',
            'significance': 'Културно добро',
            'location': 'Депо А - Полица 15',
            'condition': 'Добро',
            'protection_date': '2020-12-10',
            'acquisition_date': '2020-11-08',
            'description': 'Окамењени лист древне папрати из карбонског периода, пронађен на територији Алексинца',
            'legal_basis': 'Решење Завода за заштиту споменика културе бр. 2156/20',
            'cultural_value': 'Научно наслеђе палеоботанике',
            'period': 'Карбон (300 милиона година)',
            'origin': 'Алексинац, Србија',
            'dimensions': '20cm × 15cm × 3cm',
            'material': 'Окамењени биљни остаци',
            'weight': '2 kg',
            'protection_status': 'заштићено'
        },
        {
            'id': 4,
            'name': 'Збирка лептира Балканског полуострва',
            'registry_number': 'КД-ПМ-004/2019',
            'type': 'Покретно културно добро',
            'category': 'Природњачко наслеђе',
            'subcategory': 'Ентомолошка збирка',
            'significance': 'Културно добро од великог значаја',
            'location': 'Сала 3 - Витрина 5',
            'condition': 'Одлично',
            'protection_date': '2019-07-25',
            'acquisition_date': '2019-05-14',
            'description': 'Колекција од 120 врста лептира са Балкана, представља биодиверзитет региона',
            'legal_basis': 'Решење Министарства културе РС бр. 612-00-00891/2019-05',
            'cultural_value': 'Биолошко наслеђе Балканског полуострва',
            'period': 'Савремено (XIX-XXI век)',
            'origin': 'Балкан',
            'dimensions': '1.2m × 0.8m × 0.1m',
            'material': 'Ентомолошки препарати',
            'weight': '8 kg',
            'protection_status': 'заштићено'
        },
        {
            'id': 5,
            'name': 'Херцинит кристал из Босилеграда',
            'registry_number': 'КД-ПМ-005/2021',
            'type': 'Покретно културно добро',
            'category': 'Природњачко наслеђе',
            'subcategory': 'Минералошки узорак',
            'significance': 'Културно добро од изузетног значаја',
            'location': 'Сала 2 - Витрина 2',
            'condition': 'Одлично',
            'protection_date': '2021-10-18',
            'acquisition_date': '2021-09-03',
            'description': 'Ретки кристал херцинита са локалитета Босилеград, јединствен минералошки узорак',
            'legal_basis': 'Решење Министарства културе РС бр. 612-00-01203/2021-05',
            'cultural_value': 'Минералошко наслеђе изузетне реткости',
            'period': 'Палеозоик',
            'origin': 'Босилеград, Србија',
            'dimensions': '12cm × 8cm × 6cm',
            'material': 'Херцинит (цинк алуминијум оксид)',
            'weight': '1.5 kg',
            'protection_status': 'заштићено'
        },
        {
            'id': 6,
            'name': 'Фосил трилобита из ордовика',
            'registry_number': 'КД-ПМ-006/2017',
            'type': 'Покретно културно добро',
            'category': 'Природњачко наслеђе',
            'subcategory': 'Палеонтолошки узорак',
            'significance': 'Културно добро',
            'location': 'Сала 1 - Витрина 2',
            'condition': 'Добро',
            'protection_date': '2018-02-14',
            'acquisition_date': '2017-12-10',
            'description': 'Добро очувани фосил трилобита из ордовика, сведочи о древном животу',
            'legal_basis': 'Решење Завода за заштиту споменика културе бр. 0234/18',
            'cultural_value': 'Палеонтолошко наслеђе',
            'period': 'Ордовик (450 милиона година)',
            'origin': 'Чешка Република',
            'dimensions': '8cm × 6cm × 2cm',
            'material': 'Окамењени остаци',
            'weight': '0.3 kg',
            'protection_status': 'заштићено'
        }
    ],
    'heritage_types': ['Покретно културно добро', 'Непокретно културно добро'],
    'categories': ['Природњачко наслеђе', 'Уметничко-историјска дела', 'Архивска грађа', 'Старе и ретке књиге'],
    'subcategories': ['Палеонтолошки узорак', 'Минералошки узорак', 'Палеоботанички узорак', 'Ентомолошка збирка', 'Зоолошки узорак', 'Геолошки узорак'],
    'significance_levels': ['Културно добро', 'Културно добро од великог значаја', 'Културно добро од изузетног значаја'],
    'locations': ['Сала 1', 'Сала 2', 'Сала 3', 'Депо А', 'Депо Б', 'Привремени депо'],
    'conditions': ['Одлично', 'Добро', 'Задовољавајуће', 'Лоше', 'Захтева рестаурацију'],
    'protection_statuses': ['заштићено', 'у поступку заштите', 'предложено за заштиту', 'неевидентирано'],
    'statistics': {
        'total_heritage_items': 6,
        'exceptional_significance': 1,
        'great_significance': 2,
        'regular_significance': 3,
        'natural_heritage': 6,
        'displayed_items': 5,
        'storage_items': 1,
        'excellent_condition': 3,
        'good_condition': 3
    }
}


class CollectionBootstrapSupport:
    """Encapsulate curator collection fallback data and lazy bootstrap helpers."""

    def __init__(self, *, lazy_loaded_dict_cls, database_url=None, phase3a_databases=None):
        self._database_url = database_url
        self._phase3a_databases = phase3a_databases
        self._cached_heritage_db = None
        self._cached_meteorite_db = None

        self.botany_collection_database = lazy_loaded_dict_cls(
            lambda: self.load_collection_database('botany', BOTANY_FALLBACK),
            'botany collection',
        )
        self.ichthyology_collection_database = lazy_loaded_dict_cls(
            lambda: self.load_collection_database('ichthyology', ICHTHYOLOGY_FALLBACK),
            'ichthyology collection',
        )
        self.entomology_collection_database = lazy_loaded_dict_cls(
            lambda: self.load_collection_database('entomology', ENTOMOLOGY_FALLBACK),
            'entomology collection',
        )
        self.mycology_collection_database = lazy_loaded_dict_cls(
            lambda: self.load_collection_database('mycology', MYCOLOGY_FALLBACK),
            'mycology collection',
        )
        self.herpetology_collection_database = lazy_loaded_dict_cls(
            lambda: self.load_collection_database('herpetology', HERPETOLOGY_FALLBACK),
            'herpetology collection',
        )
        self.ornithology_collection_database = lazy_loaded_dict_cls(
            lambda: self.load_collection_database('ornithology', ORNITHOLOGY_FALLBACK),
            'ornithology collection',
        )
        self.paleozoology_collection_database = lazy_loaded_dict_cls(
            lambda: self.load_collection_database('paleozoology', PALEOZOOLOGY_FALLBACK),
            'paleozoology collection',
        )
        self.paleobotany_collection_database = lazy_loaded_dict_cls(
            lambda: self.load_collection_database('paleobotany', PALEOBOTANY_FALLBACK),
            'paleobotany collection',
        )
        self.petrology_collection_database = lazy_loaded_dict_cls(
            lambda: self.load_collection_database('petrology', PETROLOGY_FALLBACK),
            'petrology collection',
        )
        self.meteorite_collection_database = METEORITE_COLLECTION_DATABASE
        self.conservation_biology_database = CONSERVATION_BIOLOGY_DATABASE
        self.cultural_heritage_database = CULTURAL_HERITAGE_DATABASE

    def load_collection_database(self, collection_type, fallback_data):
        """Load a curator collection from PostgreSQL when configured, else use fallback data."""
        if self._database_url and self._phase3a_databases is not None:
            loader_name = _PHASE3A_COLLECTION_LOADERS.get(collection_type)
            if loader_name:
                try:
                    return getattr(self._phase3a_databases, loader_name)()
                except Exception as exc:
                    logger.warning("Failed to load %s from PostgreSQL: %s", collection_type, exc)
        return fallback_data

    def _get_cached_phase3a_database(self, *, cache_attr, loader_name, primary_key, fallback_data):
        if self._database_url and self._phase3a_databases is not None:
            cached_value = getattr(self, cache_attr)
            if cached_value is None:
                loaded_value = getattr(self._phase3a_databases, loader_name)()
                if loaded_value and loaded_value.get(primary_key):
                    setattr(self, cache_attr, loaded_value)
                return loaded_value
            return cached_value
        return fallback_data

    def get_cultural_heritage_database(self):
        """Get cultural heritage database from PostgreSQL or fallback to dict."""
        return self._get_cached_phase3a_database(
            cache_attr='_cached_heritage_db',
            loader_name='get_cultural_heritage_database',
            primary_key='heritage_items',
            fallback_data=self.cultural_heritage_database,
        )

    def get_meteorite_collection_database(self):
        """Get meteorite collection database from PostgreSQL or fallback to dict."""
        return self._get_cached_phase3a_database(
            cache_attr='_cached_meteorite_db',
            loader_name='get_meteorite_collection_database',
            primary_key='specimens',
            fallback_data=self.meteorite_collection_database,
        )
