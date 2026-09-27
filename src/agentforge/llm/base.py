"""Abstract interface every LLM backend must implement.

AgentForge is backend-agnostic: agents only ever talk to an ``LLMBackend``,
never to a specific provider's SDK. This makes it trivial to swap Anthropic,
OpenAI, a local model, or a deterministic mock in and out of an agent.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class LLMResponse:
    """A normalized response from any backend."""

    content: str
    raw: Any = None


class LLMBackend(ABC):
    """Base class for pluggable language model backends."""

    @abstractmethod
    def complete(
        self,
        system: str,
        messages: list[dict[str, str]],
        max_tokens: int = 1024,
    ) -> LLMResponse:
        """Generate a completion given a system prompt and message history.

        ``messages`` is a list of ``{"role": "user" | "assistant", "content": str}``
        dicts, following the Anthropic Messages API convention.
        """
        raise NotImplementedError
