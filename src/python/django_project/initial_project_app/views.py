
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from src.python.application.usecases.initial_project_create_use_case import InitialProjectCreateUseCase, \
    InitialProjectCreateRequest
from src.python.application.usecases.initial_project_fetch_use_case import InitialProjectFetchUseCase
from src.python.django_project.initial_project_app.repository import DjangoProjectRepository


class InitialProjectView(viewsets.ViewSet):
    def get(self, request, project_id):
        use_case = InitialProjectFetchUseCase(
            repository=DjangoProjectRepository()
        )
        project = use_case.execute(project_id=project_id)

        data = {
            'id': project.id,
            'name': project.name,
            'description': project.description
        }
        return Response(data, status=HTTP_200_OK)

    def post(self, request):
        use_case = InitialProjectCreateUseCase(
            repository=DjangoProjectRepository()
        )

        request = InitialProjectCreateRequest(
            project_name=request.data.get('name'),
            project_description=request.data.get('description')
        )

        project_id = use_case.execute(
            request
        )

        return Response(
            project_id,
            status=HTTP_201_CREATED
        )
