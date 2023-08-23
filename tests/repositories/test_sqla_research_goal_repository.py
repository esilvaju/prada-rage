pass
# import pytest
# from lib.core.entity.models import ProtocolEnum, ResearchTopic, Document
# from lib.core.ports.secondary.research_topic_repository import ResearchTopicRepository
# from lib.infrastructure.config.containers import Container
# from sqlalchemy.orm import Session

# from lib.infrastructure.repository.sqla.models import SQLAResearchGoal

# def test_return_error_when_source_doc_is_not_registered(app_container: Container, db_session: Session):
#     pass
# research_goal_factory: ResearchTopicRepository = app_container.sqla_research_goal_repository()
# research_goal = ResearchTopic(
#     title="My research goal",
#     description="This does no research to be honest",
#     archived=False,
#     contexts=[],
#     documents=[],
#     prada_tagger_node_id="ke-usho-luish",
#     prada_uuid="1222894"
# )

# source_doc: Document = Document(
#     name="test_name",
#     lfn="a/b",
#     type="pdf",
#     protocol=ProtocolEnum.LOCAL,
# )

# sqla_research_goal = SQLAResearchGoal(
#     id=research_goal.id,
#     title=research_goal.title,
#     description=research_goal.description,
#     archived=research_goal.archived,
#     contexts=[],
#     source_docs=[],
# )

# db_session.add(sqla_research_goal)
# db_session.commit()

# result = research_goal_factory.register_source_doc(research_goal, source_doc)

# assert result.status == False
