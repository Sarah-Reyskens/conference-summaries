---
title: "Specialized AI Agents: from concept to production"
talkId: "19714"
conference: devoxx-be-2026
speakers: [David Gageot]
track: Agentic Engineering & Tooling
sessionType: Deep Dive
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=npSWywhFDHo
durationMin: 139
slides: null
verdict: 9
frames: 22
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Specialized AI Agents: from concept to production

David Gageot · Deep Dive · Agentic Engineering & Tooling

## TL;DR

Gageot builds a specialized Pokémon team-builder agent with Docker Agent, a YAML-first open-source harness, going from a one-line toy to an evaluated, served system. The core argument: specialization beats a shared coding agent on cost and fitness, and the path to production runs through tool design, eval suites with LLM-as-judge scoring, and iterative measurement. Everything is demonstrated live, ending with agents fighting each other in a tournament bracket.

## Key takeaways

- Specialize agents per task: a shared coding agent ships thousands of config tokens per call, so a narrow agent doing one job costs a fraction per query.
- Give knowledge through toolsets, not prompts: point the agent at existing OpenAPI specs and trim tool responses before they reach the model to protect context and budget.
- Instructions focus the model but constrain nothing; anything that must be right (counting, schema, business rules) needs a tool or an API that enforces it.
- Treat evals like tests with scores instead of pass/fail: fixed scenarios, repeated runs to expose flakiness, a smarter model as judge, baselines to compare patches against.
- A better prompt plus a purpose-built tool beat a five-to-ten-times more expensive model on the same eval suite in the live comparison.
- Serve the same YAML over an OpenAI-compatible HTTP endpoint or as an MCP server, and add trace telemetry before calling it production.

## Notes

### [09:25](https://youtu.be/npSWywhFDHo?t=565) How an agent works: the model, the tools, and the harness loop

The talk opens with the basic loop: the user asks a question, the model requests tool calls instead of answering directly, something executes those tools and feeds results back, and the model repeats until it can produce a final answer. The piece coordinating models and tool calls is the harness, which is exactly what Docker Agent is. Gageot stresses that the loop looks simple but has to absorb many LLM providers and many tool kinds (local, remote, MCP, shell, files, enterprise endpoints) while callers treat the whole thing as a black box.

### [12:02](https://youtu.be/npSWywhFDHo?t=722) A one-line pirate agent, and why specialization saves tokens

The first demo defines an agent whose entire configuration is one instruction line ("answer like a pirate") and runs it against a model. The point is economic: typing the same request into a coding agent would drag along roughly 4,000 tokens of coding configuration for a question that needs none of it. Docker Agent itself runs locally with no Docker engine required (`docker-agent` binary, or `docker agent` as a CLI plugin), but it always needs a model: credentials via environment variables, local runners, or an AI gateway. `docker agent doctor` reports which provider credentials the machine currently holds.

### [24:09](https://youtu.be/npSWywhFDHo?t=1449) One YAML, many runtimes: TUI, exec, serve

The same agent file can run interactively in a terminal UI (tabs, forks, history, per-model cost inspection), headlessly for scripts, as JSON event streams, or as a server. The server mode speaks the OpenAI chat API, so any OpenAI client can call the specialized agent as if it were a model; a live curl turns a rude "fix this app" message into polite English. The TUI is framed as the iteration workbench (inspect tool calls, switch models mid-conversation, watch cost), not the production surface.

### [32:31](https://youtu.be/npSWywhFDHo?t=1951) Teaching the agent facts: PokéAPI over OpenAPI

The running example is a Pokémon team builder ("when I say Pokémon, think my business use case"). Since models only know training data up to a cutoff, the agent gets a PokéAPI OpenAPI toolset. Docker Agent expands the spec into tools automatically (over a hundred here), so Gageot restricts the agent to a single retrieve tool and adds a response hook that keeps only name, type, and stats. The untrimmed Pikachu response is shown as a wall of JSON to motivate the trimming: full payloads burn money and bury the model. Live queries then answer "what type is Pikachu" and compare regional Pokémon from the API.

### [44:37](https://youtu.be/npSWywhFDHo?t=2677) Scripts, guidelines, and the sparring-partner action API

Three more toolset kinds follow. A script toolset runs a shell command with typed arguments for things LLMs do unreliably (sums, random integers); Gageot admits it resembles code and prefers APIs, but uses it where no API exists. Guideline files (AGENTS.md style) load either as appended instructions or as a read-only file tool. Finally a plain `api` toolset wraps a sparring-partner HTTP endpoint that has no OpenAPI spec: knowledge APIs and action APIs are different things, and the action side is where the backend validates teams, because the model may hallucinate names or ignore rules.

### [58:38](https://youtu.be/npSWywhFDHo?t=3518) Permissions, hooks, API keys, structured output

Permissions decide per tool whether Docker Agent allows, forbids, or asks the user before calling (read-only Pokémon retrieval is auto-allowed; joining the arena asks). Finer-grained control comes from hooks running before or after tool calls, for example to strip secrets. Credentials can come from environment variables, environment providers like 1Password or keychain, fixed YAML values, or pass-through of the caller's HTTP auth header to the endpoint. Structured output with a JSON schema makes the agent consumable as an API, with the caveat that schema adherence varies by backing model.

### [68:57](https://youtu.be/npSWywhFDHo?t=4137) Evals: test cases plus LLM-as-judge

After the break the topic turns to proving the agent works: legal teams and honest coaching (reporting the sparring result truthfully). Eval cases are JSON files, each with an ID, a first user message (build-only prompts, an invalid-team probe, an over-budget probe, a loss the agent might misreport as a win), strict assertions (structure, regex), and relevance checks. Relevance checks are fuzzy assertions verified by a separate LLM-as-judge: production can run a cheap fast model while evals judge with a smarter expensive one, trading judge cost for verdict quality.

### [80:58](https://youtu.be/npSWywhFDHo?t=4858) Running evals: baselines, flakiness, cost outliers

`docker agent eval` runs every case file against the YAML, five repeats each, with a chosen judge model, and prints a summary: assertions 95%, relevance 87%, pass-at-5 100% but pass-hat-5 only 60%, plus per-case cost. The flaky duplicated-team case and cost outliers (one case near two cents against others ten times cheaper) get flagged for investigation. Each eval runs isolated in its own container, and past sessions stay inspectable so a failure can be traced tool call by tool call. Full JSON output is available for trend tracking.

### [89:21](https://youtu.be/npSWywhFDHo?t=5361) Fixing a failure with a flavor: better prompt plus a counting tool

The duplicate-team failure traced to bad arithmetic: the model swapped a Pokémon but summed the old trio's stats. The fix ships as a flavor, a patch on the base agent adding instruction lines and a stat-summing tool, then re-runs the identical suite against the saved baseline. Result on screen: no regressions, pass-hat-5 up to 100%, slightly higher cost from the extra instruction and tool-description tokens. Eval cases themselves can be authored by saving a live session as JSON and filling in the relevance checks, or generated synthetically in bulk by a strong model.

### [99:53](https://youtu.be/npSWywhFDHo?t=5993) Swapping the model: a stronger LLM loses to a better prompt

The same suite runs against a model five to ten times more expensive (Saul vs Luna), without the prompt and tool fix, to isolate the effect of model strength. It stays flaky on the duplicate case and underperforms the cheaper model with the fix, live evidence that prompt and tooling improvements can dominate model spend. Gageot ties this to Gordon, Docker's assistant: a 4,000-question synthetic suite plus manual and complaint-driven non-regression cases, used to hold quality while keeping the serving model cheap.

### [105:09](https://youtu.be/npSWywhFDHo?t=6309) An agent that optimizes your agent, and the overfitting trap

An optimizer agent is shown: a smarter model with read-only file tools, the YAML, the evals, and shell access, looping over run-measure-patch cycles. Gageot warns it must run sandboxed with least privilege, citing optimizer escape anecdotes. He also warns against training on the final exam: optimizing against the eval set bloats instructions with hardcoded question-answer pairs, and admits part of Gordon's shipped YAML is overfitted this way (hardcoded URLs for compose questions) because it beats the knowledge base on real questions.

### [112:29](https://youtu.be/npSWywhFDHo?t=6749) Sub-agents: coordinator, builder, coach

A coordinator-builder-coach decomposition runs live: the builder drafts teams on a capable model while the coach merely submits them via API on a dumber one. Motivations are smaller per-agent context, cheaper models for trivial steps, and least-privilege tool separation so no single agent holds a dangerous tool mix. Gageot argues against it for this simple task (coordination chatter costs tokens; Gordon ships a single agent) and calls his own model pairing wrong, since the "dumb" coach model costs more than the builder's.

### [118:50](https://youtu.be/npSWywhFDHo?t=7130) Serving in production: OpenAI API, MCP, Jaeger traces

Production means `docker agent serve`: the OpenAI-compatible chat endpoint for code clients, or MCP-server mode so other agents (Claude Code, Codex, another Docker Agent) can call this agent as a tool. Gageot recommends plain HTTP for company-internal serving and calls MCP still-churning. Telemetry answers the introspection question: with Jaeger collecting spans, a trace shows four LLM calls dominating latency while tool calls take near-zero time, pointing optimization at call count or concurrency.

### [127:09](https://youtu.be/npSWywhFDHo?t=7629) Packaging with Compose, pushing YAML as OCI, the arena finale

The agent ships in a Compose stack (read-only mounts, secrets injected from 1Password, local PokéAPI and arena services, state in volumes), reachable over HTTP identically to the local run. Agent YAML can also be pushed to a registry as an OCI artifact for pull-and-run sharing, the mechanism Docker Desktop uses to distribute Gordon. The finale submits agent-built teams to the arena UI (permission prompt approved live), agent A wins its match, and a 32-player tournament bracket starts filling before being cut short. Uncovered features are listed: ACP, A2A, LSPs, webhooks, background jobs, MCP clients, sandboxes.

## Tools, libraries and specs

- Docker Agent (open-source YAML agent harness; TUI, exec, serve, eval, flavors, permissions, hooks, sub-agents)
- Gordon (Docker Desktop AI assistant; v2 built on Docker Agent, shipped to millions of users)
- PokéAPI (public Pokémon REST API consumed via its OpenAPI spec, self-hosted locally for the demo)
- Models via an AI gateway: GPT-6 Luna (cheap default), Saul (5–10x pricier), GPT-4.1, Astra, Fable; Jeff-class models named as future judge candidates
- Protocols: OpenAI chat completions API, MCP (client and server), A2A, ACP
- Jaeger (trace collection for served agents), Docker Compose and OCI artifacts (packaging and sharing agents), demoit (the demo presentation tool), 1Password (secret injection)

## Who should watch

Engineers about to put a task-specific agent into production who want a full loop (tools, evals, measurement, serving) rather than a prompting tutorial. Docker Agent users get the most, since every mechanism is its feature set. Skip it if you want model internals or training: models are interchangeable, mostly unnamed gateway endpoints here. Teams already running LLM-as-judge eval harnesses will find the methodology familiar and can skim to the optimizer-agent and serving segments.

## Verdict

**9/10**: A specialized agent is built, evaluated, served and used live, with design trade-offs and a complete demo repository; the core build mostly follows Docker Agent's documented features.

**Novelty 1/2**

- **+** [97:16](https://youtu.be/npSWywhFDHo?t=5836) Gordon's evaluation practice combines 4,000 stronger-model-generated questions with manual and complaint-driven non-regression cases.
- **+** [111:57](https://youtu.be/npSWywhFDHo?t=6717) The speaker explains why Gordon's shipped instructions include overfitted compose URLs that outperform knowledge-base retrieval on real questions.
- **−** Docker Agent's official toolset and evaluation documentation covers most of the feature-led build, while the Gordon experience and speaker-run comparison occupy smaller parts of the session.

**Demonstrated 2/2**

- **+** [83:36](https://youtu.be/npSWywhFDHo?t=5016) The full eval suite executes live with per-case scores, flakiness counts and cost output visible.
- **+** [121:59](https://youtu.be/npSWywhFDHo?t=7319) The served agent returns a structured team to a Python client, and the later arena match finishes with agent A winning 2989 to 2873 at [132:45](https://youtu.be/npSWywhFDHo?t=7965).
- **−** [123:00](https://youtu.be/npSWywhFDHo?t=7380) The alternative MCP-serving route is explained without a client run, although HTTP serving completes.

**Measured 2/2**

- **+** [94:08](https://youtu.be/npSWywhFDHo?t=5648) The five-repeat flavor run prints relevance 0.800 → 1.000 and assertions 0.991 → 1.000 against a saved baseline, with the duplicate-team failure fixed and no regressions.
- **+** [102:00](https://youtu.be/npSWywhFDHo?t=6120) The model-only swap on the same suite reaches relevance 95.0% and pass^5 80.0% at $0.455792 per suite, versus 100% and about $0.026 for the fixed cheap setup.
- **−** [103:34](https://youtu.be/npSWywhFDHo?t=6214) The speaker warns that ambiguous relevance checks and imperfect judge models can cause flakiness, so the suite scores alone do not establish correctness on unseen questions.

**Depth 2/2**

- **+** [52:25](https://youtu.be/npSWywhFDHo?t=3145) Instructions are explained as focus aids while tools carry enforceable constraints, a design rule applied throughout the build.
- **+** [108:48](https://youtu.be/npSWywhFDHo?t=6528) Eval cases run in isolated containers with only their required files, with container overhead weighed against sandboxes and Gordon's environment chosen to represent a user's machine.
- **+** [114:04](https://youtu.be/npSWywhFDHo?t=6844) The sub-agent design weighs smaller contexts and cheaper models against coordination-token cost, then explains separating tool permissions by responsibility.

**Reusable 2/2**

- **+** [137:06](https://youtu.be/npSWywhFDHo?t=8226) The Presentation QR opens github.com/dgageot/devoxx-be-2026, which carries agents/01-pirate.yaml to 16-tournament.yaml, evals/arena/*.json with baselines and measurements, and the arena and Compose files.
- **+** [129:47](https://youtu.be/npSWywhFDHo?t=7787) Agent YAML is pushed to a registry as an OCI artifact and pulled or run by name and tag, the way Gordon ships.


