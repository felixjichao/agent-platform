# Verification Ladder 与 Cost per Successful Outcome

## 文章中的关键观点

编译器团队不是修完单个错误就宣布成功，而是逐步通过越来越接近真实目标的测试：局部测试、回归、真实程序、Linux 构建以及不同架构验证。

## 我们的架构分析

可以抽象出 Verification Ladder：

```text
Local Checks
   ↓
Regression
   ↓
Representative Workloads
   ↓
Integration
   ↓
Production-like Verification
```

越靠后越昂贵，但也越接近真实 Acceptance。

Verifier 还应提供 **Differential Oracle**：不仅说 pass / fail，还给 Agent 高信号差异反馈，帮助下一轮行动。

成本指标也应从：

```text
cost per token / request
```

升级为：

```text
Cost per Successful Outcome
```

因为便宜但成功率极低的执行策略并不真正高效。

## 对 Agent Platform 的影响

Verification 需要分层调度，Harness 可以先使用便宜检查快速反馈，再在接近完成时升级到高成本真实验证。

## 核心结论

> **验证应形成从便宜局部反馈到昂贵真实验收的阶梯；成本最终应按成功结果衡量。**