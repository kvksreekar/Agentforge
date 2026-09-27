"""Rolling short-term memory for a single agent's conversation."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Memory:
    """A fixed-size buffer of conversation turns.

    Keeps only the most recent ``max_turns`` messages so long-running agents
    don't grow their context window without bound. ``summary`` is a hook for
    future work (see docs/ROADMAP.md) where older turns get compressed into a
    running summary instead of being dropped outright.
    """

    max_turns: int = 20
    summary: str = ""
    _turns: list[dict[str, str]] = field(default_factory=list)

    def add(self, role: str, content: str) -> None:
        self._turns.append({"role": role, "content": content})
        if len(self._turns) > self.max_turns:
            self._turns = self._turns[-self.max_turns :]

    def as_messages(self) -> list[dict[str, str]]:
        return list(self._turns)

    def clear(self) -> None:
        self._turns.clear()
        self.summary = ""

    def __len__(self) -> int:
        return len(self._turns)
