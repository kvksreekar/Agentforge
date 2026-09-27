"""FastAPI server exposing AgentForge agents over HTTP.

Run locally with:
    uvicorn api.server:app --reload

Or via Docker:
    docker compose up --build
"""
from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from agentforge.agent import Agent
from agentforge.llm.mock import MockBackend
from agentforge.tools.builtin import builtin_tools

app = FastAPI(title="AgentForge API", version="0.1.0")


class RunRequest(BaseModel):
    task: str
    agent_name: str = "assistant"


class RunResponse(BaseModel):
    result: str
    trace: str


@app.post("/agents/run", response_model=RunResponse)
def run_agent(req: RunRequest) -> RunResponse:
    agent = Agent(name=req.agent_name, llm=MockBackend(), tools=builtin_tools)
    result = agent.run(req.task)
    return RunResponse(result=result, trace=agent.tracer.render())


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
