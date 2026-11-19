"""测试 shared 模块的核心功能."""

import pytest

from shared.config import PROJECT_ROOT, Settings


def test_project_root_exists() -> None:
    """项目根目录应该存在."""
    assert PROJECT_ROOT.exists()
    assert (PROJECT_ROOT / "pyproject.toml").exists()


def _hermetic_settings(monkeypatch: pytest.MonkeyPatch) -> Settings:
    """构造不受本地 .env 和环境变量影响的 Settings（测试专用）."""
    for var in (
        "ANTHROPIC_API_KEY",
        "OPENAI_API_KEY",
        "ANTHROPIC_BASE_URL",
        "OPENAI_BASE_URL",
        "CLAUDE_MODEL",
        "OPENAI_MODEL",
        "DEFAULT_PROVIDER",
        "LOG_LEVEL",
    ):
        monkeypatch.delenv(var, raising=False)
    return Settings(_env_file=None)


def test_settings_default_values(monkeypatch: pytest.MonkeyPatch) -> None:
    """Settings 应该有合理的默认值（不受本地 .env 影响）."""
    s = _hermetic_settings(monkeypatch)
    assert s.claude_model == "claude-sonnet-4-20250514"
    assert s.openai_model == "gpt-4o"
    assert s.default_provider == "claude"
    assert s.log_level == "INFO"


def test_settings_api_key_detection(monkeypatch: pytest.MonkeyPatch) -> None:
    """未配置或占位符 API key 时，has_* 应该返回 False."""
    s = _hermetic_settings(monkeypatch)
    assert not s.has_anthropic
    assert not s.has_openai

    # .env.example 的占位符也算未配置
    monkeypatch.setenv("OPENAI_API_KEY", "sk-xxxxx")
    s2 = Settings(_env_file=None)
    assert not s2.has_openai


def test_settings_base_url_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """OPENAI_BASE_URL 环境变量应该被读取为自定义端点."""
    monkeypatch.setenv("OPENAI_BASE_URL", "https://relay.example.com/v1")
    monkeypatch.delenv("ANTHROPIC_BASE_URL", raising=False)
    s = Settings(_env_file=None)  # 忽略 .env 文件，只看环境变量
    assert s.openai_base_url == "https://relay.example.com/v1"
    assert s.anthropic_base_url is None


def test_settings_base_url_empty_is_none(monkeypatch: pytest.MonkeyPatch) -> None:
    """留空的 base_url 应该归一化为 None，而不是空字符串."""
    monkeypatch.setenv("OPENAI_BASE_URL", "   ")
    s = Settings(_env_file=None)
    assert s.openai_base_url is None
