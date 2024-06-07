from __future__ import annotations
from typing import TYPE_CHECKING
from urllib.parse import quote

from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject

from src.application.deps import MainContainer
from src.config.game import urls
from src.domain.pattern.person import compiled
from src.use_cases.person.parameter import PERSON_PARAMS


if TYPE_CHECKING:
    from src.infrastructure.request.nl import BaseConnection


class Person:
    def __init__(self, nick: str) -> None:
        self.nick = nick
        self.login: bytes = nick.encode("cp1251")
        self.mp: float | None = None
        self.all_mp: float | None = None
        self.hp: float | None = None
        self.all_hp: float | None = None
        self.buffs: list[str | None] = []
        self.level: int | None = None

        self.need_effects: list[str | None] = []
        self.need_parameters: list[str | None] = []

        self.info_page_text = ""
        self.person_url_info = urls.URL_PLAYER_INFO.format(name=quote(self.login))

        self.parameters: list[list[str | int], list[list[str, int, int], list[str, int]]] | None = None  # type: ignore[type-arg]

        self.fight_link: str | None = None

    def _execute(self) -> None:
        parameters = self._get_parameters()
        self.parameters = parameters

        effects = self._get_effects_from_info()
        self.effects = effects

        param_dict = self._get_param_dict()
        self.param_dict = param_dict

        fight_link = self._get_fight_link()
        self.fight_link = fight_link

    def _update_info(self, *, page_text: str) -> None:
        self.info_page_text = page_text
        self._execute()

    def _get_effects_from_info(self) -> list[list[str]]:
        new_result: list[list[str]] = []
        result = compiled.var_effects.findall(self.info_page_text)
        if not result:
            return new_result
        elements_row: str = result.pop()
        cleared_string = elements_row.replace("<b>", "").replace("</b>", "").replace("'", "").split("],[")
        return [x.split(",") for x in cleared_string]

    def _get_param_dict(self) -> dict:
        find_stats = compiled.find_stats.findall(self.info_page_text)
        prepared: list[str] = find_stats[0].split("],[")
        param_dict = dict.fromkeys(PERSON_PARAMS)
        for num, key in enumerate(param_dict.keys()):
            cleared_string = prepared[num + 1].replace("[", "").replace("]", "").replace(f"'{key}',", "")
            elements = cleared_string.split(",")
            if len(elements) > 1:
                all_count = 0.0
                for count in elements:
                    all_count += float(count)
            else:
                (all_count,) = elements  # type: ignore[assignment]
            param_dict[key] = float(all_count)
        return param_dict

    def _get_parameters(self) -> list[list[str | int], list[list[str, int, int], list[str, int]]]:  # type: ignore[type-arg]
        result = compiled.var_effects2.findall(self.info_page_text)
        if not result:
            msg = "Why empty params in info?"
            raise Exception(msg)  # noqa: TRY002
        elements_row: str = result.pop()
        parameters = eval(elements_row)  # noqa: S307
        self.level = int(parameters[0][3])
        return parameters

    def _get_fight_link(self) -> str | None:
        if self.parameters[0][7]:  # type: ignore[index]
            return urls.URL_LOG + f"?fid={self.parameters[0][7]}"  # type: ignore[index]
        return None

    @inject
    async def update_info_person(self, connection: BaseConnection = Provide[MainContainer.connection]) -> Person:
        answer = await connection.get_html(self.person_url_info)
        self._update_info(page_text=answer)
        return self
