from __future__ import annotations
import json
import random
import re
from typing import TYPE_CHECKING
from typing import Any

import aiohttp

from src.config import logger
from src.config.game import urls
from src.domain.item import use
from src.domain.item.elixir import Elixir
from src.domain.item.scroll import Scroll
from src.domain.pattern.inv import pattern
from src.domain.pattern.location import compiled
from src.domain.value_object.classes import LocationState
from src.use_cases.person.buff import effects
from src.use_cases.person.buff import group
from src.use_cases.person.buff.group import DEFAULT_MAG_EFFECTS


if TYPE_CHECKING:
    from src.infrastructure.request import Connection
    from src.use_cases.game.location.base import Location
    from src.use_cases.person.buff.castle import MagicTower


class Buff:
    def __init__(self, *, connection: Connection, location: Location) -> None:
        self.connection = connection
        self.location = location

        self.last_page_text: str = ""
        self.logger = logger
        self.json_data: dict[str, Any] = {}

    async def use_strategy_buff(self, *, page_text: str, need_effects: list[effects.Effect] | None = None) -> None:
        self.last_page_text = page_text
        if need_effects is None:
            need_effects = DEFAULT_MAG_EFFECTS

        self.effects = effects.PersonEffects(page_text=self.last_page_text, need_effects=need_effects)
        element_list = self.effects.get_effects()
        text = f"Need effects: {element_list}"
        self.logger.info(text)

        self.last_page_text = await self.connection.get_html(urls.URL_POTION)

        if element_list:
            for element in element_list:
                match element.type_:
                    case effects.ElementType.POTION:
                        await self._use_potion(element=element, count=element.count)
                    case effects.ElementType.SCROLL:
                        await self._use_scroll(scroll_name=element.name, count=element.count)  # type: ignore[arg-type]
                    case effects.ElementType.ELIXIR:
                        await self._use_elixir(elixir_name=element.name, count=element.count)  # type: ignore[arg-type]
                    case effects.ElementType.CASTLE:
                        await self._use_castle_tower(elements=element.castle)  # type: ignore[arg-type]
                    case effects.ElementType.CASTLE_MP:
                        await self._use_castle_mp()
                    case effects.ElementType.CASTLE_HP:
                        await self._use_castle_hp()

    async def _return_to_castle(self) -> bool:
        result = compiled.finder_return_vcode.findall(self.last_page_text)
        if result:
            vcode = result[0]

            params = {
                "get_id": 56,
                "act": 10,
                "go": "ret",
                "vcode": vcode,
            }
            self.last_page_text = await self.connection.get_html(urls.URL_MAIN, params=params)

        if self.location.get_actual_location(self.last_page_text) == LocationState.CASTLE:
            bcodes = self.location.info_string
            self.json_data = json.loads(bcodes[0])
            return True

        self.logger.info("Not in castle")
        return False

    async def _use_castle_tower(self, elements: list[MagicTower] = group.DODGE_TOWER) -> None:
        self.logger.info("use_castle_tower")
        if await self._return_to_castle():
            data = {
                "action": "building",
                "building": "mtower",
                "vcode": self.json_data["mtower"],
                "r": random.random(),
            }
            self.last_page_text = await self.connection.get_html(urls.URL_CASTLE, params=data)
            self.json_data = json.loads(self.last_page_text)
            effects = ",".join(map(str, elements))

            params = {"r": random.random()}

            form_data = aiohttp.FormData(charset="windows-1251")  # cp1251
            form_data.add_field("action", "mtowerApply")
            form_data.add_field("effects", effects)
            form_data.add_field("vcode", self.json_data["r"]["vcode"])
            self.logger.critical(effects)

            self.last_page_text = await self.connection.post_html(urls.URL_CASTLE, params=params, data=form_data)
            self.logger.critical(self.last_page_text)
            self.json_data = json.loads(self.last_page_text)
            self.logger.critical(self.json_data)

    async def _use_castle_hp(self) -> None:
        if await self._return_to_castle():
            vcode = (
                self.json_data.get("fountain")
                if self.json_data.get("fountain")
                else self.json_data.get("ba")["fountain"]  # type: ignore[index]
            )
            data = {
                "action": "building",
                "building": "fountain",
                "vcode": vcode,
                "r": random.random(),
            }
            self.last_page_text = await self.connection.get_html(urls.URL_CASTLE, params=data)
            data = json.loads(self.last_page_text)

            params = {"r": random.random()}

            form_data = aiohttp.FormData(charset="windows-1251")  # cp1251
            form_data.add_field("action", "restoreHP")
            form_data.add_field("hp", 1000)
            form_data.add_field("vcode", data["r"]["hp_vcode"])

            self.last_page_text = await self.connection.post_html(urls.URL_CASTLE, params=params, data=form_data)
            self.json_data = json.loads(self.last_page_text)

    async def _use_castle_mp(self) -> None:
        if await self._return_to_castle():
            vcode = self.json_data.get("pond") if self.json_data.get("pond") else self.json_data.get("ba")["pond"]  # type: ignore[index]
            data = {
                "action": "building",
                "building": "pond",
                "vcode": vcode,
                "r": random.random(),
            }
            self.last_page_text = await self.connection.get_html(urls.URL_CASTLE, params=data)
            data = json.loads(self.last_page_text)

            params = {"r": random.random()}

            form_data = aiohttp.FormData(charset="windows-1251")  # cp1251
            form_data.add_field("action", "restoreMP")
            form_data.add_field("mp", 1000)
            form_data.add_field("vcode", data["r"]["mp_vcode"])

            self.last_page_text = await self.connection.post_html(urls.URL_CASTLE, params=params, data=form_data)
            self.json_data = json.loads(self.last_page_text)

    async def _use_potion(self, *, element: effects.Effect, count: int = 1) -> None:
        potion_name = element.name
        item_pattern = pattern.FIND_USE_ITEM_MAGICREFORM.format(name=potion_name)
        finder_use_item = re.compile(item_pattern)

        result = finder_use_item.finditer(self.last_page_text)
        if not result:
            potion_name = element.equivalent
            item_pattern = pattern.FIND_USE_ITEM_MAGICREFORM.format(name=potion_name)
            finder_use_item = re.compile(item_pattern)
            result = finder_use_item.finditer(self.last_page_text)

        if not result:
            return

        for _ in range(count):
            if not result:
                break

            try:
                item = next(result).group(0)
            except StopIteration:
                msg = f"Can't find item: {potion_name}"
                self.logger.exception(msg)
                break

            (magicreuid, fornickname, _, vcode) = item.replace("'", "").split(",")
            form_data = aiohttp.FormData(charset="windows-1251")  # cp1251
            form_data.add_field("post_id", 46)
            form_data.add_field("magicrestart", 1)
            form_data.add_field("magicreuid", magicreuid)
            form_data.add_field("vcode", vcode)
            form_data.add_field("fornickname", fornickname)

            self.last_page_text = await self.connection.post_html(urls.URL_MAIN, data=form_data)

            result = finder_use_item.finditer(self.last_page_text)

    async def _use_elixir(self, *, elixir_name: Elixir = Elixir.BLISS, count: int = 1) -> None:
        self.last_page_text = await self.connection.get_html(urls.URL_ELIXIR)
        item_id = use.binding_dict.get(elixir_name)  # type: ignore[call-overload]
        if item_id is None:
            msg = f"Unknown buff name: {elixir_name}\nNeed update binding_dict in use.py"
            self.logger.critical(msg)
            return

        item_pattern = pattern.FIND_USE_ITEM_SCROLL.format(name=item_id)

        finder_use_item = re.compile(item_pattern)

        for _ in range(count):
            result = finder_use_item.finditer(self.last_page_text)

            if not result:
                break

            try:
                item = next(result).group(0)
            except StopIteration:
                msg = f"Can't find item: {elixir_name}"
                self.logger.exception(msg)
                break

            arg_lst = item.replace(r"' ", "").split("&")
            params = {
                "get_id": 43,
                "act": item_id,
                "uid": arg_lst[0],
            }
            for item in arg_lst[1:]:
                key, value = item.split("=")
                params[key] = value

            self.last_page_text = await self.connection.get_html(urls.URL_MAIN, params=params)

    async def _use_scroll(self, *, scroll_name: Scroll = Scroll.STONE_SKIN, count: int = 1) -> None:
        self.last_page_text = await self.connection.get_html(urls.URL_SCROLL)
        item_id = use.binding_dict.get(scroll_name)  # type: ignore[call-overload]
        if item_id is None:
            msg = f"Unknown buff name: {scroll_name}\nNeed update binding_dict in use.py"
            self.logger.critical(msg)
            return

        item_pattern = pattern.FIND_USE_ITEM_SCROLL.format(name=item_id)

        finder_use_item = re.compile(item_pattern)

        for _ in range(count):
            result = finder_use_item.finditer(self.last_page_text)

            if not result:
                break

            try:
                item = next(result).group(0)
            except StopIteration:
                msg = f"Can't find item: {scroll_name}"
                self.logger.exception(msg)
                break

            arg_lst = item.replace(r"' ", "").split("&")
            params = {
                "get_id": 43,
                "act": item_id,
                "uid": arg_lst[0],
            }
            for item in arg_lst[1:]:
                key, value = item.split("=")
                params[key] = value

            self.last_page_text = await self.connection.get_html(urls.URL_MAIN, params=params)
