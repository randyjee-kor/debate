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


## GitHub Pages 배포로 결과 확인

이 저장소에는 토론 결과를 정적 페이지로 배포하는 워크플로우가 포함되어 있습니다.

1. GitHub 저장소의 **Settings → Pages**에서 Source를 **GitHub Actions**로 설정합니다.
2. **Actions → Build and Deploy Pages** 워크플로우를 실행합니다.
   - 입력값 `topic`, `rounds`를 원하는 값으로 바꿀 수 있습니다.
3. 완료 후 Actions 로그의 `page_url` 또는 Pages URL에서 결과를 확인합니다.

워크플로우는 내부적으로 다음을 수행합니다.
- `run_debate.py --mode mock`으로 `outputs/final_report.md` 생성
- `scripts/build_pages.py`로 `site/index.html` 생성
- `site/`를 GitHub Pages로 배포
