"""
手写 JSON Schema 定义 Tool — 理解底层机制.

学习要点:
  1. Claude 和 OpenAI 的 tool 定义格式差异
  2. JSON Schema 的基本语法
  3. 如何把 tool 定义传给 LLM（只是定义，不执行）

运行:
  uv run python 02_tool_definition/src/basic_tools.py
"""

import json

from shared.logger import console, print_separator, print_step

# ============================================================
# Step 1: Claude 格式的 Tool 定义
# ============================================================
print_step("Claude 格式的 Tool 定义", step_num=1)

# Claude 的 tool 定义是平铺的: {name, description, input_schema}
claude_tools = [
    {
        "name": "get_weather",
        "description": "获取指定城市的当前天气信息。当用户询问天气时使用此工具。",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "城市名称，如 '北京' 或 'San Francisco, CA'",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "温度单位，默认 celsius",
                },
            },
            "required": ["location"],
        },
    },
    {
        "name": "search_docs",
        "description": "在文档库中搜索相关内容。当用户提问需要查阅文档时使用。",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词或问题",
                },
                "max_results": {
                    "type": "integer",
                    "description": "返回的最大结果数",
                    "default": 5,
                },
            },
            "required": ["query"],
        },
    },
]

console.print("[bold]Claude Tool 定义:[/bold]")
console.print_json(json.dumps(claude_tools[0], ensure_ascii=False))

# ============================================================
# Step 2: OpenAI 格式的 Tool 定义
# ============================================================
print_step("OpenAI 格式的 Tool 定义", step_num=2)

# OpenAI 多了一层包装: {type: "function", function: {name, description, parameters}}
# 注意: input_schema → parameters
openai_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的当前天气信息。当用户询问天气时使用此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，如 '北京' 或 'San Francisco, CA'",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位，默认 celsius",
                    },
                },
                "required": ["location"],
            },
        },
    },
]

console.print("[bold]OpenAI Tool 定义:[/bold]")
console.print_json(json.dumps(openai_tools[0], ensure_ascii=False))

# ============================================================
# Step 3: 两种格式的核心差异
# ============================================================
print_step("核心差异对比", step_num=3)
print_separator()

console.print("""
[bold]Claude 格式:[/bold]
  {
    "name": "...",
    "description": "...",
    "input_schema": { ... }      ← 扁平结构，schema 在顶层
  }

[bold]OpenAI 格式:[/bold]
  {
    "type": "function",           ← 多了 type 包装
    "function": {
      "name": "...",
      "description": "...",
      "parameters": { ... }       ← 叫 parameters 不叫 input_schema
    }
  }

[bold yellow]结论:[/bold yellow] 内部的 JSON Schema 完全一样，只是外层包装不同。
这就是为什么我们需要一个 provider-agnostic 的 tool 注册中心！
""")
