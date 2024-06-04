import logging.config
from pathlib import Path
from typing import Final

import yaml

from .settings import settings


LOGGER_FOLDER_NAME: Final[str] = "logger"
LOGGER_CONFIG_FOLDER_NAME: Final[str] = "logging_config"

ROOT_PATH_LOGGER_FOLDER = Path(LOGGER_FOLDER_NAME)
PATH_LOGGER_FOLDER = ROOT_PATH_LOGGER_FOLDER / LOGGER_CONFIG_FOLDER_NAME

logger = logging.getLogger(settings.APP_NAME)


def setup_logging(config_file: str) -> None:
    config_file = PATH_LOGGER_FOLDER / config_file  # type: ignore[assignment]
    with Path(config_file).open() as f_in:
        config = yaml.safe_load(f_in)

    logging.config.dictConfig(config)


debug_level = "DEBUG" if settings.DEBUG else "INFO"
logger_level = settings.LOGGER_LEVEL if settings.LOGGER_LEVEL else debug_level
logger.setLevel(logger_level)
setup_logging(settings.LOGGER_CONFIG_FILE)
