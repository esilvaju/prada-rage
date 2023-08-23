from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import os
from pathlib import Path
from typing import Any, Dict, List
from langchain.vectorstores import Chroma

# https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/excel.html?highlight=xlsx#microsoft-excel
from langchain.document_loaders import CSVLoader, PDFMinerLoader, TextLoader, UnstructuredExcelLoader, Docx2txtLoader
from langchain.docstore.document import Document
import logging

from lib.infrastructure.config.devices import DeviceType


class EmbeddingService(ABC):
    def __init__(
        self,
        device_type: DeviceType,
        docs_dir: Path,
        db_dir: Path,
        embedding_model_name: str,
        chunk_size: int,
        chunk_overlap: int,
    ) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._document_map = {
            ".txt": TextLoader,
            ".md": TextLoader,
            ".py": TextLoader,
            ".pdf": PDFMinerLoader,
            ".csv": CSVLoader,
            ".xls": UnstructuredExcelLoader,
            ".xlsx": UnstructuredExcelLoader,
            ".docx": Docx2txtLoader,
            ".doc": Docx2txtLoader,
        }
        self._docs_dir = docs_dir
        self._db_dir = db_dir
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self._device_type = device_type
        self._embedding_model_name = embedding_model_name

    @property
    def document_map(self):
        return self._document_map

    @property
    def docs_dir(self):
        return self._docs_dir

    @property
    def db_dir(self):
        return str(self._db_dir)

    @property
    def model_name(self):
        return self._embedding_model_name

    @property
    def ingest_threads(self):
        return os.cpu_count() or 8

    @property
    def device_type(self):
        return self._device_type

    @property
    def chunk_size(self):
        return self._chunk_size

    @property
    def chunk_overlap(self):
        return self._chunk_overlap

    @abstractmethod
    def create_embeddings(self, documents: list[Document]) -> Chroma:
        raise NotImplementedError

    def load_single_document(self, path: str) -> Document:
        file_extension = f".{path.split('.')[-1]}"
        loader_class = self.document_map.get(file_extension)
        if loader_class:
            loader = loader_class(path)
        else:
            raise ValueError(f"Document type {file_extension} for file {path} is undefined")
        dataset: List[Document] = loader.load()
        return dataset[0]

    def load_document_batch(self, filepaths):
        self.logger.info("Loading document batch")
        # create a thread pool
        with ThreadPoolExecutor(len(filepaths)) as exe:
            # load files
            futures = [exe.submit(self.load_single_document, name) for name in filepaths]
            # collect data
            data_list = [future.result() for future in futures]
            # return data and file paths
            return (data_list, filepaths)

    def load_documents(self, source_dir: Path) -> list[Document]:
        # Loads all documents from the source documents directory
        all_files = os.listdir(source_dir)
        paths = []
        for file_path in all_files:
            file_extension = os.path.splitext(file_path)[1]
            source_file_path = os.path.join(source_dir, file_path)
            if file_extension in self.document_map.keys():
                paths.append(source_file_path)

        # Have at least one worker and at most INGEST_THREADS workers
        n_workers = min(self.ingest_threads, max(len(paths), 1))
        chunksize = round(len(paths) / n_workers)
        docs = []
        with ProcessPoolExecutor(n_workers) as executor:
            futures = []
            # split the load operations into chunks
            for i in range(0, len(paths), chunksize):
                # select a chunk of filenames
                filepaths = paths[i : (i + chunksize)]
                # submit the task
                future = executor.submit(self.load_document_batch, filepaths)
                futures.append(future)
            # process all results
            for future in as_completed(futures):
                # open the file and load the data
                contents, _ = future.result()
                docs.extend(contents)

        return docs

    def group_documents_by_extension(self, documents: List[Document]) -> dict[str, List[Document]]:
        # Groups documents by file extension
        document_groups: Dict[str, List[Document]] = {}
        for document in documents:
            file_extension = os.path.splitext(document.metadata["source"])[1]
            if file_extension not in document_groups:
                document_groups[file_extension] = []
            document_groups[file_extension].append(document)
        return document_groups
