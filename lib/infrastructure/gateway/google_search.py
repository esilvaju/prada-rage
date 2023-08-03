from googlesearch import search
from lib.core.ports.secondary.search_engine_output_port import SearchEngineOutputPort


class GoogleSearchEngine(SearchEngineOutputPort):
    def __init__(self):
        pass

    def get_links(self, query: str, num: int, lang: str = "en") -> list[dict]:
        results = search(query, num_results=num, lang=lang)
        return results