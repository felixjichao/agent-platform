# Work / Session / Run 层级修正

## 我们的架构分析

编译器实验带来的一个重要修正是：长期 Goal 不应该天然等于一个超长 Session。

更合理的层级是：

```text
Work / Project
├── Goal
├── Shared Resources
├── Work Frontier
├── Artifacts
├── Environment / Workspace
├── Long-term Progress
└── Sessions
     └── Runs
```

### Work

长期工作的真实载体。多个 Agent、多个 Session 可以围绕同一个 Work 持续推进。

### Session

一个 Agent 与某个 Work 之间相对连续的认知 / 执行关系。它可以长，也可以短；同一 Work 可以并行存在多个 Session。

### Run

> **Runtime 被触发后，在一个 Session 内发生的一次连续执行片段。**

典型新 Run：

- 新用户消息；
- Human Approval；
- Timer / Webhook；
- Child Completion Event。

基础设施内部恢复通常仍属于同一个 Run，例如 worker restart、tool retry。

## 对 Agent Platform 的影响

长期连续性从“Session 必须永生”转向：

> **Durable work continuity should not depend on durable agent continuity.**

Agent 可以忘记、退出、被替换；Work 必须记住。

## 核心结论

> **Work 承载长期目标与共享世界，Session 承载 Agent 与 Work 的连续关系，Run 承载一次被触发后的连续执行。**