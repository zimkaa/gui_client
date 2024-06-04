from enum import Enum
from enum import StrEnum
from enum import auto


class PersonRole(Enum):
    SLAVE = auto()
    LEADER = auto()
    SOLO = auto()


class PersonType(Enum):
    WARRIOR = auto()
    MAG = auto()


class Location(StrEnum):
    CITY = auto()
    FIGHT = auto()
    INVENTAR = auto()
    NATURE = auto()
    ELIXIR = auto()
    INFO = auto()


class Teleport(Enum):
    FP = auto()
    OKTAL = auto()
    PODGORN = auto()
    OKREST_FEIDANA = auto()
    OKREST_OKTAL = auto()
    OKREST_ERINGARD = auto()
    OKREST_FP = auto()
    SAMYM_BEYT = auto()
    NORTHERN_TRACT = auto()
    EASTERN_FORESTS = auto()
    OKREST_KENGI = auto()
    GORGE_EL_TER = auto()
