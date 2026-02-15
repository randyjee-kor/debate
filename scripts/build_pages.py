#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build GitHub Pages artifacts from markdown report")
    parser.add_argument("--report", default="outputs/final_report.md")
    parser.add_argument("--site-dir", default="site")
    args = parser.parse_args()

    report_path = Path(args.report)
    site_dir = Path(args.site_dir)
    site_dir.mkdir(parents=True, exist_ok=True)

    report_text = report_path.read_text(encoding="utf-8") if report_path.exists() else "리포트가 없습니다."
    (site_dir / "final_report.md").write_text(report_text, encoding="utf-8")

    title = report_text.splitlines()[0].lstrip("# ") if report_text else "Debate Report"

    html_doc = f"""<!doctype html>
<html lang=\"ko\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 2rem; line-height: 1.5; }}
    .actions {{ margin-bottom: 1rem; }}
    .btn {{ display: inline-block; padding: 0.5rem 0.8rem; border-radius: 8px; border: 1px solid #ddd; text-decoration: none; color: #111; }}
    pre {{ white-space: pre-wrap; background: #fafafa; border: 1px solid #eee; border-radius: 10px; padding: 1rem; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <p>이 페이지는 GitHub Actions가 생성한 토론 결과입니다.</p>
  <div class=\"actions\">
    <a class=\"btn\" href=\"./final_report.md\">마크다운 원본 다운로드</a>
  </div>
  <pre>{html.escape(report_text)}</pre>
</body>
</html>
"""
    (site_dir / "index.html").write_text(html_doc, encoding="utf-8")


if __name__ == "__main__":
    main()
