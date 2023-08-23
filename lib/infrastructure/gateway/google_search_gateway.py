from typing import Any
from googlesearch import search
from lib.core.ports.secondary.search_engine_output_port import SearchEngineOutputPort


class GoogleSearchGateway(SearchEngineOutputPort):
    def __init__(self):
        pass

    def get_links(self, query: str, num: int, lang: str = "en") -> Any:
        results = search(query, num_results=num, lang=lang)
        return results
