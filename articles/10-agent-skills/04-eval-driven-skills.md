# Eval-driven Skill Engineering

## 我们的架构分析

Skill 不应该因为“我们有一份文档”就被创建。正确起点是 Capability Gap：

```text
Real Task
   ↓
Agent Failure
   ↓
Failure Analysis
   ↓
Procedure / Knowledge Gap?
   ↓ yes
Skill Candidate
   ↓
Eval
   ↓
Publish / Revise
```

Skill 常见失败类型：

- **Discovery Failure**：需要时没找到；
- **False Activation**：不需要时错误激活；
- **Navigation Failure**：激活后找不到具体资源；
- **Instruction Failure**：说明不足或模糊；
- **Over-contexting**：加载过多无关内容；
- **Procedure Failure**：流程本身错误。

因此 Skill Eval 要同时测：

- Activation：该用时会不会用；
- Restraint：不该用时能不能不加载；
- Outcome：激活后是否真的改善任务结果。

## 对 Agent Platform 的影响

Skill Revision 与 Tool Revision 一样，应有 Capability Eval 和 Regression Eval，并与 Trial Trace 关联。

## 核心结论

> **Skill 从真实 Capability Gap 中产生，并通过 Activation + Restraint + Outcome Eval 验证。**