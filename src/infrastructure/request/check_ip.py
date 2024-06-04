from __future__ import annotations
import random
from http import HTTPStatus

import aiohttp

from src.config import settings
from src.config.game import constants
from src.config.game import ip
from src.infrastructure.errors import request


async def my_ip(*, use_proxy: bool) -> str:
    random_site = random.choice(list(ip.CheckIPSite))  # noqa: S311

    proxy_dict = {}
    if use_proxy:
        proxy_auth = aiohttp.BasicAuth(settings.connection.PROXY_LOG, settings.connection.PROXY_PASS)
        proxy_url = f"http://{settings.connection.PROXY_IP}:{settings.connection.PROXY_PORT}"
        proxy_dict = {"proxy": proxy_url, "proxy_auth": proxy_auth}

    async with aiohttp.ClientSession(headers=constants.HEADER) as session:  # noqa: SIM117
        # async with session.get(random_site, proxy=proxy_url, proxy_auth=proxy_auth) as answer:
        async with session.get(random_site, **proxy_dict) as answer:  # type: ignore[arg-type]
            text = await answer.text()

    if answer.status != HTTPStatus.OK:
        text = "PROXY DON'T RESPONSE!!!"
        raise request.ProxyError(text)
    return text
