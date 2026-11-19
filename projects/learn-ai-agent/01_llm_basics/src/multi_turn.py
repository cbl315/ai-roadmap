"""
多轮对话 — Claude 和 OpenAI 的对比实现.

学习要点:
  1. API 是无状态的 — 每次请求都要发送完整的对话历史
  2. messages 列表必须 user/assistant 交替
  3. 两个 Provider 的消息格式本质相同，只是 API 调用方式不同

运行:
  uv run python 01_llm_basics/src/multi_turn.py
"""

from shared.config import settings
from shared.llm_client import get_claude_client, get_openai_client
from shared.logger import console, print_response, print_separator, print_step


def claude_multi_turn() -> None:
    """Claude 多轮对话示例."""
    console.print("\n[bold green]═══ Claude 多轮对话 ═══[/bold green]\n")
    client = get_claude_client()

    # API 是无状态的！每次都要发送完整对话历史
    messages: list[dict[str, str]] = []

    conversations = [
        "我叫小明，我是一个 Python 开发者。",
        "你还记得我叫什么名字吗？我的主要编程语言是什么？",
        "帮我用我擅长的语言写一个 hello world。",
    ]

    for i, user_msg in enumerate(conversations, 1):
        print_step(f"轮次 {i}: 用户发言", step_num=i)
        console.print(f"  [dim]用户: {user_msg}[/dim]")

        # 添加用户消息到历史
        messages.append({"role": "user", "content": user_msg})

        # 发送完整对话历史
        response = client.messages.create(
            model=settings.claude_model,
            max_tokens=1024,
            messages=messages,
        )

        # 提取助手回复
        assistant_text = next(
            (block.text for block in response.content if block.type == "text"),
            "",
        )

        # 添加助手回复到历史（下次请求时会带上）
        messages.append({"role": "assistant", "content": assistant_text})

        print_response("Claude", assistant_text)

    # 打印最终的消息历史
    print_separator()
    console.print("[bold]完整对话历史:[/bold]")
    for msg in messages:
        role_color = "cyan" if msg["role"] == "user" else "green"
        console.print(f"  [{role_color}]{msg['role']}:[/{role_color}] {msg['content'][:80]}...")


def openai_multi_turn() -> None:
    """OpenAI 多轮对话示例 — 和 Claude 的模式完全一样."""
    console.print("\n[bold blue]═══ OpenAI 多轮对话 ═══[/bold blue]\n")
    client = get_openai_client()

    messages: list[dict[str, str]] = [
        # OpenAI 的 system prompt 在 messages 里
        {"role": "system", "content": "你是一个友好的助手，回答简洁明了。"},
    ]

    conversations = [
        "我叫小红，我是一个 Java 开发者。",
        "你还记得我叫什么名字吗？我的主要编程语言是什么？",
        "帮我用我擅长的语言写一个 hello world。",
    ]

    for i, user_msg in enumerate(conversations, 1):
        print_step(f"轮次 {i}: 用户发言", step_num=i)
        console.print(f"  [dim]用户: {user_msg}[/dim]")

        messages.append({"role": "user", "content": user_msg})

        response = client.chat.completions.create(
            model=settings.openai_model,
            max_completion_tokens=1024,  # GPT-5/o 系列必需；旧模型两者皆可
            messages=messages,  # type: ignore[arg-type]
        )

        assistant_text = response.choices[0].message.content or ""
        messages.append({"role": "assistant", "content": assistant_text})

        print_response("OpenAI", assistant_text)


# ============================================================
# 运行演示
# ============================================================
if __name__ == "__main__":
    console.print("[bold]📚 多轮对话演示[/bold]")
    console.print("[dim]核心概念: API 是无状态的，每次请求都要发送完整对话历史[/dim]\n")

    # 根据可用的 API Key 运行
    if settings.has_anthropic:
        claude_multi_turn()
    else:
        console.print("[yellow]跳过 Claude（未配置 ANTHROPIC_API_KEY）[/yellow]")

    if settings.has_openai:
        openai_multi_turn()
    else:
        console.print("[yellow]跳过 OpenAI（未配置 OPENAI_API_KEY）[/yellow]")
