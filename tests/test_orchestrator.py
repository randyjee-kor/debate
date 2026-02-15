from debate_app.clients import MockModelClient
from debate_app.orchestrator import DebateOrchestrator
from debate_app.schema import DebateRule, DebateSession


def test_orchestrator_runs_rounds_and_scores():
    session = DebateSession(
        topic="원격근무 확대",
        rules=DebateRule(rounds=2),
        assignments={"chatgpt": "pro", "gemini": "con", "claude": "fact_checker"},
    )
    clients = {
        "chatgpt": MockModelClient("chatgpt"),
        "gemini": MockModelClient("gemini"),
        "claude": MockModelClient("claude"),
    }
    result = DebateOrchestrator(clients).run(session)

    assert len(result.rounds) == 2
    assert result.score.logic >= 0
    assert result.consensus_conclusion
