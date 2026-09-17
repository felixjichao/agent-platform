from __future__ import annotations

from pathlib import Path

from .l1_world import LocalFileWorld
from .models import (
    Action,
    ActionOutcome,
    AttemptResult,
    AttemptResultStatus,
    CapabilityDefinition,
    EvaluationResult,
    ExecutionAttempt,
    Observation,
    OutcomeStatus,
    new_id,
    to_dict,
)


class LocalActionExecutor:
    """L2 execution mechanism; it knows tools, not agent strategy."""

    name = "local-file-executor"

    def __init__(self, world: LocalFileWorld, capability: CapabilityDefinition):
        self.world = world
        self.allowed_tools = {tool.name for tool in capability.allowed_tools}

    def execute(self, action: Action, attempt: ExecutionAttempt) -> AttemptResult:
        if action.name not in self.allowed_tools:
            return AttemptResult(
                result_id=new_id("result"),
                attempt_id=attempt.attempt_id,
                status=AttemptResultStatus.PERMANENT_ERROR,
                error=f"Tool is not granted: {action.name}",
            )

        try:
            if action.name == "read_text":
                content = self.world.read_text(action.arguments["path"])
                return AttemptResult(
                    result_id=new_id("result"),
                    attempt_id=attempt.attempt_id,
                    status=AttemptResultStatus.SUCCEEDED,
                    output={"path": action.arguments["path"], "content": content},
                )

            if action.name == "write_text":
                record = self.world.write_text(
                    action.arguments["path"],
                    action.arguments["content"],
                    action.idempotency_key,
                )
                # The external side effect succeeded, but the first response is
                # deliberately lost. L3 must reconcile instead of blind retry.
                if action.arguments.get("simulate_timeout_after_commit") and self.world.mark_fault_once(
                    action.idempotency_key
                ):
                    return AttemptResult(
                        result_id=new_id("result"),
                        attempt_id=attempt.attempt_id,
                        status=AttemptResultStatus.TIMEOUT,
                        error="response lost after external commit",
                    )
                return AttemptResult(
                    result_id=new_id("result"),
                    attempt_id=attempt.attempt_id,
                    status=AttemptResultStatus.SUCCEEDED,
                    output=to_dict(record),
                )
        except (OSError, ValueError) as exc:
            return AttemptResult(
                result_id=new_id("result"),
                attempt_id=attempt.attempt_id,
                status=AttemptResultStatus.PERMANENT_ERROR,
                error=str(exc),
            )

        return AttemptResult(
            result_id=new_id("result"),
            attempt_id=attempt.attempt_id,
            status=AttemptResultStatus.PERMANENT_ERROR,
            error=f"Executor has no adapter for: {action.name}",
        )

    def reconcile(self, action: Action) -> ActionOutcome:
        record = self.world.lookup(action.idempotency_key)
        if record is not None:
            return ActionOutcome(
                outcome_id=new_id("outcome"),
                action_id=action.action_id,
                status=OutcomeStatus.SUCCEEDED,
                output=to_dict(record),
                resolution="external_state_reconciliation",
            )
        return ActionOutcome(
            outcome_id=new_id("outcome"),
            action_id=action.action_id,
            status=OutcomeStatus.FAILED,
            error="external side effect not found during reconciliation",
            resolution="external_state_reconciliation",
        )


class ObservationProjector:
    """L2 controls what raw execution data becomes visible to the harness."""

    def project(self, run_id: str, action: Action, outcome: ActionOutcome) -> Observation:
        return Observation(
            observation_id=new_id("observation"),
            run_id=run_id,
            action_id=action.action_id,
            source_outcome_id=outcome.outcome_id,
            kind=f"{action.name}_result",
            content={"status": outcome.status.value, **outcome.output},
        )


class ArtifactVerifier:
    """L2 deterministic verifier executing the L6 evaluation contract."""

    def __init__(self, world: LocalFileWorld):
        self.world = world

    def verify(self, contract_id: str, relative_path: str) -> EvaluationResult:
        exists = self.world.exists(relative_path)
        content = self.world.read_text(relative_path) if exists else ""
        checks = {
            "artifact_exists": exists,
            "has_title": content.startswith("# Agent Platform 案例报告"),
            "has_runtime_boundary": "Runtime 管事实，Harness 管策略" in content,
            "has_source_evidence": "来源摘要：" in content,
        }
        return EvaluationResult(
            contract_id=contract_id,
            passed=all(checks.values()),
            checks=checks,
            evidence=[relative_path] if exists else [],
        )
