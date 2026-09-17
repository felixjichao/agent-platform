from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from .models import ResourceRecord, to_dict


class LocalFileWorld:
    """L1 adapter for the demo's real file resources.

    All paths are relative to one explicit root. Idempotency records model an
    external system that can answer whether a side effect already happened.
    """

    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.ledger = self.root / ".idempotency"
        self.ledger.mkdir(exist_ok=True)

    def read_text(self, relative_path: str) -> str:
        return self._resolve(relative_path).read_text(encoding="utf-8")

    def write_text(self, relative_path: str, content: str, idempotency_key: str) -> ResourceRecord:
        previous = self.lookup(idempotency_key)
        if previous is not None:
            return previous

        target = self._resolve(relative_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + ".tmp")
        temporary.write_text(content, encoding="utf-8")
        os.replace(temporary, target)

        record = ResourceRecord(
            uri=relative_path,
            sha256=hashlib.sha256(content.encode("utf-8")).hexdigest(),
            size_bytes=len(content.encode("utf-8")),
            idempotency_key=idempotency_key,
        )
        self._ledger_path(idempotency_key).write_text(
            json.dumps(to_dict(record), ensure_ascii=False), encoding="utf-8"
        )
        return record

    def lookup(self, idempotency_key: str) -> ResourceRecord | None:
        ledger_path = self._ledger_path(idempotency_key)
        if not ledger_path.exists():
            return None
        record = ResourceRecord(**json.loads(ledger_path.read_text(encoding="utf-8")))
        target = self._resolve(record.uri)
        if not target.exists():
            return None
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        return record if actual == record.sha256 else None

    def mark_fault_once(self, key: str) -> bool:
        marker = self.ledger / f"fault-{hashlib.sha256(key.encode()).hexdigest()}.marker"
        if marker.exists():
            return False
        marker.write_text("injected", encoding="utf-8")
        return True

    def exists(self, relative_path: str) -> bool:
        return self._resolve(relative_path).exists()

    def _ledger_path(self, key: str) -> Path:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        return self.ledger / f"{digest}.json"

    def _resolve(self, relative_path: str) -> Path:
        candidate = (self.root / relative_path).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise ValueError(f"Path escapes workspace: {relative_path}")
        return candidate
