# Module 02: Tool/Function 定义

> 🎯 **学习目标**: 理解 Function Calling 的核心机制，学会定义 Tool，为后续的 Agent 开发打基础

## 📖 理论知识

### 1. 什么是 Function Calling / Tool Use？

LLM 本身只能生成文本。**Function Calling** 让 LLM 能"调用函数"——
实际上，LLM 并不真的执行代码，而是：

1. 你告诉 LLM："这里有一些 tool 可以用"（提供 tool 定义）
2. LLM 分析用户请求后说："我需要调用 `get_weather` 这个 tool，参数是 `{location: '北京'}`"
3. **你的代码**负责执行这个函数调用
4. 你把结果告诉 LLM
5. LLM 根据结果生成最终回复

```
用户: "北京今天天气怎么样？"
    ↓
LLM: "我需要调用 get_weather(location='北京')"  ← LLM 的输出
    ↓
你的代码: 执行 get_weather('北京') → "晴天, 25°C"  ← 你来执行
    ↓
LLM: "北京今天天气晴朗，气温 25°C..."  ← LLM 的最终回复
```

**关键理解**: LLM 不执行任何代码！它只是"建议"调用哪个函数、传什么参数。

### 2. Tool 定义的核心：JSON Schema

Tool 通过 **JSON Schema** 定义，告诉 LLM：
- **name**: 工具名称（LLM 用这个来"调用"）
- **description**: 工具描述（LLM 根据这个判断何时使用）
- **input_schema**: 参数的 JSON Schema（LLM 据此生成正确的参数）

```json
{
  "name": "get_weather",
  "description": "获取指定城市的当前天气信息",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "城市名称，如 '北京' 或 'San Francisco, CA'"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "description": "温度单位"
      }
    },
    "required": ["location"]
  }
}
```

### 3. Claude vs OpenAI 的 Tool 定义差异

| 特性 | Claude (Anthropic) | OpenAI (GPT) |
|------|-------------------|--------------|
| 参数名 | `input_schema` | 包裹在 `function.parameters` 中 |
| 顶层格式 | `{name, description, input_schema}` | `{type: "function", function: {name, description, parameters}}` |
| 响应中的工具调用 | `tool_use` content block | `tool_calls` 数组 |
| 工具调用 ID | `block.id` | `tool_call.id` |

### 4. 用 Pydantic 自动生成 Schema

手写 JSON Schema 容易出错且冗长。Pydantic 模型可以自动生成：

```python
from pydantic import BaseModel, Field

class GetWeather(BaseModel):
    location: str = Field(description="城市名称")
    unit: str = Field(default="celsius", description="温度单位")

# 自动生成 JSON Schema
schema = GetWeather.model_json_schema()
```

### 5. 装饰器模式：优雅的 Tool 注册

最终目标是用装饰器一行代码注册 tool：

```python
@tool(description="获取天气")
def get_weather(location: str, unit: str = "celsius") -> str:
    return f"{location}: 晴天 25°C"
```

## 💻 示例代码

按以下顺序运行：

1. `src/basic_tools.py` — 手写 JSON Schema 定义 tool（理解底层）
2. `src/pydantic_tools.py` — 用 Pydantic 自动生成 schema（更好的方式）
3. `src/tool_registry.py` — 工具注册中心（装饰器模式，后续模块复用）

运行方式：
```bash
uv run python 02_tool_definition/src/basic_tools.py
```

## ✏️ 练习

见 `exercises/README.md`
