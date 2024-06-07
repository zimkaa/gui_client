from typing import Final


# OLD variant
# WHOLE_INV_INFO: Final[str] = (
#     r"(?<=<font class=inv><b>Масса Вашего инвентаря:).+(?=</tr></table></td></tr></table></td></tr></table></td></tr>)"  # noqa: RUF001, ERA001, RUF003, RUF100, E501
# )  # noqa: ERA001, RUF100

# OLD variant
# ITEM_NAME: Final[str] = (
#     r"(?<=<font class=nickname>).*?(?=<img src=http://image.neverlands.ru/1x1.gif width=5 height=1></td>)"  # noqa: ERA001, E501
# )  # noqa: ERA001, RUF100

# OLD variant
# ALL_ITEMS: Final[str] = r"(?<=<font class=nickname><b> ).*?(?=</b><br>)"  # noqa: ERA001

# OLD variant
# ALL_ITEMS_FILL_INFO: Final[str] = r"(?<=td colspan=2 width=100%>).*?(?=</tr></table></td>)"  # noqa: ERA001

ALL_ITEMS_FULL_INFO: Final[str] = (
    r"(?<=<table cellpadding=0 cellspacing=0 border=0 width=100%>).*?font class=nickname.*?(?=</tr></table></td>)"
)

ITEM_NAME: Final[str] = r"class=nickname><b>([^<>]+)<"

PROPERTY_AND_REQUIREMENTS: Final[str] = r"(?<=font class=weaponch).*?(?=img src=http://image.neverlands.ru/1x1.gif)"

EVERY_TEXT_IN_TAG_BRACKETS: Final[str] = r">([^<>]+)<"

EVERY_ACTION: Final[str] = r"<input[^>]*onclick=\"([^\"]+)\"[^>]*value=\"([^\"]+)\""
