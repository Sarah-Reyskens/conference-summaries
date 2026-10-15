---
title: "In the loop, not in the dark: staying in control in the era of dark software factories"
talkId: "25652"
conference: devoxx-be-2026
speakers: [Alex Gavrilescu]
track: Agentic Engineering & Tooling
sessionType: Tools-in-Action
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=_dcauZC9ST8
durationMin: 29
slides: null
verdict: 8
frames: 6
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# In the loop, not in the dark: staying in control in the era of dark software factories

Alex Gavrilescu · Tools-in-Action · Agentic Engineering & Tooling

## TL;DR

After agents wrote an entire side project he could no longer debug during a live outage, Gavrilescu built Groma.md, an open-source tool that keeps a live architectural blueprint of a codebase so humans review architecture diffs instead of agent-written code. The talk pairs that production incident with a live run mapping Keycloak's 8,467 Java files into a navigable map.

## Key takeaways

- Reviewing every agent-written line does not scale; reviewing the architecture diff each change produces keeps a human in the loop with less effort.
- Agent-generated architecture diagrams go stale after the next commit, so the scan must be deterministic, offline, and re-run continuously.
- Stable component IDs plus Markdown output checked into the repo let architecture changes ride along with the PR that caused them.
- Per-feature validity is the trap: each PR looks fine alone while the system drifts (20 Button components, label-asserting tests, dead code) because no reviewer holds the whole context.
- When agents write all the code, end-to-end and BDD-style tests carry more weight than agent-written unit tests.

## Notes

### [00:34](https://youtu.be/_dcauZC9ST8?t=34) Fifty features a day, then a 500 in production

Gavrilescu spent 2026 pushing agent throughput with Ralph loops, bids, and Backlog.md (his own task tool), going from one or two features a day to about fifty, and stopped reading code while agents reviewed their own PRs. During a 100-person hackathon, his AI-written platform returned a 500 and he did not know how to connect to production, the database, or the logs. He asked Codex, which streamed the Cloudflare Worker logs, found a WHERE IN list that had grown until it crashed, and hotfixed production in 2 minutes by deleting rows, with a join rewrite deployed 20 minutes later. The save disturbed him: an agent had deleted rows in production SQL on a verbal go-ahead, and the fix depended on connectivity and model availability at that exact moment.

### [07:52](https://youtu.be/_dcauZC9ST8?t=472) The dark software factory, and fixes that did not stick

Opening the repo the next day, he found the Button component implemented 20 times, tests asserting labels like "submit", and dead code he could not distinguish from what was deployed. He calls this a dark software factory: the human supplies input and checks output while everything in between runs without oversight. Agents.md rules, linter rules, removing wrongly installed skills (React guidance in a Vue project), and an AI simplification pass all helped temporarily, but within weeks the agents drifted again because each feature request stays valid on its own.

### [11:27](https://youtu.be/_dcauZC9ST8?t=687) Groma.md: three failed iterations before the working one

Groma.md is his answer: create tasks with intent, let agents write code, and review only the architecture differences. Version 1 was a static UI mockup that could not generalize. Version 2 ran 72 unsupervised hours to 700 commits and arrived completely broken, repeating the original problem. Version 3 had agents write hardcoded folder-to-component rules that collapsed on the second repo. Version 4 ("Groma tree") took an MVP path: a small TypeScript scan via the compiler API, persisted as Markdown files, rendered as a diagram. The name comes from the Roman surveying instrument used for straight roads and town plans.

### [15:34](https://youtu.be/_dcauZC9ST8?t=934) Demo: watching agents move across the map

This segment used mocked data on the Groma repo itself. The map offers isometric and 2D views with actors on the left, external systems on the right, and C4-model components (system, container, component, code) between them, with source visible inline so review never leaves the tool. Flows can be drawn across components, and Backlog.md tasks attach to the components agents touch, with progress rings showing acceptance-criteria completion. Exports of the view attach to GitHub PRs as links to a static per-PR architecture diff.

### [19:12](https://youtu.be/_dcauZC9ST8?t=1152) Live: mapping Keycloak from a raw scan to a curated map

The Keycloak run was live: `git clone` followed by `groma web`, with setup asking for a project name, a Markdown output folder, and per-language scanners (Java via javac, C# via Roslyn, TypeScript via its compiler API). The raw deterministic scan produced an unreadable map in 21 containers, shown on screen (the tree root reads "keycloak-devoxx (7174)"). Because the scan is offline and deterministic with stable unique IDs, an agent curation pass (done beforehand by Claude, unreviewed) could group and label it into a Keycloak server view with Sign-in, Protocols, Persistence, Runtime, Federation, SPI, Admin console, and APIs, plus actors and a sign-in-with-password flow. Later features appear on the same map instead of requiring a fresh start.

### [22:48](https://youtu.be/_dcauZC9ST8?t=1368) What Groma is, and Q&A

Groma is open source and free, works without AI, integrates natively with Backlog.md (abstracted for other task tools later), and ships scanners for major languages with more available on request. In Q&A, he covered self-hosting through a CI/CD export to static HTML (single commit or diff across commits) and the Groma-action GitHub Action, which runs on the Groma repo itself so every PR carries its architecture diagram. Asked about unit tests, he said the map shows components rather than test detail, and that he leans on end-to-end and Gherkin BDD tests instead of agent-written unit tests.

## Tools, libraries and specs

- Groma.md (https://groma.md): open-source live architecture blueprints from deterministic repo scans
- Groma-action: GitHub Action attaching per-PR architecture diagrams
- Backlog.md: the speaker's task-tracking tool, integrated into the Groma map
- Keycloak: authentication/authorization suite mapped live (8,467 Java files)
- C4 model: the notation used for the maps
- Codex, Cloudflare Workers, Cloudflare D1: the agent and hosting stack in the outage story

## Who should watch

Developers who let agents write most of their code and want an architecture-level review loop, and leads deciding how humans stay accountable for agent output. Skip it if you want scanner internals or independently evaluated evidence; the talk shows what the tool does, not how the parsers work or how accurate the maps are.

## Verdict

**8/10**: Design rationale from the tool's author plus a live large-repo scan of an open-source tool, limited by a partly simulated review loop and self-reported numbers.

**Novelty 2/2**

- **+** [03:08](https://youtu.be/_dcauZC9ST8?t=188) Facing a live 500 in an AI-written hackathon platform with no idea how to reach production logs or the database supplies first-hand incident experience.
- **+** [11:58](https://youtu.be/_dcauZC9ST8?t=718) The three scrapped Groma designs, each with the reason it failed, are design rationale from the tool's author.

**Demonstrated 1/2**

- **+** [20:43](https://youtu.be/_dcauZC9ST8?t=1243) The Keycloak scan runs live and its raw map appears on screen.
- **−** [15:34](https://youtu.be/_dcauZC9ST8?t=934) The agent-change review loop uses mocked data in a live map interface, leaving actual agent-driven changes unproven.
- **−** [22:16](https://youtu.be/_dcauZC9ST8?t=1336) The curated Keycloak map is shown without checking whether its inferred architecture is correct.

**Measured 1/2**

- **+** [04:12](https://youtu.be/_dcauZC9ST8?t=252) The outage account gives recovery durations of two minutes for the hotfix and twenty minutes for the replacement query to reach production.
- **−** [01:36](https://youtu.be/_dcauZC9ST8?t=96) The ramp from one or two features a day to fifty is self-reported with no method behind the count.

**Depth 2/2**

- **+** [11:58](https://youtu.be/_dcauZC9ST8?t=718) Each scrapped design carries its failure reason: the static mockup could not generalize, 72 unsupervised hours yielded 700 broken commits, and hardcoded folder rules collapsed on a second repo.
- **+** [14:01](https://youtu.be/_dcauZC9ST8?t=841) Persisting the scan as Markdown lets architecture changes travel in the same commits and PRs as the code that caused them.
- **+** [21:44](https://youtu.be/_dcauZC9ST8?t=1304) Deterministic offline scans with stable component IDs explain why later features land on the existing map instead of requiring a fresh start.

**Reusable 2/2**

- **+** [22:48](https://youtu.be/_dcauZC9ST8?t=1368) Groma is open source and free at groma.md, covering the talk's main content.
- **+** [26:54](https://youtu.be/_dcauZC9ST8?t=1614) The Groma-action GitHub Action provides the per-PR architecture-diff workflow and runs on the Groma repo itself.
- **+** [25:52](https://youtu.be/_dcauZC9ST8?t=1552) Static HTML exports support sharing architecture views from CI, with commit ranges producing architecture diffs.
