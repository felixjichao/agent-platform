# Containment 与 Observability 的张力

## 文章中的关键观点

强 VM 隔离可以限制 Agent，但同时也可能让 Host 上的 EDR / Security Agent 无法看到 VM 内部进程、文件和网络行为。Isolation 与 Visibility 需要共同设计。

## 我们的架构分析

存在一个重要张力：

```text
Isolation ↑
→ Blast Radius ↓
→ Host Visibility 也可能 ↓
```

所以被隔离环境必须有受控的 Out-of-band Telemetry：

```text
Sandbox / VM
   ├── normal egress → restricted
   └── telemetry channel
       ├── structured
       ├── append-oriented
       └── controlled destination
```

至少应记录：

- process events；
- Capability / Tool Actions；
- filesystem changes / violations；
- network attempts；
- credential use；
- policy decisions；
- resource limits。

还应区分：

### Agent Trace

解释 Agent 为什么这么做：model step、delegation、tool selection、outcome。

### Security Trace

记录 Agent 实际触碰了什么确定性边界：process、filesystem、network、credential、policy enforcement。

Security Trace 应尽量来自 Sandbox、Proxy、Hypervisor、Capability Gateway 等更靠近 Enforcement 的位置。

## 对 Agent Platform 的影响

Containment Architecture 必须同时定义 Telemetry Contract。Governance = Policy + Enforcement + Observability。

## 核心结论

> **Containment 与 Observability 必须共同设计；越强的隔离越需要可信的 out-of-band security telemetry。**