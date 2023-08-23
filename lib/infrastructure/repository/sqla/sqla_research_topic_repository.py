from lib.core.dto.research_topic_repository_dto import RegisterSourceDocDTO
from lib.core.entity.models import Document, ResearchTopic
from lib.core.ports.secondary.research_topic_repository import ResearchTopicRepository
from sqlalchemy.orm import Session

from lib.infrastructure.repository.sqla.models import SQLADocument, SQLAResearchGoal

class SQLAResearchTopicRepository(ResearchTopicRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session: Session = session

    def register_source_doc(self, research_topic, source_doc):
        if(source_doc is None):
            errorDTO = RegisterSourceDocDTO(
                status=False, 
                errorCode=-1, 
                errorMessage=f"Source document {source_doc} is None", 
                errorName="Document Not Provided", 
                errorType="DocumentNotProvided")
            self.logger.error(f"{errorDTO}")
            return errorDTO
        
        if(source_doc.id is None):
            self.logger.error(f"Source document has no id: {source_doc}")
            errorDTO = RegisterSourceDocDTO(
                status=False, 
                errorCode=-1, 
                errorMessage=f"Invalid Source document. {source_doc} has no id", 
                errorName="Invalid Document", 
                errorType="InvalidDocument")
            self.logger.error(f"{errorDTO}")
            return errorDTO
        
        if(research_topic is None):
            self.logger.error(f"Research goal is None")
            errorDTO = RegisterSourceDocDTO(
                status=False, 
                errorCode=-1, 
                errorMessage=f"Research goal is None", 
                errorName="Research Goal Not Provided", 
                errorType="ResearchGoalNotProvided")
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if(research_topic.id is None):
            self.logger.error(f"Research goal has no id: {research_topic}")
            errorDTO = RegisterSourceDocDTO(
                status=False, 
                errorCode=-1, 
                errorMessage=f"Invalid Research goal. {research_topic} has no id", 
                errorName="Invalid Research Goal", 
                errorType="InvalidResearchGoal")
            self.logger.error(f"{errorDTO}")
            return errorDTO
        
        sqla_document: SQLADocument | None = self.session.get(SQLADocument, source_doc.id)
        
        if(sqla_document is None):
            self.logger.error(f"Document {source_doc} not found in the database.")
            errorDTO = RegisterSourceDocDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Document {source_doc} not found in the database.",
                errorName="Document Not Found",
                errorType="DocumentNotFound"
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO
        
        research_topic: SQLAResearchGoal | None = self.session.get(SQLAResearchGoal, research_topic.id)
        if(research_topic is None):
            self.logger.error(f"Research goal {research_topic} not found in the database.")
            errorDTO = RegisterSourceDocDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Research goal {research_topic} not found in the database.",
                errorName="Research Goal Not Found",
                errorType="ResearchGoalNotFound"
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO
        
        # add the source document to the research goal
        existing_sqla_documents = research_topic.documents
        if(sqla_document in existing_sqla_documents):
            self.logger.error(f"Document {sqla_document} already registered for research goal {research_topic}")
            errorDTO = RegisterSourceDocDTO(
                status=False,
                errorCode=0,
                errorMessage=f"Document {sqla_document} already registered for research goal {research_topic}",
                errorName="Document Already Registered",
                errorType="DocumentAlreadyRegistered"
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO
        
        research_topic.documents.extend([sqla_document])

        # commit the changes
        try:
            self.session.commit()
        except Exception as e:
            self.logger.error(f"Error committing changes to the database: {e}")
            errorDTO = RegisterSourceDocDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Error committing changes to the database: {e}",
                errorName="Database Error",
                errorType="DatabaseError"
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO
        
        self.logger.info(f"Successfully registered document {sqla_document} for research goal {research_topic}")
        
        return RegisterSourceDocDTO(
            status=True,
            errorCode=0,
        )

    def unregister_source_doc(self, research_topic: ResearchTopic, source_doc: Document):
        pass

    def archive_research_topic(self, research_topic: ResearchTopic):
        pass
