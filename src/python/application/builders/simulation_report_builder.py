from typing import List

from src.python.application.domain.full_simulation_report import SimulationSummary
from src.python.application.domain.monthly_summary import MonthlySummary
from src.python.application.domain.simulation_result import SimulationResult, CompoundingFrequency, Investment
from src.python.application.domain.year_summary import YearSummary


class SimulationReportBuilder:
    def __init__(self, result: SimulationResult) -> None:
        self.result = result

    def build_monthly_evolution(self) -> List[MonthlySummary]:

        if not self.result.period_details:
            raise ValueError("Detailed simulation required")

        monthly = []
        accumulated_interest = 0.0
        accumulated_deposits = 0.0
        previous_balance = 0.0

        for detail in self.result.period_details:
            initial_balance = previous_balance
            final_balance = detail.balance

            accumulated_interest += detail.interest_earned
            accumulated_deposits += detail.contribution

            monthly.append(
                MonthlySummary(
                    month=detail.period,
                    initial_balance=initial_balance,
                    final_balance=final_balance,
                    deposits_this_month=detail.contribution,
                    deposits_total=accumulated_deposits,
                    interest_this_month=detail.interest_earned,
                    interest_total=accumulated_interest
                )
            )

            previous_balance = final_balance

        return monthly

    def build_yearly_evolution(self, frequency: CompoundingFrequency) -> List[YearSummary]:

        if not self.result.period_details:
            raise ValueError("Detailed simulation required")

        periods_per_year = frequency.value

        years = []
        accumulated_interest = 0.0
        accumulated_deposits = 0.0

        for year_index in range(0, len(self.result.period_details), periods_per_year):

            year_periods = self.result.period_details[
                year_index: year_index + periods_per_year
            ]

            if not year_periods:
                continue

            initial_balance = (
                self.result.period_details[year_index - 1].balance
                if year_index > 0 else 0.0
            )

            final_balance = year_periods[-1].balance

            interest_this_year = sum(p.interest_earned for p in year_periods)
            deposits_this_year = sum(p.contribution for p in year_periods)

            accumulated_interest += interest_this_year
            accumulated_deposits += deposits_this_year

            years.append(
                YearSummary(
                    year=len(years) + 1,
                    initial_balance=initial_balance,
                    final_balance=final_balance,
                    deposits_this_year=deposits_this_year,
                    deposits_total=accumulated_deposits,
                    interest_this_year=interest_this_year,
                    interest_total=accumulated_interest
                )
            )

        return years

    def build_summary(self, result: SimulationResult, investment: Investment) -> SimulationSummary:

        total_deposits = result.total_invested - investment.principal

        years = (investment.total_periods /investment.compounding_frequency.value)

        if result.total_invested > 0:
            effective_annual_rate = (
                                            (result.final_amount / result.total_invested) ** (1 / years)
                                    ) - 1
        else:
            effective_annual_rate = 0.0

        return SimulationSummary(
            final_balance=result.final_amount,
            total_invested=result.total_invested,
            total_interest=result.total_interest,
            total_deposits=total_deposits,
            effective_annual_rate=effective_annual_rate
        )
