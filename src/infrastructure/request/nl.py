from __future__ import annotations
import inspect
import logging
import os
from collections import defaultdict
from datetime import datetime
from http import HTTPStatus
from http.cookies import SimpleCookie
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any
from urllib.parse import quote

import aiohttp

from src.config import logger
from src.config.game import connection

# from tenacity import retry  # noqa: ERA001
# from tenacity import stop_after_attempt  # noqa: ERA001
# from tenacity import wait_incrementing  # noqa: ERA001
from src.config.game import constants
from src.config.game import urls
from src.infrastructure.errors import request
from src.use_cases.request.base import BaseConnection


formatter = logging.Formatter("%(asctime)s | %(levelname)8s | %(filename)s:%(lineno)3d | %(message)s")

logging.getLogger("urllib3").setLevel("WARNING")
request_file_logger = logging.getLogger("request_to_nl")
request_handler = RotatingFileHandler("request.log", maxBytes=5_242_880, backupCount=10)
request_handler.setFormatter(formatter)
request_file_logger.addHandler(request_handler)
request_file_logger.setLevel(logging.DEBUG)

request_error_file_logger = logging.getLogger("error_request")
error_handler = RotatingFileHandler("error_request.log", maxBytes=5_242_880, backupCount=10)
error_handler.setFormatter(formatter)
request_error_file_logger.addHandler(error_handler)
request_error_file_logger.setLevel(logging.DEBUG)


COOKIE_FOLDER = Path("cookies")


class Connection(BaseConnection):
    def __init__(self, login: str, password: str, proxy: bool = False) -> None:  # noqa: FBT001, FBT002
        self.cookies_file_path = COOKIE_FOLDER / f"{login}_cookies.txt"
        self.cookies_binary_file_path = COOKIE_FOLDER / f"{login}_cookie"
        self.proxy = proxy
        self._data: aiohttp.FormData | None = None
        if login and password:
            form_data = aiohttp.FormData(charset="windows-1251")  # cp1251
            form_data.add_field("player_nick", login)
            form_data.add_field("player_password", password)
            self._data = form_data

        self._cookies: defaultdict[Any, SimpleCookie] = defaultdict(SimpleCookie)
        self.login = login

        self._session: aiohttp.ClientSession

    async def start(self) -> None:
        logger.info("\n\nstart object id = %s \n\n", id(self))
        self._set_session()
        await self._log_in()

    async def reconnect(self) -> None:
        logger.debug("reconnect")
        await self._log_in()

    def _set_session(self) -> None:
        logger.debug("_set_session")
        self._session = aiohttp.ClientSession(trust_env=self.proxy, headers=constants.HEADER)

    async def close(self) -> None:
        logger.info("close")
        await self._session.close()

    def _is_valid_cookies(self) -> bool:
        logger.debug("_is_valid_cookies?")
        if not os.listdir(COOKIE_FOLDER):
            logger.error("NO FILE COOKIE_FOLDER=%s", COOKIE_FOLDER)
            return False

        dt = datetime.now()  # noqa: DTZ005
        dt_without_microseconds = dt.replace(microsecond=0)
        # with open(COOKIE_FILE_PATH, "rb") as file:
        #     self._cookies = pickle.load(file)  # noqa: ERA001

        with Path(self.cookies_file_path).open() as f:
            info = f.read()

        self._cookies[("neverlands.ru", "/")] = SimpleCookie(info)

        if not self._cookies.get(("neverlands.ru", "/")).get("NeverExpi"):  # type: ignore[union-attr]
            logger.error("NO COOKIES %s", self._cookies)
            return False
        timestamp = self._cookies.get(("neverlands.ru", "/")).get("NeverExpi").value  # type: ignore[union-attr]

        user = self._cookies.get(("neverlands.ru", "/")).get("NeverNick").value  # type: ignore[union-attr]

        login = quote(self.login, encoding=constants.ENCODING)

        if user != login:
            logger.error("Cookie another person user-%s != login-%s", user, login)
            return False
        if int(dt_without_microseconds.timestamp()) >= int(timestamp):
            logger.error("int(dt_without_microseconds.timestamp()) >= int(timestamp)")
            logger.error("%s", int(dt_without_microseconds.timestamp()) >= int(timestamp))
            logger.error("%s %s", int(dt_without_microseconds.timestamp()), int(timestamp))
            return False
        return True

    def _is_logged_in(self, result: str) -> bool:
        logger.debug("_is_logged_in")
        if connection.LOGIN_TEXT in result:
            logger.error("NOT LOGGED")
            self._session.cookie_jar.clear()
            return False
        if connection.RELOGIN_TEXT in result:
            logger.error("NEED RELOGIN")
            self._session.cookie_jar.clear()
            return False
        return True

    def _save_cookies(self) -> None:
        logger.debug("_save_cookies")
        self._session.cookie_jar.save(self.cookies_binary_file_path)  # type: ignore[attr-defined]

        # # HACK: for see cookies  # noqa: FIX004
        # for cookie in self._session.cookie_jar:
        #     logger.debug("key = %s value = %s", cookie.key, cookie.value)  # noqa: ERA001
        # logger.debug("SAVE COOKIES")  # noqa: ERA001

    async def _get_login(self) -> str:
        logger.debug("_get_login")

        await self.get_html(urls.URL)
        if self._data:
            logger.debug("try to login")
            await self.post_html(urls.URL_GAME, self._data, auth=True)  # type: ignore[arg-type]
        else:
            text = f"No login data {self._data=}"
            logger.error(text)
            raise Exception(text)  # noqa: TRY002
        self._save_cookies()
        return await self.get_html(urls.URL_MAIN)

    async def _log_in(self) -> None:
        logger.debug("_log_in")
        if self._is_valid_cookies():
            self._session.cookie_jar.update_cookies(self._cookies.get(("neverlands.ru", "/")))  # type: ignore[arg-type]
            logger.debug("Valid cookies update_cookies")
            result = await self.get_html(urls.URL_MAIN)
        else:
            logger.debug("Log in NOT Valid cookies")
            result = await self._get_login()

        if not self._is_logged_in(result):
            await self._get_login()
            # msg = "LOGIN ERROR"  # noqa: ERA001
            # raise Exception(msg)  # noqa: ERA001

        await self.get_html(urls.URL_SELL_INFO)

        self._session.cookie_jar.clear()
        if self._is_valid_cookies():
            self._session.cookie_jar.update_cookies(self._cookies.get(("neverlands.ru", "/")))  # type: ignore[arg-type]
            logger.debug("Updated cookies")
        await self.get_html(urls.URL_MAIN)

    def _write_all_debug_logs(self, text: str) -> None:
        request_file_logger.debug(text)

    def _write_error_logs(self, text: str, response: str | None = None) -> None:
        response_text = f"{response}\n" if response else ""
        all_text = f"{text}\n{response_text}"
        request_file_logger.error(all_text)
        request_error_file_logger.error(all_text)
        request_error_file_logger.info("Delimiter")

    # @retry(
    #     wait=wait_incrementing(start=0.5, increment=0.5, max=3),  # noqa: ERA001
    #     stop=stop_after_attempt(3),  # noqa: ERA001
    #     reraise=True,  # noqa: ERA001
    # )  # noqa: ERA001, RUF100
    async def get_html(self, site_url: str, data: dict | None = None) -> str:
        func = inspect.currentframe()
        assert func

        answer = await self._session.get(site_url, params=data)  # OLD WORK

        print_debug_text = ""
        for key, value in answer.__dict__.items():
            print_debug_text += f"{key}: {value}\n"

        if answer.status == HTTPStatus.OK:
            result = await answer.text()
            text = f"{self.login} {func.f_code.co_name} {data=} {site_url=} {result=}"
            self._write_all_debug_logs(text)
            return result

        if answer.status == HTTPStatus.BAD_GATEWAY:
            text = f"{self.login} {func.f_code.co_name} {answer.status=}\n {data=} {site_url=}\n"
            response = await answer.text()
            text += print_debug_text
            self._write_error_logs(text, response)
            raise request.GetCode502Error

        if answer.status == HTTPStatus.GATEWAY_TIMEOUT:
            text = f"{self.login} {func.f_code.co_name} {answer.status=}\n {data=} {site_url=}\n"
            response = await answer.text()
            text += print_debug_text
            self._write_error_logs(text, response)
            raise request.GetCode504Error

        if answer.status == 546:  # noqa: PLR2004
            text = f"{self.login} {func.f_code.co_name} {answer.status=}\n {data=} {site_url=}\n"
            response = await answer.text()
            text += print_debug_text
            self._write_error_logs(text, response)
            raise request.GetCode546Error

        text = f"{self.login} {func.f_code.co_name} error code: {answer.status=}"
        response = await answer.text()
        text += print_debug_text
        self._write_error_logs(text, response)
        raise request.GetNewCodeError(text)

    # @retry(
    #     wait=wait_incrementing(start=0.5, increment=0.5, max=3),  # noqa: ERA001
    #     stop=stop_after_attempt(3),  # noqa: ERA001
    #     reraise=True,  # noqa: ERA001
    # )  # noqa: ERA001, RUF100
    async def post_html(self, site_url: str, data: dict | None = None, auth: bool = False) -> str:  # noqa: FBT002, FBT001
        func = inspect.currentframe()
        assert func

        if auth:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
            }
            answer = await self._session.post(site_url, data=data, headers=headers)
        else:
            answer = await self._session.post(site_url, data=data)

        print_debug_text = ""
        for key, value in answer.__dict__.items():
            print_debug_text += f"{key}: {value}\n"

        if answer.status == HTTPStatus.OK:
            result = await answer.text()
            text = f"{self.login} {func.f_code.co_name} {data=} {site_url=} {result=}"
            self._write_all_debug_logs(text)
            return result

        if answer.status == HTTPStatus.BAD_GATEWAY:
            text = f"{self.login} {func.f_code.co_name} {answer.status=}\n {data=} {site_url=}\n"
            response = await answer.text()
            text += print_debug_text
            self._write_error_logs(text, response)
            raise request.PostCode502Error

        text = f"{self.login} {func.f_code.co_name} error code: {answer.status=}"
        response = await answer.text()
        text += print_debug_text
        self._write_error_logs(text, response)
        raise request.PostNewCodeError(text)
