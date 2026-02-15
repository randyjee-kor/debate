from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal

Role = Literal["pro", "con", "neutral", "fact_checker"]


@dataclass
class DebateRule:
    rounds: int = 2
    evidence_required: bool = True
    rebuttal_intensity: int = 2  # 1~3


@dataclass
class ModelTurn:
    model_name: str
    role: Role
    claim: str
    evidence: List[str]
    confidence: float
    counter_to: str
    weaknesses: List[str]


@dataclass
class RoundResult:
    round_no: int
    opening: List[ModelTurn] = field(default_factory=list)
    rebuttal: List[ModelTurn] = field(default_factory=list)


@dataclass
class DebateSession:
    topic: str
    rules: DebateRule
    assignments: Dict[str, Role]


@dataclass
class ScoreResult:
    logic: float
    evidence: float
    rebuttal_response: float
    feasibility: float
    consensus: float


@dataclass
class DebateOutcome:
    rounds: List[RoundResult]
    score: ScoreResult
    consensus_conclusion: str
    conservative_alternative: str
    verification_needed: List[str]
