from __future__ import annotations
from abc import ABC
from abc import abstractmethod


class BaseConnection(ABC):
    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def reconnect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_html(self, site_url: str, *, data: dict | None = None, log_response: bool = False) -> str:
        raise NotImplementedError

    @abstractmethod
    async def post_html(
        self,
        site_url: str,
        *,
        data: dict | None = None,
        log_response: bool = False,
        auth: bool = False,
    ) -> str:
        raise NotImplementedError
