// 本地学习进度数据 —— 修改 status 后刷新 docs/index.html
// status 取值: "done" 已完成 | "doing" 进行中 | "todo" 未开始
const ROADMAP = {
  updatedAt: "2026-10-17",
  repoBase: "../",

  phases: [
    { id: 1, name: "基础能力", range: "01–02", desc: "LLM API 与 Tool 的基本盘" },
    { id: 2, name: "Agent 核心", range: "03–05", desc: "从工具调用到自主循环", core: true },
    { id: 3, name: "工作流 & RAG", range: "06–08", desc: "编排、检索与知识增强" },
    { id: 4, name: "实战", range: "09", desc: "综合项目收尾" },
  ],

  modules: [
    {
      id: "01", dir: "01_llm_basics", title: "LLM 基础", phase: 1, status: "done", doneAt: "2026-10-17",
      topics: [
        "Claude / OpenAI API 与多轮对话",
        "流式输出（HTTP + SSE）与选型",
        "Chat vs Responses API 范式",
        "多模态：content 块列表",
      ],
    },
    {
      id: "02", dir: "02_tool_definition", title: "Tool 定义", phase: 1, status: "doing",
      topics: ["JSON Schema 工具定义", "Pydantic v2", "Tool Registry"],
    },
    {
      id: "03", dir: "03_tool_execution", title: "Tool 执行", phase: 2, status: "todo",
      topics: ["完整执行循环", "错误处理与重试", "结果回传模型"],
    },
    {
      id: "04", dir: "04_agentic_loop", title: "Agent 循环", phase: 2, status: "todo", core: true,
      topics: ["ReAct 与 agentic loop", "逐轮追踪与 token 统计", "上下文截断与压缩"],
    },
    {
      id: "05", dir: "05_mcp", title: "MCP 协议", phase: 2, status: "todo",
      topics: ["手写 MCP Server", "stdio 传输", "接入 ZCode 等真实客户端"],
    },
    {
      id: "06", dir: "06_workflow_agent", title: "工作流 Agent", phase: 3, status: "todo",
      topics: ["状态机编排", "Human-in-the-Loop", "危险操作防护"],
    },
    {
      id: "07", dir: "07_rag_fundamentals", title: "RAG 基础", phase: 3, status: "todo",
      topics: ["Embedding", "ChromaDB", "检索管道"],
    },
    {
      id: "08", dir: "08_rag_agent", title: "RAG Agent", phase: 3, status: "todo",
      topics: ["RAG as Tool", "LangGraph 编排对比"],
    },
    {
      id: "09", dir: "09_capstone", title: "Capstone", phase: 4, status: "todo",
      topics: ["DevOps 工作流助手", "评估 (evals)", "可观测性"],
    },
  ],

  advanced: [
    "多 Agent 协作（编排 · 消息传递 · A2A）",
    "长期记忆与上下文工程",
    "Agent 评估（固定场景回归 · LLM-as-judge）",
    "生产化（限流 · 重试 · 成本控制 · 工具沙箱）",
  ],

  // 模块思维导图（path 相对于 docs/，即 Pages 站点根目录）
  mindmaps: [
    { module: "01", title: "LLM API 基础", path: "images/module01-mindmap.png" },
  ],
};
