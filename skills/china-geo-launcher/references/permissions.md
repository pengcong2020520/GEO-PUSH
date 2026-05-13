# Permissions And Configuration

## `.env` Fields

V1 expects a project-level `.env`. Use `.env.example` as the source of available keys.

Minimum useful profile fields:

- `GEO_PERSON_NAME`
- `GEO_PERSON_FIELD`
- `GEO_PERSON_POSITIONING`
- `GEO_TARGET_AUDIENCE`
- `GEO_CORE_TOPICS`

Provider keys are optional. A provider API is useful for GEO verification only when it can perform web search or return citations.

## Playwright Login State

Use a persistent profile directory from `GEO_PLAYWRIGHT_USER_DATA_DIR`. The first live browser verification may require manual login or QR-code scanning. Reuse that profile for later runs.

If a provider requires captcha, fresh login, SMS verification, or blocks automation, mark it as `blocked` and record the blocker. Do not mark the campaign as failed solely because verification was blocked.

## Publishing Permissions

Use configured local skills, CLIs, APIs, or logged-in sessions where available. For unsupported platforms, generate manual publishing instructions and request published URLs from the user.

Never ask the user to place secrets in generated reports. Keep secrets in `.env` or local credential stores.
