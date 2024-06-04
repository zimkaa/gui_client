from __future__ import annotations
import asyncio
import time
from http import HTTPStatus

import aiohttp

from src.config import logger
from src.config import settings
from src.config.game import constants


TG_SEND_REQUEST = f"https://api.telegram.org/bot{settings.message.TG_TOKEN}/sendMessage"


def create_tg_id_list() -> list[int]:
    tg_id_list = []
    if settings.message.CHANNEL_ID:
        tg_id_list.append(int(settings.message.CHANNEL_ID))
    if settings.message.CHANNEL_ID_WATCHER and settings.message.CHANNEL_ID_WATCHER not in tg_id_list:
        tg_id_list.append(int(settings.message.CHANNEL_ID_WATCHER))
    return tg_id_list


async def tg_post_request(session: aiohttp.ClientSession, text: str, chat_id: str) -> None:
    logger.debug("tg_post_request start at = %s", time.perf_counter())
    data = {
        "chat_id": chat_id,
        "text": text,
    }
    async with session.get(TG_SEND_REQUEST, data=data) as answer:
        pass
    logger.debug("chat_id = %s", chat_id)
    if answer.status != HTTPStatus.OK:
        logger.warning("Some trouble with TG")


async def send_to_telegram(text: str) -> None:
    id_list = create_tg_id_list()
    logger.debug("Send to telegram %s", id_list)
    async with aiohttp.ClientSession(headers=constants.HEADER) as session:
        tasks = [tg_post_request(session, text, str(chanel_id)) for chanel_id in id_list]
        # for chanel_id in id_list:
        #     tasks.append(tg_post_request(session, text, str(chanel_id)))  # noqa: ERA001

        await asyncio.gather(*tasks)
