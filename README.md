# skill-finder-zh / 中文 Skill 搜索 / 中文 Skill 发现 / Skill 中文导航

> **中文 Agent Skill 发现工具** — 填补 `vercel-labs/find-skills`(英文 579K 安装)的中文空白

**中文别名**:`中文 Skill 搜索` / `中文 Skill 发现` / `Skill 中文导航` — 中文用户搜这些关键词也能找到。

**English**: `skill-finder-zh` / `Chinese Skill Finder`

## 为什么需要它

GitHub 上**已经有 33,000+ Agent Skills**(见 [Skillsmp](https://skillsmp.com))。生态已经分得很清楚:

| 类别 | 已有项目 | 中文友好? |
|---|---|---|
| 🔍 **Discover**(英文) | `vercel-labs/find-skills`(579K 安装,生态第一) | ❌ 英文 |
| 🔍 **Discover**(中文) | ❌ **没有** | — |
| 🛠️ Create | `anthropics/skill-creator` | ⚠️ 部分 |
| 📦 Install | `npx skills add`(Vercel) | ⚠️ 英文 |
| 🚀 Publish | `Weiming3/skill-publisher`(姊妹项目) | ✅ |

**skill-finder-zh 填补唯一空白:中文 Skill 发现**。

## 核心特性

| 特性 | 说明 |
|---|---|
| 🔍 **多数据源聚合** | GitHub Search API + awesome-claude-skills + skills.sh + Skillsmp |
| 🀄 **中文自然语言** | 支持 "找中文 PDF 处理 skill" / "推荐一个写测试的" |
| 🌐 **中英双语匹配** | `PDF` ↔ `文档处理`,`单元测试` ↔ `unit test` |
| 📊 **跨源置信度** | 在 awesome + skills.sh + GitHub 都出现 = 高分 |
| 🚀 **一键安装命令** | 每个结果附 `mavis skill install` + `npx skills add` |
| ⭐ **智能过滤** | 按 star / 更新时间 / 平台 / 语言过滤 |
| 📝 **中文推荐说明** | 每个 skill 写中文理由 + 适合谁 + 已知坑 |

## 安装

### 通过 `mavis skill install`(Mavis)
```bash
mavis skill install https://github.com/Weiming3/skill-finder-zh
```

### 通过 `npx skills add`(Claude Code / Codex / Cursor)
```bash
npx skills add Weiming3/skill-finder-zh
```

### 手动
把 `SKILL.md` 复制到 `~/.mavis/agents/<your-agent>/skills/skill-finder-zh/SKILL.md`。

## 使用

### 基础搜索

```bash
python scripts/find.py "中文 PDF 处理"
python scripts/find.py "React 编码"
python scripts/find.py "我想找一个能帮我写测试的 skill"
```

### 高级搜索

```bash
# 限定 star 数(>= 100)
python scripts/find.py --min-stars 100 "数据库"

# 限定语言(zh / en / any)
python scripts/find.py --language zh "中文文档处理"

# 限定返回数量
python scripts/find.py --top 5 "React"
```

### 环境变量

```bash
# 提升 GitHub Search API 限速(60/小时 → 5000/小时)
export GITHUB_TOKEN=ghp_xxx...
python scripts/find.py "React"
```

## 输出示例

```text
============================================================
  Skill Finder ZH — 搜索:中文 PDF 处理
============================================================

🥇 pdf-toolkit (1,234 ⭐)
   URL: https://github.com/xxx/pdf-toolkit
   简介:中文 PDF 拆分 / 合并 / OCR / 加水印
   更新:2025-12-01
   安装(mavis): mavis skill install https://github.com/xxx/pdf-toolkit
   安装(npx):   npx skills add xxx/pdf-toolkit
   数据源:github, awesome, skills.sh (cross-source hits: 3)

🥈 document-master (456 ⭐)
   ...

💡 下一步:
   - 直接装:mavis skill install <URL> 或 npx skills add <owner/repo>
   - 再找 5 个相关:跑 python find.py '<相关关键词>'
   - 调权重:--min-stars 50 或更高
```

## 工作流程

```
用户 query
   ↓
解析关键词 + 意图分类
   ↓
并发 4 数据源搜索
├─ GitHub Search API(按 star 排序)
├─ awesome-claude-skills 列表(精选)
├─ skills.sh(安装量)
└─ Skillsmp(33,000 skill 聚合)
   ↓
合并去重 + 跨源打分
(stars * 0.6 + 跨源命中数 * 1000 * 0.4)
   ↓
生成中文推荐说明
   ↓
返回 top-N + 一键安装命令
```

## 数据源说明

| 源 | 数据量 | 限速 | 中文覆盖 |
|---|---|---|---|
| GitHub Search API | 33,000+ | 60/h 未认证 / 5000/h 认证 | 用 `language:zh` + `in:readme` 过滤 |
| awesome-claude-skills | ~200 精选 | 无 | 靠 README 关键词 |
| skills.sh | ~1000+ | 推测 100/h | 靠描述关键词 |
| Skillsmp | 33,000+ | 推测 60/h | 靠标签 |

## 项目结构

```
skill-finder-zh/
├── SKILL.md                  # skill 自己的描述(Anthropic 标准)
├── README.md                 # 本文件
├── LICENSE                   # Apache 2.0
├── .gitignore
├── scripts/
│   └── find.py               # 主搜索脚本(Python 3.8+)
└── examples/
    └── sample-search.txt     # 示例输出
```

## 依赖

- Python 3.8+
- `requests`:`pip install requests`

## 相关项目

- [vercel-labs/skills](https://github.com/vercel-labs/skills) — `find-skills`(英文 579K 安装)
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — 数据源
- [skills.sh](https://skills.sh) — 数据源
- [Skillsmp](https://skillsmp.com/zh) — 数据源
- [Weiming3/skill-publisher](https://github.com/Weiming3/skill-publisher) — 姊妹项目:发布 skill

## License

Apache 2.0

## 维护者

Weiming3 — 用 Mavis agent + Anthropic Agent Skills 标准构建。