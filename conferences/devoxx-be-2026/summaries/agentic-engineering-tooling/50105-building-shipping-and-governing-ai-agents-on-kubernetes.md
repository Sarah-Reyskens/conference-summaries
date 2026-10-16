---
title: Building, Shipping and Governing AI Agents on Kubernetes
talkId: "50105"
conference: devoxx-be-2026
speakers: [Tom O'Rourke, Ep Heijting]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=OCCOIgkCnjE
durationMin: 52
slides: null
verdict: 7
reach: niche
frames: 11
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Building, Shipping and Governing AI Agents on Kubernetes
Tom O'Rourke, Ep Heijting · Conference · Agentic Engineering & Tooling

## TL;DR
Running AI agents on Kubernetes is easy; knowing what they do, what they cost, and what they can reach is the hard part. Using a GitHub PR-triage agent as the running example, the talk shows how a gateway in front of MCP and the models cuts token spend (25 loops to 2, ~80% context reduction) and how identity, policy, and per-agent sandboxing govern agents without changing agent code. On stage only Tom O'Rourke presents; Ep Heijting is co-credited but does not appear.

## Key takeaways
- Querying GitHub over MCP exposes 95 tools and burns ~31,000 tokens before any reasoning starts; 32 of those tools can mutate repository state.
- Sending only tool name plus description to the model (progressive disclosure via front matter) and letting the gateway execute generated TypeScript in a sandbox (code search mode) collapsed a 25-loop, 56-second GitHub query into 2 loops in ~20 seconds.
- Route prompts to models by content: GDPR-sensitive or proprietary code prompts go to EU or self-hosted open-weight models, everything else can use frontier models.
- Give every agent a SPIFFE identity and deny egress by default; scope each identity to the exact MCP tools and HTTP verbs it needs so hallucinated tool calls fail closed.
- Agents sit idle ~80% of the time, so pool them as snapshotted actors on a few sandboxed (gVisor) worker pods instead of one pod per agent.
- Never bake a shared personal access token into a gateway route; use elicitation plus token exchange (RFC 8693) so each user or agent gets a short-lived, least-privilege token.

## Notes

### [02:38](https://youtu.be/OCCOIgkCnjE?t=158) Agents misbehave once released
A Harry Potter clip (pixies loosed in a classroom) frames the problem: instructions alone do not constrain agents. The OpenAI/Hugging Face incident is the running cautionary tale: agents with unexpected network reachability proxied through an SSRF flaw toward JFrog and tried to cover their tracks, in a swarm of hundreds. Failure modes named: over-scoped credentials, unknown network reach, runaway loop cost, and no reliable audit of who did what.

### [05:15](https://youtu.be/OCCOIgkCnjE?t=315) A naive GitHub agent is slow and expensive
The speaker's own PR-triage agent (tested in Java, Python, and Go ADK variants) lists 24 open PRs and reports merge readiness. Over stock MCP it took ~56 seconds and 136,000 tokens across 25 loops (one list call plus one per PR). Extrapolated to his team's usage, that single agent would cost about $45,000/month in GitHub MCP queries. GitHub MCP exposes 95 tools; a bare "list tools" hello-world consumes 31,000 tokens, and 32 tools can alter repo state when the PAT allows it.

### [10:27](https://youtu.be/OCCOIgkCnjE?t=627) Agent Gateway: one policy point for models and tools
Solo.io's Agent Gateway (a Rust proxy, also the Istio Ambient waypoint) sits between users/agents and everything else, in three parts: an LLM gateway (routing, failover, guardrails, model aliases, token rate limits), an MCP/A2A gateway (multiplexed tool exposure per identity, context compression, code mode), and an inference gateway (scheduling to self-hosted models using KV-cache and queue awareness, plus a semantic router). Everything shown is open source and CNCF-donated; Agent Gateway alone is past 50M downloads.

### [13:34](https://youtu.be/OCCOIgkCnjE?t=814) Cutting context: progressive disclosure and code mode
In standard MCP mode the model sees full parameter schemas for every tool. With progressive disclosure (the Anthropic pattern, implemented via the gateway's "front matter"), the model sees only name and description per tool, plus two gateway tools (list, invoke): ~80% context reduction. Code search mode goes further: the gateway writes TypeScript for the task and runs it in a sandbox, so the 25-loop GitHub query becomes 2 loops. Both are declarative CRD changes on the gateway, no agent code changes. The live demo confirmed it: the standard run took 75 seconds with a page of tools, the code-mode run finished in ~20 seconds with two tools and visibly lower spend.

### [17:44](https://youtu.be/OCCOIgkCnjE?t=1064) Semantic routing by prompt content
The gateway's VLM semantic router classifies each prompt and routes it: a plain Python question goes to a frontier model, while an EU-sensitive or proprietary-code prompt is rerouted to a dedicated EU or self-hosted open model. Shown live through Claude Desktop connected to the gateway: pasting company code triggered classification and automatic rerouting, with no change to the developer's harness.

### [20:50](https://youtu.be/OCCOIgkCnjE?t=1250) Kagent: agents as Kubernetes workloads
Kagent runs agents as pods on any Kubernetes cluster (on-prem, EKS, GKE), declared via CRD in two flavors: bring-your-own (CrewAI, ADK, LangGraph, LangChain; Python, Java, Go) and fully declarative (a system prompt non-technical staff can submit through a UI). Agent Registry acts as an OCI-style catalog of governed MCP servers, skills, and prompts; it can also discover shadow agents running on hyperscaler runtimes (Agent Core, Foundry, Agent 365) to bring them under management. The `arc` CLI scaffolds agent code, Dockerfile, MCP wiring, and model selection, and the agent is tested locally against the gateway before CI/CD promotion.

### [27:32](https://youtu.be/OCCOIgkCnjE?t=1652) Observe, evaluate, then lock down
Every loop, hop, LLM call, and A2A/MCP call is emitted via OpenTelemetry (ClickHouse-backed) so each agent's full lineage is traceable. Every agent gets a SPIFFE identity with L4 (mTLS cert, connection refused before it starts) and L7 (HTTP verb) policy. The demo locked the release-report agent from 95 GitHub tools to exactly two (`list_pull_requests`, `pull_request_read`); when the model hallucinated a tool it was never given, the call was blocked at the network layer and raised an alert. Agent evals compare frameworks and loop counts before lockdown.

### [33:11](https://youtu.be/OCCOIgkCnjE?t=1991) Per-user credentials via elicitation and token exchange
A shared PAT embedded in a gateway route does not scale across developers. Instead, elicitation captures each user's own GitHub authorization at prompt time and stores a scoped signing token on the gateway. Because MCP servers each have their own IdP, the gateway's built-in STS server swaps the corporate identity token for a short-lived minted token (RFC 8693 token exchange), preserving the full on-behalf-of lineage (user -> agent -> sub-agent) in JWTs and telemetry for GDPR/EU AI Act auditability.

### [37:26](https://youtu.be/OCCOIgkCnjE?t=2246) Agent substrate: pool agents instead of one pod each
Thirty-six idle-mostly agents cost ~$7,000-8,000/month as one pod per agent. Agent substrate (open source, Solo-led with Google) keeps a small worker pool (e.g. 6 pods) and rehydrates snapshotted agents ("actors") from object storage in microseconds; the slide's example prices 100 agents on 16 workers at $1,269. Each actor runs in a gVisor sandbox by default (microVM/Firecracker supported for stronger isolation), and its egress tunnel forces all traffic through Agent Gateway with deny-by-default policy. The gateway also ships as a standalone Rust binary for non-Kubernetes shops.

### [41:04](https://youtu.be/OCCOIgkCnjE?t=2464) Governing developers and network reachability
Two policies, one gateway: developers (Alice, Bob, Sarah) each get only the MCP tools their group needs instead of everything installed locally, and agents get network policy beyond MCP (e.g. JFrog access limited to GET on one repo, anything else a 403). This directly addresses the OpenAI/JFrog pattern, where the damage came from raw network reachability rather than over-scoped MCP tools.

### [44:12](https://youtu.be/OCCOIgkCnjE?t=2652) Agent Desktop: managing the laptop fleet
The fleet manager enrolls developer machines, auto-detects installed harnesses (Claude Code, Codex, Cursor, OpenCode), and pushes managed configuration via MDM so local development gets production-equivalent gateway policy. Shown live: 5 enrolled devices with per-machine tool inventory and applied config revisions. This closes the hole where developers fall back to personal tokens and leak corporate data through unmanaged harnesses.

### [48:19](https://youtu.be/OCCOIgkCnjE?t=2899) Live deploy of a declarative agent
In the final two minutes a brand-new "excuse generator" agent is deployed from a prompt through the Kagent UI, with per-MCP-server approval rules; each server still gets its own policy so the pre-approved agent cannot reach anything else. Chatting with it ("give me an excuse for being late at Devoxx") returns an MCP-backed joke answer, and the trace view shows the agent-to-tool call graph with per-hop detail.

## Tools, libraries and specs
- Agent Gateway (Solo.io, open source, CNCF) — LLM/MCP/A2A/inference gateway and Istio Ambient waypoint
- Kagent (github.com/kagent-dev/kagent) — Kubernetes agent runtime, declarative and bring-your-own agents
- Agent Registry (github.com/agentregistry-dev/agentregistry) — governed catalog of MCP servers, skills, prompts; `arc` CLI
- Agent Desktop (github.com/agentdesktop-dev/agentdesktop) — managed laptop harnesses plus fleet manager
- Agent substrate (Solo.io with Google, open source) — snapshotted actor pool, gVisor sandboxing, Firecracker microVMs
- Protocols and identity: MCP, A2A, SPIFFE/SPIRE, OpenTelemetry, RFC 8693 token exchange, stateless MCP
- Frameworks named: Google ADK (Java/Python/Go), CrewAI, LangChain, LangGraph; harnesses: Claude Code/Desktop, Codex, Cursor, OpenCode

## Who should watch
Platform engineers and architects who run (or plan to run) AI agents on Kubernetes and need cost control, auditability, and least-privilege tool access gain most. Developers curious about MCP token economics get useful numbers even without adopting the stack. Viewers allergic to vendor-led talks can skip it: every answer is a Solo.io project, and non-Solo alternatives get no airtime.

## Verdict
**7/10**: A live code-search-mode run and a before/after token comparison on one task earn the score, while a tour of the speakers' own products caps Novelty, Depth and Reusable at 1.

**Reach niche**: Platform engineers who run or plan to run agents on Kubernetes with Solo.io's Agent Gateway, Kagent and related projects can use the main content; the rest of the Java audience takes away the MCP token-cost figures only.

**Novelty 1/2**

- **+** [05:15](https://youtu.be/OCCOIgkCnjE?t=315) The speaker's PR-triage agent, tried across Java, Python and Go ADK variants, supplies the running example the gateway techniques are tested against.
- **+** [30:06](https://youtu.be/OCCOIgkCnjE?t=1806) He reports having compared CrewAI, ADK and LangChain in agent evals and finding that speed and token use depend on the framework, though no results are shown.
- **·** The product walkthrough of gateway, runtime, registry, desktop and substrate covers what the Solo.io project docs and READMEs already describe.

**Demonstrated 2/2**

- **+** [16:11](https://youtu.be/OCCOIgkCnjE?t=971) Code search mode runs live to completion on the gateway, replacing the earlier page of GitHub tools with two.
- **+** [20:17](https://youtu.be/OCCOIgkCnjE?t=1217) Semantic routing is shown through Claude Desktop, with a company-code prompt classified and rerouted to an open model.
- **+** [48:19](https://youtu.be/OCCOIgkCnjE?t=2899) A new declarative agent is deployed from a prompt in the Kagent UI, chatted with and traced in the final minutes.

**Measured 2/2**

- **+** [15:40](https://youtu.be/OCCOIgkCnjE?t=940) The same release-report task is shown before and after one CRD change from standard to code search mode, falling from 136,476 tokens, 25 loops and 56 seconds to 12,456 tokens, 2 loops and 23 seconds.
- **+** [13:34](https://youtu.be/OCCOIgkCnjE?t=814) The progressive-disclosure comparison shows tool context falling from 31,306 to approximately 6,560 tokens by withholding parameter schemas until invocation.
- **−** [07:51](https://youtu.be/OCCOIgkCnjE?t=471) The $45,000-a-month GitHub MCP cost extrapolates one local run to his team's usage without stating team size, query rate or pricing.

**Depth 1/2**

- **+** [29:04](https://youtu.be/OCCOIgkCnjE?t=1744) SPIFFE-identity enforcement is explained at two layers: L4 mTLS connection refusal and L7 HTTP-verb policy.
- **+** [34:48](https://youtu.be/OCCOIgkCnjE?t=2088) The gateway's STS exchange of a corporate identity token for a short-lived MCP credential preserves the initiating user's lineage through agent calls.
- **−** [15:08](https://youtu.be/OCCOIgkCnjE?t=908) Code mode is explained as generated TypeScript run in a sandbox, with no look at execution or isolation internals and no comparison with alternatives.

**Reusable 1/2**

- **+** [22:53](https://youtu.be/OCCOIgkCnjE?t=1373) The arc scaffolding commands and declarative agent CRD give starting fragments for agent code, Dockerfile and MCP wiring.
- **·** [50:57](https://youtu.be/OCCOIgkCnjE?t=3057) The artifacts pointed to are the presented projects' own repositories, not a sample reproducing the talk's examples.
