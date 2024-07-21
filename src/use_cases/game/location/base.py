from __future__ import annotations
import asyncio
import json
import random
import re
from typing import TYPE_CHECKING
from typing import Callable

import aiohttp

from src.config import logger
from src.config.game import urls
from src.domain.constants.consts import AGREE
from src.domain.constants.location import base as location_constants
from src.domain.pattern.location import compiled
from src.domain.pattern.location import pattern as location_pattern
from src.domain.value_object.classes import LocationState
from src.domain.value_object.classes import Teleport
from src.use_cases.game.location.graph import CitiesGraph
from src.use_cases.game.location.implementation_logic import BFS
from src.use_cases.game.location.main import LocationNode
from src.use_cases.person.base import Person


if TYPE_CHECKING:
    from src.infrastructure.request import Connection


class Location:
    def __init__(self, *, connect: Connection, last_page: str) -> None:
        self._connect = connect
        self.logger = logger
        self._last_page = last_page

        self.info_string: list[str]
        self._location: LocationState

        self._where_i_am()

    def get_actual_location(self, actual_page: str) -> LocationState:
        self.logger.debug("get_actual_location")
        self._last_page = actual_page
        self._where_i_am()
        return self._location

    async def get_person_on_cell(self) -> str:
        self.logger.debug("get_person_on_cell")
        text = await self._connect.get_html(urls.URL_SELL_INFO)
        count2 = compiled.person_om_cell_group.findall(text)
        string = ""
        persons: list[Person] = []
        for row in count2:
            name = row[1]
            level = row[2]
            row[3]
            row[6]  # травма
            text = f"{name=} {level=} clan={row[1]}"
            if name.startswith("<i>") and name.endswith("</i>"):
                nick = name.replace("<i>", "").replace("</i>", "")
            else:
                nick = name
            persons.append(
                asyncio.create_task(Person(connection=self._connect, login=nick)._execute()),  # type: ignore[func-returns-value, call-arg, arg-type]  # noqa: SLF001
            )

        persons = await asyncio.gather(*persons)  # type: ignore[call-overload]
        for person in persons:
            text = f"nick={person.nick} level={person.level}"  # type: ignore[attr-defined]
            string += f"{text} {'В бою ' + person.fight_link if person.fight_link else 'Не в бою'}\n"  # type: ignore[attr-defined]  # noqa: RUF001
        self.person_on_cell = string
        return string

    async def _from_city_go_to_inventory(self) -> None:
        self.logger.debug("_from_city_go_to_inventory")
        (prepare,) = compiled.finder_in_city.findall(self._last_page)
        vcode = prepare.split("=")[-1]
        data = {"get_id": "56", "act": "10", "go": "inv", "vcode": vcode}

        self._last_page = await self._connect.get_html(urls.URL_MAIN, params=data)
        self._where_i_am()

    async def _from_castle_go_to_inventory(self) -> None:
        self.logger.debug("_from_castle_go_to_inventory")

        (prepare,) = compiled.finder_vcode_castle.findall(self._last_page)
        data_list = eval(prepare)  # noqa: S307
        data = {"get_id": "56", "act": "10", "go": "inv", "vcode": data_list[1][1]}

        self._last_page = await self._connect.get_html(urls.URL_MAIN, params=data)
        self._where_i_am()

    async def _from_nature_go_to_inventory(self) -> None:
        self.logger.debug("_from_nature_go_to_inventory")
        (prepare,) = compiled.finder_nature_to_inv.findall(self._last_page)
        text = f"{prepare=}"
        self.logger.debug(text)

        if prepare:
            request_data = {"get_id": "56", "act": "10", "go": "inv", "vcode": prepare}

            self._last_page = await self._connect.get_html(urls.URL_MAIN, params=request_data)
            self._where_i_am()

    async def _from_info_go_to_inventory(self) -> None:
        self.logger.debug("_from_info_go_to_inventory")

        if not self.info_string:
            self.logger.debug("not self.info_string")
            try:
                (prepare,) = compiled.finder_inv.findall(self._last_page)
            except Exception:
                text = f"{self._connect.login} {self._last_page=}"
                self.logger.exception(text)
                # raise
                return
        else:
            self.logger.debug("self.info_string exists")
            prepare = self.info_string
            self.logger.debug(prepare)

        if prepare:
            vcode = prepare[-1]
            data = {"get_id": "56", "act": "10", "go": "inv", "vcode": vcode}

            self._last_page = await self._connect.get_html(urls.URL_MAIN, params=data)
            self._where_i_am()
        else:
            self.logger.debug('from_info_to_inventar not find ?<=&go=inv&vcode=).+(?=\'" value="Инвентарь')

    async def _from_elixir_go_to_inventory(self) -> None:
        self.logger.debug("_from_elixir_go_to_inventory")
        self._last_page = await self._connect.get_html(urls.URL_ALL_ITEMS)
        self._where_i_am()

    async def _do_nothing(self) -> None:
        """Do nothing."""
        self.logger.debug("Do nothing")

    def _is_fight(self) -> bool:
        self.logger.debug("_is_fight")
        if location_constants.FIND_FIGHT in self._last_page:
            self.info_string = []
            self._location = LocationState.FIGHT
            self.logger.info(self._location)
            return True

        return False

    def _is_nature(self) -> bool:
        self.logger.debug("_is_nature")
        # if location_constants.FIND_DISABLED not in self.last_page:
        if location_constants.FIND_NATURE in self._last_page:
            self.info_string = []
            self._location = LocationState.NATURE
            self.logger.info(self._location)
            return True

        return False

    def _is_inventory(self) -> bool:
        self.logger.debug("_is_inventory")
        if location_constants.FIND_INVENTORY in self._last_page:
            self.info_string = []
            self._location = LocationState.INVENTORY
            self.logger.info(self._location)
            return True

        return False

    def _is_city(self) -> bool:
        self.logger.debug("_is_city")
        prepare = compiled.finder_in_city.findall(self._last_page)
        if prepare:
            self.info_string = prepare
            self._location = LocationState.CITY
            self.logger.info(self._location)
            return True

        return False

    def _is_info(self) -> bool:
        self.logger.debug("_is_info")
        prepare = compiled.finder_inv.findall(self._last_page)
        if prepare:
            self.info_string = prepare
            self._location = LocationState.INFO
            self.logger.info(self._location)
            return True

        return False

    def _is_elixir(self) -> bool:
        self.logger.debug("_is_elixir")
        if location_constants.FIND_ELIXIR in self._last_page:
            self.info_string = []
            self._location = LocationState.ELIXIR
            self.logger.info(self._location)
            return True

        return False

    def _is_ability(self) -> bool:
        self.logger.debug("_is_ability")
        prepare = compiled.finder_page_ability.findall(self._last_page)
        if prepare:
            self.info_string = []
            self._location = LocationState.ABILITY
            self.logger.info(self._location)
            return True

        return False

    def _is_castle(self) -> bool:
        self.logger.debug("_is_castle")
        prepare = compiled.finder_bcodes.findall(self._last_page)
        if prepare:
            self.info_string = prepare
            self._location = LocationState.CASTLE
            self.logger.info(self._location)
            return True

        if location_constants.FIND_MTOWER in self._last_page:
            self.info_string = [self._last_page]
            self._location = LocationState.CASTLE
            self.logger.info(self._location)
            return True

        return False

    def _where_i_am(self) -> LocationState:  # noqa: PLR0911
        self.logger.debug("_where_i_am")
        self.info_string = []

        if self._is_fight():
            return LocationState.FIGHT

        if self._is_nature():
            return LocationState.NATURE

        if self._is_elixir():
            return LocationState.ELIXIR

        if self._is_inventory():
            return LocationState.INVENTORY

        if self._is_city():
            return LocationState.CITY

        if self._is_info():
            return LocationState.INFO

        if self._is_castle():
            return LocationState.CASTLE

        if self._is_ability():
            return LocationState.ABILITY

        self._location = LocationState.ELIXIR
        self.logger.info(self._location)
        return LocationState.ELIXIR

    def _find_teleport(self) -> str | None:
        self.logger.debug("_find_teleport")
        prepare = compiled.finder_teleport.findall(self._last_page)
        if not prepare:
            self.logger.error(self._last_page)
            text = "No scrolls Teleport----"
            self.logger.error(text)
            return None
        return prepare.pop()

    def _create_data(self, city: int, founded: list[str]) -> aiohttp.FormData:
        self.logger.debug("_create_data")
        clean_data = founded.pop().replace("'", "").split(",")

        form_data = aiohttp.FormData(charset="windows-1251")  # cp1251
        form_data.add_field("post_id", 25)
        form_data.add_field("agree", AGREE)
        form_data.add_field("wtelid", city)
        form_data.add_field("vcode", clean_data[0])
        form_data.add_field("wuid", clean_data[1])
        form_data.add_field("wsubid", clean_data[2])
        form_data.add_field("wsolid", clean_data[3])

        return form_data

    async def _go_while(self, *, destination: str) -> None:
        self.logger.debug("_go_while")
        start = "city2_1"
        graph = CitiesGraph.OKTAL.value
        location = LocationNode(graph, start)
        bfs = BFS(location, destination)
        results = bfs.search()
        query = {"get_id": "56", "act": "10"}
        assert results is not None
        for go in results:
            pattern_vcode = location_pattern.FIND_CITY_ACTION_VCODE_PART1
            pattern_vcode += go
            pattern_vcode += location_pattern.FIND_CITY_ACTION_VCODE_PART2
            logger.error(f"{pattern_vcode=}")
            vcode = re.findall(pattern_vcode, self._last_page)
            query.update({"go": go, "vcode": vcode[0]})
            self._last_page = await self._connect.get_html(urls.URL_MAIN, params=query)
            self._where_i_am()

    async def _go_to_building(self) -> None:
        self.logger.debug("_go_to_building")
        base_query = {"get_id": "56", "act": "10", "go": "", "vcode": ""}

        self._last_page = await self._connect.get_html(urls.URL_MAIN, params=base_query)
        self._where_i_am()

    async def _go_to_watch_tower(self) -> None:
        self.logger.debug("_go_to_watch_tower")
        vcode = compiled.finder_vcode_bait.findall(self._last_page)
        base_query = {"get_id": "56", "act": "10", "go": "build", "pl": "citydef2", "vcode": vcode[0]}
        self._last_page = await self._connect.get_html(urls.URL_MAIN, params=base_query)
        self._where_i_am()

    async def _go_to_market(self) -> None:
        self.logger.debug("_go_to_market")
        await self._go_while(destination="city2_2")
        await self._go_to_building()

    async def _use_teleport(self, city: Teleport) -> None:
        prepare = self._find_teleport()
        prepare2 = compiled.finder_use.findall(prepare)  #  type: ignore[arg-type]
        if not prepare2:
            text = f"{prepare=}"
            self.logger.error(text)
            text = "DONT UNDERSTAND WHY"
            self.logger.error(text)
            return
        data = self._create_data(city=city.value, founded=prepare2)

        text = f"request : {data}"
        self.logger.debug(text)
        self._last_page = await self._connect.post_html(urls.URL_MAIN, data=data)
        self._where_i_am()

    async def go_to_location(self, destination: LocationState) -> None:
        text = f"go_to_location {destination=}"
        self.logger.debug(text)
        if destination == self._location:
            self.logger.info("person already on needed location")
            return

        if destination == LocationState.INVENTORY:
            await self._go_to_inventory(self._location)
            return

        if destination == LocationState.BAIT:
            await self._go_to_bait()
            return

        raise NotImplementedError

    async def _go_to_bait(self) -> None:
        self.logger.debug("_go_to_bait")
        self._last_page = await self._connect.get_html(urls.URL_MAIN)
        self._where_i_am()
        if self._location != LocationState.CITY:
            await self.go_to_location(destination=LocationState.INVENTORY)
            self._where_i_am()
            if self._location == LocationState.ELIXIR:
                self._last_page = await self._connect.get_html(urls.URL_ALL_ITEMS)
            self._last_page = await self._connect.get_html(urls.URL_SCROLL)
            await self._use_teleport(Teleport.OKTAL)

        await self._go_to_watch_tower()
        await self._join_to_bait()

    async def _join_to_bait(self) -> None:
        self.logger.debug("_join_to_bait")
        actions = compiled.finder_request_add.findall(self._last_page)
        if not actions:
            msg = "Not found action"
            self.logger.error(msg)
            return

        self.json_data = json.loads(actions[0])
        vcode = self.json_data.get("addRequest")
        if not vcode:
            msg = "NO BUTTON JOIN"
            self.logger.error(msg)
            return
        form_data = aiohttp.FormData(charset="windows-1251")  # cp1251
        form_data.add_field("type", "citydef")
        form_data.add_field("action", "requestAdd")
        form_data.add_field("vcode", vcode)
        form_data.add_field("r", random.random())  # noqa: S311, RUF100

        self._last_page = await self._connect.post_html(urls.URL_EVENT, data=form_data)
        self.json_data = json.loads(self._last_page)

        await self._set_money()

    async def _set_money(self) -> None:
        self.logger.debug("_set_money")
        vcode = self.json_data.get("a").get("upRequest")
        if not vcode:
            msg = "NO BUTTON SET MONEY"
            self.logger.error(msg)
            return

        form_data = aiohttp.FormData(charset="windows-1251")  # cp1251
        form_data.add_field("type", "citydef")
        form_data.add_field("action", "requestUp")
        form_data.add_field("vcode", vcode)
        form_data.add_field("r", random.random())  # noqa: S311, RUF100

        self._last_page = await self._connect.post_html(urls.URL_EVENT, data=form_data)

    async def _go_to_inventory(self, location: LocationState) -> None:
        self.logger.debug("_go_to_inventory")
        location_to_inventory: dict[LocationState, Callable] = {
            LocationState.FIGHT: self._do_nothing,
            LocationState.CITY: self._from_city_go_to_inventory,
            LocationState.NATURE: self._from_nature_go_to_inventory,
            LocationState.INVENTORY: self._do_nothing,
            LocationState.ELIXIR: self._from_elixir_go_to_inventory,
            LocationState.INFO: self._from_info_go_to_inventory,
            LocationState.CASTLE: self._from_castle_go_to_inventory,
        }
        await location_to_inventory[location]()
