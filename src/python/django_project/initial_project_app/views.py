# python
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from src.python.application.usecases.exemplo.initial_project_create_use_case import (
    InitialProjectCreateUseCase,
    InitialProjectCreateRequest,
)
from src.python.application.usecases.exemplo.initial_project_fetch_use_case import InitialProjectFetchUseCase
from src.python.django_project.initial_project_app.repository import DjangoProjectRepository
from src.python.django_project.initial_project_app.serializers import InitialProjectSerializer

class InitialProjectView(viewsets.ViewSet):
    def retrieve(self, request: Request, pk=None):
        use_case = InitialProjectFetchUseCase(repository=DjangoProjectRepository())
        project = use_case.execute(project_id=pk)

        serializer = InitialProjectSerializer(project)
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(request_body=InitialProjectSerializer, responses={201: InitialProjectSerializer})
    def create(self, request: Request):
        use_case = InitialProjectCreateUseCase(repository=DjangoProjectRepository())

        dto = InitialProjectCreateRequest(
            project_name=request.data.get("name"),
            project_description=request.data.get("description"),
        )

        project_id = use_case.execute(dto)

        return Response({"id": project_id}, status=HTTP_201_CREATED)
