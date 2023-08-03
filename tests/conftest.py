import pytest
import lib
from lib.infrastructure.config.containers import Container


container = Container()
container.wire(modules=[lib])

@pytest.fixture(scope="session")
def app_container() -> Container:
    return container
