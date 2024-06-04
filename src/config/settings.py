from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from .project_info import get_name
from .project_info import get_version


app_version = get_version()
app_name = get_name()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow", env_file=".env", env_file_encoding="utf-8")

    DEBUG: bool = Field(default=False)
    LOGGER_LEVEL: str = Field(default="")
    LOGGER_CONFIG_FILE: str = Field(default="config.yaml")

    APP_VERSION: str = Field(default=app_version)
    APP_NAME: str = Field(default=app_name)


settings = Settings()
