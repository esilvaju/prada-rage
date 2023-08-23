from faker import Faker
from sqlalchemy.orm import Session
from lib.core.entity.models import ProtocolEnum
from lib.infrastructure.repository.sqla.models import SQLADocument, SQLAUser, SQLAResearchTopic

def test_user_research_goal_accessibility(db_session: Session, fake: Faker):
    lfn = fake.file_path(depth=2)

    doc1 = SQLADocument(
        name=fake.name(),
        lfn=lfn,
        protocol=ProtocolEnum.LOCAL,
    )

    username = fake.name()
    maany = SQLAUser(
        prada_user_uuid=username,
        research_topics=[
            SQLAResearchTopic(
                title="Test Research Topic",
                description="This is a test research topic",
                prada_tagger_node_id="ke-usho-luish",

            ),
        ]
    )
 
    maany.knowledge_base.append(doc1)
    
    with db_session() as session:
        session.add(maany)
        session.commit()      


    with db_session() as session:
        user = session.query(SQLAUser).filter_by(prada_user_uuid=username).first()
        assert len(user.knowledge_base) == 1
        assert user.knowledge_base[0].lfn == lfn

        research_topic = session.query(SQLAResearchTopic).filter_by(title="Test Research Topic").first()
        assert research_topic.user.prada_user_uuid == username
