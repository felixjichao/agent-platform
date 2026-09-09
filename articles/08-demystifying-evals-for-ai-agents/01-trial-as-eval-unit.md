# Trial 才是 Agent Eval 的基本单位

## 文章中的关键观点

Agent 会跨多轮调用模型、使用工具、修改环境并根据中间结果调整策略，因此不能像传统单轮 LLM 一样只对最终 response 打分。

## 我们的架构分析

Agent Eval 的基本对象应该是 **Trial**：

```text
Task
  ↓
Trial
├── Agent / Harness Revision
├── Environment
├── Transcript / Trace
├── Outcome
└── Grader Results
```

其中必须分开：

### Transcript / Trace

描述执行过程发生了什么：

- 模型步骤；
- Action；
- Tool Result；
- Delegation；
- Retry；
- Budget 消耗。

### Outcome

描述执行结束后真实世界处于什么状态、产出了什么结果。

一个过程看起来很合理，并不代表最终 Outcome 正确；反过来，一个成功结果也可能来自成本极高或不可接受的过程。

## 对 Agent Platform 的影响

Eval Harness 应调用真实 Agent Runtime，而不是重新实现一套简化 Agent。Trial 需要关联 Task、Harness Revision、Environment Revision、Trace 和 Outcome。

## 核心结论

> **Agent Eval 的基本单位是完整 Trial；Transcript 描述过程，Outcome 描述结果。**