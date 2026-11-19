"""
统一日志模块.

使用 rich 提供美观的终端输出，适合学习项目的演示效果。

用法:
    from shared.logger import get_logger, print_step, print_response

    logger = get_logger(__name__)
    logger.info("Starting agent...")

    # 演示用的格式化输出
    print_step("Calling Claude API...")
    print_response("Claude", "Hello! How can I help?")
"""

import logging

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.text import Text

from shared.config import settings

# Rich console 单例
console = Console()
# 错误输出专用 console（写入 stderr，不影响正常输出管道）
error_console = Console(stderr=True)


def get_logger(name: str) -> logging.Logger:
    """获取带 Rich 格式的 logger."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = RichHandler(
            console=console,
            show_time=True,
            show_path=False,
            rich_tracebacks=True,
        )
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)

    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
    return logger


def print_step(message: str, step_num: int | None = None) -> None:
    """打印步骤信息（用于演示脚本）."""
    prefix = f"Step {step_num}" if step_num else "→"
    console.print(f"\n[bold cyan]{prefix}:[/bold cyan] {message}")


def print_response(provider: str, content: str) -> None:
    """打印 LLM 响应（带美观格式）."""
    color = "green" if provider.lower() == "claude" else "blue"
    panel = Panel(
        Text(content),
        title=f"[bold {color}]{provider} Response[/bold {color}]",
        border_style=color,
        padding=(1, 2),
    )
    console.print(panel)


def print_tool_call(tool_name: str, args: dict) -> None:  # type: ignore[type-arg]
    """打印 Tool 调用信息."""
    console.print(f"\n[bold yellow]🔧 Tool Call:[/bold yellow] {tool_name}")
    console.print(f"   [dim]Args: {args}[/dim]")


def print_tool_result(tool_name: str, result: str) -> None:
    """打印 Tool 执行结果."""
    console.print(f"[bold green]✅ Tool Result:[/bold green] {tool_name}")
    console.print(f"   [dim]{result[:200]}{'...' if len(result) > 200 else ''}[/dim]")


def print_thinking(thought: str) -> None:
    """打印 Agent 思考过程（ReAct 模式）."""
    console.print(f"\n[bold magenta]💭 Thinking:[/bold magenta] {thought}")


def print_error(message: str) -> None:
    """打印错误信息."""
    error_console.print(f"\n[bold red]❌ Error:[/bold red] {message}")


def print_separator() -> None:
    """打印分隔线."""
    console.print("[dim]" + "─" * 60 + "[/dim]")
