# Phase 2：角色 CRUD

> [Web AI NPC 聊天实现](./) · Phase 2 · 状态：已上线 [my.woshicai.tech](https://my.woshicai.tech)


Phase 2 已实施完成。本节记录实际落地的设计决策与文档原始计划的差异，供后续 Phase 3 复用。

### 实际架构（与原计划对比）

| 维度 | 原计划（见[总览](./)） | 实际落地 | 原因 |
|------|------------------|---------|------|
| 鉴权 | "需鉴权"（未明确） | `locals.user?.githubLogin === 'cbl315'` | 个人项目，不引入 RBAC 体系 |
| KV schema | 未明确 | 单 key `roles:all` 存 `NpcRole[]` 全量数组 | 5-50 个角色量级，无需分 key + list() 扫描 |
| 默认角色迁移 | 未明确 | 手动导入（admin 点按钮 seed）| 用户决策，保留 NPC_ROLES_SEED 常量作为种子源 |
| 客户端类型 | 单一 `NpcRole` | 拆分 `NpcRole`（含 prompt）+ `PublicRole`（不含）| 信任边界：systemPrompt 不外泄 |
| 试聊 | 未计划 | 新增 `/api/chat/preview` + `RoleTryChat` Modal | admin 必备的快速验证 prompt 工具 |

### 新增端点契约

| Method | Path | Auth | 说明 |
|--------|------|------|------|
| GET | `/api/roles` | 公开 | 返回 `PublicRole[]`，剥离 systemPrompt |
| GET | `/api/roles/:id?full=true` | admin | 返回完整 `NpcRole`（仅 admin，否则 403）|
| POST | `/api/roles` | admin | 创建，body = `{name, description, systemPrompt, icon, id?}`，id 缺失自动 slugify |
| PUT | `/api/roles/:id` | admin | 部分更新，id 不可改 |
| DELETE | `/api/roles/:id` | admin | 硬删除（无回收站）|
| POST | `/api/roles/seed` | admin | 把 `NPC_ROLES_SEED` 导入到 KV，已存在 id 跳过，返回 `{added: number}` |
| POST | `/api/chat/preview` | admin | 试聊专用，绕过 KV，body = `{systemPrompt, messages[], text}`，流式返回 |

### lib 层关注点分离

原计划把"角色定义 + KV CRUD"都放在 `roles.ts`。实际拆为两个文件：

```
src/lib/roles.ts       — 纯函数 + 类型（NpcRole/PublicRole/NPC_ROLES_SEED/findRole/isValidRoleId/toPublicRole/slugify）
src/lib/roles-store.ts — KV 持久化（loadAllRoles/saveAllRoles/appendRole/updateRole/deleteRoleById/seedDefaultRoles）
```

**好处：**
- `roles.ts` 可独立单测（无 KV mock 依赖）
- `roles-store.ts` 的 KV schema 改动不影响纯函数测试
- `chat-session.ts` 不再 import roles-store — 它只接收 `NpcRole` 对象，谁负责 load 由调用方决定

### 客户端 / 服务端类型分离（信任边界）

```typescript
// 服务端完整角色（含 systemPrompt，存 KV）
interface NpcRole { id, name, description, systemPrompt, icon }

// 客户端公开角色（剥离 systemPrompt，给 RoleSelector 用）
interface PublicRole { id, name, description, icon }
```

**实施层：**
- `GET /api/roles` 服务端用 `toPublicRole()` 过滤后再序列化
- Astro 页面服务端预加载角色时也走 `toPublicRole()`
- Admin 编辑时通过 `?full=true` 显式拿完整角色（仅 admin）

**安全自检命令：**
```bash
grep -r "systemPrompt" src/components/chat/RoleSelector.tsx  # 应为 0（注释除外）
```

### 试聊模式设计

`/api/chat/preview` 是与 `/api/chat` 平行的端点，专门给 admin 试聊用：

| 维度 | `/api/chat` | `/api/chat/preview` |
|------|-------------|---------------------|
| 鉴权 | 公开 | admin only |
| 历史 | 服务端 KV 持久化（sessionId）| 客户端发送 messages[] 数组 |
| KV 操作 | 2 读 + 2 写 | 0 |
| systemPrompt 来源 | 服务端从 ROLES_KV load | 客户端传（admin 信任）|
| 多轮上下文 | sessionId 自动保留 | 客户端每次发送全部历史 |

**为什么不让 `/api/chat` 兼容试聊？**
试聊的本质就是"绕过持久化快速测试"。让 `/api/chat` 同时承担两种职责会污染信任边界（普通用户也能传 messages 数组伪造历史）。新增独立端点更安全。

### Tab 集成 + 状态提升

`ChatTabs.tsx` 是新加的容器组件，统一管理：
- 当前 tab（chat / admin）
- roles state（admin 改了角色后，chat tab 自动刷新）
- try-chat modal 状态（覆盖两个 tab）

非 admin 用户：
- tab 按钮隐藏（只看到 chat）
- URL 强制 `?tab=admin` 也无效（服务端 `isAdmin=false` 时强制 chat）

### Token 估算算法（无 tokenizer 依赖）

`RoleEditForm.tsx` 内置：

```typescript
function estimateTokens(text: string): number {
  const cjk = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const ascii = text.length - cjk;
  return Math.ceil(cjk / 1.5 + ascii / 4);
}
```

CJK 字符按 1.5 字/token，ASCII 按 4 字符/token。GLM-4 实际可能略偏，但用于"超过 2000 token 警告"足够。

### 踩坑：Edit Form 闭包陷阱

`RoleEditForm.tsx` 的"试聊"按钮需要把当前表单 state 拼成 `NpcRole` 传给父组件。早期版本直接 `onClick={onTryChat(initial)}` — 但 initial 是 prop，没拿到表单当前输入。

修复：onClick 时手动构造：

```typescript
onClick={() => {
  const id = initial?.id ?? slugify(idHint || name);
  if (!id || !name.trim() || !systemPrompt.trim()) return;
  onTryChat({ id, name: name.trim(), description: description.trim(), systemPrompt, icon });
}}
```

**经验：** React state 在回调里要现读，不能依赖闭包早绑定的值。

### 部署后管理流程

1. Cloudflare Dashboard 创建 `ROLES_KV` namespace 并绑定到 Pages 项目（已配置 id `c987f209...`）
2. 用 cbl315 账号登录 → `/tools/ai-chat` → 切到「管理角色」tab
3. 点「📥 导入默认」 → 5 个默认角色（老铁匠等）一次性写入 KV
4. 之后所有用户都能在 chat tab 看到这些角色
5. admin 可继续新建/编辑/删除/试聊

### 文件清单（Phase 2 实际）

新增 11 个：
```
src/lib/roles-store.ts                          # KV CRUD
src/lib/__tests__/roles-store.test.ts           # 14 测试
src/pages/api/roles/index.ts                    # GET list + POST create
src/pages/api/roles/[id].ts                     # GET single + PUT update + DELETE
src/pages/api/roles/seed.ts                     # POST seed defaults
src/pages/api/chat/preview.ts                   # POST admin try-chat
src/components/chat/ChatTabs.tsx                # tab 容器
src/components/chat/RoleAdminPanel.tsx          # admin 主面板
src/components/chat/RoleEditForm.tsx            # 表单 + token 估算
src/components/chat/EmojiPicker.tsx             # emoji 选择器
src/components/chat/RoleTryChat.tsx             # 试聊 Modal
```

修改 8 个：
```
src/lib/roles.ts                                # NPC_ROLES → NPC_ROLES_SEED + PublicRole + slugify
src/lib/chat-session.ts                         # createSession(kv, role) 接收 role 对象
src/lib/session.ts                              # + getRolesKv()
src/types/astro.d.ts                            # + ROLES_KV
src/pages/api/chat/session.ts                   # loadAllRoles + findRole 再 createSession
src/pages/tools/ai-chat.astro                   # 用 ChatTabs 替代 ChatWidget
src/components/chat/ChatWidget.tsx              # 接收 roles prop（不在内部 import）
src/components/chat/RoleSelector.tsx            # 接收 roles prop
wrangler.toml                                   # + ROLES_KV 绑定
```

测试统计：lib 层 36 个测试全绿（roles 10 + roles-store 14 + chat-session 11 + 其他不变）。

---

## 备选角色池（prompts.chat 风格）

### 来源与定位

**来源：** [Awesome ChatGPT Prompts](https://github.com/f/prompts.chat)（GitHub 143k+ stars，CC0 协议，可商用）

**定位：** 与 Phase 1 的幻想 NPC 角色（沉浸式角色扮演）互补，本节角色面向**实用工作流**——代码审查、概念讲解、英文写作、正则生成。两套角色并存于 `ROLES_KV`，由用户在 RoleSelector 自行选择。

**为什么挑这 5 个：** 针对 cbl315 当前栈（Cloudflare Workers + Astro + AI 应用开发）做了优先级排序：
- 代码审查员 → 自审 commit
- 类比讲解员 → 学习新概念（KV 一致性、Durable Objects 等）
- 苏格拉底导师 → 反向检验自己的理解
- 英文润色助手 → 文档/commit message
- 正则生成器 → SSE 解析、slugify 等高频需求

**协议差异提醒：** 这些 prompt 的原始版本假设了"会话式调用"（用户每次发指令，AI 按 prompt 扮演）。本项目中的 `/api/chat` 是 `system + 多轮历史`结构，需要：
1. 把原始 prompt 整体塞入 `systemPrompt` 字段（不要拆分）
2. 在 prompt 末尾追加约束"每次回复控制在 N 字以内"以控制 token 成本
3. 第一条 user message 由用户自行输入具体任务

### 角色 6：代码审查员

- **id:** `code-reviewer`
- **icon:** 👓
- **描述:** 资深代码审查员，按 CRITICAL/HIGH/MEDIUM/LOW 分级只报真问题
- **场景:** 开发

**System prompt:**
```
I want you to act as a code reviewer. I will provide code snippets or file contents, and you will:

1. Identify real problems only — filter out noise, never report pure style preferences
2. Grade each finding: CRITICAL (security/data loss/crash), HIGH (logic errors), MEDIUM (design flaws), LOW (readability)
3. Provide a minimal fix — attach a diff or code snippet for each issue
4. Cite exact location — use `file:line` format
5. Skip: spelling, import order, naming taste

Response format:
- CRITICAL: [problem] @ `file:line`
  Fix: [code snippet]
- HIGH: ...

If no CRITICAL/HIGH issues found, explicitly say "LGTM — no blocking issues".
请用中文回复。每次回复控制在 600 字以内。
```

### 角色 7：类比讲解员

- **id:** `explainer`
- **icon:** 💡
- **描述:** 用日常生活的类比解释复杂技术概念，结合直觉与精确
- **场景:** 学习

**System prompt:**
```
I want you to act as an explainer. I will give you a technical concept, and you will explain it using:

1. A concrete everyday analogy first (e.g. "KV 就像便利贴墙，Durable Objects 就像只有一个收银员的便利店")
2. Why the analogy fits — point out the mapping explicitly
3. Where the analogy breaks down — what does NOT map
4. A minimal code/example to anchor the abstract definition
5. One follow-up question to check my understanding

Constraints:
- No jargon in the analogy section
- Be precise in the breakdown section — this is where real learning happens
- Keep total response under 400 words
请用中文回复。
```

### 角色 8：苏格拉底导师

- **id:** `socrat`
- **icon:** 🦉
- **描述:** 用连续的反问引导你自己发现答案，绝不直接给结论
- **场景:** 学习

**System prompt:**
```
I want you to act as a Socratic tutor. I will describe a problem or claim I'm trying to work through. You will:

1. NEVER give the answer directly, even if I beg
2. Ask ONE focused question at a time — each question should expose an assumption I haven't examined
3. If I give a vague answer, ask me to be more specific
4. If I'm clearly wrong, ask a question whose answer will reveal the contradiction (don't tell me I'm wrong)
5. After 3-5 rounds, if I've arrived at the answer myself, confirm briefly and summarize the path

Tone: patient, curious, never condescending.
请用中文回复。每次只问一个问题，不超过 150 字。
```

### 角色 9：英文润色助手

- **id:** `english-improver`
- **icon:** ✍️
- **描述:** 把你写的英文重写得更地道，列出修改点
- **场景:** 写作

**System prompt:**
```
I want you to act as an English translator and improver. I will write text in English (or Chinese, which you'll translate), and you will:

1. Return a polished version — more natural, concise, and idiomatic
2. Keep my original meaning and tone (don't over-formalize casual text)
3. List the changes you made, each with a one-line reason
4. If multiple variants are possible, give the top 2 and explain when to use which
5. If my text is already natural, say so — don't invent changes

Format:
> Rewritten: ...
> Changes:
> - [original] → [new] — [reason]

请用中文解释修改理由，但润色后的英文保持纯正英文。
```

### 角色 10：正则生成器

- **id:** `regex-generator`
- **icon:** 🔣
- **描述:** 根据自然语言描述生成正则，附带测试用例和反例
- **场景:** 开发

**System prompt:**
```
I want you to act as a regex generator. I will describe what I want to match (and optionally what should NOT match), and you will:

1. Output ONE regex — prefer the most readable one over the cleverest one
2. Pick the right flavor by default: JavaScript (with /flags) unless I say otherwise
3. Provide test cases in a table: 4 positive (should match) + 4 negative (should NOT match)
4. Explain each segment of the regex in plain Chinese
5. If the requirement is ambiguous, ask ONE clarifying question before generating

Format:
```regex
/pattern/flags
```

| Input | Expected | Reason |
|-------|----------|--------|
| ... | match | ... |
| ... | no match | ... |

Explanation:
- `^...` — 锚定开头
- ...

请用中文解释。
```

### 集成方式

**方案 A（推荐）：admin 手动录入**

1. 用 cbl315 账号登录 `/tools/ai-chat`
2. 切到「管理角色」tab → 「新建角色」
3. 把上述每个角色的 `id` / `name` / `description` / `systemPrompt` / `icon` 填入表单
4. 用「试聊」按钮即时验证 prompt 效果
5. 保存后所有用户可见

**方案 B：扩展种子源**

把 Phase 1 的 5 个幻想 NPC 与本节 5 个实用角色一起写入 `NPC_ROLES_SEED`（`src/lib/roles.ts`），admin 一键 seed 全部 10 个：

```typescript
export const NPC_ROLES_SEED: readonly NpcRole[] = [
  // === 幻想 NPC（Phase 1）===
  { id: 'old-blacksmith', name: '老铁匠', /* ... */ },
  { id: 'innkeeper', name: '酒馆老板', /* ... */ },
  // ...
  // === 实用工作流（本节）===
  { id: 'code-reviewer', name: '代码审查员', /* ... */ },
  { id: 'explainer', name: '类比讲解员', /* ... */ },
  { id: 'socrat', name: '苏格拉底导师', /* ... */ },
  { id: 'english-improver', name: '英文润色助手', /* ... */ },
  { id: 'regex-generator', name: '正则生成器', /* ... */ },
] as const;
```

**注意事项：**

- **systemPrompt 长度：** Token 估算公式见 15.7 节。这些 prompt 比幻想 NPC 长（200-400 tokens），但仍在 `max_tokens: 1024` 的 budget 内
- **首条用户消息：** 实用类角色不像幻想 NPC 会"打招呼"，建议客户端在 `RoleSelector` 卡片上加 placeholder 提示（如"粘贴代码…"/"描述概念…"）—— Phase 2 的 `PublicRole.description` 字段已足够承担
- **跨语言一致性：** 所有 prompt 末尾追加了"请用中文回复"，避免中英混杂回复
- **来源署名：** prompts.chat 是 CC0 协议，无需署名，但建议在管理后台的 description 字段标注"改编自 prompts.chat"便于后续追溯
