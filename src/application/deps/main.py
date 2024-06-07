from dependency_injector import containers
from dependency_injector import providers

from src.infrastructure.connection import connection_factory
from src.infrastructure.request.nl import BaseConnection


class MainContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src",
        ],
    )

    connection: providers.Factory[BaseConnection] = providers.Factory(connection_factory)  # type: ignore[arg-type]
