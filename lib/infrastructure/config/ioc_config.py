import logging.config
import sys
from dependency_injector import containers, providers
from lib.core.ports.secondary.website_scraper_output_port import WebsiteScraperOutputPort

from lib.infrastructure.gateway.google_search_gateway import GoogleSearchGateway
from lib.infrastructure.gateway.website_scraper_gateway import WebsiteScraperGateway

class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    logging = providers.Resource(
        logging.basicConfig,
        stream=sys.stdout,
        level=config.log.level,
        format=config.log.format,
    )

    # Gateways:
    google_search_gateway = providers.Factory(
        GoogleSearchGateway,
    )
    
    website_scraper_gateway = providers.Factory(
        WebsiteScraperGateway,
    )

    