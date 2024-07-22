from __future__ import annotations
import contextlib
import logging
import re
import time
from collections.abc import AsyncGenerator
from collections.abc import Generator
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import TYPE_CHECKING

import aiohttp

from src.config.game import urls
from src.domain.pattern.fight import compiled
from src.domain.pattern.fight import pattern
from src.domain.value_object.classes import PersonType
from src.use_cases.game.fight.fight import Fight


if TYPE_CHECKING:
    from src.infrastructure.request import Connection

formatter = logging.Formatter("%(asctime)s | %(levelname)8s | %(filename)s:%(lineno)3d | %(message)s")

request_file_logger = logging.getLogger("fight")
request_handler = RotatingFileHandler("battle_history.log", maxBytes=5_242_880, backupCount=10)
request_handler.setFormatter(formatter)
request_file_logger.addHandler(request_handler)
request_file_logger.setLevel(logging.DEBUG)


@contextlib.asynccontextmanager
async def timing_decorator() -> AsyncGenerator[None, None]:
    start_time = time.perf_counter()
    try:
        yield
    finally:
        end_time = time.perf_counter()
        text = f"Time spent: {end_time - start_time:.5f} seconds"
        request_file_logger.info(text)


def check_iter(fight_iteration: int, start_time: float, nickname: str) -> float:
    text = f"fight_iteration - '{fight_iteration}'"
    request_file_logger.info(text)
    if fight_iteration % 50 == 0:
        text = f"{nickname} ----TOO LONG FIGHT---- >= {fight_iteration}"
        request_file_logger.error(text)
    end_time = time.perf_counter()
    text = f"iter_time - {end_time - start_time}"
    request_file_logger.debug(text)
    return end_time


class Node:
    def __init__(self, data: str) -> None:
        self.data = data
        self.next: Node | None = None

    def __repr__(self) -> str:
        return self.data


class LinkedList:
    def __init__(self, node: Node | None = None) -> None:
        self.head: Node | None = None

        if node is not None:
            self.head = node

    def add_last(self, node: Node) -> None:
        if self.head is None:
            self.head = node
            return
        for current_node in self:  # noqa: B007
            pass
        current_node.next = node

    def get_latest(self) -> str | None:
        node = self.head
        if node is None:
            return None
        last = node.data
        while node is not None:
            last = node.data
            node = node.next

        return last

    def __repr__(self) -> str:
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        return "\n".join(nodes)

    def __iter__(self) -> Generator[Node, None, None]:
        node = self.head
        while node is not None:
            yield node
            node = node.next


class AssistFight:
    def __init__(
        self,
        connection: Connection,
        login: str,
        person_type: PersonType = PersonType.MAG,
    ) -> None:
        self.connection = connection
        self._fight_class = Fight(login, person_type)
        self.login = login
        self._continue_fight = True
        self.last_page_text = ""
        self.log_linked_list = LinkedList()
        self.log_file_linked_list = LinkedList()
        self.fight_id = "0"
        self.log_page = 1

    def _is_alive(self, hp: str) -> bool:
        return hp != "0"

    def _raise_error(self) -> None:
        text_for_message = f"{self.login} YOU KILLED BUT FIGHT NOT ENDED"
        request_file_logger.error(text_for_message)

    def _is_check_alive(self) -> bool:
        result: list[str] = re.findall(pattern.FIND_PARAM_OW, self.last_page_text)
        if result:
            new_result = result.pop()
            param_ow = new_result.replace("]", "").replace('"', "").replace("[", "").split(",")
            if param_ow:
                hp = param_ow[1]
                if not self._is_alive(hp):
                    self._raise_error()
                    return False
        return True

    def _is_end_battle(self) -> bool:
        self._end_battle = re.findall(pattern.FIND_FEXP, self.last_page_text)
        if self._end_battle:
            text = f"{self.login} END BATTLE {self._end_battle=}"
            request_file_logger.info(text)
            return True
        return False

    def _create_end_battle_data(self) -> dict[str, str]:
        new_result: str = self._end_battle.pop()
        fexp: list[str] = new_result.replace("]", "").replace('"', "").replace("[", "").split(",")
        return self._prepare_data_end_battle(fexp)

    def _prepare_data_end_battle(self, fexp: list[str]) -> dict[str, str]:
        text_for_message = (
            f"{self.login} END BATTLE {self._fight_class._bot_level} count {self._fight_class._bot_count}"  # noqa: SLF001
        )
        request_file_logger.info(text_for_message)
        return {
            "get_id": "61",
            "act": "7",
            "fexp": fexp[0],
            "fres": fexp[1],
            "vcode": fexp[3],
            "ftype": fexp[5],
            "min1": fexp[8],
            "max1": fexp[9],
            "min2": fexp[10],
            "max2": fexp[11],
            "sum1": fexp[12],
            "sum2": fexp[13],
        }

    def _create_fight_data(self, bait: bool = False) -> dict[str, str]:  # noqa: FBT001, FBT002
        if not self._is_check_alive():
            return {"STOP": "STOP"}
        self._fight_class.setup_value(self.last_page_text)
        if self._is_end_battle():
            return self._create_end_battle_data()

        return self._logic(bait=bait)

    def _write_log(self) -> None:
        part1 = f"inu-{self._inu} inb-{self._inb} ina-{self._ina}"
        part2 = f" my_od-{self._my_od} my_mp-{self._my_mp}"
        part3 = f" my_hp-{self._my_hp}"
        text = part1 + part2 + part3
        request_file_logger.debug(text)

    def _logic(self, bait: bool = False) -> dict[str, str]:  # noqa: FBT001, FBT002
        self._my_od, self._my_mp, self._my_hp = self._fight_class.get_state()

        self._fight_class.fight(bait=bait)
        data = self._fight_class.get_queries_param()
        self._inu = data.inu
        self._inb = data.inb
        self._ina = data.ina

        self._write_log()
        return self._fight_class.get_data()

    def _data_to_formdata(self, data: dict[str, str]) -> aiohttp.FormData:
        form_data = aiohttp.FormData(charset="windows-1251")  # cp1251
        for key, value in data.items():
            form_data.add_field(key, value)
        return form_data

    def _battle_log(self) -> None:
        self._log_to_dict()

    def _log_to_dict(self) -> None:  # noqa: PLR0912, C901, RUF100
        all_nodes = []
        element = self._fight_class.logs
        start_add = False
        latest = self.log_linked_list.get_latest()
        if latest is None:
            start_add = True

        for item in element[::-1]:
            if isinstance(item, int):
                continue
            my_string = f"{item[0][1]} " if isinstance(item, list) else "    WTF    "
            for _i, el in enumerate(item[1:], start=1):
                if isinstance(el, list) and len(el) == 2:  # noqa: PLR2004
                    pass
                elif isinstance(el, list) and len(el) in (3, 4):
                    my_string += f"{el[1]} "
                elif isinstance(el, list) and len(el) > 5:  # noqa: PLR2004
                    my_string += f"{el[2]} {el[3]} "
                else:
                    my_string += f"{el} "

            if start_add:
                self.log_linked_list.add_last(Node(my_string))
            if latest == my_string:
                start_add = True
            all_nodes.append(Node(my_string))

        if not start_add:
            for node in all_nodes:
                self.log_linked_list.add_last(node)

    def _write_log_to_file(self) -> None:
        name = f"logs/{self.login}_{self._fight_class.fight_ty[8]}.txt"
        with Path(name).open("w") as file:
            file.write(str(self.log_linked_list))

    def _write_log_history(self) -> None:
        name = f"logs/{self.login}_full_{self._fight_class.fight_ty[8]}.txt"
        with Path(name).open("w") as file:
            file.write(str(self.log_file_linked_list))

    async def _stop_or_hit(self, end_battle: bool = True, write_log: bool = False, bait: bool = False) -> None:  # noqa: FBT002, FBT001
        data = self._create_fight_data(bait=bait)

        if write_log:
            if self.fight_id == "0" and self._fight_class.fight_ty:
                self.fight_id = self._fight_class.fight_ty[8]

            if self.fight_id != "0":
                await self.get_logs()

        if "post_id" in data:
            form_data = self._data_to_formdata(data)
            self.last_page_text = await self.connection.post_html(urls.URL_MAIN, data=form_data)
            self._battle_log()
        elif "retry" in data:
            request_file_logger.debug("retry")
            self.last_page_text = await self.connection.get_html(urls.URL_MAIN)
            self._battle_log()
        elif "STOP" in data:
            self._continue_fight = False
        else:
            request_file_logger.info("Request for the end battle")
            if end_battle:
                self.last_page_text = await self.connection.get_html(urls.URL_MAIN, params=data)
            self._battle_log()
            self._continue_fight = False

    async def get_logs(self) -> None:  # noqa: C901
        request_file_logger.debug("get_logs")
        data = {
            "fid": self.fight_id,
            "p": self.log_page,
        }

        log_text = await self.connection.get_html(urls.URL_LOG, params=data)

        logs_string = compiled.finder_logs.findall(log_text)
        normal_logs_string = logs_string[0].replace(",,", ',"was empty in log",')
        logs = eval(normal_logs_string)  # nosec B307  # noqa: S307
        if logs == []:
            text = f"Empty log file  {logs_string=}"
            request_file_logger.debug(text)
            return

        params_string = compiled.finder_params.findall(log_text)
        params = eval(params_string[0])  # nosec B307  # noqa: S307
        pages = params[0]

        if pages == 0:
            return

        request_file_logger.debug("pages not 0")

        if self.log_page > pages:
            request_file_logger.debug("pages != 1 and self.log_page >= pages")
            return

        request_file_logger.debug("pages == 1 or self.log_page < pages")
        request_file_logger.debug("self page %s", self.log_page)

        latest = self.log_file_linked_list.get_latest()
        all_nodes = []
        start_add = False
        if latest is None:
            start_add = True

        text = f"{latest=}"
        request_file_logger.debug(text)
        for log in logs[1:]:
            if start_add:
                self.log_file_linked_list.add_last(Node(str(log)))

            if latest == str(log):
                start_add = True

            all_nodes.append(Node(str(log)))

        if not start_add:
            for node in all_nodes:
                self.log_file_linked_list.add_last(node)

        text = f"{start_add=} {bool(all_nodes)=}"
        request_file_logger.debug(text)

        if len(logs) >= 21:  # noqa: PLR2004
            self.log_page += 1
        if pages == 1:
            return
        await self.get_logs()

    @timing_decorator()
    async def run_fight(
        self,
        last_page_text: str,
        ab_started: bool,  # noqa: FBT001
        end_battle: bool = True,  # noqa: FBT001, FBT002
        write_log: bool = False,  # noqa: FBT001, FBT002
        bait: bool = False,  # noqa: FBT002, FBT001
    ) -> None:
        self.last_page_text = last_page_text
        fight_iteration = 0
        start_time = time.perf_counter()

        self._continue_fight = True
        while self._continue_fight:
            await self._stop_or_hit(end_battle, write_log, bait=bait)
            fight_iteration += 1
            start_time = check_iter(fight_iteration, start_time, self.login)

        if ab_started:
            self._write_log_to_file()

        if write_log:
            self._write_log_history()
