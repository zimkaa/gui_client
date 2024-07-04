from enum import IntEnum


SOURCE_OF_LIFE_NAME = "Источник жизни"
SOURCE_OF_MAGIC_NAME = "Источник магии"
MAGICAL_ENHANCEMENT_NAME = "Магическое усиление"


class MagicTower(IntEnum):
    LUCK = 11
    DODGE = 10

    CRUSHING_BONUS = 18
    DODGE_BONUS = 20

    DAMAGE = 26

    FIRE_RESISTANCE = 27
    WIND_RESISTANCE = 28

    RESTORE_HP = 37
    RESTORE_MP = 38
    OBSERVATION = 41
    STRANGER = 43

    FIRE_MAGIC = 45
    WIND_MAGIC = 46
