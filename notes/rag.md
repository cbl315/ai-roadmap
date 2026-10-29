# RAG（检索增强生成）学习指南

> 本文档整理 RAG 的核心原理、进阶技术、主流实现方案对比与选型建议，以及系统化学习资料。
> 本 repo 只整理**学习路线与资料**，具体的代码实现会在独立 repo 中进行。

---

## 一、RAG 是什么：建立直觉

**RAG = Retrieval-Augmented Generation（检索增强生成）**

核心思想一句话：**LLM 自己不背书，先去你的知识库里查资料，再带着查到的资料回答问题。**

```
用户提问
   ↓
[① 检索 Retrieval] ──→ 在向量数据库里找出最相关的文档片段（chunk）
   ↓
[② 增强 Augmentation] ─ 把检索到的片段 + 用户问题 拼成 prompt
   ↓
[③ 生成 Generation] ──→ LLM 基于拼好的 prompt 生成答案
```

### 为什么需要 RAG？

解决 LLM 三个痛点：
1. **知识过时** — 训练数据有截止日期，RAG 可随时更新知识库
2. **会幻觉** — 让模型基于检索到的真实资料回答，而非自由编造
3. **不懂私有数据** — 接入企业/个人知识库，无需微调

比微调便宜得多，且知识可随时更新。

> 💡 **2026 补充：长上下文没有杀死 RAG。** 如今上下文窗口已达百万级 token，但决策因素从"能不能塞进窗口"变成了**成本、延迟、新鲜度、权限管控** — 大规模语料下 RAG 的成本优势依然碾压；且实测上下文越长性能反而退化（lost in the middle）。最佳实践是两者结合：RAG 管高频常规查询，长上下文管小数据量的复杂跨文档推理。

> ⚠️ 2026 年的共识：**"把 PDF 塞进向量库就完事"的朴素 RAG 已经不够用了**。生产级系统都在用进阶技术（见第三节，含 2026-10 五条路线对比）。

### RAG 与规则 / Memory / 工具检索的区别（上下文工程视角）

这四者做的是同一件事：**往有限的上下文窗口里塞"此刻最该知道的信息"** —— 都是上下文工程（context engineering）的策略，区别在于**装什么、谁来决定装什么、什么时候装**。

| 维度 | Context Prompt / 规则文件 | Harness Memory / 摘要 | RAG | Agent 工具检索 |
|------|--------------------------|----------------------|-----|---------------|
| 内容性质 | 行为指令（"怎么做事"） | 对话的压缩记忆（"刚才发生了什么"） | 外部知识（"世界/领域资料"） | 精确查询（grep / DB / API） |
| 注入时机 | 每轮全量注入 | 自动 / 按需 | 按问题语义检索 | 模型主动调用 |
| 谁决定内容 | 人（手工维护） | 模型（自动提炼） | 相似度算法 | 模型（agentic 循环） |
| 规模 | KB | KB | GB+ | 取决于数据源 |
| 确定性 | 完全确定 | 模糊、会漂移 | 可测量可调优 | 可复现 |
| 基础设施 | 无 | 无 | 向量库 + 索引管线 | 工具接口 |
| 典型失效 | 内容太多稀释注意力 | 记错 / 遗忘细节 | 检索不到 / 检索错 | 查错关键词 |

**要点展开：**

- **规则文件（AGENTS.md / system prompt）** — 确定性注入，无论相不相关每轮都占 token，只适合小体量、高价值、永远适用的内容
- **Memory / 摘要** — 解决"对话太长塞不下"，靠压缩换空间、细节有损；它是情景记忆，不是外部知识
- **RAG** — 与当前问题无关的内容一个 token 不占，规模上限 GB+，可引用溯源
- **Agent 工具检索** — coding agent（Claude Code 等）处理代码库时默认既不用 memory 也不用 RAG，而是 grep / 读文件；对代码这种精确匹配语料，grep 常比语义向量更准（即 Agentic 检索思想）

**生产系统里四层并存，各管一摊：**

```
system prompt / 规则   →  "怎么做事"（永远在场，小而关键）
memory / 摘要          →  "刚才发生了什么"（对话压缩）
RAG                    →  "世界/领域知识"（按需检索，海量）
工具检索               →  "精确查询"（数据库、grep、API）
```

> 💡 **对照本路线图：** B1 小说管线（角色卡 DB + 情节向量库 = RAG 管设定与前情；摘要链 = compression memory 管超长文本）和 web chat 的"服务端截断保留最近 20 轮"（最朴素的 memory 窗口策略）都是这套分层的实例。

> 一句话：**规则是"永远带上的说明书"，memory 是"对话的压缩快照"，RAG 是"按问题查资料"—— 分别解决指令遵循、会话延续、外部知识三个问题，组合使用而非互相替代。**

---

## 二、学习资料

### 🇨🇳 中文入门（先看，建立直觉）

| 资料 | 价值 |
|------|------|
| [一文读懂大模型 RAG（含高级方法）— 知乎](https://zhuanlan.zhihu.com/p/675509396) | 最快建立直觉 |
| [RAG 全面指南 — Elastic 中文](https://www.elastic.co/cn/what-is/retrieval-augmented-generation) | 官方权威，概念清晰 |
| [什么是 RAG — AWS 中文](https://aws.amazon.com/cn/what-is/retrieval-augmented-generation/) | 配图好，适合入门 |
| [什么是 RAG — Google Cloud 中文](https://cloud.google.com/use-cases/retrieval-augmented-generation?hl=zh-CN) | 传统 IR 与 LLM 结合的视角 |
| [RAG 工作原理 — IBM 中文](https://www.ibm.com/cn-zh/think/topics/retrieval-augmented-generation) | 概念定义权威 |
| [检索增强生成 — Prompt Engineering Guide 中文版](https://www.promptingguide.ai/zh/techniques/rag) | 系统教程，含原理+代码 |

### 🌍 英文进阶（深入必读）

| 资料 | 价值 |
|------|------|
| [What Is RAG in 2026 — Atlan](https://atlan.com/know/what-is-rag/) | 2026 年视角的完整概览 |
| [12 Advanced RAG Techniques — Atlan](https://atlan.com/know/advanced-rag-techniques/) | **进阶必读**：查询改写、混合检索、重排序 |
| [15 Advanced RAG Techniques — Neo4j](https://neo4j.com/blog/genai/advanced-rag-techniques/) | 含 GraphRAG 等前沿方法 |
| [RAG Techniques Compared — Starmorph](https://blog.starmorph.com/blog/rag-techniques-compared-best-practices-guide) | **Adaptive RAG**（2026 最佳实践：按查询复杂度路由） |
| [Designing Production-Grade RAG](https://levelup.gitconnected.com/designing-a-production-grade-rag-architecture-bee5a4e4d9aa) | 生产架构设计 |
| [10 RAG Shifts in 2026 — Microsoft Azure](https://medium.com/microsoftazure/10-rag-shifts-redefining-production-ai-in-2026-7acbdd66076c) | 2026 年的 10 大变化 |
| [RAG vs Graph RAG vs Agentic RAG — ByteByteGo](https://newsletter.bytebytego.com/p/rag-vs-graph-rag-vs-agentic-rag) | 三条路线的取舍，一图看懂 |
| [Is GraphRAG Needed? — arXiv 2026](https://arxiv.org/html/2606.25656v1) | **冷水文**：简单 RAG 多数场景可打平 GraphRAG，且开销低得多 |
| [RAG vs. Long Context in 2026 — Towards AI](https://pub.towardsai.net/rag-vs-long-context-in-2026-when-retrieval-still-wins-e6ebad9a4096) | 长上下文时代 RAG 的定位：决策因素是成本/延迟/新鲜度，不是窗口大小 |
| [How Anthropic Is Reinventing RAG with Contextual Retrieval](https://jhparmar.medium.com/how-anthropic-is-reinventing-rag-systems-with-contextual-retrieval-0ed7706ca0a0) | chunk 补上下文再嵌入，大幅降低检索失败率 |
| [Reranker Guide — acta.ai](https://acta.ai/blogs/build-a-reranker-text-ranking-for-search-and-rag) | cross-encoder / LLM 重排实操（含代码） |
| [Agentic RAG vs. GraphRAG — AWS Builder](https://builder.aws.com/content/3KJJFgfpoZmb47QJEc6VDIcXL9q/agentic-rag-vs-graphrag-why-vector-search-alone-is-failing-your-llm-in-production) | 纯向量检索在生产会失败：Agentic 管检索决策，GraphRAG 管数据关系 |
| [RAG and Long Context: Why You Need Both — Google Cloud](https://medium.com/google-cloud/rag-and-long-context-windows-why-you-need-both-1b75cf4509d9) | 官方建议：RAG 管常规查询，长上下文管复杂跨文档推理 |
| [Long Context vs RAG Performance — Databricks](https://www.databricks.com/blog/long-context-rag-performance-llms) | 实测：上下文越长性能退化（lost in the middle） |

### 🎥 视频

- [Is RAG Dead in 2026? — 从第一性原理构建本地 RAG](https://www.youtube.com/watch?v=jdknLDkBS3k)（YouTube）
- [Advanced Retrieval Pipeline (HyDE + Hybrid + Reranking)](https://www.youtube.com/watch?v=_ZHM4wsUwPs)（YouTube）

### 📄 论文（想深入原理）

- **Lewis et al. 2021** — RAG 开山之作 *[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)*
- [大语言模型检索增强生成优化技术综述 — 计算机学报 2025](http://cjc.ict.ac.cn/online/onlinepaper/008_yl-2026227143149.pdf)（中文综述）
- [RAG 驱动的知识服务：原理、范式及评估 — SciOpen 2025](https://www.sciopen.com/local/article_pdf/10.16510/j.cnki.kjycb.20250409.002.pdf)

---

## 三、进阶 RAG 的关键技术（2026 生产标准）

朴素 RAG 之外，现代系统在**索引侧**和**查询侧**分别叠加这些层：

**索引侧（建库时做一次）：**

```
[切块 + Contextual Retrieval]  切块后给每个 chunk 补一段 LLM 生成的原文语境说明，再嵌入   ← 大幅降低检索失败率
```

**查询侧（每次提问时）：**

```
用户查询
  ↓
[查询改写]  HyDE / 子问题分解 / 同义扩展        ← 提升召回
  ↓
[混合检索]  向量检索(语义) + BM25(关键词)       ← 兼顾语义和精确匹配
  ↓
[重排序]    Cross-encoder 对候选重新打分         ← 提升精度
  ↓
[自适应路由] 简单问题走快路，复杂问题走深路      ← Adaptive RAG
  ↓
[生成 + 引用标注]
```

### 关键术语速查

| 术语 | 含义 | 解决什么问题 |
|------|------|-------------|
| **Chunking** | 把长文档切成小块 | 单次检索粒度可控，避免上下文过长 |
| **Contextual Retrieval** | 嵌入前给 chunk 补一段 LLM 生成的原文语境说明 | 脱离语境的 chunk 检索失败率高（Anthropic） |
| **Embedding** | 把文本转成向量 | 让"语义相似"可计算 |
| **Hybrid Search** | 向量 + 关键词联合检索 | 向量擅长语义，关键词擅长专有名词/代码 |
| **Reranking** | 用 cross-encoder 重排 top-K | 双塔召回快但粗，重排提精度 |
| **HyDE** | 让 LLM 先编一个"假想答案"再去检索 | 用户问题太短/太模糊时提升召回 |
| **Query Rewriting** | 改写/扩展用户查询 | 口语化、多义、指代问题 |
| **Adaptive RAG** | 按查询复杂度路由不同管线 | 简单查询别浪费算力，复杂查询别太草率 |
| **Agentic RAG** | Agent 循环决定检索什么、检索几步、自我校验（Self-RAG / Corrective RAG） | 复杂多跳问题、需拆解的研究型查询 |
| **GraphRAG** | 用知识图谱组织检索 | 跨文档推理、全局性问题 |

### 五条技术路线对比（2026-10 调研）

2026 年的共识不是"五选一"，而是**分层组合**：快路径用经典 RAG（混合检索 + 重排序），复杂问题才上 Agentic 检索，GraphRAG 只在关系型查询真的痛时才用。

| 路线 | 核心思路 | 优势 | 代价 | 适合场景 |
|------|---------|------|------|---------|
| 朴素 RAG | 向量检索 → 拼 prompt → 生成 | 便宜、快、好调试 | 多跳问题弱、易漏检 | 延迟敏感场景（如游戏 NPC） |
| **Hybrid + Rerank**（生产基线） | BM25 + 向量双路召回 → cross-encoder 重排 | 显著降漏检，成本增量小 | 维护两路索引 | 绝大多数生产系统 |
| GraphRAG | 知识图谱 + 向量，按实体关系检索 | 关系型/多跳问题强 | 构建贵、更新慢 | 关系密集型语料 |
| Agentic RAG | Agent 循环决定检索什么/几步，自我校验 | 最强，能拆解复杂问题 | 慢、贵、难调试 | 研究型深度问答 |
| 长上下文（不用 RAG） | 语料全塞 prompt | 小数据时准确率可反超 | 成本随语料线性涨、lost-in-the-middle | 语料小且稳定 |

**四个关键判断**（来源见第二节资料表）：

1. **混合检索 + 重排是底线，不是可选项** — 纯向量检索在生产中会失败（AWS Builder，2026-10）
2. **GraphRAG 是特定痛点的解药，不是默认架构** — 简单 RAG 多数场景可打平且开销低得多（arXiv，2026-06）
3. **"能不能塞进上下文窗口"已不是决策因素** — 决策因素变成成本、延迟、新鲜度、权限；大规模语料下 RAG 成本优势碾压（Towards AI，2026-10）
4. **Contextual Retrieval 值得尽早上** — 嵌入前给 chunk 补上下文，大幅降低检索失败率（Anthropic）

**落地到本路线图：**

| 场景 | 推荐架构 | 理由 |
|------|---------|------|
| 游戏 NPC 对话（方向 A1） | 朴素 RAG + Hybrid，不上 Agentic | 实时场景，延迟/成本敏感；每句话都走 Agent 循环太贵 |
| 小说一致性（方向 B1） | 角色卡 DB + 情节向量库 + 摘要链 | 结构化记忆 + 向量即可；仅当人物关系多跳推理频繁出错，才考虑给角色关系单独建图谱 |
| 小说多 Agent 管线（方向 B1） | LangGraph 编排写作 Agent，检索层仍用简单 RAG | 编排的是"写作"不是"检索"，两层分开、不冲突 |

**技术深化顺序**（对应上方生产基线的搭建顺序）：

```
第 1 步：自建 embedding + pgvector + BM25 混合检索     ← 理解原理
第 2 步：加 Reranker（bge-reranker-v2-m3 / Cohere）   ← 2026 生产底线
第 3 步：切块时做 Contextual Retrieval                 ← chunk 带语境再嵌入
第 4 步：按需加 Adaptive 路由                          ← 简单问题走快路，复杂问题才进 Agent 检索
```


---

## 四、三种实现方案对比

### 方案 A：LlamaIndex

**定位：为「数据 → 索引 → 检索 → 问答」而生，RAG 专精。**

| 维度 | 评价 |
|------|------|
| RAG 能力 | ⭐⭐⭐⭐⭐ 最全，高级检索技术覆盖最好 |
| 学习曲线 | 中等，API 设计清晰 |
| 灵活性 | 中，围绕「索引/查询引擎」抽象 |
| 适合 | 知识库问答、文档检索、企业搜索 |
| 社区评价 | 企业开发者为稳定性偏好它 |

### 方案 B：LangChain（+ LangGraph）

**定位：通用 LLM 编排框架，RAG 只是它众多能力之一。**

| 维度 | 评价 |
|------|------|
| RAG 能力 | ⭐⭐⭐⭐ 够用，但不如 LlamaIndex 深 |
| 学习曲线 | 偏陡，概念多（Chain/Agent/Tool/Memory） |
| 灵活性 | ⭐⭐⭐⭐⭐ 最高，能做 Agent、工具调用、多步推理 |
| 适合 | 需要 Agent + 工具 + 多步任务的复杂应用 |
| 2026 趋势 | 编排重心转向 **LangGraph**（状态机/多 Agent） |
| 2026 中观察 | 生产团队收敛到「LlamaIndex 管检索 + LangGraph 管编排 + 裸 API 调用」的混用模式，不押注单一框架 |

### 方案 C：自建 embedding + pgvector

**定位：不用框架，PostgreSQL + pgvector 扩展自己写。**

| 维度 | 评价 |
|------|------|
| 可控性 | ⭐⭐⭐⭐⭐ 完全透明，无黑盒 |
| 运维 | ⭐⭐⭐⭐ 只需一个 PostgreSQL，少一个组件 |
| 性能 | 配合 **pgvectorscale**（Timescale 扩展），50M 向量下 471 QPS@99% recall，据称比 Qdrant 还快 |
| 学习价值 | ⭐⭐⭐⭐⭐ **最能让你真正理解 RAG 每一步** |
| 适合 | 已用 Postgres、中小规模（百万级向量）、想深入理解原理 |

### 对比参考文章

- [LlamaIndex vs LangChain: Which To Choose In 2026 — Contabo](https://contabo.com/blog/llamaindex-vs-langchain-which-one-to-choose-in-2026/)
- [LlamaIndex vs LangChain: RAG framework differences — Statsig](https://www.statsig.com/perspectives/llamaindex-vs-langchain-rag)
- [Llamaindex vs Langchain — IBM Think](https://www.ibm.com/think/topics/llamaindex-vs-langchain)
- [RAG Frameworks: LangChain vs LangGraph vs LlamaIndex — AIMultiple](https://aimultiple.com/rag-frameworks)
- [LLM Orchestration Frameworks Compared — MachineLearningMastery](https://machinelearningmastery.com/llm-orchestration-frameworks-compared-langchain-vs-llamaindex-vs-raw-api-calls)
- [LangChain vs LlamaIndex: 2026 Framework Guide — PE Collective](https://pecollective.com/blog/ai-orchestration-frameworks-2026)
- [Vector Databases in 2026: pgvector, Qdrant, Pinecone — Dev Note](https://devstarsj.github.io/2026/03/31/vector-databases-pgvector-qdrant-pinecone-production-comparison-2026/)
- [When to Use pgvector vs Pinecone — DEV](https://dev.to/polliog/postgresql-as-a-vector-database-when-to-use-pgvector-vs-pinecone-vs-weaviate-4kfi)
- [Top 15 Vector Databases in 2026 — Medium](https://medium.com/@pratik-rupareliya/top-15-vector-databases-in-2026-a-production-decision-guide-from-100-enterprise-deployments-dd58a04f51a5)

---

## 五、选型建议与学习路径

### 🎯 推荐学习路径

```
第 1 步：先用 pgvector 手写一个最小 RAG（1~2 天）
         ── 真正理解 embedding / 相似度 / chunk / 检索 每一步
         ── 这是地基，框架会屏蔽这些细节

第 2 步：用 LlamaIndex 重写同一个 demo（1 天）
         ── 体会框架帮你省了什么、封装了什么
         ── 学它的高级检索（Hybrid / Rerank / SubQuestion）

第 3 步：按需了解 LangChain / LangGraph
         ── 当你想做 Agent、工具调用、多步推理时再用

第 4 步：生产化向量库选型
         ── 小规模 / 已用 Postgres → pgvector（+ pgvectorscale）
         ── 纯向量大规模 → Qdrant
         ── 不想运维 → Pinecone（托管）
```

### 为什么先自建？

框架（LlamaIndex/LangChain）会让你**很快做出能跑的东西**，但也会让你**不理解它在干什么**。手写一遍 `embedding → 存向量 → 余弦相似度查询 → 拼 prompt`，你以后用任何框架都能心里有数、知道怎么调优。

> 符合本 repo 的避坑原则：「先 API 后框架 — 原生 API 调通后再引入框架」「学原理不学框架」。

### 生产向量库选型决策树

```
是否已用 PostgreSQL？
  ├─ 是 → pgvector (+ pgvectorscale)，百万级以内首选
  └─ 否 → 数据规模？
           ├─ 中小（< 千万向量）→ Qdrant（自托管）或 pgvector
           ├─ 大规模 / 高并发 → Qdrant 集群 / Milvus
           └─ 不想运维 → Pinecone（全托管）
```

---

## 六、推荐技术栈（pgvector 路线）

| 组件 | 推荐选型 | 备注 |
|------|---------|------|
| Embedding 模型 | `text-embedding-3-small`（OpenAI）或 `bge-m3`（开源，中文好） | 开发期用 API，生产可自托管 bge |
| 向量库 | PostgreSQL + pgvector（+ pgvectorscale 提速） | 一个库搞定关系数据 + 向量 |
| 框架 | 可选 LlamaIndex 或纯 SQL 手写 | 学习期建议手写 |
| Rerank 模型 | `bge-reranker-v2-m3`（开源） | 显著提升精度 |
| 评估工具 | RAGAS 或 TruLens | 衡量检索/生成质量，不可跳过 |

### 评估为什么重要

没有评估就没有调优方向。RAG 的两个核心指标：
- **检索质量** — 召回率（relevant chunk 有没有被检索到）
- **生成质量** — 忠实度（答案是否基于检索内容，而非幻觉）

[RAGAS 文档](https://docs.ragas.io/) / [TruLens 文档](https://www.trulens.org/)

---

## 七、与本 repo 的关系

- ✅ **这里放**：学习路线、概念梳理、选型决策、资料链接
- 🚫 **不放这里**：具体 RAG 实现代码、demo 项目
- 实现会在独立 repo 进行（如 `rag-lab` 或类似），完成后在此处补上链接
- 🔗 **相关实战**：[Web AI NPC 聊天](../references/web-chat/) — LLM API 流式调用、token 统计、会话管理已落地（RAG 生成层的基础能力），检索管线实现待做
