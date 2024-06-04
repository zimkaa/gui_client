import re

from . import pattern


finder_msg = re.compile(pattern.MSG_PATTERN)

finder_spl = re.compile(pattern.MSG_SPL_PATTERN)

finder_span = re.compile(pattern.MSG_SPAN_PATTERN)

finder_color = re.compile(pattern.MSG_COLOR_PATTERN)
