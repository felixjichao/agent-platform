# Budget、Trace 与 Governance

## 我们的架构分析

PTC 把一个高层 Action 展开成大量内部执行，因此需要新的预算和 Trace 粒度。

### Program Budget

至少包括：

```text
max_tool_calls
max_runtime
max_cost
max_parallelism
max_cpu / memory
max_data_read / write
```

Harness 可以生成任意复杂程序，但 Runtime 必须保证程序不会无限循环或爆炸式调用。

### Action Trace

错误做法：

```text
CodeExecutionStarted
CodeExecutionSucceeded
```

中间完全黑盒。

正确做法：

```text
Program Execution
├── Action A
├── Action B
├── Action C
├── Policy Decision
├── Retry
└── Result
```

平台仍然能回答：

- 调用了什么 Capability；
- 读写了什么资源；
- 哪一步被拒绝；
- 总预算消耗多少。

## 对 Agent Platform 的影响

Run Trace 需要支持层级结构：Reasoning Step → Program → Actions。Observability 和 Security 都不能止于外层代码执行事件。

## 核心结论

> **PTC 提高了组合能力，也放大了调用和数据流风险；必须对程序内部 Action 做预算、授权和可观测治理。**