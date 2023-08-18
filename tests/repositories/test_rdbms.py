import docker

def test_pg_container_is_available(postgres_container):
    client = docker.from_env()
    containers = client.containers.list()
    assert len(containers) != 0
    image_names = [container.image.tags[0] for container in containers]
    assert "postgres:latest" in image_names
