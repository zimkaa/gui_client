from typing import Final


URL: Final[str] = "http://neverlands.ru"
URL_LOG: Final[str] = URL + "/logs.fcg"
URL_GAME: Final[str] = URL + "/game.php"
URL_MAIN: Final[str] = URL + "/main.php"
URL_EVENT: Final[str] = URL + "/gameplay/ajax/event.php"
URL_CASTLE: Final[str] = URL + "/gameplay/ajax/castle_ajax.php"
URL_KEEP_CONNECTION: Final[str] = URL + "/ch.php?{rand_float}&show=1&fyo=0"
URL_PLAYER_INFO: Final[str] = URL + "/pinfo.cgi?{name}"
URL_SELL_INFO: Final[str] = URL + "/ch.php?lo=1&"

# filters
URL_POTION: Final[str] = URL_MAIN + "?wca=27"
URL_INV: Final[str] = URL_MAIN + "?wca=28"
URL_SCROLL: Final[str] = URL_MAIN + "?wca=28"
URL_PHARMACY: Final[str] = URL_MAIN + "?wca=85"

URL_ALL_ITEMS: Final[str] = URL_MAIN + "?im=0"
URL_ALCHEMY: Final[str] = URL_MAIN + "?im=1"
URL_FISH: Final[str] = URL_MAIN + "?im=2"
URL_HUNT: Final[str] = URL_MAIN + "?im=3"
URL_CARPENTRY_EQUIPMENT: Final[str] = URL_MAIN + "?im=4"  # Плотник деревообработка
URL_COOKING_EQUIPMENT: Final[str] = URL_MAIN + "?im=5"
URL_ELIXIR: Final[str] = URL_MAIN + "?im=6"
URL_QUESTS: Final[str] = URL_MAIN + "?im=7"
