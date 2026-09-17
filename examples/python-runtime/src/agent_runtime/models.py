from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class StrEnum(str, Enum):
    pass


class WorkStatus(StrEnum):
    OPEN = "open"
    COMPLETED = "completed"
    FAILED = "failed"


class RunStatus(StrEnum):
    READY = "ready"
    RUNNING = "running"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ActionStatus(StrEnum):
    REQUESTED = "requested"
    RUNNING = "running"
    OUTCOME_UNKNOWN = "outcome_unknown"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class AttemptResultStatus(StrEnum):
    SUCCEEDED = "succeeded"
    TEMPORARY_ERROR = "temporary_error"
    PERMANENT_ERROR = "permanent_error"
    TIMEOUT = "timeout"


class OutcomeStatus(StrEnum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    UNKNOWN = "unknown"


# L7: business/product owns the business request and its final acceptance state.
@dataclass(slots=True)
class BusinessTask:
    task_id: str
    goal: str
    source_path: str
    output_path: str
    status: str = "submitted"
    accepted_artifact_id: str | None = None


# L6: a stable definition of what successful capability execution means.
@dataclass(slots=True)
class CapabilityContract:
    contract_id: str
    capability_name: str
    input_schema: dict[str, str]
    acceptance_criteria: list[str]
    quality_criteria: list[str]
    evidence_requirements: list[str]


@dataclass(slots=True)
class EvaluationResult:
    contract_id: str
    passed: bool
    checks: dict[str, bool]
    evidence: list[str]


# L5: discoverable, versioned capability metadata. It does not own execution state.
@dataclass(slots=True)
class ToolSpec:
    name: str
    description: str
    risk_level: str
    side_effect: bool


@dataclass(slots=True)
class CapabilityDefinition:
    capability_id: str
    name: str
    revision: str
    contract_id: str
    skill_revision: str
    allowed_tools: list[ToolSpec]


# L1: the external world's resource identity and side-effect evidence.
@dataclass(slots=True)
class ResourceRecord:
    uri: str
    sha256: str
    size_bytes: int
    idempotency_key: str


# L3: durable execution facts and lifecycle entities.
@dataclass(slots=True)
class Work:
    work_id: str
    goal: str
    business_task_id: str
    contract_id: str
    capability_id: str
    status: WorkStatus = WorkStatus.OPEN
    artifact_ids: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Session:
    session_id: str
    work_id: str
    agent_identity: str
    harness_revision: str
    model_config: dict[str, Any]


@dataclass(slots=True)
class Run:
    run_id: str
    work_id: str
    session_id: str
    trigger: dict[str, Any]
    status: RunStatus = RunStatus.READY
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass(slots=True)
class Action:
    action_id: str
    run_id: str
    capability_id: str
    name: str
    arguments: dict[str, Any]
    idempotency_key: str
    status: ActionStatus = ActionStatus.REQUESTED
    attempt_ids: list[str] = field(default_factory=list)
    outcome_id: str | None = None


@dataclass(slots=True)
class ExecutionAttempt:
    attempt_id: str
    action_id: str
    executor: str
    ordinal: int
    result_id: str | None = None


@dataclass(slots=True)
class AttemptResult:
    result_id: str
    attempt_id: str
    status: AttemptResultStatus
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass(slots=True)
class ActionOutcome:
    outcome_id: str
    action_id: str
    status: OutcomeStatus
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    resolution: str = "attempt_result"


@dataclass(slots=True)
class Observation:
    observation_id: str
    run_id: str
    action_id: str
    source_outcome_id: str
    kind: str
    content: dict[str, Any]


@dataclass(slots=True)
class Artifact:
    artifact_id: str
    work_id: str
    run_id: str
    kind: str
    uri: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Event:
    event_id: str
    event_type: str
    schema_version: str
    work_id: str
    session_id: str
    run_id: str
    sequence: int
    timestamp: str
    actor: str
    causation_id: str | None
    correlation_id: str
    payload: dict[str, Any]


@dataclass(slots=True)
class StateView:
    run_id: str
    run_status: str
    action_statuses: dict[str, str]
    latest_observation_ids: list[str]
    event_sequence: int


@dataclass(slots=True)
class ExecutionCheckpoint:
    run_id: str
    cursor: str
    harness_state: dict[str, Any]
    waiting_for: dict[str, Any] | None
    pending_action_ids: list[str]
    updated_at: str


# L4/L3 stable control boundary.
@dataclass(slots=True)
class RuntimeSnapshot:
    work: Work
    session: Session
    run: Run
    state_view: StateView
    checkpoint: ExecutionCheckpoint
    observations: list[Observation]


@dataclass(slots=True)
class ExecuteDecision:
    action_name: str
    arguments: dict[str, Any]
    next_harness_state: dict[str, Any]


@dataclass(slots=True)
class WaitDecision:
    condition: dict[str, Any]
    next_harness_state: dict[str, Any]


@dataclass(slots=True)
class CompleteDecision:
    output: dict[str, Any]
    artifact_kind: str
    artifact_uri: str


@dataclass(slots=True)
class FailDecision:
    reason: str


Decision = ExecuteDecision | WaitDecision | CompleteDecision | FailDecision


def to_dict(value: Any) -> Any:
    """Convert nested dataclasses/enums to JSON-compatible data."""
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "__dataclass_fields__"):
        return {key: to_dict(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {key: to_dict(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_dict(item) for item in value]
    return value
