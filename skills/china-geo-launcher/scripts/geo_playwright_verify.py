#!/usr/bin/env python3
"""Prepare Playwright-based verification artifacts for a China GEO run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare Playwright verification for a China GEO run.")
    parser.add_argument("--run-dir", required=True, help="Run directory.")
    parser.add_argument("--user-data-dir", default=".playwright-profile", help="Persistent Playwright profile directory.")
    parser.add_argument("--dry-run", action="store_true", help="Only write verification plan and commands.")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    queries = json.loads((run_dir / "verification-queries.json").read_text(encoding="utf-8"))
    playwright_dir = run_dir / "playwright"
    playwright_dir.mkdir(exist_ok=True)

    plan = {
        "mode": "dry-run" if args.dry_run else "manual-live-required",
        "user_data_dir": args.user_data_dir,
        "queries": queries.get("queries", []),
        "commands": [
            f"npx playwright open --user-data-dir={args.user_data_dir} https://www.doubao.com/",
            f"npx playwright open --user-data-dir={args.user_data_dir} https://kimi.moonshot.cn/",
            f"npx playwright open --user-data-dir={args.user_data_dir} https://chat.deepseek.com/",
        ],
        "notes": [
            "Use persistent profile login once, then reuse it.",
            "Record answer text, mention evidence, citation URLs, competitors, and blockers.",
            "Do not bypass captchas or platform controls.",
        ],
    }
    (playwright_dir / "verification-plan.json").write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    (playwright_dir / "manual-results.json").write_text(
        json.dumps(
            {
                "providers": [
                    {
                        "name": "doubao",
                        "method": "playwright",
                        "status": "blocked",
                        "answer_excerpt": "",
                        "mentioned_names": [],
                        "citation_urls": [],
                        "competitors": [],
                        "blocker": "not_run",
                    },
                    {
                        "name": "kimi",
                        "method": "playwright",
                        "status": "blocked",
                        "answer_excerpt": "",
                        "mentioned_names": [],
                        "citation_urls": [],
                        "competitors": [],
                        "blocker": "not_run",
                    },
                    {
                        "name": "deepseek",
                        "method": "playwright",
                        "status": "blocked",
                        "answer_excerpt": "",
                        "mentioned_names": [],
                        "citation_urls": [],
                        "competitors": [],
                        "blocker": "not_run",
                    },
                ]
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(playwright_dir / "verification-plan.json")
    if args.dry_run:
        for command in plan["commands"]:
            print(command)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
