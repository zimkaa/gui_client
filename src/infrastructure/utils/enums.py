from enum import StrEnum


class CaseInsensitiveEnum(StrEnum):
    @classmethod
    def _missing_(cls, value):  # noqa: ANN206, ANN001, ANN102
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None
