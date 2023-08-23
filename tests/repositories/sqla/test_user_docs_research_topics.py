from sqlalchemy.orm import Session
from lib.core.entity.models import ProtocolEnum
from lib.infrastructure.repository.sqla.models import SQLADocument, SQLAUser, SQLAResearchTopic
import pytest

def test_user_research_goal_accessibility(db_session: Session):
    doc1 = SQLADocument(
        name="test_name",
        lfn="a/b",
        protocol=ProtocolEnum.LOCAL,
    )
    doc2 = SQLADocument(
        name="test_name",
        lfn="a/b/c",
        protocol=ProtocolEnum.LOCAL,
    )

    maany = SQLAUser(
        prada_user_uuid="maany",
        research_topics=[
            SQLAResearchTopic(
                title="Test Research Topic",
                description="This is a test research topic",
                prada_tagger_node_id="ke-usho-luish",

            ),
        ]
    )
 
    with db_session() as session:
        session.add(maany)
        maany.knowledge_base.append(doc1)
        session.commit()      


    with db_session() as session:
        user = session.query(SQLAUser).filter_by(prada_user_uuid="maany").first()
        assert len(user.knowledge_base) == 1
        assert user.knowledge_base[0].lfn == "a/b"

        research_topic = session.query(SQLAResearchTopic).filter_by(title="Test Research Topic").first()
        assert research_topic.user.prada_user_uuid == "maany"
        
def test_user_save_failes_if_document_in_research_topic_not_in_knowledge_base(db_session):
    maany = SQLAUser(
        prada_user_uuid="maany",
    )

    user2 = SQLAUser(
        prada_user_uuid="user2",
    )

    knowledge_base_doc = SQLADocument(
        name="knowledge base doc",
        lfn="a/b",
        protocol=ProtocolEnum.LOCAL,
    )

    unknown_document = SQLADocument(
        name="unknown doc",
        lfn="a/b/c",
        protocol=ProtocolEnum.LOCAL,
    )

    maany.knowledge_base.append(knowledge_base_doc)
    user2.knowledge_base.append(unknown_document)

    research_topic = SQLAResearchTopic(
        title="Test Research Topic",
        description="This is a test research topic",
        prada_tagger_node_id="ke-usho-luish",
        documents=[unknown_document],
    )

    maany.research_topics.append(research_topic)

    with db_session() as session:
        with pytest.raises(ValueError):
            maany.save(session=session)

def test_research_topic_cannot_be_saved_if_doc_not_in_users_knowledge_base(db_session):
    user =  SQLAUser(
        prada_user_uuid="maany",
    )

    user2 = SQLAUser(
        prada_user_uuid="user2",
    )

    known_doc = SQLADocument(
        name="known doc",
        lfn="a/b",
        protocol=ProtocolEnum.LOCAL,
    )

    unknown_doc = SQLADocument(
        name="unknown doc",
        lfn="a/b/c",
        protocol=ProtocolEnum.LOCAL,
    )

    user.knowledge_base.append(known_doc)
    user2.knowledge_base.append(unknown_doc)

    research_topic = SQLAResearchTopic(
        title="Test Research Topic",
        description="This is a test research topic",
        prada_tagger_node_id="ke-usho-luish",
        documents=[unknown_doc],
        user=user,
    )

    with db_session() as session:
        with pytest.raises(ValueError):
            research_topic.save(session=session)
