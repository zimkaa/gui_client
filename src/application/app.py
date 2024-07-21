import flet as ft

from src.application.deps import MainContainer
from src.config import logger
from src.infrastructure.flet_comp.root import RootElement


def run_app() -> None:
    logger.info("Starting app.")
    MainContainer()
    main = RootElement()

    try:
        ft.app(port=8580, view=ft.AppView.WEB_BROWSER, target=main.mass_start)
        # ft.app(port=8580, view=ft.AppView.WEB_BROWSER, target=main.start)  # noqa: ERA001
    finally:
        logger.info("App stopped.")
