from __future__ import annotations
import asyncio
import re
from typing import TYPE_CHECKING
from urllib.parse import quote

import aiohttp

from src.config import logger
from src.config.game import constants
from src.config.game import urls
from src.domain.pattern.inv.pattern import FIND_USE_ITEM_MAGICREFORM
from src.domain.pattern.location.compiled import person_om_cell_group
from src.infrastructure.request import Connection
from src.infrastructure.request import my_ip
from src.use_cases.person.base import Person


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

        self.logger = logger

    async def init_connection(  # noqa: PLR0913
        self,
        ip: str,
        login: str,
        password: str,
        proxy_data: Proxy | None = None,
        proxy: bool = False,  # noqa: FBT001, FBT002
    ) -> None:
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

    async def close(self) -> None:
        await self.connection.close()

    async def get_person_on_cell(self) -> str:
        text = await self.connection.get_html(urls.URL_SELL_INFO)
        self.last_page_text = text
        count2 = person_om_cell_group.findall(text)
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

    async def get_info(self, nick: str) -> str:
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

    async def use_buff(self, *, buff_name: str = "Превосходное Зелье Маны") -> None:
        item_pattern = FIND_USE_ITEM_MAGICREFORM.format(name=buff_name)
        self.finder_use_item = re.compile(item_pattern)
        await self._use()

    async def _use(self) -> None:
        result = self.finder_use_item.finditer(self.last_page_text)
        item = next(result).group(0)
        (magicreuid, fornickname, _, vcode) = item.replace("'", "").split(",")
        form_data = aiohttp.FormData(charset="windows-1251")  # cp1251
        form_data.add_field("post_id", 46)
        form_data.add_field("magicrestart", 1)
        form_data.add_field("magicreuid", magicreuid)
        form_data.add_field("vcode", vcode)
        form_data.add_field("fornickname", fornickname)

        self.last_page_text = await self.connection.post_html(urls.URL_MAIN, data=form_data)

    @property
    def status(self) -> str:
        if self.error:
            return "Error need relogin!"
        return "Online"
