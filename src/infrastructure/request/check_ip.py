from __future__ import annotations
import random
from http import HTTPStatus

import aiohttp

from src.config import logger
from src.config.game import constants
from src.config.game import ip
from src.infrastructure.errors import request
from src.use_cases.request.base import Proxy


async def my_ip(*, user_proxy: Proxy | None = None) -> str:
    random_site = random.choice(list(ip.CheckIPSite))  # noqa: S311

    if not user_proxy:
        user_proxy = Proxy(proxy=None, proxy_auth=None)
    logger.debug("user_proxy=%s", user_proxy)
    async with aiohttp.ClientSession(headers=constants.HEADER) as session:  # noqa: SIM117
        async with session.get(random_site, proxy=user_proxy.proxy, proxy_auth=user_proxy.proxy_auth) as answer:
            text = await answer.text()

    if answer.status != HTTPStatus.OK:
        logger.error("PROXY DON'T RESPONSE!!!")
        logger.error("answer.status=%s", answer.status)
        logger.error("text=%s", text)
        text = "PROXY DON'T RESPONSE!!!"
        raise request.ProxyError(text)

    logger.info("my_ip = %s", text)
    return text
