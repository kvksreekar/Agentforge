# Contributing to AgentForge

Thanks for considering a contribution! This project aims to stay small,
readable, and well-tested rather than feature-maximal.

## Getting set up

```bash
git clone https://github.com/<you>/agentforge.git
cd agentforge
pip install -e ".[dev]"
pytest
```

## Before opening a PR

- `ruff check .` — no lint errors
- `mypy src/agentforge` — no new type errors
- `pytest` — all tests passing, and add tests for new behavior
- Keep functions small and typed; prefer dataclasses over ad-hoc dicts for
  structured data.

## Adding a tool

Tools are plain functions registered on a `ToolRegistry`:

```python
from agentforge.tools.registry import ToolRegistry

my_tools = ToolRegistry()

@my_tools.register("weather", "Get the current weather for a city.", {"city": "str"})
def weather(city: str) -> str:
    ...
```

## Adding a backend

Implement `agentforge.llm.base.LLMBackend` — a single `complete()` method —
and your backend works with every existing agent, tool, and the orchestrator
without any other code changes.

## Reporting bugs / proposing features

Please open an issue describing the problem or idea before submitting a large
PR, so we can agree on the approach first.
