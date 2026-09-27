from agentforge.agent import Agent
from agentforge.llm.mock import MockBackend
from agentforge.tools.builtin import builtin_tools


def test_agent_returns_a_string_final_answer():
    agent = Agent(name="test-agent", llm=MockBackend(), tools=builtin_tools, max_steps=3)
    result = agent.run("hello there")
    assert isinstance(result, str)
    assert len(result) > 0


def test_agent_invokes_calculator_tool_and_finishes():
    agent = Agent(name="calc-agent", llm=MockBackend(), tools=builtin_tools, max_steps=4)
    result = agent.run("please calculate 2 + 2")
    kinds = [s.kind for s in agent.tracer.steps]
    assert "action" in kinds
    assert "observation" in kinds
    assert isinstance(result, str)


def test_agent_stops_after_max_steps_if_never_finishing():
    class NeverFinishBackend(MockBackend):
        def complete(self, system, messages, max_tokens=1024):
            from agentforge.llm.base import LLMResponse

            return LLMResponse(content="Thought: still thinking...")

    agent = Agent(name="stubborn", llm=NeverFinishBackend(), tools=builtin_tools, max_steps=2)
    result = agent.run("do something")
    assert "max_steps" in result
