---
title: "The Rise of Agent Enablement: Coding Agents Don't Scale Themselves. Neither Do Your Teams."
talkId: "21671"
conference: devoxx-be-2026
speakers: [Patrick Debois]
track: People, Practices & Career
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=wxNQRGPnJ24
durationMin: 47
slides: null
verdict: 7
frames: 9
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# The Rise of Agent Enablement: Coding Agents Don't Scale Themselves. Neither Do Your Teams.
Patrick Debois · Conference · People, Practices & Career

## TL;DR
Debois argues that scaling coding agents is an organizational problem, not a tooling one: treat context as code with its own lifecycle, then enable it across four layers (agent, team, platform, organization). The second half reframes the agent "factory" as a concurrency-control problem rather than a pipeline problem, and offers risk-based merging as the way up the autonomy ladder.

## Key takeaways
- Treat prompts, skills, AGENTS.md files and specs as code: lint, eval, security-scan and version them, and read agent logs the way you read production telemetry.
- Stop fixing code the agent wrote; fix the context, harness or loop so the agent gets it right next time.
- Make agent improvement a team ritual: planning checks whether a task is specified enough for solo agent execution, retros review context quality, and team leads own shared context.
- Scale through an AI platform team that provides models, routers, registries and paved-road harnesses, with an appointed owner and goals set by engineering leadership.
- Track agent effectiveness by human touches per agent task, and org leverage by how many teams improve when one shared context change lands.
- Treat the review queue as a risk problem: auto-merge low-risk changes, canary medium ones, verify high-risk ones further, and keep humans on critical paths.
- Design parallel-agent work for concurrency (isolation, ordering, semantic merge, cache invalidation) instead of serializing everything back into one loop.

## Notes
### [02:41](https://youtu.be/wxNQRGPnJ24?t=161) Context is the new code
The opening parallel structures the first half: developers now write context (prompts, docs, ticket text, specs, AGENTS.md) the way they wrote code, so it deserves a context development lifecycle. Testing means linters for skill front matter, LLM-as-judge evals, security scanners over context (motivated by an OpenClaw incident), and cost checks. Distribution means packaging skills with dependencies, versioning and marketplaces, mirroring npm and Maven. Observability means reading agent logs for refusals and corrections as failure signals, then feeding that back into better context. Context also rots like code: drift, tech debt, conflicting skills across authors. The compounding move is sharing context beyond the laptop so several people improve it together.

### [08:56](https://youtu.be/wxNQRGPnJ24?t=536) Four enablement layers
Better context only enables the agent. The developer becomes a conductor: stop touching code, and instead correct agents, improve harnesses and sharpen context. Teams need new rituals: planning asks whether a task is specified enough for an agent to run solo, retros ask what improved the agents rather than the code, and team leads must own shared context quality or everyone drifts back to solo habits. Enterprises then need an AI platform team (carved out of developer experience, the cloud team or IT) providing models, routers, gateways, registries and paved-road harnesses, with an appointed owner. Leadership sets the goals and watches two new signals alongside DORA metrics: human touches per agent task, and reuse reach across teams.

### [19:48](https://youtu.be/wxNQRGPnJ24?t=1188) The factory hits concurrency
Skills composed into goal-driven loops, run serially or in parallel, become the shared factory. Most factories disappoint Debois: the same review-deploy-spec loop with the agent where the developer sat. Running shared factories at Tessl surfaced the real phenomenon: agents trip over each other with duplicate work, conflicting edits and merges, and published factory stories all hit the same wall. A 16-agent build task was blocked by inter-agent dependencies, so adding agents could not unlock it. The weekend insight: rebase loops, duplicated work and stale assumptions are races, livelocks and stale reads, and git conflicts are only the visible data races. He calls the resulting mindset concurrent delivery.

### [24:01](https://youtu.be/wxNQRGPnJ24?t=1441) Where parallel work trips
Planning fails when naive schedulers parallelize blindly and collide, so tools model tasks as dependency graphs with claims and revision loops, echoing agile. Isolation moves from worktrees to VMs and memory-forking microVMs such as 4D, plus git-like dataset versioning (Dolt-style) so data conflicts stay reproducible. Merging moves from text merge to semantic merge (still coherent with the code's behavior) to intent merge (still in line with the spec), with invalidation signals when a parallel agent's assumptions expire. Piling PRs get answered by stacked PRs, release trains and order optimization that re-sequences the queue when assumptions invalidate.

### [29:45](https://youtu.be/wxNQRGPnJ24?t=1785) Review is a risk gate
The review queue is the visible bottleneck, but autonomy comes from survivable mistakes rather than perfect review. Four levers: reduce the likelihood of bad decisions (tests, policy checks, adversarial reviewer agents); verify the outcome (acceptance scenarios, before/after behavior, evidence bundles tied to intent); locate the risk (an autonomy budget from criticality, blast radius and data sensitivity); reduce impact (feature flags, circuit breakers, automatic rollback). That yields a risk-aware gate: low risk ships, medium risk canaries, high risk gets more verification, critical stays human. Debois illustrates risk labeling with a live-TV interactivity startup: one hour of show meant a one-hour ROI window, so the team labeled which code was safe to touch mid-broadcast. Startups with no users can ship everything; enterprises isolate pieces by risk.

### [37:34](https://youtu.be/wxNQRGPnJ24?t=2254) Concurrent versions in production
Since staging can never include real users, Debois asks what happens if concurrent versions in production become normal: keep options open longer instead of forcing one common denominator. Variants get their own risk analysis (Cursor's best-of-n as a technical precedent), business-level flagging tests which version customers prefer, and per-customer versions or customer vibe-coding on the platform become conceivable. He relates this to world models: awareness of the whole system instead of single-task code generation. He presents this part as belief, not a finished position.

### [40:13](https://youtu.be/wxNQRGPnJ24?t=2413) Air-traffic control for the factory
The pipeline problem becomes a concurrency-control problem: the industry built a faster plane and now must land many at once. Humans historically reduced concurrency to what they could follow (CFEngine's agents collapsed into Puppet and Chef runs, then Ansible's single loop), so the likely shape is serial above the line and concurrent inside the factory. Coordination load grows with longer agent trajectories, adversarial-speed security feedback loops, and continuous factory maintenance. Bottlenecks move to integration, verification, freshness (everything reconciled) and human attention; the ambient factory pages a human only when needed.

### [44:29](https://youtu.be/wxNQRGPnJ24?t=2669) Tessl: the factory joins the chat
At Tessl, support staff work inside the same factory, releases and chat: a customer feature request in Slack becomes a coded PR, reviewed and merged in the moment, replacing capacity planning. Remote workers finally see everything, but the new complaint is volume: nobody knows what happened this week. Docs and training lagged behind code output until they too were folded into the factory, creating more concurrency. Debois closes by predicting a reverse Conway move in which agent tech reshapes org structure, the topic of a promised follow-up talk; slides go out by LinkedIn DM and the concurrent-delivery post is still pending.

## Tools, libraries and specs
- Tessl: the speaker's employer; "Context-Driven Factories" post at tessl.io/blog/context-driven-factories
- AGENTS.md: emerging standard file for agent instructions
- OpenClaw: its context-security incident motivated scanning context for vulnerabilities
- Cursor best-of-n: cited as precedent for generating multiple solution variants
- 4D: microVM that forks memory in parallel for agents
- Dolt-style dataset versioning: git-like versioning so data conflicts stay reproducible
- CFEngine, Puppet, Chef, Ansible: cited as the historical arc from concurrent config agents to serial loops

## Who should watch
Engineering leaders, team leads and platform engineers scaling agents beyond individual use gain the most; solo developers get the lifecycle framing but little hands-on technique. Skip it for live demos, benchmarks, or factory implementation details.

## Verdict
**7/10**: Original concurrency-control framing backed by Tessl factory experience and a clear risk-gate model, limited by an all-speech format, anecdote-level numbers and no repository or checklist.

**Novelty 2/2**

- **+** [23:00](https://youtu.be/wxNQRGPnJ24?t=1380) The slide reframes rebase loops, duplicated work and stale assumptions as races, livelocks and stale reads, with git conflicts as the visible data races, and the speaker builds a "concurrent delivery" mindset on it.
- **+** [44:29](https://youtu.be/wxNQRGPnJ24?t=2669) Tessl factory observations (support staff merging from Slack, docs and training lagging code output) come from production use of the framework.
- **+** [02:41](https://youtu.be/wxNQRGPnJ24?t=161) The context development lifecycle maps linting, evals, security scanning, packaging, marketplaces and log observability onto context work as one cycle.

**Demonstrated 1/2**

- **·** [19:48](https://youtu.be/wxNQRGPnJ24?t=1188) A strategy and culture talk whose frameworks have nothing to run, so no demo slot applies.

**Measured 1/2**

- **+** [22:24](https://youtu.be/wxNQRGPnJ24?t=1344) The 16-agent C-compiler run, from Anthropic's public experiment, is cited with the remark that 100 agents would still be blocked by dependencies.
- **−** [17:15](https://youtu.be/wxNQRGPnJ24?t=1035) Human touches per agent task and reuse reach are proposed as effectiveness signals, with no before/after numbers from Tessl's own factories.

**Depth 2/2**

- **+** [28:11](https://youtu.be/wxNQRGPnJ24?t=1691) Merging moves from text merge to semantic merge to intent merge, and each agent's assumptions behave like a cache that parallel work can invalidate.
- **+** [35:30](https://youtu.be/wxNQRGPnJ24?t=2130) The risk gate slide weighs four levers (reduce likelihood, verify outcome, locate risk, reduce impact) and maps them to ship, canary, verify-more and human tiers.
- **+** [33:55](https://youtu.be/wxNQRGPnJ24?t=2035) The live-TV startup anecdote shows risk-labeled code under a one-hour ROI window, justifying progressive release over blanket review.

**Reusable 1/2**

- **+** [09:59](https://youtu.be/wxNQRGPnJ24?t=599) "Stop building the thing, but build the thing that builds the thing" is a practice a developer can apply, and planning and retro questions for context follow at [10:29](https://youtu.be/wxNQRGPnJ24?t=629).
- **−** [47:05](https://youtu.be/wxNQRGPnJ24?t=2825) The closing slide points to Tessl's "Context-Driven Factories" post and a pending concurrent-delivery post, with no repository, sample configuration or checklist for the practices.
