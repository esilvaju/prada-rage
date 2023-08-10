import pytest
import lib
from dependency_injector import providers
from lib.infrastructure.config.containers import Container
from pathlib import Path

container = Container()
print(container.config())
container.wire(modules=[lib])
@pytest.fixture(scope="session")
def app_container() -> Container:
    return container
