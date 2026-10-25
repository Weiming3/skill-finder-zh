# skill-finder-zh / 中文 Skill 搜索 / 中文 Skill 发现

> 用中文关键词，在开放的 Agent Skills 生态里找到**能直接装**的 skill。

官方生态里的 `find-skills`（[vercel-labs/skills](https://github.com/vercel-labs/skills)，403 万安装）是英文检索。
中文用户搜「文档处理」「单元测试」这类词时，GitHub 的英文相关性排序基本帮不上忙。
这个工具把三路数据合成一个中文结果列表，每条都直接给 `npx skills add` 命令。

## 数据源（3 个，均实测可用）

| 源 | 用途 | 限制 |
|---|---|---|
| GitHub Search API | 按关键词 + star 搜仓库 | 未认证 60 次/小时；设 `GITHUB_TOKEN` 提到 5000 |
| awesome-claude-skills | ComposioHQ 的精选列表 | 静态列表，靠关键词匹配 |
| skills.sh | 按安装量排序的 skill 注册表 | 无公开文档，字段是 `installs` 不是 star |

> 结果里**没有 URL** 的条目会被丢弃——既不能安装，也不能参与去重。

## 安装

```bash
# 通过 Skills CLI（Claude Code / Codex / Cursor 通用）
npx skills add Weiming3/skill-finder-zh
```

手动方式：把 `SKILL.md` 复制到你所用 agent 的 skills 目录。

## 用法

```bash
pip install requests

python scripts/find.py "中文 PDF 处理"
python scripts/find.py "推荐一个写测试的"

# 限定 star 数 / 语言 / 返回条数
python scripts/find.py --min-stars 100 --language zh --top 5 "数据库"
```

```text
--min-stars  默认 10，低于这个 star 的仓库不返回
--language  zh / en / any（默认 any）
--top       返回条数，默认 5
```

设 `GITHUB_TOKEN` 可以把 GitHub Search 的限速从 60 次/小时提到 5000 次/小时：

```bash
export GITHUB_TOKEN=ghp_xxx
```

## 输出长什么样

```text
============================================================
  Skill Finder ZH — 搜索:数据库
============================================================

🥇 liyupi/yupi-hot-monitor (724 ⭐)
   URL: https://github.com/liyupi/yupi-hot-monitor
   简介:2026 年编程导航 AI 编程实战新项目…
   更新:2026-10-20
   安装:npx skills add liyupi/yupi-hot-monitor
   数据源:github (cross-source hits: 1)

💡 下一步:
   - 直接装:npx skills add <owner/repo>
   - 官方 CLI 直接搜:npx skills find '<关键词>'
```

## 排序逻辑

```text
score = stars * 0.6 + 跨源命中数 * 1000 * 0.4
```

同一个 skill 在多个源里出现会加分；skills.sh 的 `installs` 单独展示，**不会**被当成 star 计入排序。

## 测试

```bash
python tests/test_smoke.py    # 期望 6 passed, 0 failed
```

全部离线（不依赖 GitHub / skills.sh 的可用性），CI 在 ubuntu + windows × Python 3.10–3.12 上跑同一套。

## 项目结构

```text
skill-finder-zh/
├── SKILL.md              # skill 行为描述（Anthropic Agent Skills 标准）
├── README.md
├── LICENSE               # Apache-2.0
├── scripts/find.py       # 主搜索脚本（Python 3.8+）
└── tests/test_smoke.py
```

## 相关项目

- [vercel-labs/skills](https://github.com/vercel-labs/skills) — 英文生态第一的 `find-skills` + Skills CLI
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — 数据源
- [skills.sh](https://skills.sh) — 数据源（按安装量）
- [Weiming3/skill-publisher](https://github.com/Weiming3/skill-publisher) — 姊妹项目：校验并发布 skill

## License

Apache-2.0