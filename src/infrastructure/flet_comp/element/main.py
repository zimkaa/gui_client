from collections.abc import Callable
from collections.abc import Coroutine
from typing import Any

import flet as ft


class GreetingText(ft.Text):
    def __init__(self, login: str, **kwargs) -> None:
        if "selectable" not in kwargs:
            kwargs["selectable"] = True

        if "value" in kwargs:
            kwargs.pop("value")

        super().__init__(value=f"Hello, {login}!", **kwargs)


class LogOutButton(ft.ElevatedButton):
    def __init__(self, on_click: Callable[[Any], Coroutine[Any, Any, None]], **kwargs) -> None:
        if "text" not in kwargs:
            kwargs["text"] = "LogOut"

        super().__init__(on_click=on_click, **kwargs)


class PotionText(ft.Text):
    def __init__(self, **kwargs) -> None:
        if "selectable" not in kwargs:
            kwargs["selectable"] = True

        super().__init__(**kwargs)


class LogOutText(ft.Text):
    def __init__(self, **kwargs) -> None:
        if "value" not in kwargs:
            kwargs["value"] = "LogOut"

        super().__init__(**kwargs)


class TopBar(ft.AppBar):
    def __init__(self, **kwargs) -> None:
        if "bgcolor" not in kwargs:
            kwargs["bgcolor"] = ft.colors.SURFACE_VARIANT

        if "center_title" not in kwargs:
            kwargs["center_title"] = True

        if "title" not in kwargs:
            kwargs["title"] = LogOutText()
        elif isinstance(kwargs["title"], str):
            kwargs["title"] = LogOutText(value=kwargs["title"])
        elif isinstance(kwargs["title"], int):
            kwargs["title"] = LogOutText(value=str(kwargs["title"]))

        super().__init__(**kwargs)


class ClanItemsButton(ft.ElevatedButton):
    def __init__(self, on_click: Callable[[Any], Coroutine[Any, Any, None]], **kwargs) -> None:
        if "text" not in kwargs:
            kwargs["text"] = "Clan item"

        super().__init__(on_click=on_click, **kwargs)


class BuffButton(ft.ElevatedButton):
    def __init__(self, on_click: Callable[[Any], Coroutine[Any, Any, None]], **kwargs) -> None:
        if "text" not in kwargs:
            kwargs["text"] = "Use default buff"

        super().__init__(on_click=on_click, **kwargs)


class Status(ft.Text):
    def __init__(self, status: str, **kwargs) -> None:
        super().__init__(value=f"Status={status}", **kwargs)


class UseStatus(ft.Text):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class GoToBaitButton(ft.ElevatedButton):
    def __init__(self, on_click: Callable[[Any], Coroutine[Any, Any, None]], **kwargs) -> None:
        if "text" not in kwargs:
            kwargs["text"] = "Start Bait"

        super().__init__(on_click=on_click, **kwargs)


class BaitStatus(ft.Text):
    def __init__(self, **kwargs) -> None:
        if "value" not in kwargs:
            kwargs["value"] = "Bait Not started"

        super().__init__(**kwargs)


class StartABButton(ft.ElevatedButton):
    def __init__(self, on_click: Callable[[Any], Coroutine[Any, Any, None]], **kwargs) -> None:
        if "text" not in kwargs:
            kwargs["text"] = "Start AB"

        super().__init__(on_click=on_click, **kwargs)


class ABStatus(ft.Text):
    def __init__(self, **kwargs) -> None:
        if "value" not in kwargs:
            kwargs["value"] = "AB Not started"

        super().__init__(**kwargs)
