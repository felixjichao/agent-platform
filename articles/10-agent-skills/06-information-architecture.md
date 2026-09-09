# Skill Information Architecture

## 我们的架构分析

随着 Skill 内容增长，最容易出现的问题是把 `SKILL.md` 变成一个超大手册。这样会破坏 Progressive Disclosure。

更合理的是：

```text
SKILL.md
├── 核心原则
├── 决策路径
├── Knowledge Map
└── Resource Entry Points

references/
├── scenario-a.md
├── scenario-b.md
└── deep-details.md
```

拆分原则不是传统文档目录，而是 **Context Co-occurrence**：

> 哪些内容通常会在同一个任务阶段一起被需要？

如果两个主题互斥、很少共同使用，就应该拆开，避免每次激活 Skill 都把所有内容注入 Context。

Skill 也不应该长成 Mega Workflow。它提供方法和导航，但当前任务具体如何执行仍由 Harness 决定。

## 对 Agent Platform 的影响

Skill Authoring Guidelines 应围绕 Context 成本、导航和组合性设计，而不只是 Markdown 风格。

## 核心结论

> **Skill 的信息架构应该按任务上下文的共同出现关系组织，而不是按传统文档分类堆成大手册。**