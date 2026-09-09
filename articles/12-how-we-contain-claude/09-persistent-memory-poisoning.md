# Persistent Memory Poisoning

## 文章中的关键观点

文章展望了持久状态带来的 Memory Poisoning：如果恶意内容被写入长期 Memory、Workspace 配置或跨 Session 状态，后续启动时可能持续重新进入 Context。

## 我们的架构分析

一次 Prompt Injection：

```text
Malicious Content
→ Current Context
→ Session ends
→ effect disappears
```

持久污染：

```text
Malicious Content
   ↓
Agent summarizes / writes
   ↓
Memory / Notes / CLAUDE.md / Workspace State
   ↓
New Session
   ↓
Startup loads poisoned state
   ↓
Persistent Influence
```

因此长期 Memory 写入不是低风险内部操作，它近似于：

> **修改未来 Agent 的启动 Context。**

建议 Promotion Pipeline：

```text
External Content
      ↓
Working Memory
      ↓
Candidate Memory
      ↓
Trust / Validation / Provenance
      ↓
Long-term Memory
```

Memory Entry 需要保留 source refs、provenance、trust、created_by、promotion reason。

Recall 排序也要考虑 Trust，而不只是 semantic similarity、recency 和 importance。

## 对 Agent Platform 的影响

Session Startup 本身成为 Context Ingress Boundary。Memory Promotion、Compaction Summary 和长期 Recall 都需要 Trust-aware Governance。

## 核心结论

> **持久 Memory 会把 Prompt Injection 从 Session-level 风险升级成跨 Session Persistence Attack。**