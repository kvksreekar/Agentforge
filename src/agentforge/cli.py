"""Command-line interface for AgentForge.

    agentforge "What is 12 * 7?"

(Typer collapses to a bare command when an app has only one subcommand —
as more subcommands are added, this will become `agentforge run "..."`.)
"""
from __future__ import annotations

import typer
from rich.console import Console

from .agent import Agent
from .llm.mock import MockBackend
from .tools.builtin import builtin_tools

app = typer.Typer(help="AgentForge: build, run, and inspect tool-using agents.")
console = Console()


@app.command()
def run(
    task: str,
    agent_name: str = typer.Option("assistant", help="Display name for the agent."),
    max_steps: int = typer.Option(8, help="Maximum reasoning steps before giving up."),
    show_trace: bool = typer.Option(True, help="Print the full reasoning trace."),
) -> None:
    """Run a single agent on TASK using the offline mock backend.

    Swap MockBackend() for AnthropicBackend() in your own code (see
    examples/research_assistant.py) to run against a real model.
    """
    agent = Agent(name=agent_name, llm=MockBackend(), tools=builtin_tools, max_steps=max_steps)
    result = agent.run(task)

    console.print(f"[bold green]Result:[/bold green] {result}")
    if show_trace:
        console.print("\n[dim]--- trace ---[/dim]")
        console.print(agent.tracer.render())


if __name__ == "__main__":
    app()
