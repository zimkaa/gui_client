from typing import Final


FIND_VAR_EFF: Final[str] = r"(?<=var eff = \[\[).+(?=]];)"

FIND_STATS: Final[str] = r"(?<=var parameters = \[\[).+(?=\]\]\];\nvar slots )"

FIND_STATS2: Final[str] = r"(?<=var parameters = ).+(?=;\nvar slots )"
