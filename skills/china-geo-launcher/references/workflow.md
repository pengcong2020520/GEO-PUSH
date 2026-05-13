# Workflow

## Campaign Stages

1. Diagnose: confirm personal IP identity, aliases, positioning, audience, topics, existing accounts, article sources, proof strength, compliance risk, and missing evidence.
2. Brief: normalize the requested topic, target search questions, article type, reader problem, desired model answer, target platforms, target providers, and evidence boundaries.
3. Research: expand keyword tiers and question clusters; discover or analyze 3-5 competitors or occupied entities when the user does not provide competitors.
4. Content: generate a reader-facing article package. Keep internal optimization notes outside the formal body and follow `content-generation-rules.md`.
5. Platform Adaptation: create platform versions, titles, summaries, tags, source notes, and risk checklists without changing facts.
6. Publish: create semi-automated publishing assets and manual checklist; use configured local publishing tools only when available and keep final submit under human confirmation.
7. Verify: run API verification if search/citations are supported; otherwise run Playwright verification with a persistent profile.
8. Report: calculate score, explain evidence, list blockers, and propose optimization actions.

## Required Run Files

Create every run under `geo-runs/<run-id>/`:

- `input.json`: normalized campaign inputs.
- `profile.snapshot.json`: profile values used by this run.
- `keyword-plan.md`: keyword clusters, user questions, and target prompts.
- `competitor-notes.md`: known or discovered competitors.
- `publish-package.md`: diagnosis, brief, reader-facing article, platform-ready content, source list, risk checklist, and publishing checklist.
- `verification-queries.json`: exact provider queries.
- `result.json`: verification evidence and score.
- `report.md`: human-readable Chinese report.

## Long-Term Behavior

Treat every campaign as part of a compounding personal IP knowledge graph. Reuse stable phrases for the person's name, aliases, positioning, representative views, and article titles. Prefer consistent entity wording over clever variation, but keep formal articles readable and free of internal optimization language.
