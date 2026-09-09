# Eval-driven Tool Engineering

## 文章中的关键观点

Anthropic 使用真实任务和 Agent Eval 来迭代工具设计，而不是只检查 API 是否返回正确结果。

## 我们的架构分析

需要区分：

```text
Tool Correctness
→ API 调用本身是否正确

Tool Effectiveness
→ Agent 能否在真实 Task 中发现、选择、调用并正确解释它
```

Tool Engineering 闭环：

```text
Real Tasks
   ↓
Agent Trials
   ↓
Trace Mining
   ↓
Tool-use Smells
   ↓
Tool Revision
   ↓
Held-out / Regression Eval
```

常见 smell：

- wrong-tool switching；
- 重复 retry；
- chaining hotspot；
- oversized result；
- under-utilized tool；
- invalid parameter cluster。

## 对 Agent Platform 的影响

Capability / Tool Revision 需要与 Trial Trace 关联，并拥有自己的 Regression Suite。不能只做服务接口单测。

## 核心结论

> **Tool 是否“好用”必须由 Agent 在真实任务中的 Outcome 和 Trace 证明。**