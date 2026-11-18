# AI 学习路线 & 副业发展计划

> Backend Developer → AI-Powered One Person Company

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

- [x] OpenAI API / Anthropic API 基础调用（以 GLM API 实践，OpenAI 兼容协议，纯 fetch 零 SDK）
- [x] 流式输出（Streaming）处理（SSE 解析、级联取消、30s 超时兜底）
- [x] Token 计费与速率限制（usage 帧统计 + 无 tokenizer 估算；API 限流待有真实并发场景再补）
- [ ] 结构化输出（JSON Mode / Tool Use）

> 🛠️ 实战成果：[Web AI NPC 聊天](../references/web-chat/) — Phase 1-3 已上线 [my.woshicai.tech](https://my.woshicai.tech)

**资料：**
- [Anthropic API Docs](https://docs.anthropic.com/en/api)
- [OpenAI API Docs](https://platform.openai.com/docs)

### RAG（检索增强生成）

> 📖 完整学习指南：[RAG 检索增强生成](../notes/rag)（原理、进阶技术、三种实现方案对比、选型建议、资料合集）

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

### 系统化实践：从 LLM API 到工作流 Agent

面向后端开发者，以 Python 为主要语言，从 LLM API 基础逐步走到工作流自动化 Agent。学习原则是**先用原生 SDK 理解协议和控制流，再引入框架**；LangGraph / LangChain 放在后续 RAG Agent 模块中作对比，而不是一开始就依赖框架。

**9 个渐进式模块：**

1. LLM API 基础 → 2. Tool 定义 → 3. Tool 执行 → 4. Agent 循环（ReAct、追踪与上下文管理）→ 5. MCP → 6. 工作流 Agent（状态机与人机协作）→ 7. RAG 基础（Embedding、ChromaDB）→ 8. RAG Agent（含 LangGraph 对比）→ 9. DevOps 助手综合项目（评估与可观测性）。

> **当前实践进度：**已有代码和练习集中在 Module 01、02；Module 03–09 是后续学习计划，尚未实现。技术栈使用 Python 3.12、uv、Anthropic / OpenAI SDK 与 Pydantic v2，后续计划引入 MCP Python SDK、ChromaDB 和 LangGraph / LangChain。

**已整理内容与关键收获：**

- **Module 01：LLM API 基础。** 对比 Claude Messages、OpenAI Chat Completions 与 Responses API；理解 API 无状态时需要由客户端重发历史，以及 Responses API 有状态链和无状态重放的取舍。消息内容是文本、图片等类型化 block 的列表，`tool_use` / `tool_result` 也是这套协议的延伸。流式传输基于 HTTP + SSE，适合面向人的交互；代码消费完整结果时通常用单次请求更简单。不同 Provider 的 system prompt、输出上限参数和响应结构也需要分别处理。
- **Module 02：Tool 定义。** Function Calling 不是模型执行代码：模型只根据工具说明生成工具名和参数，应用负责校验、执行，并把结果交回模型。课程从手写 JSON Schema 开始，再用 Pydantic 生成参数 schema，并通过装饰器和注册表管理工具；同时认识 Claude 与 OpenAI 工具格式的差异。现阶段重点是定义与注册，完整执行循环属于后续模块。
- **练习与验证。** Module 01 的练习覆盖多轮对话、system prompt、流式聊天、Responses API 两种历史管理方式和图片输入；Module 02 练习覆盖复杂参数 schema、注册表改进及 Provider 格式转换。课程倾向通过运行代码观察 token 用量、网关兼容性和模型差异，而不只停留在概念阅读。

#### Module 01：6 个示例脚本

这些脚本位于独立实践项目的 `01_llm_basics/src/`，需要相应 Provider 的 API Key 和可用模型；以下路径和命令不是本资料站内的可执行文件。

| 脚本 | 实际演示内容 | 运行时重点观察 |
|------|--------------|----------------|
| `hello_claude.py` | 创建 Anthropic 客户端；调用 `messages.create()`；遍历 text block；打印 usage、停止原因与模型；再用独立 `system` 参数切换为海盗角色 | `input_tokens` / `output_tokens`、`stop_reason`、system prompt 如何影响回答 |
| `hello_openai.py` | 创建 OpenAI 客户端；调用 Chat Completions；读取 `choices[0].message.content`；打印 usage 与结束原因；在消息列表中加入 system 角色 | 与 Claude 的响应结构、参数名和 system 位置差异 |
| `multi_turn.py` | 分别用两个 Provider 演示三轮固定对话：自我介绍 → 追问姓名和编程语言 → 请求对应语言的 Hello World；逐轮追加 user 与 assistant 历史 | 模型的“记忆”来自重发历史；这是固定场景演示，不是交互式 CLI 聊天程序 |
| `streaming.py` | Claude 用 `messages.stream()` + `text_stream` 实时打印，并读取最终消息中的输出 token；OpenAI 用 `stream=True` 遍历文本 delta | 两种 SDK 的流式接口差异；OpenAI 示例未请求 usage 帧，不能把它当作完整的流式计费统计实现 |
| `responses_api.py` | 三个 Demo：基础调用与 output item 类型检查、有状态多轮、无状态重放；有状态第二轮遇到 `BadRequestError` 后打印说明，继续无状态 Demo | `previous_response_id` 对服务端存储的依赖；重放时包含原问题、完整 `output` items 与新问题；端点必须支持 Responses API，而不只是兼容 Chat Completions |
| `multimodal.py` | 内置一张 128×128 PNG 的 base64 数据；分别组装 OpenAI 的 `image_url` data URI 和 Claude 的 image/source block；对比描述和输入 token；两个 Provider 独立容错 | 图片块与文本块的组合、模型视觉差异，以及图片对 token 消耗的影响；换成自己的图片是练习内容 |

**建议运行顺序（在独立实践项目根目录执行）：**

```bash
uv sync
cp .env.example .env
# 在 .env 中配置 API Key、模型，以及可选的自定义端点；不要提交真实密钥

uv run python 01_llm_basics/src/hello_claude.py
uv run python 01_llm_basics/src/hello_openai.py
uv run python 01_llm_basics/src/multi_turn.py
uv run python 01_llm_basics/src/streaming.py
uv run python 01_llm_basics/src/responses_api.py
uv run python 01_llm_basics/src/multimodal.py
```

#### Module 01：5 个动手练习

练习目录目前提供任务说明，没有额外的独立解答脚本。

1. **模型回答对比。** 把“微服务与单体架构的区别”分别交给 Claude 和 OpenAI，打印回答与 token 使用量，比较风格、内容和成本。
2. **System prompt 对比。** 对同一个 Docker 问题使用初学者老师、高级架构师、段子手三种角色，观察回答变化。
3. **交互式 CLI 聊天。** 结合 `multi_turn.py` 的历史管理与 `streaming.py` 的实时输出，自己实现持续对话、输入 `quit` 退出、逐轮显示 token。注意 OpenAI 流式统计还需请求 usage 帧并解析结果。
4. **Responses 多轮对比。** 分别实现 `previous_response_id` 链和 output→input 重放，观察第二轮输入 token；进一步尝试 `store=False`、删除历史片段，理解服务端状态与客户端控制权的取舍。
5. **自己的图片输入。** 用 `base64.b64encode(Path(...).read_bytes())` 编码本地图片，分别发给两个 Provider；缩小图片后比较 token，分析远程图片与 base64 输入在隐私、体积及下载责任上的取舍。

**已有完成记录：**Module 01 已收尾；练习 4、5 通过相应示例验证，练习 1–3 没有独立打卡，只记录为核心知识点已由示例覆盖。不能据此认定交互式 CLI 练习已经实现。

**实测经验：**所用中转网关在有状态链上返回 `previous_response_not_found`，但无状态重放成功；同一测试图片在当时两个模型上的识别结果不同。它们是特定端点和模型版本的观察，不是所有网关或模型的通用结论。

#### Module 02：3 个示例脚本

这些脚本位于 `02_tool_definition/src/`，均可在本地展示，不需要调用 LLM API。

| 脚本 | 实际演示内容 | 核心实现与边界 |
|------|--------------|----------------|
| `basic_tools.py` | 手写天气与文档搜索 schema，输出 Claude / OpenAI 格式，并对比外层包装 | 学习 `properties`、`required`、`enum`、`default`；脚本只展示定义，没有把工具发送给模型，也没有执行工具 |
| `pydantic_tools.py` | 定义天气、文档搜索输入模型；包含温度枚举、可选分类与 1–20 的结果数约束；生成两种 Provider 格式；验证正常参数和缺少必填字段的失败案例 | `Field` 提供说明和约束，`model_json_schema()` 生成 schema，`model_validate()` 校验模拟模型输出 |
| `tool_registry.py` | 用装饰器注册天气、计算器、知识库搜索；输出两种 Provider 格式；按名称本地执行工具 | `inspect.signature()` + `get_type_hints()` 提取签名，`create_model()` 生成参数模型；保留函数引用和默认值，支持自定义工具名。天气与知识库搜索是模拟实现，计算器是本地运算 |

```bash
uv run python 02_tool_definition/src/basic_tools.py
uv run python 02_tool_definition/src/pydantic_tools.py
uv run python 02_tool_definition/src/tool_registry.py
```

**注册表需要特别理解的边界：**当前 `execute()` 直接调用 Python 函数，并没有用生成的参数模型自动校验输入；生成 schema 不等于运行时验证。它也还没有模型驱动的完整执行循环、重试、超时或工具沙箱。参数说明目前是通用的 `Parameter: 参数名`，工具 description 仍需显式传入。

#### Module 02：3 个扩展练习

这些是待动手完成的任务说明，仓库未提供对应独立解答或完成记录。

1. **复杂工具参数。** 用 Pydantic 定义 `create_github_issue`：必填 `title`、`body`，可选 `labels` 字符串列表、`priority`（low / medium / high / critical）和 `assignee`；生成两种 Provider 格式，验证模拟模型输出。任务重点是参数定义，不代表已实现真实 GitHub Issue 创建。
2. **改进注册中心。** 从函数 docstring 提取参数说明，并允许省略装饰器的 description，改用 docstring 作为工具说明。
3. **双向格式转换。** 实现 `convert_openai_to_claude(tools)` 与 `convert_claude_to_openai(tools)`，保留内部 schema，仅转换外层包装。

#### 共享设施与离线测试

- `shared/config.py`：通过 Pydantic Settings 加载项目根目录的 `.env` 和环境变量；API Key 使用 `SecretStr`，检测未配置或占位符密钥，把空白自定义端点归一化为 `None`，缺少 Key 时给出明确报错。
- `shared/llm_client.py`：缓存同步 / 异步 Anthropic 与 OpenAI 客户端，处理密钥和自定义端点初始化；刻意保留原生 API 差异，不提供统一对话抽象层。
- `shared/logger.py`：用 Rich 输出步骤、回答面板、工具调用和结果，错误输出走 stderr；存在展示 Agent 思考的辅助函数，但不能据此认为 Agent 循环已实现。
- `tests/test_shared.py`：5 个测试覆盖项目根目录、配置默认值、密钥检测、环境变量端点和空白端点处理；通过隔离 `.env` / 环境变量避免本机配置干扰测试。
- `02_tool_definition/tests/test_tool_registry.py`：5 个测试覆盖注册、本地执行、两种 Provider 格式和 schema 必填字段。这些测试不需要 API Key，但没有覆盖真实模型调用或执行前参数校验。

```bash
uv sync --extra dev
# pytest 默认只收集根目录 tests/，必须显式传入 Module 02 的测试目录
uv run pytest tests 02_tool_definition/tests
```

**与本路线的衔接：**这套材料可补充本阶段的 LLM API、Tool Use、Agent 和 MCP 学习。尤其可用 Module 01 巩固消息与 API 范式，用 Module 02 建立工具 schema 的基础；但要完成本路线里的 Tool Use / Function Calling，还需继续学习工具执行与 Agent 循环（Modules 03–04）。RAG 对应 Modules 07–08，属于后续计划。

---

## 第三阶段：副业深耕（第 7-16 周）

> 🎯 **主线：AI 互动小说 / 视觉小说 MVP** —— 三个方向（游戏 / 小说 / 生图）的交叉点，也是「先 niche 后扩展」里那个 niche：一个人能完成的产品。A/B/C 三条轨道不并行推进，而是作为主线的技能储备，按 MVP 各阶段需要逐项解锁。

### 主线：AI 互动小说 / 视觉小说

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

**MVP 计划（第 7-16 周）：**

- [ ] 第 7-8 周：ComfyUI 出角色立绘 + 场景图（← 轨道 C）
- [ ] 第 9-10 周：Claude API + RAG 做剧情生成管线（← 轨道 B + 第二阶段 RAG）
- [ ] 第 11-12 周：Godot 搭建游戏框架（← 轨道 A）
- [ ] 第 13-14 周：集成 AI 管线，做出可玩 Demo
- [ ] 第 15-16 周：发布 itch.io / Steam 收集反馈
- [ ] 发布前：调研 Steam AI 内容披露要求（2024 起强制）与 itch.io AI 政策

---

### 技能轨道 A：AI 游戏开发（服务主线）

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

### 技能轨道 B：AI 创作小说（服务主线）

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

### 技能轨道 C：AI 生图（服务主线）

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

- Mac Mini（本地开发）— Apple Silicon（M 系列），统一内存架构
- GPU：集成 GPU、无 CUDA → 本地跑 SD / 小模型可行但慢，批量出图走云端（Replicate）

### 云服务

| 服务 | 用途 | 月预算参考* |
|------|------|------------|
| GLM API | LLM 调用（web chat 已在用） | ¥10-50 |
| Anthropic API | LLM 调用（写作管线主力） | $10-30 |
| Replicate | 云端 SD 出图（无 GPU 替代） | $5-20 |
| Pinecone / pgvector | 向量数据库 | $0（pgvector 自托管） |
| Cloudflare Pages / Workers | 应用部署（web chat 已在用） | $0（免费额度内） |

\* 初始参考值；副业项目对 API 成本敏感，每月按实际账单回填复盘。

---

## 变现路径总览

```
M1: 提升主业效率 → 涨薪/跳槽溢价
    ↓
M2: 做 AI 工具 → SaaS 订阅收入
    ↓
M3: AI 互动小说/游戏 → 平台分成/直接销售
    ↓
M4: 多个产品组合 → One Person Company
```

> M = Milestone（变现里程碑），与学习阶段（第一~四阶段）、项目阶段（web chat 的 Phase 1-3）区分。

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
| 2026-06-29 | Web AI NPC 聊天 Phase 1-3 实施完成并上线 my.woshicai.tech | [实现记录](../references/web-chat/) |
| 2026-06-29 | 本站（VitePress）上线 GitHub Pages | - |
| 2026-10-29 | RAG 调研更新：2026 技术版图五路线对比 | [RAG 笔记](../notes/rag) |

---

## 避坑指南

- ❌ 不要从数学/理论开始 — 你不是算法工程师
- ❌ 不要学 TensorFlow/PyTorch 底层 — 99% 场景用 API 就够了
- ❌ 不要追每个新框架 — LangChain/LlamaIndex/CrewAI 变化极快，学原理不学框架
- ❌ 不要只看不动手 — AI 领域一周不写代码就落后
- ✅ 先 API 后框架 — 原生 API 调通后再引入框架
- ✅ 先产品后优化 — MVP 快速上线验证，不要追求完美
- ✅ 先 niche 后扩展 — 找到一个细分点做到极致
