from __future__ import annotations

import hashlib
import json
import os
from abc import ABC, abstractmethod
from typing import List

from debate_app.schema import Role


class BaseModelClient(ABC):
    model_name: str

    @abstractmethod
    def generate_structured_response(
        self,
        *,
        topic: str,
        role: Role,
        round_no: int,
        phase: str,
        prior_claims: List[str],
    ) -> dict:
        raise NotImplementedError


class MockModelClient(BaseModelClient):
    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate_structured_response(
        self,
        *,
        topic: str,
        role: Role,
        round_no: int,
        phase: str,
        prior_claims: List[str],
    ) -> dict:
        seed = f"{self.model_name}|{topic}|{role}|{round_no}|{phase}"
        digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()
        confidence = (int(digest[:2], 16) / 255) * 0.35 + 0.55

        stance_map = {
            "pro": "채택을 지지",
            "con": "신중한 반대",
            "neutral": "중립적 비교",
            "fact_checker": "검증 우선",
        }
        focus = stance_map.get(role, "균형 검토")

        evidence = [
            f"{topic} 관련 선행사례({self.model_name})",
            f"라운드 {round_no} 위험-편익 분석({focus})",
        ]
        if phase == "rebuttal" and prior_claims:
            counter_to = prior_claims[0][:80]
        else:
            counter_to = ""

        return {
            "claim": f"[{self.model_name}/{role}] {topic}에 대해 {focus} 관점에서 {phase} 의견을 제시합니다.",
            "evidence": evidence,
            "confidence": round(min(confidence, 0.97), 2),
            "counter_to": counter_to,
            "weaknesses": [
                "실증 데이터 표본이 제한적일 수 있음",
                "외부 정책/시장 변화에 민감함",
            ],
        }


class LiveAPINotConfiguredError(RuntimeError):
    pass


class LiveProxyClient(BaseModelClient):
    """Placeholder for real API integration. Uses mock until keys are configured."""

    def __init__(self, model_name: str, env_key: str):
        self.model_name = model_name
        self.env_key = env_key

    def generate_structured_response(
        self,
        *,
        topic: str,
        role: Role,
        round_no: int,
        phase: str,
        prior_claims: List[str],
    ) -> dict:
        if not os.getenv(self.env_key):
            raise LiveAPINotConfiguredError(
                f"{self.model_name} 실API 사용을 위해 {self.env_key} 환경 변수가 필요합니다."
            )

        # Real API integration can be added here. For now, we preserve JSON contract.
        payload = {
            "topic": topic,
            "role": role,
            "round_no": round_no,
            "phase": phase,
            "prior_claims": prior_claims,
        }
        return {
            "claim": f"[{self.model_name}] live mode placeholder: {json.dumps(payload, ensure_ascii=False)}",
            "evidence": ["API 연결 구현 필요"],
            "confidence": 0.5,
            "counter_to": prior_claims[0] if prior_claims else "",
            "weaknesses": ["live connector is not implemented"],
        }
