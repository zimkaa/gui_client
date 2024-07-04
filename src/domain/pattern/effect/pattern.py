from typing import Final


FIND_VAR_EFF: Final[str] = r"(?<=var eff = \[\[).+(?=]];)"

FIND_EFFECTS_INFO_PATTERN: Final[str] = r"(?<=effects_view\(\[).+(?=\],)"

PATTERN_COUNT: Final[str] = r"(?<= \(x)\d{1,2}(?=\))"

PATTERN_PART_TIME: Final[str] = r"\d{2}"

PATTERN_EFFECT_NAME: Final[str] = r".+(?= \(x)"


FIND_EFFECT_NAME = r">([^<|>]+)</"

name_count_time = r">([^<|>]+)</.+?\(x([^ ]+)\) \(еще ([^<>]+)\)"

FIND_NAME_COUNT_TIME = r"<b>([^<|>]+)</.+?\(x([^ ]+)\) \(еще (\d{,3}:\d\d:\d\d)\)"
