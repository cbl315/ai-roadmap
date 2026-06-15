# 市场调研：AI Roguelike 文字探险游戏

> 前置：已完成「AI NPC 对话」功能（见 `phase2-web-chat.md`）。
> 本调研为下一产品方向「AI Roguelike 文字探险游戏」做市场论证，解决两个问题：
> 1. 这个赛道被验证过吗？（数据）
> 2. 玩家对现有产品满意吗？痛点在哪？（反馈）
>
> 调研时间：2026-06

---

## 目录

1. [调研结论速览（TL;DR）](#1-调研结论速览tldr)
2. [市场盘面：标杆产品数据](#2-市场盘面标杆产品数据)
3. [玩家真实反馈：爱与恨](#3-玩家真实反馈爱与恨)
4. [商业模式拆解](#4-商业模式拆解)
5. [竞品矩阵与差异化定位](#5-竞品矩阵与差异化定位)
6. [对标路线图的结论与建议](#6-对标路线图的结论与建议)
7. [参考来源](#7-参考来源)

---

## 1. 调研结论速览（TL;DR）

- **赛道已验证**：Latitude（AI Dungeon）以 <20 人团队做到 **$7M+ ARR、800 万用户、已盈利**（2025），证明「AI 文字冒险」需求真实、天花板够养活小团队。
- **玩家痛点集中且未被解决**：记忆丢失、剧情跑偏、重复循环、缺乏目标——前 4 个痛点恰恰是 **roguelike 规则骨架** 能根治的。AI Dungeon 之所以「好玩但留不住人」，根因是它**是沙盒而不是游戏**：没有规则约束，LLM 的自由度反而成了缺点。
- **「AI + Roguelike」是当前空白**：最接近的竞品 Questsmith 把 LLM 叙事和 D20/属性系统结合，但**长期记忆仍是头号投诉**（r/QuestSmith 置顶话题）。规则托管状态、LLM 只负责叙事，是差异化靶心。
- **成本结构有利**：纯 LLM 沙盒每轮都要调模型（AI Dungeon 单次下载曾耗费 $0.30–0.40 算力）；roguelike 架构让规则托管 80% 状态，LLM 只承担 20% 叙事，单局成本可显著降低。

---

## 2. 市场盘面：标杆产品数据

### 2.1 AI Dungeon（Latitude Inc.）— 品类定义者，数据最硬

| 指标 | 数据 | 来源 |
|---|---|---|
| 总用户 | ~800 万（2025） | [Lean AI Leaderboard](https://x.com/henrythe9ths/status/1925515233113907464) |
| ARR | **$7M+**（约 ¥5000 万） | 同上 |
| 盈利状态 | **已盈利**，员工 <20 人 | 同上 |
| 历史下载量 | 7000 万次（2021） | [Reddit 投资人帖](https://www.reddit.com/r/AIDungeon/comments/n3g2b0/) |
| 深度玩家 | 2100 万人完成过 500+ 次行动 | 同上 |
| 融资 | $3.3M（2021） | 同上 |
| 上线爆发 | 首周 10 万玩家、50 万次游玩 | [AI21 案例](https://www.ai21.com/blog/latitude-case-study/) |
| Steam 评价 | 282 条（主力在 web/app） | [games-stats.com](https://games-stats.com/steam/game/ai-dungeon/) |

**数据解读：**
- 这是整个赛道目前**唯一公开的「成功样本」**——不到 20 人、$7M ARR、已盈利。
- 用户基数大（千万级下载），但 **ARPU 偏低**：800 万用户 × 假设 30% 付费 ≈ 240 万付费，对应 $7M ARR 意味着人均年付 ~$30，即月均 ~$2.5——**低客单订阅模型**。
- 启示：纯订阅做不大，但需求真实存在，关键在提升 ARPU 或切更轻量的变现。

### 2.2 Questsmith — 最接近目标产品的参照系

闭源商业产品（web + iOS），核心特征：

| 维度 | 实现 |
|---|---|
| LLM 后端 | 多模型，不绑死单一供应商，成本可控 |
| 记忆系统 | 持久追踪 ~500 个剧情细节/战役 |
| RPG 机制 | D20 骰子 + 4 核心属性（战斗/魔法/潜行/社交）+ HP/MP |
| 附加 | 同伴 NPC、6 种题材、实时视觉特效（火/闪电/烟/震屏） |
| 渠道 | iOS App Store「Questsmith: AI Dungeon Master」+ [thequestsmith.com](https://www.thequestsmith.com/en) |

**⚠️ 核心反馈：** r/QuestSmith 社区置顶痛点 = **长期记忆**：
> *"I've been testing a lot of AI text RPGs recently, and one issue keeps showing up over and over again: **long-term memory**."* — [r/QuestSmith](https://www.reddit.com/r/QuestSmith/)

闭源，无公开技术架构；最接近的开源替代为 `envy-ai/ai_rpg`、`MoonlightByte/NeverEndingQuest`。

### 2.3 NovelAI（Anlatan LLC）— 创作者向，付费意愿高

私营公司，**不公开财务**。已知商业模式：
- 订阅制，无限生成，靠**套餐分级控制算力配额**：$10 / $15 / $25（月）。
- 定位是**写作工具**而非游戏，用户付费意愿显著高于游戏玩家（创作者 vs 玩家）。
- 社区推测采用「power user 补贴」模型：高价档用户补贴低价档重度用户。

### 2.4 其他值得关注的样本

| 产品 | 形态 | 价值 |
|---|---|---|
| **Adventure AI** | ChatGPT 驱动手游，苹果「New games we love」推荐 | 证明移动端有需求 |
| **Intra**（Ian Bicking, 2025） | LLM 当解析器的经典交互小说 | 设计思路参考 |
| **AI Town**（a16z） | 多 Agent 沙盒，持久世界状态 | 多 NPC 互动参考，但缺游戏目标 |
| **KoboldAI** | 开源，可本地部署 | 写作质量好，但非「游戏」 |

---

## 3. 玩家真实反馈：爱与恨

数据来源：r/AIDungeon、r/QuestSmith、社区评测帖的负面反馈聚类。

### 3.1 玩家最恨的 7 个问题（按出现频率排序）

| # | 痛点 | 典型反馈 | roguelike 能否解决 |
|---|---|---|---|
| 1 | **记忆丢失 / 失忆** | 「AI 忘了角色性别」「第十轮就忘了前情」 | ⭐⭐⭐ 用结构化世界状态托管 |
| 2 | **质量下滑 / 不一致** | 「角色反应不合逻辑」「完全误解我的角色」 | ⭐⭐ 状态注入 + 风格约束 |
| 3 | **重复循环** | 「AI 反复同一句话」「陷入死循环」 | ⭐⭐⭐ 节点推进天然打破循环 |
| 4 | **缺乏目标 / 无方向** | 「故事没头没尾」「纯即兴没意义」 | ⭐⭐⭐ 楼层/BOSS/胜利条件 |
| 5 | **不尊重设定** | 「无视性别」「美式中心主义」「不懂残障」 | ⭐⭐ 世界观词条 + 玩家自定义 |
| 6 | **成本 / 付费墙** | 「太贵」「免费档没法玩」 | ⭐ 工程成本控制 |
| 7 | **不当/攻击性内容** | 「AI 突然暴力/出戏」 | ⭐ 风格约束 prompt |

**核心洞察：前 4 个高频痛点（记忆、一致、重复、无目标）恰好都是 roguelike 架构能根治的。** 这就是产品差异化的靶心。

### 3.2 玩家最爱的体验（必须保留）

| 体验 | 说明 |
|---|---|
| 自由度 | 「想干嘛干嘛」——品类立身之本 |
| 意外性 | 「AI 会生成我没想到的剧情」 |
| 沉浸感 | 「真的像在和角色对话」（你的 NPC 能力直接复用） |
| 重玩性 | 「每次都不一样」（roguelike 天然具备） |

---

## 4. 商业模式拆解

综合三个标杆，AI 文字游戏目前有 3 种成熟变现模式：

| 模式 | 代表 | 客单价 | 优点 | 风险 |
|---|---|---|---|---|
| **订阅（算力分级）** | AI Dungeon、NovelAI | $10–25/月 | 收入稳定可预测 | 重度用户成本高，需「轻度补贴重度」 |
| **按量（token 额度）** | NovelAI 高级档 | 按 token 充值 | 成本可控 | 玩家「计费焦虑」，不敢自由玩 |
| **F2P + 内购/广告** | Adventure AI | 免费 + 内购 | 用户基数大、获客快 | ARPU 低、留存差 |

**关键判断：**
- AI Dungeon $7M ARR / 800 万用户 ≈ **人均年付仅 ~$0.9**（含免费用户），说明**纯订阅难做大**。
- roguelike 有 AI Dungeon 没有的独特优势：**元进度解锁**（死亡后解锁新内容）。这天然适配「一局短、想再来、轻付费」的手游 roguelite 节奏（参考《弹壳特攻队》《不休骑士》），变现天花板更高。

---

## 5. 竞品矩阵与差异化定位

### 5.1 二维定位图

```
                    游戏性强（有规则/目标）
                           ▲
                           │
        Slay the Spire ●   │   ◆ 目标产品
        FTL                 │
                           │
 自由度高 ◀─────────────────┼─────────────────▶ 规则约束强
                           │
        AI Dungeon ●       │        ● Questsmith
        NovelAI            │
                           │
                           ▼
                    游戏性弱（纯沙盒）
```

### 5.2 量化对比

| 维度 | AI Dungeon | Questsmith | **目标产品** |
|---|---|---|---|
| 记忆 | 弱（RAG 补救） | 中（500 细节） | **强（roguelike 状态机托管）** |
| 目标感 | 无 | 弱（有属性无楼层） | **强（楼层/BOSS/解锁）** |
| 留存设计 | 靠玩家自驱 | 靠属性养成 | **靠 roguelite 元进度（最强）** |
| 单局节奏 | 不可控 | 中等 | **可控（节点地图）** |
| 单局成本 | 高（每轮纯 LLM） | 高 | **低（规则管 80%，LLM 管 20%）** |
| NPC 对话 | 有 | 有 | **复用已实现的 NPC 系统** |

### 5.3 护城河

相对现有竞品，差异化优势集中在三点：
1. **规则托管状态**——LLM 不「记忆」，只「演」，根治失忆。
2. **节点地图 + roguelike 循环**——给 LLM 自由度套上游戏目标，根治「无方向」。
3. **元进度解锁**——把单局死亡转化为长期留存动力，补足 AI Dungeon 最弱的环节。

---

## 6. 对标路线图的结论与建议

### 结论

1. **赛道已验证**：Latitude 20 人做到 $7M ARR 且盈利，需求真实、天花板够高。
2. **玩家痛点明确且集中**：记忆、一致、重复、无目标——前人没解决好，是差异化靶心。
3. **「AI + Roguelike」方向是解药**：roguelike 规则骨架正好根治 LLM 沙盒四大病，且成本更低。

### MVP 优先级建议

> 原则：别一上来就追求 AI Dungeon 的自由度。用 roguelike 的确定性框住 LLM 的不确定性。

竖切第一版（MVP）只做这一条线：
```
节点地图 + 文字事件 + 简单战斗/抉择 + 死亡解锁
```

技术护城河押在**状态管理**：玩家属性、关系、剧情旗标、物品全部结构化入库，LLM 每次只读状态生成描述，绝不承担「记忆」职责——这是解决所有竞品失忆痛点的关键。

### 对应路线图位置

本产品位于 README 第三阶段「AI 游戏开发」下的交叉点：
- 复用 **A1. AI NPC 智能对话系统**（已完成的 `phase2-web-chat.md`）
- 结合 **AI 叙事管线**
- 属于「AI 互动小说 / 视觉小说」组合拳的落地形态之一

---

## 7. 参考来源

### AI 文字游戏 / LLM 游戏
- [Best Text-Based Adventure Games Powered by AI (howworks.ai)](https://howworks.ai/blog/best-ai-text-adventure-games)
- [Building a real-time AI RPG — Questsmith (OpenAI Community)](https://community.openai.com/t/building-a-real-time-ai-rpg-with-evolving-narratives-using-llms/1379208)
- [Questsmith 官网](https://www.thequestsmith.com/en)
- [Intra: design notes on an LLM-driven text adventure (Ian Bicking, 2025)](https://ianbicking.org/2025/07/intra-llm-text-adventure/)
- [AdventureGPT: Using LLM-Backed Agents in Text Adventures](https://betterprogramming.pub/adventuregpt-using-llm-backed-agents-to-play-text-based-adventure-games-be52f243866a)
- [Show HN: turn any book into a text adventure](https://news.ycombinator.com/item?id=44725202)

### AI Dungeon 数据与架构
- [Lean AI Leaderboard — $7M ARR / 8M users (X)](https://x.com/henrythe9ths/status/1925515233113907464)
- [Investors gave Latitude $3.3M (Reddit)](https://www.reddit.com/r/AIDungeon/comments/n3g2b0/investors_gave_latitude_330000000/)
- [AI21 Labs — Latitude case study](https://www.ai21.com/blog/latitude-case-study/)
- [How the New Memory System Works (Latitude.io)](https://latitude.io/blog/how-the-new-memory-system-works)
- [What is the Memory System? (AI Dungeon 官方)](https://help.aidungeon.com/faq/the-memory-system)
- [Memory Systems for AI Agents: Beyond Context Windows](https://levelup.gitconnected.com/memory-systems-for-ai-agents-beyond-context-windows-967b39ce9896)
- [AI Dungeon on Steam 统计](https://games-stats.com/steam/game/ai-dungeon/)

### 玩家反馈（Reddit）
- [Has AI Dungeon's story quality gotten worse lately?](https://www.reddit.com/r/AIDungeon/comments/1kt3fnq/has_ai_dungeons_story_quality_gotten_worse_lately/)
- [AI's biggest problem with roleplay](https://www.reddit.com/r/AIDungeon/comments/1ifg64e/ai_biggest_problem_with_roleplay/)
- [Issues with AI being uncreative and lackluster](https://www.reddit.com/r/AIDungeon/comments/11y37kb/issues_with_ai_being_uncreative_and_lackluster/)
- [What players HATE about AI writing](https://www.reddit.com/r/AIDungeon/comments/1qxu8rq/you_told_us_what_you_hate_about_ai_writing/)
- [r/QuestSmith — long-term memory 痛点](https://www.reddit.com/r/QuestSmith/)

### Roguelike 设计
- [What is a Traditional Roguelike? (Cogmind 开发者)](https://www.gridsagegames.com/blog/2020/02/traditional-roguelike/)
- [Analysis: The Eight Rules of Roguelike Design (Game Developer)](https://www.gamedeveloper.com/game-platforms/analysis-the-eight-rules-of-roguelike-design)
- [Roguelike — Wikipedia (Berlin Interpretation)](https://en.wikipedia.org/wiki/Roguelike)

### Slay the Spire 循环设计
- [Slay the Spire core loop 讨论 (r/gamedesign)](https://www.reddit.com/r/gamedesign/comments/1blba7d/slay_the_spire_might_have_the_most_efficientbest/)
- [Project Roguelite Strategy — Bryon Wilkins](http://www.bryonwilkins.com/Project-Roguelite-Strategy/)
- [The Perfect Roguelike Deckbuilder (节点地图)](https://videogamegeek.com/thread/3522750/the-perfect-roguelike-deckbuilder)
