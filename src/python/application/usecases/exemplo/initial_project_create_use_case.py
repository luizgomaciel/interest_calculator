from dataclasses import dataclass

from src.python.application.domain.initial_project import InitialProject
from src.python.application.repositories.project_repository import ProjectRepository


@dataclass
class InitialProjectCreateRequest:
    project_name: str
    project_description: str

class InitialProjectCreateUseCase:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def execute(self, request: InitialProjectCreateRequest) -> str:
        domain = InitialProject(
            name=request.project_name,
            description=request.project_description
        )

        project_id = self.repository.create_project(
            domain
        )

        return project_id