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
                self.button_logout,
                self.greetings_text,
                self.status,
                self.button_clan_item,
                # Text(f"person_on_cell\n{person_on_cell[0]}", selectable=True),  # noqa: ERA001
                # Persons(),  # noqa: ERA001
                # persons,
                # dd,
                self.button_buff,
                self.use_status,
                self.potion_text,
                self.button_bait,
                self.bait_status,
                self.button_ab,
                self.ab_status,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def _create_main_elements(self) -> None:
        self.logger.debug("_create_main_elements")
        self.potion_text = main.PotionText()
        self.greetings_text = main.GreetingText(login=self.game.login)
        self.button_buff = main.BuffButton(on_click=self.use_default_buff)
        self.button_clan_item = main.ClanItemsButton(on_click=self.see_clan)
        self.status = main.Status(status=self.game.status)
        self.use_status = main.UseStatus()

        self.button_bait = main.GoToBaitButton(on_click=self.go_to_bait)
        self.bait_status = main.BaitStatus()

        self.button_ab = main.StartABButton(on_click=self.start_ab)
        self.ab_status = main.ABStatus()

        self.button_logout = main.LogOutButton(on_click=self._logout)

    async def use_default_buff(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("use_default_buff")
        # await self.game._use_potion(buff_name="Превосходное Зелье Жизни")  # noqa: ERA001
        await self.game.use_strategy_buff()
        self.use_status.value = "Buff used"
        await self.use_status.update_async()

    async def go_to_bait(self, e) -> None:  # noqa: ANN001, ARG002
        await self.game.start_wait_bait()
        self.bait_status.value = "Bait started wait for end"
        self.button_bait.disabled = True
        await self.button_bait.update_async()
        await self.bait_status.update_async()

    async def start_ab(self, e) -> None:  # noqa: ANN001, ARG002
        if self.button_ab.text == "Stop AB":
            self.ab_status.value = "AB stopped"
            self.button_ab.text = "Start AB"
            await self.button_ab.update_async()
            await self.ab_status.update_async()
            await self.game.stop_ab_while()
            return

        self.ab_status.value = "AB started wait for battle"
        self.button_ab.text = "Stop AB"
        await self.button_ab.update_async()
        await self.ab_status.update_async()
        await self.game.start_ab_while()

    async def _logout(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("logout")
        await self.game.close()
        await self.page.go_async("/")

    async def see_clan(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("see_clan")
        clan_potions = await self.game.see_clan_items_potion()
        self.potion_text.value = clan_potions
        await self.potion_text.update_async()
