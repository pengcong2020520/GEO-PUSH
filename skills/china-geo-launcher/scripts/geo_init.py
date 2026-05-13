#!/usr/bin/env python3
"""Initialize and check China GEO Launcher configuration."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_KEYS = [
    "GEO_PERSON_NAME",
    "GEO_PERSON_FIELD",
    "GEO_PERSON_POSITIONING",
    "GEO_TARGET_AUDIENCE",
    "GEO_CORE_TOPICS",
]


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description="Check or initialize .env for China GEO Launcher.")
    parser.add_argument("--env", default=".env", help="Path to .env file.")
    parser.add_argument("--example", default=".env.example", help="Path to .env.example.")
    parser.add_argument("--check", action="store_true", help="Only check current configuration.")
    parser.add_argument("--create", action="store_true", help="Create .env from .env.example if missing.")
    args = parser.parse_args()

    env_path = Path(args.env)
    example_path = Path(args.example)

    if args.create and not env_path.exists():
        if not example_path.exists():
            print(f"Missing example file: {example_path}")
            return 2
        env_path.write_text(example_path.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Created {env_path} from {example_path}")

    values = parse_env(env_path)
    missing = [key for key in REQUIRED_KEYS if not values.get(key)]

    print(f"Config file: {env_path}")
    print(f"Exists: {env_path.exists()}")
    if missing:
        print("Missing required profile keys:")
        for key in missing:
            print(f"- {key}")
        return 1 if args.check else 0

    print("Minimum personal IP profile is configured.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
