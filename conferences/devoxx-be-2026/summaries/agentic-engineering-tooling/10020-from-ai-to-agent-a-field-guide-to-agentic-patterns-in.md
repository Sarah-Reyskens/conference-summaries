---
title: "From AI to Agent: A Field Guide to Agentic Patterns in LangChain4j"
talkId: "10020"
conference: devoxx-be-2026
speakers: [Loïc Magnette]
track: Agentic Engineering & Tooling
sessionType: Deep Dive
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=IXcQYp51PLM
durationMin: 144
slides: https://speakerdeck.com/magnette/devoxxbe-from-ai-to-agent-a-field-guide-to-agentic-patterns-in-langchain4j
verdict: 8
frames: 16
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# From AI to Agent: A Field Guide to Agentic Patterns in LangChain4j

Loïc Magnette · Deep Dive · Agentic Engineering & Tooling

Slides: https://speakerdeck.com/magnette/devoxxbe-from-ai-to-agent-a-field-guide-to-agentic-patterns-in-langchain4j

## TL;DR

The session grows a single LangChain4j `@Agent` into a multi-agent system live, covering fixed workflows (sequence, loop, parallel, routing) before moving to autonomous patterns (supervisor, goal-oriented planning, peer-to-peer, blackboard, voting, debate, BDI) and custom planners. Every pattern is demonstrated in a local-model demo app with its use cases and failure modes. The closing advice: start with workflows and only adopt the autonomy you can still debug.

## Key takeaways

- Fixed workflows solve most real cases: Magnette estimates roughly 90% of client agentic systems end up as workflows, so a supervisor is the wrong starting point.
- Shared state goes in the AgenticScope, and scope keys should be typed (`TypedKey` records) instead of strings once the system has any size, because string typos compile and fail only at runtime.
- Every autonomous pattern needs explicit bounds (max loop iterations, max sub-agent invocations, conflict strategies), otherwise cost and runaway execution are unbounded.
- The supervisor pattern demands a capable model: with Llama 3.2 small it never delegated and tried to do everything itself.
- Agents that return enums instead of free text make routing and voting strategies robust against casing and phrasing drift.
- Deterministic work belongs in non-AI agents (plain Java behind `@Agent`); calling an LLM for computation adds latency and failure for no benefit.
- An `AgentListener`/`AgentMonitor` with its HTML topology and timing report is presented as mandatory once a system passes roughly 10 agents.

## Notes

### [03:09](https://youtu.be/IXcQYp51PLM?t=189) LangChain4j basics: AI services, tools, guardrails

Magnette frames LangChain4j as "Hibernate for LLMs": a uniform integration layer over models. An `AiService` is a Java interface with `@SystemMessage`/`@UserMessage` prompts, built via the builder API. Demos show `@Tool`-annotated methods so the model can act, plus input guardrails (blocking prompt injection and off-topic input) and output guardrails (e.g. max length) with a retry configuration that re-asks the model up to N times before failing. Exceptions from guardrails are catchable in calling code.

### [10:26](https://youtu.be/IXcQYp51PLM?t=626) What counts as an agent

An agent is a service using an AI model to fulfil a goal, using tools (without tools a model cannot touch any system) and context (prompts, RAG). In LangChain4j this is one annotation plus a builder:

```java
// from published slides p.10-11
@Agent(description = "Turns a rambling message about the dog into a structured sitter card")
@UserMessage("Turn this message into a sitter card ... Message: {{message}}")
String card(@V("message") String message);

var clerk = AgenticServices.agentBuilder(SitterCardClerk.class)
    .chatModel(model)
    .name("SitterCardClerk")
    .outputKey("Notes")
    .build();
```

The description states what the agent can do; the `outputKey` names what it produces into shared state. Agentic features need the extra `langchain4j-agentic` dependency. All demos run on a local model (Gemma 4 for most of the session) with a dog-rescue narrative and no API keys.

### [13:33](https://youtu.be/IXcQYp51PLM?t=813) Shared state and planners

Multi-agent chatter becomes an N-to-N mess, so LangChain4j provides the AgenticScope: shared state every agent reads inputs from and writes outputs to. A `Planner` interface orchestrates agents with `init` (initial state), `firstAction` (where to start) and `nextAction` (called as the system evolves). Most planners are embedded and invisible. Following the Anthropic taxonomy, the talk splits patterns into deterministic workflows first and autonomous agentic patterns second.

### [16:41](https://youtu.be/IXcQYp51PLM?t=1001) Sequence workflow

`sequenceBuilder` with ordered sub-agents, an output key and a listener runs agents one after another; the live diagram shows scope entries accumulating per agent. Without a provided class the builder returns an untyped agent with no return-type guarantee. Use cases: pipelines and multi-step transformations. Cons: rigid order, wasted work when an early agent over-delivers, and failure propagation from the first bad answer to the end.

### [22:33](https://youtu.be/IXcQYp51PLM?t=1353) Loop workflow

A worker plus an evaluator agent iterate until an exit condition holds. Providing an interface yields a typed agent with real method signatures instead of map keys. The exit condition is a lambda on scope state (demo: feedback score above 0.8), with a max-iterations cap and a `testExitAtEndOfLoop` option to check after every agent rather than every round, saving latency. The demo loops a poster draft from 3/4 to an acceptable score. Cons: exit conditions are hard to calibrate, cost grows per iteration as scope/memory grows, and iteration cannot fix garbage input.

### [31:30](https://youtu.be/IXcQYp51PLM?t=1890) Parallel and parallel-mapper workflows

`parallelBuilder` runs independent agents concurrently on a provided executor; LangChain4j handles the threading. An `output` lambda can merge the parallel outputs into one answer, but it should stay plain Java: no LLM calls and no scope writes there. A parallel-mapper variant runs one agent over each item of an iterable from scope, shown finding eight lost ducklings. Cons: branches/items must be independent, concurrent writes to the same scope key lose data, the run waits for the slowest branch, and there is no shared chat memory.

### [42:33](https://youtu.be/IXcQYp51PLM?t=2553) Routing workflow

A classifier agent picks the expert branch (police, herding, speed in the rescue demo). Magnette recommends the classifier return an enum rather than a string to avoid case and phrasing mismatches. Use cases: expert, risk-based, and format/language routing. Cons: everything hinges on routing state, zero or multiple branches can match, and branch outputs may be incompatible.

### [48:52](https://youtu.be/IXcQYp51PLM?t=2932) Typed keys

String scope keys caused live demo failures from typos that compile fine. The fix is `TypedKey` records carrying the value type:

```java
// from published slides p.38
public record Checklist() implements TypedKey<String> {}
var list = AgenticServices.agentBuilder(FridgeChecklist.class)
    .chatModel(model)
    .name("FridgeChecklist")
    .outputKey(Checklist.class)
    .build();
```

### [51:30](https://youtu.be/IXcQYp51PLM?t=3090) Human in the loop

`humanInTheLoopBuilder` with input/output keys and a response provider (web listener in the demo, keyboard in a terminal) pauses execution for approve/reject. Positioned as required before sensitive external actions: the speaker does not want an unsupervised agent moving bank money.

### [54:07](https://youtu.be/IXcQYp51PLM?t=3247) Error handling and optional agents

Agents can be marked optional to skip on failure or on missing inputs (the missing-input use case was contributed from the audience by Mario Fusco). An error handler receives an attempt counter so code can retry transient failures (e.g. malformed JSON) up to a max and then either throw or land gracefully with `ErrorRecoveryResult`.

### [58:19](https://youtu.be/IXcQYp51PLM?t=3499) Non-AI agents

Any deterministic step should be plain Java behind `@Agent` with an output key, composed into the same builders indistinguishably from AI agents. The example extracts data with an AI agent then computes on it with code, which is faster and cannot hallucinate.

### [60:27](https://youtu.be/IXcQYp51PLM?t=3627) Observability: listeners and AgentMonitor

`AgentListener` hooks before/after agent invocation, tool execution, scope creation/destruction and suspension; multiple listeners can attach and propagate to sub-agents. `AgentMonitor` adds an HTML report generator showing the system topology plus per-step execution time, which the speaker calls essential past 10 to 20 agents and preferable to wiring Grafana for this purpose.

### [65:10](https://youtu.be/IXcQYp51PLM?t=3910) Dynamic model switching

The chat model can be a lambda over scope state, e.g. read a severity flag and pick a cheap model for near-done refinements versus a strong model for poor drafts, so not every step pays frontier-model cost.

### [69:50](https://youtu.be/IXcQYp51PLM?t=4190) Supervisor pattern

One chief agent picks which sub-agents to call with which inputs, inspects outputs, and decides whether more work is needed; a cap limits sub-agent invocations. Context strategies range from full history to per-agent summaries. The live run called three of four agents in about 24 seconds. Use cases: customer support and open-ended assistants. Cons: nondeterministic planning (same request, different paths), heavy dependence on supervisor model quality, cost, and safety exposure since the supervisor can invoke every tool of every sub-agent.

### [77:12](https://youtu.be/IXcQYp51PLM?t=4632) Goal-oriented planning

Each agent declares preconditions (required inputs) and postconditions (produced outputs), so the planner builds a dependency graph and walks the shortest path from initial scope to the goal output key. The path is fixed once chosen; different inputs take different paths. Cons: keys carry no semantic quality guarantees, shortest means fewest agents rather than cheapest or fastest, and there is no mid-run replanning.

### [84:02](https://youtu.be/IXcQYp51PLM?t=5042) Peer-to-peer

There is no chief: any agent whose required inputs are present in scope runs, scope updates trigger the next round, and matching agents run in parallel until the goal key appears or nothing changes. An agent re-runs only when its required inputs changed, preventing infinite self-loops. Good for collaborative research; risks are invocation explosions, concurrent write conflicts, and unpredictable cost.

### [90:15](https://youtu.be/IXcQYp51PLM?t=5415) Blackboard

Peer-to-peer plus a conflict-resolution strategy that picks exactly one agent when several match (classroom analogy: the teacher picks one raised hand). Strategies are user code: declaration order, named priority, or load balancing by invocation count. The strategy becomes the bottleneck, sequential execution is slower, and a stable state with no runnable agent does not guarantee an answer; the speaker's dry run ended exactly that way once.

### [94:58](https://youtu.be/IXcQYp51PLM?t=5698) Voting

Agents sharing one input each return a verdict (demo: lake-ice safety from depth data), then a strategy aggregates: majority, veto, or the demo's all-must-agree-safe rule. Enum outputs keep aggregation parseable. Cons: correlated errors when voters share a model, tools or context (four biased voters still agree), aggregation design, and higher cost without guaranteed quality gain.

### [100:39](https://youtu.be/IXcQYp51PLM?t=6039) Debate

At least two debaters plus a judge as final sub-agent. Each round, every debater sees the others' previous answers via a dedicated debate-context scope key and produces a new solution; a convergence strategy (the demo uses unanimity, "the Belgian solution") decides when to stop, with a max-rounds cap before the judge summarises or decides. Use cases: risk analysis, architecture decisions with persona agents (product owner, architect, developer, tester), investment analysis. Cons: high cost and latency, agreement is not truth, and convergence checks are hard to write.

### [107:26](https://youtu.be/IXcQYp51PLM?t=6446) Belief-Desire-Intention

Beliefs are current scope state; each desire has an activation precondition, a definition of done, and a priority; intentions are the agent lists that may fulfil a desire. The planner loops: find achievable desires, pick the highest priority, run its next intention, update state, re-check. Priority switching means the run can bounce between desires like "a headless chicken". The live graph shows a rescue desire preempting a squirrel chase mid-run. Cons: desires are hard to design, plans are predefined by listed intentions, and a hard high-priority desire can starve simple low-priority ones.

### [119:27](https://youtu.be/IXcQYp51PLM?t=7167) Custom planners

Implementing the `Planner` interface (`init`, `nextAction`) in plain Java yields bespoke patterns; the demo `NapSchedule` planner never calls the same puppy agent twice in a row. Workflows need the `langchain4j-agentic` dependency while the autonomous patterns (peer-to-peer, blackboard, BDI and others) need the separate `langchain4j-agentic-patterns` module. The speaker warns against putting an LLM inside a planner.

### [124:10](https://youtu.be/IXcQYp51PLM?t=7450) Combining patterns

Every composite (sequence, loop, supervisor) is itself an agent, so patterns nest freely: loops inside sequences, voting inside parallel mappers. The "Mega Mutt" and "Lake Party" demos chain several pattern types. An audience note: used with only non-AI agents, this is just a Java workflow orchestrator.

### [128:54](https://youtu.be/IXcQYp51PLM?t=7734) Where to start

The closing comparison table ranks workflows as high-control, low-cost, excellent auditability versus the supervisor's inverse, with goal-oriented, peer-to-peer and voting in the middle. The guidance is to start deterministic and climb only as far as the problem demands, ending on the deck's line: "the pattern you do not adopt is the one you do not have to debug".

### [132:02](https://youtu.be/IXcQYp51PLM?t=7922) Declarative API and pointers

Every builder has an annotation equivalent (`@SequenceAgent`, `@Loop`, `@SupervisorAgent`, `@PlannerAgent` with a planner supplier), colocating wiring with the agent class. Mentioned without demo: async agents, A2A protocol integration, and the new agent registry. The LangChain4j tutorial docs are recommended as the moving target's best reference.

### [140:30](https://youtu.be/IXcQYp51PLM?t=8430) Q&A: decision models and contributions

Mario Fusco (in the room) announced decision-model routing, integrated the week of the talk: a purpose-built small model returns either a single choice or per-agent probabilities, optionally with a threshold that fires multiple agents above it in parallel. He invited contributions of new planner implementations to the `langchain4j-agentic-patterns` module.

## Tools, libraries and specs

- LangChain4j (agentic modules: `langchain4j-agentic`, `langchain4j-agentic-patterns`), builder and declarative APIs
- Quarkus LangChain4j extension (called the most advanced framework integration; demos use only the vanilla API plus Quarkus live reload)
- Spring and LangChain4j CDI integrations (mentioned)
- Ollama with Gemma 4 and Llama 3.2 (local demo models)
- A2A agent protocol, agent registry, decision-model API (mentioned, not demoed)
- Timefold (mentioned for constraint solving beyond LLMs)

## Who should watch

Java developers who have shipped a basic LLM integration and now face multi-step orchestration will get the most: the pattern catalogue maps directly onto build decisions. LangChain4j users deciding between frameworks benefit from the Quarkus extension pointer. Skip if you want Python ecosystems, LangGraph comparisons, or production-war-story depth on cost and eval harnesses, which the session barely touches.

## Verdict

**8/10**: Every pattern runs on screen with its failure modes and the demo repository is public; the timings and client figures have no baseline or method, and the core mechanics match the LangChain4j tutorial.

**Novelty 1/2**

- **+** [128:54](https://youtu.be/IXcQYp51PLM?t=7734) Client work grounds the closing guidance: most client systems end as workflows, so start deterministic and climb only as far as the problem demands.
- **+** [74:36](https://youtu.be/IXcQYp51PLM?t=4476) The supervisor warning rests on the speaker's own negative result: with the smallest Llama 3.2 it never delegated and tried to do everything itself.
- **−** The builders and the pattern catalogue are what the LangChain4j tutorial's "Agents and Agentic AI" page already documents, as the speaker points out at the end.

**Demonstrated 2/2**

- **+** [28:52](https://youtu.be/IXcQYp51PLM?t=1732) Live on screen, the loop iterates a poster draft scoring 3/4 in scope until it passes the 0.8 exit threshold.
- **+** [72:28](https://youtu.be/IXcQYp51PLM?t=4348) The supervisor run completes in about 24 seconds having called three of four sub-agents on its own discretion, with the diagram and logs visible.
- **−** [119:27](https://youtu.be/IXcQYp51PLM?t=7167) The custom planner was loaded from a checked-out branch instead of coded live, though it then ran with its logs visible.

**Measured 1/2**

- **+** [41:32](https://youtu.be/IXcQYp51PLM?t=2492) The parallel-mapper batch over eight lost ducklings completes in about 30 seconds on the local model, timing visible in the run.
- **−** [72:28](https://youtu.be/IXcQYp51PLM?t=4348) No baseline run, comparison, or stated method stands behind the supervisor's 24 seconds or the parallel-mapper's 30 seconds.
- **−** [128:54](https://youtu.be/IXcQYp51PLM?t=7734) The client-workflows figure and the cost and latency warnings come from experience, with no production metrics or method shown.

**Depth 2/2**

- **+** [14:36](https://youtu.be/IXcQYp51PLM?t=876) Planner mechanics are explained before use: init for the initial scope, firstAction for the entry point, nextAction called as the system evolves.
- **+** [78:14](https://youtu.be/IXcQYp51PLM?t=4694) Goal-oriented planning is explained as a precondition/postcondition graph walk taking the shortest path, with the caveat that shortest means fewest agents rather than cheapest or fastest.
- **−** [99:37](https://youtu.be/IXcQYp51PLM?t=5977) The voting aggregation strategy is left at "start with something simple", with no worked comparison of strategies.

**Reusable 2/2**

- **+** [137:49](https://youtu.be/IXcQYp51PLM?t=8269) A QR code links to a GitHub repository holding the demo code for the patterns shown.
- **+** [09:54](https://youtu.be/IXcQYp51PLM?t=594) The demo application runs on a local model, so the repository can be tried without any token or API key.
- **−** [137:49](https://youtu.be/IXcQYp51PLM?t=8269) The declarative-API branch was not yet pushed at talk time.

