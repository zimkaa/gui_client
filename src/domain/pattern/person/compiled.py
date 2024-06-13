import re

from . import pattern


var_effects = re.compile(pattern.FIND_VAR_EFF)

var_effects2 = re.compile(pattern.FIND_STATS2)

find_stats = re.compile(pattern.FIND_STATS)

find_effects_info = re.compile(pattern.FIND_EFFECTS_INFO_PATTERN)
