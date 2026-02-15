# AI 다자 토론 조율 앱 설계안

## 1) 목표
사용자가 **주체(사회자)**가 되어 특정 주제에 대해 여러 LLM(예: ChatGPT, Gemini, Claude)을 토론시키고,
핵심 쟁점을 정리·검증해 **최적 결론**을 도출하도록 돕는 앱을 만든다.

---

## 2) 핵심 사용자 흐름 (MVP)
1. 사용자가 토론 주제 입력
2. 토론 규칙 선택 (라운드 수, 근거 필수 여부, 반박 강도)
3. 각 모델에게 역할 부여 (찬성/반대/중립/팩트체커)
4. 라운드별 주장 → 반박 → 재반박 진행
5. 앱이 합의점/충돌점/근거 신뢰도를 자동 요약
6. 사용자가 최종 결론안 선택 또는 수정
7. 최종 리포트(PDF/Markdown)로 저장

---

## 3) 시스템 아키텍처
- **Frontend**: Next.js + Tailwind
- **Backend API**: FastAPI 또는 Next.js Route Handlers
- **Orchestrator**: 모델 호출 순서/토론 상태/룰 엔진 관리
- **Model Connectors**:
  - OpenAI API
  - Google Gemini API
  - Anthropic Claude API
- **Data Store**: PostgreSQL (세션, 라운드, 메시지, 점수)
- **Optional**: 벡터DB(근거 문서 검색용)

### 핵심 모듈
- Debate Session Manager
- Prompt Policy Engine
- Evidence Verifier
- Consensus Scorer
- Report Generator

---

## 4) 프롬프트 전략 (중요)
각 모델에 동일 질문을 던지면 품질이 고르지 않으므로, 아래처럼 역할 기반 프롬프트를 사용:

- **역할 프롬프트**: "당신은 엄격한 반대 토론자"
- **출력 형식 강제**: JSON 스키마(주장, 근거, 불확실성)
- **근거 의무화**: 출처 없는 단정은 감점
- **자기점검 단계**: "당신 주장 중 가장 취약한 지점 2개"

예시 구조:
```json
{
  "claim": "핵심 주장",
  "evidence": ["근거1", "근거2"],
  "confidence": 0.0,
  "counter_to": "반박 대상",
  "weaknesses": ["약점1", "약점2"]
}
```

---

## 5) 결론 품질을 올리는 평가 프레임
앱에서 라운드 종료 후 자동 채점:

- **논리성**: 전제→결론의 일관성
- **근거성**: 출처/재현 가능성
- **반박 대응력**: 반론 수용 및 수정 여부
- **실행가능성**: 실제 적용 비용/리스크
- **합의도**: 모델 간 공통 분모 비율

최종 결론은 단일 문장이 아니라 아래 3단 구조로 추천:
1. 공통 합의 결론
2. 쟁점이 남은 보수적 대안
3. 추가 검증이 필요한 항목

---

## 6) 데이터 모델 (초안)
- `debate_sessions(id, topic, owner_id, rules_json, created_at)`
- `debate_rounds(id, session_id, round_no, started_at, ended_at)`
- `model_messages(id, round_id, model_name, role, content_json, score_json)`
- `final_reports(id, session_id, conclusion_md, export_url)`

---

## 7) MVP 구현 순서 (2주 스프린트 기준)
### Week 1
- 토론 세션 생성 UI
- 3개 모델 API 연결
- 1라운드 주장/반박 파이프라인
- 라운드 로그 저장

### Week 2
- 자동 요약/점수화
- 최종 결론 생성기
- 리포트 export
- 간단한 비용 대시보드(모델 호출 토큰)

---

## 8) 운영 시 주의사항
- 모델 환각(hallucination) 대응: "확실하지 않음" 필드 필수
- 민감 주제 정책: 금지 카테고리 및 안전 필터 적용
- 비용 통제: 토큰 상한/라운드 제한/캐시
- 감사 로그: 어떤 프롬프트와 응답으로 결론이 났는지 추적 가능하게 저장

---

## 9) 바로 시작 가능한 기술 스택 추천
- Next.js + TypeScript
- FastAPI(or Next API)
- PostgreSQL + Prisma(or SQLModel)
- Vercel/Render 배포
- Sentry + OpenTelemetry 모니터링

---

## 10) 다음 단계 제안
1. 우선 토론 주제 3개를 정해 MVP로 품질 측정
2. "역할 프롬프트 템플릿"부터 고정
3. 모델별 강점 맵핑(창의성/정확성/보수성)
4. 결론 채택 UI(사용자 최종 승인) 구현

이 순서대로 가면 "단순 챗봇"이 아니라 **의견 조율 엔진**으로 차별화할 수 있다.
