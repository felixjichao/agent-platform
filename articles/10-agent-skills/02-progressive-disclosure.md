# Progressive Disclosure：发现与加载分离

## 文章中的关键观点

Skill 不会把全部内容一次性加载进 Context，而是分层暴露：先看到 name / description，需要时再读取 `SKILL.md`，进一步需要时才读取 references、scripts 和 resources。

## 我们的架构分析

这是标准的 Progressive Disclosure：

```text
Level 1
Skill Metadata
name + description
      ↓ activate
Level 2
SKILL.md
      ↓ navigate
Level 3
references / scripts / resources
```

它与 Tool Discovery 的本质一致：

> **Discovery != Loading。**

Metadata 实际上是一种 Knowledge Routing Prompt。它必须足够准确，让 Agent 知道何时激活，也必须足够克制，避免所有 Skill 同时进入 Context。

随着 Skill 数量扩大，还可以引入层级 Discovery：Domain → Skill Family → Skill。

## 对 Agent Platform 的影响

Capability Catalog 可以统一支持 Tool / Skill 的“轻量发现元数据 + JIT 详细加载”。

## 核心结论

> **Skill 的关键不是文件格式，而是可发现、可导航、按需加载的程序性知识。**