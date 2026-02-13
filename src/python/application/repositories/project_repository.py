from abc import ABC, abstractmethod

from src.python.application.domain.initial_project import InitialProject

class ProjectRepository(ABC):
    @abstractmethod
    def get_project_by_id(self, project_id: str) -> InitialProject:
        raise NotImplementedError

    @abstractmethod
    def create_project(self, initial_project: InitialProject) -> str:
        raise NotImplementedError