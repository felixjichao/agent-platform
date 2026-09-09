# AGENTS.md

本文件定义自动化 Agent、Coding Agent 和其他代码生成工具在本仓库中工作时必须遵守的约束。

## 文档首页同步

`README.md` 面向 GitHub 仓库首页，`index.md` 面向 VitePress / GitHub Pages 首页。两者职责不同，但核心项目定位、架构判断和研究路线必须保持同步。

**强制规则：修改 `README.md` 时，必须同时检查并按需更新 `index.md`。**

尤其当 `README.md` 发生以下变化时，必须同步更新 `index.md`：

- 项目定位或核心观点变化；
- 核心架构判断增加、删除或调整；
- Agent Software Stack 等总体架构变化；
- 研究路线、文章列表或主要阅读入口变化。

提交前必须确认：

```text
README.md changed
      ↓
review index.md
      ↓
update index.md when affected
      ↓
Docs CI passes
```

仓库的 Docs CI 会检查：如果 `README.md` 被修改而 `index.md` 没有同步修改，则构建失败。

不要通过删除、绕过或弱化该 CI 检查来规避此约束。
