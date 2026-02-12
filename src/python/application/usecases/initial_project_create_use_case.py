from dataclasses import dataclass

from src.python.application.domain.initial_project import InitialProject

@dataclass
class InitialProjectCreateRequest:
    project_name: str
    project_description: str

class InitialProjectCreateUseCase:
    def __init__(self, project_repository):
        self.project_repository = project_repository

    def execute(self, request: InitialProjectCreateRequest) -> str:
        domain = InitialProject(
            name=request.project_name,
            description=request.project_description
        )

        project_id = self.project_repository.create_project(
            domain
        )

        return project_id