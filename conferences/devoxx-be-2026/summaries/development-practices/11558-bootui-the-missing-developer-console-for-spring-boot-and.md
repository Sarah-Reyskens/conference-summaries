---
title: BootUI, the missing developer console for Spring Boot and Quarkus
talkId: "11558"
conference: devoxx-be-2026
speakers: [Julien Dubois]
track: Development Practices
sessionType: Tools-in-Action
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=NkstzPeo400
durationMin: 30
slides: https://www.julien-dubois.com/conferences/bootui/index-en.html
verdict: 7
frames: 9
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# BootUI, the missing developer console for Spring Boot and Quarkus

Julien Dubois · Tools-in-Action · Development Practices

Slides: https://www.julien-dubois.com/conferences/bootui/index-en.html

## TL;DR

Julien Dubois, creator of JHipster, demos BootUI, his open-source developer console for Spring Boot and Quarkus that exposes a scorecard of 400+ diagnostic rules plus a live view of requests, SQL, transactions, exceptions and the JVM from a single added dependency. The session argues the real consumer is the AI coding agent, showing an MCP server, an agent skill and a CLI that let agents read runtime state, then previews unreleased V2 work: an event graph database with change-impact analysis and an optional bytecode-instrumentation agent.

## Key takeaways

- Drop one dependency into a Spring Boot or Quarkus app and a `/bootui` console appears with advisors and live runtime panels, no sidecar or configuration.
- Run the advisor scorecard first: 400+ rules name the issue, its location and the fix, which makes findings directly consumable by AI agents.
- Point a coding agent at the running app through the BootUI MCP server or skill instead of letting it guess runtime behavior from source alone.
- Gate CI builds on the scorecard and the CLI's severity counts: too many rollbacks or exceptions means the build does not ship.
- Tutorials that only read source code cannot see rollbacks, cache misses or slow queries; runtime capture is what closes that gap.
- Expect V2 to diff runs for agents ("19 changes since run 1") so a fix loop can verify the exception or rollback actually disappeared.

## Notes

### [01:05](https://youtu.be/NkstzPeo400?t=65) Why Java apps need a console

Dubois frames the problem from his JHipster years: developers cannot see inside a running app, so failed transactions, useless caches and broken ORM mappings stay mysterious. Spring Boot Actuator is too basic, and most tools read source code instead of observing the runtime, missing exceptions and rollbacks entirely.

### [02:09](https://youtu.be/NkstzPeo400?t=129) What BootUI is

Two halves: an advisor with 400+ rules, and a live console of panels over the running application. One shared engine sits behind three adapters (Spring MVC, Spring WebFlux, Quarkus) under a single Vue console. Setup is one dependency in Maven or Gradle, then open `/bootui`. The stated engineering philosophy: own the capture (a hand-written JDBC proxy, an in-house OpenTelemetry implementation) to avoid transitive dependencies, capture everything possible, and label confidence where correlation is uncertain.

### [04:44](https://youtu.be/NkstzPeo400?t=284) Scorecard demo

Running the scorecard on the sample app surfaces findings such as field-based injection (Spring prefers constructor injection) and Hibernate eager fetching that should be lazy. Each finding states the issue, the affected classes and a recommended fix. Dubois notes this issue-plus-location-plus-remediation shape is exactly what an agent needs to fix things autonomously.

### [06:48](https://youtu.be/NkstzPeo400?t=408) Live Activity dashboard

Clicking through the sample app builds a live graphical flow: requests hitting the cache, red rows for exceptions, tinted rows for slow calls. Opening a request reveals its HTTP call, Hibernate session, transaction and SQL with timings. The V2 build on stage shows more detail than the released V1.

### [08:54](https://youtu.be/NkstzPeo400?t=534) Runtime: the JVM half

Panels cover Micrometer metrics, live memory, thread dumps with blocked-thread stacks, the Spring Boot startup timeline, and a memory tuner that computes JVM flags for bare metal or Kubernetes from observed data. GraalVM readiness checks report what works and generate `reachability-metadata.json`, writable back into the project; CRaC support is offered as the alternative for fast startup.

### [10:59](https://youtu.be/NkstzPeo400?t=659) Application panels and database

Configuration (viewable and editable) and runtime log levels come from JHipster, plus a graphical Spring beans view. Database coverage spans server-level PostgreSQL/MySQL stats read straight from the server (sessions, statements, indexes), Spring transaction boundaries with nesting and rollbacks, and a SQL trace from the JDBC proxy that flags possible N+1 queries with execution detail. Flyway and Liquibase get control panels.

### [13:04](https://youtu.be/NkstzPeo400?t=784) Security and services

Security panels explain endpoint rules and stream authentication failures live. Services coverage includes REST clients (failed connections counted separately from error responses), Spring Retry and Resilience4j breakers, Spring AI and LangChain4j calls with full detail, plus cache, email (via a JavaMail proxy), and Kafka.

### [15:07](https://youtu.be/NkstzPeo400?t=907) Diagnostics

The in-house OpenTelemetry traces show where time went (waiting on the LLM, waiting on the database). The exceptions panel groups by fingerprint Sentry-style with Open/Acknowledged/Resolved states and regression detection. HTTP exchanges and an HTTP probe round out failure analysis. Dubois admits the panel count is getting beyond what a human tracks, which motivates the agent story.

### [17:43](https://youtu.be/NkstzPeo400?t=1063) Agents: MCP server, skill, CLI

Flipping on the MCP server lets a GitHub Copilot agent query transactions and correlate failures across panels, e.g. 28 transactions with 6 problematic, then drill into the SQL involved. A BootUI agent skill and a `bootui` CLI expose the same data; the CLI also suits CI gating on score, rollbacks or exception counts. The live skill invocation misfired on stage, so the CLI equivalent was shown from the terminal instead.

### [21:19](https://youtu.be/NkstzPeo400?t=1279) V2 preview: event graph and run diffing

V2 builds a graph database of runtime events, shown through change-impact analysis: a REST endpoint touches a table that another endpoint shares, so an agent sees side effects before editing. Run diffing ("19 changes since run 1") lets an agent verify a fix by re-running and checking the exception, rollback or missing index use is gone. New graph algorithms surface issues such as a held connection behind a response.

### [25:26](https://youtu.be/NkstzPeo400?t=1526) V2 preview: bytecode instrumentation agent

An optional Java agent instruments bytecode to see inside user code: executed code paths with timings, a code inventory, and external side effects (network calls, files, processes, environment variables). It costs roughly 5% overhead and stays off in production; the skill enables it only when a code-level issue needs it. The session closes with the one-dependency install, the Apache 2.0 repository at github.com/jdubois/boot-ui, and a pointer to the Thursday talk on the agent-driven build process.

## Tools, libraries and specs

- BootUI (github.com/jdubois/boot-ui, Apache 2.0, Maven Central): `bootui-spring-boot-starter` / `bootui-quarkus`, console at `/bootui`, JSON at `/bootui/api/**`
- Spring Boot 4 (servlet and WebFlux), Quarkus 3 LTS, Java 17
- JHipster (configuration and logger panels originated there)
- GitHub Copilot, MCP, BootUI agent skill (`gh skill install jdubois/boot-ui bootui`), `bootui` CLI
- Spring AI, LangChain4j, Micrometer, OpenTelemetry, Resilience4j, Spring Retry
- GraalVM (reachability metadata), CRaC, PostgreSQL, MySQL, Flyway, Liquibase, Apache Kafka

## Who should watch

Spring Boot or Quarkus developers who want runtime visibility beyond Actuator, and anyone wiring coding agents to live application state. Skip it if you already evaluated BootUI V1 and only want the V2 internals, since the agent internals get one fast pass rather than a deep treatment.

## Verdict

**7/10**: Live demos of an original tool and unreleased V2 work from its author, with a published repository; held back by V1 panels that Actuator-level docs already cover, a failed skill demo, one-line explanations of the internals and numbers without a baseline.

**Novelty 1/2**

- **+** [22:21](https://youtu.be/NkstzPeo400?t=1341) The V2 event graph with change impact, run diffing and the bytecode agent were shown from a development build made that morning (06:48), before release.
- **+** [03:40](https://youtu.be/NkstzPeo400?t=220) The author explains why he owns the capture: his own JDBC proxy and OpenTelemetry implementation instead of transitive dependencies.
- **−** The Micrometer metrics, thread dump, startup timeline and Flyway/Liquibase panels surface data that the Spring Boot Actuator reference documentation already covers.

**Demonstrated 2/2**

- **+** [04:44](https://youtu.be/NkstzPeo400?t=284) The advisor scorecard runs live on the sample app, starting from "0 of 9 advisors assessed", and surfaces findings with locations and fixes.
- **+** [18:16](https://youtu.be/NkstzPeo400?t=1096) A Copilot agent queries the MCP server live and reports which of the 28 transactions are problematic.
- **−** [19:48](https://youtu.be/NkstzPeo400?t=1188) The agent-skill invocation fails on stage and the speaker falls back to the CLI, which runs after a typo.

**Measured 1/2**

- **+** [02:09](https://youtu.be/NkstzPeo400?t=129) The deck gives exact scale figures (411 rules across 10 advisors, 60 panels in 9 groups) and defines the 0–100 score.
- **+** [07:20](https://youtu.be/NkstzPeo400?t=440) The live KPI strip states its base ("over 17 retained requests") beside p50/p95, error rate and cache hit ratio.
- **−** [27:31](https://youtu.be/NkstzPeo400?t=1651) The ~5% instrumentation overhead is an estimate ("maybe 5%") with no benchmark setup or before/after measurement behind it.

**Depth 1/2**

- **+** [03:40](https://youtu.be/NkstzPeo400?t=220) The own-the-capture philosophy is explained with reasons: no proxy libraries, fewer transitive dependencies, confidence labels where correlation is uncertain.
- **+** [22:53](https://youtu.be/NkstzPeo400?t=1373) The reason for the event graph is stated: it links an endpoint to the table it touches and to other endpoints that share it, so an agent sees side effects before editing.
- **−** [09:26](https://youtu.be/NkstzPeo400?t=566) The memory tuner's flag computation gets one sentence ("calculated straight from your data … probably very good") with no account of how the parameters are derived.

**Reusable 2/2**

- **+** [28:35](https://youtu.be/NkstzPeo400?t=1715) The talk points to the open-source repository (github.com/jdubois/boot-ui), which covers the product demoed.
- **+** [02:39](https://youtu.be/NkstzPeo400?t=159) The one-dependency install is concrete enough to reproduce on any Spring Boot or Quarkus app.
- **+** [20:18](https://youtu.be/NkstzPeo400?t=1218) The CLI gives a scriptable path for CI gating on score, rollbacks and exception counts.
