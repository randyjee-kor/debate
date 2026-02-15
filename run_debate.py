#!/usr/bin/env python3
from __future__ import annotations

import argparse

from debate_app.clients import LiveProxyClient, MockModelClient
from debate_app.orchestrator import DebateOrchestrator
from debate_app.report import to_markdown, write_report
from debate_app.schema import DebateRule, DebateSession


def build_clients(mode: str):
    if mode == "live":
        return {
            "chatgpt": LiveProxyClient("chatgpt", "OPENAI_API_KEY"),
            "gemini": LiveProxyClient("gemini", "GEMINI_API_KEY"),
            "claude": LiveProxyClient("claude", "ANTHROPIC_API_KEY"),
        }
    return {
        "chatgpt": MockModelClient("chatgpt"),
        "gemini": MockModelClient("gemini"),
        "claude": MockModelClient("claude"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="AI 다자 토론 조율 MVP 실행기")
    parser.add_argument("topic", help="토론 주제")
    parser.add_argument("--rounds", type=int, default=2)
    parser.add_argument("--mode", choices=["mock", "live"], default="mock")
    parser.add_argument("--out", default="outputs/final_report.md")
    args = parser.parse_args()

    session = DebateSession(
        topic=args.topic,
        rules=DebateRule(rounds=args.rounds, evidence_required=True, rebuttal_intensity=2),
        assignments={
            "chatgpt": "pro",
            "gemini": "con",
            "claude": "fact_checker",
        },
    )

    orchestrator = DebateOrchestrator(build_clients(args.mode))
    outcome = orchestrator.run(session)
    md = to_markdown(session, outcome)
    write_report(args.out, md)

    print(f"토론 완료: {args.topic}")
    print(f"리포트 저장: {args.out}")


if __name__ == "__main__":
    main()
