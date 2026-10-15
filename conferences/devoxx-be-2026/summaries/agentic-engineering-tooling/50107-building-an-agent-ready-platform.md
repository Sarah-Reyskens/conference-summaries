---
title: Building an Agent Ready Platform
talkId: "50107"
conference: devoxx-be-2026
speakers: [Timo Salm]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=q58Y2tyRdCE
durationMin: 49
slides: null
verdict: 6
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Building an Agent Ready Platform

Timo Salm · Conference · Agentic Engineering & Tooling

## TL;DR

Writing an agent with a framework like Spring AI is the easy part; running agents in production needs a platform that provides approved model access, agent identity, inherited guardrails and observability. The talk maps each of those platform capabilities and ends with the questions developers should put to their platform teams.

## Key takeaways

- Consume every model through one OpenAI-compatible gateway endpoint with virtual keys, so switching models is a platform configuration change instead of an application rewrite.
- Never wire agents straight to arbitrary public MCP servers; use an approved-tool catalog behind an MCP gateway that checks every call, because you cannot audit code you did not review and version drift against on-premise systems breaks tools.
- Replace broad service accounts with agent identity: the user signs in via SSO, the agent gets its own identity with tokens scoped to exactly the tools and privileges the task needs.
- Put guardrails in three layers: application code validates output and asks for human approval, the gateway enforces allowed tools plus data masking and prompt filters, and the runtime sandboxes the agent with denied-by-default network access.
- Treat cost as a first-class signal: trace every agent step with its token usage so each user interaction gets a price tag, then enforce per-team budgets on the platform.
- Automate patching end to end now, because frontier models find vulnerabilities and generate working exploits within hours of a CVE publication; manual release testing measured in weeks no longer fits.

## Notes

### [00:32](https://youtu.be/q58Y2tyRdCE?t=32) From Spring AI demos to the production gap

Timo Salm, a Broadcom solutions architect and Agentic AI Foundation ambassador, opens by distinguishing an agent (a reason-act-observe loop where the model calls tools until a goal is reached) from a plain AI application. Spring AI builds such agents with minimal code, and the Agentic AI Foundation (a Linux Foundation project hosting MCP from Anthropic, Agent-to-Agent from Google, and Agent Gateway from Solo.io) supplies open implementations of several platform capabilities the talk covers. A free hands-on Spring Academy course covers building agents; this session covers running them in production.

### [04:09](https://youtu.be/q58Y2tyRdCE?t=249) Why agents stall before production

Most organizations adopted AI before their platforms were ready, so developers face unanswered questions: which model is approved, how to reach on-premise models, where credentials live, how to add guardrails, and how to observe what agents do. Keys and provider SDKs baked into application code make switching providers expensive at the scale of hundreds of thousands of agents. The situation mirrors microservices on containers five to ten years ago, and a cited study says 90% of organizations already run a developer platform that now needs extending toward AI.

### [09:22](https://youtu.be/q58Y2tyRdCE?t=562) Lead time and the new security reality

Agile promised changes in production within hours, yet customers report four-week manual test gates and a fear of breaking things. That delay is now dangerous: since getting frontier-model code scanning this year, the Spring team went from about one published vulnerability per month across 50-plus projects to finding over 450 candidates since March, publishing 200-plus CVEs across four releases, while researchers submit roughly 40 possible vulnerabilities per month. Smaller models turn a fresh CVE plus its patch into a working exploit within hours, and AI makes chaining low-severity CVEs into critical attacks easy. A 1Password study found only 70 of 100 AI-generated security fixes fully correct, so human experts must validate fixes. The prescription is automated patching of the whole stack, automated tests, supported versions, and release exceptions that put vulnerability patches live in hours or days.

### [17:47](https://youtu.be/q58Y2tyRdCE?t=1067) Platform as a product

Platform teams should build for real use cases: GPU enablement or gateway projects started without knowing which models anyone needs cannot drive adoption, and developers will otherwise get a better experience in the public cloud. The recommendation runs both ways: platform teams should gather feedback from at least one or two use cases across roles (including data scientists), and developers with a use case should approach the platform team to validate it together.

### [21:26](https://youtu.be/q58Y2tyRdCE?t=1286) What developers need from the platform

Six needs structure the rest of the talk: model access through a single API with virtual tokens covering public and fine-tuned private models; tool access to approved, version-compatible MCP servers; ready components such as embedding models, vector stores, and chat-memory databases; authentication where the agent acts with the user's identity instead of a shared service account; a common, customizable guardrail set; and observability plus auditability of every action.

### [25:06](https://youtu.be/q58Y2tyRdCE?t=1506) One endpoint for models: the AI gateway

Without consolidation, every agent talks to different models, shadow AI spreads, keys and model names sit in code, and updates take weeks in many organizations. An AI gateway (usually OpenAI-compatible) fixes this: applications integrate once, authenticate with a virtual key, and the gateway handles provider protocol differences, per-request model routing, and central budgets. Switching from a public to a private model then needs no application restart. Agent Gateway from the Agentic AI Foundation is named as the full-featured open option alongside commercial offerings.

### [28:43](https://youtu.be/q58Y2tyRdCE?t=1723) Approved tools: MCP and the MCP gateway

MCP, the standard (framed as USB-C for AI) connecting models to tools, resources, and prompts, supports HTTP streaming (server-sent events is deprecated) and local stdio. Stdio servers on a developer machine risk full disk access, and Broadcom forbids local MCP servers entirely. The answer is an MCP gateway whose registry acts as a marketplace of approved servers: agents and coding assistants sign in with company SSO, the gateway exchanges tokens with downstream services, and every tool call gains authentication, tracing, observability, and audit data. Teams building custom MCP servers still benefit from putting them behind the gateway.

### [32:53](https://youtu.be/q58Y2tyRdCE?t=1973) Agent identity

A service account holding privileges for hundreds of attached tools cannot express accountability, loses track of which user a ticket or action belongs to, and turns prompt injection into broad compromise. The proposed flow has the user sign in with SSO, the agent receive its own derived identity with tokens scoped to the tools the task needs, and the gateway audit and further restrict each call. This remains an area where standards are still forming.

### [34:58](https://youtu.be/q58Y2tyRdCE?t=2098) Guardrails in three layers

Agents pursuing a goal can break out of their intended scope (the OpenAI/Hugging Face incident is cited), overreach privileges, leak user data to models, or burn money for hours; attaching many tools is itself expensive because tool metadata travels with every request. Hand-built checks exist, such as Spring AI's safeguard advisor with word whitelists and blacklists, but company-wide concerns should not be rebuilt per agent. The layering: application code validates structured output and uses human-in-the-loop approvals for actions; the gateway enforces the allowed-tool catalog, data masking, and prompt-injection filters (bought, not built, since a dedicated team must maintain them); the runtime isolates the agent in locked-down containers with deny-by-default network policies, which matters more as agent skills execute shell commands. A slide shows the MCP gateway checking every call against a per-agent catalog (find an order: read; issue a refund: write plus approval; delete customer data: blocked).

### [39:37](https://youtu.be/q58Y2tyRdCE?t=2377) Observability: traces, cost, audit

Owners need to know what an agent did, why, and what each user interaction cost; a Gartner study from June 2025 predicts over 40% of agentic AI projects cancelled by end of 2027 over cost, unclear value, or weak risk controls. An illustrated trace prices one customer conversation at 8.4 seconds and 4 cents, with a refund tool call denied by policy. Spring AI already emits token-usage metrics and traces through Micrometer, and OpenTelemetry (with an official Spring Boot starter since 4.1 and GenAI semantic conventions) lets platform teams combine gateway, tool, and application telemetry into views developers get without extra effort.

### [43:15](https://youtu.be/q58Y2tyRdCE?t=2595) The platform, the split, and what to ask

The closing diagram stacks six capabilities under agents and coding assistants: AI gateway, MCP gateway, marketplace (vector stores and memory), identity, guardrails, and observability, all on a container runtime with agent sandboxes. Developers keep prompts, tools and business logic, workflows, and evaluations; the platform owns model access and budgets, the tool catalog, stores and memory, identity, guardrails and sandboxes, traces, cost, and audit. Broadcom runs this internally with an MCP registry for Jira, Confluence, GitHub, and on-premise systems. Developers should ask their platform teams for the model endpoint plus a self-service model marketplace, the approved-tool catalog, AI components, agent identity, out-of-the-box guardrails and sandboxes, and cost management. The takeaway: writing the agent is the easy part, so ask for a platform that makes the safe way the easy way.

## Tools, libraries and specs

- Spring AI (safeguard advisor, Micrometer token-usage observations)
- Spring Boot 4.1 (official OpenTelemetry starter)
- Model Context Protocol (tools, resources, prompts; HTTP streaming transport)
- Agent Gateway (Agentic AI Foundation, contributed by Solo.io)
- Agent-to-Agent protocol (Agentic AI Foundation, contributed by Google)
- OpenTelemetry with GenAI semantic conventions
- Tanzu Platform (Broadcom container platform with locked-down runtime defaults)
- pgvector (PostgreSQL extension for vector storage)
- Spring Application Advisor (automated transitive dependency updates)
- Dependabot / Renovate (automated patching)

## Who should watch

Developers being asked to take agents from demo to production, and platform engineers deciding what to build first for AI workloads, gain a complete checklist of platform capabilities. Teams already running an AI gateway with an approved-tool registry in production can skip the architecture; viewers wanting Spring AI implementation code should pick the companion sessions instead.

## Verdict

**6/10**: A beginner platform blueprint with first-hand Spring CVE data and reasoned identity and guardrail layers; nothing runs on screen, the figures have no method, and no artifact is published.

**Novelty 1/2**

- **+** [12:00](https://youtu.be/q58Y2tyRdCE?t=720) Spring's own scan results (one vulnerability per month historically, over 450 candidates since March, 200-plus CVEs published in four releases) are first-hand vendor data no search result offers.
- **+** [45:19](https://youtu.be/q58Y2tyRdCE?t=2719) The Broadcom internal MCP registry for Jira, Confluence, GitHub, and on-premise systems grounds the gateway advice in the speaker's own organization.

**Demonstrated 1/2**

- **·** [03:39](https://youtu.be/q58Y2tyRdCE?t=219) The talk sets out to explain how to run agents in production through slides of platform layers and promises no demo, so there is nothing to run and the criterion is not applicable.

**Measured 1/2**

- **+** [12:00](https://youtu.be/q58Y2tyRdCE?t=720) The Spring vulnerability counts carry a baseline (one per month) against the post-scanning totals, backing the patch-faster claim.
- **−** [16:43](https://youtu.be/q58Y2tyRdCE?t=1003) The claim that only 70 of 100 AI-generated vulnerability fixes were correct is a third-party figure with no method shown.
- **−** [40:09](https://youtu.be/q58Y2tyRdCE?t=2409) The Gartner 40%-cancelled prediction is cited with a date but no method, and the per-interaction cost figures are labelled "Example numbers for illustration" on the slide.

**Depth 2/2**

- **+** [32:53](https://youtu.be/q58Y2tyRdCE?t=1973) The identity section explains why a service account for an agent with hundreds of tools fails (too many privileges, no control over what the agent does) before showing SSO-derived, tool-scoped tokens.
- **+** [37:35](https://youtu.be/q58Y2tyRdCE?t=2255) The three guardrail layers give each concern its owner with a reason: output validation in application code, masking and prompt filters bought centrally, and a network-isolated sandbox because agent skills can run bash scripts.
- **·** [27:41](https://youtu.be/q58Y2tyRdCE?t=1661) Gateway routing and protocol translation stay at the architecture-box level, which fits the beginner slot.

**Reusable 1/2**

- **+** [46:21](https://youtu.be/q58Y2tyRdCE?t=2781) The closing questions for platform teams (model endpoint, tool catalog, identity, guardrails, cost) reconstruct into a usable checklist.
- **−** [46:21](https://youtu.be/q58Y2tyRdCE?t=2781) No repository, configuration or checklist is published or linked; the named Spring Academy course covers building agents rather than this talk's platform content.
