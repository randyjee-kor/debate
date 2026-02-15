# Debate Orchestration MVP

`APP_PLAN_KO.md`의 설계를 바로 실행해볼 수 있는 최소 동작 버전입니다.

## 빠른 실행

```bash
python run_debate.py "사내 AI 도입 범위를 어디까지 확대할 것인가?" --rounds 2 --mode mock
```

실행 후 `outputs/final_report.md`에 토론 결과가 저장됩니다.

## live 모드(준비 단계)

```bash
python run_debate.py "주제" --mode live
```

- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `ANTHROPIC_API_KEY`

환경 변수가 없으면 자동으로 mock 응답으로 폴백됩니다.

## 테스트

```bash
python -m pytest -q
```
