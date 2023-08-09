import pytest
import lib
from dependency_injector import providers
from lib.infrastructure.config.containers import Container


container = Container()
container.config = providers.Configuration(yaml_files=["config.yml"])
container.wire(modules=[lib])

@pytest.fixture(scope="session")
def app_container() -> Container:
    return container
