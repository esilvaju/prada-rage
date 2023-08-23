from abc import ABC, abstractmethod
from lib.core.ports.secondary.search_engine_output_port import SearchEngineOutputPort
from lib.core.ports.secondary.website_scraper_output_port import (
    WebsiteScraperOutputPort,
)
from lib.core.usecase_models.research_usecase_models import ResearchRequest


class ResearchInputPort(ABC):
    def __init__(
        self,
        presenter,
        search_engine_gateway: SearchEngineOutputPort,
        website_scraper_gateway: WebsiteScraperOutputPort,
    ):
        self.presenter = presenter
        self.search_engine_gateway = search_engine_gateway
        self.website_scraper_gateway = website_scraper_gateway

    @abstractmethod
    def execute(self, request_model: ResearchRequest):
        pass


class ResearchOutputPort(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def present_success(self, response_model):
        pass

    @abstractmethod
    def present_error(self, error_model):
        pass
