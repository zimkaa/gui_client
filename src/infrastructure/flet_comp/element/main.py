import flet as ft


class GreetingText(ft.Text):
    def __init__(self, login: str) -> None:
        super().__init__(f"Hello, {login}!", selectable=True)


POTION_TEXT = ft.Text("", selectable=True)
