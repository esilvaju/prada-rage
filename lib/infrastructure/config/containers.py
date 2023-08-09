import logging.config
from pathlib import Path
import sys
from dependency_injector import containers, providers
from chromadb.config import Settings

from lib.core.entity.devices import DeviceType

from lib.core.ports.secondary.website_scraper_output_port import WebsiteScraperOutputPort
from lib.core.service.localgpt_embedding_service import LocalGPTEmbeddingService

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

    # Domain Services:
    device_type: DeviceType = DeviceType(config.embedding_service.device_type.toUpper())
    
    chrome_settings = Settings(
        chroma_db_impl=config.db.chrome_db_impl,
        persist_directory=config.db.persist_dir,
    )

    localgpt_embedding_service = providers.Factory(
        LocalGPTEmbeddingService,
        device_type=config.embedding_service.device_type,
        embedding_model_name=config.embedding_service.embedding_model_name,
        docs_dir = Path(config.files.root_directory) / Path(config.files.source_docs_directory),
        chunk_size=config.embedding_service.chunk_size,
        chunk_overlap=config.embedding_service.chunk_overlap,
        db_directory=Path(config.files.root_directory) / Path(config.db.persist_dir),
        chroma_settings=chrome_settings
    )

    