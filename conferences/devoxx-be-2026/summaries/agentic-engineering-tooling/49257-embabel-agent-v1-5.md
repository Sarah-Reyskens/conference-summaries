---
title: Embabel Agent v1.5
talkId: "49257"
conference: devoxx-be-2026
speakers: [Rod Johnson]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=DniA37kVfvI
durationMin: 51
slides: null
verdict: 7
reach: segment
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Embabel Agent v1.5
Rod Johnson · Conference · Agentic Engineering & Tooling

## TL;DR
Rod Johnson, creator of Spring and now of Embabel, presents the JVM-native agent framework that replaces LLM-driven orchestration with deterministic Goal-Oriented Action Planning over typed action steps. The talk walks through Embabel's programming model (goals, actions, preconditions, blackboard world state), a live code tour of a Sherlock Holmes RAG agent, and the framework's positions on agentic RAG, per-call model selection, agent skills, and code mode. It leaves JVM developers with a concrete alternative to prompt-and-tools spaghetti: decompose flows into typed steps, let a planner order them, and spend LLM calls only where code cannot do the job.

## Key takeaways
- Decompose every agent flow into typed steps that take domain objects in and return domain objects out, so each step is unit-testable and can use a smaller model or no model at all.
- Let a deterministic planner (GOAP), not the LLM, decide the order of steps: actions declare preconditions and expected postconditions, and the planner re-plans against blackboard world state after each action.
- Choose the model per AI call through named roles in configuration instead of using a frontier model everywhere; smaller steps make this possible and cheaper.
- Retrieval should be agentic, not a fixed pipeline: give the LLM vector, text, and chunk-expansion tools so it can search, evaluate results, and retry differently.
- Prefer code mode over long tool-call chains when the LLM must touch many objects: one sandboxed program beats a hundred round trips.
- Externalize prompts in Jinja templates and reuse prompt atoms via contributors rather than scattering long strings through code.

## Notes

### [00:33](https://youtu.be/DniA37kVfvI?t=33) What Embabel is and the 1.5 release stream
Embabel is an open source JVM agent framework sitting on Spring and Spring AI, though its programming model is independent enough that Quarkus support is in progress and LangChain4j can be used underneath. Two release streams exist: 1.0 targets Spring Boot 3.5 and Spring AI 1.0, while 1.5 targets Spring Boot 4 and Spring AI 2; new users should take 1.5, and code written against either stream does not break. Experimental features land in the core framework marked `@ApiStatus.Experimental` rather than in branches, with JEV model support given as a recent example. The framework is mostly Kotlin but kept idiomatic for Java callers, and the project reports over 4,500 stars, 67 contributors, and production use including a large bank's global payments AI.

### [09:28](https://youtu.be/DniA37kVfvI?t=568) Typed steps and goal-oriented action planning
The central argument: LLMs seduce developers into delegating whole flows to a model with tools, which ties the app to an expensive model and makes behavior unpredictable. Instead, decompose flows into steps and connect them with strongly typed objects rather than text. Steps written in code (API lookups, record assembly) cost effectively nothing and run instantly compared to LLM calls. A horoscope example shows the pattern:

```java
// reconstructed from speech at 14:10
Person extractPerson(UserInput input) { ... }              // LLM call: text to type
StarPerson enhance(Person person) { ... }                  // API call, no LLM
WriteUp summarize(StarPerson p, Horoscope h, News n) { ... } // @AchievesGoal LLM call
```

Ordering is the framework's job. Embabel uses Goal-Oriented Action Planning (GOAP), a non-LLM planning algorithm from 1950s AI popularized by games such as F.E.A.R.: each action declares preconditions (required world state) and expected postconditions (promises, verified after the run), and the planner finds a path from current blackboard state to an `@AchievesGoal` action. If no path exists it says so instead of hallucinating, and if a step fails (a birth date cannot be extracted) it re-plans, for instance by asking the user a question. State machines like LangGraph's are called out as brittle by comparison: adding states and handling deviating paths requires explicit rewiring.

### [21:23](https://youtu.be/DniA37kVfvI?t=1283) Code tour: the Sherlock Holmes case agent
The demo project (johnsonr's devoxx-demo repo) builds a Dr Watson agent doing retrieval-augmented generation over the full Sherlock Holmes corpus. An `@Agent` class holds `@Action` methods; Spring meta-annotations make it a regular Spring bean with injectable dependencies. Preconditions and postconditions are derived from method signatures: `gatherEvidence(UserInput question, Ai ai)` returning `Evidence` means "given user input, produce evidence", with the `Ai` gateway treated as infrastructure like a servlet request in Spring MVC. Domain facts travel as Java records (`Evidence`, `Reasoning`, `Conclusion`), with free text kept only where structure is impossible. The `Ai` interface is explicitly about AI, not just GenAI: every call selects a model, preferably via configured roles (`withLlmByRole`) rather than model names, so apps can be tested against different models and route simple steps to small or open-weights models for cost, data sovereignty, and energy reasons. A fluent prompt-runner API (`withDefaultLlm`, `withReference`, `creating(Evidence.class)`) builds typed LLM calls, with few-shot examples given as typed objects that survive refactoring.

### [34:33](https://youtu.be/DniA37kVfvI?t=2073) Agentic RAG: pipelines are the past
Classic RAG pipelines (chunk, embed, retrieve once, stuff into the prompt) suffer from chunking: meaning crosses chunk boundaries and no fixed chunk size fixes that. Embabel's agentic RAG instead hands the LLM search tools (vector search, full-text search, next/previous chunk expansion) so it reflects on poor results and retries with different queries. Configuration centers on a `SearchOperations` interface covering vector search, text search, chunk retrieval, and custom tools; shipped stores are Neo4j, PGVector, and Lucene (in-memory and on disk), with the demo running on Lucene. A `ToolishRag` instance (name, description, search operations) attaches to any LLM interaction via `withReference`, and multiple named RAG stores can coexist with disambiguated tools. The commercial product built on the framework is said to score exceptionally well on FinanceBench-style and legal RAG benchmarks, but no numbers are shown.

### [44:23](https://youtu.be/DniA37kVfvI?t=2663) Chat, skills, code mode, and what is next
Chat sessions are modeled as long-running agent processes: a `@Action(trigger = UserMessage.class)` method responds to user messages with the framework managing and persisting the conversation. Agent skills plug in through the same reference concept from classpath or GitHub, with progressive disclosure handled by the framework so the full skill text is not stuffed into the prompt. Code mode (LLMs generating one program instead of many tool calls, after a Cloudflare blog term) is presented as the future: experimental sandbox support with Docker execution lives in the embabel-agent-experimental repo. A closing rush names the `Ai` gateway's support for new model classes (JEV, decision models), flow persistence across restarts over JDBC and other backends, and the DICE (Domain Integrated Context Engineering) agent-memory project, with hub.embabel.com and the examples repos as starting points.

## Tools, libraries and specs
- Embabel Agent 1.5 (Spring Boot 4, Spring AI 2) and 1.0 stream (Spring Boot 3.5, Spring AI 1.0)
- LangChain4j (supported LLM backend)
- Jinja templates for prompt externalization
- Lucene, PGVector, Neo4j vector stores for RAG
- Spring Shell (`embabel agents` introspection), Spring MVC handler-method injection model
- embabel-agent-experimental repo (sandboxed code execution, extra tool integrations)
- DICE agent-memory project (github.com/embabel/dice)

## Who should watch
JVM developers building or evaluating AI agents, especially in Spring shops wrestling with brittle prompt-and-tools flows, will get the most from the planning model and the RAG treatment. Viewers wanting a from-zero tutorial should start with the Java template and examples repos instead; those after measured benchmark comparisons or a full live demo will find neither here.

## Verdict
**7/10**: Embabel's planning model is explained with working framework introspection and published examples, but the agent flow is not run end to end and performance claims lack measurements.

**Reach segment**: JVM developers adding LLM agent or RAG features to their applications within the next year.

**Novelty 1/2**

- **+** [07:22](https://youtu.be/DniA37kVfvI?t=442) The speaker reports that production adoption is concentrated in complex applications at large companies, including a bank's global-payments infrastructure.

**Demonstrated 1/2**

- **+** [22:10](https://youtu.be/DniA37kVfvI?t=1330) On screen, the running Spring Shell lists discovered agents, goals, actions, preconditions and postconditions.
- **−** [43:53](https://youtu.be/DniA37kVfvI?t=2633) The speaker says there is no time for a demo, so no agent run executes end to end with visible output.

**Measured 1/2**

- **+** [06:51](https://youtu.be/DniA37kVfvI?t=411) Adoption is quantified as over 4,500 stars and 67 contributors with production use.
- **−** [39:13](https://youtu.be/DniA37kVfvI?t=2353) Agentic RAG benchmarks on finance and legal sets are described only as exceptionally good, with no numbers, baseline or method and no public figures.

**Depth 2/2**

- **+** [18:19](https://youtu.be/DniA37kVfvI?t=1099) The planner assesses world state against a goal and re-plans after each action, with a blackboard retaining the flow's state.
- **+** [22:26](https://youtu.be/DniA37kVfvI?t=1346) Preconditions are mandatory while postconditions are promises requiring verification, explaining why world state must be reassessed after execution.
- **+** [28:45](https://youtu.be/DniA37kVfvI?t=1725) Per-call model selection through named roles is argued on cost, confidentiality, data sovereignty and energy grounds.

**Reusable 2/2**

- **+** [17:48](https://youtu.be/DniA37kVfvI?t=1068) The full horoscope flow lives in the agent examples repository for the audience to run.
- **+** [50:44](https://youtu.be/DniA37kVfvI?t=3044) As starting points covering the main content, the closing points to the agent examples repository and the Java template repository.
- **+** [49:09](https://youtu.be/DniA37kVfvI?t=2949) Built wholly on Embabel agentic RAG, the hub.embabel.com chatbot is open source as a reference application.
