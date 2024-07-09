from enum import Enum
from enum import IntEnum
from enum import StrEnum
from enum import auto

from src.infrastructure.utils.enums import CaseInsensitiveEnum


class PersonRole(Enum):
    SLAVE = auto()
    LEADER = auto()
    SOLO = auto()


class PersonType(CaseInsensitiveEnum):
    WARRIOR = auto()
    MAG = auto()


class LocationState(StrEnum):
    CITY = auto()
    FIGHT = auto()
    INVENTORY = auto()
    NATURE = auto()
    ELIXIR = auto()
    INFO = auto()
    BAIT = auto()
    CASTLE = auto()
    ABILITY = auto()


class Teleport(IntEnum):
    FP = 1
    OKTAL = 2
    PODGORN = 3
    OKREST_FEIDANA = 4
    OKREST_OKTAL = 5
    OKREST_ERINGARD = 6
    OKREST_FP = 7
    SAMYM_BEYT = 8
    NORTHERN_TRACT = 9
    EASTERN_FORESTS = 10
    OKREST_KENGI = 11
    GORGE_EL_TER = 12
