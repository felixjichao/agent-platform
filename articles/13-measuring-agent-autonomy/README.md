# Measuring AI agent autonomy in practice

- 原文：<https://www.anthropic.com/research/measuring-agent-autonomy>
- 发布时间：2026-02-18
- 研究主题：真实部署中的智能体自主性如何由模型、用户监督方式和产品设计共同形成，以及如何在风险边界内观测和治理这种自主性。

## 小节

1. [自主性是部署特征，不是模型属性](01-autonomy-as-deployment-characteristic.md)
2. [人工监督不等于逐步审批](02-oversight-as-control-transfer.md)
3. [自主性是测量投影，不是运行时事实](03-measuring-autonomy.md)
4. [自主性必须与风险联合治理](04-autonomy-and-risk-governance.md)
5. [部署后监控补足上线前评估](05-post-deployment-monitoring.md)
6. [从人工审批走向可监督执行](06-supervisory-control.md)

## 对平台架构的核心影响

- 自主性（Autonomy）不是模型或智能体的静态等级，而是模型能力、执行框架、权限边界、产品设计和人工监督共同形成的部署特征。
- 执行策略与自主性是两个不同维度：工作流、多智能体或智能体循环都可以表现出不同程度的自主性。
- 人工监督应从“每一步审批”扩展为观察、中断、纠偏、澄清、评审、升级和验收等动态控制权转移机制。
- 运行、动作和控制权转移事件是事实；自主性指标是基于这些事实形成的测量投影。
- 自主性不能单独优化，应在风险、可逆性、可达范围和验证能力约束下动态分配。
- 上线前评估测能力潜力，部署后监控测真实行为；二者共同构成能力演进闭环。

> **生产级智能体的目标不是最大化自主性，而是在可验证、可观察、可干预的边界内，最大化有用的自主性。**
