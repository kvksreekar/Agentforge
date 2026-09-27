# Roadmap

AgentForge intentionally ships small. These are the directions it's designed
to grow in without breaking the core abstractions.

## Near term
- [ ] Streaming responses through `LLMBackend.complete` (or a new `stream()`)
- [ ] A `RetryPolicy` for transient tool/backend failures
- [ ] More built-in tools: web search, HTTP fetch, shell (sandboxed)
- [ ] `pip install agentforge` published to PyPI

## Memory & retrieval
- [ ] Summarizing old turns instead of dropping them (`Memory.summary`)
- [ ] Pluggable vector-store backend for long-term / retrieval-augmented memory
- [ ] Per-agent and shared (cross-agent) memory scopes

## Orchestration
- [ ] Fan-out / fan-in: run N agents in parallel and merge results
- [ ] Voting / debate patterns between agents
- [ ] A declarative graph (YAML/DSL) for wiring agent pipelines

## Observability
- [ ] Export traces to OpenTelemetry
- [ ] A small web dashboard for replaying and diffing traces
- [ ] Token/cost accounting per run

## Evaluation
- [ ] A benchmark harness: define tasks + expected outcomes, score agents
- [ ] Regression testing for prompts (catch behavior drift over time)

Contributions toward any of these are very welcome — see CONTRIBUTING.md.
