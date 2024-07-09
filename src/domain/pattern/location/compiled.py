import re

from . import pattern


finder_in_city = re.compile(pattern.FIND_IN_CITY)

finder_nature_to_inv = re.compile(pattern.FIND_FROM_NATURE_TO_INV)

finder_inv = re.compile(pattern.FIND_PAGE_INVENTORY)

person_om_cell_group = re.compile(pattern.PATTERN_PERSONS_ON_CELL_GROUP)

finder_frame = re.compile(pattern=pattern.FIND_FRAME)

finder_use = re.compile(pattern=pattern.FIND_USE)

finder_teleport = re.compile(pattern=pattern.FIND_TELEPORT)

finder_vcode_bait = re.compile(pattern=pattern.FIND_BAIT_VCODE)

finder_bcodes = re.compile(pattern=pattern.FIND_BCODES)

finder_page_ability = re.compile(pattern=pattern.PAGE_ABILITY)

finder_return_vcode = re.compile(pattern=pattern.FIND_RETURN_VCODE)

finder_request_add = re.compile(pattern=pattern.FIND_REQUEST_ADD)

finder_vcode_castle = re.compile(pattern=pattern.FIND_VCODE_CASTLE)
