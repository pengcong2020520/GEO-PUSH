#!/usr/bin/env python3
"""Generate a human-readable report from a China GEO run result."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Render China GEO campaign report.")
    parser.add_argument("--run-dir", required=True, help="Run directory.")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    input_data = load_json(run_dir / "input.json")
    result = load_json(run_dir / "result.json")
    profile = load_json(run_dir / "profile.snapshot.json")

    providers = result.get("providers", [])
    provider_lines = []
    for provider in providers:
        provider_lines.append(
            f"| {provider.get('name', '')} | {provider.get('status', '')} | "
            f"{provider.get('mention_score', 0)} | {provider.get('citation_score', 0)} | "
            f"{provider.get('blocker', '')} |"
        )
    if not provider_lines:
        provider_lines.append("| 暂无 | created | 0 | 0 | 尚未验证 |")

    blockers = result.get("blockers", [])
    blocker_text = "\n".join(f"- {item}" for item in blockers) if blockers else "- 暂无"

    report = f"""# GEO投放报告

## 基本信息

- 运行ID：{input_data.get('run_id')}
- 主题：{input_data.get('topic')}
- GEO目标：{input_data.get('geo_goal')}
- 个人IP：{profile.get('name') or '未配置'}
- 文章URL：{', '.join(input_data.get('article_urls', [])) or '未提供'}

## 综合评分

{result.get('score') if result.get('score') is not None else '尚未评分'}

默认评分权重：个人IP出现 35%，文章引用 35%，观点匹配 20%，竞品压制 10%。

## 验证结果

| 入口 | 状态 | 人名得分 | 引用得分 | 阻塞原因 |
| --- | --- | ---: | ---: | --- |
{chr(10).join(provider_lines)}

## 阻塞项

{blocker_text}

## 优化建议

1. 如果未出现人名，强化文章中的稳定实体表达：姓名、别名、领域、定位和代表观点。
2. 如果未引用文章，补充清晰标题、作者块、FAQ、摘要和可独立引用段落。
3. 如果竞品占位明显，围绕其出现的问题补充更直接的长尾问答。
4. 如果验证被阻塞，先补齐 API key 或 Playwright 持久化登录态。
"""
    (run_dir / "report.md").write_text(report, encoding="utf-8")
    print(run_dir / "report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
