from __future__ import annotations
import json
from collections import defaultdict
from collections.abc import Iterator
from pathlib import Path

from typing_extensions import Self

from src.config import logger
from src.domain.item.actions import ActionVariants
from src.domain.item.base import NeverItem
from src.domain.item.property import PropertyVariants
from src.domain.item.requirements import RequirementsVariants
from src.domain.pattern.inv import compiled


class IdenticalItemCollection:
    __instance: Self | None = None

    def __new__(cls):  # noqa: ANN204
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.items: dict[str, int] = defaultdict(int)

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> Iterator[str]:
        return iter(self.items)

    def add_item(self, name: str) -> None:
        self.items[name] += 1

    def get_item(self, name: str) -> int | None:
        return self.items.get(name)

    def __repr__(self) -> str:
        sorted_items = sorted(self.items.items(), key=lambda x: x[1], reverse=True)
        return "\n".join(f"{key} - {value}" for key, value in sorted_items)


def get_groups(text: str) -> list[str]:
    return compiled.finder_property_and_request.findall(text)


def get_requirement_elements(text: str) -> dict[RequirementsVariants, str]:
    text_matches: list[str] = compiled.finder_every_text_in_tag_brackets.findall(text)

    item: dict[RequirementsVariants, str] = {}
    previous = ""
    for match in text_matches:
        clear_string = match.strip()

        if previous and previous.endswith(":"):
            item_key = RequirementsVariants(previous.replace(":", "").replace("&nbsp;", " ").strip())
            if item_key == RequirementsVariants.CLAN:
                continue
            item[item_key] = f"+{clear_string}"

        previous = clear_string

    return item


def get_property_elements(text: str) -> dict[PropertyVariants, str]:
    text_matches: list[str] = compiled.finder_every_text_in_tag_brackets.findall(text)

    item = {}
    previous = ""
    for match in text_matches:
        clear_string = match.strip()

        if previous:
            if previous.endswith(": +"):
                item_key = PropertyVariants(previous.replace(": +", "").replace("&nbsp;", " ").strip())
                item[item_key] = f"+{clear_string}"
            elif previous.endswith(":"):
                item_key = PropertyVariants(previous.replace(":", "").replace("&nbsp;", " ").strip())
                item[item_key] = f"+{clear_string}"
            elif previous.endswith(": -"):
                item_key = PropertyVariants(previous.replace(": -", "").replace("&nbsp;", " ").strip())
                item[item_key] = f"-{clear_string}"

        previous = clear_string

    return item


def get_action_elements(text: str) -> dict[ActionVariants, str] | None:
    text_matches: list[tuple[str, str]] = compiled.finder_every_action.findall(text)

    if not text_matches:
        return None

    item = {}
    for match in text_matches:
        (onclick, value) = match

        item_key = ActionVariants(value.replace("&nbsp;", " ").strip())
        item[item_key] = onclick

    return item


def get_items(search_result: list[str]) -> tuple[list[NeverItem], IdenticalItemCollection]:
    identical_item_collection = IdenticalItemCollection()
    items: list[NeverItem] = []
    for i, item in enumerate(search_result):
        text_matches = compiled.finder_item_name.findall(item)
        try:
            (group_property, group_requirements) = get_groups(item)
        except Exception as e:
            logger.error("i=%s item=%s error=%s", i, item, e)
            raise
        try:
            property_elements = get_property_elements(group_property)
        except Exception as e:
            logger.error("i=%s item=%s error=%s", i, item, e)
            raise
        try:
            requirements_elements = get_requirement_elements(group_requirements)
        except Exception as e:
            logger.error("i=%s item=%s error=%s", i, item, e)
            raise
        actions_elements = get_action_elements(item)

        # if not actions_elements:
        #     logger.error(f"{i=} {item=}")  # noqa: ERA001

        name = text_matches.pop(0).strip()
        identical_item_collection.add_item(name)
        items.append(
            NeverItem(
                name=name,
                property=property_elements,
                requirements=requirements_elements,
                actions=actions_elements,
            ),
        )
    return items, identical_item_collection


def add_to_unique_items(identical_item_collection: IdenticalItemCollection) -> None:
    with Path("./store/unique_item_names.json").open("r+") as f:
        j_file = json.load(f)

        set_names_in_file = set(j_file)
        set_names_from_request = {
            element.replace(" (+1)", "")
            .replace(" (+2)", "")
            .replace(" (+3)", "")
            .replace(" (+4)", "")
            .replace(" (+5)", "")
            for element in identical_item_collection
        }

        set_names_in_file.update(set_names_from_request)
        j_file = list(set_names_in_file)

        f.seek(0)
        json.dump(j_file, f, indent=4, ensure_ascii=False)
