from typing import Final


FIND_IN_CITY: Final[str] = r"(?<=Инвентарь\" onclick=\"location=\'main\.php\?).+(?=\'\">)"

FIND_FROM_NATURE_TO_INV: Final[str] = r"(?<=Инвентарь\",\")\w+(?=\",\[\]\]|\",\[\]\],)"

FIND_PAGE_INVENTORY: Final[str] = r"(?<=&go=inv&vcode=).+(?=\'\" value=\"Инвентарь)"

PATTERN_PERSONS_ON_CELL_GROUP: Final[str] = (
    r"\"(.{1,33}):(.{1,33}):(\d{1,3}):(\w{1,6}\.gif;(.{1,30});.{0,35})?:(\d|.{1,10000}):(\d|.{1,10000}):(\d|.{1,10000}):(\d|.{1,10000}):(0|\w{1,10}\.gif;.{1,30})\"[,|\)]"
    # r"\"(.{1,33}):(.{1,33}):(\d{1,3}):\w{1,6}\.gif;(.{1,30});.{0,35}:(\d|.{1,10000}):(\d|.{1,10000}):(\d|.{1,10000}):(\d|.{1,10000}):\w{1,10}\.gif;.{1,30}\"[,|\)]"  # noqa: ERA001, E501  # in use GAME
    # r"\"(.{1,33}:.{1,33}:\d{1,3}):\w{1,6}\.gif;(.{1,30});.{1,35}:(\d:\d:\d:\d):\w{1,10}\.gif;.{1,30}\"[,|)]"  # noqa: ERA001, E501
)

FIND_FRAME: Final[str] = r'<SCRIPT src="./js/fight_v10.js"></SCRIPT>'

FIND_USE: Final[str] = r"(?<=w28_form\(').+(?='\)\")"

FIND_TELEPORT: Final[str] = r"(?<=http://image\.neverlands\.ru/weapon/i_w28_22\.gif).+?\">"

FIND_CITY_ACTION_VCODE_PART1: Final[str] = r"(?<=HREF=\"main\.php\?get_id=56&act=10&go="

FIND_CITY_ACTION_VCODE_PART2: Final[str] = r"&vcode=).+(?=\" COORDS=\")"

FIND_BAIT_VCODE: Final[str] = r"(?<=get_id=56&act=10&go=build&pl=citydef2&vcode=).+(?=\" COORDS)"

FIND_BCODES: Final[str] = r"(?<=var bcodes = ).+(?=;)"

FIND_REQUEST_ADD: Final[str] = r"(?<=var objActions = ).+(?=;)"

FIND_RETURN_VCODE: Final[str] = r"(?<=get_id=56&act=10&go=ret&vcode=).+?(?='\" value=\"Вернуться\">)"

FIND_VCODE_CASTLE: Final[str] = r"(?<=var vcode = ).+?(?=;)"
