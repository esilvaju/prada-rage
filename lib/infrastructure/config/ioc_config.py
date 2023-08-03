import logging.config
from dependency_injector import containers, providers

from lib.infrastructure.gateway.google_search import GoogleSearchEngine

class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.yaml"
    )

    # Gateways:
    google_search_gateway = providers.Factory(
        GoogleSearchEngine,
    )
    
