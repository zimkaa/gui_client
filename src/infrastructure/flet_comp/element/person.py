from collections.abc import Callable
from collections.abc import Coroutine
from typing import Any

import flet as ft


class BuffButton(ft.ElevatedButton):
    def __init__(self, on_click: Callable[[Any], Coroutine[Any, Any, None]], **kwargs) -> None:
        if "text" not in kwargs:
            kwargs["text"] = "Start buffing"

        super().__init__(on_click=on_click, **kwargs)


class UserSwitch(ft.Switch):
    def __init__(self, login: str, **kwargs) -> None:
        if "value" not in kwargs:
            kwargs["value"] = True

        super().__init__(label=f"{login}", **kwargs)


class StatusText(ft.Text):
    def __init__(self, **kwargs) -> None:
        if "selectable" not in kwargs:
            kwargs["selectable"] = True

        if "value" in kwargs:
            kwargs.pop("value")

        super().__init__(value="   Статус   ", **kwargs)


class PersonsText(ft.Text):
    def __init__(self, **kwargs) -> None:
        if "selectable" not in kwargs:
            kwargs["selectable"] = True

        super().__init__(**kwargs)


class UseStatus(ft.Text):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class ConfigChoice(ft.Dropdown):
    def __init__(self, **kwargs) -> None:
        if "width" not in kwargs:
            kwargs["width"] = 200

        if "value" not in kwargs:
            kwargs["value"] = "ТЕСТ"  # noqa: RUF001

        super().__init__(**kwargs)
