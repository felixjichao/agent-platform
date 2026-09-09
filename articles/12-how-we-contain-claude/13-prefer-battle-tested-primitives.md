# 优先使用 Battle-tested Security Primitives

## 文章中的关键观点

Anthropic 总结多次安全问题时发现，成熟的 hypervisor、seccomp、gVisor、Seatbelt、bubblewrap 等基础安全原语往往比自研 allowlist、proxy 和启动 glue logic 更可靠。

## 我们的架构分析

Agent 是新的软件形态，但系统级行为并不新：

```text
read files
open sockets
spawn processes
use credentials
call APIs
```

这些问题已有长期成熟的安全机制。因此平台应该把：

### Governance / Policy

作为 Agent-specific 创新重点：

- Goal / Risk；
- Capability Policy；
- Trust Policy；
- Data Flow Policy；
- Approval Policy；
- Containment Profile。

### Enforcement Primitives

尽量复用成熟基础设施：

- Hypervisor；
- OS Sandbox；
- Filesystem ACL / namespace；
- Firewall / proxy；
- IAM / scoped credential；
- Resource limit。

```text
Governance Policy
      ↓ compile
Containment Profile
      ↓
Battle-tested Enforcement Primitives
```

需要注意：Primitive 正确不等于系统一定安全。成熟原语解决“边界能否可靠执行”，平台仍然需要正确决定“边界应该画在哪里”。

## 对 Agent Platform 的影响

不要构建一个包办一切的自研 Agent Security Runtime。更合理的是 Governance Plane 定义边界，Work Environment / Infrastructure 使用成熟 Primitive 执行边界。

## 核心结论

> **Governance 决定边界画在哪里；成熟 Infrastructure 保证 Agent 越不过边界。**

> **Agent-specific innovation should focus on policy composition, not reinventing isolation primitives.**