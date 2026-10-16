---
title: "From Autocomplete to Autopilot: How AI Is Changing the Developer Experience"
talkId: "23529"
conference: devoxx-be-2026
speakers: [Tugdual Grall]
track: Agentic Engineering & Tooling
sessionType: Deep Dive
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=pMv_39iSXVA
durationMin: 182
slides: null
verdict: 7
reach: segment
frames: 13
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---
# From Autocomplete to Autopilot: How AI Is Changing the Developer Experience
Tugdual Grall · Deep Dive · Agentic Engineering & Tooling

## TL;DR
GitHub's Tugdual Grall traces his own path from Copilot tab-completion in 2021 to delegating whole features to parallel agents, and argues the developer's job is shifting from typing code to expressing intent, reviewing plans, and managing cost and quality gates. Across three hours of live demos he rebuilds apps, localizes the Spring PetClinic, reviews PRs, and embeds the Copilot SDK, with running commentary on credits, models, and enterprise governance.

## Key takeaways
- Match your AI intensity to the project's goal: daily releases and heavy token spend make sense for innovation bets, while a banking app wants stability and fewer, safer changes.
- Never start a complex task with implementation; write a plan first (Grall's "grill me" skill forces the agent to ask questions until the spec is sharp), then review and execute it.
- Work in parallel sessions, not one chat: git worktrees plus one agent per task beats watching a single agent type, and scheduled sessions can pick up labeled issues on their own.
- Judge cost in dollars per outcome, not tokens: his full PetClinic rewrite burned 53M input tokens but cost $80, and nearly all of it was cached input.
- Do not write agent-driven code without a strict CI pipeline: automated tests, dependency scanning, secret scanning, and static analysis on every commit are the precondition, not the follow-up.
- Re-tune your setup every few months: harnesses and models improve so fast that instruction files, skills, and model choices from six months ago are probably stale.
- Keep customization in the repo, not in a central platform team: each team moves at its own speed, so share what works through an internal registry instead of mandating one configuration.

## Notes

### [04:45](https://youtu.be/pMv_39iSXVA?t=285) The numbers behind the talk
A 10-person GitHub team built the Copilot CLI starting September 2025 and merges around 500 pull requests per week, which means most lines are AI-written and human-reviewed rather than human-typed. Asked live, the CLI reported an average of 1.21 releases per day since September, peaking at 57 releases in May. That same team later rewrote the CLI/SDK from TypeScript to Rust: one engineer, three weeks, about $120,000 in tokens, against an original estimate of 18 months to two years for a small team. Copilot is now the top committer on GitHub's own platform repositories. Grall's framing question for the session: pick your AI posture (prototype, migration, long-term product) before picking your tools.

### [11:38](https://youtu.be/pMv_39iSXVA?t=698) Five years from completion to delegation
Grall installed the Copilot VS Code plugin in September 2021 (Codex era, over a year before ChatGPT) and describes the successive jumps: tab completion, chat, agent mode, then context engineering with instruction files, skills, and hooks. His own workflow moved from the IDE to the CLI in late 2025 and then to the Copilot desktop app in 2026, driven by two motives: forcing himself to write full task context up front, and running many tasks in parallel instead of watching one agent work. He also notes he has deleted most of his custom instructions over time because current harnesses already know, for example, how to write idiomatic Java.

### [27:53](https://youtu.be/pMv_39iSXVA?t=1673) Rebuilding a side project without typing
His running example is a windsurfing GPS tracker running since 2017 (Java parsing, Express plus Bootstrap frontend, MongoDB). He asked Copilot to analyze the undocumented codebase and rebuild it: TypeScript GPS parsing, PostgreSQL (chosen purely because it is cheaper to host), a new design, more tests, multilingual support, and a Tauri desktop app with animations. The point he returns to throughout: tell the agent your business domain explicitly (what an "alpha 500" turn means in sailing) because it cannot infer it.

### [32:38](https://youtu.be/pMv_39iSXVA?t=1958) VS Code tips for those still in the IDE
Grall admits he barely uses the IDE anymore but shows the features he misses least: per-interaction cost in credits (one demo question cost 13 cents; he watches dollars, not token counts), the agent debug log for seeing which instruction files, skills, hooks, and MCP servers fired in a session, inline chat for single-file edits, terminal command generation (finding the five biggest files in a repo), and AI commit messages plus the sparkle shortcuts in both VS Code and IntelliJ. His optimization rule: make the output right first, check the price, and only then switch models or trim tokens.

### [49:07](https://youtu.be/pMv_39iSXVA?t=2947) The CLI: autopilot, permissions, worktrees
In the Copilot CLI he copies Spring PetClinic's main branch into a new private repo and asks for French and Italian localization in a new branch. Permission modes run from manual approval through assisted to full autopilot ("YOLO mode"); he lives in autopilot for coding but switches to step-by-step for production pushes and database changes, and sets per-task credit caps since sessions can run for hours. Sandboxing can constrain filesystem, network, and commands. The segment introduces git worktrees (a 2015 feature he, like most of the audience, discovered through agentic work): one isolated checkout per task so parallel sessions never collide.

### [69:31](https://youtu.be/pMv_39iSXVA?t=4171) Plan mode and "grill me"
For anything beyond a trivial task, Grall insists on planning before implementing. In plan mode he asks for drug management in PetClinic with 20 seed rows, then invokes his favorite skill, "grill me", which interrogates him: standalone entity or relation, fields, validation, REST API, per-language labels, deletion semantics. The resulting plan becomes the spec and the prompt. Execution can then fan out to subagents working in parallel on the same task, which he presents as the one thing no human developer can match: two hands cannot type two features at once. He has largely dropped formal spec-driven frameworks (SpecKit, OpenSpec, BMAD) in favor of this plan document plus architecture notes.

### [81:37](https://youtu.be/pMv_39iSXVA?t=4897) Why he moved to the desktop app
The Copilot app is now his daily driver: one window listing local and cloud sessions, issues, and PRs, with one-click jumps into VS Code or IntelliJ when he wants to read code. Sessions support keep-alive, phone-based monitoring via QR code, and a large rotating set of commands and experimental features. His broader point is that roadmaps are fiction in this market: nobody predicted the CLI in 2024 or the desktop app in 2025, so vendors ship behind feature flags and users should re-check release notes continuously.

### [100:33](https://youtu.be/pMv_39iSXVA?t=6033) PRs, automated review, adoption metrics
After the break he finishes the localization PR and shows Copilot's review behavior: it noticed unrelated staged changes from an earlier VS Code edit and deliberately left them out of the PR. Copilot can be assigned as a reviewer with configurable effort, optionally auto-approving; rulesets control when review is requested, and reviews run on the same GitHub Actions infrastructure as CI. He then tours the enterprise dashboard: client mix (IDE, CLI, cloud agent, app), passive versus active users, PR throughput (AI users shipping about 16% more PRs in the demo org), time to merge, and per-model token consumption, all available via API for internal dashboards.

### [114:49](https://youtu.be/pMv_39iSXVA?t=6889) Automating the simple work away
Back in the app, he clones PetClinic again, auto-generates labeled issues, and creates a scheduled session that every two minutes picks up unassigned `AI-auto` issues, builds each in its own worktree, assigns the issue, opens a PR with screenshots of the new feature, and keeps the human out of the loop. Side chats let him ask follow-up questions without polluting the main session context, and clearing or compacting context keeps long sessions coherent. He also opens the same worktree in IntelliJ to show the IDE remains one click away whenever reading code matters.

### [123:22](https://youtu.be/pMv_39iSXVA?t=7402) The $80 full-stack rewrite
The centerpiece demo is a single giant prompt executed end to end with no questions asked: keep the database but add SQLite as default, expose everything as REST CRUD, rebuild the frontend with a modern multi-theme, multi-language design, add tests per layer with explicit coverage targets, document each run, and use "rubber duck" mode (a second model challenging the implementation as it goes). Output was a working app with a REST backend and a new frontend, verified live in the browser. Cost: 53M input tokens, roughly 400K output tokens, $80, with the vast majority of input served from cache. His lesson is to evaluate benchmark-style: same prompt, same context, compare price and test results across models rather than reading generated code line by line.

### [138:23](https://youtu.be/pMv_39iSXVA?t=8303) Model pricing and personal benchmarks
One AI credit equals one cent, and every model card shows per-million-token input/output prices, so he shops for models the way others shop for cloud instances: when a vendor discounts a model 50%, large tasks move to it. He keeps a standing benchmark prompt (PetClinic backend to .NET, frontends to Angular and Node) and reruns it as harnesses and models change; one run hit 400M tokens and $120 because he accidentally used the expensive tier instead of medium. The takeaway is organizational: give your developer-experience team a small benchmark suite and rerun it regularly, because vendors do exactly that internally.

### [144:46](https://youtu.be/pMv_39iSXVA?t=8686) Quality gates for agent-written code
Grall's rule is blunt: do not code the way he demos without a rigorous automated pipeline. His repos run the test suite plus Dependabot, secret scanning, and CodeQL static analysis on every commit (free for public repos, he notes, so there is no excuse). When CodeQL finds a vulnerability, AI drafts the fix PR with an explanation of the data flow. For large diffs he asks for review by three models at once, and review behavior itself can be pinned down in instruction files. He also demos `/chronicle tips` and cost tips, which mine local session history for suggestions on instructions, skills, and spending; his teams run them weekly.

### [153:13](https://youtu.be/pMv_39iSXVA?t=9193) Skills, registries, and a supply-chain warning
Centralized platform configuration (models, MCP servers, agents) is giving way to per-repo skills at GitHub, because teams adopt at different speeds; the Copilot app and CLI repos carry their own skill sets, including project-specific performance-testing skills. The public awesome-copilot registry collects agents, instructions, and skills as inspiration, and an agent-finder command searches registries for things like SQL development packs. His warning is pointed: treat every third-party skill or MCP server as untrusted code, because autopilot mode will execute whatever they say; if governance blocks one, discuss it rather than bypassing it.

### [162:09](https://youtu.be/pMv_39iSXVA?t=9729) Debates, consensus debugging, and the Copilot SDK
Three advanced patterns close the technical arc. `spar` runs two agents against each other (Electron versus Tauri, in his example) with a fixed intro, rebuttal, summary, and open-question format for challenging architecture opinions. Consensus mode asks three models to diagnose a problem, such as a slow parser on 10 MB files or a hypothetical million-pet slowdown, without changing code. Finally, he embeds the Copilot SDK directly in the rewritten PetClinic behind a feature flag: a chat tab finds pets ("a pet named Max"), proposes visits, and drafts workflow changes using the app's own data rather than calling a model vendor directly. He generates an HTML report from session history showing time, tokens, and credits per task.

### [178:35](https://youtu.be/pMv_39iSXVA?t=10715) Canvas extensions and closing
Canvas plugins embed custom React interfaces in the app: a Jira canvas for non-GitHub trackers, a Devoxx schedule viewer, mock Azure DevOps dashboards, and a log-and-trace visualizer the Copilot app team built for itself. His closing advice splits by codebase age: for anything new or being rewritten, aim to implement without touching code yourself; for legacy systems you maintain, adopt the same practices incrementally. No slide deck or link was shared; the session ends with open Q&A.

## Tools, libraries and specs
- GitHub Copilot (VS Code, JetBrains, CLI, desktop app, cloud coding agent) with Auto/Balance mode, plan mode, autopilot, sandboxing, subagents, `spar`, consensus review, rubber-duck mode, `/chronicle` tips, scheduled sessions, side chat, Canvas extensions
- Copilot SDK, embedded in the demo PetClinic app behind a feature flag
- Spring PetClinic (Java original; rewritten to a TypeScript/SQLite/REST backend with a modern multi-theme frontend)
- Rust and Tauri 2 (Copilot CLI/SDK rewrite; desktop app framework, compared against Electron)
- CodeQL, Dependabot, secret scanning, GitHub Actions, `gh` CLI, git worktrees, Awesome Copilot registry
- Spec-driven predecessors mentioned: SpecKit, OpenSpec, BMAD; rival harnesses named in passing: Cursor, Claude, Codex
- Playwright (used for generated UI tests), PostgreSQL, SQLite, MongoDB, Express, Bootstrap

## Who should watch
Developers and team leads already using an AI coding assistant who want a complete tour of agentic workflows: planning, parallel sessions, cost control, review automation, and quality gates. Engineering managers rolling out Copilot at enterprise scale get the governance half (model allowlists, credit budgets, adoption APIs). Skip it if you want a balanced comparison of assistants: every demo is Copilot, and Cursor, Claude, and Codex appear only as names.

## Verdict
**7/10**: working Copilot workflows and comparative session-cost reports support a useful delegation tour, but the three-hour intermediate slot mostly teaches operation and leaves its examples unpublished.

**Reach segment**: Copilot users can apply the CLI, app, review and enterprise controls directly; users of other assistants can transfer the planning and quality-gate practices.

**Novelty 1/2**

- **+** [154:51](https://youtu.be/pMv_39iSXVA?t=9291) GitHub's move from centralized configuration to per-repo skills reflects teams' differing needs and adoption speeds, adding organizational experience beyond the feature tour.
- **+** [22:07](https://youtu.be/pMv_39iSXVA?t=1327) Grall connects his move away from the IDE to the need to stop watching agents and prepare several independent tasks, giving the workflow advice a personal rationale.
- **·** The main feature walkthrough is within the search baseline of GitHub's official Copilot CLI and customization documentation rather than a tested cross-tool decision framework.

**Demonstrated 2/2**

- **+** [68:30](https://youtu.be/pMv_39iSXVA?t=4110) The requested French and Italian localization runs in the browser before the workflow proceeds to a pull request.
- **+** [175:26](https://youtu.be/pMv_39iSXVA?t=10526) The rewritten PetClinic's embedded Copilot SDK returns Max from the application data and then proposes a visit for user confirmation.
- **·** [127:48](https://youtu.be/pMv_39iSXVA?t=7668) The rewritten application's pages, languages and themes are visible, while exhaustive feature correctness remains the speaker's assurance.

**Measured 2/2**

- **+** [06:50](https://youtu.be/pMv_39iSXVA?t=410) The CLI release series states its counting method, including stable and prerelease releases but excluding drafts, and covers 348.37 days.
- **+** [142:40](https://youtu.be/pMv_39iSXVA?t=8560) A session report compares models' token use, cost and elapsed time for the same PetClinic rewrite prompt and context, with UI and unit tests used to check the outputs.
- **−** [109:28](https://youtu.be/pMv_39iSXVA?t=6568) The adoption dashboard's PR uplift is demo-organization data that the speaker explicitly says not to interpret as a real effect.

**Depth 1/2**

- **+** [59:37](https://youtu.be/pMv_39iSXVA?t=3577) Permission choices distinguish ordinary coding from production database changes, which he performs manually step by step.
- **+** [136:16](https://youtu.be/pMv_39iSXVA?t=8176) Side conversations use a subset or summary of the main context to avoid mixing unrelated questions into an implementation session.
- **·** [144:46](https://youtu.be/pMv_39iSXVA?t=8686) The delegation safety model rests on tests and security scans, but this intermediate deep dive mainly shows configuration and operation rather than examining how to establish sufficient acceptance criteria for generated changes.

**Reusable 1/2**

- **+** [123:54](https://youtu.be/pMv_39iSXVA?t=7434) The rewrite prompt describes REST operations, test coverage targets and run reports in enough detail to reconstruct the approach.
- **+** [157:28](https://youtu.be/pMv_39iSXVA?t=9448) Awesome Copilot supplies public instructions and skills as inspiration, rather than the session's complete example.
- **−** [158:30](https://youtu.be/pMv_39iSXVA?t=9510) The migrated repository is promised as future-public, leaving no linked artifact that reproduces the main demos.
