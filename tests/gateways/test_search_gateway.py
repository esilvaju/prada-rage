
from lib.infrastructure.config.containers import Container


def test_google_search_gateway(app_container: Container):
    google_search_gateway = app_container.google_search_gateway()
    assert google_search_gateway is not None
    results = google_search_gateway.get_links(query="best sex positions for south american super horny couple", num=15, lang="en")
    for result in results:
        print(result)
