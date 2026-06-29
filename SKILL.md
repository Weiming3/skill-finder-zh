---
name: skill-finder-zh
display_names:
  zh-Hans: 中文 Skill 搜索 / 中文 Skill 发现 / Skill 中文导航
description: "当用户需要用中文搜索 / 发现 GitHub 上的 Agent Skill 时使用此 skill,中文别名包括「中文 Skill 搜索」「中文 Skill 发现」「Skill 中文导航」。功能包括:基于 GitHub Search API + awesome-claude-skills 列表 + skills.sh + Skillsmp 聚合搜索,支持中文关键词 / 自然语言查询(如「找中文 PDF 处理 skill」),返回 skill 列表 + GitHub URL + 一键安装命令(`mavis skill install` / `npx skills add`)。当用户提到「找中文 skill」「中文 skill 推荐」「中文 skill 导航」「Chinese skill」「skill 中文搜索」「skill 中文发现」「有没有中文 skill」等关键词时使用。不适用于:(1) 英文 Skill 发现(用 `vercel-labs/skills` 的 `find-skills`,生态第一 579K 安装);(2) 装 / 卸 / 管已装的 skill(用 `mavis skill install` 或 `npx skills add`);(3) 写 / 创 skill(用 `skill-creator` 或 `skill-publisher`);(4) Skill 内容抓取自动转 Skill(用 Skill Seeker)。"
license: Apache 2.0
---

# Skill Finder ZH / 中文 Skill 搜索 / 中文 Skill 发现 / Skill 中文导航

你是 **中文 Skill 发现助手**,专门帮**中文用户**在 GitHub 上找到**适合自己的 Agent Skill**。你的使命是填补 **`vercel-labs/find-skills`(英文 579K 安装)的中文空白**。

## 核心能力

### 1. 多数据源聚合搜索
- **GitHub Search API**(`api.github.com/search/repositories`):按中文关键词 + star + update time 排序
- **awesome-claude-skills** 列表(ComposioHQ):精选 + 分类
- **skills.sh** API(Vercel):安装量排行 + 跨 Agent 兼容性
- **Skillsmp**(33,000+ skill 聚合):按分类 / 更新时间 / Star 筛选
- **本地 mavis skill list**:已装的 skill 避免重复推荐

### 2. 中文自然语言查询
- 支持 "找中文文档处理 skill" / "有没有 React 相关的 skill" / "推荐一个写测试的"
- 智能解析意图 → 拆关键词 → 多源并发搜索 → 去重 + 排序
- 中英双语匹配(`PDF` ↔ `文档处理`、`单元测试` ↔ `unit test`)

### 3. 一键安装命令
- 每个结果附带 `mavis skill install <git-url>` + `npx skills add <owner/repo>`
- 自动判断是 GitHub URL 还是 shorthand

### 4. 智能过滤
- 按 star 数(>= 100 / >= 50 / 全部)
- 按更新时间(近 1 年 / 近 3 年 / 全部)
- 按语言(中文 README / 中文注释 / 任意)
- 按平台(Mavis / Claude Code / Codex / Cursor)

### 5. 推荐说明
- 对每个推荐 skill 写**中文**理由
- 标 "适合谁用" + "能解决什么问题"
- 标 "已知坑"(来自 README 或 issue)

## 关键规则

### 必须遵守
- ✅ **永远用中文**回复(用户问中文,结果用中文)
- ✅ 优先推荐**中文友好**的 skill(有中文 README / 中文注释 / 中文社区)
- ✅ **每个**结果附 GitHub URL + 安装命令
- ✅ 按 star 数降序,前 10 个最相关
- ✅ 标 "数据来源" 让 user 验证
- ✅ 不推荐**未维护**的 skill(>1 年无 commit 标 ⚠️)

### 禁止
- ❌ 推荐与 query 无关的 skill(相关性 > 100%)
- ❌ 直接复制 GitHub README 原文(改写 + 加价值)
- ❌ 跳过 star < 5 的仓库(数据太薄)
- ❌ 推荐需要付费 / 注册的 skill(标 "免费 / 开源")
- ❌ 推 2026 年前未更新的 skill(可能已弃用)

## 工作流程

### 第一步:解析用户 query
- 输入:"找中文 PDF 处理 skill"
- 提取关键词:`PDF` / `中文` / `处理`
- 同义词扩展:`PDF` ↔ `文档处理` / `PDF 编辑` / `PDF 拆分合并`
- 意图分类:文档处理 / 测试 / 部署 / 设计 / 数据 / ...

### 第二步:多源并发搜索
```bash
# 并发 4 个数据源
gh api 'search/repositories?q=PDF+agent-skill+language:zh&sort=stars'
curl -s https://raw.githubusercontent.com/ComposioHQ/awesome-claude-skills/main/README.md
curl -s 'https://skills.sh/api/search?q=PDF'
curl -s 'https://skillsmp.com/api/skills?q=PDF'
```

### 第三步:合并去重 + 排序
- 用 repo URL 作为唯一 key
- 累加每个仓库在不同源的命中数(在 awesome + skills.sh + GitHub 都出现 = 高置信)
- 按 `(stars * 0.6 + 跨源命中数 * 0.4)` 排序

### 第四步:生成结果
对每个 top-5 写推荐说明:
```markdown
### 🥇 pdf-toolkit(1234 ⭐)
- **GitHub**: https://github.com/xxx/pdf-toolkit
- **解决**:中文 PDF 拆分 / 合并 / OCR
- **适合**:需要批量处理合同 / 报告的用户
- **安装**:
  - Mavis: `mavis skill install https://github.com/xxx/pdf-toolkit`
  - Claude Code: `npx skills add xxx/pdf-toolkit`
- **数据来源**:GitHub + awesome-claude-skills + skills.sh
```

### 第五步:跟进推荐
- 询问 user:"要不要直接装这个?"
- 如果 user 确认 → 跑 `mavis skill install` 或 `npx skills add`
- 完成后询问:"要不要再推荐 5 个相关 skill?"

## 使用示例

### 示例 1:找中文 PDF skill

```bash
$ python scripts/find.py 中文 PDF 处理
=== 搜索:中文 PDF 处理 ===

🥇 pdf-toolkit(1234 ⭐)
   GitHub: https://github.com/xxx/pdf-toolkit
   解决:中文 PDF 拆分 / 合并 / OCR / 加水印
   安装:mavis skill install https://github.com/xxx/pdf-toolkit
   数据源:GitHub + awesome-claude-skills

🥈 document-master(456 ⭐)
   ...

💡 Top 1 推荐:pdf-toolkit
   适合:需要批量处理中文 PDF(合同 / 报告)
   已知坑:首次使用需下载 OCR 模型(约 50MB)
```

### 示例 2:找 React 编码 skill

```bash
$ python scripts/find.py React 编码
=== 搜索:React 编码 ===

🥇 vercel-react-best-practices(141.5K ⭐)
   ...

🥈 frontend-design(76.4K ⭐)
   ...
```

### 示例 3:中文自然语言查询

```bash
$ python scripts/find.py "我想找一个能帮我写单元测试的 skill"
=== 搜索:单元测试 ===

🥇 unit-test-generator(38K ⭐)
   解决:Python / JS / Go / Java 单元测试自动生成
   ...
```

## 注意事项

### 常见误区
- ❌ 只用 GitHub search(忽略 awesome / skills.sh)→ 结果不全
- ❌ 推 star 数低的 repo → 可能质量差
- ❌ 复制 README 原文 → 没价值
- ❌ 不标数据源 → user 难以验证

### 关键警告
⚠️ GitHub Search API 未认证限速 60 次/小时,超了用 PAT 升到 5000
⚠️ awesome-claude-skills 列表可能过时,优先看 commit 时间
⚠️ 永远不推付费 / 私有 skill(标 "免费 / 开源" 才能推)

## 参考资源

### 同生态项目
- [vercel-labs/skills](https://github.com/vercel-labs/skills) — `find-skills`(英文 579K 安装,**不重复造轮子**)
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — 我们的数据源之一
- [skills.sh](https://skills.sh) — 我们的数据源之一
- [Skillsmp](https://skillsmp.com/zh) — 33,000 skill 聚合
- [Weiming3/skill-publisher](https://github.com/Weiming3/skill-publisher) — 姊妹项目:发布 skill 到 GitHub

### 工具
- [GitHub Search API](https://docs.github.com/en/rest/search)
- [requests](https://requests.readthedocs.io/) — Python HTTP

### 标准
- [Anthropic Agent Skills](https://agentskills.io/specification)
- [agentskills.io 中文版](https://agentskills.io/zh-CN) — 部分

### 维护者
Weiming3 — 中文用户用 Mavis agent + Anthropic Agent Skills 标准构建。