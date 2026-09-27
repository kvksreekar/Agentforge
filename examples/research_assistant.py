"""Example: a single research-assistant agent.

Run with:
    python examples/research_assistant.py

Uses the real Anthropic backend if ANTHROPIC_API_KEY is set, otherwise
falls back to the offline MockBackend so the example always runs.
"""
from __future__ import annotations

import os

from agentforge.agent import Agent
from agentforge.tools.builtin import builtin_tools

if os.environ.get("ANTHROPIC_API_KEY"):
    from agentforge.llm.anthropic_backend import AnthropicBackend

    backend = AnthropicBackend()
else:
    from agentforge.llm.mock import MockBackend

    backend = MockBackend()

agent = Agent(
    name="researcher",
    llm=backend,
    tools=builtin_tools,
    persona="You are a meticulous research assistant who double-checks numbers.",
)

if __name__ == "__main__":
    answer = agent.run("What is 128 * 47, and how did you get it?")
    print("ANSWER:", answer)
    print("\nTRACE:\n", agent.tracer.render())
