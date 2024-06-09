from __future__ import annotations
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import aiohttp


@dataclass
class Proxy:
    proxy: str | None = None
    proxy_auth: aiohttp.BasicAuth | None = None


class BaseConnection(ABC):
    @abstractmethod
    async def start(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def reconnect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_html(self, site_url: str, *, params: dict | None = None, log_response: bool = False) -> str:
        raise NotImplementedError

    @abstractmethod
    async def post_html(
        self,
        site_url: str,
        *,
        data: aiohttp.FormData | None = None,
        log_response: bool = False,
        auth_headers: dict | None = None,
    ) -> str:
        raise NotImplementedError
