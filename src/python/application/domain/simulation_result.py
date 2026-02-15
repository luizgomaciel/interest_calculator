from dataclasses import dataclass
from enum import Enum
from typing import Optional, List


class CompoundingFrequency(Enum):
    DAILY = 365
    MONTHLY = 12
    YEARLY = 1


@dataclass(frozen=True)
class Contribution:
    amount: float
    frequency: CompoundingFrequency


@dataclass(frozen=True)
class Investment:
    principal: float
    annual_rate: float
    total_periods: int
    compounding_frequency: CompoundingFrequency
    contribution: Optional[Contribution] = None


@dataclass(frozen=True)
class PeriodDetail:
    period: int
    balance: float
    interest_earned: float
    contribution: float


@dataclass(frozen=True)
class SimulationResult:
    final_amount: float
    total_invested: float
    total_interest: float
    period_details: Optional[List[PeriodDetail]] = None
