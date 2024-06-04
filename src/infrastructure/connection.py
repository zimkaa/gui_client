import os

from src.config import logger
from src.config import settings
from src.infrastructure.errors.exception import WrongIPError
from src.infrastructure.request import Connection
from src.infrastructure.request import my_ip


async def connect() -> Connection:
    if settings.connection.PROXY:
        logger.debug("Proxy on")
        login = settings.connection.PROXY_LOG
        password = settings.connection.PROXY_PASS
        port = settings.connection.PROXY_PORT
        ip = settings.connection.PROXY_IP
        protocol_http = "http"
        proxy_url_http = f"{protocol_http}://{login}:{password}@{ip}:{port}"
        real_ip = await my_ip(use_proxy=True)
        os.environ.setdefault("HTTP_PROXY", proxy_url_http)

        # protocol_https = "https"  # noqa: ERA001
        # proxy_url_https = f"{protocol_https}://{login}:{password}@{ip}:{port}"  # noqa: ERA001
        # os.environ.setdefault("HTTPS_PROXY", proxy_url_https)  # noqa: ERA001
    else:
        logger.debug("Proxy off")
        real_ip = await my_ip(use_proxy=False)

    logger.debug("real_ip=%s settings=%s", real_ip, settings)
    if settings.connection.PROXY_IP in real_ip:
        text = f"\n-------ip------- {real_ip} LOGIN {settings.person.LOGIN}" * 5
        logger.info(text)
    else:
        text = f"{settings.person.LOGIN} {settings.connection.PROXY_IP=} not in real IP={real_ip}"
        logger.error(text)
        msg = "Wrong IP or proxy not work"
        raise WrongIPError(msg)

    try:
        text = f"{settings.connection.PROXY=}"
        logger.debug(text)
        connection = Connection(
            proxy=settings.connection.PROXY,
            login=settings.person.LOGIN,
            password=settings.person.PASSWORD,
        )
        logger.debug("connect connection id = %s", id(connection))
        await connection.start()
    except Exception as err:
        logger.error("err=%s", err)
        raise
    return connection
