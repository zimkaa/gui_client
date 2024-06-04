from dependency_injector import containers
from dependency_injector import providers

from src.infrastructure.connection import connect
from src.infrastructure.request.nl import BaseConnection


class MainContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src",
        ],
    )

    connection: providers.Singleton[BaseConnection] = providers.Singleton(connect)  # type: ignore[arg-type]
