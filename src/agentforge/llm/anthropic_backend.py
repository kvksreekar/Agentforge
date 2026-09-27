"""Anthropic-powered LLM backend.

Requires the optional ``anthropic`` dependency:
    pip install "agentforge[anthropic]"
"""
from __future__ import annotations

import os

from .base import LLMBackend, LLMResponse


class AnthropicBackend(LLMBackend):
    """Drives agents using Claude via the Anthropic Messages API."""

    def __init__(self, model: str = "claude-sonnet-4-6", api_key: str | None = None) -> None:
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover - exercised only without the extra
            raise ImportError(
                "The 'anthropic' package is required for AnthropicBackend. "
                'Install it with: pip install "agentforge[anthropic]"'
            ) from exc

        self._client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = model

    def complete(
        self,
        system: str,
        messages: list[dict[str, str]],
        max_tokens: int = 1024,
    ) -> LLMResponse:
        response = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )
        text = "".join(block.text for block in response.content if block.type == "text")
        return LLMResponse(content=text, raw=response)
