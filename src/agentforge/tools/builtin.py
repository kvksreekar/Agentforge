"""A small set of safe, dependency-free built-in tools."""
from __future__ import annotations

import ast
import operator as op
from collections.abc import Callable

from .registry import ToolRegistry

builtin_tools = ToolRegistry()

_OPS: dict[type[ast.AST], Callable[..., float]] = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
}


def _safe_eval(node: ast.AST) -> float:
    """Evaluate a restricted arithmetic AST (no names, calls, or attributes)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_safe_eval(node.operand))
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


@builtin_tools.register(
    "calculator",
    "Evaluate a basic arithmetic expression, e.g. '12 * (3 + 4)'.",
    {"expression": "str"},
)
def calculator(expression: str) -> str:
    tree = ast.parse(expression, mode="eval").body
    result = _safe_eval(tree)
    return str(result)


@builtin_tools.register(
    "read_file",
    "Read the first 4000 characters of a local text file.",
    {"path": "str"},
)
def read_file(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()[:4000]
