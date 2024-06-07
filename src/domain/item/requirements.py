from src.domain.item import name as item_name
from src.domain.person import name as person_name
from src.infrastructure.utils.enums import CaseInsensitiveEnum


class RequirementsVariants(CaseInsensitiveEnum):
    # Person
    HP = person_name.HP_NAME
    MP = person_name.MP_NAME

    STRENGTH = person_name.STRENGTH_NAME
    DODGE = person_name.DODGE_NAME
    LUCK = person_name.LUCK_NAME
    KNOWLEDGE = person_name.KNOWLEDGE_NAME
    HEALTH = person_name.HEALTH_NAME
    WISDOM = person_name.WISDOM_NAME

    # Unique only requirements
    CLAN = item_name.CLAN_NAME
    WEIGHT = item_name.WEIGHT_NAME
    LEVEL = item_name.LEVEL_NAME
    ENERGY = item_name.ENERGY_NAME
    POCKETS = item_name.POCKETS_NAME
    OD = item_name.OD_NAME

    # Peaceful skills
    CAUTION = item_name.CAUTION_NAME
    STEALTH = item_name.STEALTH_NAME
    OBSERVATION = item_name.OBSERVATION_NAME
    STRANGER = item_name.STRANGER_NAME
    LINGUISTICS = item_name.LINGUISTICS_NAME
    SELF_HEALING = item_name.SELF_HEALING_NAME
    FAST_MANA_RECOVERY = item_name.FAST_MANA_RECOVERY_NAME
    LEADERSHIP = item_name.LEADERSHIP_NAME

    # Combat skills
    HAND_TO_HAND_COMBAT = item_name.HAND_TO_HAND_COMBAT_NAME
    SWORDSMANSHIP = item_name.SWORDSMANSHIP_NAME
    AXEMANSHIP = item_name.AXEMANSHIP_NAME
    BLUNT_WEAPON_MASTERY = item_name.BLUNT_WEAPON_MASTERY_NAME
    KNIFE_MASTERY = item_name.KNIFE_MASTERY_NAME
    THROWING_WEAPON_MASTERY = item_name.THROWING_WEAPON_MASTERY_NAME
    HALBERD_AND_SPEAR_MASTERY = item_name.HALBERD_AND_SPEAR_MASTERY_NAME
    STAFF_MASTERY = item_name.STAFF_MASTERY_NAME
    EXOTIC_WEAPON_MASTERY = item_name.EXOTIC_WEAPON_MASTERY_NAME
    TWO_HANDED_WEAPON_MASTERY = item_name.TWO_HANDED_WEAPON_MASTERY_NAME
    TWO_HAND_HANDLING = item_name.TWO_HAND_HANDLING_NAME
    ADDITIONAL_ACTION_POINTS = item_name.ADDITIONAL_ACTION_POINTS_NAME

    # Resistance
    FIRE_MAGIC_RESISTANCE = item_name.FIRE_MAGIC_RESISTANCE_NAME
    WATER_MAGIC_RESISTANCE = item_name.WATER_MAGIC_RESISTANCE_NAME
    AIR_MAGIC_RESISTANCE = item_name.AIR_MAGIC_RESISTANCE_NAME
    EARTH_MAGIC_RESISTANCE = item_name.EARTH_MAGIC_RESISTANCE_NAME
    PHYSICAL_DAMAGE_RESISTANCE = item_name.PHYSICAL_DAMAGE_RESISTANCE_NAME

    # Magic skills
    FIRE_MAGIC = item_name.FIRE_MAGIC_NAME
    WATER_MAGIC = item_name.WATER_MAGIC_NAME
    AIR_MAGIC = item_name.AIR_MAGIC_NAME
    EARTH_MAGIC = item_name.EARTH_MAGIC_NAME

    # Professions
    THEFT = item_name.THEFT_NAME
    TRADING = item_name.TRADING_NAME
    CALLIGRAPHY = item_name.CALLIGRAPHY_NAME
    JEWELRY_CRAFTING = item_name.JEWELRY_CRAFTING_NAME
    CRAFTSMAN = item_name.CRAFTSMAN_NAME
    DOCTOR = item_name.DOCTOR_NAME
    ALCHEMY = item_name.ALCHEMY_NAME
    MINING_DEVELOPMENT = item_name.MINING_DEVELOPMENT_NAME
    FISHING = item_name.FISHING_NAME
    HUNTING = item_name.HUNTING_NAME
    COOKING = item_name.COOKING_NAME
    LOGGING = item_name.LOGGING_NAME
    CARPENTER = item_name.CARPENTER_NAME
    STEELWORKER = item_name.STEELWORKER_NAME
    HERBALIST = item_name.HERBALIST_NAME
