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

> ⚠️ 2026 年的共识：**"把 PDF 塞进向量库就完事"的朴素 RAG 已经不够用了**。生产级系统都在用进阶技术（见第三节）。

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

### 🎥 视频

- [Is RAG Dead in 2026? — 从第一性原理构建本地 RAG](https://www.youtube.com/watch?v=jdknLDkBS3k)（YouTube）
- [Advanced Retrieval Pipeline (HyDE + Hybrid + Reranking)](https://www.youtube.com/watch?v=_ZHM4wsUwPs)（YouTube）

### 📄 论文（想深入原理）

- **Lewis et al. 2021** — RAG 开山之作 *[Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)*
- [大语言模型检索增强生成优化技术综述 — 计算机学报 2025](http://cjc.ict.ac.cn/online/onlinepaper/008_yl-2026227143149.pdf)（中文综述）
- [RAG 驱动的知识服务：原理、范式及评估 — SciOpen 2025](https://www.sciopen.com/local/article_pdf/10.16510/j.cnki.kjycb.20250409.002.pdf)

---

## 三、进阶 RAG 的关键技术（2026 生产标准）

朴素 RAG 之外，现代系统通常叠加这些层：

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
| **Embedding** | 把文本转成向量 | 让"语义相似"可计算 |
| **Hybrid Search** | 向量 + 关键词联合检索 | 向量擅长语义，关键词擅长专有名词/代码 |
| **Reranking** | 用 cross-encoder 重排 top-K | 双塔召回快但粗，重排提精度 |
| **HyDE** | 让 LLM 先编一个"假想答案"再去检索 | 用户问题太短/太模糊时提升召回 |
| **Query Rewriting** | 改写/扩展用户查询 | 口语化、多义、指代问题 |
| **Adaptive RAG** | 按查询复杂度路由不同管线 | 简单查询别浪费算力，复杂查询别太草率 |
| **GraphRAG** | 用知识图谱组织检索 | 跨文档推理、全局性问题 |

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
- 实现会在独立 repo 进行（如 `rag-lab` 或类似），完成后在此处补上链接。
