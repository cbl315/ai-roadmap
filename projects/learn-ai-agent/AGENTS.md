# AI Agent 开发学习项目 — Agent 指引

这是一个 AI Agent 开发学习项目，包含 9 个渐进式模块。

## 项目结构

- `shared/` — 跨模块共享代码（config、llm_client、logger）
- `01_llm_basics/` ~ `09_capstone/` — 9 个学习模块，按顺序递进
- `tests/` — 全局测试
- `docs/` — 本地学习进度看板（`index.html` + `roadmap.js`）

本项目位于 ai-roadmap 的 `projects/learn-ai-agent/`。以下命令在本目录执行；当前实际实现为 Module 01、02，Module 03–09 尚未实现。

## 技术栈

- Python 3.12 + uv
- Anthropic SDK (Claude) + OpenAI SDK (GPT)
- Pydantic v2（类型安全）
- MCP Python SDK（Module 05，工具协议标准）
- ChromaDB（向量数据库，Module 07+）
- LangGraph / LangChain（仅 Module 08 对比学习）

## 开发约定

- 使用 `uv run` 运行脚本：`uv run python 01_llm_basics/src/hello_claude.py`
- API Key 配置在 `.env` 文件中（从 `.env.example` 复制）
- 所有模块共享 `shared/` 下的基础设施代码
- 代码风格：ruff 格式化，mypy 类型检查
- 每个模块都可独立运行，但建议按顺序学习
- 更新学习进度：编辑 `docs/roadmap.js` 中各模块的 `status`（`done` / `doing` / `todo`），本地运行 `uv run python -m http.server 8000` 后在浏览器打开 `/docs/`

## 运行测试

```bash
uv sync --extra dev
uv run pytest tests 02_tool_definition/tests
```

## 常用命令

```bash
# 运行某个模块的示例
uv run python 01_llm_basics/src/hello_claude.py

# 格式化代码
uv run ruff format .

# 类型检查
uv run mypy shared/
```
