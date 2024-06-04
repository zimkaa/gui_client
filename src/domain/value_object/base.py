from __future__ import annotations
from dataclasses import dataclass


@dataclass
class BotFightData:
    link: str
    nick: str
    level: str


@dataclass
class HumanFightData:
    link: str
    level: str
    nick: str
    g1: list[str]
    g2: list[str]


@dataclass
class FreeFightData:
    level: str
    nick: str


@dataclass
class FightData:
    bot: list[BotFightData]
    human: list[HumanFightData]
    free: list[FreeFightData]


@dataclass
class PersonInfo:
    nick: str
    level: str
    fight_link: str | None = None


@dataclass
class MessageData:
    fight: str
    bot: str
    free: str


class OutPutInfo:
    def __init__(self) -> None:
        self.text = b""

    def __repr__(self) -> bytes:  # type: ignore[override]
        return self.text

    def update_info(self, text: bytes) -> None:
        self.text = text
