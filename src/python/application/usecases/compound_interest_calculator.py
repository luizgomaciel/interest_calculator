from src.python.application.builders.simulation_report_builder import SimulationReportBuilder
from src.python.application.domain.full_simulation_report import FullSimulationReport
from src.python.application.domain.simulation_result import Investment
from src.python.application.service.compound_interest_calculator import CompoundInterestCalculator


class SimulateInvestmentUseCase:

    def execute(self, investment: Investment) -> FullSimulationReport:
        result = CompoundInterestCalculator().simulate(investment, detailed=True)
        report_builder = SimulationReportBuilder(result=result)

        monthly = report_builder.build_monthly_evolution()
        yearly = report_builder.build_yearly_evolution(investment.compounding_frequency)

        summary = report_builder.build_summary(result, investment)

        return FullSimulationReport(
            summary=summary,
            yearly_evolution=yearly,
            monthly_evolution=monthly
        )
