from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING
from urllib.parse import quote

from src.config import logger
from src.config.game import urls
from src.domain.pattern.location.compiled import person_om_cell_group
from src.infrastructure.request import Connection
from src.infrastructure.request import my_ip
from src.use_cases.person.base import Person


if TYPE_CHECKING:
    from src.use_cases.request.base import Proxy


class User:
    def __init__(self) -> None:
        self.connection: Connection

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
            await self.connection.start()
            self.online = True

    async def close(self) -> None:
        await self.connection.close()

    async def get_person_on_cell(self) -> str:
        text = await self.connection.get_html("http://www.neverlands.ru/ch.php?lo=1&")
        # self.logger.error(f"{text=}")  # noqa: ERA001
        # PATTERN_PERSONS_ON_CELL_GROUP = r"\"(.{1,33}):(.{1,33}):(\d{1,3}):\w{1,6}\.gif;(.{1,30});.{0,35}:(\d|.{1,10000}):(\d|.{1,10000}):(\d|.{1,10000}):(\d|.{1,10000}):\w{1,10}\.gif;.{1,30}\"[,|\)]"  # noqa: E501, ERA001

        count2 = person_om_cell_group.findall(text)
        string = ""
        persons = []
        for row in count2:
            # self.logger.debug(f"{row=}")  # noqa: ERA001
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
                asyncio.create_task(Person(self.connection, nick)._execute()),  # type: ignore[func-returns-value, call-arg, arg-type]  # noqa: SLF001
            )

        persons = await asyncio.gather(*persons)
        for person in persons:
            text = f"nick={person.nick} level={person.level}"  # type: ignore[attr-defined]
            string += f"{text} {'В бою ' + person.fight_link if person.fight_link else 'Не в бою'}\n"  # type: ignore[attr-defined]  # noqa: RUF001
        self.person_on_cell = string
        return string

    async def get_info(self, nick: bytes) -> str:
        name = quote(nick)
        site_url = urls.URL_PLAYER_INFO + name

        # TODO: need do retry get  # noqa: FIX002, TD002, TD003
        return await self.connection.get_html(site_url)

    async def see_clan_items_potion(self) -> str:
        site_url = urls.URL_MAIN
        data = {
            "useaction": "clan-action",
            "addid": "3",
            "wca": "27",
        }

        # TODO: need do retry get  # noqa: TD003, FIX002, TD002
        answer = await self.connection.get_html(site_url, params=data, log_response=True)
        self.clan = answer
        return answer

    @property
    def status(self) -> str:
        if self.error:
            return "Error need relogin!"
        return "Online"