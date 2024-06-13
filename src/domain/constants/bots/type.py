from dataclasses import dataclass

from src.domain.constants.bots import names


FORPOST_BOSSES = [
    names.MINION_OF_LOKAR,
    names.HELPER_OF_ATAMAN,
    names.GROMLECH_BLUETOOTH,
    names.RENEGADE_DRUID,
    names.FOREST_KEEPER,
]

FORPOST_BOTS = [
    names.GROMLECH_WIZARD,
    names.GROMLECH_BANDIT,
]

OKTAL_BOSSES = [
    names.KHALGHAN_RAIDER,
]

CITY_BOSSES = FORPOST_BOSSES + OKTAL_BOSSES

DUNGEON_WARRIOR_BOSSES = [
    names.ARCHI_PALADIN_MORTIUS,
    names.PALADIN_MORTIUS,
]

DUNGEON_MAG_BOSSES = [
    names.ARCHI_LICH,
    names.LICH,
]

DUNGEON_BOTS = [
    names.PLAGUE_ZOMBIE,
]

DUNGEON_BOSSES = DUNGEON_WARRIOR_BOSSES + DUNGEON_MAG_BOSSES

DUNGEON_BOSSES_AND_BOTS = DUNGEON_BOSSES + DUNGEON_BOTS


@dataclass
class Boss:
    name: str
