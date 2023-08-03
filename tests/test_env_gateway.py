
from lib.infrastructure.config.ioc_config import Container


def test_env_gateway(app_container: Container):
    google_search_gateway = app_container.google_search_gateway()
    assert google_search_gateway is not None
    results = google_search_gateway.get_links(query="is openheimer worth watching", num=10)
    for result in results:
        print(result)
