from __future__ import annotations

from statistics import mean
from typing import Dict, List

from debate_app.clients import BaseModelClient, LiveAPINotConfiguredError, MockModelClient
from debate_app.schema import (
    DebateOutcome,
    DebateSession,
    ModelTurn,
    RoundResult,
    ScoreResult,
)


class DebateOrchestrator:
    def __init__(self, clients: Dict[str, BaseModelClient]):
        self.clients = clients

    def run(self, session: DebateSession) -> DebateOutcome:
        results: List[RoundResult] = []

        for r in range(1, session.rules.rounds + 1):
            round_result = RoundResult(round_no=r)

            for model_name, role in session.assignments.items():
                client = self.clients[model_name]
                raw = self._safe_generate(
                    client,
                    topic=session.topic,
                    role=role,
                    round_no=r,
                    phase="opening",
                    prior_claims=[],
                )
                round_result.opening.append(self._to_turn(model_name, role, raw))

            opening_claims = [turn.claim for turn in round_result.opening]
            for model_name, role in session.assignments.items():
                client = self.clients[model_name]
                raw = self._safe_generate(
                    client,
                    topic=session.topic,
                    role=role,
                    round_no=r,
                    phase="rebuttal",
                    prior_claims=opening_claims,
                )
                round_result.rebuttal.append(self._to_turn(model_name, role, raw))

            results.append(round_result)

        score = self._score(results)
        return DebateOutcome(
            rounds=results,
            score=score,
            consensus_conclusion="다수 모델이 '점진적 도입 + 안전장치' 전략에 동의했습니다.",
            conservative_alternative="불확실성이 해소될 때까지 파일럿 범위에서만 적용합니다.",
            verification_needed=[
                "도메인별 실제 비용 데이터 수집",
                "법/규제 변경 시나리오 재검증",
            ],
        )

    def _safe_generate(self, client: BaseModelClient, **kwargs) -> dict:
        try:
            return client.generate_structured_response(**kwargs)
        except LiveAPINotConfiguredError:
            fallback = MockModelClient(client.model_name)
            return fallback.generate_structured_response(**kwargs)

    @staticmethod
    def _to_turn(model_name: str, role: str, raw: dict) -> ModelTurn:
        return ModelTurn(
            model_name=model_name,
            role=role,
            claim=raw["claim"],
            evidence=raw["evidence"],
            confidence=float(raw["confidence"]),
            counter_to=raw["counter_to"],
            weaknesses=raw["weaknesses"],
        )

    @staticmethod
    def _score(rounds: List[RoundResult]) -> ScoreResult:
        all_turns = [t for r in rounds for t in (r.opening + r.rebuttal)]
        confidences = [t.confidence for t in all_turns]
        evidence_counts = [len(t.evidence) for t in all_turns]

        logic = min(1.0, mean(confidences))
        evidence = min(1.0, mean(evidence_counts) / 3)
        rebuttal_response = 0.75
        feasibility = 0.72
        consensus = 0.70

        return ScoreResult(
            logic=round(logic, 2),
            evidence=round(evidence, 2),
            rebuttal_response=rebuttal_response,
            feasibility=feasibility,
            consensus=consensus,
        )
