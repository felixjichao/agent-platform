# Research Eval 与 Judge Topology

## 我们的架构分析

对 Research Agent，最终文本质量不能只看“像不像好文章”，更适合围绕证据链评估：

```text
Claims
  ↓ supported by
Evidence Refs
  ↓ point to
Source Refs
```

关键维度包括：

- Groundedness：结论是否被证据支持；
- Coverage：是否覆盖关键问题；
- Source Quality：证据来源是否可靠；
- Factual Accuracy：事实是否准确；
- Synthesis：是否正确整合冲突信息。

### Judge Topology

对于多维开放任务，一个超大 Judge Prompt 同时打所有分不一定最佳。可以采用独立 Judge：

```text
Groundedness Judge
Coverage Judge
Source Quality Judge
Synthesis Judge
```

再统一聚合。

这种拓扑是否值得使用，应通过与 Human Ground Truth 的相关性校准，而不是因为“多 Agent 看起来更高级”。

## 对 Agent Platform 的影响

Research 的 Execution、Citation、Eval 和 Audit 应尽量复用同一 Evidence Chain。Judge Strategy 可变，Evaluation Contract 保持稳定。

## 核心结论

> **Research Eval 应围绕 Claim → Evidence → Source 建立可追溯证据链；Judge 是可替换策略，不是评估标准本身。**