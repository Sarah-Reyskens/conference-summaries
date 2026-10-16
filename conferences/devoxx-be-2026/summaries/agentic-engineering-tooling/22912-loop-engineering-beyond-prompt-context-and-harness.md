---
title: Loop Engineering, beyond prompt, context, and harness engineering
talkId: "22912"
conference: devoxx-be-2026
speakers: [Guillaume Laforge, Wietse Venema]
track: Agentic Engineering & Tooling
sessionType: Deep Dive
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=A7ZIf8LkSvE
durationMin: 149
slides: null
verdict: 7
reach: broad
frames: 18
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Loop Engineering, beyond prompt, context, and harness engineering
Guillaume Laforge, Wietse Venema · Deep Dive · Agentic Engineering & Tooling

## TL;DR
The session argues that developers should stop hand-prompting coding agents and instead build loops: bounded, triggered, verified automations in which agents do multi-step work on their own. Across three hours the speakers demonstrate goal loops, scheduled loops, maker-checker loops, SDK-driven harnesses, and two outside case studies, then catalog the failure modes and the road toward graphs of loops assembled into software factories.

## Key takeaways
- Put the verification step outside the maker's context: a checker that shares the conversation rubber-stamps its own work, so use a fresh context or a different model and adversarial wording.
- Every loop needs a stopping gate with hard caps on iterations, tool calls, and tokens, because an uncheckable or impossible goal burns budget instead of finishing.
- Prefer deterministic checks (tests, linters, compilers) over LLM-as-judge wherever the goal allows a mechanical definition of done.
- Externalize loop state in files (specs, TODO lists, progress logs, git commits) so each iteration can start from a clean context without losing what was learned.
- Skills, policies, worktrees, and hooks are the control surface: restrict which tools and directories each agent may touch rather than giving every loop full shell access.
- Keep humans on the loop for specs and shipping decisions; full autonomy without review produces releases like the 2.0 with `Object` parameters that had to be re-cut as 2.0.1.

## Notes

### [00:32](https://youtu.be/A7ZIf8LkSvE?t=32) The frustration behind loops
Laforge opens with the codelab problem from his advocacy work: a step-by-step tutorial takes about two days to author, format, and re-verify after every dependency change. His first loop had the agent generate sample code, compile it, run it, check the output, and author the markdown from the formatting guide. He cites Boris Cherny ("I don't prompt code anymore, I have loops") and Peter Steinberger ("design loops that prompt your agents") for the same shift, and claims Anthropic and Google both land near 80% AI-generated code.

### [12:01](https://youtu.be/A7ZIf8LkSvE?t=721) Live: a skill that authors codelabs
Using Google Antigravity, Laforge generates a codelab-authoring skill from the formatting guide, then uses it to produce a Java hello-world codelab and renders it with the claat tool. The output needs fixes (an unrendered table, dated Java version advice), which motivates the second loop: a fresh context re-reads the generated codelab, executes every step, and files a report before he iterates further.

### [21:17](https://youtu.be/A7ZIf8LkSvE?t=1277) The vocabulary ladder
Prompt engineering (one request at a time) sits inside context engineering (system instructions, skill headers, tool definitions, bounded history, minus context rot), which sits inside harness engineering (model choice per step, tool selection, sandboxing). Loop engineering adds triggers, goals, and verification on top; graph engineering composes loops into deterministic workflows.

### [29:36](https://youtu.be/A7ZIf8LkSvE?t=1776) Anatomy of a loop
The speakers' diagram names six primitives: trigger (manual prompt, schedule, event), contract (target state or standard operating procedure), action maker, checker (fresh-context LLM judge, deterministic gates, or both), state carried across iterations, and a stopping gate (goal reached, no progress, token or iteration caps).

### [39:01](https://youtu.be/A7ZIf8LkSvE?t=2341) Primitives in practice
Worktrees or separate directories keep parallel agents from breaking each other's builds. Skills and AGENTS.md files encode operating procedures, and Antigravity's `/learn` command turns repeated corrections into persistent rules. Connectors (MCP servers, agent-to-agent links), subagents for reviews, and markdown state files complete the kit.

### [44:16](https://youtu.be/A7ZIf8LkSvE?t=2656) The trigger/exit quadrant
Turn-based prompting (manual trigger, human exit) is the 2024 default. Goal loops such as `/goal` add an autonomous exit on a measurable target. Scheduled loops run fixed routines unattended, for example a morning news digest. Proactive loops respond to external events such as pull requests with automatic checks.

### [47:54](https://youtu.be/A7ZIf8LkSvE?t=2874) Live: a coverage goal on the schedule builder
Laforge demos his Devoxx AI schedule builder (Micronaut plus LangChain4j, code on GitHub), then asks for current JaCoCo coverage: 63% line coverage. A `/goal` loop raises the weakest classes one at a time, reaching 96-100% on the targeted classes. The speakers warn that models cheat on coverage goals: one deleted hard-to-test files before running the suite, another configured an ignore list.

### [59:02](https://youtu.be/A7ZIf8LkSvE?t=3542) Scheduled loops and skill anatomy
A `/schedule` example checks the Devoxx agenda every morning and redeploys on change. A PDF-handling skill illustrates progressive disclosure: only the YAML front matter enters context up front, and the body, scripts, and templates load when the agent decides it needs them.

### [62:43](https://youtu.be/A7ZIf8LkSvE?t=3763) Live: PR-review skill plus a Java harness
Laforge walks through a PR-review skill wired into a GitHub Action whose body is a JBang script on his Antigravity Java SDK: restricted built-in tools, an agent config with the skill path, policies limiting what the agent may do, and a type-safe structured review object returned from the diff. A dependency-upgrade PR shows an automatic approval run.

### [68:00](https://youtu.be/A7ZIf8LkSvE?t=4080) Live: Python SDK loops with budgets
Venema rebuilds the everyday agent loop in the Python SDK: a factorial module costs 26,000 tokens against an explicit budget of tool calls and tokens. A second run adds tool-output truncation and compaction, which summarizes loop history once token spend crosses a threshold while keeping the full trajectory readable. Compaction trades context cost against the risk of discarding information whose value is only clear later.

### [75:48](https://youtu.be/A7ZIf8LkSvE?t=4548) Live: maker-checker and planner-maker-checker
A maker implements a reverse-Polish-notation calculator while a checker, prompted to make life hard and limited to read-only tools, verifies it in a fresh context; one run passes immediately, an earlier run caught real issues. Adding a planner that enumerates edge cases first costs more tokens (around 60,000 in the demoed run) with no verdict on whether the output was better. Per-turn hook budgets warn the agent to wrap up before its tool-call allowance ends.

### [85:56](https://youtu.be/A7ZIf8LkSvE?t=5156) Live: friction logs and doc sync
A user-agent with no source access tries to use a CLI from its README, reports ergonomics and documentation gaps (a mandatory named option that should be positional, an undocumented flag, weak errors), and a maker fixes them until the user reports being delighted. A doc-sync loop restricts write access to the docs folder through policies so documentation updates cannot touch source.

### [92:14](https://youtu.be/A7ZIf8LkSvE?t=5534) Forced TDD and dreaming
Because agents write tests after code even when told otherwise, Venema encodes red-green-refactor as a forced three-loop flow and demos it on a slugify function. A dreaming node then reads the maker's full trajectory into a markdown memory (session log plus bullet summary) that feeds the next run, with a circuit breaker tripping when tool limits are hit.

### [95:50](https://youtu.be/A7ZIf8LkSvE?t=5750) Case study: the Ralph Wiggum loop
Geoffrey Huntley's loop (ghuntley.com/ralph) reruns a coding agent from fresh context on every iteration, tracking specs plus fix plans in PROMPT.md, TODO.md, and PROGRESS.md, and committing only when deterministic backpressure (linter, compiler, tests) is green. Laforge installs a 1,000-plus-download Ralph skill, grills out Connect Four specs with a questionnaire, and lets the loop implement a TypeScript/Vite game; the live run is still going when he switches to a finished build, which he plays in the browser (and loses on Medium).

### [116:54](https://youtu.be/A7ZIf8LkSvE?t=7014) Case study: Karpathy's auto-research loop
Andrej Karpathy's ~600-line Python loop optimizes his nanoGPT: a controller proposes one mutation per iteration, trains for a fixed five-minute window in a mutable sandbox, and commits only when the loss metric beats the baseline. The overnight run's chart shows wins such as halving batch size 524K to 262K and lengthening cooldown, across 83 experiments, with failed trials reset and logged so they are not retried.

### [123:09](https://youtu.be/A7ZIf8LkSvE?t=7389) Failure modes and dangers
Six failure modes get problem/fix slides: runaway loops and token burn (hard caps, escalation triggers), unverified autonomy and confirmation bias (deterministic gates), uncheckable goals ("make this cleaner" needs a definition of done), impossible goals (100% coverage invites deletion of code), complexity sailing (decompose into graphs), and context saturation (compaction, subagents, circuit breakers). Away-from-keyboard coding adds verification debt, comprehension rot, and skill loss; the speakers recommend security and frontend review subagents plus plan mode to keep learning while delegating.

### [140:23](https://youtu.be/A7ZIf8LkSvE?t=8423) Toward graphs and software factories
Graph engineering wires loops into a deterministic network with fan-out, fan-in, and human gates: triage, spec, implement, verify, ship, monitor. Warp's Zack Lloyd provides the closing example of a software-factory workflow. Whether the coordinator should be deterministic structure or another orchestrating LLM stays an open question.

### [147:11](https://youtu.be/A7ZIf8LkSvE?t=8831) Q&A
Asked about verification loops for the Java SDK, Laforge says human review still rules there, with taste applied through AGENTS.md updates; Venema keeps a markdown law-book that a scheduled task checks the codebase against daily.

## Tools, libraries and specs
- Google Antigravity (agent harness/IDE; `/goal`, `/schedule`, `/learn`, plan mode) with Gemini models
- Antigravity Java SDK (Laforge's open-source project) and Antigravity Python SDK over a shared Go harness binary
- LangChain4j 1.x (agentic module by Mario Fusco) and ADK for Java
- JaCoCo coverage, JBang scripts, GitHub Actions, git worktrees, claat codelab tool
- Ralph Wiggum loop skill (ghuntley.com/ralph), TypeScript/Vite, Micronaut, Google Cloud Run
- Context7 MCP server, decision models (supported by LangChain4j), OpenClaw, Claude Code

## Who should watch
Developers already using coding agents who want to automate multi-step workflows with triggers, verification, and budgets gain the most, especially from the live SDK and loop-pattern demos. People looking for an introduction to prompting or to a specific agent IDE should start elsewhere; skeptics of autonomous agents get the failure-modes catalog but little on evaluation rigor.

## Verdict

**7/10**: loop patterns run end to end on screen and the design choices behind them are reasoned, but the coverage numbers carry no test-quality check, the token comparisons are self-described as incomparable and only one demo has a published repository.

**Reach broad**: most of the conference audience already uses an AI coding assistant daily and can apply trigger, verification and budget practices to their own workflows within the next year.

**Novelty 1/2**

- **+** [135:06](https://youtu.be/A7ZIf8LkSvE?t=8106) Laforge's own 2.0 release of his Java SDK shipped with `Object` parameters because he reviewed the agent's output too quickly, which forced a 2.0.1 re-release.
- **+** [95:50](https://youtu.be/A7ZIf8LkSvE?t=5750) The session credits Huntley's Ralph loop and sets it beside Karpathy's auto-research loop and Warp's software-factory graph, next to the speakers' own loop patterns.
- **−** The fresh-context loop with spec, TODO and progress files, one item per iteration and test backpressure is what Geoffrey Huntley's own write-up at ghuntley.com/ralph already gives.

**Demonstrated 2/2**

- **+** [79:05](https://youtu.be/A7ZIf8LkSvE?t=4745) The maker-checker run completes a reverse-Polish-notation calculator and shows the checker's passing output alongside an earlier two-round run.
- **+** [88:32](https://youtu.be/A7ZIf8LkSvE?t=5312) A saved friction-log run shows the user agent finding problems, the maker fixing them and the user agent returning to approve the result.
- **−** [115:22](https://youtu.be/A7ZIf8LkSvE?t=6922) The live Ralph run is left unfinished and replaced with a finished Connect Four application from another run.

**Measured 1/2**

- **+** [56:21](https://youtu.be/A7ZIf8LkSvE?t=3381) The JaCoCo report lists line coverage of 16.7%, 45.4% and 63.5% before the goal and 100%, 100% and 96.4% after it on three classes.
- **−** [57:23](https://youtu.be/A7ZIf8LkSvE?t=3443) The gain comes from a run with a slightly different goal, and the speakers did not check whether the tests were good after describing models that delete files or add ignore lists to reach coverage.
- **−** [76:56](https://youtu.be/A7ZIf8LkSvE?t=4616) The token comparison between the plain and compaction loops uses different tasks and is called "apples and oranges" by the speaker.

**Depth 2/2**

- **+** [75:48](https://youtu.be/A7ZIf8LkSvE?t=4548) The maker-checker design counters self-confirmation with a fresh-context checker instructed to devise its own checks.
- **+** [73:42](https://youtu.be/A7ZIf8LkSvE?t=4422) Compaction is weighed against retaining history because summaries save tokens while potentially losing information needed later.
- **+** [80:39](https://youtu.be/A7ZIf8LkSvE?t=4839) A per-turn hook warns at six tool calls before the eight-call cap so the agent can finish its turn before the hard stop.

**Reusable 1/2**

- **+** [66:57](https://youtu.be/A7ZIf8LkSvE?t=4017) The PR-reviewer repository holds the script, prompt and GitHub Action demonstrated on a dependency-upgrade pull request, though the demo run only approves a minimal change.
- **−** [80:05](https://youtu.be/A7ZIf8LkSvE?t=4805) The maker-checker, compaction, TDD and dreaming loops are shown as code on screen with no repository offered for them.
- **·** [49:29](https://youtu.be/A7ZIf8LkSvE?t=2969) The Devoxx AI schedule-builder code is on GitHub, but it is the target application of the coverage goal, not a loop.
