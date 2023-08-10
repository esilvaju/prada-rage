from pathlib import Path
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from typing import List
from chromadb import Client, PersistentClient
from chromadb.config import Settings

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from lib.core.entity.devices import DeviceType
from lib.core.service.embedding_service import EmbeddingService

class LocalGPTEmbeddingService(EmbeddingService):
    def __init__(self, device_type: str, 
                 embedding_model_name: str, 
                 root_dir: str, 
                 docs_dir: Path, 
                 chunk_size: int, 
                 chunk_overlap: int , 
                 db_directory: str, 
                 ):
        docs_dir = root_dir / docs_dir
        db_dir = root_dir / db_directory
        
        super().__init__(
            device_type=DeviceType(device_type), 
            embedding_model_name=embedding_model_name, 
            docs_dir=docs_dir,
            db_dir=db_dir,
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap, 
        )
        
    
    def create_embeddings(self, documents: list[Document]) -> dict[str, List[Document]]:
        # Loads all documents from the source documents directory
        if(len(documents) == 0):
            self.logger.info(f"Loading documents from {self.docs_dir}")
            documents = self.load_documents(self.docs_dir)
        
        # Groups documents by file extension
        document_groups = self.group_documents_by_extension(documents)
        self.logger.info(f"Loaded {len(documents)} documents")
        
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        data = text_splitter.split_documents(documents)
        self.logger.info(f"Split {len(documents)} documents into {len(data)} chunks")

        # Create embeddings for each document
        self.logger.info("Creating embeddings")
        embedding_fn = HuggingFaceInstructEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": self.device_type.value},
        )

        # change the embedding type here if you are running into issues.
        # These are much smaller embeddings and will work for most appications
        # If you use HuggingFaceEmbeddings, make sure to also use the same in the
        # inference service.

        # embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        
        db = Chroma.from_documents(data, embedding_fn, persist_directory=self.db_dir)
        return db
