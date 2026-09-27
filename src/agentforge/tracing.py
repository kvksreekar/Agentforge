"""Structured, replayable traces of an agent's reasoning loop.

Every thought, tool call, and observation an agent produces is recorded as a
``Step``. This is the backbone of AgentForge's observability story: traces
can be rendered to the terminal, shipped to a log aggregator, or replayed in
a debugger UI (see docs/ROADMAP.md).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Step:
    kind: str  # "thought" | "action" | "observation" | "final"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Tracer:
    """Accumulates and renders the steps of a single agent run."""

    def __init__(self) -> None:
        self.steps: list[Step] = []

    def log(self, kind: str, content: str) -> None:
        self.steps.append(Step(kind=kind, content=content))

    def render(self) -> str:
        return "\n".join(f"[{s.kind.upper()}] {s.content}" for s in self.steps)

    def to_dicts(self) -> list[dict[str, str]]:
        return [{"kind": s.kind, "content": s.content, "timestamp": s.timestamp} for s in self.steps]
