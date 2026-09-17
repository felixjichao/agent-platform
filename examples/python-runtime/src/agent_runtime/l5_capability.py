from __future__ import annotations

from .models import CapabilityDefinition


class CapabilityRegistry:
    """L5 capability discovery and version resolution."""

    def __init__(self, capabilities: list[CapabilityDefinition]):
        self._by_name = {capability.name: capability for capability in capabilities}

    def resolve(self, name: str) -> CapabilityDefinition:
        try:
            return self._by_name[name]
        except KeyError as exc:
            raise LookupError(f"Capability not found: {name}") from exc

