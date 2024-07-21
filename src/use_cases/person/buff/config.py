from __future__ import annotations
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

from src.use_cases.person.buff.effects import Effect
from src.use_cases.person.buff.effects import ElementType
from src.use_cases.person.buff.group import DAMAGE_TOWER
from src.use_cases.person.buff.group import DODGE_TOWER


if TYPE_CHECKING:
    from src.use_cases.person.buff.castle import MagicTower


def _read_config() -> dict[str, dict[str, list[str]]]:
    with Path("./INFO/buff/user.yaml").open() as f:
        return yaml.safe_load(f)


def _get_type(category: str) -> ElementType:
    match category:
        case "potion":
            type_ = ElementType.POTION
        case "scroll":
            type_ = ElementType.SCROLL
        case "elixir":
            type_ = ElementType.ELIXIR
        case "castle":
            type_ = ElementType.CASTLE
        case "castle_hp":
            type_ = ElementType.CASTLE_HP
        case "castle_mp":
            type_ = ElementType.CASTLE_MP
        case "clan_ability":
            type_ = ElementType.CLAN_ABILITY
        case "ability":
            type_ = ElementType.ABILITY
        case _:
            msg = "Unknown category"
            raise Exception(msg)  # noqa: TRY002
    return type_


def _get_castle_buff_elements(castle_type: str) -> list[MagicTower]:
    match castle_type:
        case "воздух":
            elements = DODGE_TOWER
        case "земля":
            raise NotImplementedError
        case "огонь":
            elements = DAMAGE_TOWER
        case "вода":
            raise NotImplementedError
        case _:
            msg = "Unknown castle type"
            raise Exception(msg)  # noqa: TRY002
    return elements


def _convert_config_to_list_effects(elements: list[str], type_: ElementType) -> list[Effect]:
    effects = []

    if type_ == ElementType.CASTLE:
        name, number, castle_type = elements[0].split("|")
        name = name.strip()
        castle_type = castle_type.strip().lower()
        count = int(number.strip())
        castle_elements = _get_castle_buff_elements(castle_type)
        effects.append(Effect(name=name, type_=type_, count=count, castle=castle_elements))
        return effects

    for element in elements:
        name, *number = element.split("|")  # type: ignore[assignment]
        name = name.strip()
        count = int(number[0].strip()) if number else 1
        effects.append(Effect(name=name, type_=type_, count=count))
    return effects


def _convert_config_to_dict_effects(config: dict[str, dict[str, list[str]]]) -> dict[str, list[Effect]]:
    result_dict = {}
    for group_name, elements in config.items():
        group_name_upper = group_name.upper()
        effects = []
        for element_group, value in elements.items():
            type_ = _get_type(element_group)
            effects.extend(_convert_config_to_list_effects(value, type_))
        result_dict[group_name_upper] = effects
    return result_dict


def get_config() -> dict[str, list[Effect]]:
    config = _read_config()
    return _convert_config_to_dict_effects(config)
