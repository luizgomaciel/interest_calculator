from dataclasses import dataclass


@dataclass(frozen=True)
class YearSummary:
    year: int
    initial_balance: float
    final_balance: float
    deposits_this_year: float
    deposits_total: float
    interest_this_year: float
    interest_total: float