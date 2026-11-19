"""
用 Pydantic 自动生成 Tool Schema — 更优雅的方式.

学习要点:
  1. Pydantic 模型可以自动生成 JSON Schema
  2. Field() 的 description 会出现在 schema 中
  3. 类型注解自动映射为 JSON Schema 类型

运行:
  uv run python 02_tool_definition/src/pydantic_tools.py
"""

import json
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

from shared.logger import console, print_separator, print_step

# ============================================================
# Step 1: 用 Pydantic 定义 Tool 的输入参数
# ============================================================
print_step("用 Pydantic 定义 Tool 参数", step_num=1)


class TemperatureUnit(str, Enum):
    """温度单位."""

    celsius = "celsius"
    fahrenheit = "fahrenheit"


class GetWeatherInput(BaseModel):
    """获取天气的输入参数."""

    location: str = Field(description="城市名称，如 '北京' 或 'San Francisco, CA'")
    unit: TemperatureUnit = Field(
        default=TemperatureUnit.celsius,
        description="温度单位",
    )


class SearchDocsInput(BaseModel):
    """搜索文档的输入参数."""

    query: str = Field(description="搜索关键词或问题")
    max_results: int = Field(default=5, description="返回的最大结果数", ge=1, le=20)
    category: Literal["api", "tutorial", "faq"] | None = Field(
        default=None,
        description="文档分类过滤",
    )


# ============================================================
# Step 2: 自动生成 JSON Schema
# ============================================================
print_step("自动生成 JSON Schema", step_num=2)

weather_schema = GetWeatherInput.model_json_schema()
console.print("[bold]GetWeatherInput 的 JSON Schema:[/bold]")
console.print_json(json.dumps(weather_schema, ensure_ascii=False))

search_schema = SearchDocsInput.model_json_schema()
console.print("\n[bold]SearchDocsInput 的 JSON Schema:[/bold]")
console.print_json(json.dumps(search_schema, ensure_ascii=False))

# ============================================================
# Step 3: 转换为 Claude 格式的 Tool 定义
# ============================================================
print_step("转换为 Claude Tool 定义", step_num=3)


def pydantic_to_claude_tool(
    name: str,
    description: str,
    model: type[BaseModel],
) -> dict:  # type: ignore[type-arg]
    """将 Pydantic 模型转换为 Claude tool 定义."""
    return {
        "name": name,
        "description": description,
        "input_schema": model.model_json_schema(),
    }


def pydantic_to_openai_tool(
    name: str,
    description: str,
    model: type[BaseModel],
) -> dict:  # type: ignore[type-arg]
    """将 Pydantic 模型转换为 OpenAI tool 定义."""
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": model.model_json_schema(),
        },
    }


claude_tool = pydantic_to_claude_tool(
    name="get_weather",
    description="获取指定城市的当前天气信息",
    model=GetWeatherInput,
)

openai_tool = pydantic_to_openai_tool(
    name="get_weather",
    description="获取指定城市的当前天气信息",
    model=GetWeatherInput,
)

console.print("[bold green]Claude 格式:[/bold green]")
console.print_json(json.dumps(claude_tool, ensure_ascii=False))

console.print("\n[bold blue]OpenAI 格式:[/bold blue]")
console.print_json(json.dumps(openai_tool, ensure_ascii=False))

# ============================================================
# Step 4: 验证输入数据
# ============================================================
print_step("用 Pydantic 验证 LLM 返回的参数", step_num=4)
print_separator()

# 模拟 LLM 返回的参数（JSON 对象）
llm_output = {"location": "北京", "unit": "celsius"}
validated = GetWeatherInput.model_validate(llm_output)
console.print(f"  ✅ 验证通过: location={validated.location}, unit={validated.unit}")

# 模拟缺少必填字段
try:
    bad_output: dict[str, str] = {"unit": "celsius"}  # 缺少 location
    GetWeatherInput.model_validate(bad_output)
except Exception as e:
    console.print(f"  ❌ 验证失败（预期）: {e}")

console.print("\n[bold yellow]要点:[/bold yellow]")
console.print("  Pydantic 既能生成 schema（告诉 LLM 参数格式），")
console.print("  又能验证 LLM 的输出（确保参数正确），一举两得！")
