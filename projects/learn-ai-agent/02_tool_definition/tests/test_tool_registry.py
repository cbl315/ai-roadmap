"""测试 ToolRegistry 核心功能（不需要 API key）."""

import sys
from pathlib import Path

# 把 02_tool_definition/src 加入 path，这样能导入 tool_registry
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from tool_registry import ToolRegistry


def test_tool_registration() -> None:
    """tool 应该能被正确注册."""
    registry = ToolRegistry()

    @registry.tool(description="测试工具")
    def my_tool(x: int, y: str = "hello") -> str:
        return f"{x}: {y}"

    assert "my_tool" in registry.tool_names
    tool = registry.get_tool("my_tool")
    assert tool.name == "my_tool"
    assert tool.description == "测试工具"


def test_tool_execution() -> None:
    """tool 应该能被正确执行."""
    registry = ToolRegistry()

    @registry.tool(description="加法")
    def add(a: int, b: int) -> int:
        return a + b

    result = registry.execute("add", a=3, b=5)
    assert result == 8


def test_claude_format() -> None:
    """应该能生成正确的 Claude 格式."""
    registry = ToolRegistry()

    @registry.tool(description="获取天气")
    def get_weather(location: str) -> str:
        return "sunny"

    tools = registry.get_claude_tools()
    assert len(tools) == 1
    assert tools[0]["name"] == "get_weather"
    assert tools[0]["description"] == "获取天气"
    assert "input_schema" in tools[0]
    assert tools[0]["input_schema"]["type"] == "object"


def test_openai_format() -> None:
    """应该能生成正确的 OpenAI 格式."""
    registry = ToolRegistry()

    @registry.tool(description="获取天气")
    def get_weather(location: str) -> str:
        return "sunny"

    tools = registry.get_openai_tools()
    assert len(tools) == 1
    assert tools[0]["type"] == "function"
    assert tools[0]["function"]["name"] == "get_weather"
    assert "parameters" in tools[0]["function"]


def test_schema_has_required_fields() -> None:
    """必填参数应该出现在 schema 的 required 中."""
    registry = ToolRegistry()

    @registry.tool(description="test")
    def func(required_param: str, optional_param: str = "default") -> str:
        return ""

    schema = registry.get_tool("func").input_schema
    assert "required_param" in schema.get("required", [])
