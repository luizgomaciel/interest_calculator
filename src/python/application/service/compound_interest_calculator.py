from src.python.application.domain.simulation_result import SimulationResult, CompoundingFrequency, Investment, \
    PeriodDetail


def _convert_annual_rate_to_period_rate(annual_rate: float, frequency: CompoundingFrequency) -> float:
    periods_per_year = frequency.value
    return annual_rate / periods_per_year


class CompoundInterestCalculator:
    def simulate(self, investment: Investment, detailed: bool = False) -> SimulationResult:
        period_rate = _convert_annual_rate_to_period_rate(
            investment.annual_rate,
            investment.compounding_frequency
        )

        balance = investment.principal
        total_invested = investment.principal
        period_details = []

        for period in range(1, investment.total_periods + 1):

            contribution_amount = 0.0
            if investment.contribution:
                if investment.contribution.frequency == investment.compounding_frequency:
                    contribution_amount = investment.contribution.amount
                    balance += contribution_amount
                    total_invested += contribution_amount

            interest = balance * period_rate
            balance += interest

            if detailed:
                period_details.append(
                    PeriodDetail(
                        period=period,
                        balance=balance,
                        interest_earned=interest,
                        contribution=contribution_amount
                    )
                )

        total_interest = balance - total_invested

        return SimulationResult(
            final_amount=balance,
            total_invested=total_invested,
            total_interest=total_interest,
            period_details=period_details if detailed else None
        )