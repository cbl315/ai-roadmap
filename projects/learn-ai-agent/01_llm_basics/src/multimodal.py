"""
多模态输入 — content 是"块列表"（图片 + 文本）.

学习要点:
  1. 消息的 content 不只是字符串，而是类型化块（blocks/parts）列表
  2. OpenAI: {"type": "image_url"}，支持 http(s) URL 和 data: base64 URI
  3. Claude: {"type": "image", "source": {"type": "base64", ...}}
  4. 图片按尺寸折算 token —— 对比 usage 里的 input_tokens 直观可见
  5. 伏笔: Module 02 的 tool_use / tool_result 也是 content block，
     多模态和工具调用共享同一套分块协议

运行:
  uv run python 01_llm_basics/src/multimodal.py
"""

import anthropic
from openai import OpenAI

from shared.config import settings
from shared.llm_client import get_claude_client, get_openai_client
from shared.logger import console, print_error, print_response, print_separator

# 自包含测试图: 128x128 PNG（浅灰底 + 中央红色方块），无需外部图片/网络
IMG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAIAAABMXPacAAAA50lEQVR42u3RQQ0AMAgEQRz1"
    "j38NCKmCqiCEZjan4CauRgsXAAAgAAAEAIAAABAAAAIAQAAACAAAAQAgAAAEAIAAABAAAAIA"
    "QAAAaAFA5Vk9AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAA4AcAAQAgAAAEAIAAABAAAAIAQAAACAAAAAIAQAAACAAAAQAgAAAEAIAAAFB7D4fx"
    "GSXTesHHAAAAAElFTkSuQmCC"
)


def openai_vision(client: OpenAI) -> None:
    """OpenAI 图片输入 — content 是 parts 列表，图片用 image_url."""
    console.print("\n[bold blue]═══ OpenAI 图片输入 ═══[/bold blue]\n")

    response = client.chat.completions.create(
        model=settings.openai_model,
        max_completion_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "描述这张图片的内容，一句话。"},
                    {
                        "type": "image_url",
                        # 两种写法都支持:
                        #   1. 公网 URL: "https://example.com/a.png"（OpenAI 服务端去下载）
                        #   2. base64 data URI: 本地图片的常用方式（无需公网可访问）
                        "image_url": {"url": f"data:image/png;base64,{IMG_B64}"},
                    },
                ],
            }
        ],
    )
    print_response("OpenAI", response.choices[0].message.content or "")
    if response.usage:
        print(
            f"  [dim]输入 tokens: {response.usage.prompt_tokens}（纯文本问题大约只要 10 个）[/dim]"
        )


def claude_vision(client: anthropic.Anthropic) -> None:
    """Claude 图片输入 — content 是 blocks 列表，图片用独立的 source 结构."""
    console.print("\n[bold green]═══ Claude 图片输入 ═══[/bold green]\n")

    response = client.messages.create(
        model=settings.claude_model,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        # Claude 不支持 URL 直传，只收 base64（或 Files API 引用）
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": IMG_B64,
                        },
                    },
                    {"type": "text", "text": "描述这张图片的内容，一句话。"},
                ],
            }
        ],
    )
    text = next((b.text for b in response.content if b.type == "text"), "")
    print_response("Claude", text)
    print(f"  [dim]输入 tokens: {response.usage.input_tokens}[/dim]")


def print_summary() -> None:
    """多模态要点总结."""
    print_separator()
    console.print("[bold]多模态要点:[/bold]")
    lines = [
        "1. content 从字符串升级为类型化块列表 —— text / image / input_audio 平级共存",
        "2. 图片按尺寸折算 token（看上面两家 usage，图片远贵于文字）",
        "3. Claude 不收 URL 只收 base64；OpenAI 两种都收（URL 是服务端去下载）",
        "4. 音频: OpenAI 特定模型支持 input_audio；Claude 完全不支持",
        "5. 视频: 两家都不能直接输入（抽帧成图）；原生视频输入是 Gemini 的独门能力",
        "6. 🔗 伏笔: Module 02 的 tool_use / tool_result 也是 content block ——",
        "   多模态和工具调用共享同一套分块协议，这是 Anthropic 设计上很优雅的一点",
    ]
    for line in lines:
        console.print(f"  {line}")


def main() -> None:
    # 两个 demo 独立容错: 只配了其中一家 key 也能跑另一半
    try:
        openai_vision(get_openai_client())
    except Exception as e:  # noqa: BLE001
        print_error(f"OpenAI 图片输入失败: {str(e)[:200]}")

    try:
        claude_vision(get_claude_client())
    except Exception as e:  # noqa: BLE001
        print_error(f"Claude 图片输入失败: {str(e)[:200]}")

    print_summary()


if __name__ == "__main__":
    main()
