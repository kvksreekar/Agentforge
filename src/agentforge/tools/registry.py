"""Tool registration and lookup for agents."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Tool:
    """A single callable capability an agent can invoke."""

    name: str
    description: str
    func: Callable[..., Any]
    parameters: dict[str, Any] = field(default_factory=dict)

    def __call__(self, **kwargs: Any) -> Any:
        return self.func(**kwargs)


class ToolRegistry:
    """A named collection of tools, injectable into any agent."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(
        self,
        name: str,
        description: str,
        parameters: dict[str, Any] | None = None,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator that adds a function to the registry as a named tool."""

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self._tools[name] = Tool(name=name, description=description, func=func, parameters=parameters or {})
            return func

        return decorator

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name!r}. Available: {sorted(self._tools)}")
        return self._tools[name]

    def list(self) -> list[Tool]:
        return list(self._tools.values())

    def specs(self) -> list[dict[str, Any]]:
        """Machine-readable tool specs, useful for presenting to an LLM."""
        return [
            {"name": t.name, "description": t.description, "parameters": t.parameters}
            for t in self._tools.values()
        ]
