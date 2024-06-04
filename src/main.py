import flet as ft
import sentry_sdk

from src.application.app import app
from src.config import settings


sentry_sdk.init(
    dsn=settings.SENTRY,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


def main() -> None:
    ft.app(target=app)
