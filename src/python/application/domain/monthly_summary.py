from dataclasses import dataclass


@dataclass(frozen=True)
class MonthlySummary:
    month: int
    initial_balance: float
    final_balance: float
    deposits_this_month: float
    deposits_total: float
    interest_this_month: float
    interest_total: float
