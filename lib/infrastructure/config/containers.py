import logging.config
from pathlib import Path
import sys
from dependency_injector import containers, providers
from chromadb.config import Settings

from lib.core.entity.devices import DeviceType

from lib.core.service.localgpt_embedding_service import LocalGPTEmbeddingService

from lib.infrastructure.gateway.google_search_gateway import GoogleSearchGateway
from lib.infrastructure.gateway.website_scraper_gateway import WebsiteScraperGateway

class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["./config.yaml"])

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
    
    localgpt_embedding_service = providers.Factory(
        LocalGPTEmbeddingService,
        device_type=config.embedding_service.device_type,
        embedding_model_name=config.embedding_service.embedding_model_name,
        root_dir=config.files.root_directory.as_(Path),
        docs_dir = config.files.source_docs_directory.as_(Path),
        db_directory = config.db.persist_dir.as_(Path),
        chunk_size=config.embedding_service.chunk_size.as_int(),
        chunk_overlap=config.embedding_service.chunk_overlap.as_int(),
        chroma_db_impl=config.db.chroma_db_impl,
    )

    