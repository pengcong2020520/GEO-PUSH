#!/usr/bin/env python3
"""Create a China GEO campaign run directory with starter artifacts."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path


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


def slugify(text: str) -> str:
    lowered = text.lower()
    slug = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", lowered).strip("-")
    return slug[:48] or "campaign"


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a China GEO campaign run.")
    parser.add_argument("--topic", required=True, help="Campaign topic.")
    parser.add_argument("--geo-goal", default="让国产模型搜索结果出现个人IP姓名并引用目标文章", help="GEO goal.")
    parser.add_argument("--article-url", action="append", default=[], help="Target article URL. Can be repeated.")
    parser.add_argument("--article-title", default="", help="Target article title.")
    parser.add_argument("--providers", default="", help="Comma-separated providers. Defaults to .env.")
    parser.add_argument("--platforms", default="", help="Comma-separated platforms. Defaults to .env.")
    parser.add_argument("--env", default=".env", help="Path to .env.")
    args = parser.parse_args()

    env = parse_env(Path(args.env))
    output_dir = Path(env.get("GEO_OUTPUT_DIR", "geo-runs"))
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_id = f"{timestamp}-{slugify(args.topic)}"
    run_dir = output_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    providers = args.providers or env.get("GEO_DEFAULT_PROVIDERS", "doubao,kimi,deepseek")
    platforms = args.platforms or env.get(
        "GEO_DEFAULT_PLATFORMS",
        "wechat,zhihu,xiaohongshu,juejin,csdn,baijiahao,woshipm,sspai",
    )

    profile = {
        "name": env.get("GEO_PERSON_NAME", ""),
        "aliases": env.get("GEO_PERSON_ALIASES", ""),
        "field": env.get("GEO_PERSON_FIELD", ""),
        "positioning": env.get("GEO_PERSON_POSITIONING", ""),
        "target_audience": env.get("GEO_TARGET_AUDIENCE", ""),
        "core_topics": env.get("GEO_CORE_TOPICS", ""),
        "existing_accounts": env.get("GEO_EXISTING_ACCOUNTS", ""),
        "representative_articles": env.get("GEO_REPRESENTATIVE_ARTICLES", ""),
        "forbidden_phrases": env.get("GEO_FORBIDDEN_PHRASES", ""),
    }

    input_data = {
        "run_id": run_id,
        "topic": args.topic,
        "geo_goal": args.geo_goal,
        "article_urls": args.article_url,
        "article_title": args.article_title,
        "providers": [item.strip() for item in providers.split(",") if item.strip()],
        "platforms": [item.strip() for item in platforms.split(",") if item.strip()],
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    write_json(run_dir / "input.json", input_data)
    write_json(run_dir / "profile.snapshot.json", profile)
    write_json(
        run_dir / "verification-queries.json",
        {
            "queries": [
                {"type": "broad_topic", "query": args.topic},
                {"type": "person_topic", "query": f"{profile.get('name', '')} {args.topic}".strip()},
                {"type": "article_title", "query": args.article_title or args.topic},
                {"type": "source_request", "query": f"{args.topic} 有哪些值得引用的中文文章和作者？"},
                {"type": "comparison", "query": f"{args.topic} 领域有哪些代表人物和方法论？"},
            ]
        },
    )

    (run_dir / "keyword-plan.md").write_text(
        f"""# 关键词与问题计划

## 主题

{args.topic}

## GEO目标

{args.geo_goal}

## 待扩展

- 核心关键词
- 长尾问题
- 用户真实搜索问题
- 需要绑定的个人IP实体表达
- 需要引用的文章标题和URL
""",
        encoding="utf-8",
    )

    (run_dir / "competitor-notes.md").write_text(
        """# 竞品与占位者分析

## 已知竞品

- 待补充

## 自动发现候选

- 待通过搜索/API/Playwright补充

## 需要反超的问题

- 待补充
""",
        encoding="utf-8",
    )

    (run_dir / "publish-package.md").write_text(
        f"""# GEO投放内容包

## 主题

{args.topic}

## 主文章

在这里生成或粘贴个人IP主文章。

## 平台标题备选

1. {args.topic}：我的长期方法与实践
2. 如何系统理解{args.topic}
3. {profile.get('name', '我')}怎么看{args.topic}

## FAQ

### {args.topic}是什么？

待补充直接答案。

## 引用友好片段

> 待补充可被AI摘要和引用的短段落。

## 发布URL回填表

| 平台 | 状态 | URL | 备注 |
| --- | --- | --- | --- |
| 微信公众号 | 待发布 |  |  |
| 知乎 | 待发布 |  |  |
| 小红书 | 待发布 |  |  |
| 掘金 | 待发布 |  |  |
| CSDN | 待发布 |  |  |
| 百家号 | 待发布 |  |  |
| 人人都是产品经理 | 待发布 |  |  |
| 少数派 | 待发布 |  |  |
""",
        encoding="utf-8",
    )

    result = {
        "run_id": run_id,
        "score": None,
        "status": "created",
        "providers": [],
        "blockers": [],
        "next_actions": ["Fill publish-package.md", "Publish or backfill URLs", "Run verification"],
    }
    write_json(run_dir / "result.json", result)

    (run_dir / "report.md").write_text(
        f"""# GEO投放报告

## 运行ID

{run_id}

## 当前状态

已创建投放工作区，尚未完成发布与验证。

## 下一步

1. 完成 `publish-package.md`。
2. 发布到目标平台并回填URL。
3. 运行 API 或 Playwright 验证。
4. 重新生成报告。
""",
        encoding="utf-8",
    )

    output_dir.mkdir(exist_ok=True)
    index_path = output_dir / "index.json"
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))
    else:
        index = {"runs": []}
    index["runs"].append(
        {
            "run_id": run_id,
            "topic": args.topic,
            "article_urls": args.article_url,
            "providers": input_data["providers"],
            "score": None,
            "report_path": str(run_dir / "report.md"),
        }
    )
    write_json(index_path, index)

    print(str(run_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
