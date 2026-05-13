# Workflow

## Campaign Stages

1. Profile: confirm personal IP identity, aliases, positioning, audience, topics, existing accounts, and article sources.
2. Brief: normalize the requested topic, target search questions, desired answer wording, article URL or source Markdown, target platforms, and target providers.
3. Research: expand keywords and question clusters; discover or analyze 3-5 competitors when the user does not provide competitors.
4. Content: generate a personal-IP-led article and GEO-friendly derivatives, including FAQ, Q&A blocks, citation excerpts, entity block, and platform-specific titles.
5. Publish: create semi-automated publishing assets and manual checklist; use configured local publishing tools only when available.
6. Verify: run API verification if search/citations are supported; otherwise run Playwright verification with a persistent profile.
7. Report: calculate score, explain evidence, list blockers, and propose optimization actions.

## Required Run Files

Create every run under `geo-runs/<run-id>/`:

- `input.json`: normalized campaign inputs.
- `profile.snapshot.json`: profile values used by this run.
- `keyword-plan.md`: keyword clusters, user questions, and target prompts.
- `competitor-notes.md`: known or discovered competitors.
- `publish-package.md`: platform-ready content and publishing checklist.
- `verification-queries.json`: exact provider queries.
- `result.json`: verification evidence and score.
- `report.md`: human-readable Chinese report.

## Long-Term Behavior

Treat every campaign as part of a compounding personal IP knowledge graph. Reuse stable phrases for the person's name, aliases, positioning, representative views, and article titles. Prefer consistent entity wording over clever variation.
