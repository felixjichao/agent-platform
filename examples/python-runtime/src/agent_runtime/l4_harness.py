from __future__ import annotations

from .models import CompleteDecision, Decision, ExecuteDecision, FailDecision, RuntimeSnapshot


class ReportHarness:
    """L4 deterministic harness used in the example.

    Replacing this class with an LLM-based agent loop does not change L3 or L2.
    """

    revision = "report-harness@1"

    def next(self, snapshot: RuntimeSnapshot) -> Decision:
        state = snapshot.checkpoint.harness_state
        step = state["step"]

        if step == "read_source":
            return ExecuteDecision(
                action_name="read_text",
                arguments={"path": state["source_path"]},
                next_harness_state={**state, "step": "write_report"},
            )

        if step == "write_report":
            source = self._latest_content(snapshot, "read_text_result")
            if source is None:
                return FailDecision("missing read_text observation")
            first_line = next((line.strip("# ") for line in source.splitlines() if line.strip()), "无标题")
            report = "\n".join(
                [
                    "# Agent Platform 案例报告",
                    "",
                    f"来源摘要：输入文档标题为“{first_line}”。",
                    "",
                    "## 架构判断",
                    "",
                    "Runtime 管事实，Harness 管策略，Environment 管执行机制。",
                    "",
                    "## 可靠性验证",
                    "",
                    "动作与执行尝试分离；结果未知时先核对真实世界，再决定是否重试。",
                    "",
                ]
            )
            return ExecuteDecision(
                action_name="write_text",
                arguments={
                    "path": state["output_path"],
                    "content": report,
                    "simulate_timeout_after_commit": True,
                },
                next_harness_state={**state, "step": "complete"},
            )

        if step == "complete":
            write_result = self._latest_content(snapshot, "write_text_result")
            if write_result is None:
                return FailDecision("missing write_text observation")
            return CompleteDecision(
                output={"report": state["output_path"], "write": write_result},
                artifact_kind="markdown_report",
                artifact_uri=state["output_path"],
            )

        return FailDecision(f"unknown harness step: {step}")

    @staticmethod
    def _latest_content(snapshot: RuntimeSnapshot, kind: str):
        for observation in reversed(snapshot.observations):
            if observation.kind == kind and observation.content.get("status") == "succeeded":
                if kind == "read_text_result":
                    return observation.content.get("content")
                return observation.content
        return None

