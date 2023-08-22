from enum import Enum
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import uuid4

class ProtocolEnum(Enum):
    """
    Enum for the different protocols that can be used to store a document.
    """
    S3 = 's3'
    NAS = 'nas'
    LOCAL = 'local'

class ConversationSender(Enum):
    """
    Enum for the different participants in a conversation.
    """
    USER = 'user'
    AGENT = 'agent'


class NoteType(Enum):
    """
    Enum for the different types of notes.
    """
    DOCUMENT = 'document_note'
    CONVERSATION = 'conversation_note'
    USER = 'user_note'

class BaseRageModel(BaseModel):
    created_at: datetime
    updated_at: datetime

class BaseSoftDeleteRageModel(BaseRageModel):
    deleted: bool
    deleted_at: datetime

class BaseNote(BaseSoftDeleteRageModel):
    id: int
    title: str
    content: str

class User(BaseRageModel):
    """
    Represents a user in the system
    """
    prada_user_uuid: str
    notes: List["UserNote"]

    def __str__(self) -> str:
        return "User: " + super().__str__() + f", prada_user_uuid: {self.prada_user_uuid}"

class UserNote(BaseNote):
    """ 
    Represents a note left by the user
    """
    user: User


# class Document(BaseModel):
#     """
#     Represents a document or a file containing the information for the Knowledge Base
#     """
#     id: int = Field(default_factory=lambda: uuid4().hex)
#     name: str
#     type: str
#     lfn: str
#     protocol: ProtocolEnum

#     def __str__(self) -> str:
#         return "Document: " + super().__str__() + f", id: {self.id}, name: {self.name}, lfn: {self.lfn}, protocol: {self.protocol}"

# class Message(BaseModel):
#     """
#     Represents a message in a conversation
#     """
#     message_id: int = Field(default_factory=lambda: uuid4().hex)
#     conversation_id: str
#     timestamp: datetime
#     sender: str
#     text: str


# class Conversation(BaseModel):
#     """
#     Represents a conversation between a user and an agent in a research context
#     """
#     conversation_id: int = Field(default_factory=lambda: uuid4().hex)
#     participants: List[str]
#     messages: List[Message]
#     context: "ResearchContext"


# class Note(BaseModel):
#     """
#     Represents a note left by the user
#     """
#     note_id: int = Field(default_factory=lambda: uuid4().hex)
#     title: str
#     content: str
#     timestamp: datetime


# class ResearchContext(BaseModel):
#     """
#     A research context is a collection of documents, conversations and notes under a research goal
#     """
#     id: int = Field(default_factory=lambda: uuid4().hex)
#     title: str
#     vector_store: str
#     source_documents: List[Document]
#     conversations: List[Conversation]
#     notes: List[Note]


# class ResearchTopic(BaseModel):
#     """
#     A research goal is a collection of research contexts and knowledge base documents
#     """
#     id: int = Field(default_factory=lambda: uuid4().hex)
#     title: str
#     description: str
#     prada_tagger_node_id: str
#     archived: bool
#     prada_uuid: str
#     contexts: List[ResearchContext]
#     documents: List[Document]