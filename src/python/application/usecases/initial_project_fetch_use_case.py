from src.python.application.domain.initial_project import InitialProject

class InitialProjectFetchUseCase:
    def __init__(self, project_repository):
        self.project_repository = project_repository

    def execute(self, project_id) -> InitialProject:
        return self.project_repository.get_project_by_id(project_id)