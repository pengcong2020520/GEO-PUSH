# China GEO Launcher Design

## Purpose

Build a Codex skill for China-market GEO campaigns that helps a user make their personal IP searchable and citable in domestic AI search and model-answer surfaces such as Doubao, Kimi, DeepSeek, Tongyi, Wenxin, Tencent Yuanbao, Metaso, and 360 AI Search.

The first release is a semi-automated workflow. It generates and packages content assets for Chinese content platforms, uses available APIs or logged-in browser sessions for verification, and produces a durable report showing whether the target personal IP and article sources appear in model answers.

## Confirmed Scope

The first version supports a single controller skill named `china-geo-launcher`. The user triggers one skill, while detailed workflows and scripts live in `references/` and `scripts/`.

The workflow has six stages:

1. Initialize or update the personal IP profile.
2. Accept a topic, GEO goal, and optional existing article URL or Markdown content.
3. Research keywords, user questions, competitors, and current AI-answer occupants.
4. Generate a long-term content package for Chinese publishing platforms.
5. Prepare semi-automated publishing steps and collect published URLs.
6. Verify domestic model visibility and produce a quality report.

The skill prioritizes existing articles or URLs, but can also draft new content from a topic. It targets a Chinese platform matrix including WeChat Official Account, Zhihu, Xiaohongshu, Juejin, CSDN, Baijiahao, 人人都是产品经理, 少数派, and similar discoverable Chinese content sources.

## Non-Goals For V1

V1 will not promise fully automated publication across all platforms. Many target platforms lack stable public publishing APIs or enforce interactive login and anti-automation controls.

V1 will not treat a blocked login, unavailable API, or captcha as a failed GEO result. These conditions are recorded as verification blockers.

V1 will not maintain full time-series trend analytics. It keeps a lightweight campaign index that can later evolve into trend tracking.

## User Experience

The intended user command is conversational:

> Help me run a China GEO campaign for this topic so Doubao, Kimi, and DeepSeek can find my name and cite this article.

The first run asks for the minimum personal IP fields:

- Name or personal IP label
- Field or expertise area
- One-line positioning
- Target audience
- Target theme to bind with

Optional long-term metadata includes aliases, platform accounts, articles, representative views, cases, credentials, media mentions, prohibited wording, tone, competitors, and methodology.

After initialization, the user should only need to provide the campaign topic, GEO goal, and optional article source.

## Configuration

V1 uses a single `.env` file for simplicity. It can include both sensitive and non-sensitive settings, while `.env.example` documents the available keys.

Expected configuration categories:

- Personal IP fields
- Default verification providers
- API keys where available
- Playwright persistent profile directory
- Platform account hints and publishing mode
- Output directory

Future versions may split non-sensitive config into `profile.yml`, `providers.yml`, and `platforms.yml`.

## Publishing Strategy

Publishing is semi-automated:

- If an existing local skill, CLI, API, or logged-in workflow is available, the skill may create drafts or assist publication.
- If no stable integration exists, the skill generates a platform-ready package and manual publishing checklist.
- Published URLs are required for citation verification. The user may paste URLs back into the run if they cannot be discovered automatically.

The content package includes:

- Core article Markdown
- Platform-specific titles
- Abstracts and hooks
- Tags and keyword clusters
- FAQ and Q&A blocks
- Citation-friendly excerpts
- Personal IP entity block
- Manual publishing checklist
- URL backfill table

## Verification Strategy

Verification is the core of V1.

The default provider list is configurable, with Doubao, Kimi, and DeepSeek as the initial default. Additional providers can include Tongyi, Wenxin, Tencent Yuanbao, Metaso, and 360 AI Search.

Verification order:

1. Use official API if it supports web search or citation collection.
2. Use API only as an auxiliary semantic check if it cannot search the web.
3. Use Playwright CLI/browser automation when API is unavailable or insufficient.
4. Mark provider as blocked if login, captcha, profile, or selector requirements are missing.

Playwright uses a persistent browser profile. The first run may require the user to log in manually; later runs reuse the profile.

The verification checks:

- Whether the answer mentions the target personal IP name or aliases
- Whether the answer cites, links, names, or paraphrases the target article
- Whether the answer reflects the target viewpoints
- Whether competitors appear instead of or above the target personal IP

## Scoring

The default score is 100 points:

- Personal IP mention: 35
- Article citation or source recognition: 35
- Target viewpoint match: 20
- Competitor suppression or comparative strength: 10

The report should explain the score in plain Chinese and list concrete optimization actions. Missing configuration or blocked verification is reported separately from poor GEO performance.

## Data Model

Each run writes to a timestamped directory under `geo-runs/`:

- `input.json`: normalized user input
- `profile.snapshot.json`: personal IP metadata used for the run
- `keyword-plan.md`: keyword and query plan
- `competitor-notes.md`: competitor discovery and analysis notes
- `publish-package.md`: multi-platform publishing package
- `verification-queries.json`: prompts and search questions
- `result.json`: machine-readable verification results and score
- `report.md`: human-readable Chinese report

The project also keeps `geo-runs/index.json` with a lightweight history:

- Run ID
- Topic
- Article URLs
- Providers tested
- Mention and citation status
- Score
- Report path

## Skill Structure

The skill folder is:

```text
skills/china-geo-launcher/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── workflow.md
│   ├── permissions.md
│   ├── platform-matrix.md
│   ├── verification.md
│   └── scoring.md
└── scripts/
    ├── geo_init.py
    ├── geo_launch.py
    ├── geo_report.py
    └── geo_playwright_verify.py
```

`SKILL.md` stays concise and tells Codex how to orchestrate the workflow. Detailed platform and verification logic lives in references. Scripts provide deterministic file generation and reporting primitives.

## Validation Plan

V1 validation includes:

- Run skill validation against `SKILL.md`.
- Run `geo_init.py --check` to confirm `.env` handling.
- Run `geo_launch.py` with a sample topic and article URL to create a run directory.
- Run `geo_report.py` against the sample run.
- Run `geo_playwright_verify.py --dry-run` to confirm Playwright command generation without requiring login.

Live provider verification requires API keys or a persistent browser profile and should be tested only after user configuration.

## Open Extension Points

Future work can add:

- Real API adapters for each domestic model/search provider
- Platform-specific publishing adapters
- Browser selectors and Playwright tests per provider
- Automatic URL discovery after publication
- Historical trend scoring
- Competitor share-of-answer tracking
- Dashboard or spreadsheet export
