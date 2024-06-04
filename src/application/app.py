import asyncio

import flet as ft
from flet import AppBar
from flet import ElevatedButton
from flet import Page
from flet import Text
from flet import View
from flet import colors

from src.game import Game
from src.infrastructure.flet_comp.component import textfield


# TODO: later  # noqa: FIX002, TD002, TD003
# from src.person.base import Person  # noqa: ERA001
# async def checkbox_changed(e, page, ):
#     ip.visible = not ip.visible  # noqa: ERA001
#     port.visible = not port.visible  # noqa: ERA001
#     pr_log.visible = not pr_log.visible  # noqa: ERA001
#     pr_pass.visible = not pr_pass.visible  # noqa: ERA001
#     await page.update_async()  # noqa: ERA001


async def app(page: Page) -> None:  # noqa: C901, PLR0915
    page.scroll = "adaptive"
    page.vertical_alignment = "center"
    login = textfield.LOGIN
    password = textfield.PASSWORD

    async def checkbox_changed(e) -> None:  # noqa: ARG001, ANN001
        ip.visible = not ip.visible
        port.visible = not port.visible
        pr_log.visible = not pr_log.visible
        pr_pass.visible = not pr_pass.visible
        await page.update_async()

    proxy = ft.Checkbox(label="Proxy off/on", value=True, on_change=checkbox_changed)
    ip = textfield.IP
    port = textfield.PORT
    pr_log = textfield.PR_LOG
    pr_pass = textfield.PR_PASS

    greetings = ft.Column()
    game = Game()

    async def log_in(e) -> None:  # noqa: ARG001, ANN001
        if greetings.controls:
            greetings.controls = [Text(f"Hello, {login.value}!")]
        else:
            greetings.controls.append(Text(f"Hello, {login.value}!"))
        proxy_url = f"http://{pr_log.value}:{pr_pass.value}@{ip.value}:{port.value}" if proxy.value else None
        await game.init_connection(
            login=login.value,
            password=password.value,
            proxy=proxy.value,
            proxy_url=proxy_url,
            ip=ip.value,
        )
        login.value = ""
        password.value = ""
        ip.value = ""
        pr_log.value = ""
        pr_pass.value = ""
        port.value = ""
        await page.update_async()
        await page.go_async("/main")

    async def log_out(e) -> None:  # noqa: ARG001, ANN001
        greetings.controls = []
        await page.update_async()
        await page.go_async("/")

    async def see_clan(e) -> None:  # noqa: ARG001, ANN001
        await game.see_clan_items_potion()
        await page.update_async()

    async def route_change(e) -> None:  # noqa: ARG001, ANN001
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("LogIn"), bgcolor=colors.SURFACE_VARIANT),
                    login,
                    password,
                    proxy,
                    ip,
                    port,
                    pr_log,
                    pr_pass,
                    ElevatedButton("Log in", on_click=log_in),
                ],
                horizontal_alignment="center",
                vertical_alignment="center",
            ),
        )
        if page.route == "/main":
            # TODO: do chore  # noqa: TD002, TD003, FIX002
            # tasks = [asyncio.create_task(game.get_person_on_cell())]  # noqa: ERA001
            # person_on_cell = await asyncio.gather(*tasks)  # noqa: ERA001
            # person_on_cell = await asyncio.gather(game.get_person_on_cell())  # noqa: ERA001
            # person_on_cell = await game.get_person_on_cell()  # noqa: ERA001

            # persons = Text(f"person_on_cell:\n{person_on_cell}", selectable=True)  # noqa: ERA001

            class Persons(ft.UserControl):
                async def did_mount_async(self) -> None:
                    self.running = True
                    asyncio.create_task(self.update_persons())  # noqa: RUF006

                async def will_unmount_async(self) -> None:
                    self.running = False

                async def update_persons(self) -> None:
                    while self.running:
                        self.persons.value = await game.get_person_on_cell()
                        await self.update_async()
                        await asyncio.sleep(5)

                def build(self) -> ft.Text:
                    self.persons = ft.Text()
                    return self.persons

            # clan_potions = await game.see_clan_items_potion()  # noqa: ERA001
            # dd = ft.Dropdown(options=[], width=200)  # noqa: ERA001
            # for person in game.person_list:  # noqa: ERA001, RUF100
            #     dd.options.append(ft.dropdown.Option(f"{person.nick} {'В бою' if person.fight_link else 'Не в бою'}"))  # noqa: ERA001, RUF003, E501
            page.views.append(
                View(
                    "/main",
                    [
                        AppBar(title=Text("LogOut"), bgcolor=colors.SURFACE_VARIANT),
                        ElevatedButton(
                            "LogOut Button",
                            on_click=lambda _: page.go("/"),
                        ),
                        greetings,
                        Text(f"Status={game.status}"),
                        ElevatedButton("see clan", on_click=see_clan),
                        # Text(f"person_on_cell\n{person_on_cell[0]}", selectable=True),  # noqa: ERA001
                        Persons(),
                        # persons,
                        # dd,
                        # Text(f"clan_potions= {clan_potions}", selectable=True),  # noqa: ERA001
                    ],
                    scroll="adaptive",
                ),
            )
        await page.update_async()

    async def view_pop(e) -> None:  # noqa: ARG001, ANN001
        page.views.pop()
        top_view = page.views[-1]
        await page.go_async(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    await page.go_async(page.route)
