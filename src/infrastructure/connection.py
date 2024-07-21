from __future__ import annotations
from dataclasses import dataclass

import aiohttp

from src.config import logger
from src.infrastructure.errors.exception import WrongIPError
from src.infrastructure.request import Connection
from src.infrastructure.request import my_ip
from src.use_cases.request.base import Proxy


@dataclass
class ProxyInfo:
    active: bool
    login: str
    password: str
    port: str
    ip: str


@dataclass
class PersonWithConnectionData:
    login: str
    password: str
    proxy: ProxyInfo


def prepare_proxy_data(proxy: ProxyInfo) -> Proxy:
    protocol_http = "http"
    proxy_url = f"{protocol_http}://{proxy.ip}:{proxy.port}"
    return Proxy(proxy=proxy_url, proxy_auth=aiohttp.BasicAuth(proxy.login, proxy.password))


async def connection_factory(person: PersonWithConnectionData) -> Connection:
    if person.proxy.active:
        proxy_data = prepare_proxy_data(person.proxy)
        real_ip = await my_ip(user_proxy=proxy_data)
    else:
        real_ip = await my_ip(user_proxy=None)

    logger.debug("real_ip=%s person.proxy.ip=%s", real_ip, person.proxy.ip)
    if person.proxy.ip in real_ip:
        text = f"\n-------ip------- {real_ip} LOGIN {person.login}" * 5
        logger.info(text)
    else:
        text = f"{person.login} {person.proxy.ip=} not in real IP={real_ip}"
        logger.error(text)
        msg = "Wrong IP or proxy not work"
        raise WrongIPError(msg)

    try:
        text = f"{person.proxy.active=}"
        logger.debug(text)
        connection = Connection(
            proxy_data=proxy_data,
            login=person.login,
            password=person.password,
        )
        logger.debug("connect connection id = %s", id(connection))
        await connection.start()
    except Exception as err:
        text = f"{connection.login} {err=}"
        logger.error("err=%s", err)
        raise
    return connection
