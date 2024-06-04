import flet as ft

from src.config import settings


# PROXY = ft.Checkbox(label="Proxy off/on", value=True, on_change=checkbox_changed)  # noqa: ERA001


def create_text_field(**kwarg) -> ft.TextField:  # noqa: ANN003
    return ft.TextField(
        **kwarg,
        width=200,
    )


IP = create_text_field(
    label="proxy ip",
    value=settings.connection.PROXY_IP,
)
PORT = create_text_field(
    label="proxy port",
    value=settings.connection.PROXY_PORT,
)
PR_LOG = create_text_field(
    label="proxy login",
    value=settings.connection.PROXY_LOG,
)
PR_PASS = create_text_field(
    password=True,
    label="proxy password",
    value=settings.connection.PROXY_PASS,
)

LOGIN = create_text_field(
    label="Login",
    value=settings.person.LOGIN,
    autofocus=True,
)
PASSWORD = create_text_field(
    password=True,
    label="Password",
    value=settings.person.PASSWORD,
)
