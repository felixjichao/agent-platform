from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from typing import Any, TypeVar

from .models import (
    Action,
    ActionOutcome,
    ActionStatus,
    Artifact,
    AttemptResult,
    AttemptResultStatus,
    Event,
    ExecutionAttempt,
    ExecutionCheckpoint,
    Observation,
    OutcomeStatus,
    Run,
    RunStatus,
    Session,
    StateView,
    Work,
    WorkStatus,
    to_dict,
)

T = TypeVar("T")


class RuntimeStore:
    """SQLite implementation of the L3 persistence boundary.

    Domain state, event, state view and checkpoint writes share one database
    transaction. The generic entity table keeps the example compact without
    changing the domain boundaries.
    """

    def __init__(self, database_path: str | Path):
        self.database_path = str(database_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS entities (
                    kind TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    data TEXT NOT NULL,
                    PRIMARY KEY (kind, entity_id)
                );
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    sequence INTEGER NOT NULL,
                    data TEXT NOT NULL,
                    UNIQUE (run_id, sequence)
                );
                CREATE TABLE IF NOT EXISTS state_views (
                    run_id TEXT PRIMARY KEY,
                    data TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS checkpoints (
                    run_id TEXT PRIMARY KEY,
                    data TEXT NOT NULL
                );
                """
            )

    @contextmanager
    def transaction(self):
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def commit_transition(
        self,
        *,
        entities: Iterable[Any] = (),
        event: Event | None = None,
        state_view: StateView | None = None,
        checkpoint: ExecutionCheckpoint | None = None,
    ) -> Event | None:
        with self.transaction() as connection:
            for entity in entities:
                kind, entity_id = self._entity_identity(entity)
                connection.execute(
                    """
                    INSERT INTO entities(kind, entity_id, data) VALUES (?, ?, ?)
                    ON CONFLICT(kind, entity_id) DO UPDATE SET data=excluded.data
                    """,
                    (kind, entity_id, json.dumps(to_dict(entity), ensure_ascii=False)),
                )

            committed_event = event
            if event is not None:
                row = connection.execute(
                    "SELECT COALESCE(MAX(sequence), 0) + 1 AS sequence FROM events WHERE run_id=?",
                    (event.run_id,),
                ).fetchone()
                committed_event = replace(event, sequence=int(row["sequence"]))
                connection.execute(
                    "INSERT INTO events(event_id, run_id, sequence, data) VALUES (?, ?, ?, ?)",
                    (
                        committed_event.event_id,
                        committed_event.run_id,
                        committed_event.sequence,
                        json.dumps(to_dict(committed_event), ensure_ascii=False),
                    ),
                )

            if state_view is not None:
                view = state_view
                if committed_event is not None:
                    view = replace(state_view, event_sequence=committed_event.sequence)
                connection.execute(
                    """
                    INSERT INTO state_views(run_id, data) VALUES (?, ?)
                    ON CONFLICT(run_id) DO UPDATE SET data=excluded.data
                    """,
                    (view.run_id, json.dumps(to_dict(view), ensure_ascii=False)),
                )

            if checkpoint is not None:
                connection.execute(
                    """
                    INSERT INTO checkpoints(run_id, data) VALUES (?, ?)
                    ON CONFLICT(run_id) DO UPDATE SET data=excluded.data
                    """,
                    (checkpoint.run_id, json.dumps(to_dict(checkpoint), ensure_ascii=False)),
                )
        return committed_event

    def get(self, kind: str, entity_id: str) -> Any:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT data FROM entities WHERE kind=? AND entity_id=?",
                (kind, entity_id),
            ).fetchone()
        if row is None:
            raise KeyError(f"{kind}:{entity_id}")
        return self._decode(kind, json.loads(row["data"]))

    def list_entities(self, kind: str, *, field_name: str | None = None, value: str | None = None) -> list[Any]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT data FROM entities WHERE kind=? ORDER BY rowid",
                (kind,),
            ).fetchall()
        entities = [self._decode(kind, json.loads(row["data"])) for row in rows]
        if field_name is not None:
            entities = [entity for entity in entities if getattr(entity, field_name) == value]
        return entities

    def get_checkpoint(self, run_id: str) -> ExecutionCheckpoint:
        with self._connect() as connection:
            row = connection.execute("SELECT data FROM checkpoints WHERE run_id=?", (run_id,)).fetchone()
        if row is None:
            raise KeyError(f"checkpoint:{run_id}")
        return ExecutionCheckpoint(**json.loads(row["data"]))

    def get_state_view(self, run_id: str) -> StateView:
        with self._connect() as connection:
            row = connection.execute("SELECT data FROM state_views WHERE run_id=?", (run_id,)).fetchone()
        if row is None:
            raise KeyError(f"state_view:{run_id}")
        return StateView(**json.loads(row["data"]))

    def get_events(self, run_id: str) -> list[Event]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT data FROM events WHERE run_id=? ORDER BY sequence",
                (run_id,),
            ).fetchall()
        return [Event(**json.loads(row["data"])) for row in rows]

    @staticmethod
    def _entity_identity(entity: Any) -> tuple[str, str]:
        mapping = {
            Work: ("work", "work_id"),
            Session: ("session", "session_id"),
            Run: ("run", "run_id"),
            Action: ("action", "action_id"),
            ExecutionAttempt: ("attempt", "attempt_id"),
            AttemptResult: ("attempt_result", "result_id"),
            ActionOutcome: ("outcome", "outcome_id"),
            Observation: ("observation", "observation_id"),
            Artifact: ("artifact", "artifact_id"),
        }
        for model, identity in mapping.items():
            if isinstance(entity, model):
                kind, field_name = identity
                return kind, getattr(entity, field_name)
        raise TypeError(f"Unsupported entity: {type(entity).__name__}")

    @staticmethod
    def _decode(kind: str, data: dict[str, Any]) -> Any:
        if kind == "work":
            data["status"] = WorkStatus(data["status"])
            return Work(**data)
        if kind == "session":
            return Session(**data)
        if kind == "run":
            data["status"] = RunStatus(data["status"])
            return Run(**data)
        if kind == "action":
            data["status"] = ActionStatus(data["status"])
            return Action(**data)
        if kind == "attempt":
            return ExecutionAttempt(**data)
        if kind == "attempt_result":
            data["status"] = AttemptResultStatus(data["status"])
            return AttemptResult(**data)
        if kind == "outcome":
            data["status"] = OutcomeStatus(data["status"])
            return ActionOutcome(**data)
        if kind == "observation":
            return Observation(**data)
        if kind == "artifact":
            return Artifact(**data)
        raise KeyError(kind)
