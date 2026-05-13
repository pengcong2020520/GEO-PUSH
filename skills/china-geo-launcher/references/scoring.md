# Scoring

## Default Weights

Score each campaign out of 100:

- Personal IP mention: 35
- Article citation or source recognition: 35
- Target viewpoint match: 20
- Competitor suppression or comparative strength: 10

## Status Interpretation

- `passed`: strong evidence that the target name or article appears.
- `weak`: partial match, paraphrase, missing link, or uncertain attribution.
- `failed`: provider answered but did not mention the target name or article.
- `blocked`: verification could not run because of login, captcha, missing key, unsupported mode, selector failure, or network issue.

Blocked providers should reduce confidence, not the GEO score itself.

## Optimization Guidance

When the name is missing, strengthen stable entity wording: name, aliases, field, positioning, and repeated topic binding.

When the article is not cited, improve source clarity: title, author block, summary, FAQ, publish on more discoverable platforms, and request indexed/crawlable URLs.

When viewpoints are not reflected, add direct answer blocks, definitions, examples, and explicit "my method" phrasing.

When competitors dominate, compare against their occupied queries and publish assets that answer missing long-tail questions.
