# python
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import action

from src.python.application.domain.simulation_result import Investment, CompoundingFrequency, Contribution
from src.python.application.usecases.compound_interest_calculator import SimulateInvestmentUseCase
from src.python.django_project.calculator.serializers import (
    FullSimulationReportSerializer,
    InvestmentQuerySerializer,
)


class CalculatorView(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='simulate')
    @swagger_auto_schema(query_serializer=InvestmentQuerySerializer, responses={200: FullSimulationReportSerializer})
    def fetch(self, request: Request):
        q_serializer = InvestmentQuerySerializer(data=request.query_params)
        q_serializer.is_valid(raise_exception=True)
        q = q_serializer.validated_data

        compounding_frequency = CompoundingFrequency(q.get("compounding_frequency", CompoundingFrequency.YEARLY.value))

        contribution_amount = float(q.get("contribution_amount", 0))
        contribution = None
        if contribution_amount:
            contribution = Contribution(
                amount=contribution_amount,
                frequency=CompoundingFrequency(q.get("contribution_frequency", CompoundingFrequency.YEARLY.value))
            )

        investment = Investment(
            principal=float(q.get("principal", 0)),
            annual_rate=float(q.get("annual_rate", 0)),
            total_periods=int(q.get("total_periods", 0)),
            compounding_frequency=compounding_frequency,
            contribution=contribution
        )

        full_simulation_report = SimulateInvestmentUseCase().execute(investment=investment)

        serializer = FullSimulationReportSerializer(full_simulation_report.summary)
        return Response(serializer.data, status=HTTP_200_OK)
