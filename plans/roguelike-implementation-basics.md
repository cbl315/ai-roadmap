# 传统 Roguelike 实现基础：从机制到发布

> 目的：在结合 LLM 设计「AI Roguelike」之前，先建立对**纯肉鸽实现骨架**的完整认知。
> 本文只讲传统机制（无 LLM），下一轮 review 再讨论 LLM 该插在哪、不该插在哪。
>
> 配套文档：`ai-roguelike-market-research.md`（市场）、`phase2-web-chat.md`（已完成的 NPC 能力）

---

## 目录

1. [Roguelike 的核心特征（Berlin Interpretation）](#1-roguelike-的核心特征berlin-interpretation)
2. [技术架构总览](#2-技术架构总览)
3. [核心机制 1：回合制游戏循环](#3-核心机制-1回合制游戏循环)
4. [核心机制 2：程序生成（PCG）](#4-核心机制-2程序生成pcg)
5. [核心机制 3：实体与状态管理](#5-核心机制-3实体与状态管理)
6. [核心机制 4：战斗与检定系统](#6-核心机制-4战斗与检定系统)
7. [核心机制 5：元进度与解锁（Roguelite）](#7-核心机制-5元进度与解锁roguelite)
8. [从 0 到发布的内容清单](#8-从-0-到发布的内容清单)
9. [实现路径建议（最小可玩原型 → 完整游戏）](#9-实现路径建议最小可玩原型--完整游戏)
10. [下一步：LLM 接入点预判](#10-下一步llm-接入点预判)
11. [参考来源](#11-参考来源)

---

## 1. Roguelike 的核心特征（Berlin Interpretation）

2008 年的「柏林诠释」给 roguelike 划了 9 条特征，按重要性分高低两组。**理解这 9 条**，就理解了肉鸽的设计骨架：

### 高价值特征（必须有）

| 特征 | 含义 | 技术含义 |
|---|---|---|
| **程序生成** | 关卡/物品/怪物算法生成，非手工设计 | PCG 算法 + 随机种子 |
| **永久死亡** | 角色死亡=存档删除，不可读档 | 无持久存档（roguelite 例外，见 §7） |
| **回合制** | 玩家不动，世界不动；一步一结算 | 事件循环 + Action 队列 |
| **网格化** | 在二维网格上移动（上下左右+斜向） | tile 网格 + 寻路 |

### 低价值特征（最好有）

| 特征 | 含义 |
|---|---|
| 多模式（砍/喝/读卷轴等多种动作） |
| Hack 式物品鉴定（用前不知效果，需鉴定） |
| 资源管理（食物/照明有限，逼你推进） |
| 探索与战斗同样重要 |
| ASCII/极简视觉 |

### Roguelike vs Roguelite 的关键区别

这是新手最容易混淆的点：

| | Roguelike（如 Nethack） | Roguelite（如 Slay the Spire） |
|---|---|---|
| 永久死亡 | **硬**：死亡清零，啥都不剩 | **软**：死亡后保留部分进度 |
| 元进度 | 无 | **有**：解锁新卡/新角色/永久强化 |
| 留存设计 | 靠「下一把更好运」 | 靠「下一把能解锁 XX」 |
| 商业表现 | 小众硬核 | **主流爆款**（STS 1000 万+销量） |

> **对你的启示**：从市场调研看，你要做的是 **roguelite 而非 roguelike**——永久死亡太劝退，元进度解锁才是留存和付费的关键。

---

## 2. 技术架构总览

一个传统肉鸽的代码结构，核心就这几块：

```
┌─────────────────────────────────────────┐
│              游戏状态机                  │
│   (菜单 / 探索 / 战斗 / 物品 / 死亡)      │
├─────────────────────────────────────────┤
│  游戏循环（回合引擎）                     │
│  ├─ 输入处理 → 生成 Action               │
│  ├─ Action 队列（按速度/能量排序）        │
│  └─ 执行 Action → 更新世界               │
├──────────┬──────────┬───────────────────┤
│  PCG     │  实体     │   战斗/检定       │
│ 地图生成  │  系统    │   (HP/伤害/骰子)   │
│ 物品掉落  │ (ECS或    │                  │
│ 怪物配置  │  组件)    │                  │
├──────────┴──────────┴───────────────────┤
│           持久化层                       │
│   (种子存档 / 元进度存档)                │
└─────────────────────────────────────────┘
```

**实体组织方式**有两种主流选择：
- **ECS（Entity-Component-System）**：实体=ID，组件=数据，系统=逻辑。扩展性最强，大项目首选。详见 [Game Programming Patterns - Component](https://gameprogrammingpatterns.com/component.html)
- **OOP 继承**：`Entity → Actor → Player/Enemy`。简单，小项目够用。

文字游戏规模不大，**OOP 继承即可**，不必上 ECS（你的 NPC 聊天项目就是这种结构）。

---

## 3. 核心机制 1：回合制游戏循环

这是肉鸽的心脏。Bob Nystrom 的 [A Turn-Based Game Loop](https://journal.stuffwithstuff.com/2014/07/15/a-turn-based-game-loop/) 是公认最好的讲解。

### 3.1 基本循环（所有 actor 同速）

```text
while 游戏未结束:
    for 每个 actor（按顺序）:
        if actor == 玩家:
            action = 等待玩家输入      ← 阻塞，直到玩家按键
        else:
            action = AI 决策           ← 怪物自己算下一步
        执行 action                    ← 移动/攻击/使用物品
        渲染画面
```

**关键点**：玩家不操作时，世界是**静止**的。这是肉鸽和实时游戏的最大区别——你可以随时停下来思考。

### 3.2 Action 模式（推荐的现代写法）

不要让 actor 直接操作世界，而是**每个行为封装成一个 Action 对象**，丢进队列统一执行：

```python
class MoveAction(Action):
    def __init__(self, actor, dx, dy): ...
    def execute(self, game):
        目标格 = actor.pos + (dx, dy)
        if 可通行(目标格):
            actor.pos = 目标格
        elif 有敌人(目标格):
            生成 AttackAction(actor, 敌人).execute(game)

class AttackAction(Action):
    def __init__(self, attacker, target): ...
    def execute(self, game):
        damage = 检定伤害(attacker, target)
        target.hp -= damage

# 玩家按"右"，不直接移动，而是入队：
game.queue.append(MoveAction(player, +1, 0))
```

**为什么用 Action 模式**：
- 撤销/重播容易（存 action 列表而非世界状态）
- 网络同步容易（只传 action）
- **接入 LLM 天然友好**：LLM 输出「意图」，系统把意图转成 Action 对象（见 §10）

### 3.3 能量/速度系统（处理不同速 actor）

如果怪比玩家快，怎么办？肉鸽的标准解法是 **能量系统**：

```text
每回合：
    给所有 actor +能量（玩家 +100，怪按速度加，如哥布林 +120）
    while 某个 actor 能量 >= 100:
        该 actor 行动一次，扣 100 能量
```

这样高速怪一回合动两次，慢速怪隔回合动一次。参考 [GameDev StackExchange 讨论](https://gamedev.stackexchange.com/questions/29104/)。

---

## 4. 核心机制 2：程序生成（PCG）

PCG 让每局都不同。三大经典算法，按用途分：

### 4.1 地图生成

| 算法 | 适合场景 | 特点 |
|---|---|---|
| **BSP（二叉空间分割）** | 房间式地牢（标准肉鸽） | 递归切分空间成房间，走廊连接。最常用。 |
| **Cellular Automata（元胞自动机）** | 洞穴/有机地形 | 从随机噪声演化出自然形状，适合不规则地形 |
| **Tunneling（隧道法）** | 简单快速 | 随机挖房间和走廊，粗糙但够用 |
| **Grammar-based（语法）** | 有结构的关卡 | 用规则生成符合建筑逻辑的布局 |

Cogmind 开发者的 [Procedural Map Generation](https://www.gridsagegames.com/blog/2014/06/procedural-map-generation/) 是最权威的综述。

**Roguelite 的地图不一定要 grid**：Slay the Spire 用的是**节点地图**（branching path），本质是 PCG 在「图」上的应用，不是 tile grid。这对文字游戏更友好。

### 4.2 物品/怪物生成

- **战利品表 + 权重**：每个区域配一张掉落表，按权重随机。
- **词缀系统**（affix）：基础物品 × 随机词缀 = 变体（如「生锈的」+「剑」=「生锈的剑」）。这是重玩性的关键。
- **种子（seed）**：整局用同一个随机种子，保证「同种子同结果」，便于复现 bug。

---

## 5. 核心机制 3：实体与状态管理

### 5.1 一个 actor 的典型数据

```python
class Actor:
    pos: (x, y)              # 位置
    hp / max_hp              # 生命
    atk / def                # 攻防
    speed                    # 速度（影响回合顺序）
    faction                  # 阵营（敌/友/中立）
    ai: AIBehavior           # 怪物的 AI 策略
    inventory: List[Item]    # 背包
    status_effects: List     # 中毒/燃烧/加速等
```

### 5.2 FOV（视野）与战争迷雾

- **FOV**：玩家只能看到一定范围，用 shadowcasting 算法计算可见格子。
- **战争迷雾**：去过的格子记下地形，但不再显示怪物实时位置。
- 文字游戏里 FOV 可以简化（当前房间/相邻节点可见），不必照搬 grid 实现。

---

## 6. 核心机制 4：战斗与检定系统

### 6.1 两种主流战斗模型

| 模型 | 代表 | 特点 | 适合文字游戏？ |
|---|---|---|---|
| **确定性战斗** | Slay the Spire（卡牌） | 伤害固定，靠策略 | ✅ 简单可预测 |
| **骰子检定** | D&D 系（含 Questsmith） | 投骰子 + 修正值 | ✅ 有随机张力 |

**骰子检定（D20）标准流程**（Questsmith 用的就是这个）：
```
1d20（投20面骰） + 攻击修正 vs 目标防御值（AC/难度）
  命中 → 投伤害骰（如 1d8+力量修正）
  未命中 → 无伤害
```

### 6.2 状态效果

中毒（每回合掉血）、燃烧、加速、缴械……每个是挂载在 actor 上的 effect 对象，每回合 tick 一次。文字游戏建议精简到 3-5 种。

---

## 7. 核心机制 5：元进度与解锁（Roguelite）

**这是 roguelike 和 roguelite 的分水岭，也是商业成败的关键。** 参考 [r/roguelites 讨论](https://www.reddit.com/r/roguelites/comments/18dc2t4/)、[Entalto Studios 指南](https://entaltostudios.com/5-essential-tips-to-make-your-roguelite-game-work/)。

### 7.1 三种元进度模式

| 模式 | 机制 | 例子 | 风险 |
|---|---|---|---|
| **解锁型**（推荐） | 死亡后解锁新内容（卡/角色/词条），不强化数值 | Slay the Spire | 安全，最被认可 |
| **永久强化型** | 死亡后获得永久属性加成 | 很多手游肉鸽 | ⚠️ 易被骂「不刷打不过」 |
| **货币兑换型** | 局间赚货币，局外购买强化 | Hades（暗影盾） | 需精心平衡 |

### 7.2 Slay the Spire 的设计（教科书级）

- **解锁即教学**：前几局解锁的卡/遗物恰好引入新机制，把教程融进解锁链。
- **量控制得刚好**：约 12 局/角色解锁全部，**比掌握角色所需局数少**——解锁不会比学习慢，避免拖沓。
- **STS2 改动**：从「每角色独立解锁轨」改为「统一进度」，说明角色多了之后分轨解锁太碎。

### 7.3 元进度的设计红线

- ❌ **不要做「残缺基础版」**：故意把首日体验削弱，逼玩家靠解锁补全——必被差评。
- ✅ **首日就要好玩**：解锁是调味料，不是主菜。基础循环未完成前别碰元进度。
- ✅ **解锁教机制**：让解锁链成为难度/复杂度的阶梯。

---

## 8. 从 0 到发布的内容清单

这是回答你「需要准备哪些内容」的核心。分三块：**代码系统、游戏内容、发布物料**。

### 8.1 代码系统（必须实现）

| 系统 | 说明 | 参考章节 |
|---|---|---|
| 游戏循环 | 回合引擎 + Action 队列 | §3 |
| PCG | 地图/事件/战利品生成 | §4 |
| 实体系统 | 玩家/敌人/物品的数据与行为 | §5 |
| 战斗系统 | 检定/伤害/状态效果 | §6 |
| 存档 | 种子存档（防作弊）+ 元进度存档 | §7 |
| UI | 菜单/背包/战斗/HUD/死亡结算 | — |

### 8.2 游戏内容（决定重玩性，这量最大）

这是肉鸽最吃工量的部分。参考 STS2 EA 标准（[Mega Crit](https://www.megacrit.com/news/2026-03-05-early-access-launch/)）：**5 角色、575+ 卡、278+ 遗物、3 幕**。

针对你的 **AI 文字肉鸽 MVP**（非卡牌制），合理起点：

| 内容类型 | MVP 起步量 | 说明 |
|---|---|---|
| 楼层/幕 | 3 幕，每幕 ~8 节点 | 节点地图，不是 grid |
| 节点类型 | 5 种：战斗/事件/商店/休息/精英/Boss | 够覆盖循环 |
| 事件库 | 20-30 个文字事件模板 | 每个有 2-4 分支 |
| 怪物 | 8-12 种（含 3 Boss） | 每幕 3-4 种 |
| 物品 | 15-20 种 + 词缀系统 | 词缀带来组合爆炸 |
| 职业角色 | 2-3 个 | 区分玩法风格 |
| 元进度解锁 | 10-15 项 | 解锁新事件/NPC/词条池 |

> **注意**：这是「能玩且有重玩性」的下限，不是 EA 发布标准。EA 约需 2-3 倍内容量 + 数值平衡调优 1-2 个月。

### 8.3 发布物料（非游戏内）

- **美术**：UI 图标、关键场景插图（AI 文字游戏可极简，甚至纯文字）
- **音效/音乐**：可选，文字游戏非必需
- **商店页**：Steam/itch.io 页面、截图、GIF、描述文案
- **平衡文档**：数值表（HP/伤害/掉率）的电子表格
- **测试计划**：找 5-10 个种子玩家测留存与难度曲线

---

## 9. 实现路径建议（最小可玩原型 → 完整游戏）

建议分 4 个里程碑，每步都可玩、可验证：

### M1 — 走得动（1 周）
- grid 或节点地图，玩家能移动
- 一只怪，能撞上去
- 回合循环跑通

### M2 — 打得死（1-2 周）
- 战斗系统（最简检定）
- HP/伤害/死亡
- 死亡结算屏

### M3 — 玩得久（2-3 周）
- PCG 地图（每局不同）
- 事件库（5-10 个起步）
- 商店/物品/简单词缀
- **此时已是一个可玩 roguelike 原型**

### M4 — 留得住（2-4 周）
- 元进度解锁系统
- 角色职业区分
- 数值平衡
- **此时是 EA 候选**

> **关键建议**：M3 完成前不要碰元进度（§7.3 红线）。先证明核心循环好玩，再做留存。

---

## 10. 下一步：LLM 接入点预判

这是为下一轮 review 预留的。基于上面 9 节的传统机制，LLM 的**合法接入点**只有以下几处（对应 `ai-roguelike-market-research.md` §6.1 的 L2 决策层）：

| 传统机制 | 纯代码做法 | LLM 可介入点（L2） | 不可介入（L1 装饰） |
|---|---|---|---|
| 回合循环 | 玩家按键→Action | **解析玩家自由输入→生成 Action**（如「我想说服他」→对话 Action） | 把「造成 5 伤」改写成文字 |
| PCG 事件 | 从事件库随机抽 | **按当前状态生成定制化事件描述**（结果仍走规则） | 生成整个事件含结果 |
| 战斗检定 | 骰子+修正 | — | 战斗台词 |
| NPC 交互 | 菜单选项 | **自由对话→结果映射状态**（说服/威胁/套话） | NPC 即兴闲聊 |
| 物品系统 | 词缀随机组合 | — | 物品描述润色 |

**一句话总结**：LLM 只能接在「输入解析」和「NPC 对话」两个口，且输出必须先转成 Action / 状态变更，再由规则系统执行——绝不让它直接修改世界状态或决定数值结果。

这条原则在下一轮结合 LLM 做 review 时会逐条验证。

---

## 11. 参考来源

### 综合教程（从 0 搭建）
- [Complete Roguelike Tutorial (Python+libtcod) — RogueBasin](https://www.roguebasin.com/index.php/Complete_Roguelike_Tutorial,_using_python3+libtcod)
- [Roguelike Tutorials (Rust) — Herbert Wolverson](https://rogueliketutorials.com/)
- [SelinaDev - Yet Another Roguelike Tutorial](https://selinadev.github.io/14-rogueliketutorial-10/)

### 游戏循环与回合制
- [A Turn-Based Game Loop — Bob Nystrom](https://journal.stuffwithstuff.com/2014/07/15/a-turn-based-game-loop/)
- [FAQ Friday #3: The Game Loop — r/roguelikedev](https://www.reddit.com/r/roguelikedev/comments/2uxv79/faq_friday_3_the_game_loop/)
- [How to manage different speeds in Roguelikes — GameDev SE](https://gamedev.stackexchange.com/questions/29104/)

### 程序生成
- [Procedural Map Generation — Cogmind / Grid Sage Games](https://www.gridsagegames.com/blog/2014/06/procedural-map-generation/)
- [Procedural Dungeon Generation with BSP (教程)](https://www.youtube.com/watch?v=Pj4owFPH1Hw)
- [Cellular Automata 地图生成 — jrheard](https://blog.jrheard.com/procedural-dungeon-generation-cellular-automata)

### 架构与 ECS
- [Component — Game Programming Patterns (Bob Nystrom)](https://gameprogrammingpatterns.com/component.html)
- [Entity Component System — RogueBasin](https://www.roguebasin.com/index.php/Entity_Component_System)

### 元进度与 Roguelite 设计
- [How to develop a good meta-progression — r/roguelites](https://www.reddit.com/r/roguelites/comments/18dc2t4/)
- [5 essential tips for roguelite — Entalto Studios](https://entaltostudios.com/5-essential-tips-to-make-your-roguelite-game-work/)
- [Slay the Spire design choices — r/slaythespire](https://www.reddit.com/r/slaythespire/comments/17rn2ie/)
- [Meta-progression with gradual tutorial — Hamatti](https://notes.hamatti.org/gaming/video-games/meta-progression-with-gradual-tutorial-in-roguelike-games)

### 内容量基准（EA 发布）
- [Slay the Spire 2 Early Access launch — Mega Crit](https://www.megacrit.com/news/2026-03-05-early-access-launch/)
- [EA content expectations — r/slaythespire](https://www.reddit.com/r/slaythespire/comments/1rh0i9w/)

### Roguelike 定义
- [Roguelike — Wikipedia (Berlin Interpretation)](https://en.wikipedia.org/wiki/Roguelike)
- [What is a Traditional Roguelike? — Cogmind](https://www.gridsagegames.com/blog/2020/02/traditional-roguelike/)
