from typing import Final


FIND_FEXP: Final[str] = r"(?<=fexp = \[).+(?=];)"

FIND_ERROR: Final[str] = r"error.css"

FIND_PARAM_OW: Final[str] = r"(?<=param_ow = \[).+(?=];)"

FIND_DEAD_HIT: Final[str] = r"(?<=\</B\> \[).+(?=\]\.)"

FIND_LOGS: Final[str] = r"(?<=var logs = ).+(?=;)"

FIND_PARAMS: Final[str] = r"(?<=var params = ).+(?=;)"

PATTERN_OFF: Final[str] = r"(?<=off = )\d+(?=;)"

PATTERN_LIVES_G1: Final[str] = r"(?<=lives_g1 = \[).+(?=];)|(?<=lives_g1 = \[).+\n.+(?=];)"

PATTERN_LIVES_G2: Final[str] = r"(?<=lives_g2 = \[).+(?=];)|(?<=lives_g2 = \[).+\n.+(?=];)"
