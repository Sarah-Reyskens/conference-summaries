---
title: "In the loop, not in the dark: staying in control in the era of dark software factories"
talkId: "52104"
conference: devoxx-be-2026
speakers: [Alex Gavrilescu]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=jhvT8hVYSvQ
durationMin: 45
slides: null
verdict: 9
frames: 7
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15

# In the loop, not in the dark: staying in control in the era of dark software factories

Alex Gavrilescu · Conference · Agentic Engineering & Tooling

## TL;DR

After agents generated hundreds of thousands of lines for him with no review, Alex Gavrilescu lost the ability to debug his own production system during a live outage. He answers with Groma.md, an MIT-licensed tool that keeps a deterministic, real-time architectural blueprint of a codebase so humans review architecture instead of every generated line.

## Key takeaways

- Reviewing generated code line by line does not scale; reviewing the architecture diagram after each agent run catches structural decay (duplicated components, per-page auth logic) that per-file review misses.
- AGENTS.md rules, linter rules (cognitive complexity helps against agent-written nested loops), and post-write simplification passes reduce agent mess temporarily but do not prevent architectural drift on their own.
- A useful architecture map must regenerate in seconds without an LLM call, or it goes stale the moment agents write more code; Groma scans deterministically with per-language plugins and stores results as markdown.
- Raw deterministic scans need one curation pass (grouping, names, connections) by a human or an agent; stable deterministic IDs then keep later incremental updates cheap and diffable.
- Giving agents production credentials (tailing logs, deploying fixes) trades incident speed for real risk: the same agent that fixed a bad query in two minutes could have deleted production data.
- Don't relay agent output verbatim to colleagues; a human asked for advice owes a human answer, not a pasted Codex response.

## Notes

### [00:37](https://youtu.be/jhvT8hVYSvQ?t=37) Shipping fast with agents, skipping review

Gavrilescu set out in January to raise feature throughput with AI loops and orchestrators, including Backlog.md, a tool he built last year that turns markdown tasks over to agents. Throughput rose month after month, measured in finished features used by real users rather than commits. As shipping sped up, he stopped doing code review, and nothing broke for a while, so the habit stuck.

### [03:43](https://youtu.be/jhvT8hVYSvQ?t=223) A production outage he could not debug

Mid-hackathon, his vibe-coded event platform (submissions, judging, hosting on Cloudflare) started returning 500 errors, an authentication failure surfacing through the UI. With 14 years of experience and many war rooms behind him, he froze: he had never touched the codebase or connected to production himself, having handed his agent a deploy token that automated everything. He asked Codex to fix production; it tailed the Cloudflare Worker logs, found a bad SQL query with an infinitely growing WHERE IN list, deleted rows to stop the bleeding in 2 minutes, and shipped a permanent fix through CI/CD in 20. The incident left him feeling like a pass-through between requirements, Codex, and production rather than a senior developer.

### [09:31](https://youtu.be/jhvT8hVYSvQ?t=571) The architectural mess, and rules that didn't hold

Inspecting the code afterward, he found 20 copy-pasted instances of one button in a Vue.js app instead of a single reusable component, per-page authentication instead of middleware, tests asserting UI trivia rather than business logic, and dead code he could not distinguish from live code. Each file was correct in isolation; the architecture was the mess. He tightened AGENTS.md, cut his 20+ installed skills down to remove overlapping instructions, added a cognitive-complexity lint rule, and appended simplification passes (including context-free subagents) to his loops. Quality improved briefly, then drifted back within weeks: new pages again carried their own auth logic.

### [14:14](https://youtu.be/jhvT8hVYSvQ?t=854) Four iterations to Groma

First came Archifi, an open-source skill that has agents draw architecture diagrams; it worked once and went stale on the next change. Groma itself took three failed attempts: a UI-first mockup with the same staleness problem, an agent-built version that produced 700 commits in 72 hours and nothing working, and a self-mapping version whose agent-authored core was a 3,000-line switch case on folder names that collapsed on any other repo. The fourth attempt started minimal (one TypeScript scanner, one markdown generator, one simple visualizer) and grew feature by feature. The name comes from the Roman surveyor's tool for laying straight streets.

### [19:27](https://youtu.be/jhvT8hVYSvQ?t=1167) How Groma works

The proposed flow: write tasks with intent, let agents implement, then review the regenerated architecture in a viewer. Groma.md mapped by itself shows the C4 hierarchy (system, containers, components, code) with drawable flows between components. Underneath, one scanner plugin per language or framework uses native language tooling (TypeScript compiler API, Roslyn for C#, Java tooling) to extract file structure and relationships into a unified Groma core, so mixed codebases such as a Java backend with a React frontend map together. Scans take seconds on large repos and milliseconds on small ones.

### [22:07](https://youtu.be/jhvT8hVYSvQ?t=1327) Live Keycloak scan, then curation

On stage, Groma scanned a local Keycloak clone: mostly Java (197 declarations) plus React, JavaScript, and TypeScript. The raw first scan renders as an unreadable hairball of ungrouped files, which is deliberate. During development the speaker found that predicting connections automatically meant hardcoding guesses, so the first scan stays near-raw and a curation pass (grouping, titles, descriptions, actors, connections) follows, done by a human or an agent via `groma agent-instructions` in about five minutes. The curated result, prepared ahead because curation takes minutes, shows a legible map: end user signing in through the authentication module to OpenID Connect, with protocols, persistence, federation, and SPI containers inside the Keycloak server.

### [27:18](https://youtu.be/jhvT8hVYSvQ?t=1638) Six agents tracked live, with diffs

Six Codex agents took six Backlog.md tasks on the Groma repo itself (one added an architecture-history fast-forward view requested at the conference) and the map updated in real time as they wrote, each agent's touched components visible with task IDs. The on-screen cost counter reached about $28.59 for 11.7M tokens. The live-diffs view then showed what changed: new components in blue, modified in yellow, deleted in red, with a per-component change list. Incremental updates stay fast because components carry deterministic IDs and each scanner only recomputes what the filesystem watcher reports as changed.

### [30:58](https://youtu.be/jhvT8hVYSvQ?t=1858) Open source, standards, and wrap-up

Groma is MIT-licensed; the speaker prefers issues over PRs since his own agent workflows ingest them. Everything shown can run fully offline with local models. Backlog.md integration is a plugin, so Jira, Linear, or GitHub Issues could plug in the same way. Scanners already cover COBOL and Assembly (agent-built in days after audience requests), which frames the tool as a way to supervise even code no human wants to read. Storage follows the C4 model and Google's Open Knowledge Format 0.2 (markdown bundle), so uninstalling Groma leaves readable docs behind, and a GitHub Action publishes per-PR architecture-change pages. He closes by arguing the developer's remaining expertise is architectural judgment: either stop reviewing code entirely or review at the architecture level, and keep enough hands-on knowledge to survive being cut off from AI.

### [38:25](https://youtu.be/jhvT8hVYSvQ?t=2305) Q&A

Missing connections on the map (a new component with no link to the auth logic) reveal duplicated logic, and a future architectural linter could flag these as warnings. Replaying a task step by step across commits is possible manually via branch diffs but has no click-through automation yet. Custom ad-hoc flows traced from a bug report don't exist but would be easy to add. Multi-repo overviews work except for git-history features, which assume a single repo.

## Tools, libraries and specs

- Groma.md (MIT, launched ~1.5 weeks before the talk): deterministic codebase mapper with viewer, `groma web` wizard, `groma agent-instructions`, GitHub Action for per-PR architecture pages
- Backlog.md: the speaker's markdown task orchestrator, integrated with Groma as a plugin
- Keycloak: brownfield demo target mapped live on stage
- C4 model and Google Open Knowledge Format 0.2: the modeling and markdown-storage standards Groma follows
- TypeScript compiler API, Roslyn (C#), Java tooling: per-language scanner foundations; COBOL and Assembly scanners added during the conference week
- Codex and GPT-6.1 Sol Ultrafast: agents and model behind the six-agent live demo
- skills.sh marketplace: source of the speaker's 20+ conflicting agent skills
- Cloudflare Workers: production host of the hackathon platform in the outage story

## Who should watch

Developers and tech leads running coding agents on real codebases who feel review slipping will get the most, including a tool to try immediately. Beginners get a clear mental model with no prerequisites. Skip it if you want Groma internals at contributor depth (scanner plugin authoring is only sketched) or measured before/after evidence that architecture review beats line review; the case rests on one developer's experience.

## Verdict

**9/10**: A first-hand outage, an open-source tool built through four documented iterations, and a live scan and agent-tracking demo; held back only by unmeasured claims.

**Novelty 2/2**

- **+** [03:43](https://youtu.be/jhvT8hVYSvQ?t=223) A first-hand production outage caused by unsupervised agent code, with the specific failure (an ever-growing WHERE IN list) and the two-minute agent fix.
- **+** [15:16](https://youtu.be/jhvT8hVYSvQ?t=916) The author's build record: three failed attempts (a stale UI mockup, 700 commits in 72 hours with nothing working, a 3,000-line folder-name switch) before the fourth Groma.
- **+** [24:10](https://youtu.be/jhvT8hVYSvQ?t=1450) The raw-scan-plus-curation trade-off, explained from the author's own over-hardcoding mistakes rather than from docs.

**Demonstrated 2/2**

- **+** [22:37](https://youtu.be/jhvT8hVYSvQ?t=1357) A Keycloak clone scanned live with the init wizard, which detected Java (197 declarations), React, JavaScript and TypeScript, and the raw hairball map rendered on screen.
- **+** [28:21](https://youtu.be/jhvT8hVYSvQ?t=1701) Six Codex agents editing the Groma repo live while the map tracks their touched components in real time.
- **+** [29:55](https://youtu.be/jhvT8hVYSvQ?t=1795) The live-diffs view marking new components blue and modified ones yellow while the agents were still running.
- **−** [25:13](https://youtu.be/jhvT8hVYSvQ?t=1513) The Keycloak curation step is skipped on stage ("this takes few minutes, I skipped it"), so the curated map shown is pre-made rather than produced live.

**Measured 1/2**

- **+** [30:00](https://youtu.be/jhvT8hVYSvQ?t=1800) The live run displays token spend with its basis on screen (about $28.59 for 11.7M tokens, 6 agents, list prices).
- **−** [28:21](https://youtu.be/jhvT8hVYSvQ?t=1701) The claim that each of the six tasks would take "few hours if not a single day" by hand is the speaker's own estimate, with no baseline.
- **·** [09:31](https://youtu.be/jhvT8hVYSvQ?t=571) Decay is reported as self-observed totals (20 duplicated buttons, a 3,000-line switch case) with no before/after comparison of review methods.

**Depth 2/2**

- **+** [21:05](https://youtu.be/jhvT8hVYSvQ?t=1265) Scanner design: per-language plugins on native tooling feeding a unified core, with deterministic IDs enabling fast incremental updates.
- **+** [34:40](https://youtu.be/jhvT8hVYSvQ?t=2080) Format choices with reasons: C4 for the hierarchy, Open Knowledge Format 0.2 so the markdown survives uninstalling the tool.
- **+** [12:09](https://youtu.be/jhvT8hVYSvQ?t=729) Why shallower fixes failed: agents tolerate deeply nested loops, so a cognitive-complexity lint rule helps, yet AGENTS.md rules, skill pruning and simplification passes improved the code only briefly before drift returned.

**Reusable 2/2**

- **+** [30:58](https://youtu.be/jhvT8hVYSvQ?t=1858) The MIT-licensed Groma repository, installable as a global tool and started with `groma web` ([35:43](https://youtu.be/jhvT8hVYSvQ?t=2143)).
- **+** [25:13](https://youtu.be/jhvT8hVYSvQ?t=1513) The `groma agent-instructions` command ships agent-usable curation workflows, and a marketplace GitHub Action ([33:36](https://youtu.be/jhvT8hVYSvQ?t=2016)) publishes per-PR architecture pages.
