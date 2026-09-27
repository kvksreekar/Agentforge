import pytest

from agentforge.agent import Agent
from agentforge.llm.mock import MockBackend
from agentforge.orchestrator import Orchestrator
from agentforge.tools.builtin import builtin_tools


def _agent(name: str) -> Agent:
    return Agent(name=name, llm=MockBackend(), tools=builtin_tools, max_steps=2)


def test_delegate_runs_named_agent():
    orch = Orchestrator()
    orch.register(_agent("a"))
    result = orch.delegate("a", "hello")
    assert isinstance(result, str)


def test_delegate_unknown_agent_raises():
    orch = Orchestrator()
    with pytest.raises(KeyError):
        orch.delegate("ghost", "hello")


def test_pipeline_chains_agents():
    orch = Orchestrator()
    orch.register(_agent("first"))
    orch.register(_agent("second"))
    result = orch.pipeline("start", order=["first", "second"])
    assert isinstance(result, str)
