from typing import Final

from src.infrastructure.utils.enums import CaseInsensitiveEnum


USE_NAME: Final[str] = "Использовать"
DROP_NAME: Final[str] = "x"
PUT_ON_NAME: Final[str] = "Надеть"
TRANSFER_NAME: Final[str] = "Передать"
GIVE_NAME: Final[str] = "Подарить"
SELL_NAME: Final[str] = "Продать"

HEAL_MINOR_NAME: Final[str] = "Лечить лёгкую травму"
HEAL_AVERAGE_NAME: Final[str] = "Лечить среднюю травму"
HEAL_SEVERE_NAME: Final[str] = "Лечить тяжелую травму"
HEAL_COMBAT_NAME: Final[str] = "Лечить боевую травму"

BIND_TO_POINT_NAME: Final[str] = "Привязать к точке"


class ActionVariants(CaseInsensitiveEnum):
    USE = USE_NAME
    DROP = DROP_NAME
    PUT_ON = PUT_ON_NAME
    TRANSFER = TRANSFER_NAME
    GIVE = GIVE_NAME
    SELL = SELL_NAME

    HEAL_MINOR = HEAL_MINOR_NAME
    HEAL_AVERAGE = HEAL_AVERAGE_NAME
    HEAL_SEVERE = HEAL_SEVERE_NAME
    HEAL_COMBAT = HEAL_COMBAT_NAME

    BIND_TO_POINT = BIND_TO_POINT_NAME
