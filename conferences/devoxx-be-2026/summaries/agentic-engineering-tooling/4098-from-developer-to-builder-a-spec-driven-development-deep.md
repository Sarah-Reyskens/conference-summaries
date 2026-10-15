---
title: "From Developer to Builder: A Spec-Driven Development Deep Dive"
talkId: "4098"
conference: devoxx-be-2026
speakers: [Simon Martinelli]
track: Agentic Engineering & Tooling
sessionType: Deep Dive
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=z8lal-Yt_04
durationMin: 157
slides: https://speakerdeck.com/simas/from-developer-to-builder-a-spec-driven-development-deep-dive
verdict: 8
frames: 15
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# From Developer to Builder: A Spec-Driven Development Deep Dive

Simon Martinelli · Deep Dive · Agentic Engineering & Tooling

Slides: https://speakerdeck.com/simas/from-developer-to-builder-a-spec-driven-development-deep-dive

## TL;DR

Martinelli teaches his AI Unified Process (AIUP): use cases, an entity model and requirements live in the repository next to the code, and an agent harness of skills, MCP servers and guardrail tests turns specs into code and tests. Live with Claude Code he builds a hotel reservation system from a vision statement to a running Spring Boot app with tests and coverage checks, then covers harness hardening, token economy, brownfield reverse engineering and how AIUP compares with OpenSpec, BMAD, Spec Kit and Kiro.

## Key takeaways

- Keep the spec in the repo next to the code (spec-anchored) and change the spec first; generated code and tests follow from it.
- Specify behavior, not code: a guest can cancel up to 24 hours before arrival, never which endpoint or column implements it.
- Engineer the harness, not the prompt: skills, MCP servers, hooks and deterministic checks decide output quality far more than model choice.
- Turn guidelines into guardrails: a rule in CLAUDE.md is a wish, a failing build is a fact.
- Treat generated unit tests as white-box tests with limited value; put real confidence in black-box acceptance tests derived from business processes.
- Review is the bottleneck: plan review time, keep diffs to one use case per session, prefer synchronous review over per-PR async review.

## Notes

### [00:34](https://youtu.be/z8lal-Yt_04?t=34) Setup, poll and agenda

Martinelli, a self-employed Swiss engineer with 30 years mostly modernizing decades-old Java systems, splits the session in two: part one motivates spec-driven development and builds a hotel reservation system live, part two covers testing, the harness, brownfield work and method choice. An opening poll shows some attendees already tried spec-driven development. He demos in Claude Code; most of his customers use Copilot.

### [04:28](https://youtu.be/z8lal-Yt_04?t=268) Why spec-driven development: a vibe-coding failure

He vibe-coded a volunteer management system with Windsurf in late 2024, then could not adapt it when a festival asked for a different process: he no longer knew what his own code did. Inspiration came from Tessl and Fowler's framing of LLMs as a new abstraction layer, except non-deterministic: a compiler reproduces output, an LLM does not. His extra goal is sustainability, so the next modernization wave starts from specs instead of software archaeology. Untested legacy code gets "balcony architecture" (nested ifs in sequence diagrams) because nobody dares refactor.

### [09:40](https://youtu.be/z8lal-Yt_04?t=580) Three levels of spec-driven development

Per Birgitta Böckeler: level 1 is spec-first (specs discarded after coding); level 2 is spec-anchored (specs stay in the repo and evolve with the code); level 3 is spec-as-source (only the spec is kept, code always regenerated). The session commits to level 2. Level 3 fails twice: regeneration is non-deterministic, and regenerating everything per change burns tokens. Core warning: AI is not a compiler, and the developer stays responsible for the output.

### [14:23](https://youtu.be/z8lal-Yt_04?t=863) From developer to builder

On Boris Cherny's ladder (gated, assisted, parallel, supervised autonomy, AI-native) he sits at step 2, orchestrating a few agents. The role shift: write specs and review code, own architecture and quality instead of following tickets ("commercial Scrum"), move knowledge from heads into the repo, build the harness instead of living in the IDE. Reviewing generated code has the legacy-PR context problem, and AI reviewers can outgrow the change. Typing is outsourced to the LLM; software engineering remains.

### [19:03](https://youtu.be/z8lal-Yt_04?t=1143) The AI Unified Process at a glance

AIUP borrows from the Rational Unified Process (keep what helps) with four iterative phases: vision and requirements, use cases plus architecture, code plus tests, delivery and acceptance. The chain runs from a vision through a requirements catalog to entity models plus use cases, acceptance tests, and architecture input. The "blue thing" between spec and code is the harness: skills, MCP servers and guidelines.

### [30:30](https://youtu.be/z8lal-Yt_04?t=1830) Demo setup: hotel reservation system

The demo (github.com/simasch/hrs, H2 by default, PostgreSQL branch with Testcontainers, JDK 25) is a ten-room hotel with Guest, Receptionist, Manager and Housekeeping actors. Stack rationale is review cost: Vaadin's tested components mean less frontend code to review, and jOOQ shows executed SQL where JPA hides it behind annotations. The Maven pom is already harness: it pins the stack, and the agent is forbidden from changing dependencies. Scaffolding comes from start.spring.io.

### [35:17](https://youtu.be/z8lal-Yt_04?t=2117) AIUP plugins: core plus stack skills

AIUP ships as a Claude Code marketplace with a technology-agnostic core (requirements, entity model, use-case diagram and spec, spec review, test case, business process, reverse engineering) and stack plugins (Vaadin plus jOOQ by him, Angular, Blazor, NestJS by contributors). A skill is a directory with SKILL.md: front matter, instructions, templates, checklists and validation scripts. Warnings: skills can carry prompt injection (audit before installing), scripts can damage the machine, and versioned skills recreate Maven-style dependency management.

### [42:34](https://youtu.be/z8lal-Yt_04?t=2554) From vision to requirements and glossary

From a short docs/vision.md, /requirements produces docs/requirements.md and a glossary. He runs Claude Sonnet; students reproducing the flow with local Qwen models got the same results. Every requirement needs a stable ID for traceability. He marks the generated non-functional requirements as hallucinated guesses, useful in familiar domains like retail, useless for Swiss parliamentary case management. Constraints carry IDs and sources such as GDPR.

### [47:50](https://youtu.be/z8lal-Yt_04?t=2870) Deriving the entity model

/entity-model emits docs/entity_model.md with an ER diagram (RoomType, Room, Reservation, Guest, Stay, CleaningTask) and check constraints. A wholesale ERP with 1200 entities proves the modularization point: it fits neither one diagram nor one context. Monoliths overflow contexts while scattered microservices (a Swiss insurer: 1000 developers, 400 services) split one use case across services; the answer is vertically sliced self-contained systems. Diagrams are code: Mermaid, PlantUML for use-case diagrams.

### [51:30](https://youtu.be/z8lal-Yt_04?t=3090) Why use cases, and how to write them for AI

Use cases (Jacobson; Cockburn's 2002 book) give a trackable diagram plus specs with ID, actors, goal, status, contract (preconditions, postconditions), main success scenario and alternative flows. Statuses (Draft through Done plus Obsolete) drive tracking and automation. His guide (leanpub.com/writing-use-cases-for-ai) says write them as fine-grained as possible: a 22-page parliament use case proved unreadable. Actors can be humans, systems, APIs or events. Rule: no screens, no APIs, no tables in a use case.

### [62:54](https://youtu.be/z8lal-Yt_04?t=3774) Use-case diagram and first use-case spec

/use-case-diagram produces a PlantUML diagram (UC-001 Search Availability through UC-010) doubling as the progress board; a bigger volunteer-system diagram shows module splitting with green done and white pending use cases. Actors usually become authorization roles. /use-case-spec UC-001 drafts the spec: actor, trigger, linked requirements, scenario (enter dates and guest count, submit, validate, search, display), alternative flows, business rules, success versus failure postconditions. He also demos Studio, a web use-case editor over the git repo.

### [72:24](https://youtu.be/z8lal-Yt_04?t=4344) Harness engineering: guides, sensors, human steering

Guides steer before acting; sensors check after acting so the agent self-corrects. Computational sensors (ArchUnit, scripts, linters) block; LLM-based sensors only warn, since AI checking AI can loop forever. Example ArchUnit rule: no domain class depends on a Vaadin class. CLAUDE.md stays short and links detail files (architecture docs, ADRs). On a repeated mistake, fix the harness rather than just the code, pushing everything checkable out of human review.

### [88:33](https://youtu.be/z8lal-Yt_04?t=5313) Implementing UC-001: migration, code, running app

With the use case Approved (other states are refused), /flyway-migration generates SQL with check constraints; he defends database integrity as the last durable layer. /implement UC-001 generates repository, view and wiring in 52 seconds. Reviewing jOOQ is a quick SQL scan (he spots a possible N+1 and defers it). The running app works but UX is weak: past dates selectable, checkout before check-in allowed, raw errors. Cause: nobody specified UI validation. Unspecified behavior yields default behavior.

### [96:26](https://youtu.be/z8lal-Yt_04?t=5786) Browserless tests and the coverage check

/browserless-test generates a use-case-level integration test with a @UseCase annotation; server-side Vaadin tests run as Java without a browser. He favors the testing trophy over the pyramid for data-centric apps: lint at the base, few unit tests for isolated logic such as price calculation, many integration tests, since database-less tests mostly test mocks. Coverage reaches about 95 percent, but he openly questions its value when tests and code are generated together. /coverage-check then audits spec against code and tests.

### [104:19](https://youtu.be/z8lal-Yt_04?t=6259) Bonus: business processes to end-to-end test cases

A parliament analyst's "where is the business process?" adds BPMN: each activity maps to one use case, lanes to roles, each path to a test case whose data forces every gateway decision. /business-process drafted hotel-stay.bpmn and caught a gap (FR-011's cleaning task has no use case). A wholesale order example shows the chain: Markdown workflow to generated Playwright test with engineer-built helpers. The live /test-case run fails honestly: only UC-001 is implemented, so no journey exists yet.

### [111:08](https://youtu.be/z8lal-Yt_04?t=6668) Hardening: 4+1 views, guardrails, sensors, constraints

AIUP maps onto Kruchten's 4+1 model (logical: entity model; development: plugin packages; process: transactions; physical: Kubernetes, SSO; plus-one: use cases). Guidelines are soft; guardrails (hooks, ArchUnit, CI gates, permissions, sandbox) are hard; ADRs carry the why. The PetClinic sensor suite (github.com/AI-Unified-Process/petclinic, ./mvnw test -Dgroups=sensor) holds traceability, architecture and convention tests. Hooks block unverified turns and demand coverage audits before Done. Constraints live versioned in git, never in a wiki.

### [125:10](https://youtu.be/z8lal-Yt_04?t=7510) Where agents run: sandboxing and isolation

Claude Code's sandbox (filesystem limits, network controls, permission prompts) is a soft boundary, not full isolation. He warns against agents unzipping jars to decompile code; use the javadoc MCP server or IntelliJ-as-MCP instead. Real isolation means a VM (Hetzner, serverless Fly.io Sprites, driven via Remote Control) or local sandboxes (Docker SPX, Nano, OpenGEL). One project implements via GitHub Actions when a use case is pushed as Approved. Parallel agents also bring exhausting task-switching.

### [131:29](https://youtu.be/z8lal-Yt_04?t=7889) Skill management and token economy

Harness content rots: an insurer workshop discarded most framework skills after four days because specs carried the knowledge and models had improved. He tests skills with Tessl-style evals across agent and model combinations, citing a 6000-skill sprawl as the failure mode. Input tokens drive cost (history resent per turn); output is the small part. Levers: one use case per session, modular architecture, precise file references, short specs, prompt caching (model or MCP changes destroy it), matched model strength, subagents.

### [135:13](https://youtu.be/z8lal-Yt_04?t=8113) Brownfield: reverse engineering to specs

Brownfield inverts the flow: feed code, schema, tests and documents to the agent and regenerate specs one module at a time. The PetClinic demo shows /reverse-engineer producing the entity model, diagram and use cases; a parliament-expenses case shows architecture recovery (SAP and tax interfaces, layers). Domain experts must review, with granularity tuned to strip implementation detail. New features then fold into the same spec-first flow. Warning: AI omits edge cases (one became a day-three blocker), so repeat the cycle and keep old and new systems running in parallel.

### [144:11](https://youtu.be/z8lal-Yt_04?t=8651) Fit, challenges and choosing a method

AIUP fits long-lived, rule-heavy, regulated systems and brownfield modernization; it fits poorly for prototypes, algorithms, performance tuning and visual design. Challenges: spec drift, non-determinism across agents (same model, different results in Claude Code, Copilot, Junie), data protection (no production data, on-premises models), daily tool churn (method before tool), unbalanced trust (a junior stopped reviewing after day one; seniors read every line). The table casts AIUP as enterprise process, BMAD as product-team method, OpenSpec and Spec Kit as developer toolkits, Kiro as a solo IDE, Tessl as a skills registry. Separate the stack-independent what from the stack-specific how.

### [154:15](https://youtu.be/z8lal-Yt_04?t=9255) Conclusion

Specs plus the harness reduce non-determinism and target sustainability; most of the session went to specs, not code. Solo, knowing specs and domain, he felt six times faster building his Studio tool, but enterprise settings run far slower. Closing line: know your architecture and your domain.

```text
# from published slides p.25-52: the AIUP lab command chain
/requirements → /entity-model → /use-case-diagram → /use-case-spec UC-001
/spec-review → /flyway-migration → /implement UC-001
/browserless-test UC-001 → /coverage-check UC-001
/test-case hotel-stay → /playwright-test TC-001
```

## Tools, libraries and specs

- Claude Code with Sonnet (Qwen, Copilot, Junie, OpenCode mentioned for comparison)
- AI Unified Process: unifiedprocess.ai marketplace, aiup-core, aiup-vaadin-jooq (plus Angular, Blazor, NestJS contributor stacks)
- Demo: JDK 25, Spring Boot, Vaadin Flow 25, jOOQ, Flyway, H2 / PostgreSQL with Testcontainers (github.com/simasch/hrs)
- ArchUnit, SonarQube, JUnit, Playwright, Surefire; PlantUML, Mermaid, BPMN via demo.bpmn.io
- MCP servers: Vaadin, jOOQ, javadoc, Playwright, Confluence, IntelliJ-as-MCP
- Docker SPX, Fly.io Sprites, Hetzner VMs, Claude Code Remote Control, GitHub Actions
- OpenSpec, BMAD, GitHub Spec Kit, Kiro (AWS), Tessl; sensors: github.com/AI-Unified-Process/petclinic

## Who should watch

- Enterprise developers, architects and modernization teams wanting a full spec-anchored loop to copy onto their stack.
- Requirements engineers, analysts and test engineers curious how use cases and BPMN plug into agent-generated code and E2E tests.
- Skip for hands-on depth on other frameworks (only AIUP runs live), algorithms, UI craft, or a shortcut around learning the domain.

## Verdict

**8/10**: A three-hour original method with a published sample project, held back by a live loop that stops short of its reconcile and end-to-end steps and by anecdotal numbers.

**Novelty 2/2**

- **+** [26:52](https://youtu.be/z8lal-Yt_04?t=1612) AIUP is the speaker's own method, with design rationale for skipping the planning/task phase other spec-driven tools keep.
- **+** [48:22](https://youtu.be/z8lal-Yt_04?t=2902) The 1200-entity wholesale ERP modernization behind the modularization argument is unpublished production experience.
- **+** [130:57](https://youtu.be/z8lal-Yt_04?t=7857) At an insurer's one-week workshop most framework skills were thrown away on day four because the specs carried that knowledge and the models had improved.

**Demonstrated 1/2**

- **+** [94:21](https://youtu.be/z8lal-Yt_04?t=5661) The generated repository and view are reviewed on screen and the app starts and runs ("And it works"), weak UX and raw errors included.
- **−** [102:12](https://youtu.be/z8lal-Yt_04?t=6132) The /coverage-check audit is only launched in the background and its report never appears on screen.
- **−** [117:51](https://youtu.be/z8lal-Yt_04?t=7071) The live /test-case run ends without output because only UC-001 is implemented.

**Measured 1/2**

- **+** [92:46](https://youtu.be/z8lal-Yt_04?t=5566) The 52-second implementation is timed on screen.
- **−** [100:06](https://youtu.be/z8lal-Yt_04?t=6006) The 95 percent coverage figure is stated without showing the report behind it.
- **−** [155:16](https://youtu.be/z8lal-Yt_04?t=9316) Six-times-faster is a solo gut feeling, offered with the warning that enterprise settings run far slower.

**Depth 2/2**

- **+** [75:00](https://youtu.be/z8lal-Yt_04?t=4500) An ArchUnit rule (no domain class may depend on a Vaadin class) shows how deterministic sensors enforce architecture.
- **+** [76:04](https://youtu.be/z8lal-Yt_04?t=4564) Deterministic sensors block the next step while AI-based sensors only warn, because repeated AI checks can fix and re-find issues in an endless loop.
- **+** [12:19](https://youtu.be/z8lal-Yt_04?t=739) Spec-as-source is rejected with reasons: regeneration is non-deterministic and per-change regeneration burns tokens.

**Reusable 2/2**

- **+** [116:48](https://youtu.be/z8lal-Yt_04?t=6998) The PetClinic repository (github.com/AI-Unified-Process/petclinic) publishes the specs, the use-case traceability sensors and the architecture tests, and its Claude Code hooks ([119:24](https://youtu.be/z8lal-Yt_04?t=7164)) guard the session.
- **+** [35:48](https://youtu.be/z8lal-Yt_04?t=2148) The AIUP core skills and stack plugins ship through a public marketplace (unifiedprocess.ai), covering the loop the talk runs live.
- **−** [30:30](https://youtu.be/z8lal-Yt_04?t=1830) The hotel demo repo (github.com/simasch/hrs) is the starter only: its docs/ folder holds vision.md, not the specs and tests built live.
