from __future__ import annotations
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from enum import auto

from src.config import logger


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, element: Element) -> None:
        pass


class AbstractHandler(Handler):
    _next_handler: Handler | None = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, element: Element) -> None:
        if self._next_handler:
            self._next_handler.handle(element)


class PotionHandler(AbstractHandler):
    def handle(self, element: Element) -> None:
        logger.error(f"START PotionHandler {element=}")
        if element.type_ == ElementType.POTION:
            for _ in range(element.count):
                logger.error(f"use {element.name=}")
        else:
            logger.error(f"PotionHandler go to next handler {element=}")
            super().handle(element)


class ScrollHandler(AbstractHandler):
    def handle(self, element: Element) -> None:
        logger.error(f"START ScrollHandler {element=}")
        if element.type_ == ElementType.SCROLL:
            for _ in range(element.count):
                logger.error(f"use {element.name=}")
        else:
            logger.error(f"ScrollHandler go to next handler {element=}")
            super().handle(element)


class ElementType(StrEnum):
    POTION = auto()
    SCROLL = auto()
    ELIXIR = auto()


@dataclass
class Element:
    name: str
    count: int
    type_: ElementType


def use_effects(handler: Handler) -> None:
    e1 = Element("Зелье Иммунитета", 1, ElementType.POTION)
    e2 = Element("Превосходное Зелье Ловких Ударов", 2, ElementType.POTION)
    e3 = Element("Превосходное Зелье Жизни", 2, ElementType.POTION)
    e4 = Element("Свиток каменной кожи", 2, ElementType.SCROLL)
    elements = [e1, e4, e2, e3]
    for element in elements:
        handler.handle(element)


def check_effects(handler: Handler) -> None:
    e1 = Element("Зелье Иммунитета", 1, ElementType.POTION)
    e2 = Element("Превосходное Зелье Ловких Ударов", 2, ElementType.POTION)
    e3 = Element("Превосходное Зелье Жизни", 2, ElementType.POTION)
    e4 = Element("Свиток каменной кожи", 2, ElementType.SCROLL)
    elements = [e1, e4, e2, e3]
    for element in elements:
        handler.handle(element)


if __name__ == "__main__":
    potion = PotionHandler()
    scroll = ScrollHandler()

    potion.set_next(scroll)

    use_effects(potion)
