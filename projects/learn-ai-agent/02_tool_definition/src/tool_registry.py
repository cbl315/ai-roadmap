"""
工具注册中心 — 用装饰器优雅地注册和管理 Tool.

这是整个项目最重要的基础设施之一，后续所有模块都会复用它。

学习要点:
  1. 装饰器模式注册 tool
  2. 从函数签名自动生成 JSON Schema
  3. Provider-agnostic: 同一个 tool 可以输出 Claude 或 OpenAI 格式

运行:
  uv run python 02_tool_definition/src/tool_registry.py

设计理念:
  我们故意不使用 LangChain 的 @tool 装饰器，而是自己实现。
  这样你能理解"注册一个 tool"到底做了什么：
  1. 记录函数引用
  2. 从类型注解提取 JSON Schema
  3. 提供执行入口
"""

import inspect
import json
from collections.abc import Callable
from typing import Any, get_type_hints

from pydantic import BaseModel, Field, create_model

from shared.logger import console, print_separator, print_step


class ToolInfo(BaseModel):
    """一个注册的 Tool 的完整信息."""

    name: str
    description: str
    input_schema: dict[str, Any]
    fn: Callable[..., Any] = Field(exclude=True)  # 实际的函数引用，不序列化

    model_config = {"arbitrary_types_allowed": True}

    def to_claude_format(self) -> dict[str, Any]:
        """转换为 Claude API 的 tool 定义格式."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }

    def to_openai_format(self) -> dict[str, Any]:
        """转换为 OpenAI API 的 tool 定义格式."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_schema,
            },
        }

    def execute(self, **kwargs: Any) -> Any:
        """执行这个 tool."""
        return self.fn(**kwargs)


class ToolRegistry:
    """工具注册中心 — 管理所有可用的 tool.

    用法:
        registry = ToolRegistry()

        @registry.tool(description="获取天气")
        def get_weather(location: str, unit: str = "celsius") -> str:
            return f"{location}: 晴天 25°C"

        # 获取所有 tool 的定义（Claude 格式）
        tools = registry.get_claude_tools()

        # 根据名称执行 tool
        result = registry.execute("get_weather", location="北京")
    """

    def __init__(self) -> None:
        self._tools: dict[str, ToolInfo] = {}

    def tool(
        self,
        description: str,
        name: str | None = None,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """装饰器：注册一个函数为 tool.

        Args:
            description: tool 的描述（LLM 根据这个判断何时使用）
            name: tool 名称，默认使用函数名

        Example:
            @registry.tool(description="获取天气信息")
            def get_weather(location: str) -> str:
                ...
        """

        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            tool_name = name or fn.__name__
            schema = self._build_schema(fn)

            self._tools[tool_name] = ToolInfo(
                name=tool_name,
                description=description,
                input_schema=schema,
                fn=fn,
            )
            return fn

        return decorator

    def get_tool(self, name: str) -> ToolInfo:
        """获取指定名称的 tool."""
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found. Available: {list(self._tools.keys())}")
        return self._tools[name]

    def get_claude_tools(self) -> list[dict[str, Any]]:
        """获取所有 tool 的 Claude 格式定义."""
        return [t.to_claude_format() for t in self._tools.values()]

    def get_openai_tools(self) -> list[dict[str, Any]]:
        """获取所有 tool 的 OpenAI 格式定义."""
        return [t.to_openai_format() for t in self._tools.values()]

    def execute(self, name: str, **kwargs: Any) -> Any:
        """根据名称执行 tool."""
        return self.get_tool(name).execute(**kwargs)

    @property
    def tool_names(self) -> list[str]:
        """所有已注册的 tool 名称."""
        return list(self._tools.keys())

    def _build_schema(self, fn: Callable[..., Any]) -> dict[str, Any]:
        """从函数签名自动生成 JSON Schema.

        这是注册中心的核心 — 把 Python 类型注解转换为 JSON Schema。
        """
        sig = inspect.signature(fn)
        hints = get_type_hints(fn)

        # 动态构建 Pydantic 模型的字段
        fields: dict[str, Any] = {}
        for param_name, param in sig.parameters.items():
            if param_name in ("self", "cls"):
                continue

            param_type = hints.get(param_name, str)

            # 处理默认值
            if param.default is inspect.Parameter.empty:
                # 必填参数
                fields[param_name] = (param_type, Field(description=f"Parameter: {param_name}"))
            else:
                # 可选参数
                fields[param_name] = (
                    param_type,
                    Field(default=param.default, description=f"Parameter: {param_name}"),
                )

        # 用 Pydantic create_model 动态创建模型
        model = create_model(f"{fn.__name__}_Input", **fields)
        return model.model_json_schema()


# ============================================================
# 演示：使用注册中心
# ============================================================

# 创建全局注册中心实例
registry = ToolRegistry()


# 用装饰器注册 tool
@registry.tool(description="获取指定城市的当前天气信息")
def get_weather(location: str, unit: str = "celsius") -> str:
    """获取天气（模拟实现）."""
    return f"{location}: 晴天, 25°C"


@registry.tool(description="计算两个数的数学运算")
def calculate(a: float, b: float, operation: str = "add") -> float:
    """简单计算器."""
    ops = {"add": a + b, "subtract": a - b, "multiply": a * b, "divide": a / b if b != 0 else 0}
    return ops.get(operation, 0)


@registry.tool(description="在知识库中搜索相关文档")
def search_knowledge_base(query: str, max_results: int = 5) -> str:
    """搜索知识库（模拟实现）."""
    return f"搜索 '{query}' 找到 {max_results} 条结果"


# ============================================================
# 运行演示
# ============================================================
if __name__ == "__main__":
    console.print("[bold]🔧 Tool 注册中心演示[/bold]\n")

    # 查看注册的 tools
    print_step("已注册的 Tools", step_num=1)
    for name in registry.tool_names:
        tool = registry.get_tool(name)
        console.print(f"  • {tool.name}: {tool.description}")

    # 查看 Claude 格式
    print_step("Claude 格式输出", step_num=2)
    claude_tools = registry.get_claude_tools()
    for tool_def in claude_tools:
        console.print(f"\n  [bold green]{tool_def['name']}:[/bold green]")
        console.print_json(json.dumps(tool_def, ensure_ascii=False, indent=2))

    # 查看 OpenAI 格式
    print_step("OpenAI 格式输出", step_num=3)
    openai_tools = registry.get_openai_tools()
    console.print(f"  [dim]共 {len(openai_tools)} 个 tool（格式差异仅在外层包装）[/dim]")
    console.print_json(json.dumps(openai_tools[0], ensure_ascii=False, indent=2))

    # 执行 tool
    print_step("执行 Tool", step_num=4)
    print_separator()

    result1 = registry.execute("get_weather", location="北京")
    console.print(f"  get_weather(location='北京') → {result1}")

    result2 = registry.execute("calculate", a=10, b=3, operation="multiply")
    console.print(f"  calculate(10, 3, 'multiply') → {result2}")

    result3 = registry.execute("search_knowledge_base", query="如何部署", max_results=3)
    console.print(f"  search_knowledge_base('如何部署') → {result3}")

    console.print("\n[bold yellow]要点:[/bold yellow]")
    console.print("  ToolRegistry 是 provider-agnostic 的：")
    console.print("  同一个 @registry.tool 装饰器注册的函数，")
    console.print("  可以输出 Claude 格式 (.get_claude_tools())")
    console.print("  也可以输出 OpenAI 格式 (.get_openai_tools())")
    console.print("  还可以直接执行 (.execute('name', **args))")
