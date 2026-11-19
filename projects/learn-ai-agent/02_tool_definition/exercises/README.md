# Module 02 练习

## 练习 1: 定义一个复杂的 Tool

用 Pydantic 定义一个 `create_github_issue` tool，包含：
- `title`: 必填，字符串
- `body`: 必填，字符串
- `labels`: 可选，字符串列表
- `priority`: 可选，枚举类型 (low/medium/high/critical)
- `assignee`: 可选，字符串

**要求**: 生成 Claude 和 OpenAI 两种格式，并验证模拟的 LLM 输出。

## 练习 2: 扩展 ToolRegistry

给 `ToolRegistry` 添加以下功能：
1. 从函数的 docstring 中提取参数描述（而不是使用通用的 "Parameter: xxx"）
2. 支持 `@registry.tool()` 不传 description 时，使用函数的 docstring 作为描述

## 练习 3: Provider 格式互转

编写一个函数 `convert_openai_to_claude(tools)` 和 `convert_claude_to_openai(tools)`，
实现两种格式之间的互转。

**提示**: 核心 schema 是一样的，只需要处理外层包装的差异。
