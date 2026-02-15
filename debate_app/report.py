from __future__ import annotations

from pathlib import Path

from debate_app.schema import DebateOutcome, DebateSession


def to_markdown(session: DebateSession, outcome: DebateOutcome) -> str:
    lines = [
        f"# 토론 리포트: {session.topic}",
        "",
        "## 설정",
        f"- 라운드 수: {session.rules.rounds}",
        f"- 근거 필수: {session.rules.evidence_required}",
        f"- 반박 강도: {session.rules.rebuttal_intensity}",
        "",
        "## 모델 역할",
    ]

    for model, role in session.assignments.items():
        lines.append(f"- {model}: {role}")

    for round_result in outcome.rounds:
        lines.append("")
        lines.append(f"## Round {round_result.round_no}")
        lines.append("")
        lines.append("### Opening")
        for turn in round_result.opening:
            lines.extend(
                [
                    f"- **{turn.model_name}({turn.role})**: {turn.claim}",
                    f"  - evidence: {', '.join(turn.evidence)}",
                    f"  - confidence: {turn.confidence}",
                ]
            )

        lines.append("")
        lines.append("### Rebuttal")
        for turn in round_result.rebuttal:
            lines.extend(
                [
                    f"- **{turn.model_name}({turn.role})**: {turn.claim}",
                    f"  - counter_to: {turn.counter_to}",
                    f"  - weakness: {', '.join(turn.weaknesses)}",
                ]
            )

    lines.extend(
        [
            "",
            "## 자동 점수",
            f"- 논리성: {outcome.score.logic}",
            f"- 근거성: {outcome.score.evidence}",
            f"- 반박 대응력: {outcome.score.rebuttal_response}",
            f"- 실행가능성: {outcome.score.feasibility}",
            f"- 합의도: {outcome.score.consensus}",
            "",
            "## 최종 제안",
            f"1. 공통 합의 결론: {outcome.consensus_conclusion}",
            f"2. 보수적 대안: {outcome.conservative_alternative}",
            "3. 추가 검증 필요 항목:",
        ]
    )
    lines.extend(f"   - {item}" for item in outcome.verification_needed)
    lines.append("")

    return "\n".join(lines)


def write_report(path: str, markdown: str) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
