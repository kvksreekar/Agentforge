"""Example: a two-agent pipeline (reviewer -> fixer) via the Orchestrator.

Run with:
    python examples/code_reviewer.py
"""
from __future__ import annotations

from agentforge.agent import Agent
from agentforge.llm.mock import MockBackend
from agentforge.orchestrator import Orchestrator
from agentforge.tools.builtin import builtin_tools

orchestrator = Orchestrator()
orchestrator.register(
    Agent(
        name="reviewer",
        llm=MockBackend(),
        tools=builtin_tools,
        persona="You review code for bugs, style, and missing edge cases.",
    )
)
orchestrator.register(
    Agent(
        name="fixer",
        llm=MockBackend(),
        tools=builtin_tools,
        persona="You rewrite code to address reviewer feedback.",
    )
)

if __name__ == "__main__":
    snippet = "def add(a, b):\n    return a+b"
    result = orchestrator.pipeline(f"Review this code:\n{snippet}", order=["reviewer", "fixer"])
    print(result)
