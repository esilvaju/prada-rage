from datetime import datetime
from typing import List

from sqlalchemy import (
    CheckConstraint,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Table,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SAEnum
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import mapped_column, object_mapper, relationship, Mapped

from lib.infrastructure.repository.sqla.database import Base
from lib.core.entity.models import ConversationSender, NoteType, ProtocolEnum


class ModelBase(object):
    """Base class for Rage Models"""

    __table_initialized__ = False

    @declared_attr
    def __table_args__(cls):  # pylint: disable=no-self-argument
        # exception for CERN Oracle identifier length limitations
        # pylint: disable=maybe-no-member
        # otherwise, proceed normally
        # pylint: disable=maybe-no-member
        return (
            CheckConstraint(
                "CREATED_AT IS NOT NULL", name=cls.__tablename__.upper() + "_CREATED_NN"
            ),
            CheckConstraint(
                "UPDATED_AT IS NOT NULL", name=cls.__tablename__.upper() + "_UPDATED_NN"
            ),
            {"mysql_engine": "InnoDB"},
        )

    @declared_attr
    def created_at(cls):  # pylint: disable=no-self-argument
        return mapped_column("created_at", DateTime, default=datetime.utcnow)

    @declared_attr
    def updated_at(cls):  # pylint: disable=no-self-argument
        return mapped_column(
            "updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
        )

    def save(self, flush=True, session=None):
        """Save this object"""
        # Sessions created with autoflush=True be default since sqlAlchemy 1.4.
        # So explicatly calling session.flush is not necessary.
        # However, when autogenerated primary keys involved, calling
        # session.flush to get the id from DB.
        session.add(self)
        if flush:
            session.flush()

    def delete(self, flush=True, session=None):
        """Delete this object"""
        session.delete(self)
        if flush:
            session.flush()

    def update(self, values, flush=True, session=None):
        """dict.update() behaviour."""
        for k, v in values.items():
            self[k] = v
        if session and flush:
            session.flush()

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __iter__(self):
        self._i = iter(object_mapper(self).columns)
        return self

    def __next__(self):
        n = next(self._i).name
        return n, getattr(self, n)

    def keys(self):
        return list(self.__dict__.keys())

    def values(self):
        return list(self.__dict__.values())

    def items(self):
        return list(self.__dict__.items())

    def to_dict(self):
        dictionary = self.__dict__.copy()
        dictionary.pop("_sa_instance_state")
        return dictionary

    next = __next__


class SoftModelBase(ModelBase):
    """Base class for Rage Models with soft-deletion support"""

    __table_initialized__ = False

    @declared_attr
    def __table_args__(cls):  # pylint: disable=no-self-argument
        # pylint: disable=maybe-no-member
        return (
            CheckConstraint(
                "CREATED_AT IS NOT NULL", name=cls.__tablename__.upper() + "_CREATED_NN"
            ),
            CheckConstraint(
                "UPDATED_AT IS NOT NULL", name=cls.__tablename__.upper() + "_UPDATED_NN"
            ),
            CheckConstraint(
                "DELETED IS NOT NULL", name=cls.__tablename__.upper() + "_DELETED_NN"
            ),
            {"mysql_engine": "InnoDB"},
        )

    @declared_attr
    def deleted(cls):  # pylint: disable=no-self-argument
        return mapped_column("deleted", Boolean, default=False)

    @declared_attr
    def deleted_at(cls):  # pylint: disable=no-self-argument
        return mapped_column("deleted_at", DateTime)

    def delete(self, flush=True, session=None):
        """Delete this object"""
        self.deleted = True
        self.deleted_at = datetime.utcnow()
        self.save(session=session)


class SQLAUser(Base, ModelBase):
    __tablename__ = "user"

    prada_user_uuid: Mapped[str] = mapped_column(
        "prada_user_uuid", String, primary_key=True
    )
    notes: Mapped[List["SQLAUserNote"]] = relationship("SQLAUserNote", backref="user")
    research_topics: Mapped[List["SQLAResearchTopic"]] = relationship("SQLAResearchTopic", backref="user")
    knowledge_base: Mapped[List["SQLADocument"]] = relationship("SQLADocument", backref="user")

    def __repr__(self):
        return f"<User(prada_user_uuid={self.prada_user_uuid})>"


class NoteModelBase:
    """Base class for Notes"""

    __table_initialized__ = False

    @declared_attr
    def title(cls):
        return mapped_column("title", String, nullable=False)

    @declared_attr
    def content(cls):
        return mapped_column("content", Text, nullable=False)


class SQLANote(Base, NoteModelBase, SoftModelBase):
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[NoteType] = mapped_column(SAEnum(NoteType), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "note", "polymorphic_on": "type"}



ResearchTopicKnowledgeBaseAssociation = Table(
    'research_topic_knowledge_base_association',
    Base.metadata,
    Column('research_topic_id', Integer, ForeignKey('research_topic.id')),
    Column('document_id', Integer, ForeignKey('knowledge_base.id'))
)

class SQLADocument(Base, SoftModelBase):
    __tablename__ = "knowledge_base"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    lfn: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    protocol: Mapped[ProtocolEnum] = mapped_column(
        SAEnum(ProtocolEnum), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("user.prada_user_uuid"), nullable=False
    )
    notes: Mapped[List['SQLADocumentNote']] = relationship('SQLADocumentNote', backref='document')

    def __repr__(self):
        return f"<Document (id={self.id}, name={self.name})>"
    

class SQLAResearchTopic(Base, SoftModelBase):
    __tablename__ = 'research_topic'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    prada_tagger_node_id: Mapped[str] = mapped_column(String, nullable=True)
    documents: Mapped[List['SQLADocument']] = relationship('SQLADocument', secondary=ResearchTopicKnowledgeBaseAssociation)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("user.prada_user_uuid"), nullable=False
    )
    research_contexts: Mapped[List['SQLAResearchContext']] = relationship('SQLAResearchContext', backref='research_topic')
    notes: Mapped[List['SQLAResearchTopicNotes']] = relationship('SQLAResearchTopicNotes', backref='research_topic')

    def __repr__(self):
        return f"<ResearchTopic (id={self.id}, title={self.title})>"

Document_ResearchContext_Association = Table(
    'document_research_context_association',
    Base.metadata,
    Column('document_id', Integer, ForeignKey('knowledge_base.id')),
    Column('research_context_id', Integer, ForeignKey('research_context.id'))
)

class SQLAVectorStore(Base, ModelBase):
    __tablename__ = 'vector_store'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    lfn: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    protocol: Mapped[ProtocolEnum] = mapped_column(
        SAEnum(ProtocolEnum), nullable=False
    )
    research_context_id: Mapped[int] = mapped_column(ForeignKey("research_context.id"), nullable=False)
    research_context: Mapped['SQLAResearchContext'] = relationship('SQLAResearchContext',back_populates='vector_store')

class SQLAResearchContext(Base, SoftModelBase):
    __tablename__ = 'research_context'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    research_topic_id: Mapped[int] = mapped_column(
        ForeignKey("research_topic.id"), nullable=False
    )
    documents: Mapped[List['SQLADocument']] = relationship('SQLADocument', secondary=Document_ResearchContext_Association)
    vector_store: Mapped['SQLAVectorStore'] = relationship('SQLAVectorStore', back_populates='research_context', uselist=False)
    conversations: Mapped[List['SQLAConversation']] = relationship('SQLAConversation', backref='research_context')


class SQLAConversation(Base, SoftModelBase):
    __tablename__ = 'conversation'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    research_context_id = mapped_column(ForeignKey('research_context.id'), nullable=False)
    messages: Mapped[List['SQLAMessage']] = relationship('SQLAMessage', backref='conversation')
    notes: Mapped[List['SQLAConversationNote']] = relationship('SQLAConversationNote', backref='conversation')

class SQLAMessage(Base, SoftModelBase):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sender: Mapped[ConversationSender] = mapped_column(SAEnum(ConversationSender), nullable=False)
    conversation_id: Mapped[int] = mapped_column(ForeignKey('conversation.id'), nullable=False)

class SQLAUserNote(SQLANote):
    __tablename__ = "user_note"
    id: Mapped[int] = mapped_column(Integer, ForeignKey("note.id"), primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("user.prada_user_uuid"), nullable=False
    )

    __mapper_args__ = {
        "polymorphic_identity": NoteType.USER,
    }

    def __repr__(self):
        return f"<UserNote (id={self.id}, user={self.user_id})>"


class SQLAConversationNote(SQLANote):
    __tablename__ = "conversation_note"
    id: Mapped[int] = mapped_column(Integer, ForeignKey("note.id"), primary_key=True)
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversation.id"), nullable=False
    )

    __mapper_args__ = {
        "polymorphic_identity": NoteType.CONVERSATION,
    }

    def __repr__(self):
        return f"<ConversationNote (id={self.id}, conversation={self.conversation_id})>"
    
class SQLADocumentNote(SQLANote):
    __tablename__ = "document_note"
    id: Mapped[int] = mapped_column(Integer, ForeignKey("note.id"), primary_key=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("knowledge_base.id"), nullable=False
    )

    __mapper_args__ = {
        "polymorphic_identity": NoteType.DOCUMENT,
    }

    def __repr__(self):
        return f"<DocumentNote (id={self.id}, document={self.document_id})>"


class SQLAResearchTopicNotes(SQLANote):
    __tablename__ = "research_topic_note"
    id: Mapped[int] = mapped_column(Integer, ForeignKey("note.id"), primary_key=True)
    research_topic_id: Mapped[int] = mapped_column(
        ForeignKey("research_topic.id"), nullable=False
    )

    __mapper_args__ = {
        "polymorphic_identity": NoteType.RESEARCH_TOPIC,
    }

    def __repr__(self):
        return f"<ResearchTopicNote (id={self.id}, research_topic={self.research_topic_id})>"