"""The core ReAct-style agent loop.

An ``Agent`` alternates between three phases until it produces a final
answer or runs out of steps:

    Thought  -> the model reasons about what to do next
    Action   -> the model calls a tool with structured arguments
    Observation -> the tool's result is fed back into context

This is a well-known, deliberately simple pattern (see the ReAct paper,
Yao et al. 2022) chosen because it's easy to audit and easy to extend.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from .llm.base import LLMBackend
from .memory import Memory
from .tools.registry import ToolRegistry
from .tracing import Tracer

_ACTION_RE = re.compile(r"Action:\s*(\w+)\s*Action Input:\s*(\{.*\})", re.DOTALL)

SYSTEM_TEMPLATE = """You are {name}, an autonomous agent. {persona}

You can use the following tools:
{tool_list}

When you need a tool, respond in exactly this format:
Thought: <your reasoning>
Action: <tool name>
Action Input: <a single JSON object of arguments>

When you have the final answer, respond in exactly this format:
Thought: <your reasoning>
Final Answer: <your answer>
"""


@dataclass
class Agent:
    """A single tool-using agent driven by a pluggable LLM backend."""

    name: str
    llm: LLMBackend
    tools: ToolRegistry
    persona: str = "You are helpful, precise, and careful."
    max_steps: int = 8
    memory: Memory = field(default_factory=Memory)
    tracer: Tracer = field(default_factory=Tracer)

    def _system_prompt(self) -> str:
        tool_list = "\n".join(f"- {t.name}: {t.description}" for t in self.tools.list())
        return SYSTEM_TEMPLATE.format(
            name=self.name,
            persona=self.persona,
            tool_list=tool_list or "(no tools available)",
        )

    def run(self, task: str) -> str:
        """Run the agent on ``task`` until it finishes or hits ``max_steps``."""
        self.memory.add("user", task)

        for _ in range(self.max_steps):
            response = self.llm.complete(self._system_prompt(), self.memory.as_messages())
            text = response.content
            self.memory.add("assistant", text)

            if "Final Answer:" in text:
                final = text.split("Final Answer:", 1)[1].strip()
                self.tracer.log("final", final)
                return final

            match = _ACTION_RE.search(text)
            if not match:
                self.tracer.log("thought", text.strip())
                continue

            tool_name, raw_args = match.group(1), match.group(2)
            self.tracer.log("action", f"{tool_name}({raw_args})")

            try:
                args = json.loads(raw_args)
                observation = self.tools.get(tool_name)(**args)
            except Exception as exc:  # noqa: BLE001 - surfaced to the model, not raised
                observation = f"Error: {exc}"

            self.tracer.log("observation", str(observation))
            self.memory.add("user", f"Observation: {observation}")

        return "Agent stopped: reached max_steps without producing a final answer."
