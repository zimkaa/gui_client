from src.domain.item.elixir import Elixir
from src.domain.item.potion import Potion
from src.domain.item.scroll import Scroll
from src.use_cases.person.buff import effects


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
    # effects.Effect(name=Scroll.STONE_SKIN, type_=effects.ElementType.CASTLE),  # noqa: ERA001
    # effects.Effect(name=Scroll.STONE_SKIN, type_=effects.ElementType.CASTLE),  # noqa: ERA001
    # effects.Effect(name=Scroll.STONE_SKIN, type_=effects.ElementType.CASTLE),  # noqa: ERA001
]


MAG_FULL = [
    effects.Effect(name=Potion.IMMUNITY, type_=effects.ElementType.POTION),
    effects.Effect(name=Potion.MOBILITY, type_=effects.ElementType.POTION, count=3),
    effects.Effect(name=Scroll.FIRE_MAGIC, type_=effects.ElementType.SCROLL, count=10),
    effects.Effect(name=Scroll.FIRE_MAGIC, type_=effects.ElementType.SCROLL, count=10),
    effects.Effect(name=Elixir.SWIFTNESS, type_=effects.ElementType.SCROLL, count=1),
    # effects.Effect(name=Elixir.FIRE_MAGIC, type_=effects.ElementType.SCROLL, count=5),  # пунша   # noqa: ERA001
    # effects.Effect(name=Scroll.STONE_SKIN, type_=effects.ElementType.CASTLE),  # noqa: ERA001
    # effects.Effect(name=Scroll.STONE_SKIN, type_=effects.ElementType.CASTLE),  # noqa: ERA001
    # effects.Effect(name=Scroll.STONE_SKIN, type_=effects.ElementType.CASTLE),  # noqa: ERA001
]


FULL_WARRIOR = [
    effects.Effect(name=Potion.IMMUNITY, type_=effects.ElementType.POTION),
    effects.Effect(name=Potion.EXCELLENT_SHELL, type_=effects.ElementType.POTION, count=4),
    effects.Effect(name=Elixir.POTION_BLOODTHIRSTY, type_=effects.ElementType.POTION, count=2),
    effects.Effect(name=Elixir.SWIFTNESS, type_=effects.ElementType.SCROLL, count=2),
    # effects.Effect(name=Elixir.SWIFTNESS, type_=effects.ElementType.SCROLL, count=2),  # 2 льда  # noqa: ERA001
    # effects.Effect(name=Scroll.STONE_SKIN, type_=effects.ElementType.CASTLE),  # noqa: ERA001
    # effects.Effect(name=Scroll.STONE_SKIN, type_=effects.ElementType.CASTLE),  # noqa: ERA001
    # effects.Effect(name=Scroll.STONE_SKIN, type_=effects.ElementType.CASTLE),  # noqa: ERA001
]
