import pytest

from agentforge.tools.builtin import builtin_tools
from agentforge.tools.registry import ToolRegistry


def test_calculator_tool_respects_precedence():
    tool = builtin_tools.get("calculator")
    assert tool(expression="2 + 2 * 3") == "8"


def test_unknown_tool_raises_key_error():
    with pytest.raises(KeyError):
        builtin_tools.get("does_not_exist")


def test_registry_specs_shape():
    registry = ToolRegistry()

    @registry.register("noop", "Does nothing.", {"x": "int"})
    def noop(x: int) -> int:
        return x

    specs = registry.specs()
    assert specs == [{"name": "noop", "description": "Does nothing.", "parameters": {"x": "int"}}]
