class SearchEngineOutputPort:
    def __init__(self):
        pass

    def get_links(self, query: str, num: int) -> list[str]:
        raise NotImplementedError("Should have implemented this")
