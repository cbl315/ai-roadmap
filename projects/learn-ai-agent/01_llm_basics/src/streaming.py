"""
流式输出 — 实时打印 LLM 的回复（像打字机一样）.

学习要点:
  1. 为什么需要流式输出（用户体验、长回复不超时）
  2. Claude 的 messages.stream() context manager
  3. OpenAI 的 stream=True 参数
  4. 流式 vs 非流式的 trade-off
  5. 底层是 HTTP + SSE（Server-Sent Events），不是 WebSocket —— 详见模块 README 4.1 节
  6. 流式 vs 单次怎么选（谁在消费输出: 人眼 → 流式，代码 → 单次）—— 详见 4.2 节

运行:
  uv run python 01_llm_basics/src/streaming.py
"""

from shared.config import settings
from shared.llm_client import get_claude_client, get_openai_client
from shared.logger import console, print_separator, print_step


def claude_streaming() -> None:
    """Claude 流式输出 — 使用 messages.stream() context manager."""
    console.print("\n[bold green]═══ Claude 流式输出 ═══[/bold green]\n")
    client = get_claude_client()

    print_step("开始流式请求")
    console.print("  [bold green]Claude:[/bold green] ", end="")

    # Claude 推荐使用 messages.stream() context manager
    # 它自动处理连接管理，并提供 text_stream 迭代器
    with client.messages.stream(
        model=settings.claude_model,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "请用 3 个要点解释什么是 RESTful API，每个要点一句话。"}
        ],
    ) as stream:
        # text_stream 只产出文本 delta，最简单的用法
        for text in stream.text_stream:
            print(text, end="", flush=True)  # flush=True 确保实时显示

        # stream 结束后，可以获取完整消息（包含 usage 等元数据）
        final_message = stream.get_final_message()

    print()  # 换行
    print_separator()
    console.print(f"  [dim]输出 tokens: {final_message.usage.output_tokens}[/dim]")


def openai_streaming() -> None:
    """OpenAI 流式输出 — 使用 stream=True 参数."""
    console.print("\n[bold blue]═══ OpenAI 流式输出 ═══[/bold blue]\n")
    client = get_openai_client()

    print_step("开始流式请求")
    console.print("  [bold blue]OpenAI:[/bold blue] ", end="")

    # OpenAI 通过 stream=True 参数开启流式
    stream = client.chat.completions.create(
        model=settings.openai_model,
        max_completion_tokens=1024,  # GPT-5/o 系列必需；旧模型两者皆可
        messages=[
            {"role": "user", "content": "请用 3 个要点解释什么是 RESTful API，每个要点一句话。"}
        ],
        stream=True,
    )

    # 遍历流式 chunks
    for chunk in stream:
        # 每个 chunk 可能包含内容 delta
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

    print()  # 换行


# ============================================================
# 运行演示
# ============================================================
if __name__ == "__main__":
    console.print("[bold]🌊 流式输出演示[/bold]")
    console.print("[dim]核心概念: 流式输出让用户实时看到回复，提升体验[/dim]")
    console.print(
        "[dim]对比: Claude 用 messages.stream() + text_stream, OpenAI 用 stream=True[/dim]\n"
    )

    if settings.has_anthropic:
        claude_streaming()
    else:
        console.print("[yellow]跳过 Claude（未配置 ANTHROPIC_API_KEY）[/yellow]")

    if settings.has_openai:
        openai_streaming()
    else:
        console.print("[yellow]跳过 OpenAI（未配置 OPENAI_API_KEY）[/yellow]")
