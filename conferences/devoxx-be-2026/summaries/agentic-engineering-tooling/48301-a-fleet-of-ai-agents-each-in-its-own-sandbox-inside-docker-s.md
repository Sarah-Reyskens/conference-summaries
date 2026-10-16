---
title: "A Fleet of AI Agents, Each in Its Own Sandbox: Inside Docker's Agentic Platform"
talkId: "48301"
conference: devoxx-be-2026
speakers: [Jean-Laurent de Morlhon]
track: Agentic Engineering & Tooling
sessionType: Keynote
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=mnoUXIT4nMY
durationMin: 21
slides: null
verdict: 5
reach: segment
frames: 8
summarizedAt: 2026-10-14
reviewedAt: 2026-10-15
---

# A Fleet of AI Agents, Each in Its Own Sandbox: Inside Docker's Agentic Platform

Jean-Laurent de Morlhon · Keynote · Agentic Engineering & Tooling

## TL;DR

Docker's answer to coding agents holding live credentials is one agent per hardware-isolated microVM sandbox, with filesystem mounts, network policy, and secret injection controlled from the host. The speaker walks through the local `sbx` CLI, shareable Docker kits configs, cloud sandboxes, and the internal "AI factory" Docker runs on top, where orchestrated agents design, implement in parallel, and review before a human merges.

## Key takeaways

- Run each coding agent in its own microVM sandbox so a compromised agent cannot reach host credentials or the full filesystem.
- Keep secrets on the host and inject them at the network boundary: the agent sees a dummy env value while the proxy substitutes the real key on outbound calls.
- Share agent setups as versioned config (Docker kits: Dockerfile plus sandbox policy in one OCI image) instead of per-machine hand configuration.
- Constrain MCP access per tool, not per server, distinguishing read actions from destructive ones.
- When agents work unattended, review artifacts (design docs, PRs) rather than transcripts, and put the most human time into the design phase.
## Notes

### [01:35](https://youtu.be/mnoUXIT4nMY?t=95) Agents need seatbelts

The speaker opens with his own mistake: handing a GitHub token with repository-delete scope to an agent and getting caught by his security team. Sandboxes are a seatbelt that catches the agent when it goes wrong. He poses four questions the platform answers: can you trust it, can you repeat it, can it run without you, and can you build your own.

### [03:37](https://youtu.be/mnoUXIT4nMY?t=217) Sandbox architecture and policy demo

Each sandbox is a microVM with its own kernel, memory, and CPU on Intel VT-x or AMD-V; fast boot allows 6 to 20 agents on one laptop. A filesystem manager mounts only chosen host directories, and a network proxy keeps credentials on the host, injecting real keys on outbound calls while the agent sees dummy values. A screenshot shows `sbx run` denying an agent's call to a blocked site; policies can be pushed company-wide.

### [09:16](https://youtu.be/mnoUXIT4nMY?t=556) Docker kits: shareable sandbox configs

Kits bundle a Dockerfile with a kit YAML (network rules, injected keys) into one OCI image under a single digest, so one address reproduces the setup. The format is an open spec less than a month old, which Docker is working to hand to the CNCF.

### [11:20](https://youtu.be/mnoUXIT4nMY?t=680) Cloud sandboxes and MCP gateway

The same `sbx` command targets the cloud, with `sbx move` to shift a local sandbox there under the same policies. An MCP gateway grants access per server and per tool. The web UI at agentic-platform.docker.com shows one sandbox on XL compute at $1.12/hr billed per second; signup offered $250 in credits.

### [14:26](https://youtu.be/mnoUXIT4nMY?t=866) The internal AI factory

Since February, Docker has run an opinionated internal product on the platform: design agents produce documents you iterate on, a PM-style agent writes tickets, and an orchestrator fans out to typically four or five implementers coding in parallel, each sandboxed. Review agents check PRs before a human gets a Slack ping to approve the merge. Artifacts sync to the phone's file share so unattended output stays visible.

### [20:02](https://youtu.be/mnoUXIT4nMY?t=1202) Try it

Three calls to action: `brew install docker/tap/sbx` (free, no Docker Desktop needed), cloud signup with credits, and a TypeScript SDK plus OpenAPI API at docs.docker.com/ai/sandboxes-api. Closing line on screen: "Solve safety first. Ship fastest."

## Tools, libraries and specs

- `sbx` CLI (`docker/tap/sbx`): runs agents in local or cloud sandboxes
- Docker kits: open spec bundling Dockerfile plus sandbox policy in one OCI image, heading to CNCF
- Docker cloud sandboxes: agentic-platform.docker.com, XL compute at $1.12/hr billed per second
- MCP gateway: per-server and per-tool access control for agents
- TypeScript SDK and OpenAPI API: docs.docker.com/ai/sandboxes-api
- Agents named as sandbox workloads: Claude Code, Hermes agent, Codex, Pi, OpenCode

## Who should watch

Engineers about to give coding agents real credentials or repository access, and platform teams standardizing agent setup across a company. Skip if you already run agents in disposable VMs or containers with egress filtering; the sandbox mechanics will be familiar and the factory portion is a product preview rather than a reusable guide.

## Verdict

**5/10**: A clear microVM and secret-injection rationale with a visible policy block and a free CLI and SDK, held back by a stored demo, unmeasured scale claims and an internal-only factory.

**Reach segment**: Java teams that let coding agents touch repositories or standardize agent setup across a company can apply the sandbox policies and shared kit configs in their own work within the next year.

**Novelty 1/2**

- **+** [14:26](https://youtu.be/mnoUXIT4nMY?t=866) The internal AI factory, running at Docker since February with design agents, parallel implementers and review agents before a human merge, is production experience no search result offers.
- **−** The sbx CLI, kits format and SDK walkthrough covers Docker's public product surface, documented at docs.docker.com/ai/sandboxes-api.

**Demonstrated 1/2**

- **+** [08:15](https://youtu.be/mnoUXIT4nMY?t=495) The network log shows 6 allowed and 1 blocked request, with the agent's call to news.ycombinator.com denied and the approval commands to follow up.
- **−** [08:15](https://youtu.be/mnoUXIT4nMY?t=495) He narrates a stored session synced 05 Oct, two days before the talk, instead of running the command live, and secret injection and the factory are never shown running.

**Measured 1/2**

- **+** [02:06](https://youtu.be/mnoUXIT4nMY?t=126) The talk quotes platform scale as 20 million developers, 20 billion image pulls and 1 billion installs.
- **−** [07:44](https://youtu.be/mnoUXIT4nMY?t=464) "6, 10, 20 different agents running on your laptop" and the "sub-second boot" slide come with no load, memory or boot-time measurement.

**Depth 1/2**

- **+** [06:42](https://youtu.be/mnoUXIT4nMY?t=402) Secret handling is explained step by step: the agent sees a dummy environment value and the host proxy injects the real key on outbound calls.
- **+** [07:13](https://youtu.be/mnoUXIT4nMY?t=433) The microVM choice gets a reason: own kernel, memory and CPU, enforced by Intel VT-x or AMD-V rather than by policy.
- **−** [16:29](https://youtu.be/mnoUXIT4nMY?t=989) The review agents that gate every PR get one line with no word on what they check.

**Reusable 1/2**

- **+** [20:02](https://youtu.be/mnoUXIT4nMY?t=1202) The free sbx CLI (brew install, no Docker Desktop needed) plus the TypeScript SDK and OpenAPI API cover the sandbox portion and building on the platform.
- **−** [15:27](https://youtu.be/mnoUXIT4nMY?t=927) The AI factory the speaker calls the main message is "internal for now", so that part has no artifact to take away.
