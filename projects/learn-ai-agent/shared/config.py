"""
环境变量与配置管理.

使用 pydantic-settings 从 .env 文件加载配置，提供类型安全的配置访问。

用法:
    from shared.config import settings

    # 访问 API Key
    print(settings.anthropic_api_key)

    # 检查某个 provider 是否可用
    if settings.has_anthropic:
        ...
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# 项目根目录（learn-ai-agent/）
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """项目全局配置，从 .env 文件和环境变量加载."""

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",  # 忽略 .env 中未定义的变量
    )

    # --- API Keys ---
    anthropic_api_key: SecretStr = SecretStr("")
    openai_api_key: SecretStr = SecretStr("")

    # --- 自定义 API 端点（可选，用于代理 / 中转 / OpenAI 兼容服务）---
    anthropic_base_url: str | None = None
    openai_base_url: str | None = None

    # --- 模型配置 ---
    claude_model: str = "claude-sonnet-4-20250514"
    openai_model: str = "gpt-4o"
    openai_embedding_model: str = "text-embedding-3-small"

    # --- 默认 Provider ---
    default_provider: Literal["claude", "openai"] = "claude"

    # --- 日志 ---
    log_level: str = "INFO"

    @field_validator("anthropic_base_url", "openai_base_url", mode="before")
    @classmethod
    def _empty_base_url_to_none(cls, v: object) -> object:
        """空字符串视为未配置，避免把 base_url="" 传给 SDK."""
        return None if isinstance(v, str) and not v.strip() else v

    # --- 便捷属性 ---
    @property
    def has_anthropic(self) -> bool:
        """Anthropic API Key 是否已配置."""
        key = self.anthropic_api_key.get_secret_value()
        return bool(key) and key != "sk-ant-xxxxx"

    @property
    def has_openai(self) -> bool:
        """OpenAI API Key 是否已配置."""
        key = self.openai_api_key.get_secret_value()
        return bool(key) and key != "sk-xxxxx"

    def require_anthropic(self) -> str:
        """获取 Anthropic API Key，未配置时抛出清晰的错误信息."""
        if not self.has_anthropic:
            raise ValueError(
                "❌ ANTHROPIC_API_KEY 未配置！\n"
                "请执行以下步骤:\n"
                "  1. cp .env.example .env\n"
                "  2. 编辑 .env 填入你的 Anthropic API Key\n"
                "  获取地址: https://console.anthropic.com/settings/keys"
            )
        return self.anthropic_api_key.get_secret_value()

    def require_openai(self) -> str:
        """获取 OpenAI API Key，未配置时抛出清晰的错误信息."""
        if not self.has_openai:
            raise ValueError(
                "❌ OPENAI_API_KEY 未配置！\n"
                "请执行以下步骤:\n"
                "  1. cp .env.example .env\n"
                "  2. 编辑 .env 填入你的 OpenAI API Key\n"
                "  获取地址: https://platform.openai.com/api-keys"
            )
        return self.openai_api_key.get_secret_value()


@lru_cache
def get_settings() -> Settings:
    """获取全局配置单例（带缓存）."""
    return Settings()


# 便捷访问
settings = get_settings()
