# Programmatic Execution Runtime

## 我们的架构分析

如果把 PTC 仅实现成一个 `python` Tool，会低估它的风险和平台能力要求。生产级代码执行需要真正的 Programmatic Execution Runtime：

```text
Programmatic Execution Runtime
├── Sandbox / Isolation
├── Workspace
├── Capability Proxy
├── Permission Policy
├── Data Flow Policy
├── Resource Budget
├── Secrets Isolation
├── Action Trace
├── Kill / Timeout
└── Recovery
```

关键原则：

### Code Permission != Business Capability Permission

允许程序执行 Python，不代表它自动获得 GitHub、数据库或 Slack 权限。程序内部仍必须通过 Capability Proxy 调用受治理 Tool。

### Effective Permission

```text
Effective Permission
≈ Sandbox Boundary
  ∩ Capability Grant
  ∩ User Permission
  ∩ Task Policy
```

### PTC 不绕过治理

直接 Tool Call 需要的授权、Approval、Audit，在 PTC 内部仍然存在。改变的是 orchestration，不是 security semantics。

## 对 Agent Platform 的影响

Code Execution 属于 L2 Agent Work Environment 的执行能力，PTC 属于 L4 Execution Strategy；二者不能混为一个组件。

## 核心结论

> **PTC 需要受治理的 Programmatic Execution Plane，而不是一个拥有无限权限的 Python Tool。**