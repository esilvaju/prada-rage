from lib.infrastructure.config.containers import Container


def test_scrape_docs(app_container: Container):
    website_scaper_gateway = app_container.website_scraper_gateway()
    assert website_scaper_gateway is not None
    # text = website_scaper_gateway.extract_text_from_html(url="https://python-dependency-injector.ets-labs.org/tutorials/asyncio-daemon.html")
    # print(text)