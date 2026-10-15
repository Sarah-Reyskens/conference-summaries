---
title: We created our own AI orchestrator and it became so much more!
talkId: "23531"
conference: devoxx-be-2026
speakers: [Ricky van Rijn]
track: Development Practices
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=niBYuCuViGw
durationMin: 52
slides: null
verdict: 7
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# We created our own AI orchestrator and it became so much more!
Ricky van Rijn · Conference · Development Practices

## TL;DR
A CTO describes how his team at MetaFactory built an AI agent orchestrator on Embabel Agent to coordinate coding agents, and how the tool forced them to rewrite requirements practice, centralize agent definitions, and rethink review and product ownership. The payoff: a Node.js to Java backend migration in 18 productive staff hours, and an open-sourced cockpit (OpenJCockpit) for running spec-driven agent workflows.

## Key takeaways
- Keep spec files small enough to review: a 500-line spec fed to agents produced gap-filling assumptions and unreviewable pull requests, while sliced single-use-case specs produced ~100-line reviewable changes.
- Centralize agent definitions, skills, and MCP configuration in one shared repository; developers with divergent local agents produced inconsistent output and review friction.
- Importing a user story into a spec file with AI is not understanding it: unclear requirements returned from agent output to analysis must become an explicit feedback path, not a retry.
- Define automerge conditions instead of inspecting every detail: small changes with all quality checks passing can merge without human review, with the human still accountable for enabling it.
- Agentic execution outruns planning, so the product owner must join analysis earlier and steer on value and readiness; a quarterly roadmap became the working queue.
- Route models through a proxy (the team used LiteLLM) and mix large hosted models with local models such as Qwen to control token cost.

## Notes

### [00:41](https://youtu.be/niBYuCuViGw?t=41) From assisted coding to agentic AI
Van Rijn frames three phases: traditional teams, AI-assisted work (ChatGPT on the side), and agentic AI where agents draft and execute code while humans review. His team at MetaFactory set out to build an overview of active agents and work, expecting a technical tool, and ended up changing how the team wrote requirements and reviewed software.

### [03:21](https://youtu.be/niBYuCuViGw?t=201) First use case and spec-driven setup
The pilot was converting an internal Node.js backend to Java: a safe internal experiment with an OpenAPI contract as starting requirements. The team defined agent roles (QA engineer, solution architect, lead backend developer), recorded responsibilities on a Confluence page, and agreed that agents write code while humans review and give feedback. They committed to spec-driven development and pulled in the current and next sprint for a long-term view.

### [07:50](https://youtu.be/niBYuCuViGw?t=470) Turning Jira stories into spec files
The team built an MCP server to Jira and had AI convert user stories into markdown spec files meant as the version-controlled source for coding agents. One long story became a 500+ line spec. A slide shows the story-to-spec conversion and the resulting agent chain: business analyst, lead backend developer, solution architect, backend, frontend, QA, ending in a pull request with reviewers assigned.

### [12:35](https://youtu.be/niBYuCuViGw?t=755) The first review shock
The first agent output was a giant pull request (shown diff: +19,525 −319 across 225 files changed) that shocked the assigned reviewer into refusing it. Agents had filled requirement gaps with assumptions, including inventing an employee-retrieval service the team already had. Quality varied because each developer ran locally customized agents with different emphases (security vs. coding guidelines), which slowed reviews and demotivated the team.

### [15:47](https://youtu.be/niBYuCuViGw?t=947) Centralizing agents in one repository
The fix was to move agent definitions, skills, MCP configuration, and guardrails into a shared central git repository. Review feedback that recurred (for example, unwanted shorthand notation) was folded back into the shared definitions, so each developer's strengths improved the agents for everyone. Spec files stayed at project level; agent definitions lived at team level across clients.

### [19:36](https://youtu.be/niBYuCuViGw?t=1176) Building the orchestrator cockpit
The team built its orchestrator with an Embabel Agent core on the JVM and a React frontend. A dashboard screenshot shows a spec file with a running workflow rendered as stage orbs (impact, test-design, implementation, review, realisation, evidence), an agent log, and quality checks on the right: unit test coverage, NIST 2, OWASP ZAP, ISO 25010, SAST, dependency scan, architecture rules. Workflows run inside Docker workspaces, Open Policy Agent checks authorization (actions run as the triggering user, not a system account), and models are reached through a LiteLLM proxy.

### [26:12](https://youtu.be/niBYuCuViGw?t=1572) Slicing specs and shifting pressure left
Pressure moved from code review to making requirements concrete up front. Large specs were sliced into smaller single-use-case specs, discussed jointly by developers, business analysts, and the product owner. A later pull request of about 100 lines was easy to verify against its linked use cases. Refinement participation became mandatory: staying silent and criticizing the agent output afterward now visibly burned tokens.

### [32:39](https://youtu.be/niBYuCuViGw?t=1959) Cost, models, and governance
The team started on the largest hosted models, then moved to a hybrid setup with local Qwen models on large laptops for overnight runs, keeping fast models for urgent customer work. Open questions remain around guardrails versus harnessing (his image: a guardrail tells the child not to leave the garden, a harness is the fence), audit logging, monitoring, and one-click exportable reports for audits and the EU AI Act.

### [37:27](https://youtu.be/niBYuCuViGw?t=2247) Queue, automerge, and workflow designer
New UI screenshots show a spec queue with a per-project auto-merge checkbox (merge happens only when every check passes) and a graphical workflow designer so business-oriented users can compose agent processes. The team agreed to stop inspecting every detail and to define where human judgment mattered; unclear requirements loop back to analysis and re-enter the queue. Execution then outpaced decisions: sprints finished faster than planning, so the whole quarterly roadmap became the queue and the product owner joined analysis full-time.

### [46:31](https://youtu.be/niBYuCuViGw?t=2791) Migration result and takeaways
The Node.js to Spring Boot migration took about 18 productive staff hours (excluding unattended agent runtime), is in production, and meets requirements. His three takeaways: collaboration matters more than before, AI knows the product but does not understand it, and teams should trust the new process while questioning old habits. A "control tower" idea would use AI to interview people into writing smaller specs. The orchestrator is open-sourced as OpenJCockpit at https://github.com/OpenJCockpit.

## Tools, libraries and specs
- Embabel Agent (JVM agent framework, orchestrator core)
- Spring AI (MCP server)
- React (cockpit frontend)
- LiteLLM (model proxy for hybrid routing)
- Qwen (local models for cheap overnight runs)
- Open Policy Agent (authorization checks)
- OWASP ZAP, SAST, dependency scan, NIST 2, ISO 25010 (quality gates)
- EU AI Act (compliance consideration)
- OpenJCockpit (https://github.com/OpenJCockpit, the open-sourced orchestrator)

## Who should watch
Teams adopting coding agents who are hitting review overload, inconsistent agent output, or vague-requirements failures gain the most, especially leads designing the surrounding process. Viewers wanting Embabel internals, orchestrator source walkthroughs, or benchmarked agent comparisons should look elsewhere.

## Verdict
**7/10**: A first-hand account of an agent orchestrator built and run in production, with an open-sourced repository, limited by screenshots instead of a run, numbers without a baseline, and the orchestrator itself left unexplained.

**Novelty 2/2**

- **+** [46:31](https://youtu.be/niBYuCuViGw?t=2791) The Node.js to Spring Boot migration result (18 productive hours, in production) comes from the speaker's own team and no public source documents it.
- **+** [15:47](https://youtu.be/niBYuCuViGw?t=947) The local-agents-to-central-repository turnaround, including the demotivation episode and the notation-feedback loop, is original production experience rather than assembled advice.

**Demonstrated 1/2**

- **+** [22:19](https://youtu.be/niBYuCuViGw?t=1339) The dashboard screenshot shows a real spec workflow mid-run with stage orbs, an agent log line, and the quality-gate panel.
- **+** [37:27](https://youtu.be/niBYuCuViGw?t=2247) The queue screenshot shows the per-project auto-merge checkbox over real spec rows; the workflow designer next to it is introduced as "a small preview" of work in progress.
- **−** [22:51](https://youtu.be/niBYuCuViGw?t=1371) The quality-gate results are described over static screenshots ("good for the show"); no workflow runs end to end on screen with its output visible.

**Measured 1/2**

- **+** [12:50](https://youtu.be/niBYuCuViGw?t=770) The first agent pull request is shown at +19,525 −319 across 225 files, against a ~100-line pull request after the specs were sliced [29:26](https://youtu.be/niBYuCuViGw?t=1766).
- **+** [46:31](https://youtu.be/niBYuCuViGw?t=2791) The migration cost is quantified as 18 productive staff hours, counting employee time only and excluding unattended agent runtime.
- **−** [46:31](https://youtu.be/niBYuCuViGw?t=2791) The 18 hours have no baseline: no manual-migration estimate or before/after comparison backs the implied saving, and the speaker says it "cannot be seen like it's a person working eight hours".

**Depth 1/2**

- **+** [17:26](https://youtu.be/niBYuCuViGw?t=1046) The centralization decision is argued with reasons: divergent local agents caused inconsistent output, so shared definitions absorb recurring review feedback.
- **+** [26:12](https://youtu.be/niBYuCuViGw?t=1572) The small-spec practice is explained through the gap-filling mechanism: large specs let agents invent services, small ones make assumptions reviewable.
- **−** [19:04](https://youtu.be/niBYuCuViGw?t=1144) The orchestrator's own internals (Embabel wiring, workflow execution) and the choice to build one instead of adopting an existing tool are named rather than explained.

**Reusable 2/2**

- **+** [50:50](https://youtu.be/niBYuCuViGw?t=3050) The final slide points to the open-sourced orchestrator at https://github.com/OpenJCockpit, whose repository documents the cockpit, Keycloak, PostgreSQL, the LiteLLM gateway, the local Qwen model and the seven-stage agent pipeline with a Docker Compose start-up.
