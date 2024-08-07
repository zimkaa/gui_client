from collections.abc import Callable
from collections.abc import Coroutine
from typing import Any

import flet as ft

from src.domain.value_object.classes import PersonType


class MagOrWarrior(ft.Dropdown):
    def __init__(self, **kwargs) -> None:
        if "options" not in kwargs:
            kwargs["options"] = [
                ft.dropdown.Option(PersonType.MAG.name),
                ft.dropdown.Option(PersonType.WARRIOR.name),
            ]

        if "width" not in kwargs:
            kwargs["width"] = 200

        if "value" not in kwargs:
            kwargs["value"] = PersonType.MAG.name

        super().__init__(**kwargs)


class TestText(ft.Text):
    def __init__(self, **kwargs) -> None:
        if "selectable" not in kwargs:
            kwargs["selectable"] = True

        super().__init__(**kwargs)


class LogInText(ft.Text):
    def __init__(self, **kwargs) -> None:
        if "value" not in kwargs:
            kwargs["value"] = "LogIn"

        super().__init__(**kwargs)


class TopBar(ft.AppBar):
    def __init__(self, **kwargs) -> None:
        if "bgcolor" not in kwargs:
            kwargs["bgcolor"] = ft.colors.SURFACE_VARIANT

        if "center_title" not in kwargs:
            kwargs["center_title"] = True

        if "title" not in kwargs:
            kwargs["title"] = LogInText()
        elif isinstance(kwargs["title"], str):
            kwargs["title"] = LogInText(value=kwargs["title"])
        elif isinstance(kwargs["title"], int):
            kwargs["title"] = LogInText(value=str(kwargs["title"]))

        super().__init__(**kwargs)


class LogInButton(ft.ElevatedButton):
    def __init__(self, on_click: Callable[[Any], Coroutine[Any, Any, None]], **kwargs) -> None:
        if "text" not in kwargs:
            kwargs["text"] = "Log in"

        super().__init__(on_click=on_click, **kwargs)


class LabelProxy(ft.Markdown):
    def __init__(self, **kwargs) -> None:
        if "value" not in kwargs:
            kwargs["value"] = "Proxy"

        super().__init__(**kwargs)


class ProxyCheckbox(ft.Checkbox):
    def __init__(self, **kwargs) -> None:
        if "value" not in kwargs:
            kwargs["value"] = True

        super().__init__(**kwargs)


class TextFieldElement(ft.TextField):
    def __init__(self, **kwargs) -> None:
        if "width" not in kwargs:
            kwargs["width"] = 200

        super().__init__(**kwargs)


class IpElement(TextFieldElement):
    def __init__(self, **kwargs) -> None:
        if "label" not in kwargs:
            kwargs["label"] = "proxy ip"

        super().__init__(**kwargs)


class PortElement(TextFieldElement):
    def __init__(self, **kwargs) -> None:
        if "label" not in kwargs:
            kwargs["label"] = "port"

        super().__init__(**kwargs)


class ProxyLoginElement(TextFieldElement):
    def __init__(self, **kwargs) -> None:
        if "label" not in kwargs:
            kwargs["label"] = "login"

        super().__init__(**kwargs)


class ProxyPassElement(TextFieldElement):
    def __init__(self, **kwargs) -> None:
        if "label" not in kwargs:
            kwargs["label"] = "password"

        if "password" not in kwargs:
            kwargs["password"] = True

        super().__init__(**kwargs)


class LoginElement(TextFieldElement):
    def __init__(self, **kwargs) -> None:
        if "label" not in kwargs:
            kwargs["label"] = "Login"

        if "autofocus" not in kwargs:
            kwargs["autofocus"] = True

        super().__init__(**kwargs)


class PasswordElement(TextFieldElement):
    def __init__(self, **kwargs) -> None:
        if "label" not in kwargs:
            kwargs["label"] = "Password"

        if "password" not in kwargs:
            kwargs["password"] = True

        super().__init__(**kwargs)


class FlashElement(TextFieldElement):
    def __init__(self, **kwargs) -> None:
        if "label" not in kwargs:
            kwargs["label"] = "FlashPassword"

        if "password" not in kwargs:
            kwargs["password"] = True

        super().__init__(**kwargs)
