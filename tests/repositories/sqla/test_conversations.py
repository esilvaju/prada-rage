from lib.core.entity.models import ConversationSender
from lib.infrastructure.repository.sqla.models import (
    SQLAConversation,
    SQLAMessage,
    SQLAResearchContext,
    SQLAResearchTopic,
    SQLAUser,
)


def test_add_conversation_to_research_context(db_session, fake):
    message_1 = SQLAMessage(
        content="Knock Knock",
        timestamp=fake.date_time(),
        sender=ConversationSender.USER,
    )
    message_2 = SQLAMessage(
        content="Who's there?",
        timestamp=fake.date_time(),
        sender=ConversationSender.AGENT,
    )

    conversation_title = "Knock Knock Jokes"
    conversation = SQLAConversation(
        title=conversation_title,
        messages=[message_1, message_2],
    )

    researchContext = SQLAResearchContext(
        title=fake.name(),
        conversations=[conversation],
    )

    researchTopic = SQLAResearchTopic(
        title=fake.name(),
        description=fake.text(),
        prada_tagger_node_id=fake.name(),
        research_contexts=[researchContext],
    )

    user = SQLAUser(
        prada_user_uuid=fake.name(),
        research_topics=[researchTopic],
    )

    with db_session() as session:
        researchTopic.save(session=session, flush=True)
        session.commit()

    with db_session() as session:
        conversation = session.query(SQLAConversation).filter_by(title=conversation_title).first()
        messages = conversation.messages
        assert len(messages) == 2
        assert messages[0].content == "Knock Knock"
        assert messages[0].sender == ConversationSender.USER
        assert messages[1].content == "Who's there?"
        assert messages[1].sender == ConversationSender.AGENT
