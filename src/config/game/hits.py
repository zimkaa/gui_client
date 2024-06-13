from __future__ import annotations
from typing import Any
from typing import Final

from src.domain.constants.buffs import name


MP_LIST_MP = [337, 521, 33, 306, 309]

DICT_NAME_BOOST_MP = {
    "name": [
        "Тыквенное зелье",
        "Превосходное Зелье Маны",
        "Восстановление MP",  # it's can be 500 MP or 5000 MP or anything else
        "Зелье Восстановления Маны",
        "Зелье Энергии",
    ],
    "code": MP_LIST_MP,
    "priority": [0, 1, 2, 3, 4],
    "mp_boost": [999, 500, 5_000, 100, 100],
    "od": [30, 30, 30, 30, 30],
}


HIT_SCROLLS: Final[list[str]] = [
    "Свиток Воскрешения",
    "Свиток Выжигания Маны",
    "Свиток Светлого Удара",
    "Свиток Темного Удара",
    "Свиток Изгнания Из Боя",
    "Свиток Удар Ярости",
    "Свиток Излечения Союзника",
    "Свиток Завершения Боя",
    "Свиток Женской Злости",
    "Снежок",
]


# WARRIOR_KICK = [  # noqa: ERA001, RUF100
#     name.INCREDIBLE_ACCURACY,
#     name.PUSH,
#     name.DEADLY_ATTACK,
#     name.DIAMOND_SKIN,
#     name.ROCK,
#     name.ALVAS_SECRET,
#     name.VAMPIRISM,
#     name.SECOND_WIND,
#     name.DETERMINATION,
#     name.MORAL,
#     name.OAK_LEATHER,
#     name.FORTRESS,
#     name.PROTECTIVE_STAND,
#     name.TOTAL_DEFENSE,
#     name.IMPENETRABLE_PROTECTION,
#     name.STUN,
# ]  # noqa: ERA001, RUF100

WARRIOR_KICK = [
    name.DEADLY_ATTACK,
    name.DIAMOND_SKIN,
    name.ALVAS_SECRET,
]


warrior_zombie_kick = [
    name.DIAMOND_SKIN,
    name.ROCK,
    name.ALVAS_SECRET,
    name.PUSH,
    name.MORAL,
    name.OAK_LEATHER,
    name.FORTRESS,
    name.PROTECTIVE_STAND,
    name.IMPENETRABLE_PROTECTION,
    name.STUN,
    # name.IMPENETRABLE_PROTECTION,
    name.STUN,
]
warrior_buffs = [name.PUSH, name.DEADLY_ATTACK, name.INCREDIBLE_ACCURACY]

# use for mag
mag_buffs = [
    name.BOUNTY_OF_LIGHTNING,
    name.DEADLY_ATTACK,
    name.SAND_WALL,
    name.POISONING,
    name.STONE_FLESH,
    name.POWER,
    name.METEOR_SHIELD,
    name.QUICKSAND,
    name.SOURCE,
    name.ALVAS_SECRET,
]
mag_zombie_kick = [
    name.DIAMOND_SKIN,
    name.ROCK,
    name.ALVAS_SECRET,
    name.PUSH,
    name.MORAL,
    name.OAK_LEATHER,
    name.FORTRESS,
    name.PROTECTIVE_STAND,
    name.IMPENETRABLE_PROTECTION,
    name.STUN,
]

# mag_kick = [  # noqa: ERA001, RUF100
#     BOUNTY_OF_LIGHTNING,
#     DEADLY_ATTACK,
#     SAND_WALL,
#     POISONING,
#     STONE_FLESH,
#     POWER,
#     METEOR_SHIELD,
#     QUICKSAND,
#     SOURCE,
# ]  # noqa: ERA001, RUF100

MAG_KICK = [
    name.VULNERABLE_TO_FIRE,
    name.DEADLY_ATTACK,
    name.FLAMING_RACK,
    name.IFRITS_CURSE,
    name.VULNERABLE_TO_FIRE,
    name.FIRE_SHIELD,
    name.HEADWIND,
    name.AIR_BARRIER,
    name.BOUNTY_OF_LIGHTNING,
    name.SAND_WALL,
    name.POISONING,
    name.STONE_FLESH,
    name.POWER,
    name.METEOR_SHIELD,
    name.QUICKSAND,
    name.SOURCE,
    name.ALVAS_SECRET,
    name.STUN,
]


# ZOMBIE_KICK = zombie_kick  # noqa: ERA001

# BUFFS: Final[list[str]] = buffs  # noqa: ERA001

# KICK: Final[list[str]] = kick  # noqa: ERA001

HIT_PRIORITY: Final[bool] = True

ONLY_NUM_HIT: Final[bool] = True
NUMBER_HIT: Final[int] = 0

EVERY_NUM_HIT: Final[bool] = True
EVERY_NUMBER_HIT: Final[int] = 5

USE_PROF_HIT_NAME: Final[str] = "Цепная молния"

ANY_PROF_HITS: Final[dict[str, Any]] = {
    "name": [
        # wind
        "Гнев Титанов",
        "Ураган",
        "Молния",
        "Цепная молния",
        # ground
        "Каменная стрела",
        "Песочная стрела",
        "Колючки",
        # fire
        "Огненная стрела",
        "Стрела из магмы",
        "Воспламенение",  # old name "Тело-огонь"
        "Огненный дождь",
        # water
    ],
    "code": [207, 208, 205, 206, 123, 122, 94, 37, 124, 56, 81],
    "mp_cost": [75, 100, 50, 150, 75, 50, 75, 50, 75, 75, 150],
    "od": [100, 100, 100, 125, 100, 100, 100, 100, 100, 100, 125],
    "priority": [1, 5, 8, 99, 6, 9, 3, 4, 2, 7, 99],
    # "priority": [2, 6, 9, 1, 7, 10, 4, 5, 3, 8, 1],  # for hit zombie Цепная молния  # noqa: ERA001
}

ALL_ANY_PROF_HITS: Final[dict[str, Any]] = {
    "name": [
        "Огненная стрела",
        "Воспламенение",  # old name "Тело-огонь"
        "Огненный дождь",
        "Каменный дождь",
        "Колючки",
        "Песочная стрела",
        "Каменная стрела",
        "Стрела из магмы",
        "Ледяная стрела",
        "Ледяная глыба",
        "Прикосновение льдом",
        "Метель",
        "Молния",
        "Цепная молния",
        "Гнев Титанов",
        "Ураган",
        "Смазанный удар",
    ],
    "code": [
        37,
        56,
        81,
        86,
        94,
        122,
        123,
        124,
        144,
        146,
        148,
        184,
        205,
        206,
        207,
        208,
        269,
    ],
    "mp_cost": [
        50,
        75,
        150,
        150,
        75,
        50,
        75,
        75,
        50,
        75,
        75,
        150,
        50,
        150,
        75,
        100,
        0,
    ],
    "od": [
        100,
        100,
        125,
        125,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        125,
        100,
        125,
        100,
        100,
        90,
    ],
    "priority": [
        1,
        1,
        2,
        2,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        2,
        3,
        99,
        1,
        2,
        99,
    ],
}
