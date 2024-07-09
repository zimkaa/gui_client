from __future__ import annotations
import inspect
import logging
import os
import pickle
from collections import defaultdict
from datetime import UTC
from datetime import datetime
from http import HTTPStatus
from http.cookies import SimpleCookie
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import quote

import aiohttp
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_incrementing

from src.config import logger
from src.config import settings
from src.config.game import connection
from src.config.game import constants
from src.config.game import urls
from src.infrastructure.errors import exception
from src.infrastructure.errors import request
from src.use_cases.request.base import BaseConnection


if TYPE_CHECKING:
    from src.use_cases.request.base import Proxy


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
    def __init__(
        self,
        login: str,
        password: str,
        proxy_data: Proxy | None = None,
    ) -> None:
        self.cookies_txt_file_path = COOKIE_FOLDER / f"{login}_cookies.txt"
        self.cookies_binary_file_path = COOKIE_FOLDER / f"{login}_cookie"
        self.proxy_data = proxy_data
        self.proxy_kwargs = {}
        if proxy_data:
            self.proxy_kwargs = {
                "proxy": proxy_data.proxy,
                "proxy_auth": proxy_data.proxy_auth,
            }
        form_data = aiohttp.FormData(charset="windows-1251")  # cp1251
        form_data.add_field("player_nick", login)
        form_data.add_field("player_password", password)
        self._data = form_data

        self._cookies: defaultdict[tuple[str, str], SimpleCookie] = defaultdict(SimpleCookie)  # aiohttp CookieJar
        self.login = login

        self._session: aiohttp.ClientSession

    async def start(self) -> str:
        logger.info("\n\nConnection start object id = %s \n\n", id(self))
        self._set_session()
        return await self._log_in()

    async def reconnect(self) -> None:
        logger.debug("Connection reconnect")
        await self._log_in()

    def _set_session(self) -> None:
        logger.debug("_set_session")
        self._session = aiohttp.ClientSession(headers=constants.HEADER)

    async def close(self) -> None:
        logger.critical("Connection close")
        await self._session.close()

    def _read_txt_cookie_file(self, file_path: Path) -> None:
        logger.debug("_read_txt_cookie_file %s", file_path)
        with file_path.open() as f:
            info = f.read()

        if info:
            self._cookies[("neverlands.ru", "/")] = SimpleCookie(info)

    def _read_binary_cookie_file(self, file_path: Path) -> None:
        logger.debug("_read_cookie_file %s", file_path)
        with file_path.open(mode="rb") as f:
            self._cookies = pickle.load(f)  # noqa: S301

    def _is_valid_cookies(self) -> bool:
        logger.debug("_is_valid_cookies")
        if not os.listdir(COOKIE_FOLDER):
            raise exception.NoCookiesFolderError

        dt = datetime.now(tz=UTC)
        dt_without_microseconds = dt.replace(microsecond=0)

        file_path = Path(self.cookies_txt_file_path)
        if file_path.exists():
            self._read_txt_cookie_file(file_path)

        if not self._cookies:
            binary_file_path = Path(self.cookies_binary_file_path)
            logger.debug("_is_valid_cookies False NO TEXT FILE %s", self.cookies_txt_file_path)
            if binary_file_path.exists():
                self._read_binary_cookie_file(binary_file_path)
            else:
                logger.debug("_is_valid_cookies False NO BINARY FILE %s", self.cookies_binary_file_path)
                return False

        if not self._cookies:
            logger.debug("_is_valid_cookies self._cookies NO COOKIES")
            return False

        user = self._cookies.get(("neverlands.ru", "/")).get("NeverNick").value  # type: ignore[union-attr]
        login = quote(self.login, encoding=constants.ENCODING)
        login = login.replace("~", "%7E")
        login = login.replace("%20", "+")

        if user != login:
            logger.critical("_is_valid_cookies False Cookie another person user-%s != login-%s", user, login)
            return False

        end_timestamp = self._cookies.get(("neverlands.ru", "/")).get("NeverExpi").value  # type: ignore[union-attr]
        if int(dt_without_microseconds.timestamp()) >= int(end_timestamp):
            logger.debug("_is_valid_cookies False int(dt_without_microseconds.timestamp()) >= int(end_timestamp)")
            logger.debug("%s", int(dt_without_microseconds.timestamp()) >= int(end_timestamp))
            logger.debug("%s %s", int(dt_without_microseconds.timestamp()), int(end_timestamp))
            return False

        logger.debug("_is_valid_cookies True")
        return True

    def _is_logged_in(self, result: str) -> bool:
        logger.debug("_is_logged_in")
        if connection.LOGIN_TEXT in result:
            logger.warning("NOT LOGGED cookies cleared")
            self._session.cookie_jar.clear()
            return False
        if connection.RELOGIN_TEXT in result:
            logger.warning("NEED RELOGIN cookies cleared")
            self._session.cookie_jar.clear()
            return False
        logger.debug("_is_logged_in true")
        return True

    def _save_cookies_to_file_txt(self) -> None:
        logger.debug("_save_cookies_to_file_txt")
        lines = []
        for cookie in self._session.cookie_jar:
            key = cookie.key
            value = cookie.value
            tine = f"{key}={value}"
            lines.append(tine)

        cookie = "; ".join(lines)  # type: ignore[assignment]
        logger.debug("cookie %s", cookie)
        with Path(self.cookies_txt_file_path).open("w") as f:
            f.write(cookie)  # type: ignore[arg-type]

    def _save_cookies(self) -> None:
        logger.debug("_save_cookies")
        self._session.cookie_jar.save(self.cookies_binary_file_path)  # type: ignore[attr-defined]
        self._save_cookies_to_file_txt()

    async def _get_login(self) -> str:
        logger.debug("_get_login")

        await self.get_html(urls.URL)

        logger.debug("try to login")
        auth_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        await self.post_html(urls.URL_GAME, data=self._data, auth_headers=auth_headers)  # type: ignore[arg-type]

        self._save_cookies()
        return await self.get_html(urls.URL_MAIN)

    async def _log_in(self) -> str:
        logger.debug("_log_in")
        if self._is_valid_cookies():
            self._session.cookie_jar.update_cookies(self._cookies.get(("neverlands.ru", "/")))  # type: ignore[arg-type]
            logger.debug("Valid cookies update_cookies")
            result = await self.get_html(urls.URL_MAIN)
        else:
            logger.debug("Log in NOT Valid cookies")
            result = await self._get_login()

        if not self._is_logged_in(result):
            result = await self._get_login()

        if not self._is_logged_in(result):
            result = await self._get_login()

        if not self._is_logged_in(result):
            logger.error(result)
            raise

        await self.get_html(urls.URL_SELL_INFO)

        self._session.cookie_jar.clear()
        if self._is_valid_cookies():
            self._session.cookie_jar.update_cookies(self._cookies.get(("neverlands.ru", "/")))  # type: ignore[arg-type]
            logger.debug("Updated cookies")

        self._save_cookies()
        return result

    def _write_all_debug_logs(  # noqa: PLR0913
        self,
        *,
        result,  # noqa: ANN001
        func_name: str,
        site_url: str,
        log_response: bool,
        params: dict | None = None,
        data: aiohttp.FormData | None = None,
    ) -> None:
        text = f"{self.login} {func_name} {site_url=} {params=} {data=} "
        if log_response and settings.DEBUG:
            text += f"\n{result=}"
        request_file_logger.debug(text)

    async def _write_error_logs(  # noqa: PLR0913
        self,
        *,
        answer,  # noqa: ANN001
        func_name: str,
        site_url: str,
        params: dict | None = None,
        data: aiohttp.FormData | None = None,
    ) -> None:
        result = await answer.text()
        text = f"{self.login} {func_name} {site_url=} \n{answer.status=} {params=} {data=} \n"

        response_text = f"{result}\n" if result else ""
        all_text = f"{text}\n{response_text}"
        request_file_logger.error(all_text)
        request_error_file_logger.error(all_text)

    @retry(
        wait=wait_incrementing(start=1, increment=1, max=3),
        stop=stop_after_attempt(3),
        reraise=True,
    )  # noqa: ERA001, RUF100
    async def get_html(self, site_url: str, *, params: dict | None = None, log_response: bool = False) -> str:
        func = inspect.currentframe()
        assert func

        answer = await self._session.get(
            site_url,
            params=params,
            timeout=aiohttp.ClientTimeout(total=5),
            **self.proxy_kwargs,  # type: ignore[arg-type]
        )

        match answer.status:
            case HTTPStatus.OK:
                result = await answer.text()
                self._write_all_debug_logs(
                    result=result,
                    func_name=func.f_code.co_name,
                    params=params,
                    site_url=site_url,
                    log_response=log_response,
                )
                return result

            case HTTPStatus.BAD_GATEWAY:
                await self._write_error_logs(
                    answer=answer,
                    func_name=func.f_code.co_name,
                    params=params,
                    site_url=site_url,
                )
                raise request.GetCode502Error

            case HTTPStatus.GATEWAY_TIMEOUT:
                await self._write_error_logs(
                    answer=answer,
                    func_name=func.f_code.co_name,
                    params=params,
                    site_url=site_url,
                )
                raise request.GetCode504Error

            case 546:
                await self._write_error_logs(
                    answer=answer,
                    func_name=func.f_code.co_name,
                    params=params,
                    site_url=site_url,
                )
                raise request.GetCode546Error

            case _:
                await self._write_error_logs(
                    answer=answer,
                    func_name=func.f_code.co_name,
                    params=params,
                    site_url=site_url,
                )
                raise request.GetNewCodeError

    @retry(
        wait=wait_incrementing(start=1, increment=1, max=3),
        stop=stop_after_attempt(3),
        reraise=True,
    )  # noqa: ERA001, RUF100
    async def post_html(  # noqa: PLR0913
        self,
        site_url: str,
        *,
        data: aiohttp.FormData | None = None,
        params: dict | None = None,
        log_response: bool = False,
        auth_headers: dict[str, str] | None = None,
    ) -> str:
        func = inspect.currentframe()
        assert func

        answer = await self._session.post(
            site_url,
            params=params,
            data=data,
            headers=auth_headers or {"Content-Type": "application/x-www-form-urlencoded"},
            timeout=aiohttp.ClientTimeout(total=5),
            **self.proxy_kwargs,
        )

        match answer.status:
            case HTTPStatus.OK:
                result = await answer.text()
                self._write_all_debug_logs(
                    result=result,
                    func_name=func.f_code.co_name,
                    data=data,
                    params=params,
                    site_url=site_url,
                    log_response=log_response,
                )
                return result

            case HTTPStatus.BAD_GATEWAY:
                await self._write_error_logs(
                    answer=answer,
                    params=params,
                    func_name=func.f_code.co_name,
                    data=data,
                    site_url=site_url,
                )
                raise request.PostCode502Error

            case _:
                await self._write_error_logs(
                    answer=answer,
                    params=params,
                    func_name=func.f_code.co_name,
                    data=data,
                    site_url=site_url,
                )
                raise request.PostNewCodeError
