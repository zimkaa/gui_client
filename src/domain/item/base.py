from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.domain.item.actions import ActionVariants
    from src.domain.item.property import PropertyVariants
    from src.domain.item.requirements import RequirementsVariants


@dataclass
class NeverItem:
    name: str
    property: dict[PropertyVariants, str] | None = None
    requirements: dict[RequirementsVariants, str] | None = None
    actions: dict[ActionVariants, str] | None = None
