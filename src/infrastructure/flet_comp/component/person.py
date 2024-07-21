from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

import flet as ft

from src.config import logger
from src.infrastructure.flet_comp.element import person as person_element
from src.use_cases.game.game import User
from src.use_cases.person.buff.config import get_config


if TYPE_CHECKING:
    from src.use_cases.game.game import User


class PersonComponent(ft.View):
    def __init__(self, persons: dict[str, User], page: ft.Page) -> None:
        self.logger = logger
        self.logger.debug("PersonComponent init")
        self.page = page
        self.persons = persons
        self.page = page
        self.person_elements: dict[str, ft.Row] = {}
        self._default_effect = "ТЕСТ"  # noqa: RUF001
        self._get_config()
        self._create_person_elements()

        self._create_rows()

        super().__init__(
            "/",
            [
                self.person_text,
                *self.rows,
                self.start_button,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
        )

    def _get_config(self) -> None:
        self._config = get_config()
        self._options = [ft.dropdown.Option(name) for name in self._config]
        default_effects = self._config[self._default_effect]
        for person in self.persons.values():
            person.set_saved_effects(default_effects)

    def _dropdown_changed(self, e) -> None:  # noqa: ANN001
        self.logger.debug("_dropdown_changed on_change")
        logger_text = f"{e.control=}"
        self.logger.debug(logger_text)
        effects = self._config[e.control.value]
        self.persons[e.control.label].set_saved_effects(effects)
        person_effects = f"{self.persons[e.control.label]._saved_effects=}"  # noqa: SLF001
        self.logger.debug(person_effects)

    def _create_row(self, person: User) -> ft.Row:
        value = person.is_active
        assert person.login is not None
        button = person_element.UserSwitch(
            value=value,
            login=person.login,
            on_change=self._on_change,
        )

        return [
            button,
            person_element.StatusText(),
            person_element.ConfigChoice(
                label=person.login,
                options=self._options,
                on_change=self._dropdown_changed,
            ),
        ]

    def _create_rows(self) -> None:
        self.rows = []

        for controls in self.person_elements.values():
            row = ft.Row(
                spacing=0,
                controls=controls,
            )
            self.rows.append(row)

    def _create_person_elements(self) -> None:
        self.logger.debug("_create_main_elements")
        self.person_text = person_element.PersonsText(value="Hello!")
        self.start_button = person_element.BuffButton(on_click=self.start_buffing)
        self._create_person_rows()

    def _create_person_rows(self) -> None:
        for person in self.persons.values():
            assert person.login is not None
            self.person_elements[person.login] = self._create_row(person)

    def _on_change(self, e) -> None:  # noqa: ANN001
        self.logger.debug("on_change")
        logger_text = f"{e.control=}"
        self.logger.debug(logger_text)
        person = self.persons[e.control.label]
        person.change_active()

    async def start_buffing(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("start_buffing")
        await self.log_in_all_persons()

        tasks = [person.use_buff() for person in self.persons.values() if person.is_active]

        await asyncio.gather(*tasks)

        await self.page.update_async()
        await self.page.go_async("/main")

    async def log_in_all_persons(self) -> None:
        self.logger.debug("log_in_all_persons")

        tasks = [person.new_init_connection() for person in self.persons.values() if person.is_active]

        await asyncio.gather(*tasks)

    async def log_in_all_persons_button(self, e) -> None:  # noqa: ANN001, ARG002
        self.logger.debug("log_in_all_persons_button")

        await self.log_in_all_persons()

        await self.page.update_async()
        await self.page.go_async("/main")
