"""
统一 LLM 客户端.

提供一个简单的工厂函数，根据 provider 返回对应的 SDK 客户端。
这不是一个抽象层 —— 你仍然直接使用 Anthropic/OpenAI 的原生 API。
它只是帮你处理 API Key 加载和客户端初始化。

用法:
    from shared.llm_client import get_claude_client, get_openai_client

    # 获取 Claude 客户端
    claude = get_claude_client()
    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello!"}],
    )

    # 获取 OpenAI 客户端
    openai_client = get_openai_client()
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello!"}],
    )

设计理念:
    我们故意不做统一接口抽象，因为学习的目的就是理解每个 Provider 的原生 API。
    Claude 和 OpenAI 的 API 设计有本质差异（比如 tool_use 的消息格式），
    隐藏这些差异会妨碍学习。

    两个 SDK 都支持通过 base_url 指向自定义端点（代理 / 中转 / OpenAI 兼容服务），
    在 .env 中配置 ANTHROPIC_BASE_URL / OPENAI_BASE_URL 即可，留空则用官方地址。
"""

from functools import lru_cache

import anthropic
import openai

from shared.config import settings


@lru_cache
def get_claude_client() -> anthropic.Anthropic:
    """获取 Anthropic (Claude) 客户端."""
    api_key = settings.require_anthropic()
    return anthropic.Anthropic(api_key=api_key, base_url=settings.anthropic_base_url)


@lru_cache
def get_async_claude_client() -> anthropic.AsyncAnthropic:
    """获取异步 Anthropic (Claude) 客户端."""
    api_key = settings.require_anthropic()
    return anthropic.AsyncAnthropic(api_key=api_key, base_url=settings.anthropic_base_url)


@lru_cache
def get_openai_client() -> openai.OpenAI:
    """获取 OpenAI 客户端."""
    api_key = settings.require_openai()
    return openai.OpenAI(api_key=api_key, base_url=settings.openai_base_url)


@lru_cache
def get_async_openai_client() -> openai.AsyncOpenAI:
    """获取异步 OpenAI 客户端."""
    api_key = settings.require_openai()
    return openai.AsyncOpenAI(api_key=api_key, base_url=settings.openai_base_url)
