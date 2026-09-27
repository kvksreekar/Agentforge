"""A deterministic, offline LLM backend.

Useful for demos, CI, and unit tests that shouldn't depend on network access
or an API key. It implements a tiny slice of ReAct-style behavior: it will
reach for the calculator tool on arithmetic-looking prompts and otherwise
answer directly.
"""
from __future__ import annotations

from .base import LLMBackend, LLMResponse


class MockBackend(LLMBackend):
    """Deterministic backend requiring no API key or network access."""

    def complete(
        self,
        system: str,
        messages: list[dict[str, str]],
        max_tokens: int = 1024,
    ) -> LLMResponse:
        last = messages[-1]["content"] if messages else ""

        if "Observation:" in last:
            observation = last.split("Observation:", 1)[1].strip()
            return LLMResponse(
                content=(
                    "Thought: I now have the information I need.\n"
                    f"Final Answer: {observation}"
                )
            )

        if any(op in last for op in ("calculate", "+", "-", "*", "/")) and any(c.isdigit() for c in last):
            return LLMResponse(
                content=(
                    "Thought: This looks like a calculation, I'll use the calculator tool.\n"
                    'Action: calculator\nAction Input: {"expression": "2 + 2"}'
                )
            )

        return LLMResponse(content=f"Thought: I can answer directly.\nFinal Answer: (mock) You asked: {last}")
