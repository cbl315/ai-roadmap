# AI 学习路线 & 副业发展计划

> Backend Developer → AI-Powered One Person Company

🌐 **在线访问**：<https://cbl315.github.io/ai-roadmap/>

整理学习过程中调研的各种资料、总结，以及学习成果的 reference。本 repo 只放**学习路线与资料**，具体实现放独立 repo。

## 内容结构

| 目录 | 用途 | 示例 |
|------|------|------|
| [`guide/`](./guide/roadmap.md) | 学习路线总览 | 分阶段计划、目标、避坑指南 |
| [`notes/`](./notes/rag.md) | 调研笔记 / 深度资料 | RAG 原理、方案对比、选型建议 |
| [`references/`](./references/phase2-web-chat.md) | 学习成果 reference | 项目实现记录、踩坑总结 |

## 本地运行

本站基于 [VitePress](https://vitepress.dev/) 构建，部署在 GitHub Pages。包管理器使用 [pnpm](https://pnpm.io/)。

```bash
pnpm install        # 安装依赖
pnpm docs:dev       # 本地预览 http://localhost:5173/ai-roadmap/
pnpm docs:build     # 构建产物到 .vitepress/dist
```

推送到 `main` 分支后，GitHub Actions 会自动构建并发布。

## 目录说明

```
ai-roadmap/
├── .vitepress/config.mts   # 站点配置（导航/侧边栏/搜索）
├── .github/workflows/      # 自动部署到 GitHub Pages
├── guide/                  # 学习路线
├── notes/                  # 调研笔记
├── references/             # 学习成果
├── claude-rules/           # 开发规范（不纳入站点）
└── index.md                # 站点首页
```
