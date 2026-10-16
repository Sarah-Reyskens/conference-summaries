---
title: "223 Pull Requests in 11 Days: The Recipe for Building Real Software with AI Agents"
talkId: "11556"
conference: devoxx-be-2026
speakers: [Julien Dubois]
track: Development Practices
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=0A2jqCqSIjg
durationMin: 50
slides: https://www.julien-dubois.com/conferences/building-with-ai-agents/index-en.html
verdict: 7
reach: broad
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# 223 Pull Requests in 11 Days: The Recipe for Building Real Software with AI Agents

Julien Dubois · Conference · Development Practices

Slides: https://www.julien-dubois.com/conferences/building-with-ai-agents/index-en.html

## TL;DR

Julien Dubois, GitHub principal manager and JHipster creator, built BootUI (an 83,000-line Spring Boot developer console) in 11 days by merging 223 agent-generated pull requests, and presents the workflow as six ingredients of "agentic engineering". The thesis: heavy specifications, tests and CI form a harness that lets agents loop to a green build, so the human shifts from typing code to briefing, reviewing and merging a fleet of agents. The talk leaves a replicable daily routine plus a priced tour of token caching that argues the harness matters more than the model.

## Key takeaways

- Put the effort into specifications and tests before agents run: business specs that state what "done" looks like plus a one-command build let agents loop until green instead of shipping a first draft.
- Fan independent tasks out to many agents in parallel, one branch or worktree each, and queue two or three long runs overnight; throughput comes from parallelism, not from faster typing.
- Cross-check hard work with other model families ("rubber ducking"): about half the tokens in this project went to auditing generated code rather than generating it.
- Stay on one workhorse model while its cache is warm, because switching models destroys cached context and can multiply the input bill; use small models or Auto mode only for mechanical tasks.
- Treat merge conflicts as an agent task: the agent-merge skill resolved every conflict in the project, and the speaker reports never resolving one by hand since.
- Expect the multiplier to shrink on codebases that are neither repetitive nor well documented; the ~40 near-identical panels and extensive Spring documentation did much of the lifting here.

## Notes

### [00:34](https://youtu.be/0A2jqCqSIjg?t=34) The experiment: BootUI in 11 days

Dubois time-boxed a project he had wanted for years, a developer UI showing transactions, exceptions and internals inside any Spring Boot app, and built it as the open-source BootUI in 11 calendar days. The scope he had always feared was real: a 5-module Maven build with Spring Boot 4, an embedded Vue 3 SPA with about 40 panels, security, tests, CI and a release. His commits cluster between 05:00 and midnight most days, which he reads as evidence of parallel async agents rather than continuous typing. Most commits are authored by Copilot, many landing in parallel, and new features still merged on release day.

### [03:11](https://youtu.be/0A2jqCqSIjg?t=191) The numbers: with and without AI

Figures on screen come from the git history: about 264 commits on main, 223 squash-merged PRs, 50k lines of Java in 461 files, 52 Vue components, 35 end-to-end specs, 116 test suites, 5,800 documentation lines and roughly 80 to 110 hours of human hands-on effort. Against that he sets an honest solo estimate of 6.5 to 8.5 months (1,100 to 1,450 hours), with the 40 panels as the dominant cost, yielding 15 to 20 times the productivity. Two caveats follow: a human team would have needed several people and their coordination overhead, and the business prize is shipping in two weeks while competitors take six months. Token spend for the sprint was about $2,000, or $9 per merged PR.

### [07:55](https://youtu.be/0A2jqCqSIjg?t=475) Agentic engineering, not vibe coding

Vibe coding (one prompt, accept the output) ships on day one and becomes unmaintainable, Dubois argues; agentic engineering invests days in specs and tests up front and profits over months. Months later the project has absorbed 500 further PRs across 20 releases with no maintenance backlog, still on current Spring Boot and Quarkus versions. That contrast frames the six ingredients that follow.

### [09:29](https://youtu.be/0A2jqCqSIjg?t=569) Ingredients 1 to 3: model, specifications, test harness

The workhorse model for the sprint was GPT-5.5 Extra-High with about 90% of tokens served from cache; hard tasks get cross-checked by Claude Opus 4.8 and Gemini 3.1 Pro, and trivial tasks go to a small model or Auto mode for speed rather than cost. Repository rules live in AGENTS.md (Maven, JUnit, Docker Compose, Spotless formatting) so parallel agents produce consistent code, while per-task specs define what to build, where, and what "done" looks like. Local JUnit and integration tests plus a GitHub Actions pass with CodeQL form the loop: agents rerun and fix until green, which is what makes merging 20 PRs a day safe. Specs plus tests are the harness around the model, and he reports an unnamed team found a better harness beats a better model.

### [17:47](https://youtu.be/0A2jqCqSIjg?t=1067) Ingredient 4: equip your agents

Four skills carried the workflow: Impeccable for the Vue front end and accessibility, orchestrate for advisor audits, agent-merge for PR review and conflict resolution, and a custom bootui-release skill distilled from releases first performed by hand. For Java code intelligence the agents query a language server (Eclipse JDT-LS; JetBrains announced its own at this Devoxx) about symbols instead of grepping text, which is more exact, faster and token-free at the price of one backend IDE per agent. Ten agents each running Java is why the laptop, not the model, became the bottleneck.

### [22:26](https://youtu.be/0A2jqCqSIjg?t=1346) Ingredients 5 and 6: parallel fleet and daily loop

The day runs on a fixed rhythm: merge the overnight PRs over coffee from 9 to 11, brief tasks and fan out the fleet at 11, then review, merge and re-task all afternoon while most PRs land by evening. Around 19:00 two or three deep jobs (heavy integration, test generation, big refactors, cross-model audits) are specified and left to run overnight. Review is the bottleneck: each morning brings a few large PRs to merge, cherry-pick or re-task over two hours. The speaker describes the resulting role as a manager of agents rather than a developer.

### [27:39](https://youtu.be/0A2jqCqSIjg?t=1659) Why the multiplier was large, and pitfalls

Two properties inflated the gain: massive structural repetition across the panels, and mature documentation for Spring and Hibernate, a stack the speaker himself wrote a book about. Expect closer to 10x than 15 to 20x on less repetitive or worse documented codebases. Four pitfalls close the section: vague briefs that let agents wander, missing tests that remove the trust loop, giant PRs that invite rubber-stamp merges through review fatigue, and weak models whose failures waste the scarcest resource, the human's time.

### [31:18](https://youtu.be/0A2jqCqSIjg?t=1878) The GitHub platform loop

Issues hold the brief, pull requests the review conversation, Actions the CI feedback and Copilot the execution, so the coding agent is one part of a larger loop rather than a standalone tool. Cloud agents offload work from an overloaded laptop but time out after one hour; the mobile app lets him assign issues and review PRs from the tram. GitHub Advanced Security closes the loop further: CodeQL findings land in the PR for the agent to fix, Dependabot feeds version bumps (with a dedicated skill for the volume), and secret scanning covers agent commits too.

### [36:30](https://youtu.be/0A2jqCqSIjg?t=2190) Token economics

Copilot meters fresh input, cached input at a steep rebate, cache writes on some models, and output, which is typically the expensive side. Two audience quizzes make the point: 100,000 cached input tokens ($0.05) cost less than 2,000 output tokens ($0.06) at GPT-5.5 rates, and switching to a half-price model quintuples the next input bill ($0.05 to $0.25) by killing the cache. Cache dies on model switches, instruction edits, tool or history changes, and plain eviction after minutes of idle time. Since micro-optimizing saves cents of tokens against dollars of attention, the recommendation is Auto mode (cache-aware routing, 10% rebate) and, for complex tasks, HydraFusion, a research preview that routes between single-model, cascade and cross-model critique strategies, including local models.

### [44:57](https://youtu.be/0A2jqCqSIjg?t=2697) Live demo: Copilot App and HydraFusion

The closing demo opens the Copilot App that ran agents throughout the talk: a main agent orchestrating subagents, a chat log, and a canvas showing the BootUI 2.0 implementation plan. Session insights show one session running over 200 hours with heavy subagent, shell and MCP-tool usage toward a v2 near 400,000 lines. A new release-prep run is launched in an isolated worktree using the bootui-release skill, autopilot and the HydraFusion preview; the full release takes over an hour through PRs and Actions, so only the launch is shown. Final minute pitches BootUI itself: a local-only console for Spring Boot 4 and Quarkus with advisors, live CVE checks, a CLI, and an opt-in MCP server so agents can read runtime diagnostics.

## Tools, libraries and specs

- BootUI (`github.com/jdubois/boot-ui`, Apache 2.0): Spring Boot 4 / Quarkus developer console, embedded Vue 3 SPA, MCP server, bootui CLI
- GitHub Copilot App, Copilot CLI, Copilot cloud coding agent, GitHub Mobile
- GPT-5.5 Extra-High (sprint workhorse), Claude Opus 4.8, Gemini 3.1 Pro (cross-checks), HydraFusion (research preview, announced 4 Sept 2026), Copilot Auto mode
- Agent skills: Impeccable, orchestrate, agent-merge, bootui-release (custom)
- Eclipse JDT-LS Java language server; JetBrains LSP server (announced at Devoxx)
- Spring Boot 4, Java 17, Vue 3, JUnit, Docker Compose, Playwright, Spotless, ArchUnit, Micrometer/OTLP, Flyway/Liquibase, GraalVM, OSV scanning
- GitHub Actions, CodeQL, Dependabot, secret scanning/push protection

## Who should watch

Developers and leads already using coding agents who want a full workflow (specs, harness, parallel orchestration, overnight runs) rather than another prompt-tips talk; engineering managers weighing what agent-led delivery costs and where review becomes the bottleneck. Skip it if you want framework-free advice: every ingredient is demonstrated inside the GitHub and Copilot stack, and model names and prices will date fast.

## Verdict

**7/10**: A first-hand agent workflow with git-logged numbers, an explained harness loop and an open repository, limited by an estimated solo baseline, a release demo that never completes on screen, and a repository that is the project itself rather than a template.

**Reach broad**: Most of the conference audience uses AI coding assistants daily and can carry the specs-and-tests harness, parallel fleet and overnight-run routine into their own work within the year.

**Novelty 2/2**

- **+** [25:03](https://youtu.be/0A2jqCqSIjg?t=1503) The daily rhythm (merge overnight PRs 9 to 11, fan out at 11, brief two or three deep jobs for the night) is read off the speaker's own commit log, not recommended in the abstract.
- **+** [28:11](https://youtu.be/0A2jqCqSIjg?t=1691) The self-critique names the conditions that inflated the gain (near-identical panels, mature Spring documentation), telling viewers when to expect 10x rather than 15 to 20x.

**Demonstrated 1/2**

- **+** [45:27](https://youtu.be/0A2jqCqSIjg?t=2727) The Copilot App is shown live mid-run with orchestrating agents, a 200-hour session's insights and the BootUI 2.0 implementation board.
- **−** [48:02](https://youtu.be/0A2jqCqSIjg?t=2882) The release-prep run is launched but takes over an hour through PRs and Actions, so no agent task completes on screen.

**Measured 1/2**

- **+** [03:11](https://youtu.be/0A2jqCqSIjg?t=191) With-AI figures (PRs, commits, lines, suites, hours) are extracted from git logs by a stated method.
- **−** [05:50](https://youtu.be/0A2jqCqSIjg?t=350) The 6.5-to-8.5-month solo baseline behind the 15-to-20x claim is the speaker's estimate, not a second measured build.
- **−** [43:22](https://youtu.be/0A2jqCqSIjg?t=2602) HydraFusion is said to be cheaper on simple tasks and better on complex ones ("All our tests show us"), with no test setup or number shown.

**Depth 2/2**

- **+** [14:09](https://youtu.be/0A2jqCqSIjg?t=849) The harness argument explains the mechanism: specs define "done", tests close the loop, and agents iterate to green instead of emitting first drafts.
- **+** [39:11](https://youtu.be/0A2jqCqSIjg?t=2351) The cost trade-off is explained by how the cache works: switching to a half-price model kills the cache and raises the bill, and so do editing AGENTS.md, compacting history and idling for minutes.
- **−** [16:43](https://youtu.be/0A2jqCqSIjg?t=1003) The claim that a better harness beats a better model rests on "a team that proved it", unnamed and unlinked.

**Reusable 1/2**

- **+** [02:40](https://youtu.be/0A2jqCqSIjg?t=160) The BootUI repository holds the build the talk measures: code, AGENTS.md, Copilot instructions, the project's own agents, CI workflows and docs, all inspectable per PR.
- **·** [18:17](https://youtu.be/0A2jqCqSIjg?t=1097) The Impeccable, orchestrate and agent-merge skills ship with Copilot or third parties, so the repository carries only this project's own instantiation of the recipe, not a template for the viewer's.
