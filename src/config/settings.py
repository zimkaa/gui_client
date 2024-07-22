from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from src.config.game import persons
from src.config.project_info import get_name
from src.config.project_info import get_version
from src.domain.value_object.classes import PersonRole
from src.domain.value_object.classes import PersonType


app_version = get_version()
app_name = get_name()


class ConnectionSettings(BaseModel):
    PROXY: bool = Field(default=False)  # without proxy
    PROXY_IP: str = Field(default="empty")  # without proxy
    LOCAL_IP: str = Field(default="empty")
    SERVER_IP: str = Field(default="empty")

    PROXY_LOG: str = Field(default="empty")
    PROXY_PASS: str = Field(default="empty")
    PROXY_PORT: str = Field(default="empty")


class SendMessageSettings(BaseModel):
    CHANNEL_ID: str = Field(default="")
    CHANNEL_ID_ROMANSON: str = Field(default="")
    CHANNEL_ID_HUNTER: str = Field(default="")
    CHANNEL_ID_TURNOFF: str = Field(default="")
    CHANNEL_ID_ANGEL: str = Field(default="")
    CHANNEL_ID_ABYSS: str = Field(default="")
    CHANNEL_ID_LEGALAS: str = Field(default="")
    CHANNEL_ID_WATCHER: str = Field(default="")  # TODO: later compute it  # noqa: TD002, TD003, FIX002
    TG_TOKEN: str = Field(default="")


class DungeonSettings(BaseModel):
    AUTO_BUFF: bool = Field(default=True)
    PERSON_ROLE: PersonRole = Field(default=PersonRole.SLAVE)
    DUNGEON_WATCHER: persons.PersonsNick = Field(default=persons.PersonsNick.ROMANSON)
    LEADER_TYPE: PersonType = Field(default=PersonType.WARRIOR)
    LEADER_NAME: persons.PersonsNick = Field(default=persons.PersonsNick.HUNTER)
    MAG_KILLER: bool = Field(default=True)
    PERSON_TYPE: PersonType = Field(default=PersonType.MAG)
    PARTY_MEMBERS: list[persons.PersonsNick] = Field(
        default=[
            persons.PersonsNick.TURNOFF,
            persons.PersonsNick.HUNTER,
        ],
    )
    LEN_PARTY: int = Field(
        default=1,
        ge=1,
        le=2,
    )  # TODO: delete from settings it must be count of PARTY_MEMBERS  # noqa: TD002, TD003, FIX002
    MAG_DAMAGER: persons.PersonsNick = Field(default=persons.PersonsNick.TURNOFF)
    DEAD_PLAGUE_ZOMBIE: str = Field(default="0/125")


class PersonSettings(BaseModel):
    LOGIN: str = Field(default="None")
    PASSWORD: str = Field(default="None")
    FLASH: str = Field(default="")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
    )

    DEBUG: bool = Field(default=False)
    LOGGER_LEVEL: str = Field(default="")
    LOGGER_CONFIG_FILE: str = Field(default="config.yaml")

    APP_VERSION: str = Field(default=app_version)
    APP_NAME: str = Field(default=app_name)

    SENTRY: str = Field(default="")

    SIEGE: bool = Field(default=False)
    dungeon: DungeonSettings = DungeonSettings()
    FIGHT_ITERATIONS: int = Field(default=5)
    SLEEP_TIME: float = Field(default=5)
    SLEEP_TIME_PER_HIT: float = Field(default=0.5)
    FIGHT_TEST_MODE: bool = Field(default=False)
    AB: bool = Field(default=True)
    connection: ConnectionSettings = ConnectionSettings()
    CITY: str = Field(default="2")
    TELEPORT_CITY: int = Field(default=2)  # OKTAL
    SIEGE_DRESS: str = Field(default="Маг")  # noqa: RUF001
    HOME_DIR: str = Field(default=".\\files")
    FLOOR: str = Field(default="99")
    message: SendMessageSettings = SendMessageSettings()
    person: PersonSettings = PersonSettings()

    test: PersonSettings = PersonSettings()


settings = Settings()


CHANNEL_ID_DICT: dict[str, str] = {
    persons.PersonsNick.ROMANSON: settings.message.CHANNEL_ID_ROMANSON,
    persons.PersonsNick.HUNTER: settings.message.CHANNEL_ID_HUNTER,
    persons.PersonsNick.TURNOFF: settings.message.CHANNEL_ID_TURNOFF,
    persons.PersonsNick.ANGEL: settings.message.CHANNEL_ID_ANGEL,
    persons.PersonsNick.ABYSS: settings.message.CHANNEL_ID_ABYSS,
    persons.PersonsNick.LEGALAS: settings.message.CHANNEL_ID_LEGALAS,
}

settings.dungeon.LEN_PARTY = len(settings.dungeon.PARTY_MEMBERS)
