# Verification Protocol

## Provider Order

Default providers are `doubao`, `kimi`, and `deepseek`. The list is configurable through `.env`.

For each provider:

1. Check whether a configured API supports web search and citation output.
2. If yes, use the API and record raw evidence.
3. If API lacks search/citations, use it only for auxiliary viewpoint matching.
4. Use Playwright browser verification for live search/model answer surfaces.
5. If login, captcha, profile, selector, or network requirements block verification, set status to `blocked`.

## Query Design

Use 5-8 queries per campaign:

- Broad topic query.
- Topic + personal IP name.
- Topic + article title.
- Problem-oriented query the target audience would ask.
- Comparison query involving known competitors.
- Methodology or viewpoint query.
- Long-tail citation query asking for sources.

## Evidence To Capture

For every query, record:

- Provider
- Method: `api`, `playwright`, or `manual`
- Query
- Timestamp
- Status
- Answer excerpt
- Mentioned target names
- Citation URLs or article titles
- Competitors mentioned
- Screenshot path if browser verification ran
- Blocker, if any

## Playwright CLI Strategy

Use Playwright with a persistent user data directory. Generate or run provider-specific scripts only after selectors and login state are confirmed.

Recommended dry-run command generation:

```bash
python3 skills/china-geo-launcher/scripts/geo_playwright_verify.py --run-dir geo-runs/<run-id> --dry-run
```

Live verification should be provider-specific and conservative. Avoid bypassing platform controls. Ask the user to log in manually when needed.
