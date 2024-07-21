import flet as ft

from src.config import logger
from src.infrastructure.flet_comp.component.login import LoginComponent
from src.infrastructure.flet_comp.component.main import MainComponent
from src.infrastructure.flet_comp.component.person import PersonComponent
from src.infrastructure.utils.person_files import get_all_persons
from src.use_cases.game.base import BaseGame
from src.use_cases.game.game import User


class RootElement(BaseGame):
    def _initialize(self) -> None:
        self.logger = logger
        self.logger.debug("_initialize")
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.page.adaptive = True
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.route_dict = {
            "/": "",
            "/main": "",
        }

    async def start(self, page: ft.Page) -> None:
        self.page = page
        self.game = User()
        self._initialize()
        self.logger.debug("start")

        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop

        await self.page.go_async("/")

        await self.page.update_async()

    async def route_change(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("route_change")
        self.page.views.clear()
        self.page.views.append(LoginComponent(self.game, self.page))
        if self.page.route == "/main":
            self.page.views.append(MainComponent(self.game, self.page))
        await self.page.update_async()

    async def mass_route_change(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("mass_route_change")
        self.page.views.clear()
        self.page.views.append(PersonComponent(self.users_game, self.page))
        # if self.page.route == "/main":
        #     self.page.views.append(MainComponent(self.game, self.page))  # noqa: ERA001
        await self.page.update_async()

    async def view_pop(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("view_pop")
        self.page.views.pop()
        top_view = self.page.views[-1]
        await self.page.go_async(top_view.route)

    def create_mass_persons(self) -> None:
        self.users = get_all_persons()
        self.users_game = {
            user.login: User(
                login=user.login,
                user_info=user,
            )
            for user in self.users
        }

    async def mass_start(self, page: ft.Page) -> None:
        self.page = page
        self.create_mass_persons()
        self._initialize()
        self.logger.debug("start")

        self.page.on_route_change = self.mass_route_change
        self.page.on_view_pop = self.view_pop

        await self.page.go_async("/")

        await self.page.update_async()
