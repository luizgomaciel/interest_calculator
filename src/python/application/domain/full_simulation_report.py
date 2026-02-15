from dataclasses import dataclass
from typing import List

from src.python.application.domain.monthly_summary import MonthlySummary
from src.python.application.domain.year_summary import YearSummary


@dataclass(frozen=True)
class SimulationSummary:
    final_balance: float
    total_invested: float
    total_interest: float
    total_deposits: float
    effective_annual_rate: float


@dataclass(frozen=True)
class FullSimulationReport:
    summary: SimulationSummary
    yearly_evolution: List[YearSummary]
    monthly_evolution: List[MonthlySummary]
