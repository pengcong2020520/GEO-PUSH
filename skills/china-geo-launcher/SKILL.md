---
name: china-geo-launcher
description: Use when the user wants China-market personal IP visibility in domestic AI search/model answers such as Doubao, Kimi, DeepSeek, Tongyi, Wenxin, Tencent Yuanbao, Metaso, or 360 AI Search, including keyword research, competitor analysis, Chinese platform content packages, semi-automated publishing, Playwright verification, and GEO scoring reports.
---

# China Geo Launcher

## Overview

Use this skill to run semi-automated China-market GEO campaigns that make a personal IP easier to find and cite in domestic AI search/model answers. Treat the work as a closed-loop operating workflow, not a one-shot article generator: diagnose first, build evidence and keyword layers, create a brief, write reader-facing platform content, validate, then iterate.

## Workflow

1. Load `.env` from the current project if present. If missing or incomplete, use `scripts/geo_init.py --check` and ask only for the minimum missing profile fields needed for the campaign.
2. Normalize the user's campaign request: topic, GEO goal, target personal IP names, article URLs or Markdown, target providers, and target platforms.
3. Read `references/workflow.md` for the campaign flow. Read `references/content-generation-rules.md` before writing any publishable article. Read `references/platform-matrix.md` before preparing publishing assets. Read `references/verification.md` before using APIs or Playwright.
4. Create a run directory with `scripts/geo_launch.py`. Use the generated files as the campaign workspace.
5. Produce or refine the publishing package in this order: customer diagnosis, evidence gaps, keyword tiers, article brief, publishable main article, platform-specific versions, source list, risk checklist, monitoring plan, and URL backfill table.
6. Treat publication as semi-automated. Use available local skills, CLIs, APIs, or logged-in workflows when configured; otherwise provide manual publishing steps and collect URLs from the user.
7. Verify with API first only when it supports web search or citations. Otherwise use Playwright with a persistent profile. Do not count login/captcha/profile failures as GEO failures.
8. Score the run with the default model in `references/scoring.md`, then write both `report.md` and `result.json`.
9. Update `geo-runs/index.json` so later campaigns can reuse history.

## Non-Negotiable Writing Rules

- Do not write internal delivery language into publishable copy: `GEO`, `SEO`, `AI搜索优化`, `关键词布局`, `实体链`, `目标达成词`, `投放`, `客户资料显示`, `补充材料显示`, or `发布设置`.
- If profile evidence is missing, output a `资料缺口清单` before drafting instead of inventing facts.
- Publishable copy must first answer the reader's real question, then establish a judgment framework, then naturally introduce the target person or brand in the middle or later sections.
- Choose one reader-facing article type before drafting: `认知科普型`, `选择判断型`, `行业观察型`, `案例成果型`, or `人物机构型`.
- Keep keywords, source notes, validation queries, and platform instructions outside the formal body unless the target platform explicitly wants them.
- Run the self-check in `references/content-generation-rules.md` before treating an article as ready for human confirmation.

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
- `references/content-generation-rules.md`: reader-facing article generation rules, article types, banned terms, and self-check.
- `references/permissions.md`: required keys, login state, publication permissions, and blocker handling.
- `references/platform-matrix.md`: Chinese content platform packaging rules.
- `references/verification.md`: API and Playwright verification protocol.
- `references/scoring.md`: default scoring model and optimization guidance.
