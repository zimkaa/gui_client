import aiohttp
import flet as ft

from src.config import logger
from src.infrastructure.flet_comp.component import login
from src.infrastructure.flet_comp.component import textfield
from src.use_cases.game.base import BaseGame
from src.use_cases.game.game import User
from src.use_cases.request.base import Proxy


class RootElement(BaseGame):
    def _initialize(self) -> None:
        self._page.scroll = ft.ScrollMode.ADAPTIVE
        self._page.adaptive = True
        self._page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self._page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.logger = logger
        self.logger.debug("_initialize")

    def _create_login_elements(self) -> None:
        self.logger.debug("_create_login_elements")
        self.login = textfield.LOGIN
        self.password = textfield.PASSWORD
        self.label_proxy = login.LABEL_PROXY
        self.proxy = ft.Checkbox(value=True, on_change=self.checkbox_chang_visible)
        self.ip = textfield.IP
        self.port = textfield.PORT
        self.pr_log = textfield.PR_LOG
        self.pr_pass = textfield.PR_PASS
        self.greetings = login.GREETINGS
        self.game = User()

    async def checkbox_chang_visible(self, e) -> None:  # noqa: ANN001
        self.logger.debug("checkbox_changed e=%s", e)
        self.logger.debug("type e=%s", type(e))
        self.logger.debug("e=%s", e.__dict__)
        self.ip.visible = not self.ip.visible
        self.port.visible = not self.port.visible
        self.pr_log.visible = not self.pr_log.visible
        self.pr_pass.visible = not self.pr_pass.visible
        await self._page.update_async()

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
        if self.greetings.controls:
            self.greetings.controls = [ft.Text(f"Hello, {self.login.value}!")]
        else:
            self.greetings.controls.append(ft.Text(f"Hello, {self.login.value}!"))

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
        await self._page.update_async()
        await self._page.go_async("/main")

    async def see_clan(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("see_clan")
        await self.game.see_clan_items_potion()
        await self._page.update_async()

    async def route_change(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("route_change")
        self._page.views.clear()
        self._page.views.append(
            ft.View(
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
                horizontal_alignment="center",
                vertical_alignment="center",
            ),
        )
        if self._page.route == "/main":
            # TODO: do chore  # noqa: TD002, TD003, FIX002
            # tasks = [asyncio.create_task(game.get_person_on_cell())]  # noqa: ERA001
            # person_on_cell = await asyncio.gather(*tasks)  # noqa: ERA001
            # person_on_cell = await asyncio.gather(game.get_person_on_cell())  # noqa: ERA001
            # person_on_cell = await game.get_person_on_cell()  # noqa: ERA001

            # persons = Text(f"person_on_cell:\n{person_on_cell}", selectable=True)  # noqa: ERA001

            # class Persons(ft.UserControl):
            #     async def did_mount_async(self) -> None:
            #         self.running = True  # noqa: ERA001
            #         asyncio.create_task(self.update_persons())  # noqa: ERA001

            #     async def will_unmount_async(self) -> None:
            #         self.running = False  # noqa: ERA001

            #     async def update_persons(self) -> None:
            #         while self.running:
            #             self.persons.value = await game.get_person_on_cell()  # noqa: ERA001
            #             await self.update_async()  # noqa: ERA001
            #             await asyncio.sleep(5)  # noqa: ERA001

            #     def build(self) -> ft.Text:
            #         self.persons = ft.Text()  # noqa: ERA001
            #         return self.persons  # noqa: ERA001

            # clan_potions = await game.see_clan_items_potion()  # noqa: ERA001
            # dd = ft.Dropdown(options=[], width=200)  # noqa: ERA001
            # for person in game.person_list:  # noqa: ERA001, RUF100
            #     dd.options.append(ft.dropdown.Option(f"{person.nick} {'В бою' if person.fight_link else 'Не в бою'}"))  # noqa: ERA001, RUF003, E501
            self._page.views.append(
                ft.View(
                    "/main",
                    [
                        ft.AppBar(title=ft.Text("LogOut"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton(
                            "LogOut Button",
                            on_click=lambda _: self._page.go("/"),
                        ),
                        self.greetings,
                        ft.Text(f"Status={self.game.status}"),
                        ft.ElevatedButton("see clan", on_click=self.see_clan),
                        # Text(f"person_on_cell\n{person_on_cell[0]}", selectable=True),  # noqa: ERA001
                        # Persons(),  # noqa: ERA001
                        # persons,
                        # dd,
                        # Text(f"clan_potions= {clan_potions}", selectable=True),  # noqa: ERA001
                    ],
                    scroll="adaptive",
                ),
            )
        await self._page.update_async()

    async def view_pop(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("view_pop")
        self._page.views.pop()
        top_view = self._page.views[-1]
        await self._page.go_async(top_view.route)

    async def start(self, page: ft.Page) -> None:
        self._page = page
        self._initialize()
        self.logger.debug("start")
        self._create_login_elements()

        self._page.on_route_change = self.route_change
        self._page.on_view_pop = self.view_pop

        await self._page.go_async("/")

        await self._page.update_async()
