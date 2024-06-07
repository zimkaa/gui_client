import flet as ft

from src.config import logger
from src.infrastructure.flet_comp.component.login import LoginComponent
from src.infrastructure.flet_comp.component.main import MainComponent
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

    async def route_change(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("route_change")
        self.page.views.clear()
        self.page.views.append(LoginComponent(self.game, self.page))
        if self.page.route == "/main":
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
            self.page.views.append(MainComponent(self.game, self.page))
        await self.page.update_async()

    async def view_pop(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("view_pop")
        self.page.views.pop()
        top_view = self.page.views[-1]
        await self.page.go_async(top_view.route)

    async def start(self, page: ft.Page) -> None:
        self.page = page
        self.game = User()
        self._initialize()
        self.logger.debug("start")

        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop

        await self.page.go_async("/")

        await self.page.update_async()
