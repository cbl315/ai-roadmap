# Module 01 练习

## 完成状态（2026-10-17 收尾）

- 练习 4（Responses API 两种多轮姿势）— 通过 `src/responses_api.py` 验证：A 路线在本机中转上按预期暴露 `previous_response_not_found`（有状态链绑定基础设施），B 路线无状态重放完整跑通
- 练习 5（多模态）— 通过 `src/multimodal.py` 双 Provider 验证，含 GPT / Claude 视觉差异实测（同图 GPT 漏检红方块、Claude 识别正确，两次运行结论一致）
- 练习 1–3 未单独打卡，核心知识点已通过对应示例脚本覆盖

---

## 练习 1: 比较两个模型的回答

同一个问题分别问 Claude 和 OpenAI，比较他们的回答风格和内容差异。

**任务**: 问 "什么是微服务架构？它和单体架构有什么区别？"
- 分别用 Claude 和 OpenAI 调用
- 打印两者的回答
- 比较 token 使用量

## 练习 2: System Prompt 的影响

用不同的 system prompt 让模型产生不同风格的回答。

**任务**: 对同一个问题 "解释什么是 Docker"，使用以下三个不同的 system prompt：
1. "你是一个面向初学者的老师，用简单的比喻解释技术概念。"
2. "你是一个高级架构师，回答要专业、精确、引用技术规范。"
3. "你是一个段子手，用幽默的方式解释技术。"

## 练习 3: 实现一个简单的命令行聊天

使用流式输出，实现一个可以持续对话的命令行聊天工具。

**要求**:
- 支持多轮对话（维护消息历史）
- 使用流式输出（打字机效果）
- 输入 `quit` 退出
- 每轮显示 token 使用量

**提示**: 参考 `multi_turn.py` 的对话历史管理 + `streaming.py` 的流式输出

## 练习 4: Responses API 的两种多轮姿势

用 Responses API 实现"自我介绍 → 追问记忆"的两轮对话，分别用两种方式实现：

- **A. 有状态链**：第二轮只发新消息 + `previous_response_id`
- **B. 无状态重放**：第二轮把第一轮的 `output` items 和新问题一起放进 `input`

**观察**:
- 两种方式第二轮的 `input_tokens` 有什么规律？（提示：服务端拼历史，token 照样计费）
- 把 `store=False` 和 `previous_response_id` 一起用会发生什么？为什么？
- 如果想在第二轮之前删掉第一轮历史中的某一段，哪种方式做得到？

**思考**: 为什么 Agent 框架（需要截断 / 重试 / 分支历史）普遍选择无状态重放？

**提示**: 参考 `src/responses_api.py` 的 Demo 2 和 Demo 3

## 练习 5: 多模态 — 发一张自己的图片

把一张你自己的截图（或任意本地图片）读成 base64，分别发给 GPT 和 Claude 让它们描述。

**任务**:
- 用 `base64.b64encode(Path("你的图片").read_bytes())` 编码后按 `multimodal.py` 的格式发送
- 对比两家的描述风格和 `input_tokens`

**观察**:
- 图片比纯文本多消耗多少 token？
- 把图片缩放到一半尺寸再发（预览工具导出小图即可），token 怎么变？
- `image_url` 传公网 URL 和传 base64 data URI 的取舍：隐私、大小限制、谁负责下载？

**思考**: content 块列表里 `text` 和 `image` 是平级的 —— 猜一下 Module 02 里模型的工具调用请求、
你返回的工具执行结果，会以什么形式出现在消息里？

**提示**: 参考 `src/multimodal.py`
