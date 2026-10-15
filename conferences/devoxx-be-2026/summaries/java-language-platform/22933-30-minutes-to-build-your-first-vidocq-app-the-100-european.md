---
title: 30 minutes to build your first Vidocq app, the 100% European Sovereign Java stack with zero external dependencies
talkId: "22933"
conference: devoxx-be-2026
speakers: [Sebastien Blanc]
track: Java Language & Platform
sessionType: Tools-in-Action
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=U9pOWsERF6o
durationMin: 31
slides: null
verdict: 6
frames: 8
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# 30 minutes to build your first Vidocq app, the 100% European Sovereign Java stack with zero external dependencies

Sebastien Blanc · Tools-in-Action · Java Language & Platform

## TL;DR

Vidocq is a new open-source runtime implementing Jakarta EE Core Profile and MicroProfile in pure Java with zero external dependencies, originally grown out of an experiment in generating a CDI implementation from specs and TCKs with LLMs. Blanc builds a small waffle-shop application live on it: a REST endpoint, MicroProfile Config injection, a dev console, an order service, and OpenID Connect security backed by Rossignol, a from-scratch identity server written on Vidocq itself.

## Key takeaways

- Vidocq implements Jakarta EE Core Profile and MicroProfile as one component per spec (Vauban for CDI, Cassini for REST, Cyrano for REST client, Foy for Servlet, Mansart for Jakarta Data, Knock for Health, Grimm for OpenAPI, Cervantes for JWT), each a strict JPMS module with no third-party runtime libraries.
- LLM-assisted development works best against precise specs plus executable conformance tests: the Jakarta specs gave the model the what, the TCKs gave it a pass/fail signal, which is how the project grew to 300,000 lines and 19 components in a few months.
- Developer experience mirrors Quarkus and Spring: `mvn clean compile voc` starts dev mode with fast restarts, live reload, a dev console (startup report, REST listing, config, logs, JVM state), a `voc` CLI with extension management, and dev-services-style database provisioning.
- Security follows the familiar MicroProfile JWT plus OpenID Connect pattern: issuer, public-key location and audience in `vidocq.properties`, `@RolesAllowed("customer")` on the resource, and the caller identity read from `SecurityContext` as a `JsonWebToken`.
- The project ships a project-local agent skill (`skills/vidocq/SKILL.md`) so coding agents extend a Vidocq backend using its CDI, REST, JSON, config and authorization conventions without adding runtime dependencies.

## Notes

### [04:12](https://youtu.be/U9pOWsERF6o?t=252) What Vidocq is and where it came from

The project started as an experiment at a French unconference: LLMs perform well when given precise specs, and Jakarta EE has extensive specs plus TCKs that give executable pass/fail feedback. The first target was a dependency-free CDI implementation using only the JDK; that worked, so the scope grew to all of Jakarta EE Core Profile and MicroProfile. A companion three-hour deep dive the previous day covered the runtime in depth. Blanc frames the result as a sovereign European Java stack: independent of any third-party library, open source, and welcoming contributors.

### [05:49](https://youtu.be/U9pOWsERF6o?t=349) The 19 components

Each Vidocq module targets one spec and carries a French name: Vauban (CDI 4.1 Lite), Chappe (HTTP transport), Champollion (JSON-P/JSON-B), Cassini (REST 4.0), Cyrano (REST client 4.0), Foy (Servlet 6.1, in progress), Mansart (Jakarta Data 1.0, Transactions, JDBC pool), Heisenberg (Fault Tolerance), Humboldt (Telemetry), Knock (Health), Grimm (OpenAPI), Cervantes (JWT), Dirac (Metrics), Ravel (Config), plus the Vidocq runtime orchestrator and an unreleased sixteenth project, Erasmus. Everything is strict JPMS modules, no automatic modules. The count moves fast: 15 that morning, 19 by stage time. Jakarta Concurrency was being live-implemented in the deep dive and is nearly another component.

### [07:56](https://youtu.be/U9pOWsERF6o?t=476) Scaffolding GaufreStack

Blanc scaffolds a fresh app (pom pre-filled to skip typing) with dependencies on the Knock, Grimm and Cervantes extensions plus the Vidocq core, an empty application class, and a `module-info.java`. `mvn clean compile voc` starts dev mode with a fast boot and file watching. The frame at 09:00 shows the generated pom: `io.vidocq.runtime` group, per-extension artifacts (knock-health, grimm-openapi, cervantes-jwt, cassini-rest), snapshot repository configuration.

### [10:01](https://youtu.be/U9pOWsERF6o?t=601) First REST endpoint and live reload

A `MenuResource` class annotated `@ApplicationScoped` and `@Path` with a `@GET` method returning "hello deovxx" (later "hello Devoxx") works on the first curl after a save, demonstrating live reload comparable to Quarkus and Spring. Adding a `@ConfigProperty`-injected `shop.name` from `vidocq.properties` ("GaufreStack") renders in the response on the next request.

### [13:09](https://youtu.be/U9pOWsERF6o?t=789) Dev console and CLI

The two-week-old dev console shows the startup report (boot phases in single-digit milliseconds, 15 ms for build), the exposed URLs, REST endpoints with a dashboard, health, configuration values, logs, and JVM state, refreshing every second. Dev services start provisioned infrastructure such as PostgreSQL when its JDBC driver is on the path, mirroring Quarkus dev services. A `voc` CLI with completion offers `info`, extension listing, and extension installation.

### [16:51](https://youtu.be/U9pOWsERF6o?t=1011) Menu JSON, orders service and order resource

The menu endpoint starts returning a JSON object with shop name, currency, and two waffle types. An `OrderService` holds orders in a `ConcurrentHashMap` with a `Waffle` record and static price lookup, and an `OrdersResource` exposes REST operations including a POST that accepts a JSON order and returns a placed order with an ID, verified with curl. At this point ordering is anonymous, which motivates the security segment.

### [21:06](https://youtu.be/U9pOWsERF6o?t=1266) Securing the app with Rossignol

Rather than Keycloak, Blanc secures the demo with Rossignol, a new OpenID Connect provider he vibe-coded under the constraint that it may only depend on Vidocq; named after the father of French cryptography, it supports the authorization flow, realms, key management and user creation, but is not production-ready yet. Configuration adds issuer, public-key location and audience; `module-info.java` gains the security module; `OrdersResource` gains `@RolesAllowed("customer")` and injects `SecurityContext` to record the order owner from the JWT subject.

### [25:46](https://youtu.be/U9pOWsERF6o?t=1546) 401, login flow, and the cut-short finale

Repeating the earlier curl now returns 401 Unauthorized. Logging in as Alice through the Rossignol redirect completes the authorization flow ("Authorization received"), and the secured order call succeeds. With two minutes left, Blanc opens OpenCode with a project-local Vidocq skill and prompts "Add a KitchenService that makes waffles"; the agent loads the skill and starts exploring the source tree, but time runs out before generated code appears. He closes by inviting questions and contributions.

## Tools, libraries and specs

- Vidocq 0.4.0-SNAPSHOT (Jakarta EE Core Profile and MicroProfile runtime, Java 25, zero external dependencies)
- Vidocq Maven plugin (`mvn clean compile voc`) and `voc` CLI
- Rossignol (OpenID Connect provider built on Vidocq, in development)
- MicroProfile Config (`@ConfigProperty`), MicroProfile JWT (`JsonWebToken`), Jakarta REST, Jakarta CDI, Jakarta Security (`@RolesAllowed`, `SecurityContext`)
- OpenCode with Claude Fable 5.1 and a project-local Vidocq SKILL.md

## Who should watch

Jakarta and MicroProfile developers curious about a new dependency-free runtime and its Quarkus-style developer experience gain the most, especially anyone interested in spec-driven LLM code generation. Skip it if you want Vidocq internals or benchmark data: that is the companion deep dive's job, and the security segment deliberately stays shallow.

## Verdict

**6/10**: A new dependency-free Jakarta EE runtime and its identity server shown working live from scaffold to secured endpoint, but much of the build matches the project's published getting-started, the numbers have no baseline, and no repository or site is pointed to.

**Novelty 1/2**

- **+** [04:12](https://youtu.be/U9pOWsERF6o?t=252) The origin experiment (Jakarta specs plus TCKs as an LLM pass/fail signal, from dependency-free CDI to the full Core Profile) is first-hand rationale from the project's side.
- **+** [21:06](https://youtu.be/U9pOWsERF6o?t=1266) Rossignol, the OpenID Connect provider vibe-coded on Vidocq alone, is new, in-development material shown running.
- **−** The scaffold, build and first REST endpoint ([07:56](https://youtu.be/U9pOWsERF6o?t=476)-[11:33](https://youtu.be/U9pOWsERF6o?t=693)) follow the Getting started page at doc.vidocq.dev, which a search for the subject returns first.

**Demonstrated 2/2**

- **+** [11:03](https://youtu.be/U9pOWsERF6o?t=663) The first curl against the live-reloaded endpoint returns the greeting on screen, and the injected shop name renders on the next request ([12:38](https://youtu.be/U9pOWsERF6o?t=758)).
- **+** [25:46](https://youtu.be/U9pOWsERF6o?t=1546) After `@RolesAllowed` is added, the same order curl returns 401, the Rossignol login completes with "Authorization received" ([26:47](https://youtu.be/U9pOWsERF6o?t=1607)), and the secured call returns the placed order ([27:49](https://youtu.be/U9pOWsERF6o?t=1669)).
- **−** [29:25](https://youtu.be/U9pOWsERF6o?t=1765) The OpenCode finale loads the Vidocq skill but time runs out before the KitchenService code appears.

**Measured 1/2**

- **+** [14:12](https://youtu.be/U9pOWsERF6o?t=852) The dev console startup report shows per-phase boot times in single-digit milliseconds (15 ms for build).
- **−** [04:44](https://youtu.be/U9pOWsERF6o?t=284) The 300,000 lines and 19 components are self-reported totals ("maybe this morning it was 15") with no baseline, and startup speed is never compared against another runtime.

**Depth 1/2**

- **+** [24:44](https://youtu.be/U9pOWsERF6o?t=1484) The security wiring is explained step by step: issuer, public-key location and audience in properties, the module requirement, `@RolesAllowed`, owner from the JWT subject.
- **−** [24:14](https://youtu.be/U9pOWsERF6o?t=1454) Configuration and security follow familiar OpenID Connect convention ("more or less the same"), and no alternative or trade-off is weighed.

**Reusable 1/2**

- **+** [20:34](https://youtu.be/U9pOWsERF6o?t=1234) The waffle-shop build (REST endpoint, config injection, menu JSON, order service and resource) is shown working on screen through curl, leaving the steps reconstructable.
- **−** [06:52](https://youtu.be/U9pOWsERF6o?t=412) "I will show you the website in a few moment" is never followed by a site, repository or sample URL.
- **−** [13:09](https://youtu.be/U9pOWsERF6o?t=789) The demo runs a 0.4.0-SNAPSHOT ("I'm using the snapshot"), so the build cannot be repeated on a release.
