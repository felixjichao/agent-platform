# Demystifying evals for AI agents

- 原文：<https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
- 研究主题：把 Eval 从“给回答打分”升级为对完整 Agent Trial、环境、证据、结果和可靠性的系统测量。

## 小节

1. [Trial 才是 Agent Eval 的基本单位](01-trial-as-eval-unit.md)
2. [Grader、Criterion 与 Evidence](02-graders-and-evidence.md)
3. [非确定性：pass@k 与 pass^k](03-nondeterminism-and-pass-k.md)
4. [Capability Eval 与 Regression Eval](04-capability-vs-regression.md)
5. [Task Spec 与 Eval Environment](05-task-spec-and-environment.md)
6. [Eval 系统本身也必须被验证和版本化](06-eval-system-validation.md)
7. [从离线 Eval 到整体质量系统](07-quality-system.md)
8. [Research Eval 与 Judge Topology](08-research-eval-and-judge-topology.md)
9. [Eval 是可执行的 Capability Specification](09-eval-as-capability-spec.md)

## 对平台架构的核心影响

- Eval Unit 是 Trial，不是单条回复。
- Transcript / Trace 与 Outcome 必须分离保存。
- Task、Trial、Grader、Environment、Harness 和 Score 都需要版本与可追溯关系。
- Eval Infrastructure 属于平台能力，Eval Content 属于具体 Capability 的资产。
- Eval 最终不仅验证质量，也定义“这个 Capability 到底算会了什么”。