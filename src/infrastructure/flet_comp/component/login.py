import aiohttp
import flet as ft

from src.config import logger
from src.infrastructure.flet_comp.element import login
from src.use_cases.game.game import User
from src.use_cases.request.base import Proxy


class LoginComponent(ft.View):
    def __init__(self, game: User, page: ft.Page) -> None:
        self.logger = logger
        self.logger.debug("LoginElement init")
        self.page = page
        self.game = game
        self._create_login_elements()
        super().__init__(
            "/",
            [
                ft.AppBar(title=ft.Text("LogIn"), bgcolor=ft.colors.SURFACE_VARIANT),
                self.login,
                self.password,
                self.label_proxy,
                self.proxy,
                self.ip,
                self.port,
                self.pr_log,
                self.pr_pass,
                ft.ElevatedButton("Log in", on_click=self.log_in),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def _create_login_elements(self) -> None:
        self.logger.debug("_create_login_elements")
        self.login = login.LOGIN
        self.password = login.PASSWORD
        self.label_proxy = login.LABEL_PROXY
        self.proxy = ft.Checkbox(value=True, on_change=self.checkbox_chang_visible)
        self.ip = login.IP
        self.port = login.PORT
        self.pr_log = login.PR_LOG
        self.pr_pass = login.PR_PASS

    async def checkbox_chang_visible(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("checkbox_chang_visible")
        self.ip.visible = not self.ip.visible
        self.port.visible = not self.port.visible
        self.pr_log.visible = not self.pr_log.visible
        self.pr_pass.visible = not self.pr_pass.visible
        await self.page.update_async()

    def _clear_values(self) -> None:
        self.logger.debug("_clear_values")
        self.login.value = ""
        self.password.value = ""
        self.ip.value = ""
        self.pr_log.value = ""
        self.pr_pass.value = ""
        self.port.value = ""

    async def log_in(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("log_in")
        proxy_url = f"http://{self.ip.value}:{self.port.value}" if self.proxy.value else None
        proxy_data = (
            Proxy(proxy=proxy_url, proxy_auth=aiohttp.BasicAuth(self.pr_log.value, self.pr_pass.value))
            if proxy_url
            else Proxy()
        )
        await self.game.init_connection(
            login=self.login.value,
            password=self.password.value,
            proxy=self.proxy.value,
            proxy_data=proxy_data,
            ip=self.ip.value,
        )
        self._clear_values()
        await self.page.update_async()
        await self.page.go_async("/main")
