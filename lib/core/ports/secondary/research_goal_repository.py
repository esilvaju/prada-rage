from abc import ABC, abstractmethod


from lib.core.entity.models import User, ResearchGoal


class ResearchGoalRepository(ABC):
    def __init__(self):
        self.__research_goals = {}

    @abstractmethod
    def create_research_goal(self, research_goal: ResearchGoal):
        raise NotImplementedError

    @abstractmethod
    def list_research_goals_for_user(self, user: User):
        raise NotImplementedError
    
    