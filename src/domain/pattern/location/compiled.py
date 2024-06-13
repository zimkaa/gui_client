import re

from . import pattern


finder_in_city = re.compile(pattern.FIND_IN_CITY)

finder_nature_to_inv = re.compile(pattern.FIND_FROM_NATURE_TO_INV)

finder_inv = re.compile(pattern.FIND_PAGE_INVENTAR)

person_om_cell_group = re.compile(pattern.PATTERN_PERSONS_ON_CELL_GROUP)

finder_frame = re.compile(pattern=pattern.FIND_FRAME)
