from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from datetime import timedelta
from enum import StrEnum
from enum import auto
from typing import TYPE_CHECKING

from src.config import logger
from src.domain.item.potion import Potion
from src.domain.item.potion import equivalent_potion_dict
from src.domain.pattern.effect import compiled
from src.infrastructure.errors import effect
from src.use_cases.person.buff.constants import MAX_POTION_USE


if TYPE_CHECKING:
    from src.domain.item.elixir import Elixir
    from src.domain.item.scroll import Scroll


class ElementType(StrEnum):
    POTION = auto()
    SCROLL = auto()
    ELIXIR = auto()
    CASTLE = auto()


@dataclass
class EffectCountAndTime:
    time_delta: timedelta
    count: int


@dataclass
class Effect:
    name: str | Scroll | Elixir | Potion
    type_: ElementType
    count: int = 1
    equivalent: str = ""

    def __post_init__(self) -> None:
        self.equivalent = equivalent_potion_dict.get(self.name) or self.name


class PersonEffects:
    def __init__(self, *, page_text: str, need_effects: list[Effect]) -> None:
        self.page_text: str = page_text
        self.need_effects = need_effects
        self.active_effects: dict[str, EffectCountAndTime] = {}
        self.effects_to_use: list[Effect] = []

    def _match_needs_and_active(self) -> None:
        for need_effect in self.need_effects:
            if element := self.active_effects.get(need_effect.equivalent):
                count = element.count
                if count != need_effect.count:
                    if count == MAX_POTION_USE:
                        raise effect.EffectMaxCountError
                    if count < need_effect.count:
                        new_count = need_effect.count - count
                        new_effect = Effect(name=need_effect.name, count=new_count, type_=need_effect.type_)
                        self.effects_to_use.append(new_effect)
                    if count > need_effect.count:
                        raise effect.ActiveEffectCountMoreError
                else:
                    logger.debug(f"Effect {need_effect.name} already active")
            else:
                new_effect = deepcopy(need_effect)
                self.effects_to_use.append(new_effect)

    def get_effects(self) -> list[Effect] | None:
        logger.debug("get_effects  START!!!!")
        self._find_effects()
        self._match_needs_and_active()
        if self.effects_to_use:
            logger.debug(f"{self.effects_to_use=}")
            return self.effects_to_use
        return None

    def _compute_timedelta(self, time_str: str) -> timedelta:
        parts = time_str.split(":")

        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])

        total_seconds = hours * 3600 + minutes * 60 + seconds

        return timedelta(seconds=total_seconds)

    def _find_effects(self) -> None:
        logger.debug("_find_effects  START!!!!")
        result = compiled.finder_name_count_time.findall(self.page_text)
        for name, count, time_str in result:
            time_delta = self._compute_timedelta(time_str)
            self.active_effects[name] = EffectCountAndTime(count=int(count), time_delta=time_delta)
            logger.debug(f"{name=} {count=} {time_delta=!s}")
