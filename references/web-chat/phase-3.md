# Phase 3：会话持久化

> [Web AI NPC 聊天实现](./) · Phase 3 · 状态：已上线 [my.woshicai.tech](https://my.woshicai.tech)


Phase 3 已实施完成。本节记录实际落地的设计决策与文档原始计划的差异。

### 实际架构（与原计划对比）

| 维度 | 原计划（见[总览](./)） | 实际落地 |
|------|------------------|---------|
| 匿名用户 | "登录用户 7 天或永久，匿名用户保持 1 小时" | **必须登录才能用 chat**（用户决策，简化数据模型）|
| 数据模型 | "ChatSession 接口... 不需要结构性改动" | 加 `userId` + `title` 两个字段（不可避免）|
| 跨设备 | "可选升级到 Durable Objects" | KV 最终一致（~60s 延迟可接受）|
| TTL | "7 天或永久" | **30 天滑窗** + LRU 上限 50 条/用户 |
| 会话列表 | 未明确 | 单 key `chat:user:<userId>:sessions` 存 sessionId[] |

### KV Schema（最终）

```
CHAT_KV:
  chat:session:<id>               → ChatSession JSON
                                     expirationTtl: 30 天（登录用户滑窗）
                                     新增字段：userId, title
  chat:user:<userId>:sessions     → string[] (sessionId[]，按 updatedAt 倒序)
                                     不设 TTL（永久），list 时清理已过期项 + LRU 淘汰
```

**为什么单 key 存索引而不是 KV list() 扫描：**
- KV `list()` 有 1000 keys 上限，扫所有用户性能差
- 单 key 索引读写 O(1)，列表显示快
- 索引可能短暂与实际 session 不一致（最终一致），`listUserSessions` 时校验存在性兜底

### API 契约（最终）

| Method | Path | Auth | 说明 |
|--------|------|------|------|
| POST | `/api/chat/session` | **必须登录** | 创建会话，body `{roleId, title?}`，绑定 `locals.user.githubId` |
| POST | `/api/chat` | **必须登录** | 流式聊天，`appendMessage`/`appendReplyAndUsage` 都加 userId 校验 |
| GET | `/api/chat/sessions` | **必须登录** | 当前用户会话列表（`SessionSummary[]`，无 messages）|
| GET | `/api/chat/sessions/:id` | **必须登录** | 完整 messages（历史回放用），归属校验 |
| DELETE | `/api/chat/sessions/:id` | **必须登录** | 删除会话（归属校验）|
| PATCH | `/api/chat/sessions/:id` | **必须登录** | 改标题，body `{title}`（归属校验）|

**错误响应：**
- 401 `{error: '必须登录'}` — 未登录访问任意 chat 端点
- 404 `{error: '会话不存在或无权访问'}` — sessionId 不存在或归属不符（避免泄露存在性）
- SSE error 事件 `'会话已过期或无权访问'` — `/api/chat` 流式端点统一格式

### lib 层关注点分离（与 Phase 2 一致）

```
src/lib/chat-session.ts  — 单会话 KV CRUD（加 userId 校验、TTL 可配置）
src/lib/chat-user.ts     — 用户索引管理（list/create/delete/rename + LRU + 自动清理）
```

**关键函数签名变更：**

```typescript
// chat-session.ts (Phase 1 → Phase 3)
createSession(kv, role)                                     // Phase 1
createSession(kv, role, userId, title?)                     // Phase 3

getSession(kv, id)                                          // Phase 1
getSession(kv, id, expectedUserId?)                         // Phase 3（归属校验）

appendMessage(kv, id, msg)                                  // Phase 1
appendMessage(kv, id, msg, expectedUserId)                  // Phase 3

// 新增 chat-user.ts
createUserSession(kv, role, userId, title?)                 // 创建 + 加入索引
listUserSessions(kv, userId) → SessionSummary[]             // 含 LRU + 清理
deleteUserSession(kv, id, userId)                           // 校验 + 索引同步
renameUserSession(kv, id, title, userId)
```

### 信任边界演化

| Phase | 客户端能做什么 | 服务端防什么 |
|-------|--------------|------------|
| 1 | 发 `{sessionId, text}` | 客户端不能伪造 messages 历史 |
| 2 | 发 `{roleId}` 创建会话 | 客户端不能注入 systemPrompt（角色从 ROLES_KV 读）|
| **3** | 同 Phase 1/2 | **+ 跨用户访问拒绝**（session.userId !== locals.user.githubId → null）|

跨用户访问在两个层面防护：
1. **lib 层**：`getSession/appendMessage/...` 接收 `expectedUserId`，不匹配返回 null
2. **API 层**：每个端点先 401 检查登录，再传 `locals.user.githubId` 给 lib 函数

### Title 自动生成

首条 user message 进入 `appendMessage` 时触发：

```typescript
if (msg.role === 'user' && session.messages.length === 1 && isDefaultTitle) {
  session.title = msg.content.slice(0, 30).trim() || DEFAULT_TITLE;
}
```

第二条 user message 不覆盖（用户已投入话题，保留首条作为列表标题）。
用户可通过抽屉的 ✏️ 按钮手动改名（PATCH 端点）。

### LRU 淘汰与索引清理

`listUserSessions` 是触发清理的统一入口：

```typescript
// 1. 并发拉取所有 sessionId
const sessions = await Promise.all(ids.map(id => getSession(kv, id, userId)));
// 2. 过滤已 TTL 过期的（最终一致性兜底）
const valid = sessions.filter(Boolean);
// 3. 索引有失效项时写回（异步，不阻塞响应）
if (valid.length !== ids.length) {
  void _writeIndex(kv, userId, valid.map(s => s.id));
}
// 4. 按 updatedAt 倒序
valid.sort((a, b) => b.updatedAt - a.updatedAt);
// 5. LRU：超过 50 条删最旧
if (valid.length > 50) {
  await Promise.all(valid.slice(50).map(s => deleteSession(kv, s.id)));
}
```

**为什么用 list 触发清理而不是后台 cron？**
Cloudflare Workers 没有内置 cron（Pages 项目），用读路径触发是最实用的"机会性清理"。

### UI 架构（ChatWidget 拆分）

```
ChatWidget (路由)
├── LoginCard              未登录视图（GitHub OAuth 入口）
└── ChatArea (已登录)
    ├── SessionsDrawer     左侧抽屉
    │   ├── "+ 新对话" 按钮
    │   ├── SessionItem × N（单击切换、✏️ 重命名、🗑️ 删除）
    │   └── 底部用户信息 + 退出
    ├── 主区
    │   ├── 移动端顶栏（☰ 汉堡 + 当前角色）
    │   ├── MessageList（消息列表 + 流式打字机）
    │   ├── ChatInput（输入框）
    │   └── EmptyState（无激活会话时的引导）
    └── RolePickerModal    新建会话弹窗（包 RoleSelector）
```

### 响应式策略

| 断点 | 抽屉行为 |
|------|---------|
| 桌面 (md+) | 常驻侧边栏 `w-64`，主区 flex-1 |
| 移动端 (<md) | 隐藏；点 ☰ 滑入覆盖 80% 宽度，背景遮罩点击关闭 |

用 Tailwind 的 `md:` 前缀实现，无 JS 媒体查询。

### 文件清单（Phase 3 实际）

**新增 5 个：**
```
src/lib/chat-user.ts                              # 用户会话索引 + LRU
src/lib/__tests__/chat-user.test.ts               # 11 测试
src/pages/api/chat/sessions/index.ts              # GET list
src/pages/api/chat/sessions/[id].ts               # GET / DELETE / PATCH
src/components/chat/SessionsDrawer.tsx            # 抽屉（桌面侧栏 + 移动端抽屉）
src/components/chat/RolePickerModal.tsx           # 新建会话弹窗
```

**修改 5 个：**
```
src/lib/chat-session.ts                           # 加 userId/title，TTL 1h→30d，归属校验
src/lib/__tests__/chat-session.test.ts            # 适配新签名 + 跨用户测试
src/pages/api/chat/session.ts                     # 必须登录 + 绑定 userId
src/pages/api/chat/index.ts                       # 必须登录 + appendMessage/appendReplyAndUsage 加 userId
src/components/chat/ChatWidget.tsx                # 接收 currentUser，拆 ChatArea
src/components/chat/ChatTabs.tsx                  # 传 currentUser；非登录隐藏 admin tab
src/pages/tools/ai-chat.astro                     # 服务端读 locals.user 传 currentUser；?session= 深链
```

**测试统计：** lib 层 149/150 通过（1 个预存 jwt 失败与本 phase 无关）。

### 踩坑：Phase 1 旧 session 的兼容性

Phase 1 创建的旧 session 没有 `userId` 字段。Phase 3 上线后：
- 客户端拿到的旧 sessionId 调 `/api/chat` → `appendMessage` 校验 `session.userId !== expectedUserId` → 返回 null → SSE error
- 用户看到"会话已过期"提示，自然重新新建
- 旧 session 1h TTL 后从 KV 消失

**没有写迁移脚本** — 数据量小（开发期），自然过期成本最低。

### 部署后管理流程

1. 部署完成（无新 KV namespace，复用 CHAT_KV）
2. 访问 `/tools/ai-chat` → 未登录看到登录卡片
3. 点 GitHub OAuth 登录 → 抽屉空状态 + "+ 新对话" 按钮
4. 新建会话 → 选角色 → 聊 → 关浏览器 → 重开仍在
5. 切换设备登录 → 看到同一份会话列表（最多等 60s KV 一致性）
