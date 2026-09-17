from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

from .l1_world import LocalFileWorld
from .l2_environment import ArtifactVerifier, LocalActionExecutor, ObservationProjector
from .l3_runtime import ActionCoordinator, RuntimeEngine
from .l4_harness import ReportHarness
from .l5_capability import CapabilityRegistry
from .models import (
    Action,
    ActionOutcome,
    Artifact,
    AttemptResult,
    BusinessTask,
    CapabilityContract,
    CapabilityDefinition,
    EvaluationResult,
    Event,
    ExecutionAttempt,
    ExecutionCheckpoint,
    Run,
    Session,
    StateView,
    ToolSpec,
    Work,
    new_id,
    to_dict,
)
from .persistence import RuntimeStore


@dataclass(slots=True)
class CaseResult:
    business_task: BusinessTask
    capability_contract: CapabilityContract
    capability: CapabilityDefinition
    work: Work
    session: Session
    run: Run
    actions: list[Action]
    attempts: list[ExecutionAttempt]
    attempt_results: list[AttemptResult]
    outcomes: list[ActionOutcome]
    artifact: Artifact
    evaluation: EvaluationResult
    events: list[Event]
    state_view: StateView
    checkpoint: ExecutionCheckpoint
    simulated_restart: bool

    def as_dict(self) -> dict:
        return to_dict(self)


class AgentPlatformApplication:
    """L7-to-L1 application composition root for the runnable case."""

    capability_name = "generate_architecture_report"

    def __init__(self, case_root: str | Path):
        self.case_root = Path(case_root).resolve()
        self.case_root.mkdir(parents=True, exist_ok=True)
        self.world = LocalFileWorld(self.case_root / "workspace")
        self.database_path = self.case_root / "runtime.db"

        self.contract = CapabilityContract(
            contract_id="contract.generate-architecture-report.v1",
            capability_name=self.capability_name,
            input_schema={"source_path": "workspace-relative path", "output_path": "workspace-relative path"},
            acceptance_criteria=[
                "report artifact exists",
                "report contains the Runtime/Harness boundary",
            ],
            quality_criteria=["report contains source evidence", "report is valid Markdown"],
            evidence_requirements=["artifact path", "deterministic verification checks", "runtime event trace"],
        )
        self.capability = CapabilityDefinition(
            capability_id="capability.generate-architecture-report.v1",
            name=self.capability_name,
            revision="1.0.0",
            contract_id=self.contract.contract_id,
            skill_revision="architecture-report-skill@1",
            allowed_tools=[
                ToolSpec("read_text", "Read one workspace text file", "low", False),
                ToolSpec("write_text", "Write one workspace text file", "medium", True),
            ],
        )
        self.registry = CapabilityRegistry([self.capability])

    def seed_source(self, content: str) -> None:
        source = self.world.root / "input" / "architecture.md"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(content, encoding="utf-8")

    def run_case(self, *, simulate_restart: bool = True) -> CaseResult:
        task = BusinessTask(
            task_id=new_id("business_task"),
            goal="读取架构说明并生成可验收的 Agent Platform 案例报告",
            source_path="input/architecture.md",
            output_path="output/report.md",
        )
        capability = self.registry.resolve(self.capability_name)
        store, engine = self._build_runtime(capability)
        run = engine.create_run(task, capability)

        if simulate_restart:
            engine.start(run.run_id, max_actions=1)
            # Recreate every process-local component. Only SQLite, the execution
            # checkpoint and the L1 workspace survive this boundary.
            store, engine = self._build_runtime(capability)
            run = engine.recover(run.run_id)
        else:
            run = engine.start(run.run_id)

        session = store.get("session", run.session_id)
        artifacts = store.list_entities("artifact", field_name="run_id", value=run.run_id)
        artifact = artifacts[-1]
        evaluation = ArtifactVerifier(self.world).verify(self.contract.contract_id, artifact.uri)
        work = engine.record_work_acceptance(
            run.run_id,
            passed=evaluation.passed,
            evidence=evaluation.evidence,
        )
        task = replace(
            task,
            status="accepted" if evaluation.passed else "rejected",
            accepted_artifact_id=artifact.artifact_id if evaluation.passed else None,
        )

        return CaseResult(
            business_task=task,
            capability_contract=self.contract,
            capability=capability,
            work=work,
            session=session,
            run=run,
            actions=store.list_entities("action", field_name="run_id", value=run.run_id),
            attempts=self._attempts_for_run(store, run.run_id),
            attempt_results=self._results_for_run(store, run.run_id),
            outcomes=self._outcomes_for_run(store, run.run_id),
            artifact=artifact,
            evaluation=evaluation,
            events=store.get_events(run.run_id),
            state_view=store.get_state_view(run.run_id),
            checkpoint=store.get_checkpoint(run.run_id),
            simulated_restart=simulate_restart,
        )

    def _build_runtime(self, capability: CapabilityDefinition) -> tuple[RuntimeStore, RuntimeEngine]:
        store = RuntimeStore(self.database_path)
        executor = LocalActionExecutor(self.world, capability)
        coordinator = ActionCoordinator(store, executor, ObservationProjector())
        engine = RuntimeEngine(store, ReportHarness(), coordinator)
        return store, engine

    @staticmethod
    def _attempts_for_run(store: RuntimeStore, run_id: str) -> list[ExecutionAttempt]:
        action_ids = {action.action_id for action in store.list_entities("action", field_name="run_id", value=run_id)}
        return [attempt for attempt in store.list_entities("attempt") if attempt.action_id in action_ids]

    @classmethod
    def _results_for_run(cls, store: RuntimeStore, run_id: str) -> list[AttemptResult]:
        attempt_ids = {attempt.attempt_id for attempt in cls._attempts_for_run(store, run_id)}
        return [result for result in store.list_entities("attempt_result") if result.attempt_id in attempt_ids]

    @staticmethod
    def _outcomes_for_run(store: RuntimeStore, run_id: str) -> list[ActionOutcome]:
        action_ids = {action.action_id for action in store.list_entities("action", field_name="run_id", value=run_id)}
        return [outcome for outcome in store.list_entities("outcome") if outcome.action_id in action_ids]
