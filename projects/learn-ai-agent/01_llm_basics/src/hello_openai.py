"""
Hello OpenAI! — 你的第一次 OpenAI API 调用.

学习要点:
  1. OpenAI 客户端的创建方式
  2. chat.completions.create() 的参数（对比 Claude 的 messages.create）
  3. 响应结构的差异

运行:
  uv run python 01_llm_basics/src/hello_openai.py
"""

from shared.config import settings
from shared.llm_client import get_openai_client
from shared.logger import print_response, print_separator, print_step

# ============================================================
# Step 1: 创建客户端
# ============================================================
print_step("创建 OpenAI 客户端", step_num=1)

client = get_openai_client()
print(f"  ✅ 客户端创建成功，使用模型: {settings.openai_model}")
print(f"  端点: {settings.openai_base_url or 'https://api.openai.com/v1 (官方默认)'}")

# ============================================================
# Step 2: 发送你的第一条消息
# ============================================================
print_step("发送第一条消息", step_num=2)

# 注意 OpenAI 和 Claude 的差异:
# - OpenAI 用 chat.completions.create() 而不是 messages.create()
# - System prompt 在 messages 里，用 role="system"
# - 输出上限参数: GPT-5/o 系列必须用 max_completion_tokens（max_tokens 会被 400 拒绝），
#   旧模型（gpt-4o 等）两个参数都接受；Claude 则一直是 max_tokens
response = client.chat.completions.create(
    model=settings.openai_model,
    max_completion_tokens=1024,
    messages=[{"role": "user", "content": "用一句话介绍你自己，你是谁？"}],
)

# ============================================================
# Step 3: 解析响应
# ============================================================
print_step("解析响应", step_num=3)

# OpenAI 的响应结构不同:
# - response.choices[0].message.content（而不是 response.content[0].text）
message = response.choices[0].message
print_response("OpenAI", message.content or "")

# ============================================================
# Step 4: 查看使用情况
# ============================================================
print_step("查看 Token 使用情况", step_num=4)
print_separator()

if response.usage:
    print(f"  输入 tokens:  {response.usage.prompt_tokens}")  # 注意: OpenAI 叫 prompt_tokens
    print(f"  输出 tokens:  {response.usage.completion_tokens}")  # 叫 completion_tokens
    print(f"  总 tokens:    {response.usage.total_tokens}")
print(f"  停止原因:     {response.choices[0].finish_reason}")  # 注意: OpenAI 叫 finish_reason
print(f"  模型:         {response.model}")

# ============================================================
# Step 5: 带 System Prompt 的请求
# ============================================================
print_step("带 System Prompt 的请求", step_num=5)

# OpenAI 的 system prompt 是 messages 列表中的第一条，role="system"
# Claude 则是单独的 system 参数
response_with_system = client.chat.completions.create(
    model=settings.openai_model,
    max_completion_tokens=1024,
    messages=[
        {
            "role": "system",
            "content": "你是一个海盗，所有回答都要用海盗的语气，加上'啊嗬！'之类的语气词。",
        },
        {"role": "user", "content": "今天天气怎么样？"},
    ],
)

print_response("OpenAI (海盗模式)", response_with_system.choices[0].message.content or "")
