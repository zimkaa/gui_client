from typing import Final


URL: Final[str] = "http://neverlands.ru"
URL_LOG: Final[str] = URL + "/logs.fcg"
URL_GAME: Final[str] = URL + "/game.php"
URL_MAIN: Final[str] = URL + "/main.php"
URL_EVENT: Final[str] = URL + "/gameplay/ajax/event.php"
URL_KEEP_CONNECTION: Final[str] = URL + "/ch.php?{rand_float}&show=1&fyo=0"
URL_PLAYER_INFO: Final[str] = URL + "/pinfo.cgi?{name}"
URL_SELL_INFO: Final[str] = URL + "/ch.php?lo=1&"

URL_INV: Final[str] = URL_MAIN + "?wca=28"
URL_PHARMACY: Final[str] = URL_MAIN + "?wca=85"
URL_ELIXIR: Final[str] = URL_MAIN + "?im=6"
