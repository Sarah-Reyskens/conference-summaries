---
title: "Emergent DevEx: The Good, the Bad, and the Legacy"
talkId: "7022"
conference: devoxx-be-2026
speakers: [Makan Sepehrifar, Soroosh Khodami]
track: People, Practices & Career
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=9MPYPejgTGo
durationMin: 48
slides: null
verdict: 5
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Emergent DevEx: The Good, the Bad, and the Legacy
Makan Sepehrifar, Soroosh Khodami · Conference · People, Practices & Career

## TL;DR
Developer experience is what engineers do for each other in implementation details, and top-down platform transformation programs usually miss it. Two architects who have worked from three-person startups to 8,000-engineer enterprises walk through how scaling breeds process chaos, how platform teams become the bottleneck they promised to remove, and how small bottom-up initiatives compound into standards. The closing advice: build composable capabilities, share failures and runbooks, and measure friction reduced rather than adoption enforced.

## Key takeaways
- Copying another company's DevEx model one-to-one (the "Spotify model") fails because no two organizations are carbon copies; transformation programs that start elsewhere rarely land where expected.
- Platform teams should build for composition and extension so a team that dislikes the standard path can build its own on the same APIs.
- Enable, don't enforce: making adoption the success metric pushes platform teams to force migration even when their solution is not the best fit (Goodhart's law).
- Package each new capability as a small reusable component (API first), then let CLI, pipeline tasks, portal integrations, and MCP servers wrap it.
- Standardization works best bottom-up: start with something small in one team, share it early, advocate for adoption, and let usage make it the standard.
- Define support boundaries for anything you build: supporting consumers past the boundary (for example debugging their pipeline scripts) swallows the whole week.
- Adopting an inner-source component means taking responsibility for it, including fixing what breaks, rather than filing an issue and waiting.

## Notes

### [00:33](https://youtu.be/9MPYPejgTGo?t=33) What developer experience actually is
Makan Sepehrifar (staff engineer, Productboard, five years in DevEx) opens by asking what DevEx is: IDPs, templates, actions, agents, skills? The talk's answer is that it sits beyond words, ceremonies, products, and solutions, in actions, implementation details, and culture. Soroosh Khodami (solution architect, Rabobank, usually talks security) adds that the two have worked together for over ten years across startups of three people and organizations with 8,000 engineers in e-commerce, finance, and telecom. This talk revisits ideas they presented two years earlier ("Developer Experience: From Hype to Reality") with new reflections.

### [02:41](https://youtu.be/9MPYPejgTGo?t=161) The legacy: from two-pizza teams to process chaos
Every company starts with a two-pizza team turning pizza and coffee into code with one goal: enough revenue to pay salaries. Growth brings product and business complexity until cognitive load forces a split into domain teams, usually along domain-driven-design lines, and the service architecture follows. Conway's law then bites: the software mirrors the organization's communication structure, so scaling the architecture requires scaling the org structure. The result is department silos with different goals, cultures, and processes, plus a communication gap: alignment happens manager-to-manager several levels up while the engineers who depend on each other have never met. Each silo locally optimizes its own process, producing process chaos. Nobody falls in love with bureaucracy; the alternative is informal power play.

### [06:50](https://youtu.be/9MPYPejgTGo?t=410) Platform teams promise everything, become the bottleneck
The usual fix is platform teams whose mission is visibility into the silos through standardized, self-service, unified processes. The pitch: visibility, lower cost through standardization, maintained delivery speed, compliance, secure by design, developers kept in flow. The paradox is that platform teams accelerate delivery by becoming the new bottleneck. Between 66% and 80% of DevEx book titles on Amazon target leaders rather than individual contributors, and each spawns a transformation program promising migration from one state to another. Quoting Gregor Hohpe, hardly two organizations are carbon copies, so imported programs rarely land as expected. Platform teams arrive halfway through the scaling story and must gain control to deliver visibility, caught between transformation initiatives, organizational history optimized for local value delivery, and developers who want predictability, autonomy, and room to innovate while keeping delivery speed.

### [12:34](https://youtu.be/9MPYPejgTGo?t=754) The bad: three anti-patterns and the abstraction dilemma
Doing nothing leads to "technical dictatorship": the platform team starts from market, technology, and tool research instead of developer requirements, then uses admin rights and compliance power to force migration, showing only the stick. The second anti-pattern, named after Gregor Hohpe's "Grim Reaper", is wrapping every cloud and utility provider in one grand abstraction that promises zero vendor lock-in but ends up obsolete, poorly maintained, slower than the providers, and saddled with a new taxonomy developers must learn. The third is portal-driven experience: investing in the UI (a Backstage-style portal) before the backend, ending with a logic-heavy frontend doing auth, forms, and workflows, where clicking through "wizard step 14 of 47" is the only way to use the platform. The hardest decision remains the right level of abstraction: too abstract and developers lose visibility and can't troubleshoot (support tickets flood back); too visible and onboarding becomes painful.

### [17:15](https://youtu.be/9MPYPejgTGo?t=1035) The good: principles for platform teams
Borrowing the "narrow corridor" from Acemoglu and Robinson (2024 economics Nobel laureates), the speakers argue optimal DevEx lives where developer communities temper central standardization forces. Three principles follow. First, accept you are always running behind the developers; standardizing something nobody uses yet is pointless, so learn from what communities already do. Second, happy platform customers are silent customers, and asking 100 developers yields 101 preferences, so satisfaction is a poor success metric. Third: build everything for composition and extension; make co-creation and co-evolution a primary goal so community inventions can be adopted and standardized later; enable rather than enforce. Developer empathy closes the list: give up admin rights so you feel the same pain, hunt friction points instead of market share, don't invent your own jargon, and meet developers where they are instead of shipping yet another portal, dashboard, or CLI.

### [24:41](https://youtu.be/9MPYPejgTGo?t=1481) Healthy platforms, boundaries, and reusable components
Khodami shows the utopia slide: a core platform, another platform built on top of it, applications on top, plus applications bypassing the platform entirely with their own servers and databases. Enabling includes allowing opt-out. Two rules follow. Make ownership boundaries explicit: his platform engineers spent most of their week debugging consumers' thousand-line pipeline scripts, which is like calling Oracle to debug your Java application. And package every capability as a small reusable component: a database-creator API at level zero gets wrapped by other teams into a GitHub Action, an Azure DevOps task, a CLI, a Backstage integration, pipeline templates, an MCP server, or an agent skill.

### [29:22](https://youtu.be/9MPYPejgTGo?t=1762) Small initiatives that became standards
Four stories show bottom-up standardization working. At Dutch online supermarket Picnic, a few engineers adopted Google's Error Prone to end pull-request bikeshedding over style (final vs. var), shared the idea early before it was polished, and handed out stickers to contributors and adopters; by 2023 it underpinned the Java platform team with one team maintaining configuration, and later went open source. At Rabobank, Khodami's secure-pipeline blueprint was rejected by the "housing tribe" because it would lower their standards, so he worked with them to extend their higher standard across the organization instead. A Spring Boot parent POM standardizing versions, logging, and dependency management spread from 20 microservices in one squad to 1,000, at which point onboarding all of them to OpenTelemetry took a few lines of config instead of per-service migrations. And one hardened, shared Java base container image would save every squad from repeating container hardening while lifting company-wide security.

### [37:40](https://youtu.be/9MPYPejgTGo?t=2260) Share beyond code, inner source, and agentic AI
Sharing covers articles about things that took a month to learn, runbooks from incidents, and failure stories: Khodami confesses his team once built "the worst artifact management platform in the world" on JFrog/Nexus with a tunnel-vision design, shared the story, took feedback, and rebuilt it into something the vendors themselves liked. Inner source is a bazaar culture of shared responsibility: what you build today must survive your move to another team, and platform teams are developers consuming what other developers built. On AI, the platform side should invest in high-quality service APIs with defense in depth, traceability, and documentation wired into agents via MCP (Sepehrifar's Productboard CLI let his coding agent answer process questions in week one); the developer side should document conventions in-repo as skills or policies, since agents replicate conventions well, illustrated by a pilot repo where nearly all PRs looked identical. The close: stop waiting for someone else to fix it, compose architectures others can extend, standardize proactively from small beginnings, advocate early including for failures, measure friction reduced, and treat DevEx as a moving target.

## Tools, libraries and specs
- Error Prone (Google's Java compile-time checker), adopted org-wide at Picnic
- Backstage (Spotify's internal developer portal), cited as the portal teams copy
- OpenTelemetry, onboarded to 1,000 services via a shared parent POM
- Spring Boot parent POM used as the standardization vehicle
- GitHub Actions, Azure DevOps tasks, MCP servers, agent skills as wrappers around platform APIs
- JFrog Artifactory / Sonatype Nexus artifact management

## Who should watch
Engineers on platform teams or consuming internal platforms in mid-size to large organizations, and anyone living through a DevEx transformation program. Skip it if you want implementation detail on IDPs, Backstage, or platform engineering internals; this is a strategy-and-culture talk with stories, not a technical build guide.

## Verdict
**5/10**: The speakers' own platform experience carries it past a search, but its numbers lack baselines, the central question of abstraction level is left open, and there is no artifact to take home.

**Novelty 1/2**

- **+** [33:01](https://youtu.be/9MPYPejgTGo?t=1981) The Rabobank housing-tribe story shows the speaker's own pipeline blueprint rejected for lowering the tribe's standards, then reworked into extending the tribe's higher standard to the whole organization.
- **+** [38:44](https://youtu.be/9MPYPejgTGo?t=2324) The confession of building the worst artifact-management experience on JFrog/Nexus and rebuilding it from feedback is first-hand production experience.
- **−** Conway's law, the Spotify-model critique, Gregor Hohpe's "Grim Wrapper" and platform paradox, portal-first warnings, inner-source practices and the narrow-corridor frame of Acemoglu and Robinson's book are public material a search surfaces.

**Demonstrated 1/2**

- **·** A strategy-and-culture talk about platform-team dynamics with nothing to run, so there is no demo to judge.

**Measured 1/2**

- **+** [34:32](https://youtu.be/9MPYPejgTGo?t=2072) The parent POM spread from 20 microservices in one squad to 1,000 services, an adopter count that gives the scale of the standardization.
- **−** [35:35](https://youtu.be/9MPYPejgTGo?t=2135) "Thousands of hours saved" across squads is asserted for the shared POM with no baseline or measurement behind it.
- **−** [08:57](https://youtu.be/9MPYPejgTGo?t=537) The claim that 66% to 80% of DevEx book titles target leaders comes from an AI-assisted trawl made before the talk, with no method or sample size.

**Depth 1/2**

- **+** [16:15](https://youtu.be/9MPYPejgTGo?t=975) The abstraction-level dilemma weighs both failure modes: over-abstraction kills troubleshooting ability, full visibility kills onboarding.
- **+** [23:05](https://youtu.be/9MPYPejgTGo?t=1385) The enable-don't-enforce argument is grounded in Goodhart's law: adoption targets get gamed into forced migrations.
- **−** [16:45](https://youtu.be/9MPYPejgTGo?t=1005) The abstraction-level dilemma ends at "a very narrow trade-off" with no guidance on when to choose which level.

**Reusable 1/2**

- **+** [27:46](https://youtu.be/9MPYPejgTGo?t=1666) The level-zero-API wrapping pattern (GitHub Action, CLI, Backstage integration, MCP server, skill) is a practice a team can reconstruct.
- **+** [26:45](https://youtu.be/9MPYPejgTGo?t=1605) The support-boundary rule (say where support ends, so engineers are not busy debugging consumers' pipeline scripts) is a practice a platform team can adopt.
- **−** [31:58](https://youtu.be/9MPYPejgTGo?t=1918) The talk points to no repository, sample, checklist or config of its own; Picnic's open-source project is mentioned but not named, and the QR code at 30:25 leads to Rick's talk.
