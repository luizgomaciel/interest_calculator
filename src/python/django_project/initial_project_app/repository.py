import uuid
from typing import Optional
from src.python.application.domain.initial_project import InitialProject
from src.python.application.repositories.project_repository import ProjectRepository
from src.python.django_project.initial_project_app.models import InitialProjectModel


def _to_domain(model: type[InitialProjectModel]) -> InitialProject:
    return InitialProject(
        id=str(model.id),
        name=model.name,
        description=model.description
    )

class DjangoProjectRepository(ProjectRepository):
    def __init__(self, initial_project_model: InitialProjectModel = InitialProjectModel):
        self.initial_project_model = initial_project_model

    def create_project(self, project: InitialProject) -> str:
        created = self.initial_project_model.objects.create(
            id=project.id,
            name=project.name,
            description=project.description
        )
        return str(created.id)

    def get_project_by_id(self, project_id: str) -> Optional[InitialProject]:
        try:
            model = self.initial_project_model.objects.get(id=uuid.UUID(project_id))
            return _to_domain(model)
        except self.initial_project_model.DoesNotExist:
            return None