from lib.infrastructure.repository.sqla.models import (
    SQLADocument,
    SQLAResearchContext,
    SQLAResearchTopic,
    SQLAUser,
    SQLAVectorStore,
)


def test_research_topic_can_access_research_contexts(db_session, fake):
    username = fake.name()
    research_context_title = fake.name()
    research_topic_title = fake.name()

    user = SQLAUser(
        prada_user_uuid=username,
    )

    research_topic = SQLAResearchTopic(
        title=research_topic_title,
        description=fake.sentence(),
        prada_tagger_node_id=fake.name(),
    )

    research_context = SQLAResearchContext(
        title=research_context_title,
        research_topic=research_topic,
    )

    research_topic.research_contexts.append(research_context)
    user.research_topics.append(research_topic)

    with db_session() as session:
        user.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        user = session.query(SQLAUser).filter_by(prada_user_uuid=username).first()
        assert len(user.research_topics) == 1
        assert len(user.research_topics[0].research_contexts) == 1
        assert user.research_topics[0].research_contexts[0].title == research_context_title

        research_topic = session.query(SQLAResearchTopic).filter_by(title=research_topic_title).first()
        assert research_topic.user.prada_user_uuid == username
        assert research_topic.research_contexts[0].title == research_context_title

        research_context = session.query(SQLAResearchContext).filter_by(title=research_context_title).first()
        assert research_context.research_topic.title == research_topic_title
        assert research_context.research_topic.user.prada_user_uuid == username
