from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pydantic import BaseModel
from pydantic import Field


if TYPE_CHECKING:
    from src.infrastructure.request import Connection


@dataclass
class StopOrHit:
    html: Connection
    stop: bool


@dataclass
class EndBattleProp:
    fexp: str
    fres: str
    vcode: str
    ftype: str
    min1: str
    max1: str
    min2: str
    max2: str
    sum1: str
    sum2: str


@dataclass
class EndBattle(EndBattleProp):
    get_id: str = "61"
    act: str = "7"


@dataclass
class DataForFight:
    fight_ty: list[str | int | float]
    param_ow: list[str | int | float]
    lives_g1: list[str | int | float]
    lives_g2: list[str | int | float]
    alchemy: list[str | int | float]
    magic_in: list[str | int | float]
    param_en: list[str | int | float]
    fight_pm: list[str | int | float]


@dataclass
class Post:
    post_id: str
    pnick: str
    agree: str
    vcode: str
    wuid: str
    wsubid: str
    wsolid: str


# # TODO: do class  # noqa: TD002, TD003, FIX002
# @dataclass
# class Enemy:
#     bot_name: str  # noqa: ERA001
#     bot_hp: Decimal = attr.ib(converter=Decimal)  # noqa: ERA001
#     bot_max_hp: Decimal = attr.ib(converter=Decimal)  # noqa: ERA001
#     bot_mp: Decimal = attr.ib(converter=Decimal)  # noqa: ERA001
#     bot_max_mp: Decimal = attr.ib(converter=Decimal)  # noqa: ERA001
#     bot_level: Decimal = attr.ib(converter=Decimal)  # noqa: ERA001


@dataclass
class Hit:
    inu: str
    inb: str
    ina: str


@dataclass
class QueryHit(Hit):
    vcode: str
    enemy: str
    group: str
    inf_bot: str
    inf_zb: str
    lev_bot: str
    ftr: str
    post_id: str = "7"


class FightConfig(BaseModel):
    HP: bool = Field(default=True, title="Use HP", alias="hp")
    NEED_HP_PERCENT: float = Field(
        default=1.0,
        title="HP coefficient to restore",
        alias="needHpPercent",
        ge=0.0,
        le=1.0,
    )

    MP: bool = Field(default=True, title="Use MP", alias="mp")
    NEED_MP_PERCENT: float = Field(
        default=0.4,
        title="MP coefficient to restore",
        alias="needMpPercent",
        ge=0.0,
        le=1.0,
    )
    MP_NEED_INSIDE_BATTLE: int = Field(
        default=500,
        title="Try to restore at least this amount of mana",
        alias="mpNeedInsideBattle",
        ge=0,
        le=29970,
    )  # used to get need_mp
    NEED_MP_COUNT: int = Field(
        default=500,
        title="Restore MP when least or equal this amount",
        alias="needMpCount",
        ge=0,
        le=29970,
    )

    SCROLL: bool = Field(default=False, title="Use scroll like (The Rage Strike Scroll)", alias="scroll")
    KICK: bool = Field(default=False, title="Use buffs like (Bounty of Lightning)", alias="kick")
    KICK_COUNT: int = Field(default=1, title="Count buffs per step", alias="kickCount", ge=0, le=5)

    SUPER_HIT: bool = Field(default=True, title="Use super hit", alias="superHit")
    STABLE_HIT: bool = Field(default=True, title="Use physical hit", alias="stableHit")

    STABLE_MAGIC_HIT: bool = Field(default=True, title="Use magical hit", alias="stableMagicHits")
    MP_HIT: int = Field(default=5, title="MP per hit", alias="mpHit", ge=5, le=500)
    MIN_MP_COEFFICIENT: float = Field(
        default=0.01,
        title="Coefficient when stop used magic stable hits",
        alias="minMpCoefficient",
        ge=0.0,
        le=1.0,
    )  # used for magic hits


class StableHit(BaseModel):
    name: list[str]
    code: list[int]
    mp_cost: list[int]
    od: list[int]
    priority: list[int]
