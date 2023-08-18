import os
import pytest
import lib
from lib.infrastructure.config.containers import Container
from alembic.config import Config
from alembic import command

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
def with_rdbms(app_container: Container, docker_services) -> None:
    """ Ensure that a postgres container is running before running tests """
    def is_responsive() -> bool:
        try:
            db = app_container.db()
            return db.ping()
        except Exception as e:
            return False
        
    try:
        docker_services.wait_until_responsive(
            timeout=30.0, pause=0.1, check=lambda: is_responsive()
        )
    except Exception as e:
        pytest.fail(f"Failed to start postgres container, error: {e}")

    
    return app_container.db()

@pytest.fixture(scope="session")
def with_rdbms_migrations(request, with_rdbms) -> None:
    """ Run alembic migrations before running tests and tear them down after """
    alembic_ini_path = os.path.join(str(request.config.rootdir), "alembic.ini")
    alembic_cfg = Config(alembic_ini_path)

    alembic_scripts_path = os.path.join(str(request.config.rootdir), "alembic")
    alembic_cfg.set_main_option("script_location", alembic_scripts_path)

    alembic_cfg.set_main_option("sqlalchemy.url", container.db().url)
    
    try:
        command.upgrade(alembic_cfg, "head")
    except Exception as e:
        pytest.fail("Failed to run migrations, error: {e}")
    request.addfinalizer(lambda: command.downgrade(alembic_cfg, "base"))
