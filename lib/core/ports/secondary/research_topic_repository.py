from abc import ABC, abstractmethod
import logging
from lib.core.dto.research_topic_repository_dto import RegisterSourceDocDTO

from lib.core.entity.models import ResearchTopic, Document

class ResearchTopicRepository(ABC):
    """
    Abstract base class for research goal repositories.

    @cvar logger: The logger for this class.
    @type logger: logging.Logger
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def register_source_doc(self, research_topic: ResearchTopic, source_doc: Document) -> RegisterSourceDocDTO:
        """
        Register a source document for a research goal.

        @param research_topic: The research goal to register the source document for.
        @type research_topic: ResearchGoal
        @param source_doc: The source document to register.
        @type source_doc: Document
        @return: A DTO containing the result of the operation.
        @rtype: RegisterSourceDocDTO
        """
        pass

    @abstractmethod
    def unregister_source_doc(self, research_ropiv: ResearchTopic, source_doc: Document):
        """
        Unregister a source document for a research goal.

        @param research_topic: The research goal to unregister the source document for.
        @type research_topic: ResearchGoal
        @param source_doc: The source document to unregister.
        @type source_doc: Document
        """
        pass


    @abstractmethod
    def archive_research_topic(self, research_topic: ResearchTopic):
        """
        Archive a research goal.

        @param research_topic: The research goal to archive.
        @type research_topic: ResearchGoal
        """
        pass