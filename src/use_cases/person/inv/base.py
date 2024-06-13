from __future__ import annotations
from typing import TYPE_CHECKING

from src.config import logger
from src.use_cases.item.base import get_items


if TYPE_CHECKING:
    from src.use_cases.person.buff.effects import Effect


class PersonInv:
    def __init__(self, *, page_text: str, effects_to_use: list[Effect]) -> None:
        self.page_text: str = page_text
        self.effects_to_use = effects_to_use
        self.no_elements: list[Effect] = []
        self.main_items_page: list[str] = []
        self.elixir_items_page: list[str] = []

    def _find_main_items(self) -> None:
        self.main_items, self.identical_item_collection = get_items(self.main_items_page)

    def _find_elixir_items(self) -> None:
        (self.elixir_items, _) = get_items(self.elixir_items_page, self.identical_item_collection)

    def set_main_items_page(self, page_text: list[str]) -> None:
        self.main_items_page = page_text

    def set_elixir_items_page(self, page_text: list[str]) -> None:
        self.elixir_items_page = page_text

    def _all_items(self) -> None:
        if self.elixir_items_page and self.main_items_page:
            self._find_main_items()
            self._find_elixir_items()

    def _check_elements(self) -> None:
        no_items = []
        for element in self.effects_to_use:
            if (
                self.identical_item_collection.get_item(element.name) is None
                and self.identical_item_collection.get_item(element.equivalent) is None
            ):
                logger.error(f"no element {element.name} in inventar")
                no_items.append(element)

    def check_elements(self) -> None:
        self._all_items()
        self._check_elements()
