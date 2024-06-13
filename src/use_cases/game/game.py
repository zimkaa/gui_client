from __future__ import annotations
import asyncio
import re
from typing import TYPE_CHECKING
from urllib.parse import quote

import aiohttp

from src.config import logger
from src.config.game import constants
from src.config.game import urls
from src.domain.item import use
from src.domain.pattern.inv import pattern
from src.domain.pattern.location import compiled
from src.domain.value_object.classes import PersonType
from src.infrastructure.request import Connection
from src.infrastructure.request import my_ip
from src.use_cases.game.fight_asist import AsistFight
from src.use_cases.person.base import Person
from src.use_cases.person.buff import effects


if TYPE_CHECKING:
    from src.use_cases.request.base import Proxy


class User:
    def __init__(self) -> None:
        self.connection: Connection
        self.login: str
        self.last_page_text: str = ""

        self.online: bool = False
        self.error: bool = False

        self.person_on_cell: str = ""
        self.person_list: list[Person] = []
        self.clan: str = ""
        self.ab_started = True

        self.logger = logger
        self.fight: AsistFight

    async def init_connection(  # noqa: PLR0913
        self,
        ip: str,
        login: str,
        password: str,
        mag_or_warrior: str,
        proxy_data: Proxy | None = None,
        proxy: bool = False,  # noqa: FBT001, FBT002
    ) -> None:
        self.person_type = PersonType(mag_or_warrior)
        self.login = login
        if proxy:
            real_ip = await my_ip(user_proxy=proxy_data)
        else:
            real_ip = await my_ip(user_proxy=None)

        if ip in real_ip:
            text = f"\n-------ip------- {real_ip} LOGIN {login}" * 5
            self.logger.info(text)
            self.error = False
        else:
            text = f"{login} {ip=} not in real IP={real_ip}"
            self.logger.error(text)
            self.error = True

        if not self.error:
            self.connection = Connection(
                proxy_data=proxy_data,
                login=login,
                password=password,
            )
            self.last_page_text = await self.connection.start()
            self.online = True

        self.fight = AsistFight(
            connection=self.connection,
            login=self.login,
            person_type=self.person_type,
        )

    async def close(self) -> None:
        await self.connection.close()

    async def get_person_on_cell(self) -> str:
        text = await self.connection.get_html(urls.URL_SELL_INFO)
        self.last_page_text = text
        count2 = compiled.person_om_cell_group.findall(text)
        string = ""
        persons = []
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
                asyncio.create_task(Person(connection=self.connection, login=nick)._execute()),  # type: ignore[func-returns-value, call-arg, arg-type]  # noqa: SLF001
            )

        persons = await asyncio.gather(*persons)
        for person in persons:
            text = f"nick={person.nick} level={person.level}"  # type: ignore[attr-defined]
            string += f"{text} {'В бою ' + person.fight_link if person.fight_link else 'Не в бою'}\n"  # type: ignore[attr-defined]  # noqa: RUF001
        self.person_on_cell = string
        return string

    async def get_info(self, nick: str | None = None) -> str:
        if nick is None:
            nick = self.login
        name = quote(nick, encoding=constants.ENCODING)
        # TODO: need do retry get  # noqa: FIX002, TD002, TD003
        return await self.connection.get_html(urls.URL_PLAYER_INFO.format(name=name))

    async def see_clan_items_potion(self) -> str:
        data = {
            "useaction": "clan-action",
            "addid": "3",
            "wca": "27",
        }

        # TODO: need do retry get  # noqa: TD003, FIX002, TD002
        answer = await self.connection.get_html(urls.URL_MAIN, params=data)
        self.clan = answer
        return answer

    async def use_strategy_buff(self, *, need_effects: list[effects.Effect] | None = None) -> None:
        self.last_page_text = await self.get_info()
        if need_effects is None:
            need_effects = [
                effects.Effect(name="Зелье Иммунитета", type_=effects.ElementType.POTION),
                effects.Effect(name="Превосходное Зелье Ловких Ударов", type_=effects.ElementType.POTION, count=2),
                effects.Effect(name="Превосходное Зелье Жизни", type_=effects.ElementType.POTION, count=2),
                effects.Effect(name="Свиток каменной кожи", type_=effects.ElementType.SCROLL, count=2),
            ]

        self.effects = effects.PersonEffects(page_text=self.last_page_text, need_effects=need_effects)
        element_list = self.effects.get_effects()
        # PersonInv
        self.last_page_text = await self.connection.get_html(urls.URL_POTION)
        if element_list:
            for element in element_list:
                if element.type_ == effects.ElementType.POTION:
                    await self._use_potion(buff_name=element.name)
                elif element.type_ in (effects.ElementType.SCROLL, effects.ElementType.ELIXIR):
                    await self._use_scroll(scroll_name=element.name)
                # elif element.type_ == effects.ElementType.CASTLE:  # noqa: ERA001
                #     await self._use_castle(scroll_name=element.name)  # noqa: ERA001

    async def _use_castle(self, *, buff_name: str = "Превосходное Зелье Маны") -> None:
        item_pattern = pattern.FIND_USE_ITEM_MAGICREFORM.format(name=buff_name)
        finder_use_item = re.compile(item_pattern)
        result = finder_use_item.finditer(self.last_page_text)
        item = next(result).group(0)
        (magicreuid, fornickname, _, vcode) = item.replace("'", "").split(",")
        form_data = aiohttp.FormData(charset="windows-1251")  # cp1251
        form_data.add_field("post_id", 46)
        form_data.add_field("magicrestart", 1)
        form_data.add_field("magicreuid", magicreuid)
        form_data.add_field("vcode", vcode)
        form_data.add_field("fornickname", fornickname)

        self.last_page_text = await self.connection.post_html(urls.URL_MAIN, data=form_data)

    async def _use_potion(self, *, buff_name: str = "Превосходное Зелье Маны") -> None:
        item_pattern = pattern.FIND_USE_ITEM_MAGICREFORM.format(name=buff_name)
        text = f"{item_pattern=}"
        self.logger.critical(text)
        finder_use_item = re.compile(item_pattern)
        result = finder_use_item.finditer(self.last_page_text)
        self.logger.warning(result)
        item = next(result).group(0)
        self.logger.critical(result)
        (magicreuid, fornickname, _, vcode) = item.replace("'", "").split(",")
        form_data = aiohttp.FormData(charset="windows-1251")  # cp1251
        form_data.add_field("post_id", 46)
        form_data.add_field("magicrestart", 1)
        form_data.add_field("magicreuid", magicreuid)
        form_data.add_field("vcode", vcode)
        form_data.add_field("fornickname", fornickname)

        self.last_page_text = await self.connection.post_html(urls.URL_MAIN, data=form_data)

    async def _use_scroll(self, *, scroll_name: str = "Свиток каменной кожи") -> None:
        item_id = use.binding_dict.get(scroll_name)  # type: ignore[call-overload]
        if item_id is None:
            msg = f"Unknown buff name: {scroll_name}"
            raise ValueError(msg)
        item_pattern = pattern.FIND_USE_ITEM_SCROLL.format(name=item_id)

        finder_use_item = re.compile(item_pattern)
        result = finder_use_item.finditer(self.last_page_text)
        item = next(result).group(0)
        arg_lst = item.replace(r"' }", "").split("&")
        params = {
            "get_id": 43,
            "act": item,
            "uid": arg_lst[0],
        }
        for item in arg_lst[1:]:
            key, value = item.split("=")
            params[key] = value

        self.last_page_text = await self.connection.get_html(urls.URL_MAIN, params=params)

    async def start_fight(self, end_battle: bool = True) -> None:  # noqa: FBT001, FBT002
        logger.debug("start_fight")

        await self.fight.run_fight(
            last_page_text=self.last_page_text,
            end_battle=end_battle,
            ab_started=self.ab_started,
        )

    async def start_wait_bait(self) -> None:
        not_in_fight = True
        while not_in_fight:
            fight = compiled.finder_frame.findall(string=self.last_page_text)
            if fight:
                break

            logger.error("Wait fight")
            await asyncio.sleep(0.1)

            self.last_page_text = await self.connection.get_html(urls.URL_MAIN)

        await self.start_fight(end_battle=False)

    async def wait_fight_while(self) -> None:
        logger.critical("wait_fight_while")
        while self.ab_started:
            fight = compiled.finder_frame.findall(string=self.last_page_text)
            if fight:
                break

            logger.error("Wait fight")
            await asyncio.sleep(10)

            self.last_page_text = await self.connection.get_html(urls.URL_MAIN)

    async def start_ab_while(self) -> None:
        logger.critical("start_ab_while")
        self.ab_started = True
        while self.ab_started:
            await self.wait_fight_while()
            logger.critical("After wait fight")
            if self.ab_started:
                await self.start_fight()
                self.last_page_text = await self.connection.get_html(urls.URL_MAIN)

    async def stop_ab_while(self) -> None:
        logger.critical("stop_ab_while")
        self.ab_started = False

    @property
    def status(self) -> str:
        if self.error:
            return "Error need relogin!"
        return "Online"
