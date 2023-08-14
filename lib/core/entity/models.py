from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import uuid4


class Document(BaseModel):
    document_id: int = Field(default_factory=lambda: uuid4().hex)
    title: str
    content: str


class Message(BaseModel):
    message_id: int = Field(default_factory=lambda: uuid4().hex)
    conversation_id: str
    timestamp: datetime
    sender: str
    text: str


class Conversation(BaseModel):
    conversation_id: int = Field(default_factory=lambda: uuid4().hex)
    participants: List[str]
    messages: List[Message]


class Note(BaseModel):
    note_id: int = Field(default_factory=lambda: uuid4().hex)
    title: str
    content: str
    timestamp: datetime


class ResearchContext(BaseModel):
    id: int = Field(default_factory=lambda: uuid4().hex)
    title: str
    vector_store: str
    source_documents: List[Document]
    conversations: List[Conversation]
    notes: List[Note]


class Research(BaseModel):
    id: int = Field(default_factory=lambda: uuid4().hex)
    title: str
    contexts: List[ResearchContext]
    documents: List[Document]
    prada_tagger_node_id: str
    archived: bool
    prada_uuid: str