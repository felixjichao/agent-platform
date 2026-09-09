# Skill、Tool 与 Harness 的边界

## 文章中的关键观点

Agent Skills 通过文件夹中的说明、脚本和资源，把某一类任务所需的领域程序知识按需提供给通用 Agent。

## 我们的架构分析

三个概念解决不同问题：

```text
Tool
→ Agent 能做什么动作？

Skill
→ 这类任务通常应该怎么做？

Harness
→ 当前这个任务此刻怎么推进？
```

Tool 是行动能力；Skill 是可复用程序性知识；Harness 是当前执行策略。

例如 PDF 处理：

- Tool：读写文件、调用转换器、执行脚本；
- Skill：PDF 表单填写的流程、常见陷阱、输出检查方法；
- Harness：当前用户这个 PDF 到底先检查什么、调用哪些步骤、何时完成。

这使 Agent 专门化不再等于“复制一套新 Agent Prompt”。

## 对 Agent Platform 的影响

General Agent 可以在运行时组合 Skill + Tool + Knowledge，而不是为每个业务场景创建静态 Agent 类型。

## 核心结论

> **Tool 是行动能力，Skill 是程序性知识，Harness 是当前任务的执行策略。**