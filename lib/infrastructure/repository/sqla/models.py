import uuid
from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SAEnum

from lib.infrastructure.repository.sqla.database import Base


class ProtocolEnum(Enum):
    S3 = 's3'
    NAS = 'nas'
    LOCAL = 'local'

class ConversationSender(Enum):
    USER = 'user'
    AGENT = 'agent'

class VectorStore(Base):
    __tablename__ = 'vector_stores'

    vector_store_id = Column(String, primary_key=True, default=uuid.uuid4().hex)
    name = Column(String)
    lfn = Column(String, unique=True)  # Logical File Name
    protocol = Column(SAEnum(ProtocolEnum), nullable=False)
    research_context_id = Column(String, ForeignKey('research_contexts.id'))

class Document(Base):
    __tablename__ = 'documents'
    
    document_id = Column(String, primary_key=True, default=uuid.uuid4().hex)
    name = Column(String)
    lfn = Column(String, unique=True)  # Logical File Name
    protocol = Column(SAEnum(ProtocolEnum), nullable=False)
    
class Message(Base):
    __tablename__ = 'messages'
    
    message_id = Column(String, primary_key=True, default=uuid.uuid4().hex)
    conversation_id = Column(String, ForeignKey('conversations.conversation_id'))
    timestamp = Column(DateTime)
    sender = Column(String)
    text = Column(String)
    source_documents = relationship('Document', backref='message')
    source_documents_metadata = Column(String)
    
class Conversation(Base):
    __tablename__ = 'conversations'
    
    conversation_id = Column(String, primary_key=True, default=uuid.uuid4().hex)
    participants = Column(SAEnum(ConversationSender), nullable=False)  # You might want to use a separate table for participants
    messages = relationship('Message', backref='conversation')
    research_context = Column(String, ForeignKey('research_contexts.id'))
    
class Note(Base):
    __tablename__ = 'notes'
    
    note_id = Column(String, primary_key=True, default=uuid.uuid4().hex)
    title = Column(String)
    content = Column(String)
    timestamp = Column(DateTime)
    conversation_id = Column(String, ForeignKey('conversations.conversation_id'))
    
class ResearchContext(Base):
    __tablename__ = 'research_contexts'
    
    id = Column(String, primary_key=True, default=uuid.uuid4().hex)
    title = Column(String)
    vector_store = Column(String)
    research_id = Column(String, ForeignKey('research_goals.id'), nullable=False)
    source_documents = relationship('Document', backref='research_context')
    conversations = relationship('Conversation', backref='research_context')
    notes = relationship('Note', backref='research_context')
    
class Research(Base):
    __tablename__ = 'research_goals'
    
    id = Column(String, primary_key=True, default=uuid.uuid4().hex)
    title = Column(String)
    prada_tagger_node_id = Column(String)
    archived = Column(Boolean)
    prada_uuid = Column(String)
    contexts = relationship('ResearchContext', backref='research')
    documents = relationship('Document', backref='research')