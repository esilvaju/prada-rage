from dependency_injector.wiring import inject, Provide
import pytest

from lib.infrastructure.config.ioc_config import Container


@pytest.fixture(scope="session")
def container() -> Container:
    appContainer = Container()
    appContainer.wire(modules=[
        "lib.infrastructure.gateway.env_gateway"
    ])