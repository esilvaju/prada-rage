import os
import pytest
import lib
from lib.infrastructure.config.containers import Container

container = Container()
print(container.config())
container.wire(modules=[lib])

# set autouse=True to automatically inject the container into all tests
@pytest.fixture(scope="session")
def app_container() -> Container:
    return container


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "tests", "docker-compose.yml")

# set autouse=True to automatically inject the postgres into all tests
@pytest.fixture(scope="session")
def postgres_container(app_container: Container, docker_services) -> None:
    """ Ensure that a postgres container is running before running tests """
    def is_responsive() -> bool:
        try:
            db = app_container.db()
            return db.ping()
        except Exception as e:
            return False
        
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive()
    )

    
    return app_container.db()