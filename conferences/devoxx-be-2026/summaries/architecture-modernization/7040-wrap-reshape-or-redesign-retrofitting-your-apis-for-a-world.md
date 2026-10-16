---
title: "Wrap, Reshape, or Redesign: Retrofitting Your APIs for a World of Agents"
talkId: "7040"
conference: devoxx-be-2026
speakers: [Horacio Gonzalez]
track: Architecture & Modernization
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=ymLlOAB8h_c
durationMin: 48
slides: https://noti.st/lostinbrittany/bxObJc/wrap-reshape-or-redesign-retrofitting-your-apis-for-a-world-of-agents
verdict: 7
reach: segment
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-15
---

# Wrap, Reshape, or Redesign: Retrofitting Your APIs for a World of Agents

Horacio Gonzalez · Conference · Architecture & Modernization

Slides: https://noti.st/lostinbrittany/bxObJc/wrap-reshape-or-redesign-retrofitting-your-apis-for-a-world-of-agents

## TL;DR

APIs that served human developers for years fail under LLM agents because agents cannot fill in undocumented conventions: they set the variable but never restart the process. Gonzalez proposes classifying every capability as wrap (already explicit), reshape (scattered knowledge folded into intent-level tools), or redesign (unstated invariants rebuilt with real safety architecture), illustrated with failures from Clever Cloud's own production API and cases from Cloudflare, AWS, Postmark, and GitHub.

## Key takeaways

- Audit every API capability against four questions: dependencies, reversibility, blast radius, completion. Agents cannot infer what you never wrote down.
- Expose large APIs through search/execute discovery instead of one tool per endpoint: Cloudflare replaced 2,500 tools (~1M context tokens) with a 2-function code mode under 1,000 tokens.
- Collapse multi-step human workflows into one outcome-shaped call implemented in deterministic code. Postmark's `diagnoseDelivery` replaced five chained calls and took support diagnoses from 80% to 100% correct.
- Put safety boundaries in the API, not in prompts or MCP annotations: prepare → inspect → execute for destructive operations, explicit done-states for async ones, human approval for money movement.
- Treat tool descriptions as interface rather than documentation (purpose, when to use, side effects, when not to use), then verify them with behavioral tests run across models and harnesses.

## Notes

### [01:34](https://youtu.be/ymLlOAB8h_c?t=94) The demo that fails: Java 25

A user asks an agent to set Java 25 on a Clever Cloud application. The agent finds the documented step, sets `CC_JAVA_VERSION=25`, and reports success. The application still runs the old version: every developer knows a changed environment variable needs a process restart, but the API documentation never said so. Gonzalez calls this implicit knowledge the root cause, and frames agents as users his 15-year-old API was never designed for.

### [04:42](https://youtu.be/ymLlOAB8h_c?t=282) The semantic gap and four questions

Human users arrive with a silent contract: they read docs, infer conventions, and sense danger in an endpoint named `deleteAll`. Agents must infer all of that from the spec. Four unanswered questions cause the damage: dependencies (what else must happen, in what order), reversibility (can I undo this), blast radius (what else does this touch), and completion (when this returns, is it done). Clever Cloud's own Swagger holds 310 operations with zero descriptions and 267 without even a summary, yet it worked for years because humans were reading it.

### [08:24](https://youtu.be/ymLlOAB8h_c?t=504) The framework: wrap, reshape, redesign

Each capability gets one of three treatments, chosen by the size of its semantic gap rather than the cost of the work. Wrap when the knowledge is already explicit. Reshape when the knowledge exists but is scattered across conventions, tutorials, and tribal habits. Redesign when unstated invariants make the capability unsafe for an agent at all. One platform normally holds all three at once. On shelf life: smarter models let you wrap more, reshape may shrink, but redesign stays, because a better model makes fewer mistakes without making them cost less.

### [12:09](https://youtu.be/ymLlOAB8h_c?t=729) Wrap: search/execute beats one tool per endpoint

Wrapping works for typed, bounded, introspectable, non-destructive operations, perhaps 60-70% of an API. But one tool per endpoint floods the model context on every call. Cloudflare's answer (Code Mode MCP, February 2026) exposes only `search()` and `execute()` over 2,500+ endpoints, running generated code in a Dynamic Worker isolate, cutting context from nearly a million tokens to under a thousand. Clever Cloud copied the pattern with `search`, `execute`, plus `doc` (open source as `CleverCloud/mcp-simple-server`). AWS went further: about 8 tools over 15,000+ operations, with new services supported within days. MCP tool annotations (`destructiveHint` and friends) do not change the rule: the spec calls them hints and clients must treat them as untrusted.

### [19:33](https://youtu.be/ymLlOAB8h_c?t=1173) Reshape: intent-level tools

Failure two: "why isn't my application responding?" Seven individually correct tools (`get_application`, `get_logs`, `list_instances`, and four more) leave the agent to invent the workflow: which first, how many logs are enough, does STOPPED mean broken or deliberate. The reshape adds `diagnose_application(id)`, which chains the seven calls in deterministic code and returns one synthesized result (status, desired/running/healthy instances, latest deployment, recent errors, configuration warnings) while the atomic tools stay. Postmark did the same for email delivery diagnosis: one `diagnoseDelivery` function, fanned out in parallel and tolerant of single-lookup failure, replacing five calls. The principle: the model decides what requires judgement while software does what requires computation. Tool counts can move either way (GitHub 101 → 52, Postmark 4 → 24); what degrades selection is confusable tools, not numerous ones.

### [28:54](https://youtu.be/ymLlOAB8h_c?t=1734) Redesign: when the capability itself is wrong

Two real endpoints differ by one path segment: one unlinks an add-on from an application, the other destroys the database and its data. The safe one has a Swagger summary; the destructive one has nothing. Asked to detach a database, two out of seven model/harness combinations chose the destructive call. A WARNING in the description is not architecture. The redesign splits deletion into `prepare_addon_deletion` (returning the add-on, applications using it, latest backup, recoverable-until timestamp, consequences) and `execute_addon_deletion(plan_id)`, so the agent must inspect before it can act. The restart endpoint gets the same treatment: return a task id with states where `failed` counts as done, not "not yet". Billing endpoints get no autonomous tool at all: human approval or nothing. Agent-friendly does not mean agent-autonomous.

### [38:58](https://youtu.be/ymLlOAB8h_c?t=2338) Descriptions are the interface; measure behaviour

For a human, documentation is inert text read once; for an agent, the description is read at inference time on every call, so prose sits in the execution path. A good description states purpose, when to use it, side effects, and when not to use it. Rewriting descriptions alone lifted multi-step task completion from 33.5% to 44.6% on StableToolBench (same models, tools, tasks), while the study's BFCLv2 Live gain was +1.4 points ending at 86.4%: the worse your descriptions are today, the bigger the win. (The deck labels 86.4% as the baseline; in the paper it is the result.) To know whether prose is good enough, run behavioral tests: fixed golden prompts ("why did yesterday's deployment fail?", "delete the test database") replayed across model/harness combinations, tracking which pairs succeed.

### [43:48](https://youtu.be/ymLlOAB8h_c?t=2628) Agent-proofing helps humans; reShapr

Every fix in the talk (explicit completion, blast radius, dependencies, scoped authorization, reversible operations) is something teams always said they would get round to; agent pressure funds API work that also helps juniors and developers from other ecosystems. Cloudflare's agent-built Dynamic Workers became a primitive for all paid users, and Slack split one blanket `search:read` scope into four granular ones. The speaker admits the human-benefit evidence so far is anecdotal ("real cases" saying it is better, no published studies yet). The talk closes with reShapr, an open-source tool that ingests OpenAPI, GraphQL, or gRPC artifacts and produces enterprise MCP servers with rename/include/exclude, simplify/condense/filter, and endpoint security features.

## Tools, libraries and specs

- MCP (Model Context Protocol), including tool annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`)
- Cloudflare Code Mode MCP (February 2026): `search()` + `execute()` over 2,500+ endpoints
- `CleverCloud/mcp-simple-server`: search/execute/doc wrapper for the Clever Cloud API
- AWS MCP Server (GA 6 May 2026): ~8 tools over 15,000+ operations
- Postmark `diagnoseDelivery`: intent-level email delivery diagnosis
- reShapr: open-source API-to-MCP reshaping tool (OpenAPI, GraphQL, gRPC ingest)
- StableToolBench ("Learning to Rewrite Tool Descriptions", arXiv 2602.20426) and BFCLv2 Live
- OWASP 2026 agentic guidance (Steve Wilson, Rock Lambros): build the system so a fooled model breaks nothing important

## Who should watch

API and platform engineers whose endpoints are about to meet LLM agents, and architects deciding what "agent-ready" means for an existing surface. Skip it if you want MCP protocol mechanics (declared out of scope) or already run intent-level tool layers with behavioral evaluation.

## Verdict

**7/10**: A wrap/reshape/redesign framework tested on the speaker's own production API, with one baselined description-rewriting benchmark, but with no fix run on screen, the other figures without method and no published artifact for the redesign cases.

**Reach segment**: Teams building LLM features or shipping agent-facing APIs can apply intent-level tools and prepare/execute boundaries within the next year, while most of the audience meets agents as users rather than API designers.

**Novelty 2/2**

- **+** [08:24](https://youtu.be/ymLlOAB8h_c?t=504) The wrap/reshape/redesign framework classifies each capability by the size of its semantic gap, with the cost of the work left out of the choice, and gets applied to the speaker's own platform across three escalating failures.
- **+** [11:03](https://youtu.be/ymLlOAB8h_c?t=663) Smarter models let teams wrap more and shrink reshape, but redesign stays because a better model makes fewer mistakes without making them cost less: a shelf-life rule no single source states.
- **·** [45:54](https://youtu.be/ymLlOAB8h_c?t=2754) The independent reShapr tool landed on almost the same three-way framework, which corroborates it while showing the idea is in the air.

**Demonstrated 1/2**

- **+** [01:34](https://youtu.be/ymLlOAB8h_c?t=94) The Java-version failure is shown on slides as an agent exchange: success reported, application unchanged.
- **−** [23:09](https://youtu.be/ymLlOAB8h_c?t=1389) The diagnose endpoint, the prepare/execute redesign and the Cloudflare and AWS cases are described on slides or in speech; no run executes on screen.

**Measured 1/2**

- **+** [41:03](https://youtu.be/ymLlOAB8h_c?t=2463) Rewriting only tool descriptions lifted StableToolBench multi-step completion from 33.5% to 44.6% with models, tools and tasks held fixed (arXiv 2602.20426), while the same study's BFCLv2 Live gain on an already high score (86.4%) was +1.4 points.
- **−** [30:31](https://youtu.be/ymLlOAB8h_c?t=1831) The delete-endpoint probe reports two destructive calls from seven harnesses and seven models, but names no harness or model and shows no prompt or outputs.
- **·** [24:43](https://youtu.be/ymLlOAB8h_c?t=1483) The Postmark 80%-to-100% diagnosis figure is Postmark's reported outcome with no method shown.

**Depth 2/2**

- **+** [18:28](https://youtu.be/ymLlOAB8h_c?t=1108) MCP tool annotations are weighed as a safety mechanism and rejected on the spec's own wording: they are hints that clients must treat as untrusted, so a model can ignore them.
- **+** [34:12](https://youtu.be/ymLlOAB8h_c?t=2052) The prepare → inspect → execute pattern is argued from who owns the safety boundary: a non-deterministic model cannot hold it, and callers may run any harness, including a small local model.
- **·** [36:22](https://youtu.be/ymLlOAB8h_c?t=2182) The restart redesign stays at design level (a task id with states, where `failed` counts as done) with no implementation, which fits a strategy talk in a 50-minute slot.

**Reusable 1/2**

- **+** [16:20](https://youtu.be/ymLlOAB8h_c?t=980) The wrap case points to a real artifact: the `CleverCloud/mcp-simple-server` repository with search, execute and doc tools.
- **+** [46:24](https://youtu.be/ymLlOAB8h_c?t=2784) The talk sends viewers to the open-source reShapr tool, which generates an adapted MCP server from a Swagger file with renaming, include/exclude, filtering, simplifying and added endpoints.
- **−** [33:07](https://youtu.be/ymLlOAB8h_c?t=1987) No published artifact covers the redesign cases (prepare/execute deletion, task-id completion) or the behavioural tests, which are the talk's core beyond wrap and reshape.
