from uuid import UUID

from src.python.application.domain.initial_project import InitialProject
from src.python.application.repositories.project_repository import ProjectRepository


class InitialProjectFetchUseCase:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def execute(self, project_id: str) -> InitialProject:
        return self.repository.get_project_by_id(project_id)