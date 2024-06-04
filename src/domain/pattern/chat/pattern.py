from typing import Final


MSG_PATTERN: Final[str] = r"(?<=\.add_msg\().+(?=\);)"

MSG_SPL_PATTERN: Final[str] = r"(?<=<SPL>).+(?=<SPL>)"

MSG_SPAN_PATTERN: Final[str] = r"(?<=<SPAN>).+(?=</SPAN>)"

MSG_COLOR_PATTERN: Final[str] = r"(?<=<font color=.{7}).+(?=</font>)"
