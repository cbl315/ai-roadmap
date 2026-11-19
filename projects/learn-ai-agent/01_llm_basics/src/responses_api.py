"""
Responses API — OpenAI 的第二代 API 范式（对比 Chat Completions）.

学习要点:
  1. responses.create() 的基本调用（input 而不是 messages）
  2. output 是 item 列表（message / reasoning / function_call...），而不只是 message
  3. 有状态多轮: previous_response_id（服务端记住历史，客户端只发新消息）
  4. 无状态重放: 把 output items 塞回 input（Agent 框架的常用姿势）

运行:
  uv run python 01_llm_basics/src/responses_api.py
"""

from openai import BadRequestError, OpenAI

from shared.config import settings
from shared.llm_client import get_openai_client
from shared.logger import console, print_error, print_response, print_separator, print_step


def demo_basic(client: OpenAI) -> None:
    """Demo 1: 基本调用 — input 进，item 列表出."""
    console.print("\n[bold blue]═══ Demo 1: 基本调用 ═══[/bold blue]\n")

    # 对比 chat.completions.create():
    # - 参数是 input（字符串或 item 列表），不是 messages
    # - max_output_tokens 而不是 max_tokens/max_completion_tokens
    # - 推理模型（GPT-5/o 系列）会把一部分输出预算花在 reasoning 上，所以给宽松些
    response = client.responses.create(
        model=settings.openai_model,
        max_output_tokens=2048,
        input="用一句话介绍你自己，你是谁？",
    )

    # 最简单的取文本方式（等价于拼接 output 里所有的 output_text）
    print_response("OpenAI Responses", response.output_text)

    # output 是一个 item 列表 —— 与 Chat Completions 最大的结构差异。
    # Chat Completions 只返回一条 message；Responses 的 item 可以是
    # message / reasoning / function_call / function_call_output / web_search_call ...
    # 这个设计为多步 agentic 交互准备了统一容器（Module 04 会体会更深）
    print_separator()
    print("output item 结构:")
    for item in response.output:
        print(f"  - type={item.type}, role={getattr(item, 'role', None)}")

    print(f"\n  输入 tokens: {response.usage.input_tokens}")
    print(f"  输出 tokens: {response.usage.output_tokens}")
    print(f"  response id: {response.id}")  # type: ignore[union-attr]  # 下一轮要用它


def demo_stateful(client: OpenAI) -> None:
    """Demo 2: 有状态多轮 — previous_response_id（历史在服务端）."""
    console.print("\n[bold blue]═══ Demo 2: 有状态多轮（previous_response_id）═══[/bold blue]\n")

    # 第一轮：正常的自我介绍
    first = client.responses.create(
        model=settings.openai_model,
        max_output_tokens=2048,
        input="我叫小明，我是一个 Python 开发者。",
    )
    print_step("轮次 1（正常发送）", step_num=1)
    print_response("GPT", first.output_text)

    # 第二轮：注意 —— 只发新消息，不重发历史！
    # 历史存在服务端，通过 previous_response_id 关联成链。
    # 前提: 默认 store=True；设 store=False 则服务端不保存，此路不通。
    print_step("轮次 2（只发送新消息）", step_num=2)
    console.print("  [dim]用户: 你还记得我叫什么名字吗？我的主要编程语言是什么？[/dim]")

    try:
        second = client.responses.create(
            model=settings.openai_model,
            max_output_tokens=2048,
            input="你还记得我叫什么名字吗？我的主要编程语言是什么？",
            previous_response_id=first.id,
        )
    except BadRequestError as e:
        # 很多中转/网关不支持服务端状态: 多上游账号负载均衡、禁用 store、
        # 或根本不落盘 —— 上一轮的 resp_xxx 在下一跳就找不到了。
        # 这正是"有状态链依赖你不控制的基础设施"的现实例证。
        print_separator()
        print_error(f"previous_response_id 被上游拒绝: {str(e)[:160]}")
        console.print(
            "[yellow]你的端点不支持服务端保存 Responses"
            "（多账号负载均衡 / 禁用 store 的网关常见）。[/yellow]"
        )
        console.print(
            "[yellow]这就是有状态链的生态绑定问题 —— 接着看 Demo 3: 无状态重放"
            "不依赖任何服务端状态，在任何 OpenAI 兼容端点都能工作。[/yellow]"
        )
        return

    print_response("GPT", second.output_text)
    print(f"  [dim]输入 tokens: {second.usage.input_tokens}[/dim]")

    print_separator()
    console.print(
        "[dim]💡 看 input_tokens —— 服务端把历史拼回去了，token 照样计费，"
        "只是你不用传了。代价：历史在服务端（有保留期），你想删一段、截断、分支重试都做不到。[/dim]"
    )


def demo_stateless(client: OpenAI) -> None:
    """Demo 3: 无状态重放 — 把 output items 塞回 input（历史在自己手里）."""
    console.print("\n[bold blue]═══ Demo 3: 无状态重放（output → input）═══[/bold blue]\n")

    # 第一轮
    first = client.responses.create(
        model=settings.openai_model,
        max_output_tokens=2048,
        input="我叫小明，我是一个 Python 开发者。",
    )
    print_step("轮次 1（正常发送）", step_num=1)
    print_response("GPT", first.output_text)

    # 第二轮：不靠服务端状态，自己把历史拼回去。
    # input 是 item 列表: 原始问题 + 上一轮模型的完整 output + 新问题
    # 好处: 历史控制权 100% 在你手里 —— 可以截断、修改、删除、分支重试，
    # 这正是 Agent 循环（Module 04）需要的能力，所以 Agent 框架普遍用这种姿势。
    print_step("轮次 2（自己拼接全部历史）", step_num=2)
    second = client.responses.create(
        model=settings.openai_model,
        max_output_tokens=2048,
        input=[
            {"role": "user", "content": "我叫小明，我是一个 Python 开发者。"},
            *first.output,  # 上一轮的完整输出 items
            {"role": "user", "content": "你还记得我叫什么名字吗？"},
        ],
    )
    print_response("GPT", second.output_text)
    print(f"  [dim]输入 tokens: {second.usage.input_tokens}[/dim]")

    print_separator()
    console.print(
        "[dim]💡 对比 Demo 2: 结果一样，但这份历史是你拼的 —— 想在第二轮前删掉"
        "第一轮的某段内容？改这个列表就行。服务端链做不到这一点。[/dim]"
    )


def print_summary() -> None:
    """交互差异总结."""
    print_separator()
    console.print("[bold]Chat Completions vs Responses 交互差异总结:[/bold]")
    summary = [
        ("状态", "每轮重发全部 messages", "previous_response_id 可存服务端"),
        ("结构", "返回一条 message", "返回 item 列表（含 reasoning 等）"),
        ("工具", "function calling，自己执行", "另有平台托管工具（web_search 等）"),
        ("生态", "行业互操作标准", "OpenAI 独有"),
    ]
    for aspect, chat, resp in summary:
        console.print(f"  [bold]{aspect}[/bold]: Chat → {chat}；Responses → {resp}")
    console.print(
        "\n  [dim]本项目主线用 Chat/Messages 学 Agent 循环 —— "
        "状态管理是核心练习；Responses API 做认知储备。[/dim]"
    )


def main() -> None:
    client = get_openai_client()
    demo_basic(client)
    demo_stateful(client)
    demo_stateless(client)
    print_summary()


if __name__ == "__main__":
    main()
