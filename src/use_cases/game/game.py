from __future__ import annotations
import asyncio
import random
from typing import TYPE_CHECKING
from urllib.parse import quote

from src.config import logger
from src.config.game import constants
from src.config.game import urls
from src.domain.pattern.location import compiled
from src.domain.value_object.classes import LocationState
from src.domain.value_object.classes import PersonType
from src.infrastructure.request import Connection
from src.infrastructure.request import my_ip
from src.use_cases.game.buff import Buff
from src.use_cases.game.fight_asist import AsistFight
from src.use_cases.game.location.base import Location


if TYPE_CHECKING:
    from src.use_cases.person.buff import effects
    from src.use_cases.request.base import Proxy


class User:
    def __init__(self) -> None:
        self.connection: Connection
        self.login: str
        self.last_page_text: str = ""

        self.online: bool = False
        self.error: bool = False

        self.clan: str = ""
        self.ab_started = True

        self.logger = logger

        self.fight: AsistFight
        self.location: Location
        self.buff: Buff

    async def _check_ip(
        self,
        ip: str,
        proxy_data: Proxy | None = None,
        proxy: bool = False,  # noqa: FBT001, FBT002
    ) -> None:
        if proxy:
            real_ip = await my_ip(user_proxy=proxy_data)
        else:
            real_ip = await my_ip(user_proxy=None)

        if ip in real_ip:
            text = f"\n-------ip------- {real_ip} LOGIN {self.login}" * 5
            self.logger.info(text)
            self.error = False
        else:
            text = f"{self.login} {ip=} not in real IP={real_ip}"
            self.logger.error(text)
            self.error = True

    def get_connection(self) -> Connection:
        return self.connection

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

        await self._check_ip(ip=ip, proxy_data=proxy_data, proxy=proxy)

        if not self.error:
            self.connection = Connection(
                proxy_data=proxy_data,
                login=self.login,
                password=password,
            )
            self.last_page_text = await self.connection.start()
            self.online = True

        self.fight = AsistFight(
            connection=self.connection,
            login=self.login,
            person_type=self.person_type,
        )

        self.init_location()
        self.init_buff()

    def init_location(self) -> None:
        self.location = Location(
            connect=self.connection,
            last_page=self.last_page_text,
        )

    def init_buff(self) -> None:
        self.buff = Buff(
            connection=self.connection,
            location=self.location,
        )

    async def close(self) -> None:
        await self.connection.close()

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

    async def use_buff(self, *, need_effects: list[effects.Effect] | None = None) -> None:
        location = self.location.get_actual_location(self.last_page_text)
        if location != LocationState.INVENTORY:
            await self.location.go_to_location(LocationState.INVENTORY)

        self.last_page_text = await self.get_info()
        await self.buff.use_strategy_buff(page_text=self.last_page_text, need_effects=need_effects)

    async def start_fight(self, end_battle: bool = True, write_log: bool = False, bait: bool = False) -> None:  # noqa: FBT001, FBT002
        bait = True
        text = f"start_fight {bait=}"
        logger.debug(text)

        await self.fight.run_fight(
            last_page_text=self.last_page_text,
            end_battle=end_battle,
            ab_started=self.ab_started,
            write_log=write_log,
            bait=bait,
        )

    async def start_wait_bait(self, write_log: bool = False) -> None:  # noqa: FBT002, FBT001
        not_in_fight = True
        while not_in_fight:
            fight = compiled.finder_frame.findall(string=self.last_page_text)
            if fight:
                break

            text = f"{self.login} Wait fight"
            logger.error(text)
            await asyncio.sleep(random.uniform(0.6, 1.3))

            self.last_page_text = await self.connection.get_html(urls.URL_MAIN)

        await self.start_fight(end_battle=False, write_log=write_log, bait=True)

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

    async def go_to_location(self, *, location: LocationState = LocationState.BAIT) -> None:
        await self.location.go_to_location(location)
