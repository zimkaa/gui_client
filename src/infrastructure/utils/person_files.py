from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

import aiohttp
from lxml import etree

from src.config import logger
from src.domain.value_object.classes import PersonType
from src.infrastructure.errors.helpers import NoFolderError
from src.use_cases.request.base import Proxy


@dataclass
class UserInfo:
    login: str
    password: str
    type_: PersonType
    ip: str
    proxy_data: Proxy | None = None


def _get_person_login_info(file_name: Path) -> UserInfo:
    tree = etree.parse(file_name)  # noqa: S320
    root = tree.getroot()

    user = root.find("user").attrib

    proxy = root.find("proxy").attrib
    ip, port = proxy["address"].split(":")
    user_proxy_url = f"http://{ip}:{port}"
    user_proxy_data = Proxy(proxy=user_proxy_url, proxy_auth=aiohttp.BasicAuth(proxy["username"], proxy["password"]))

    groups = root.find("LezBotsGroups")
    mmm = [element.attrib["DoMagHits"].capitalize() == "True" for element in groups]
    mag = any(mmm)
    mag_or_warrior = PersonType.MAG if mag else PersonType.WARRIOR

    return UserInfo(
        login=user["name"],
        password=user["password"],
        ip=ip,
        proxy_data=user_proxy_data,
        type_=mag_or_warrior,
    )


def _get_all_files_from_folder(folder: str = "./INFO/persons") -> list[Path]:
    folder_path = Path(folder)
    if not folder_path.exists():
        msg = f"Folder {folder} not found"
        raise NoFolderError(msg)

    return [file for file in folder_path.glob("*.profile") if file.is_file()]


def get_all_persons() -> list[UserInfo]:
    files = _get_all_files_from_folder()
    users_info = [_get_person_login_info(file) for file in files]
    text = f"{users_info=}"
    logger.info(text)
    return users_info


def get_persons_name(users: list[UserInfo]) -> list[str]:
    return [user.login for user in users]
