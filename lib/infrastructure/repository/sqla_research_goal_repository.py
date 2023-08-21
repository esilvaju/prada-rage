from lib.core.ports.secondary.research_goal_repository import ResearchGoalRepository


class SQLAResearchGoalRepository(ResearchGoalRepository):
    def __init__(self, session):
        self.session = session

