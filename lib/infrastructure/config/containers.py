import logging.config
from pathlib import Path
import sys
from dependency_injector import containers, providers
from chromadb.config import Settings

from lib.infrastructure.config.devices import DeviceType

from lib.infrastructure.gateway.google_search_gateway import GoogleSearchGateway
from lib.infrastructure.gateway.localgpt.localgpt_embedding_service import LocalGPTEmbeddingService
from lib.infrastructure.gateway.localgpt.localgpt_inference_service import LocalGPTInferenceQueryService
from lib.infrastructure.gateway.website_scraper_gateway import WebsiteScraperGateway
from lib.infrastructure.gateway.localgpt.localgpt_inference_service import supported_models
from lib.infrastructure.repository.sqla.database import Database
# from lib.infrastructure.repository.sqla.sqla_research_topic_repository import SQLAResearchTopicRepository

class Container(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["./config.yaml"])

    logging = providers.Resource(
        logging.basicConfig,
        stream=sys.stdout,
        level=config.log.level,
        format=config.log.format,
    )

    db = providers.Singleton(
        Database,
        db_host=config.rdbms.host,
        db_port=config.rdbms.port.as_int(),
        db_user=config.rdbms.username,
        db_password=config.rdbms.password,
        db_name=config.rdbms.database,
    )

    # Repositories:
    # sqla_research_topic_repository = providers.Factory(
    #     SQLAResearchTopicRepository,
    #     session=db.provided.session,
    # )
    
    # Gateways:
    google_search_gateway = providers.Factory(
        GoogleSearchGateway,
    )
    
    website_scraper_gateway = providers.Factory(
        WebsiteScraperGateway,
    )

    # Domain Services:
    localgpt_embedding_gateway = providers.Factory(
        LocalGPTEmbeddingService,
        device_type=config.embedding_service.device_type,
        embedding_model_name=config.embedding_service.embedding_model_name,
        root_dir=config.files.root_directory.as_(Path),
        docs_dir = config.files.source_docs_directory.as_(Path),
        db_directory = config.vectorstore.persist_dir.as_(Path),
        chunk_size=config.embedding_service.chunk_size.as_int(),
        chunk_overlap=config.embedding_service.chunk_overlap.as_int(),
    )

    localgpt_inference_gateway = providers.Factory(
        LocalGPTInferenceQueryService,
        llm_model = config.localgpt.llm_model,
        root_dir=config.files.root_directory.as_(Path),
        db_dir = config.vectorstore.persist_dir.as_(Path),
        embedding_model_name=config.embedding_service.embedding_model_name,
        device_type=config.embedding_service.device_type,
    )

    