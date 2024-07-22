from typing import Final


FIND_FLASH_PASS: Final[str] = r"(?<=var s = new FlashPass\(document\.getElementById\('canvas'\), ).+?(?=\);)"
