from lib.core.dto.research_goal_repository_dto import RegisterSourceDocDTO
from lib.core.entity.models import Document, ResearchTopic
from lib.core.ports.secondary.research_topic_repository import ResearchTopicRepository
from sqlalchemy.orm import Session

from lib.infrastructure.repository.sqla.models import SQLADocument, SQLAResearchGoal

class SQLAResearchGoalRepository(ResearchTopicRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session: Session = session

    def register_source_doc(self, research_goal, source_doc):
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
        
        if(research_goal is None):
            self.logger.error(f"Research goal is None")
            errorDTO = RegisterSourceDocDTO(
                status=False, 
                errorCode=-1, 
                errorMessage=f"Research goal is None", 
                errorName="Research Goal Not Provided", 
                errorType="ResearchGoalNotProvided")
            self.logger.error(f"{errorDTO}")
            return errorDTO

        if(research_goal.id is None):
            self.logger.error(f"Research goal has no id: {research_goal}")
            errorDTO = RegisterSourceDocDTO(
                status=False, 
                errorCode=-1, 
                errorMessage=f"Invalid Research goal. {research_goal} has no id", 
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
        
        research_goal: SQLAResearchGoal | None = self.session.get(SQLAResearchGoal, research_goal.id)
        if(research_goal is None):
            self.logger.error(f"Research goal {research_goal} not found in the database.")
            errorDTO = RegisterSourceDocDTO(
                status=False,
                errorCode=-1,
                errorMessage=f"Research goal {research_goal} not found in the database.",
                errorName="Research Goal Not Found",
                errorType="ResearchGoalNotFound"
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO
        
        # add the source document to the research goal
        existing_sqla_documents = research_goal.documents
        if(sqla_document in existing_sqla_documents):
            self.logger.error(f"Document {sqla_document} already registered for research goal {research_goal}")
            errorDTO = RegisterSourceDocDTO(
                status=False,
                errorCode=0,
                errorMessage=f"Document {sqla_document} already registered for research goal {research_goal}",
                errorName="Document Already Registered",
                errorType="DocumentAlreadyRegistered"
            )
            self.logger.error(f"{errorDTO}")
            return errorDTO
        
        research_goal.documents.extend([sqla_document])

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
        
        self.logger.info(f"Successfully registered document {sqla_document} for research goal {research_goal}")
        
        return RegisterSourceDocDTO(
            status=True,
            errorCode=0,
        )

    def unregister_source_doc(self, research_goal: ResearchTopic, source_doc: Document):
        pass

    def archive_research_goal(self, research_goal: ResearchTopic):
        pass
