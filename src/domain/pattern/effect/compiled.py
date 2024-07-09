import re

from . import pattern


finder_var_eff = re.compile(pattern.FIND_VAR_EFF)

finder_eff_info = re.compile(pattern.FIND_EFFECTS_INFO_PATTERN)

finder_eff_count = re.compile(pattern.PATTERN_COUNT)

finder_eff_time = re.compile(pattern.PATTERN_PART_TIME)

finder_eff_name = re.compile(pattern.PATTERN_EFFECT_NAME)

finder_name_count_time = re.compile(pattern.FIND_NAME_COUNT_TIME)

finder_ability_1 = re.compile(pattern.FIND_ABILITY_1)

finder_all_clan_ability = re.compile(pattern.FIND_ALL_CLAN_ABILITY)
