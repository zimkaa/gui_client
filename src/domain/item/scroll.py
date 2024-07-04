from enum import StrEnum


STONE_SKIN_NAME = "Свиток каменной кожи"

EARTH_MAGIC_NAME = "Свиток Магии Земли"
FIRE_MAGIC_NAME = "Свиток Магии Огня"
WIND_MAGIC_NAME = "Свиток Магии Воздуха"
WATER_MAGIC_NAME = "Свиток Магии Воды"

EARTH_POWER_NAME = "Сила земли"
FIRE_POWER_NAME = "Сила огня"
WIND_POWER_NAME = "Сила воздуха"
WATER_POWER_NAME = "Сила воды"

SCROLL_OF_MAJESTY_NAME = "Свиток Величия"
ANCIENT_SCROLL_OF_MAJESTY_NAME = "Древний Свиток Величия"
TELEPORT_DIRE_SWAMP_NAME = "Телепорт (Гиблая Топь)"
TELEPORT_FORT_RUSTLING_LEAVES_NAME = "Телепорт (Форт Звенящей Листвы)"
TELEPORT_ISLAND_TUROTOR_NAME = "Телепорт (Остров Туротор)"
SCROLL_OF_INEVITABILITY_3H_NAME = "Свиток Неизбежности (3 часа)"
FESTIVE_INEVITABILITY_NAME = "Праздничная Неизбежность"
SCROLL_OF_PURIFICATION_NAME = "Свиток Очищения"
SCROLL_OF_PATRONAGE_3H_NAME = "Свиток Покровительства (3 часа)"
FESTIVE_PATRONAGE_NAME = "Праздничное Покровительство"
DOOR_OF_DIMENSIONS_NAME = "Дверь Измерений"
WRATH_OF_LOKAR_NAME = "Гнев Локара"
SUMMON_HELPER_IMP_NAME = "Призыв импа-помощника"

TELEPORT_NAME = "Телепорт"


equivalent_scroll_dict = {
    EARTH_MAGIC_NAME: EARTH_POWER_NAME,
    FIRE_MAGIC_NAME: FIRE_POWER_NAME,
    WIND_MAGIC_NAME: WIND_POWER_NAME,
    WATER_MAGIC_NAME: WATER_POWER_NAME,
}


class Scroll(StrEnum):
    STONE_SKIN = STONE_SKIN_NAME
    EARTH_MAGIC = EARTH_MAGIC_NAME
    FIRE_MAGIC = FIRE_MAGIC_NAME
    WIND_MAGIC = WIND_MAGIC_NAME
    WATER_MAGIC = WATER_MAGIC_NAME

    SCROLL_OF_MAJESTY = SCROLL_OF_MAJESTY_NAME
    ANCIENT_SCROLL_OF_MAJESTY = ANCIENT_SCROLL_OF_MAJESTY_NAME
    TELEPORT_DIRE_SWAMP = TELEPORT_DIRE_SWAMP_NAME
    TELEPORT_FORT_RUSTLING_LEAVES = TELEPORT_FORT_RUSTLING_LEAVES_NAME
    TELEPORT_ISLAND_TUROTOR = TELEPORT_ISLAND_TUROTOR_NAME
    SCROLL_OF_INEVITABILITY_3H = SCROLL_OF_INEVITABILITY_3H_NAME
    FESTIVE_INEVITABILITY = FESTIVE_INEVITABILITY_NAME
    SCROLL_OF_PURIFICATION = SCROLL_OF_PURIFICATION_NAME
    SCROLL_OF_PATRONAGE_3H = SCROLL_OF_PATRONAGE_3H_NAME
    FESTIVE_PATRONAGE = FESTIVE_PATRONAGE_NAME
    DOOR_OF_DIMENSIONS = DOOR_OF_DIMENSIONS_NAME
    WRATH_OF_LOKAR = WRATH_OF_LOKAR_NAME
    SUMMON_HELPER_IMP = SUMMON_HELPER_IMP_NAME
