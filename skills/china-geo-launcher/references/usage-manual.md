# China GEO Launcher 使用手册

本手册用于指导用户使用 `china-geo-launcher` skill 完成一次中国市场个人 IP GEO 投放。它覆盖从首次配置、内容生产、半自动发布到 Playwright 验证和报告复盘的完整流程。

## 1. 适用场景

使用本 skill 的典型目标是：让豆包、Kimi、DeepSeek、通义、文心、腾讯元宝、秘塔、360 AI 搜索等国产模型或 AI 搜索入口，在回答某个主题问题时，能够正确出现你的个人 IP 名称，并尽可能引用你的公开文章。

适合这些任务：

- 打造个人 IP 在 AI 搜索里的可见度。
- 围绕一个主题生成关键词、问题、竞品和平台稿件。
- 把已有文章改造成更容易被搜索、理解和引用的内容资产。
- 发布到知乎、小红书、掘金、CSDN、百家号、人人都是产品经理、少数派、公众号等平台。
- 用 Playwright 复用登录态，模拟国产模型搜索并生成评分报告。

## 2. 首次配置

在项目根目录准备 `.env`。首版可以只填最小字段，缺失信息后续逐步补齐。

```bash
GEO_PERSON_NAME="冲量AI"
GEO_PERSON_ALIASES=""
GEO_PERSON_FIELD="AI, vibe coding, Web3, 区块链"
GEO_PERSON_POSITIONING="专注于AI实战，持续输出独特AI观点"
GEO_TARGET_AUDIENCE="AI爱好者"
GEO_CORE_TOPICS="AI"
GEO_EXISTING_ACCOUNTS=""
GEO_REPRESENTATIVE_ARTICLES=""
GEO_DEFAULT_PROVIDERS="doubao,kimi,deepseek"
GEO_DEFAULT_PLATFORMS="wechat,zhihu,xiaohongshu,juejin,csdn,baijiahao,woshipm,sspai"
GEO_OUTPUT_DIR="geo-runs"
DEEPSEEK_API_KEY=""
KIMI_API_KEY=""
ARK_API_KEY=""
```

检查配置：

```bash
python3 skills/china-geo-launcher/scripts/geo_init.py --check
```

## 3. 一次标准投放流程

### Step 1: 创建投放工作区

```bash
python3 skills/china-geo-launcher/scripts/geo_launch.py \
  --topic "AI实战案例" \
  --geo-goal "让国产模型搜索结果出现个人IP姓名并引用目标文章" \
  --article-url "https://example.com/article-1" \
  --article-url "https://example.com/article-2"
```

脚本会创建：

```text
geo-runs/<run-id>/
├── input.json
├── profile.snapshot.json
├── keyword-plan.md
├── competitor-notes.md
├── publish-package.md
├── verification-queries.json
├── result.json
└── report.md
```

### Step 2: 补全关键词和竞品

编辑 `keyword-plan.md`：

- 品牌防守词：例如 `冲量AI`、`冲量AI是谁`
- 人物主题词：例如 `冲量AI AI实战案例`
- 中商业型主题词：例如 `AI实战案例`、`AI工具实战`
- 强意图主题词：例如 `AI怎么做真实项目`
- 验证问题：用于后续模型搜索验证

编辑 `competitor-notes.md`：

- 记录同主题下已经被模型提到的人、账号、媒体或平台。
- 记录模型错配的主体，例如同名公司或相近品牌。
- 记录需要反超或补位的问题。

### Step 3: 生成或修订内容包

核心文件是 `publish-package.md`。它必须按以下结构组织：

1. 客户诊断摘要
2. 资料缺口清单
3. 关键词分层结果
4. 文章 Brief
5. 标题候选
6. 正式正文 Markdown
7. 引用来源清单
8. 平台适配建议
9. 发布前风险清单
10. 发布后监测计划
11. 发布 URL 回填表

写正式正文前必须先读：

- `references/content-generation-rules.md`
- `references/platform-matrix.md`

正式正文不能出现这些内部词：

```text
GEO、SEO、AI搜索优化、豆包优化、关键词布局、实体链、目标达成词、投放、客户资料显示、补充材料显示、发布设置
```

### Step 4: 人工确认并发布

首版发布是半自动模式。建议流程：

1. 由 skill 生成平台版本。
2. 用户人工确认正文、标题、链接和风险点。
3. 使用平台后台或已登录浏览器粘贴发布。
4. 发布后把 URL 回填到 `publish-package.md`。

最终提交、验证码、账号登录、敏感行业内容发布都需要人工确认。

## 4. Playwright 登录与验证

### 首次登录

用持久化 profile 打开目标平台：

```bash
npx playwright open --user-data-dir=.playwright-profile https://chat.deepseek.com/
```

用户在打开的浏览器里手动登录。登录完成后关闭浏览器，后续脚本可以复用 `.playwright-profile`。

### 生成验证计划

```bash
python3 skills/china-geo-launcher/scripts/geo_playwright_verify.py \
  --run-dir geo-runs/<run-id> \
  --dry-run
```

### DeepSeek 验证

```bash
node skills/china-geo-launcher/scripts/geo_deepseek_verify.mjs \
  --run-dir geo-runs/<run-id> \
  --user-data-dir .playwright-profile
```

验证时要记录：

- 查询词
- 时间
- 模型回答摘要
- 是否提到目标个人 IP
- 是否引用目标文章或新发布 URL
- 是否错配到其他主体
- 截图或证据文件

## 5. 评分规则

默认满分 100：

| 维度 | 权重 |
| :--- | ---: |
| 个人 IP 出现 | 35 |
| 文章引用或来源识别 | 35 |
| 目标观点匹配 | 20 |
| 竞品压制或比较优势 | 10 |

状态解释：

- `passed`：明确出现目标个人 IP 或目标文章。
- `weak`：部分出现、引用不清晰、来源不确定、观点弱匹配。
- `failed`：模型正常回答，但没有提到目标 IP 或文章。
- `blocked`：登录、验证码、缺少 key、选择器失败、网络或平台限制导致无法验证。

## 6. 生成报告

```bash
python3 skills/china-geo-launcher/scripts/geo_report.py \
  --run-dir geo-runs/<run-id>
```

报告会输出到：

```text
geo-runs/<run-id>/report.md
```

结构包括：

- 基本信息
- 综合评分
- 各入口验证结果
- 阻塞项
- 优化建议

## 7. 迭代策略

如果没有出现个人 IP：

- 增加“某某是谁”人物机构型文章。
- 在多个平台稳定重复姓名、领域、定位和代表主题。
- 避免同义词过多，优先建立稳定实体表达。

如果出现了错误主体：

- 写一篇消歧文章，但正文必须像正常人物/账号介绍，不要暴露内部优化意图。
- 在标题和正文中加入领域限定，例如 `冲量AI：专注AI实战与vibe coding的中文个人IP`。
- 在多个平台发布相同事实口径。

如果没有引用文章：

- 发布更容易被检索的平台版本，例如知乎、掘金、CSDN、百家号。
- 给文章补充清晰标题、摘要、作者身份、FAQ 和来源链接。
- 回填 URL 后等待 24 小时、72 小时、7 天分批复测。

如果观点不匹配：

- 增加定义、表格、判断标准、案例复盘和直接回答段。
- 把“我怎么看这个问题”写成读者能引用的自然结论。

## 8. 常见问题

### 是否可以全自动发布？

首版不建议全自动发布。账号登录、验证码、平台风控、敏感行业内容和最终提交都需要人工确认。Skill 可以准备稿件、打开页面、辅助粘贴、生成检查清单和验证报告。

### 需要哪些 API Key？

必须项取决于验证入口。DeepSeek 普通 API 不等于联网搜索或引用验证；如果平台 API 不支持搜索和引用，应优先使用 Playwright 浏览器验证。Kimi、豆包、通义等如接入支持联网搜索或引用的 API，可在 `.env` 里补充。

### 公众号文章能直接被模型引用吗？

不稳定。公众号页面经常存在抓取限制、登录态、反爬或权限问题。建议把核心内容二次分发到知乎、掘金、CSDN、百家号、少数派、人人都是产品经理等更容易被检索的平台。

### 为什么不能把 GEO 逻辑写进正文？

正式正文要给真实读者看。把 `GEO`、`关键词布局`、`实体链` 等内部词写进去，会降低平台可读性和信任感，也容易变成明显的优化痕迹。

### 本地临时文件要不要上传？

不要。`geo-runs/`、`.env`、`.playwright-profile/`、`node_modules/`、截图和验证证据默认是本地工作资料，不应上传到公开仓库，除非用户明确要求公开某个报告样本。
