# 🤖 AI Agent 开发学习项目

> 从 LLM API 基础到完整的工作流自动化 Agent —— 面向后端开发者的系统学习路径

> 本项目已迁入 ai-roadmap 的 `projects/learn-ai-agent/`，包含全部现有源码、练习说明、共享设施与测试。
> 当前已提供 Module 01、02；Module 03–09 是后续计划，下面的路线和目录树不代表它们已经实现。
> 📈 **本地学习进度看板**：在本目录执行 `uv run python -m http.server 8000`，浏览器打开本地服务的 `/docs/` 路径；更新进度编辑 `docs/roadmap.js`。看板不是独立 GitHub Pages 部署。

## 🎯 项目目标

通过 **9 个渐进式模块**，系统学习 AI Agent 开发的核心技术：

- ✅ LLM API 调用（Claude & OpenAI）
- ✅ Function Calling / Tool Use
- ✅ Agentic Loop（多步推理 + 追踪 + 上下文管理）
- ✅ MCP（Model Context Protocol，工具协议标准）
- ✅ 工作流编排 + Human-in-the-Loop
- ✅ RAG（检索增强生成）
- ✅ 完整的工作流自动化 Agent（含评估与可观测性）

## 📚 学习路线图

```
Phase 1: 基础能力 (01-02) → Phase 2: Agent 核心 ⭐ (03-05) → Phase 3: 工作流 & RAG (06-08) → Phase 4: 实战 (09)

┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ 01 LLM 基础  │→│ 02 Tool 定义 │→│ 03 Tool 执行 │→│ 04 Agent 循环│→│ 05 MCP 协议  │
│              │  │              │  │              │  │   (核心！)   │  │              │
│ Claude/OpenAI│  │ JSON Schema  │  │ 完整循环     │  │ ReAct 模式   │  │ MCP Server   │
│ 流式/多轮    │  │ Pydantic     │  │ 错误处理     │  │ 追踪+上下文  │  │ 接入客户端   │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  └──────┬───────┘
                                                                                 │
                                                                                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ 09 Capstone  │←│ 08 RAG Agent │←│ 07 RAG 基础  │←│ 06 工作流    │
│              │  │              │  │              │  │              │
│ DevOps 助手  │  │ RAG as Tool  │  │ Embedding    │  │ 状态机       │
│ 评估+可观测  │  │ LangGraph    │  │ ChromaDB     │  │ 人机协作     │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

## 🏗️ 技术栈

| 类别 | 选择 | 说明 |
|---|---|---|
| 语言 | Python 3.12 | AI/ML 生态最丰富 |
| 包管理 | uv | 快速现代化 Python 包管理 |
| LLM | Anthropic + OpenAI | 两大主流 Provider 都学 |
| 向量库 | ChromaDB | 本地运行，零配置 |
| 类型 | Pydantic v2 | Tool Schema + 数据验证 |
| 工具协议 | MCP Python SDK | Module 05，工具集成的事实标准 |
| 框架 | LangGraph / LangChain (Module 08) | 作为编排框架对比学习，点到为止 |

## 🚀 快速开始

### 1. 环境准备

```bash
# 从 ai-roadmap 仓库根目录进入实践项目
cd projects/learn-ai-agent

# 安装依赖
uv sync

# 配置 API Key
cp .env.example .env
# 编辑 .env 填入你的 ANTHROPIC_API_KEY 和 OPENAI_API_KEY
```

### 2. 运行第一个示例

```bash
# Hello Claude!
uv run python 01_llm_basics/src/hello_claude.py

# Hello OpenAI!
uv run python 01_llm_basics/src/hello_openai.py
```

### 3. 离线测试

```bash
uv sync --extra dev
uv run pytest tests 02_tool_definition/tests
```

显式传入两个测试目录：默认 pytest 配置只收集根目录 `tests/`。这些测试不调用 LLM，不需要 API Key。API 示例会产生真实请求与相应费用。

### 4. 按顺序学习

每个模块包含：
- 📖 `README.md` — 理论讲解（先读这个！）
- 💻 `src/` — 可运行的示例代码
- ✏️ `exercises/` — 动手练习任务说明（当前没有独立解答脚本）

## 📂 项目结构

```
learn-ai-agent/
├── shared/              # 共享基础设施
├── 01_llm_basics/       # LLM API 基础
├── 02_tool_definition/  # Tool/Function 定义
├── 03_tool_execution/   # Tool 执行循环
├── 04_agentic_loop/     # Agent 循环 ⭐（含追踪、上下文管理）
├── 05_mcp/              # MCP：把工具封装为标准协议服务
├── 06_workflow_agent/   # 工作流 Agent
├── 07_rag_fundamentals/ # RAG 基础
├── 08_rag_agent/        # RAG Agent + LangGraph 对比
├── 09_capstone/         # DevOps 助手 (综合项目 + 评估)
├── tests/               # 测试
└── docs/                # 本地学习进度看板
```

## 🔑 核心理念

**先原生 SDK，后框架。** 本项目先用 Anthropic/OpenAI 原生 SDK 理解底层原理，Module 08 才引入 LangGraph/LangChain 做对比。理解了 `tool_use` 的消息协议和 agentic loop 的 while 循环后，任何框架都只是语法糖。

## 💡 学习节奏建议

- **01–03 快速通过**：概念相对简单，跑通示例、做完练习即可前进，不必追求完美
- **04 多花时间**：agentic loop 是整个项目的核心，值得反复迭代——加上逐轮追踪（消息/token 消耗）、上下文截断与压缩、固定场景回归测试
- **05 学完原生立刻学 MCP**：手写 Tool 之后马上理解协议标准，并用真实客户端（ZCode / Claude Desktop 等）验证打通
- **09 优先跑通最小闭环**：先让 DevOps 助手端到端可用，再逐步补评估与可观测性

## 🧭 进阶方向（Capstone 之后）

- 多 Agent 协作（编排、消息传递、A2A 协议）
- 长期记忆与上下文工程
- Agent 评估（固定场景回归、LLM-as-judge）
- 生产化：限流、重试、成本控制、工具沙箱
