from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from .l2_environment import LocalActionExecutor, ObservationProjector
from .l4_harness import ReportHarness
from .models import (
    Action,
    ActionOutcome,
    ActionStatus,
    Artifact,
    AttemptResultStatus,
    BusinessTask,
    CapabilityDefinition,
    CompleteDecision,
    ExecuteDecision,
    ExecutionAttempt,
    ExecutionCheckpoint,
    FailDecision,
    OutcomeStatus,
    Run,
    RunStatus,
    RuntimeSnapshot,
    Session,
    StateView,
    WaitDecision,
    Work,
    WorkStatus,
    Event,
    new_id,
)
from .persistence import RuntimeStore


def now() -> str:
    return datetime.now(UTC).isoformat()


class ActionCoordinator:
    """L3 action/attempt/outcome reliability semantics."""

    def __init__(
        self,
        store: RuntimeStore,
        executor: LocalActionExecutor,
        observation_projector: ObservationProjector,
    ):
        self.store = store
        self.executor = executor
        self.observation_projector = observation_projector

    def execute(
        self,
        snapshot: RuntimeSnapshot,
        capability_id: str,
        decision: ExecuteDecision,
    ) -> ActionOutcome:
        action = Action(
            action_id=new_id("action"),
            run_id=snapshot.run.run_id,
            capability_id=capability_id,
            name=decision.action_name,
            arguments=decision.arguments,
            idempotency_key=f"{snapshot.run.run_id}:{snapshot.checkpoint.cursor}:{decision.action_name}",
        )
        pending_checkpoint = replace(
            snapshot.checkpoint,
            pending_action_ids=[*snapshot.checkpoint.pending_action_ids, action.action_id],
            updated_at=now(),
        )
        requested_view = self._view(snapshot, action.action_id, ActionStatus.REQUESTED)
        self.store.commit_transition(
            entities=[action],
            event=self._event(snapshot, "ActionRequested", "runtime", {"action_id": action.action_id, "name": action.name}),
            state_view=requested_view,
            checkpoint=pending_checkpoint,
        )

        attempt = ExecutionAttempt(
            attempt_id=new_id("attempt"),
            action_id=action.action_id,
            executor=self.executor.name,
            ordinal=1,
        )
        action = replace(action, status=ActionStatus.RUNNING, attempt_ids=[attempt.attempt_id])
        running_view = self._view(snapshot, action.action_id, ActionStatus.RUNNING)
        self.store.commit_transition(
            entities=[action, attempt],
            event=self._event(
                snapshot,
                "ActionAttemptStarted",
                self.executor.name,
                {"action_id": action.action_id, "attempt_id": attempt.attempt_id, "ordinal": 1},
            ),
            state_view=running_view,
            checkpoint=pending_checkpoint,
        )

        result = self.executor.execute(action, attempt)
        attempt = replace(attempt, result_id=result.result_id)

        if result.status == AttemptResultStatus.SUCCEEDED:
            outcome = ActionOutcome(
                outcome_id=new_id("outcome"),
                action_id=action.action_id,
                status=OutcomeStatus.SUCCEEDED,
                output=result.output,
            )
            return self._finalize(snapshot, decision, action, attempt, result, outcome, "ActionSucceeded")

        if result.status == AttemptResultStatus.TIMEOUT:
            unknown = ActionOutcome(
                outcome_id=new_id("outcome"),
                action_id=action.action_id,
                status=OutcomeStatus.UNKNOWN,
                error=result.error,
                resolution="attempt_timeout",
            )
            action = replace(action, status=ActionStatus.OUTCOME_UNKNOWN, outcome_id=unknown.outcome_id)
            unknown_view = self._view(snapshot, action.action_id, ActionStatus.OUTCOME_UNKNOWN)
            self.store.commit_transition(
                entities=[action, attempt, result, unknown],
                event=self._event(
                    snapshot,
                    "ActionOutcomeUnknown",
                    self.executor.name,
                    {"action_id": action.action_id, "attempt_id": attempt.attempt_id, "reason": result.error},
                ),
                state_view=unknown_view,
                checkpoint=pending_checkpoint,
            )
            reconciled = self.executor.reconcile(action)
            reconciled = replace(reconciled, outcome_id=unknown.outcome_id)
            return self._finalize(
                snapshot,
                decision,
                action,
                attempt,
                result,
                reconciled,
                "ActionReconciled",
            )

        failed = ActionOutcome(
            outcome_id=new_id("outcome"),
            action_id=action.action_id,
            status=OutcomeStatus.FAILED,
            error=result.error,
        )
        return self._finalize(snapshot, decision, action, attempt, result, failed, "ActionFailed")

    def _finalize(
        self,
        snapshot: RuntimeSnapshot,
        decision: ExecuteDecision,
        action: Action,
        attempt: ExecutionAttempt,
        result,
        outcome: ActionOutcome,
        event_type: str,
    ) -> ActionOutcome:
        succeeded = outcome.status == OutcomeStatus.SUCCEEDED
        action = replace(
            action,
            status=ActionStatus.SUCCEEDED if succeeded else ActionStatus.FAILED,
            outcome_id=outcome.outcome_id,
        )
        observation = self.observation_projector.project(snapshot.run.run_id, action, outcome)
        next_state = decision.next_harness_state if succeeded else snapshot.checkpoint.harness_state
        checkpoint = replace(
            snapshot.checkpoint,
            cursor=next_state["step"],
            harness_state=next_state,
            pending_action_ids=[],
            updated_at=now(),
        )
        view = self._view(
            snapshot,
            action.action_id,
            action.status,
            observation.observation_id,
        )
        self.store.commit_transition(
            entities=[action, attempt, result, outcome, observation],
            event=self._event(
                snapshot,
                event_type,
                "runtime",
                {
                    "action_id": action.action_id,
                    "attempt_id": attempt.attempt_id,
                    "outcome_id": outcome.outcome_id,
                    "resolution": outcome.resolution,
                },
            ),
            state_view=view,
            checkpoint=checkpoint,
        )
        return outcome

    @staticmethod
    def _view(
        snapshot: RuntimeSnapshot,
        action_id: str,
        status: ActionStatus,
        observation_id: str | None = None,
    ) -> StateView:
        statuses = dict(snapshot.state_view.action_statuses)
        statuses[action_id] = status.value
        observation_ids = list(snapshot.state_view.latest_observation_ids)
        if observation_id is not None:
            observation_ids.append(observation_id)
        return replace(
            snapshot.state_view,
            action_statuses=statuses,
            latest_observation_ids=observation_ids,
        )

    @staticmethod
    def _event(snapshot: RuntimeSnapshot, event_type: str, actor: str, payload: dict) -> Event:
        return Event(
            event_id=new_id("event"),
            event_type=event_type,
            schema_version="1.0",
            work_id=snapshot.work.work_id,
            session_id=snapshot.session.session_id,
            run_id=snapshot.run.run_id,
            sequence=0,
            timestamp=now(),
            actor=actor,
            causation_id=None,
            correlation_id=snapshot.run.run_id,
            payload=payload,
        )


class RuntimeEngine:
    """L3 single writer for Run lifecycle."""

    def __init__(
        self,
        store: RuntimeStore,
        harness: ReportHarness,
        coordinator: ActionCoordinator,
    ):
        self.store = store
        self.harness = harness
        self.coordinator = coordinator

    def create_run(
        self,
        task: BusinessTask,
        capability: CapabilityDefinition,
    ) -> Run:
        work = Work(
            work_id=new_id("work"),
            goal=task.goal,
            business_task_id=task.task_id,
            contract_id=capability.contract_id,
            capability_id=capability.capability_id,
        )
        session = Session(
            session_id=new_id("session"),
            work_id=work.work_id,
            agent_identity="demo-report-agent",
            harness_revision=self.harness.revision,
            model_config={"provider": "deterministic-demo", "model": "none"},
        )
        run = Run(
            run_id=new_id("run"),
            work_id=work.work_id,
            session_id=session.session_id,
            trigger={"type": "BusinessTaskSubmitted", "task_id": task.task_id},
        )
        checkpoint = ExecutionCheckpoint(
            run_id=run.run_id,
            cursor="read_source",
            harness_state={
                "step": "read_source",
                "source_path": task.source_path,
                "output_path": task.output_path,
            },
            waiting_for=None,
            pending_action_ids=[],
            updated_at=now(),
        )
        view = StateView(
            run_id=run.run_id,
            run_status=run.status.value,
            action_statuses={},
            latest_observation_ids=[],
            event_sequence=0,
        )
        snapshot = RuntimeSnapshot(work, session, run, view, checkpoint, [])
        self.store.commit_transition(
            entities=[work, session, run],
            event=self._event(snapshot, "RunCreated", "application", {"trigger": run.trigger}),
            state_view=view,
            checkpoint=checkpoint,
        )
        return run

    def start(self, run_id: str, *, max_actions: int | None = None) -> Run:
        snapshot = self.snapshot(run_id)
        run = replace(snapshot.run, status=RunStatus.RUNNING)
        view = replace(snapshot.state_view, run_status=run.status.value)
        self.store.commit_transition(
            entities=[run],
            event=self._event(snapshot, "RunStarted", "runtime", {}),
            state_view=view,
            checkpoint=snapshot.checkpoint,
        )
        return self._drive(run_id, max_actions=max_actions)

    def recover(self, run_id: str) -> Run:
        snapshot = self.snapshot(run_id)
        self.store.commit_transition(
            event=self._event(
                snapshot,
                "RecoveryStarted",
                "runtime",
                {"cursor": snapshot.checkpoint.cursor},
            ),
            state_view=snapshot.state_view,
            checkpoint=snapshot.checkpoint,
        )
        snapshot = self.snapshot(run_id)
        self.store.commit_transition(
            event=self._event(snapshot, "RecoveryCompleted", "runtime", {"cursor": snapshot.checkpoint.cursor}),
            state_view=snapshot.state_view,
            checkpoint=snapshot.checkpoint,
        )
        return self._drive(run_id)

    def snapshot(self, run_id: str) -> RuntimeSnapshot:
        run = self.store.get("run", run_id)
        work = self.store.get("work", run.work_id)
        session = self.store.get("session", run.session_id)
        observations = self.store.list_entities("observation", field_name="run_id", value=run_id)
        return RuntimeSnapshot(
            work=work,
            session=session,
            run=run,
            state_view=self.store.get_state_view(run_id),
            checkpoint=self.store.get_checkpoint(run_id),
            observations=observations,
        )

    def record_work_acceptance(self, run_id: str, *, passed: bool, evidence: list[str]) -> Work:
        """Apply the L6/L7 acceptance decision without conflating it with Run completion."""
        snapshot = self.snapshot(run_id)
        work = replace(snapshot.work, status=WorkStatus.COMPLETED if passed else WorkStatus.OPEN)
        self.store.commit_transition(
            entities=[work],
            event=self._event(
                snapshot,
                "WorkCompleted" if passed else "WorkAcceptanceRejected",
                "application",
                {"passed": passed, "evidence": evidence},
            ),
            state_view=snapshot.state_view,
            checkpoint=snapshot.checkpoint,
        )
        return work

    def _drive(self, run_id: str, *, max_actions: int | None = None) -> Run:
        actions_executed = 0
        while True:
            snapshot = self.snapshot(run_id)
            decision = self.harness.next(snapshot)

            if isinstance(decision, ExecuteDecision):
                outcome = self.coordinator.execute(snapshot, snapshot.work.capability_id, decision)
                actions_executed += 1
                if outcome.status != OutcomeStatus.SUCCEEDED:
                    return self._fail(self.snapshot(run_id), outcome.error or "action failed")
                if max_actions is not None and actions_executed >= max_actions:
                    return self.store.get("run", run_id)
                continue

            if isinstance(decision, CompleteDecision):
                return self._complete(snapshot, decision)

            if isinstance(decision, WaitDecision):
                run = replace(snapshot.run, status=RunStatus.SUSPENDED)
                checkpoint = replace(
                    snapshot.checkpoint,
                    waiting_for=decision.condition,
                    harness_state=decision.next_harness_state,
                    updated_at=now(),
                )
                view = replace(snapshot.state_view, run_status=run.status.value)
                self.store.commit_transition(
                    entities=[run],
                    event=self._event(snapshot, "RunSuspended", "harness", {"condition": decision.condition}),
                    state_view=view,
                    checkpoint=checkpoint,
                )
                return run

            if isinstance(decision, FailDecision):
                return self._fail(snapshot, decision.reason)

            raise TypeError(type(decision).__name__)

    def _complete(self, snapshot: RuntimeSnapshot, decision: CompleteDecision) -> Run:
        artifact = Artifact(
            artifact_id=new_id("artifact"),
            work_id=snapshot.work.work_id,
            run_id=snapshot.run.run_id,
            kind=decision.artifact_kind,
            uri=decision.artifact_uri,
            metadata={"created_by": snapshot.session.agent_identity},
        )
        work = replace(snapshot.work, artifact_ids=[*snapshot.work.artifact_ids, artifact.artifact_id])
        run = replace(snapshot.run, status=RunStatus.COMPLETED, output=decision.output)
        checkpoint = replace(
            snapshot.checkpoint,
            cursor="terminal",
            harness_state={**snapshot.checkpoint.harness_state, "step": "terminal"},
            updated_at=now(),
        )
        view = replace(snapshot.state_view, run_status=run.status.value)
        self.store.commit_transition(
            entities=[artifact, work, run],
            event=self._event(
                snapshot,
                "RunCompleted",
                "harness",
                {"artifact_id": artifact.artifact_id, "output": decision.output},
            ),
            state_view=view,
            checkpoint=checkpoint,
        )
        return run

    def _fail(self, snapshot: RuntimeSnapshot, reason: str) -> Run:
        work = replace(snapshot.work, status=WorkStatus.FAILED)
        run = replace(snapshot.run, status=RunStatus.FAILED, error=reason)
        view = replace(snapshot.state_view, run_status=run.status.value)
        self.store.commit_transition(
            entities=[work, run],
            event=self._event(snapshot, "RunFailed", "runtime", {"reason": reason}),
            state_view=view,
            checkpoint=snapshot.checkpoint,
        )
        return run

    @staticmethod
    def _event(snapshot: RuntimeSnapshot, event_type: str, actor: str, payload: dict) -> Event:
        return Event(
            event_id=new_id("event"),
            event_type=event_type,
            schema_version="1.0",
            work_id=snapshot.work.work_id,
            session_id=snapshot.session.session_id,
            run_id=snapshot.run.run_id,
            sequence=0,
            timestamp=now(),
            actor=actor,
            causation_id=None,
            correlation_id=snapshot.run.run_id,
            payload=payload,
        )
