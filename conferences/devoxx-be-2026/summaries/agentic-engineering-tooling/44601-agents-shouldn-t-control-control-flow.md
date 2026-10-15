---
title: Agents Shouldn't Control Control Flow
talkId: "44601"
conference: devoxx-be-2026
speakers: [Jeremy Adams]
track: Agentic Engineering & Tooling
sessionType: Lunch Talk
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=oey2TbFvfWE
durationMin: 40
slides: null
verdict: 7
frames: 8
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Agents Shouldn't Control Control Flow

Jeremy Adams · Lunch Talk · Agentic Engineering & Tooling

## TL;DR

Agents that pick their own tools every turn burn tokens, give inconsistent answers, and learn nothing from thousands of runs. Adams argues the fix is to watch what works, distill it into a context graph, and compile that graph into deterministic, governed code, leaving the LLM to summarize results instead of driving control flow.

## Key takeaways

- Agent telemetry (tool calls, commits, errors, traces) rots in storage unless something distills it into reusable artifacts; an agent without that loop is a brilliant hire reliving its first day forever.
- A naive memory store gets worse as it grows: semantic search retrieves lookalike memories (the V1 API answer after the V2 migration) and bad memories compound into future runs.
- Vectors lose provenance and structure, fine-tuning is expensive and opaque, and plain text does not scale; an explicit graph keeps entities, relations, and the agent run each memory came from.
- Once evals reveal a reliably successful path, pin it: run the same retrievals every time and hand the evidence to a small decision model instead of letting an LLM choose tools turn by turn.
- Treat the context graph as source code and the workflow as a build artifact: generate the code from the graph, gate deployment on drift, policy, and skill-version checks in CI, and require reviewed commits for changes.
- Version the interpretation guidance with the code: the team that owns each service should own the skill that tells the model how to read its results (AR aging, contract terms, CVE findings).

## Notes

### [02:37](https://youtu.be/oey2TbFvfWE?t=157) Agents forget everything

An agent that completed 10,000 tasks (refunds, tickets, PR reviews) knows nothing today it did not know yesterday unless something catches its learnings. Every tool call, git commit, and error is a signal about what worked, but most teams store telemetry and let it rot while generating billions of agent trajectories. The talk frames the question as what to distill experience into: code, skills, or training data, all traceable to the evidence behind them.

### [06:54](https://youtu.be/oey2TbFvfWE?t=414) Storing what agents learn

Four storage options get weighed. Plain text (markdown wikis, Obsidian vaults, Confluence) is cheap and readable but cannot serve the right chunk at the right time at volume. Vector embeddings scale retrieval but cause negative transfer: similar-but-wrong memories win, provenance is gone, and structure is lost. Training or fine-tuning a company model is expensive and opaque about how it got its answers. Knowledge graphs are explicit, inspectable, and changeable, with entities and relations visible.

### [09:30](https://youtu.be/oey2TbFvfWE?t=570) The context graph as organizational memory

Neo4j's context-graph pattern ingests agent conversations, extracts entities (people, orgs, technologies, teams), and links them into long-term memory, including the agent's own reasoning traces and tool calls back into that memory. Across many trajectories, patterns surface: a filter step followed by a search step predicts success, so it becomes a candidate for promotion into something deterministic. Graph data science adds cluster detection and hub identification (a search step many paths depend on deserves careful design). The graph doubles as a workbench for compiling skills, strict procedures, prompts, or training data.

### [14:14](https://youtu.be/oey2TbFvfWE?t=854) Demo 1: agent loop vs pinned queries

Same question on both sides: approve a $25,000 credit increase? The left side runs a classic LLM-plus-tools loop (Claude Sonnet, graph-backed tools for customer lookup, fraud patterns, precedents, policies). It makes five tool calls and ends unsure, roughly a conditional approval. Minutes earlier the same setup had said decline: choosing its own tools each turn yields different evidence and different verdicts. The right side skips the loop and runs ten fixed Cypher lookups known from evaluated successful runs (transaction summary, support tickets, alerts, precedents, policies, plus arithmetic in code for ratios), then feeds the evidence to Jev, a decision model that outputs yes, no, or escalate. Same evidence every run, typed verdict, lower cost and latency. The speaker's conclusion: smaller models match or beat large ones given the right context.

### [24:08](https://youtu.be/oey2TbFvfWE?t=1448) Demo 2: compiling a graph into a governed Java workflow

A Java project plus a Neo4j graph implement an AssessCustomerExposure operation over four vectors: contract obligations, outstanding invoices, service incidents, and production blast radius, each mapped to MCP tools owned by a team (SAP, Salesforce, PagerDuty, GitHub, Jira, Workday). A control panel compiles the graph into a deterministic Java workflow and runs CI-style gates: drift (code matches graph), policy (deployed identity holds required scopes), skills (guidance matches approved versions), and compilation. The first run reports about $9M at risk. Adding a security-risk edge (CVE findings via a security-list tool) trips a drift failure and a missing SecurityRead permission; the run is blocked until the permission is granted, reviewed, committed, and recompiled, after which the report gains a security exposure section (a critical payments-gateway vulnerability the customer does not know about). The LLM is used once, at the end, to write the human report from gathered data plus versioned team-owned skills.

### [38:48](https://youtu.be/oey2TbFvfWE?t=2328) The larger picture

The demos are one slice of an enterprise knowledge layer: ontologies, data, and memory (procedural skills plus the context graph) sitting under applications, agents, and tools. Closing line: once agents have shown how, get it into code so value compounds instead of burning tokens re-deriving the path every run.

## Tools, libraries and specs

- Neo4j (graph database) and Cypher (graph query language), backing the context graph and the pinned retrievals
- Claude Sonnet, driving the agent-tool-loop side of demo 1
- Jev (decision/classifier model, name as captioned), returning yes/no/escalate in demo 1
- MCP (Model Context Protocol) servers, the per-team tool boundary (SAP, Salesforce, PagerDuty, GitHub, Jira, Workday) in demo 2
- PagerDuty, Salesforce, SAP, Jira, GitHub: stubbed enterprise systems of record behind the demo tools

## Who should watch

Engineers building agent systems who feel the pain of inconsistent tool-loop behavior and want a concrete governed alternative, and anyone curious what a graph database vendor proposes as organizational memory. Viewers wanting a framework to download or production numbers from a real deployment should skip it: the compiler is an unpublished prototype and the evidence is demo runs.

## Verdict

**7/10**: Live demos carry the thesis from the memory problem to a governed compiler, but the cost and speed claims carry no numbers and nothing is published to reuse.

**Novelty 1/2**

- **+** [14:14](https://youtu.be/oey2TbFvfWE?t=854) The speaker runs a head-to-head on one credit question: an LLM choosing its own tools against pinned retrievals plus a decision model.
- **+** [29:25](https://youtu.be/oey2TbFvfWE?t=1765) Compiling the context graph into a Java workflow behind drift, policy and skill-version gates is the speaker's own prototype, not a tour of vendor documentation.
- **·** [09:30](https://youtu.be/oey2TbFvfWE?t=570) The context graph that ingests conversations, extracts entities and traces reasoning is Neo4j's existing pattern, presented as the company's approach.

**Demonstrated 2/2**

- **+** [17:20](https://youtu.be/oey2TbFvfWE?t=1040) The pinned-query side finishes on screen after ten Cypher lookups and returns a typed yes, no or escalate verdict from the decision model.
- **+** [32:30](https://youtu.be/oey2TbFvfWE?t=1950) After a security edge is added to the graph, the check shows a drift failure and a missing security-read permission.
- **+** [34:36](https://youtu.be/oey2TbFvfWE?t=2076) After the grant and a pre-flight check, the re-run adds the security-findings step and produces the exposure report with the payments-gateway vulnerability.

**Measured 1/2**

- **+** [15:47](https://youtu.be/oey2TbFvfWE?t=947) The agent loop shows "already five tool calls" against ten fixed Cypher lookups on the pinned side, a step count for each arm.
- **−** [18:24](https://youtu.be/oey2TbFvfWE?t=1104) "Way less cost, way less time, way less tokens" is claimed with no token counts, timings or stated method.
- **·** [21:03](https://youtu.be/oey2TbFvfWE?t=1263) The inconsistency claim rests on two earlier runs, "conditionally approve" and "decline", that were not shown on screen.

**Depth 2/2**

- **+** [05:15](https://youtu.be/oey2TbFvfWE?t=315) Negative transfer gets a mechanism: lookalike V1 API memories beat the right V2 memory under semantic search.
- **+** [07:26](https://youtu.be/oey2TbFvfWE?t=446) The vector-versus-graph trade-off is stated as lost provenance and structure against explicit, inspectable entities and relations.
- **+** [11:33](https://youtu.be/oey2TbFvfWE?t=693) A promotion rule is given: a filter-then-search path that succeeds across many runs becomes deterministic, and hub nodes get extra design care.

**Reusable 1/2**

- **+** [18:57](https://youtu.be/oey2TbFvfWE?t=1137) The Cypher query from person to accounts to flagged transactions is on screen, enough to reconstruct the retrieval pattern.
- **−** [27:51](https://youtu.be/oey2TbFvfWE?t=1671) No repository, sample project or checklist is published; the speaker has "not published a new framework yet".
