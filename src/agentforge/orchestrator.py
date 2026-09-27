"""Coordinates multiple specialist agents.

Two patterns are supported out of the box:

- ``delegate``: hand one task to one named agent.
- ``pipeline``: run agents in sequence, piping each agent's output into the
  next agent's task (e.g. a "reviewer" agent's critique feeds a "fixer"
  agent). Fan-out/fan-in and voting policies are natural extensions — see
  docs/ROADMAP.md.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .agent import Agent


@dataclass
class Orchestrator:
    """A lightweight supervisor over a set of named agents."""

    agents: dict[str, Agent] = field(default_factory=dict)

    def register(self, agent: Agent) -> None:
        self.agents[agent.name] = agent

    def delegate(self, agent_name: str, task: str) -> str:
        if agent_name not in self.agents:
            raise KeyError(f"No such agent: {agent_name!r}. Registered: {sorted(self.agents)}")
        return self.agents[agent_name].run(task)

    def pipeline(self, task: str, order: list[str]) -> str:
        """Run agents sequentially, feeding each output as the next input."""
        current = task
        for name in order:
            current = self.delegate(name, current)
        return current
