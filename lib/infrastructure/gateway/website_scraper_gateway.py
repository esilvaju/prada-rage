from bs4 import BeautifulSoup
import requests

from lib.core.ports.secondary.website_scraper_output_port import WebsiteScraperOutputPort


class WebsiteScraperGateway(WebsiteScraperOutputPort):
    def __init__(self):
        super().__init__()

    def extract_text_from_html(self, url: str) -> str:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        # text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
