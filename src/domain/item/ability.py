from src.infrastructure.utils.enums import CaseInsensitiveEnum


VETERANS_BONUS_NAME = "Навык ветерана"
BERSERKER_RAGE_NAME = "Ярость Берсерка"
BODYGUARD_NAME = "Телохранитель"

DARK_CURSE_NAME = "Темное проклятие"


class AbilityTendency(CaseInsensitiveEnum):
    DARK_CURSE = DARK_CURSE_NAME


class ClanAbility(CaseInsensitiveEnum):
    VETERANS_BONUS = VETERANS_BONUS_NAME
    BERSERKER_RAGE = BERSERKER_RAGE_NAME
    BODYGUARD = BODYGUARD_NAME
