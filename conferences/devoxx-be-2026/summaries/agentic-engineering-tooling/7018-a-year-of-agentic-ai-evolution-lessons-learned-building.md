---
title: "A Year of Agentic AI Evolution: Lessons Learned Building Production-grade Agentic Systems"
talkId: "7018"
conference: devoxx-be-2026
speakers: [Mario Fusco, Kevin Dubois]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=nEW0kosJjc8
durationMin: 52
slides: null
verdict: 8
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# A Year of Agentic AI Evolution: Lessons Learned Building Production-grade Agentic Systems

Mario Fusco, Kevin Dubois · Conference · Agentic Engineering & Tooling

## TL;DR

LangChain4j's agentic module moved from a fixed set of orchestration patterns to a pluggable planner abstraction that lets developers define, combine, and contribute their own agent-coordination strategies. The talk walks through the new planner API, several new patterns (goal-oriented, blackboard, voting, decision-model routing), a live demo, and the Quarkus-side production features around them.

## Key takeaways

- When one-size-fits-all agent patterns stop fitting, a small planner interface (given the context, which agent runs next, or done) is enough to express sequential, parallel, loop, conditional, supervisor, and custom strategies.
- Planners compose: a loop nested inside a goal-oriented graph recovers iteration that shortest-path traversal structurally forbids.
- A supervisor that routes by LLM judgment can be replaced by a decision model that answers typed yes/no or choice questions with probabilities, giving deterministic, threshold-based routing to one or several agents in parallel.
- Per-invocation model selection (cheap model while far from the quality bar, stronger model when close) controls cost better than binding one model per agent.
- Production agentic systems need the same controls as distributed systems: retries and fallbacks, tracing with token counts, persisted workflows that survive restarts and human-in-the-loop pauses, and guardrails on tool calls as well as model I/O.
- Non-AI agents (REST calls, MCP tools wrapped as agents) mix with LLM-backed agents in the same orchestration, so deterministic steps stay programmatic.

## Notes

### [00:32](https://youtu.be/nEW0kosJjc8?t=32) Recap: from one AI service to agentic systems

Dubois recaps the path from a single AI service (prompt, chat memory, tool and MCP calls, RAG, input/output guardrails, skills as just-in-time context) to multi-agent systems. Last year's module offered deterministic workflows (sequence, parallel, conditional) plus the supervisor pattern where an LLM picks which subagent to call. Feedback showed one size does not fit all, so the team reworked the fixed patterns into something pluggable.

### [07:56](https://youtu.be/nEW0kosJjc8?t=476) The pluggable planner and the goal-oriented pattern

Fusco introduces the planner interface: `nextAction` decides which agent (or set of agents) runs next given the current context, or returns done; `firstAction` and an init method carry default implementations. Every existing pattern was rewritten on top of it, including the trivial sequential planner (a cursor over subagents, done after the last). Planners are supplied to a generic builder as a `Supplier`, so each execution gets a fresh instance, and the declarative and programmatic APIs mix freely. The goal-oriented pattern treats each agent's input and output as preconditions and postconditions, builds a dependency graph, and traverses the shortest path from the initial input to the goal output. Because shortest paths cannot loop, patterns nest: a loop can replace one node of the graph.

### [17:55](https://youtu.be/nEW0kosJjc8?t=1075) Blackboard pattern and the patterns module

The new patterns live in a `langchain4j-agentic-patterns` module, and contributions are invited. Fusco sketches the blackboard pattern, where worker agents read and write shared state variables: a medical-diagnosis example feeds patient state, lab results, and medications onto the board until the agents converge on a diagnosis.

### [20:31](https://youtu.be/nEW0kosJjc8?t=1231) Live demo: the voting pattern

The demo runs a story pipeline: a creative-writer agent generates a story, then three critics (style, originality, engagement) evaluate it in parallel while a voting planner averages their scores, and an editor loop iterates until the score clears the bar. The run completes live: the review loop iterates three times before exiting.

### [24:47](https://youtu.be/nEW0kosJjc8?t=1487) Topology and execution views in the Quarkus Dev UI

The Quarkus extension renders the static agent topology (sequence containing the review loop containing the parallel critics, with data-flow edges for topic, story, and each critique) and a per-execution view showing each invocation's duration, token count, input, and output. In the demo run, story generation took 3.5 seconds, the review loop 15.4 seconds, and each critic roughly 1.3 to 1.7 seconds.

### [28:28](https://youtu.be/nEW0kosJjc8?t=1708) Dynamic per-invocation model selection

A `@ChatModelSupplier` method (with a programmatic-API equivalent) picks the model on every agent invocation. The demo configures a small base model and a larger enhanced model: below a score of 7.8 the loop keeps the cheap model since much can still improve, and near the 8.5 exit threshold it switches to the stronger model to finish the edit. The run log shows about thirty base-model calls and a couple of enhanced ones.

### [32:11](https://youtu.be/nEW0kosJjc8?t=1931) Decision-model routing with Jev

Dubois tried the newly released Jev decision model as a planner and Fusco shipped a `DecisionRouterPlanner` days later. A decision model cannot chat; it answers typed questions with probabilities. Without a threshold, one choice question ("which agent is best suited?") routes to the single most probable agent; with a threshold (0.5 in the example), one yes/no question per subagent routes to every agent above it in parallel. Asking about a broken leg plus suing the driver scores medical 74% and legal 81%, so both agents run.

### [37:54](https://youtu.be/nEW0kosJjc8?t=2274) Enterprise grade: fault tolerance, observability, guardrails

MicroProfile annotations (`@Retry`, `@Fallback`) apply directly to agents. Invocation duration and token usage flow into the LGTM stack (Loki, Grafana, Prometheus, Tempo) and into Langfuse via a Quarkus extension that starts a local instance in dev mode; its dashboard priced one agentic run at 4 cents. Guardrails now cover tool calls too, so an agent's tool input can be sanitized or its execution blocked.

### [42:31](https://youtu.be/nEW0kosJjc8?t=2551) Quarkus Flow persistence, MCP, and A2A

Quarkus Flow persists agentic workflows to a Kafka topic (and optionally a database), so human-in-the-loop pauses, pod crashes, and restarts resume instead of losing in-memory state. The talk also covers the stateless July MCP spec with auth in Quarkus MCP server 2.0 (claimed fastest behind Rust, ahead of it on latency, per a colleague's benchmark), multi-tenant A2A remote agents, and wrapping MCP tools as non-AI agents alongside LLM-backed ones.

### [47:17](https://youtu.be/nEW0kosJjc8?t=2837) Conclusion: Java as a first-class AI language

Fusco closes by arguing for strongly typed domain modeling over everything-as-a-string, and for keeping the framework open rather than opinionated: the decision-model pattern went from unknown to integrated within a day of release. References: the LangChain4j GitHub project, the agentic framework docs, and the Quarkus LangChain4j workshop. His book on the subject is due early next year.

## Tools, libraries and specs

- LangChain4j agentic module and `langchain4j-agentic-patterns` (pluggable planner, sequential/parallel/loop/conditional/supervisor/goal-oriented/blackboard/voting/decision-router patterns)
- Quarkus LangChain4j extension (Dev UI topology and execution views, `@ChatModelSupplier`, Langfuse extension)
- Quarkus Flow (workflow persistence to Kafka topic and database)
- Jev decision model (also tried: Leia, Kev)
- MCP spec with Quarkus MCP server 2.0; A2A with multi-tenancy
- LGTM stack (Loki, Grafana, Prometheus, Tempo), Langfuse, MicroProfile Fault Tolerance (`@Retry`, `@Fallback`)

## Who should watch

Java developers building or evaluating multi-agent systems on LangChain4j and Quarkus gain the most, especially anyone who outgrew the fixed patterns from last year. Viewers wanting reusable non-Java agent theory or measured production results can skip it; the patterns are framework-specific and the numbers stay at demo scale.

## Verdict

**8/10**: The framework author explains the new planner design with a live end-to-end demo and points to a workshop and docs covering it, but the measurements stay at demo scale and the patterns are not compared in the talk.

**Novelty 2/2**

- **+** [06:51](https://youtu.be/nEW0kosJjc8?t=411) Fusco says why the planner became pluggable: feedback after last year's session showed everybody has their own coordination need, so he reworked the fixed patterns onto a planner interface that mixes with them.
- **+** [32:42](https://youtu.be/nEW0kosJjc8?t=1962) Decision-model support was added to LangChain4j the Friday before the talk for a model released one or two weeks earlier, and the routing semantics (one choice question, or one yes/no per agent against a threshold) are shown on screen.

**Demonstrated 2/2**

- **+** [23:40](https://youtu.be/nEW0kosJjc8?t=1420) The voting-pattern pipeline runs live: a story is generated, scored by three parallel critics, and revised until it clears the bar.
- **+** [27:26](https://youtu.be/nEW0kosJjc8?t=1646) The execution view shows the loop iterating three times, with per-agent durations, token counts, inputs, and outputs visible.
- **−** [34:15](https://youtu.be/nEW0kosJjc8?t=2055) The Jev routing planner is shown as code and screenshots, and the blackboard result at [20:00](https://youtu.be/nEW0kosJjc8?t=1200) as a screenshot; neither is run.

**Measured 1/2**

- **+** [27:56](https://youtu.be/nEW0kosJjc8?t=1676) The execution view reports per-invocation durations and token counts for the demo run, with no baseline to compare against.
- **+** [40:58](https://youtu.be/nEW0kosJjc8?t=2458) The Langfuse dashboard prices one agentic run at 4 cents.
- **−** [44:07](https://youtu.be/nEW0kosJjc8?t=2647) The Quarkus MCP server is claimed fastest behind Rust and ahead of it on latency on a colleague's say-so, with no benchmark numbers or setup shown.

**Depth 1/2**

- **+** [09:32](https://youtu.be/nEW0kosJjc8?t=572) The sequential planner is rebuilt method by method on the new interface, and the goal-oriented graph's loop-free limit is worked through to the nested-loop fix at [13:43](https://youtu.be/nEW0kosJjc8?t=823).
- **+** [30:37](https://youtu.be/nEW0kosJjc8?t=1837) The model-selection strategy is reasoned through: cheap model while far from the quality bar, stronger model when close, with the thresholds stated.
- **−** [16:51](https://youtu.be/nEW0kosJjc8?t=1011) The table of pros, cons and best-for per pattern is left as a reference ("I don't want to go through this table"), so the talk never weighs the patterns against each other.

**Reusable 2/2**

- **+** [50:55](https://youtu.be/nEW0kosJjc8?t=3055) The Quarkus LangChain4j workshop linked at the close runs from one AI service through the agentic patterns to the enterprise features the talk covers.
- **+** [50:24](https://youtu.be/nEW0kosJjc8?t=3024) The LangChain4j repository and agentic framework docs cover the planner API and patterns shown on screen.
- **·** [50:24](https://youtu.be/nEW0kosJjc8?t=3024) The voting and model-selection demo code is not among the references.
