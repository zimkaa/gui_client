from pathlib import Path

import tomli


def get_name() -> str:
    with Path("pyproject.toml").open("rb") as f:
        data = tomli.load(f)
    return data["tool"]["poetry"]["name"]


def get_version() -> str:
    with Path("pyproject.toml").open("rb") as f:
        data = tomli.load(f)
    return data["tool"]["poetry"]["version"]
