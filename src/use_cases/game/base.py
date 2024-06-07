from abc import ABC
from abc import abstractmethod
from typing import Any


class BaseGame(ABC):
    @abstractmethod
    async def start(self, page: Any) -> None:  # noqa: ANN401
        raise NotImplementedError
