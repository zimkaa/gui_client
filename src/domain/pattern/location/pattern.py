from typing import Final


FIND_IN_CITY: Final[str] = r"(?<=Инвентарь\" onclick=\"location=\'main\.php\?).+(?=\'\">)"

FIND_FROM_NATURE_TO_INV: Final[str] = r"(?<=Инвентарь\",\")\w+(?=\",\[\]\]|\",\[\]\],)"

FIND_PAGE_INVENTAR: Final[str] = r"(?<=&go=inv&vcode=).+(?=\'\" value=\"Инвентарь)"

PATTERN_PERSONS_ON_CELL_GROUP: Final[str] = (
    r"\"(.{1,33}):(.{1,33}):(\d{1,3}):(\w{1,6}\.gif;(.{1,30});.{0,35})?:(\d|.{1,10000}):(\d|.{1,10000}):(\d|.{1,10000}):(\d|.{1,10000}):(0|\w{1,10}\.gif;.{1,30})\"[,|\)]"
    # r"\"(.{1,33}):(.{1,33}):(\d{1,3}):\w{1,6}\.gif;(.{1,30});.{0,35}:(\d|.{1,10000}):(\d|.{1,10000}):(\d|.{1,10000}):(\d|.{1,10000}):\w{1,10}\.gif;.{1,30}\"[,|\)]"  # noqa: ERA001, E501  # in use GAME
    # r"\"(.{1,33}:.{1,33}:\d{1,3}):\w{1,6}\.gif;(.{1,30});.{1,35}:(\d:\d:\d:\d):\w{1,10}\.gif;.{1,30}\"[,|)]"  # noqa: ERA001, E501
)

FIND_FRAME = r'<SCRIPT src="./js/fight_v10.js"></SCRIPT>'
