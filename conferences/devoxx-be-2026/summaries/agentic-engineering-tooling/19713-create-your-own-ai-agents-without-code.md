---
title: Create your own AI Agents without code
talkId: "19713"
conference: devoxx-be-2026
speakers: [David Gageot]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=EJv0TMNSUjw
durationMin: 45
slides: https://github.com/dgageot/devoxx-be-2026/blob/shorter/demoit.html
verdict: 6
reach: segment
frames: 11
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15

# Create your own AI Agents without code
David Gageot · Conference · Agentic Engineering & Tooling
Slides: https://github.com/dgageot/devoxx-be-2026/blob/shorter/demoit.html

## TL;DR
Docker engineer David Gageot builds a specialized AI agent with Docker Agent, an open-source harness configured in YAML instead of code, using a Pokemon team-builder as a stand-in for any business workflow. The live demo runs the full lifecycle: connecting existing APIs as tools, writing evals with an LLM judge, optimizing against a baseline, then serving the agent over an OpenAI-compatible API with tracing and packaging. The talk argues most business agents should be cheap, focused specialists rather than full coding agents.

## Key takeaways
- Reach for a specialized agent, not a coding agent, when the task is narrow: one focused job with controlled context and cost, even on the same underlying model.
- Trim pre-AI API responses to the fields the agent needs (name, stats, types) with hooks, since verbose payloads inflate token cost on every call.
- Turn desired behavior into eval cases early: hard assertions for rules plus LLM-as-judge relevance checks, repeated to expose flakiness.
- Optimize one variable at a time with flavors (small YAML patches) and keep a change only if it improves the eval score against the baseline.
- Give the model tools for what LLMs do badly: a shell command for random numbers, a calculator-style tool for stat totals it kept miscounting.
- Serve the finished agent as a black box over OpenAI-compatible HTTP, MCP, or A2A, and instrument it with OpenTelemetry to see where time and tokens go.

## Notes

### [00:35](https://youtu.be/EJv0TMNSUjw?t=35) Coding agents vs specialized agents
Gageot opens with an audience poll: most attendees use a coding agent daily, fewer a PR reviewer. He argues teams conflate the model with the tool ("we are going to use Claude" for a business agent) when coding agents and specialized agents differ: specialized agents solve one focused task with cost under control, while a coding agent's footprint (around 40k tokens of base context, per the talk) makes it too expensive to run whole business workflows. The models underneath can be identical.

### [02:38](https://youtu.be/EJv0TMNSUjw?t=158) What Docker Agent is
The speaker works on Docker Agent, the harness behind Gordon v2, Docker's AI assistant shipped to millions of users. Docker Agent is open source, configured mainly in YAML (a Go SDK exists), runs as a standalone binary or `docker agent` CLI plugin with no Docker engine required, and connects to any model provider, local models via Docker Model Runner or Ollama, or an AI gateway. A slide diagram explains the agent loop: user question to model, model requests tool calls, the harness executes them and returns results, and the model answers or calls more tools.

### [05:47](https://youtu.be/EJv0TMNSUjw?t=347) Hello world: a pirate-parrot agent
The simplest config is a parrot-talking agent started in the terminal UI. It costs a fraction of a cent per run, far less than the same trick on a coding agent because of the smaller model, prompt, and tool set. Switching models is one flag (`--model=anthropic/claude-haiku-4-5` shown on screen); a more capable model ran about 15 times the cost of the cheap one. A slightly more useful agent rewrites user text as one polite English sentence, and instructions can be edited and rerun in seconds.

### [10:26](https://youtu.be/EJv0TMNSUjw?t=626) One agent, several interfaces
The same YAML runs interactively in the TUI, headless with `--exec` for scripting (including a raw mode showing every JSON object on the wire), as an OpenAI-compatible HTTP server a curl client streams from, over A2A for agent-to-agent calls, or as an MCP server consumable by tools like Claude Code.

### [13:37](https://youtu.be/EJv0TMNSUjw?t=817) The Pokemon Arena project
Gageot frames the main demo: "when I say Pokemon, think my business use case." A local clone of the Pokedex API stands in for a company catalog, and an arena microservice hosts team battles. The agent to build looks up Pokemon facts, proposes a team under constraints, and spars it against known opponents.

### [15:08](https://youtu.be/EJv0TMNSUjw?t=908) Plugging an OpenAPI service in as tools
Pointing the agent at the Pokedex OpenAPI spec exposes dozens of tools, visible in a debug listing. Gageot restricts it to the single `pokemon_retrieve` endpoint and uses hooks to keep only three top-level JSON fields (name, stats, types), confirmed by an audience member as a token-cost move. Asked "what type is Pikachu?", the agent calls the tool and answers Electric. Other toolset types on one slide: script, filesystem, and plain HTTP API.

### [19:19](https://youtu.be/EJv0TMNSUjw?t=1159) Local tools and guideline files
Three more capabilities land in quick succession. A `random_integer` shell tool injects real randomness, since LLMs asked for random numbers keep answering 42; Gageot flags the security caveat of running shell commands. Team-building guidelines load either as always-on prompt files (the AGENTS.md pattern) or a read-only filesystem tool scoped to one file, enforced by the harness even if the model asks for another file. A second business API without an OpenAPI spec gets wired manually as one scoped HTTP tool with hand-written argument schemas, verbose but fast to iterate on.

### [24:00](https://youtu.be/EJv0TMNSUjw?t=1440) Structured output turns the agent into a service
Declaring a JSON schema makes the agent return a valid team document (piped to jq on screen), so downstream software gets a predictable answer. Gageot notes most current LLMs support this, though none guarantees valid JSON every time. The agent is now a black box with known inputs and outputs.

### [25:03](https://youtu.be/EJv0TMNSUjw?t=1503) Evals: tests for a non-deterministic agent
The builder cheats: over-budget teams presented as legal, duplicate members ignored, losses reported as wins. The fix is evals, presented as unit tests for agents. Gageot shows five cases (legal Water team, build-and-spar, honest loss report, reject over-budget, reject duplicates), each with red/green assertions plus LLM-as-judge relevance checks ("does the response follow the rules?"). Capture a run as a test case, add the checks, then run `docker agent eval agents/11-builder.yaml evals/arena --repeat 5 --judge-model openai/gpt-5.6-terra`.

### [29:43](https://youtu.be/EJv0TMNSUjw?t=1783) Reading the eval report
The report shows 80% of cases passing at least once against 40% passing every time (`pass^5`): two cases stable, two flaky, one failing, with per-case cost medians around a tenth of a cent, cost outliers flagged, and a total of $0.027 over 2m24s. Gageot reads this as "basically random" and not shippable. The fix loop is either manual or handed to another agent fed the YAML, tests, and detailed output; held-out cases stay hidden so the optimizer cannot overfit to the exam.

### [32:49](https://youtu.be/EJv0TMNSUjw?t=1969) Optimizing with flavors
A flavor is a small patch on the YAML that changes one thing, here adding a tool-backed arithmetic tool so stat totals are computed instead of guessed (the model kept summing the wrong members after redrawing duplicates). Eval suites run inside containers rather than sandboxes to keep thousands of repetitions affordable. Keep an edit only if the same evals score better than baseline.

### [36:30](https://youtu.be/EJv0TMNSUjw?t=2190) Serving, tracing, and packaging
The finished builder is served over OpenAI-compatible HTTP on port 8080 while the arena backend stays on 8090; a Python client sends one chat request and parses the structured plan. With `--otel`, a Jaeger trace shows four model calls plus tool spans, timings, and token usage, confirming little time goes to external services. A compose file packages agent, guidelines (read-only), and siblings, resolving secrets via 1Password and injecting them through the environment.

### [39:38](https://youtu.be/EJv0TMNSUjw?t=2378) Arena fights and a 32-player tournament
Two agents submit sealed teams through a permission gate (the speaker approves each external call live); the first fight draws because both built the same team without the randomness tool. A coordinator then fans out to background sub-agents for a 32-player tournament, with the backend validating, judging, and revealing each result. The deck reports 99/100 fixture-legal proposals at a 10.2s median for the fast Luna players.

### [42:15](https://youtu.be/EJv0TMNSUjw?t=2535) Closing and further capabilities
Unexplored features get a word cloud: A2A and MCP consumption, ACP for JetBrains and Zed, LSP, RAG, memory, skills, sandboxes, model routing, snapshots, and the Go SDK. The deck (DemoIt HTML), docs, source, and demo tool links close the talk, plus a hidden slide offering $250 in cloud sandbox credit.

## Tools, libraries and specs
- Docker Agent (open-source agent harness, YAML config, Go SDK) — the talk's subject, at github.com/docker/docker-agent
- Gordon — Docker's AI assistant, v2 built on Docker Agent
- DemoIt — dgageot/demoit, live-coding presentation tool used for the deck
- PokéAPI (local container clone) and the synthetic Pokemon Arena backend — demo services
- Jaeger with OpenTelemetry OTLP export (`--otel`) — agent tracing
- Protocols: MCP (serve and consume), A2A, ACP (JetBrains, Zed), LSP, OpenAI-compatible chat API
- Models and providers: Anthropic claude-haiku-4-5, openai/gpt-5.6-terra (eval judge), gpt-6-luna, Docker Model Runner, Ollama, 1Password CLI for secret injection

## Who should watch
Developers and platform engineers asked to turn a business workflow into an AI agent gain the most: the evals-first loop and cost discipline transfer directly. Viewers deciding between a coding agent and a purpose-built service get a clear framing. Skip it if you already ship evaluated agents in production, or if you want Docker Agent API internals rather than a builder's tour (the companion three-hour deep dive covers that).

## Verdict
**6/10**: A live build with an eval report read on screen and a published demo repo, held back by a cut optimization run and a tour of documented features.

**Reach segment**: Developers adding LLM features or agents to their applications can apply the evals-first loop and the serving setup directly.

**Novelty 1/2**

- **+** [31:47](https://youtu.be/EJv0TMNSUjw?t=1907) The speaker reports running thousands of Gordon evals and fixing some by hand and some with another agent, so the worked example carries production testing experience.
- **−** The evaluation and flavors pages of docs.docker.com/ai/docker-agent already cover `--repeat`, the LLM judge, container-isolated evals and the flavor patch the talk shows.

**Demonstrated 1/2**

- **+** [18:18](https://youtu.be/EJv0TMNSUjw?t=1098) The agent calls the Pokemon tool live and answers Electric for Pikachu, with the tool call visible in the terminal UI.
- **−** [33:51](https://youtu.be/EJv0TMNSUjw?t=2031) The flavor run that would show the eval score improving against the baseline is cut for time, so the optimization loop is described rather than shown.
- **−** [41:13](https://youtu.be/EJv0TMNSUjw?t=2473) The 32-agent tournament is announced as the proof and the talk closes without its output, after a first match that draws from a missing randomness tool.

**Measured 1/2**

- **+** [32:19](https://youtu.be/EJv0TMNSUjw?t=1939) The eval report shows 80% of cases passing at least once against 40% passing every time (`pass^5`) over five repetitions, with per-case cost medians and a $0.027 total over 2m24s.
- **−** [08:53](https://youtu.be/EJv0TMNSUjw?t=533) The "15 times more expensive" model comparison is stated without the per-run costs shown on screen.

**Depth 1/2**

- **+** [34:54](https://youtu.be/EJv0TMNSUjw?t=2094) Eval suites run in containers instead of sandboxes because sandboxes would cost too much across thousands of repetitions.
- **+** [35:26](https://youtu.be/EJv0TMNSUjw?t=2126) Held-out cases stay hidden from the optimizing agent so it cannot memorize the answers, a stated trade-off of agent tuning.
- **·** [42:15](https://youtu.be/EJv0TMNSUjw?t=2535) Sandbox internals go to the keynote and the three-hour companion session; this slot covers using the features.

**Reusable 2/2**

- **+** [44:19](https://youtu.be/EJv0TMNSUjw?t=2659) The speaker points to the presentation repository, which holds the agent YAML files, the eval cases, the arena backend and the compose setup used on stage.
- **+** [44:19](https://youtu.be/EJv0TMNSUjw?t=2659) The closing slide also links the Docker Agent documentation, its source and the DemoIt presentation tool.
