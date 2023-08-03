from lib.core.ports.secondary.search_engine_output_port import SearchEngineOutputPort


class GoogleSearchEngine(SearchEngineOutputPort):
    def __init__(self):
        pass

    def get_links(self, query: str, num: int) -> list[str]:
        raise NotImplementedError("Should have implemented this")