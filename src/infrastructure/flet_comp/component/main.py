import flet as ft

from src.config import logger
from src.infrastructure.flet_comp.element import main
from src.use_cases.game.game import User


class MainComponent(ft.View):
    def __init__(self, game: User, page: ft.Page) -> None:
        self.logger = logger
        self.logger.debug("MainComponent init")
        self.page = page
        self.game = game
        self._create_main_elements()

        super().__init__(
            "/main",
            [
                ft.AppBar(title=ft.Text("LogOut"), bgcolor=ft.colors.SURFACE_VARIANT),
                ft.ElevatedButton("LogOut Button", on_click=lambda _: page.go("/")),
                self.greetings_text,
                ft.Text(f"Status={game.status}"),
                ft.ElevatedButton("see clan", on_click=self.see_clan),
                # Text(f"person_on_cell\n{person_on_cell[0]}", selectable=True),  # noqa: ERA001
                # Persons(),  # noqa: ERA001
                # persons,
                # dd,
                self.potion_text,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def _create_main_elements(self) -> None:
        self.logger.debug("_create_main_elements")
        self.potion_text = main.POTION_TEXT
        self.greetings_text = main.GreetingText(self.game.login)

    # async def logout(self, e) -> None:
    #     self.logger.debug("logout")  # noqa: ERA001
    #     await self.game.close()  # noqa: ERA001
    #     await self.page.go_async("/")  # noqa: ERA001

    async def see_clan(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("see_clan")
        clan_potions = await self.game.see_clan_items_potion()
        self.potion_text.value = clan_potions
        await self.potion_text.update_async()
