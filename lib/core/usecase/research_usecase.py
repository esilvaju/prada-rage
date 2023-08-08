from lib.core.ports.primary.research_ports import ResearchInputPort
from lib.core.ports.secondary.search_engine_output_port import SearchEngineOutputPort
from lib.core.ports.secondary.website_scraper_output_port import WebsiteScraperOutputPort


class ResearchUsecase(ResearchInputPort):
    def __init__(self, presenter, search_engine_gateway: SearchEngineOutputPort, website_scraper_gateway: WebsiteScraperOutputPort):
        super().__init__(presenter, search_engine_gateway, website_scraper_gateway)

    def execute(self, request_model):
        pass