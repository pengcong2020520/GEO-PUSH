---
name: china-geo-launcher
description: Run China-market GEO campaigns for personal IP visibility. Use when the user wants domestic AI search/model answers such as Doubao, Kimi, DeepSeek, Tongyi, Wenxin, Tencent Yuanbao, Metaso, or 360 AI Search to find their name, cite their articles, analyze competitors, generate Chinese platform publishing packages, semi-automate publication, verify results with APIs or Playwright, and produce GEO scoring reports.
---

# China Geo Launcher

## Overview

Use this skill to run semi-automated China-market GEO campaigns that make a personal IP easier to find and cite in domestic AI search/model answers. Prioritize verifiable outcomes: whether target providers mention the person and cite the target article.

## Workflow

1. Load `.env` from the current project if present. If missing or incomplete, use `scripts/geo_init.py --check` and ask only for the minimum missing profile fields needed for the campaign.
2. Normalize the user's campaign request: topic, GEO goal, target personal IP names, article URLs or Markdown, target providers, and target platforms.
3. Read `references/workflow.md` for the campaign flow. Read `references/platform-matrix.md` before preparing publishing assets. Read `references/verification.md` before using APIs or Playwright.
4. Create a run directory with `scripts/geo_launch.py`. Use the generated files as the campaign workspace.
5. Produce or refine the publishing package: main article, platform-specific titles, summaries, tags, FAQ, Q&A blocks, citation-friendly excerpts, and URL backfill table.
6. Treat publication as semi-automated. Use available local skills, CLIs, APIs, or logged-in workflows when configured; otherwise provide manual publishing steps and collect URLs from the user.
7. Verify with API first only when it supports web search or citations. Otherwise use Playwright with a persistent profile. Do not count login/captcha/profile failures as GEO failures.
8. Score the run with the default model in `references/scoring.md`, then write both `report.md` and `result.json`.
9. Update `geo-runs/index.json` so later campaigns can reuse history.

## Verification Rules

Make verification evidence-driven. For each provider, record the exact query, timestamp, method, answer text excerpt, mentioned names, citation URLs, competitors, status, and blocker if any.

Use these statuses:

- `passed`: target personal IP or article was found.
- `weak`: partial mention, weak citation, or unclear source attribution.
- `failed`: provider responded but did not mention the target or article.
- `blocked`: login, captcha, missing key, selector failure, network issue, or unsupported search/citation mode.

## Script Quick Start

Run these from the project root:

```bash
python3 skills/china-geo-launcher/scripts/geo_init.py --check
python3 skills/china-geo-launcher/scripts/geo_launch.py --topic "AI 产品经理个人IP" --article-url "https://example.com/article"
python3 skills/china-geo-launcher/scripts/geo_playwright_verify.py --run-dir geo-runs/<run-id> --dry-run
python3 skills/china-geo-launcher/scripts/geo_report.py --run-dir geo-runs/<run-id>
```

The scripts are V1 scaffolding. They create stable campaign files, templates, JSON outputs, and Playwright verification plans. Add provider-specific API and browser adapters incrementally.

## References

- `references/workflow.md`: end-to-end campaign stages and expected files.
- `references/permissions.md`: required keys, login state, publication permissions, and blocker handling.
- `references/platform-matrix.md`: Chinese content platform packaging rules.
- `references/verification.md`: API and Playwright verification protocol.
- `references/scoring.md`: default scoring model and optimization guidance.
