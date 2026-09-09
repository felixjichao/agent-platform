# Harness design for long-running application development

- 原文：<https://www.anthropic.com/engineering/harness-design-long-running-apps>
- 研究主题：长时间应用开发中的执行一致性、自评估和 Harness 可移除性。

## 小节

1. [长任务不只需要连续性，还需要执行一致性](01-execution-coherence.md)
2. [生成与评估必须分离](02-generator-evaluator-separation.md)
3. [Acceptance Criteria 与 Quality Criteria](03-acceptance-vs-quality.md)
4. [Evaluation Contract](04-evaluation-contract.md)
5. [Harness 是可移除的脚手架](05-harness-as-removable-scaffolding.md)
6. [Trace + Eval 形成 Harness Engineering 闭环](06-trace-eval-feedback-loop.md)

## 对平台架构的核心影响

- 长任务不仅要能恢复，还要持续判断当前结果是否真的满足目标。
- Harness 负责“如何完成”，Evaluation Contract 负责“怎样证明完成”。
- 生成者和评估者应尽量分离，避免同一个执行路径自证正确。
- Harness 的复杂结构是对当前模型能力的补偿，必须通过 Eval 持续检验其必要性。