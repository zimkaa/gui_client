import re

from . import pattern


finder_fexp = re.compile(pattern.FIND_FEXP)

finder_error = re.compile(pattern.FIND_ERROR)

finder_param_ow = re.compile(pattern.FIND_PARAM_OW)

finder_dead_hit = re.compile(pattern.FIND_DEAD_HIT)

finder_logs = re.compile(pattern.FIND_LOGS)

finder_params = re.compile(pattern.FIND_PARAMS)

off_is = re.compile(pattern.PATTERN_OFF)

group1 = re.compile(pattern.PATTERN_LIVES_G1)

group2 = re.compile(pattern.PATTERN_LIVES_G2)
