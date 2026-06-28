# AI 学习路线 & 副业发展计划

> Backend Developer → AI-Powered One Person Company

## 目录

- [目标](#目标)
- [第一阶段：AI 提效工具链（第 1-2 周）](#第一阶段ai-提效工具链第-1-2-周)
  - [Claude Code 深度使用](#claude-code-深度使用)
  - [其他 AI 编码工具](#其他-ai-编码工具)
- [第二阶段：AI 应用开发基础（第 3-6 周）](#第二阶段ai-应用开发基础第-3-6-周)
  - [LLM API 调用](#llm-api-调用)
  - [RAG（检索增强生成）](#rag检索增强生成)
  - [Agent 开发](#agent-开发)
  - [MCP 协议](#mcp-协议)
- [第三阶段：AI 游戏开发（第 7-20 周）](#第三阶段ai-游戏开发第-7-20-周)
  - [游戏引擎上手](#游戏引擎上手)
  - [AI 美术管线（生图）](#ai-美术管线生图)
  - [AI 叙事管线（剧情/对话）](#ai-叙事管线剧情对话)
  - [游戏 AI 中间件（SaaS 备选）](#游戏-ai-中间件saas-备选)
- [第四阶段：MVP 与发布](#第四阶段mvp-与发布)
  - [AI 互动小说 MVP 计划](#ai-互动小说-mvp-计划)
  - [变现路径](#变现路径)
  - [里程碑目标](#里程碑目标)
- [第五阶段：持续学习](#第五阶段持续学习)
- [设备与基础设施](#设备与基础设施)
- [进度记录](#进度记录)
- [避坑指南](#避坑指南)

## 目标

1. **提高开发效率** — AI 工具深度使用，编码效率翻倍
2. **副业创收** — 游戏开发 + AI 小说/生图，打造一人公司
3. **跟上时代** — 了解 AI 最新发展，保持竞争力

---

## 第一阶段：AI 提效工具链（第 1-2 周）

### Claude Code 深度使用

- [x] 掌握 Plan Mode + 多 Agent 编排
- [x] 配置 Hook 系统（PreToolUse / PostToolUse / Stop）
- [x] 建立个人 rules 文件（coding-style / git-workflow / testing / security）
- [x] TDD 工作流（tdd-guide agent）
- [x] 代码审查工作流（code-reviewer agent）

**资料：**
- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)

### 其他 AI 编码工具

- [x] Cursor / Windsurf 对比选型，确定主力工具
- [x] GitHub Copilot 使用

**资料：**
- [Cursor Docs](https://docs.cursor.com)

---

## 第二阶段：AI 应用开发基础（第 3-6 周）

### LLM API 调用

- [ ] OpenAI API / Anthropic API 基础调用
- [ ] 流式输出（Streaming）处理
- [ ] Token 计费与速率限制
- [ ] 结构化输出（JSON Mode / Tool Use）

**资料：**
- [Anthropic API Docs](https://docs.anthropic.com/en/api)
- [OpenAI API Docs](https://platform.openai.com/docs)

### RAG（检索增强生成）

> 📖 完整学习指南：[docs/rag-learning-guide.md](docs/rag-learning-guide.md)（原理、进阶技术、三种实现方案对比、选型建议、资料合集）

**核心知识点（按学习顺序）：**
- [ ] 基础：文档切分（Chunking）→ Embedding → 向量存储 → 相似度检索 → 拼 prompt 生成
- [ ] 进阶检索：Hybrid Search（向量 + 关键词）、Reranking（cross-encoder 重排序）
- [ ] 查询优化：HyDE、Query Rewriting（查询改写）
- [ ] 自适应路由：Adaptive RAG（按查询复杂度选择管线，2026 生产最佳实践）
- [ ] 评估：RAGAS / TruLens 衡量检索质量与生成忠实度

**三种实现方案（详见学习指南第四节）：**
- **LlamaIndex** — RAG 专精，高级检索技术覆盖最全（推荐上手）
- **LangChain / LangGraph** — 通用编排，适合 Agent + 多步任务
- **自建 embedding + pgvector** — 最透明，最能理解原理（推荐先做一遍）

**资料：**
- [RAG 全面指南 — Elastic 中文](https://www.elastic.co/cn/what-is/retrieval-augmented-generation)（入门首选）
- [检索增强生成 — Prompt Engineering Guide 中文版](https://www.promptingguide.ai/zh/techniques/rag)
- [12 Advanced RAG Techniques — Atlan](https://atlan.com/know/advanced-rag-techniques/)（进阶必读）
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [Pinecone Learning Center](https://www.pinecone.io/learn/)

### Agent 开发

- [ ] Tool Use / Function Calling
- [ ] 多 Agent 协作（创作 Agent + 审稿 Agent）
- [ ] Agent 循环控制（ReAct / Plan-Execute）

**资料：**
- [Anthropic Tool Use Guide](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

### MCP 协议

- [ ] MCP Server 开发
- [ ] MCP Client 接入
- [ ] 现有 MCP Server 生态调研

**资料：**
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

## 第三阶段：副业方向深耕（第 9-16 周）

### 方向 A：AI 游戏开发

#### A1. AI NPC 智能对话系统

- [ ] LLM API 驱动 NPC 对话
- [ ] RAG 存储世界观/角色背景
- [ ] Function Calling 实现游戏内动作
- [ ] Streaming 逐字输出对话

**参考产品：**
- [Inworld AI](https://inworld.ai/)
- [NVIDIA ACE](https://developer.nvidia.com/ace)
- [Convai](https://convai.com/)

#### A2. AI 辅助独立游戏开发（One Person Studio）

| 环节 | AI 工具 | 掌握 |
|------|---------|------|
| 代码 | Claude Code / Cursor | [ ] |
| 2D 美术 | Midjourney / Stable Diffusion / DALL-E | [ ] |
| 3D 模型 | Meshy / Luma AI / Rodin | [ ] |
| 音效/音乐 | Suno / Udio / ElevenLabs | [ ] |
| UI 设计 | v0 / Claude Artifacts | [ ] |
| 策划文案 | Claude / GPT | [ ] |

- [ ] Godot 引擎基础
- [ ] 第一个 AI 辅助小游戏 Demo

**资料：**
- [Godot 官方文档](https://docs.godotengine.org/)
- [GameDev.tv Godot 课程](https://www.gamedev.tv/)
- [Brackeys Godot 教程](https://www.youtube.com/@Brackeys)

#### A3. 游戏 AI 中间件（SaaS）

- [ ] 调研现有游戏 AI 工具市场
- [ ] 确定切入点（对话系统 / 反作弊 / 数据分析 / 程序化生成）

### 方向 B：AI 创作小说

#### B1. 核心技术

- [ ] 大纲 → 章节 → 段落分层生成架构
- [ ] 角色卡（Character Card）系统
- [ ] 向量检索历史保持一致性
- [ ] 多 Agent 审稿系统（创作 + 审稿 + 一致性检查 + 润色）
- [ ] 摘要链（Summary Chain）处理超长文本

**技术架构：**
```
大纲管理层（世界观设定 → 卷 → 章 → 节）
       ↓
写作引擎层（创作 Agent → 审稿 Agent → 一致性 Agent → 润色 Agent）
       ↓
记忆系统层（角色卡 DB + 情节向量库 + 摘要链缓存）
```

#### B2. 产品调研

- [ ] 研究 Sudowrite / NovelCrafter / NovelAI 产品逻辑
- [ ] 研究 SillyTavern 角色卡系统
- [ ] 调研各平台 AI 创作政策（番茄小说 / 起点 / 七猫 / Amazon Kindle）

**资料：**
- [Sudowrite](https://www.sudowrite.com/)
- [NovelCrafter](https://novelcrafter.com/)
- [SillyTavern](https://github.com/SillyTavern/SillyTavern)
- [NovelAI](https://novelai.net/)

### 方向 C：AI 生图

#### C1. 基础工具

- [ ] ComfyUI 节点式工作流
- [ ] Stable Diffusion WebUI（了解即可）
- [ ] Midjourney / DALL-E 提示词

#### C2. 进阶技术

- [ ] LoRA 训练（固定角色/风格）
- [ ] ControlNet（精确控制构图）
- [ ] IP-Adapter（图像参考）
- [ ] Inpainting / Outpainting

#### C3. 工程化

- [ ] Replicate API 云端调用
- [ ] Automatic1111 API 本地调用
- [ ] 批量生成 + 自动化管线

**资料：**
- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- [Civitai](https://civitai.com/)
- [OpenArt Workflows](https://openart.ai/workflows/)
- [Replicate Docs](https://replicate.com/docs)

#### C4. 变现模式

- [ ] AI 写真/头像（LoRA 训练人脸）
- [ ] 电商素材（产品图、Banner）
- [ ] AI 漫画/绘本（固定角色 + 分镜）
- [ ] 素材库上传（Freepik / Shutterstock）
- [ ] ComfyUI 工作流模板

---

## 组合拳：AI 互动小说 / 视觉小说

三个方向的交叉点，一个人能完成：

```
AI 生图（角色立绘/场景）
      +
AI 写小说（剧情/对话）
      +
AI 游戏引擎（Godot/Unity）
      ↓
  AI 互动小说 / 视觉小说
```

**参考案例：**
- 《完蛋！我被美女包围了》类互动影游
- Steam AI Visual Novel 品类
- AI 文字冒险游戏（LLM 开放剧情）

### 组合产品 MVP 计划

- [ ] Week 1-2: ComfyUI 出角色立绘 + 场景图
- [ ] Week 3-4: Claude API + RAG 做剧情生成管线
- [ ] Week 5-6: Godot 搭建游戏框架
- [ ] Week 7-8: 集成 AI 管线，做出可玩 Demo
- [ ] Week 9-10: 发布 itch.io / Steam 收集反馈

---

## 第四阶段：持续学习

### 信息源

| 类型 | 来源 | 频率 |
|------|------|------|
| 技术趋势 | [Hacker News](https://news.ycombinator.com/) | 每日 |
| AI 新闻 | [The Batch (Andrew Ng)](https://www.deeplearning.ai/the-batch/) | 每周 |
| AI + 工程 | [Simon Willison's Blog](https://simonwillison.net/) | 每周 |
| 论文 | [arXiv CS.AI](https://arxiv.org/list/cs.AI/recent) | 每周 |
| 社区 | X/Twitter: @kaboroev @swyx @karpathy | 每日 |

### 系统课程（需要时补充）

- [ ] [DeepLearning.AI Short Courses](https://www.deeplearning.ai/short-courses/)
- [ ] [FastAI Practical Deep Learning](https://course.fast.ai/)
- [ ] [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)

---

## 设备与基础设施

### 当前设备

- [ ] Mac Mini（本地开发）
- [ ] GPU 情况：\_\_\_\_\_\_（决定跑本地 SD 还是云端）

### 云服务

| 服务 | 用途 |
|------|------|
| Anthropic API | LLM 调用 |
| Replicate | 云端 SD 出图（如无 GPU） |
| Pinecone / pgvector | 向量数据库 |
| Vercel / Railway | 应用部署 |

---

## 变现路径总览

```
Phase 1: 提升主业效率 → 涨薪/跳槽溢价
         ↓
Phase 2: 做 AI 工具 → SaaS 订阅收入
         ↓
Phase 3: AI 互动小说/游戏 → 平台分成/直接销售
         ↓
Phase 4: 多个产品组合 → One Person Company
```

### 短期目标（0-3 个月）

- [ ] AI 写作管线可用
- [ ] ComfyUI 出图工作流可用
- [ ] 第一个 AI 互动小说 Demo

### 中期目标（3-6 个月）

- [ ] 发布第一个产品（游戏或工具）
- [ ] 获得第一批用户反馈
- [ ] 产生第一笔收入

### 长期目标（6-12 个月）

- [ ] 可持续的副业收入
- [ ] 多个产品线并行
- [ ] 个人品牌建立

---

## 进度记录

| 日期 | 完成事项 | 备注 |
|------|---------|------|
| 2026-06-12 | 路线图初版 | - |
| 2026-06-13 | 第一阶段完成，开始第二阶段 | - |
| | | |

---

## 避坑指南

- ❌ 不要从数学/理论开始 — 你不是算法工程师
- ❌ 不要学 TensorFlow/PyTorch 底层 — 99% 场景用 API 就够了
- ❌ 不要追每个新框架 — LangChain/LlamaIndex/CrewAI 变化极快，学原理不学框架
- ❌ 不要只看不动手 — AI 领域一周不写代码就落后
- ✅ 先 API 后框架 — 原生 API 调通后再引入框架
- ✅ 先产品后优化 — MVP 快速上线验证，不要追求完美
- ✅ 先 niche 后扩展 — 找到一个细分点做到极致
