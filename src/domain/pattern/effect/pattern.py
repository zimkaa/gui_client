from typing import Final


FIND_VAR_EFF: Final[str] = r"(?<=var eff = \[\[).+(?=]];)"

FIND_EFFECTS_INFO_PATTERN: Final[str] = r"(?<=effects_view\(\[).+(?=\],)"

PATTERN_COUNT: Final[str] = r"(?<= \(x)\d{1,2}(?=\))"

PATTERN_PART_TIME: Final[str] = r"\d{2}"

PATTERN_EFFECT_NAME: Final[str] = r".+(?= \(x)"
