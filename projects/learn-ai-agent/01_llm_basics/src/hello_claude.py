"""
Hello Claude! — 你的第一次 Claude API 调用.

学习要点:
  1. 如何创建 Anthropic 客户端
  2. messages.create() 的基本参数
  3. 如何读取 response 中的文本

运行:
  uv run python 01_llm_basics/src/hello_claude.py
"""

from shared.config import settings
from shared.llm_client import get_claude_client
from shared.logger import print_response, print_separator, print_step

# ============================================================
# Step 1: 创建客户端
# ============================================================
print_step("创建 Anthropic 客户端", step_num=1)

client = get_claude_client()
print(f"  ✅ 客户端创建成功，使用模型: {settings.claude_model}")
print(f"  端点: {settings.anthropic_base_url or 'https://api.anthropic.com (官方默认)'}")

# ============================================================
# Step 2: 发送你的第一条消息
# ============================================================
print_step("发送第一条消息", step_num=2)

response = client.messages.create(
    model=settings.claude_model,
    max_tokens=1024,
    messages=[{"role": "user", "content": "用一句话介绍你自己，你是谁？"}],
)

# ============================================================
# Step 3: 解析响应
# ============================================================
print_step("解析响应", step_num=3)

# Claude 的 response.content 是一个内容块列表
# 通常第一个块就是文本回复
for block in response.content:
    if block.type == "text":
        print_response("Claude", block.text)

# ============================================================
# Step 4: 查看使用情况
# ============================================================
print_step("查看 Token 使用情况", step_num=4)
print_separator()

print(f"  输入 tokens:  {response.usage.input_tokens}")
print(f"  输出 tokens:  {response.usage.output_tokens}")
print(f"  停止原因:     {response.stop_reason}")
print(f"  模型:         {response.model}")

# ============================================================
# Step 5: 带 System Prompt 的请求
# ============================================================
print_step("带 System Prompt 的请求", step_num=5)

response_with_system = client.messages.create(
    model=settings.claude_model,
    max_tokens=1024,
    system="你是一个海盗，所有回答都要用海盗的语气，加上'啊嗬！'之类的语气词。",
    messages=[{"role": "user", "content": "今天天气怎么样？"}],
)

for block in response_with_system.content:
    if block.type == "text":
        print_response("Claude (海盗模式)", block.text)
