---
title: "From vibe coding to harness engineering: modernizing a regulated environment with AI"
talkId: "16414"
conference: devoxx-be-2026
speakers: [Anyul Rivas]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=zEUSFvDOiCo
durationMin: 41
slides: null
verdict: 6
frames: 14
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# From vibe coding to harness engineering: modernizing a regulated environment with AI

Anyul Rivas · Conference · Agentic Engineering & Tooling

## TL;DR

A bank mainframe modernization started with vibe coding to reach a demo fast, then switched tracks to harness engineering: deterministic checks that force stochastic agent output through the bank's rules. The thesis is that vibe coding accelerates idea-to-demo, but only a harness of builds, tests, and gates carries AI-generated code to production in a regulated environment.

## Key takeaways

- Vibe code the prototype, then switch tracks: reach the demo fast to kill requirements uncertainty, then rebuild the path to production with engineering gates instead of vibe coding all the way there.
- Review the plan, not the diff: a 300-line implementation plan is cheaper to verify than 5,000 unreviewed lines, so force spec-first development with human approval before execution.
- Put constraints in the build, not the prompt: agents forget documented rules (they kept downgrading Java 25 to 17), so Maven Enforcer, OpenRewrite recipes, and ArchUnit tests reject invalid output deterministically.
- Run one orchestrator with narrow disposable subagents: a simulated IT department of frontend, backend, DevOps, and QA subagents burned tokens on agent-to-agent chatter and handoff loss.
- Write agent instructions as positive examples of what to do rather than prohibitions; negative rules underperform, a finding backed by an Anthropic study.
- Cap agent scope explicitly (no unsolicited improvements, stop at acceptance, never rescan unchanged code) once token bills bite: three engineers were consuming 30% of the company's monthly quota.

## Notes

### [00:34](https://youtu.be/zEUSFvDOiCo?t=34) The assignment and its constraints

Rivas, senior solution architect at GFT Technologies, and two fellow architects had to modernize a COBOL mainframe bank application: extract account-opening and fund-investment events via change data capture into Kafka, consumed by Java and C# microservices behind a Kafka client SDK using the outbox pattern, dead-letter queues, and resiliency patterns. The target ran on Azure DevOps, Kafka, OpenShift, and Helm charts. Bank rules allowed only Artifactory dependencies, forbade external images, skills, MCP servers, and subagents, and initially banned any AI trace in the repo; GitHub Copilot was permitted later. Bureaucracy shrank a 3-month plan to little over a month for the proof of concept.

### [05:20](https://youtu.be/zEUSFvDOiCo?t=320) Chapter 1: vibe coding to the demo

The team vibe coded a working demo: 25K commits, 3,500 auto-merged pull requests, and 180,000 generated lines. Rivas compares it to Limitless: a genuine boost for exploring possibilities and getting client feedback, but a starting point, not a delivery strategy.

### [06:53](https://youtu.be/zEUSFvDOiCo?t=413) From vague stories to implementation-ready specs

The bank's stories invited hallucination; one shown verbatim read "As a consumer, I need to process account events using the standard SDK" with acceptance criteria "Events are consumed correctly. Errors are handled." A "Grill Me" skill interrogated each story into an implementation-ready spec covering edge cases, bank constraints, and acceptance evidence telling the model when to stop. Approving that plan before execution kept humans accountable for architectural trade-offs.

### [10:01](https://youtu.be/zEUSFvDOiCo?t=601) Research-Plan-Implement-Sync workflow

Refused spec-driven tools that store ADRs in the repo (the bank keeps docs in Confluence), the team built its own loop: read the grilled spec, plan against Confluence documentation, execute after human approval with validation scripts for fast feedback, then sync results back by posting to Azure DevOps and updating ADRs and diagrams externally. The dual track (prototype, then hardened production path) cut the distance from requirements to demo while keeping the discardable code discardable.

### [14:11](https://youtu.be/zEUSFvDOiCo?t=851) Tactical versus strategic programming

Borrowing Ousterhout's split, Rivas argues plausible output is not correct output: agents know standard patterns but not the bank's business semantics, edge cases, or definition of done. Agents don't know what good looks like; judging that is the human's job.

### [16:19](https://youtu.be/zEUSFvDOiCo?t=979) Chapter 2: the harness

The Apollo 13 CO2-adapter scene frames the core idea: engineering now means adapting stochastic model output into the deterministic rule set of production. A harness wraps the stochastic system and rejects invalid output rather than pretending the model itself is deterministic.

### [19:59](https://youtu.be/zEUSFvDOiCo?t=1199) Harness lessons: builds, tokens, tests

Early models with pre-Java-25 cutoffs kept downgrading the project to Java 17, so Maven Enforcer fails the build on version drift, banned dependencies, and wrong group/artifact patterns: don't document a constraint the build can enforce. Token pressure (30% of company quota) brought context engineering: a CLI proxy for bash output saving 60-80% of tokens, archived ADRs, trimmed AGENTS.md files, pruned skills, fresh sessions per task at 70% utilization, and optionally loaded skill packages. With only two mainframe builds a day, heavy upfront planning paid off. Further guards: a duplication threshold in the build that orders the agent to refactor copy-pasted microservice code, OpenRewrite recipes (Mockito, AssertJ, Testcontainers, Maven, Java API idioms), and ArchUnit plus ArchUnit.NET layer checks that run as fast unit tests with actionable messages.

### [27:14](https://youtu.be/zEUSFvDOiCo?t=1634) Anti-patterns: subagent teams and naive TDD

Simulating a full IT department of subagents failed: it anthropomorphizes a human process onto a compute system, repeating handoff loss while tokens go to inter-agent chatter. One orchestrator plus narrow disposable reviewers works; agent swarms are an anti-pattern. Likewise, asking for TDD produced horizontal slicing (all repository tests, then all service tests) and tests encoding the same misunderstanding as the implementation. The team used outside-in TDD with broad planning, bounded execution, and fast deterministic feedback.

### [30:53](https://youtu.be/zEUSFvDOiCo?t=1853) Working around the constraints

Denied MCP access to Confluence and Azure DevOps, the team kept a resource-list file of CLI calls with a private token and pasted query results into each plan for review. For Docker Compose end-to-end tests needing Rosetta for SQL Server on Macs, per-environment provisioning scripts with health checks and actionable errors replaced repeated agent fumbling.

### [33:28](https://youtu.be/zEUSFvDOiCo?t=2008) Clean code and landing in production

An unnamed study of 650 Claude Code trials, relayed without a source, found clean code doesn't change pass rates but cuts token use 7-8% and file revisitation 34%. The harness shipped; the demo reached production safely.

### [34:30](https://youtu.be/zEUSFvDOiCo?t=2070) Chapter 3: the engineer's new role

The Matrix metaphor: engineers now operate outside the system, supplying judgment, architecture, constraints, orchestration, environments, and tooling (filesystem access, Maven, tests, Git standards). Agents own the tactical horizon (green builds, fixed tests, compiler errors); humans own strategy (boundaries, dependency drift, future complexity, architectural intent). Without entry points and stop conditions, agents go rogue like Agent Smith.

### [38:09](https://youtu.be/zEUSFvDOiCo?t=2289) AI Harness Scorecard and Q&A

The team is building an AI Harness Scorecard script that grades a repo on five pillars (architectural documentation, mechanical constraints, testing and stability, review and risk prevention, AI-specific safeguards) with deterministic checks; the closing slide links its repository. In Q&A, Rivas said the production rollout grew from the 3 architect-prototypers to over 100 bank developers consuming the SDK.

## Tools, libraries and specs

- Kafka, Debezium (change data capture), Azure DevOps, OpenShift, Helm charts, SQL Server, Docker Compose
- Java 25 and Java 17, C#, Maven Enforcer, OpenRewrite, ArchUnit and ArchUnit.NET, Mockito, AssertJ, Testcontainers
- GitHub Copilot, MCP servers (requested, refused), Confluence, "Grill Me" spec-refinement skill, Archify skill
- AI Harness Scorecard (github.com/anyulled/ai-harness-scorecard): repo grader over the talk's five safeguard pillars

## Who should watch

Engineers shipping AI-generated code under enterprise or regulatory constraints, and leads setting agent guardrails, get a field-tested playbook. Teams wanting live demos, measured benchmarks, or the scorecard's implementation should go to the repository instead; skeptics of AI-assisted development will find the production framing more useful than the film metaphors.

## Verdict

**6/10**: Field-tested harness playbook from a bank mainframe migration, limited by nothing shown running, unsourced numbers and a linked repository that is a fork covering only the closing chapter.

**Novelty 2/2**

- **+** [19:59](https://youtu.be/zEUSFvDOiCo?t=1199) The agent that kept changing the project from Java 25 to Java 17 and the Maven Enforcer gate that replaced a prompt rule carry the "build, not prompt" lesson on the team's own production evidence.
- **+** [22:03](https://youtu.be/zEUSFvDOiCo?t=1323) The client architect's "you're consuming … 30% of the monthly quota of the whole company" is the trigger for the team's context-engineering and FinOps measures, first-hand bank experience no search result gives.
- **+** [27:45](https://youtu.be/zEUSFvDOiCo?t=1665) The failed subagent IT department, diagnosed as anthropomorphized handoffs burning tokens on inter-agent chatter, is first-hand experience against a popular trend.

**Demonstrated 0/2**

- **−** [10:01](https://youtu.be/zEUSFvDOiCo?t=601) The Research-Plan-Implement-Sync workflow appears only as a flow diagram; no agent run, plan or sync is shown.
- **−** [38:40](https://youtu.be/zEUSFvDOiCo?t=2320) The scorecard is described as "a script that you can run on your project" and QR-linked but never executed against any repository on screen.

**Measured 1/2**

- **+** [33:28](https://youtu.be/zEUSFvDOiCo?t=2008) The speaker relays a study of "650 Claude Code trials" (source unnamed on stage): clean code leaves the pass rate unchanged, cuts token use 7-8% and file revisitation 34%.
- **−** [05:51](https://youtu.be/zEUSFvDOiCo?t=351) The 25K commits, 3,500 auto-merged PRs and 180,000 lines are self-reported totals with no baseline or method.
- **−** [22:03](https://youtu.be/zEUSFvDOiCo?t=1323) The 30%-of-quota anecdote, the CLI proxy's 60-80% token saving and the output-token price ratio ("three to six times … three to eight times") come with no baseline or setup.

**Depth 2/2**

- **+** [19:28](https://youtu.be/zEUSFvDOiCo?t=1168) The harness gets a mental model: an envelope that validates stochastic output and rejects the invalid, not a deterministic model.
- **+** [25:11](https://youtu.be/zEUSFvDOiCo?t=1511) The duplication threshold in the build, with an explicit message telling the agent to refactor, replaces a prompt instruction that the agent ignored when copy-pasting across microservices.
- **+** [29:21](https://youtu.be/zEUSFvDOiCo?t=1761) Agent TDD is dissected into horizontal versus vertical slicing and the same-agent shared-misunderstanding trap, then replaced with outside-in TDD for a stated reason.

**Reusable 1/2**

- **+** [26:12](https://youtu.be/zEUSFvDOiCo?t=1572) The OpenRewrite recipe areas (Mockito, AssertJ, Testcontainers, Maven, Java API idioms), ArchUnit and Maven Enforcer are named precisely enough for a team to rebuild the same guardrails.
- **−** [38:40](https://youtu.be/zEUSFvDOiCo?t=2320) The linked AI Harness Scorecard is a fork of markmishaev76/ai-harness-scorecard that covers the extra chapter's five pillars, not the workflow, spec hardening or context engineering that make up the talk's main content.
- **·** [32:27](https://youtu.be/zEUSFvDOiCo?t=1947) The team's validation scripts, per-environment provisioning profiles and Confluence resource list are described on stage but unpublished, as internal bank tooling would be.
