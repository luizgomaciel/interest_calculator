from typing import Optional

from rest_framework import serializers

from src.python.application.domain.simulation_result import CompoundingFrequency, Contribution

class InvestmentQuerySerializer(serializers.Serializer):
    principal = serializers.FloatField(required=False, default=0.0)
    annual_rate = serializers.FloatField(required=False, default=0.0)
    total_periods = serializers.IntegerField(required=False, default=0)
    compounding_frequency = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in CompoundingFrequency],
        required=False,
        default=CompoundingFrequency.YEARLY.value
    )
    contribution_amount = serializers.FloatField(required=False, default=0.0)
    contribution_frequency = serializers.ChoiceField(
        choices=[(c.name, c.value) for c in CompoundingFrequency],
        required=False,
        default=CompoundingFrequency.YEARLY.value
    )

class FullSimulationReportSerializer(serializers.Serializer):
    final_balance = serializers.FloatField()
    total_invested = serializers.FloatField()
    total_interest = serializers.FloatField()
    total_deposits = serializers.FloatField()
    effective_annual_rate = serializers.FloatField()

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        def fmt_num(v):
            return f"{v:,.2f}" if v is not None else v

        rep["final_balance"] = fmt_num(rep.get("final_balance"))
        rep["total_invested"] = fmt_num(rep.get("total_invested"))
        rep["total_interest"] = fmt_num(rep.get("total_interest"))
        rep["total_deposits"] = fmt_num(rep.get("total_deposits"))

        rate = rep.get("effective_annual_rate")
        rep["effective_annual_rate"] = f"{rate * 100:.2f}%" if rate is not None else rate

        return rep
