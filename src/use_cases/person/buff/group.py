from src.domain.item.ability import AbilityTendency
from src.domain.item.ability import ClanAbility
from src.domain.item.elixir import Elixir
from src.domain.item.potion import Potion
from src.domain.item.scroll import Scroll
from src.use_cases.person.buff import castle
from src.use_cases.person.buff import effects


DODGE_TOWER = [
    castle.MagicTower.DODGE,
    castle.MagicTower.DODGE_BONUS,
    castle.MagicTower.STRANGER,
]

DAMAGE_TOWER = [
    castle.MagicTower.DAMAGE,
    castle.MagicTower.CRUSHING_BONUS,
    castle.MagicTower.OBSERVATION,
    castle.MagicTower.LUCK,
]

DEFAULT_MAG_TOWER = [
    castle.MagicTower.DODGE,
    castle.MagicTower.DODGE_BONUS,
    castle.MagicTower.STRANGER,
]


HANDS_FIGHT = [
    effects.Effect(name=Potion.IMMUNITY, type_=effects.ElementType.POTION),
    effects.Effect(name=Potion.EXCELLENT_AGILE_STRIKES, type_=effects.ElementType.POTION, count=2),
    effects.Effect(name=Potion.EXCELLENT_LIFE, type_=effects.ElementType.POTION, count=2),
    effects.Effect(name=Scroll.STONE_SKIN, type_=effects.ElementType.SCROLL, count=2),
]


MAG_NOOB = [
    effects.Effect(name=Potion.IMMUNITY, type_=effects.ElementType.POTION),
    effects.Effect(name=Potion.MOBILITY, type_=effects.ElementType.POTION, count=3),
    effects.Effect(name=Scroll.FIRE_MAGIC, type_=effects.ElementType.SCROLL, count=10),
]


MARINADE_WARRIOR = [
    effects.Effect(name=Potion.IMMUNITY, type_=effects.ElementType.POTION),
    effects.Effect(name=Potion.ROUGH_SKIN, type_=effects.ElementType.POTION, count=4),
    effects.Effect(name=Scroll.STONE_SKIN, type_=effects.ElementType.SCROLL, count=2),
    effects.Effect(name=castle.MAGICAL_ENHANCEMENT_NAME, castle=DAMAGE_TOWER, type_=effects.ElementType.CASTLE),
    effects.Effect(name=castle.SOURCE_OF_LIFE_NAME, type_=effects.ElementType.CASTLE_HP),
    effects.Effect(name=castle.SOURCE_OF_MAGIC_NAME, type_=effects.ElementType.CASTLE_MP),
]


MAG_FULL_FIRE_EARTH = [
    effects.Effect(name=Potion.IMMUNITY, type_=effects.ElementType.POTION),
    effects.Effect(name=Potion.MOBILITY, type_=effects.ElementType.POTION, count=3),
    effects.Effect(name=Scroll.FIRE_MAGIC, type_=effects.ElementType.SCROLL, count=10),
    effects.Effect(name=Scroll.EARTH_MAGIC, type_=effects.ElementType.SCROLL, count=10),
    effects.Effect(name=Elixir.SWIFTNESS, type_=effects.ElementType.ELIXIR, count=1),
    effects.Effect(name=castle.MAGICAL_ENHANCEMENT_NAME, castle=DODGE_TOWER, type_=effects.ElementType.CASTLE),
    effects.Effect(name=castle.SOURCE_OF_LIFE_NAME, type_=effects.ElementType.CASTLE_HP),
    effects.Effect(name=castle.SOURCE_OF_MAGIC_NAME, type_=effects.ElementType.CASTLE_MP),
]


FULL_WARRIOR = [
    effects.Effect(name=Potion.IMMUNITY, type_=effects.ElementType.POTION),
    effects.Effect(name=Potion.EXCELLENT_SHELL, type_=effects.ElementType.POTION, count=4),
    effects.Effect(name=Elixir.SWIFTNESS, type_=effects.ElementType.ELIXIR, count=2),
    effects.Effect(name=Elixir.POTION_BLOODTHIRSTY, type_=effects.ElementType.ELIXIR, count=2),
    # effects.Effect(name=Elixir.SWIFTNESS, type_=effects.ElementType.SCROLL, count=2),  # 2 льда  # noqa: ERA001
    effects.Effect(name=castle.MAGICAL_ENHANCEMENT_NAME, castle=DODGE_TOWER, type_=effects.ElementType.CASTLE),
    effects.Effect(name=castle.SOURCE_OF_LIFE_NAME, type_=effects.ElementType.CASTLE_HP),
    effects.Effect(name=castle.SOURCE_OF_MAGIC_NAME, type_=effects.ElementType.CASTLE_MP),
]


TEST = [
    effects.Effect(name=Potion.IMMUNITY, type_=effects.ElementType.POTION),
    effects.Effect(name=Potion.MOBILITY, type_=effects.ElementType.POTION, count=3),
    effects.Effect(name=Elixir.BLISS, type_=effects.ElementType.ELIXIR, count=1),
    effects.Effect(name=castle.MAGICAL_ENHANCEMENT_NAME, castle=DAMAGE_TOWER, type_=effects.ElementType.CASTLE),
    effects.Effect(name=castle.SOURCE_OF_LIFE_NAME, type_=effects.ElementType.CASTLE_HP),
    effects.Effect(name=castle.SOURCE_OF_MAGIC_NAME, type_=effects.ElementType.CASTLE_MP),
    effects.Effect(name=ClanAbility.BODYGUARD, type_=effects.ElementType.CLAN_ABILITY),
    effects.Effect(name=ClanAbility.BERSERKER_RAGE, type_=effects.ElementType.CLAN_ABILITY),
    effects.Effect(name=ClanAbility.VETERANS_BONUS, type_=effects.ElementType.CLAN_ABILITY),
    effects.Effect(name=AbilityTendency.DARK_CURSE, type_=effects.ElementType.ABILITY),
]


TURN = [
    effects.Effect(name=Potion.MOBILITY, type_=effects.ElementType.POTION, count=2),
    effects.Effect(name=Potion.EXCELLENT_MOUNTAIN_MAN, type_=effects.ElementType.POTION, count=3),
    effects.Effect(name=Elixir.CHAMPAGNE, type_=effects.ElementType.ELIXIR, count=5),
    effects.Effect(name=Elixir.BLISS, type_=effects.ElementType.ELIXIR, count=1),
    effects.Effect(name=castle.MAGICAL_ENHANCEMENT_NAME, castle=DODGE_TOWER, type_=effects.ElementType.CASTLE),
    effects.Effect(name=castle.SOURCE_OF_LIFE_NAME, type_=effects.ElementType.CASTLE_HP),
    effects.Effect(name=castle.SOURCE_OF_MAGIC_NAME, type_=effects.ElementType.CASTLE_MP),
]


TOP_MAG = [
    effects.Effect(name=Potion.MOBILITY, type_=effects.ElementType.POTION, count=2),
    effects.Effect(name=Potion.EXCELLENT_MOUNTAIN_MAN, type_=effects.ElementType.POTION, count=3),
    effects.Effect(name=Elixir.BLISS, type_=effects.ElementType.ELIXIR, count=1),
    effects.Effect(name=castle.MAGICAL_ENHANCEMENT_NAME, castle=DODGE_TOWER, type_=effects.ElementType.CASTLE),
    effects.Effect(name=castle.SOURCE_OF_LIFE_NAME, type_=effects.ElementType.CASTLE_HP),
    effects.Effect(name=castle.SOURCE_OF_MAGIC_NAME, type_=effects.ElementType.CASTLE_MP),
]


MAG_DUNGEON = [
    effects.Effect(name=Potion.EXCELLENT_MOUNTAIN_MAN, type_=effects.ElementType.POTION, count=5),
    effects.Effect(name=Elixir.BLISS, type_=effects.ElementType.ELIXIR, count=1),
    effects.Effect(name=castle.MAGICAL_ENHANCEMENT_NAME, castle=DODGE_TOWER, type_=effects.ElementType.CASTLE),
    effects.Effect(name=castle.SOURCE_OF_LIFE_NAME, type_=effects.ElementType.CASTLE_HP),
    effects.Effect(name=castle.SOURCE_OF_MAGIC_NAME, type_=effects.ElementType.CASTLE_MP),
]


HUNTER = [
    effects.Effect(name=Potion.EXCELLENT_BARDS, type_=effects.ElementType.POTION, count=3),
    effects.Effect(name=Potion.MOBILITY, type_=effects.ElementType.POTION, count=2),
    effects.Effect(name=Elixir.BLISS, type_=effects.ElementType.ELIXIR, count=1),
    effects.Effect(name=castle.MAGICAL_ENHANCEMENT_NAME, castle=DAMAGE_TOWER, type_=effects.ElementType.CASTLE),
    effects.Effect(name=castle.SOURCE_OF_LIFE_NAME, type_=effects.ElementType.CASTLE_HP),
    effects.Effect(name=castle.SOURCE_OF_MAGIC_NAME, type_=effects.ElementType.CASTLE_MP),
]


WARRIOR_DUNGEON = [
    effects.Effect(name=Potion.EXCELLENT_SHELL, type_=effects.ElementType.POTION, count=5),
    effects.Effect(name=Elixir.BLISS, type_=effects.ElementType.ELIXIR, count=1),
    effects.Effect(name=castle.MAGICAL_ENHANCEMENT_NAME, castle=DAMAGE_TOWER, type_=effects.ElementType.CASTLE),
    effects.Effect(name=castle.SOURCE_OF_LIFE_NAME, type_=effects.ElementType.CASTLE_HP),
    effects.Effect(name=castle.SOURCE_OF_MAGIC_NAME, type_=effects.ElementType.CASTLE_MP),
]


DEFAULT_MAG_EFFECTS = [
    effects.Effect(name=Potion.IMMUNITY, type_=effects.ElementType.POTION),
    effects.Effect(name=Potion.EXCELLENT_AGILE_STRIKES, type_=effects.ElementType.POTION, count=2),
    effects.Effect(name=Potion.EXCELLENT_LIFE, type_=effects.ElementType.POTION, count=2),
    effects.Effect(name=Scroll.STONE_SKIN, type_=effects.ElementType.SCROLL, count=2),
    effects.Effect(name=Elixir.BLISS, type_=effects.ElementType.ELIXIR, count=1),
    effects.Effect(name=castle.MAGICAL_ENHANCEMENT_NAME, castle=DEFAULT_MAG_TOWER, type_=effects.ElementType.CASTLE),
    effects.Effect(name=castle.SOURCE_OF_LIFE_NAME, type_=effects.ElementType.CASTLE_HP),
    effects.Effect(name=castle.SOURCE_OF_MAGIC_NAME, type_=effects.ElementType.CASTLE_MP),
]

DEFAULT_WARRIOR_TOWER = [
    castle.MagicTower.DAMAGE,
    castle.MagicTower.CRUSHING_BONUS,
    castle.MagicTower.OBSERVATION,
    castle.MagicTower.LUCK,
]

DEFAULT_WARRIOR_EFFECTS = [
    effects.Effect(name=Potion.EXCELLENT_SHELL, type_=effects.ElementType.POTION, count=5),
    effects.Effect(name=Elixir.BLISS, type_=effects.ElementType.ELIXIR, count=1),
    effects.Effect(
        name=castle.MAGICAL_ENHANCEMENT_NAME,
        castle=DEFAULT_WARRIOR_TOWER,
        type_=effects.ElementType.CASTLE,
    ),
    effects.Effect(name=castle.SOURCE_OF_LIFE_NAME, type_=effects.ElementType.CASTLE_HP),
    effects.Effect(name=castle.SOURCE_OF_MAGIC_NAME, type_=effects.ElementType.CASTLE_MP),
]
