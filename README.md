# AI 学习路线 & 副业发展计划

> Backend Developer → AI-Powered One Person Company

🌐 **在线访问**：<https://cbl315.github.io/ai-roadmap/>

整理学习过程中调研的各种资料、总结，以及学习成果的 reference。本 repo 包含**学习路线、资料与 AI Agent 实践代码**；其他应用的实现记录仍放在 references 中。

## 内容结构

| 目录 | 用途 | 示例 |
|------|------|------|
| [`guide/`](./guide/roadmap.md) | 学习路线总览 | 分阶段计划、目标、避坑指南 |
| [`notes/`](./notes/rag.md) | 调研笔记 / 深度资料 | RAG 原理、方案对比、选型建议 |
| [`references/`](./references/web-chat/) | 学习成果 reference | [Web AI NPC 聊天](./references/web-chat/index.md)（Phase 1-3 实现记录、踩坑总结） |
| `projects/learn-ai-agent/` | 可运行的 AI Agent 实践项目 | LLM API、Tool 定义、练习、共享模块与测试 |

## 本地运行

本站基于 [VitePress](https://vitepress.dev/) 构建，部署在 GitHub Pages。包管理器使用 [pnpm](https://pnpm.io/)。

```bash
pnpm install        # 安装依赖
pnpm docs:dev       # 本地预览 http://localhost:5173/ai-roadmap/
pnpm docs:build     # 构建产物到 .vitepress/dist
```

推送到 `main` 分支后，GitHub Actions 会自动构建并发布。

## AI Agent 实践代码

完整代码位于 `projects/learn-ai-agent/`，包含现有 9 个示例脚本、练习说明、共享模块、测试、依赖锁文件与本地进度看板。Modules 03–09 仍是后续计划，练习没有提供额外解答脚本。

```bash
cd projects/learn-ai-agent
uv sync --extra dev
cp .env.example .env
# 编辑 .env 填入 API Key；不要提交真实密钥
uv run python 01_llm_basics/src/hello_claude.py
uv run pytest tests 02_tool_definition/tests
```

Python 实践项目的依赖独立管理，不影响根目录的 pnpm / VitePress 配置。

## 目录说明

```
ai-roadmap/
├── .vitepress/config.mts   # 站点配置（导航/侧边栏/搜索）
├── .github/workflows/      # 自动部署到 GitHub Pages
├── guide/                  # 学习路线
├── notes/                  # 调研笔记
├── references/             # 学习成果
├── projects/learn-ai-agent/ # AI Agent 实践源码与练习
└── index.md                # 站点首页
```
