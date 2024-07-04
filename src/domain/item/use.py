from enum import IntEnum

from .elixir import Elixir
from .scroll import Scroll


binding_dict = {
    Scroll.STONE_SKIN: 20,
    Scroll.SCROLL_OF_MAJESTY: 21,
    Scroll.ANCIENT_SCROLL_OF_MAJESTY: 21,
    Scroll.TELEPORT_DIRE_SWAMP: 33,
    Scroll.TELEPORT_FORT_RUSTLING_LEAVES: 33,
    Scroll.TELEPORT_ISLAND_TUROTOR: 33,
    Scroll.WRATH_OF_LOKAR: 78,
    Scroll.SCROLL_OF_PATRONAGE_3H: 79,
    Scroll.FESTIVE_PATRONAGE: 79,
    Scroll.SCROLL_OF_INEVITABILITY_3H: 80,
    Scroll.FESTIVE_INEVITABILITY: 80,
    Scroll.SCROLL_OF_PURIFICATION: 82,
    Scroll.DOOR_OF_DIMENSIONS: 87,
    Scroll.WIND_MAGIC: 92,
    Scroll.WATER_MAGIC: 93,
    Scroll.FIRE_MAGIC: 94,
    Scroll.EARTH_MAGIC: 95,
    Elixir.RESTORATION: 101,  # Эликсир восстановления
    Elixir.BOT_BAIT: 102,  # Приманку Для Ботов
    Elixir.CHAMPAGNE_BOTTLE: 103,  # Бутылку Шампанского
    Elixir.INSTANT_HEALING: 104,  # Эликсир Мгновенного Исцеления
    Elixir.POTION_BLOODTHIRSTY: 105,  # Зелье Кровожадности
    Elixir.SWIFTNESS: 106,  # Эликсир Быстроты
    Elixir.BLISS: 107,  # Эликсир Блаженства
    Elixir.ILANAS_GIFT: 108,  # Дар Иланы
    Elixir.SNOWDROP: 109,  # Эликсир из Подснежника
    Elixir.YOUTH: 110,  # Молодильное яблочко
    Elixir.IRIS_BOWL: 141,
    Elixir.PLANAR_SUMMONING: 152,  # Планарный призыв!!!
    Elixir.FAROS_WINE: 156,  # Фаросское Вино
    Elixir.FIRE_ENHANCEMENT: 161,  # Усиление огня
    Scroll.SUMMON_HELPER_IMP: 165,
}


class UseBinding(IntEnum):
    STONE_SKIN = 20

    SCROLL_OF_MAJESTY = 21
    ANCIENT_SCROLL_OF_MAJESTY = 21
    TELEPORT_DIRE_SWAMP = 33
    TELEPORT_FORT_RUSTLING_LEAVES = 33
    TELEPORT_ISLAND_TUROTOR = 33
    WRATH_OF_LOKAR = 78
    SCROLL_OF_PATRONAGE_3H = 79
    FESTIVE_PATRONAGE = 79
    SCROLL_OF_INEVITABILITY_3H = 80
    FESTIVE_INEVITABILITY = 80
    SCROLL_OF_PURIFICATION = 82
    DOOR_OF_DIMENSIONS = 87

    WIND_MAGIC = 92
    WATER_MAGIC = 93
    FIRE_MAGIC = 94
    EARTH_MAGIC = 95

    RESTORATION = 101  # Эликсир восстановления
    BOT_BAIT = 102  # Приманку Для Ботов
    CHAMPAGNE_BOTTLE = 103  # Бутылку Шампанского
    INSTANT_HEALING = 104  # Эликсир Мгновенного Исцеления
    POTION_BLOODTHIRSTY = 105  # Зелье Кровожадности
    SWIFTNESS = 106  # Эликсир Быстроты
    BLISS = 107  # Эликсир Блаженства
    ILANAS_GIFT = 108  # Дар Иланы
    SNOWDROP = 109  # Эликсир из Подснежника
    YOUTH = 110  # Молодильное яблочко
    IRIS_BOWL = 141
    PLANAR_SUMMONING = 152  # Планарный призыв!!!
    FAROS_WINE = 156  # Фаросское Вино
    FIRE_ENHANCEMENT = 161  # Усиление огня

    SUMMON_HELPER_IMP = 165
