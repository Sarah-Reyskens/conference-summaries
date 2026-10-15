---
title: "Introducing Agent Control Theory: The System Runs the Model"
talkId: "25661"
conference: devoxx-be-2026
speakers: [Mark Pollack]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=KwQ76IvU59M
durationMin: 52
slides: null
verdict: 9
frames: 11
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Introducing Agent Control Theory: The System Runs the Model
Mark Pollack · Conference · Agentic Engineering & Tooling

## TL;DR
Pollack proposes Agent Control Theory: treat coding agents as measurable systems inside a feedback loop of spec, execution, retained evidence, evaluation, and human-chosen improvement. The system (your specs, workflows, evals) runs the model, not the other way around, which is what makes cost, quality, and vendor portability controllable. He backs the loop with a family of open-source Java libraries and his own measured experiments.

## Key takeaways
- Write the spec before judging the code: 52 behavioral criteria plus 13 architectural rules let an LLM judge find a real locking bug in agent-generated PetClinic code that "looked good" with 290 passing tests.
- Demand evidence, not rulings: eval output should cite code lines and tests like a detective's file, because AI will argue you into any conclusion if you let it.
- Apply the principle of least intelligence: use deterministic tools (compiler, ArchUnit, PMD, coverage, mutation testing) first and spend AI judgment only on what genuinely needs language understanding.
- Keep prompts, plans, research, and evals in a separate steward repository bound to the codebase, not scattered as markdown files polluting every subdirectory.
- Start agent apps by driving an existing agentic CLI programmatically through a portable API instead of writing your own tool-calling harness; drop to a framework calling the completion API only when the CLI proves insufficient.
- Change one variable per experiment and re-analyze retained run logs: comparing simple vs. refined prompts over three runs each showed exploration dropping (150 to 81 explore-to-explore transitions) while writing and building rose from 15% to 23% of classified calls.

## Notes

### [00:34](https://youtu.be/KwQ76IvU59M?t=34) Framing: intent as an artifact
Pollack opens with the enterprise questions: is the AI system working, can it get cheaper, and is the team locked into one vendor. He traces how developer intent evolved from prompts to CLAUDE.md/AGENTS.md files to spec-driven development with plans and specifications up front. His own low-ceremony method keeps three persistent files: vision, design, and roadmap. He quotes Andrew Ng's claim that the biggest predictor of agent-building progress is a disciplined process of eval plus error analysis.

### [05:49](https://youtu.be/KwQ76IvU59M?t=349) The PetClinic case: specs, then judgment
JetBrains advocate Anton used spec-driven development to add a pet-pickup scheduling feature to Spring PetClinic using Timefold, writing 52 EARS-style behavioral criteria and 13 architectural rules (RFC 2119 must/should language). Claude implemented it in about 20 minutes with 290 tests. The spec then doubles as the input to evaluation: an LLM judge checks each requirement against the code. It passed nearly all behavioral criteria but most architectural rules failed, and it caught a locking-order violation with an investigative trail the human could verify.

### [11:04](https://youtu.be/KwQ76IvU59M?t=664) Agent Eval: judges, juries, verdicts
Pollack presents his Java eval library (agent-judge, being renamed agent-eval): a Judge returns a Judgment, a collection of judges forms a Jury that returns a Verdict with a full evidence report. The API follows an AssertJ-fluent style inside JUnit, and judges run on any runtime: agentic CLIs (Claude, Codex, Junie, Grok) or a Java AI framework. LLM-as-judge has two jobs, collecting evidence and then applying logic to rule on it. Conclusions are pass, fail, inconclusive, or not applicable. He also shows Jev, a "text in, judgment out" model that takes an explicit evidence payload.

### [15:18](https://youtu.be/KwQ76IvU59M?t=918) Who judges the judge, and deterministic signals
Pollack spent four hours hand-reviewing the PetClinic code to build a golden set of verdicts, and notes humans glaze over at 500-line files. His answer is to lean on deterministic tools as much as possible: cyclomatic and cognitive complexity give the agent a real numeric signal to iterate against, unlike vague "write clean code". He demos a skill bundling PMD, JaCoCo, mutation testing, Error Prone, ArchUnit, SpotBugs, and NullAway, which he ran against the Java MCP SDK and iterated toward zero findings.

### [22:39](https://youtu.be/KwQ76IvU59M?t=1359) Workflows: Java owns the process
An attempt to combine test generation with a Spring testing-utilities upgrade in one skill failed because the agent ignored the upgrade: too much attention demanded at once. The fix is splitting work into steps, which led Pollack to build a Java workflow engine with a readable DSL mixing deterministic steps and AI steps, with eval verdicts as branch conditions. His PR-review workflow (fetch, prepare, build, build-health verdict, version checks, code-quality and backport AI substeps, jury report) shows the pattern. Steps are swappable beans, so one team's backport assessment can replace the default.

### [26:14](https://youtu.be/KwQ76IvU59M?t=1574) Agent Client: one portable API over 70 CLIs
Agent Client is a Java API that drives any agentic CLI programmatically: create a client with an AgentApi bridge, set a goal prompt plus working directory, and run. The configuration boundary (harness, model, tools, timeout) stays separate from the task boundary (goal, workspace, result), so swapping Claude for Codex is a config change. Pollack, the Spring AI founder, argues most teams should start here rather than building their own harness, since a good harness handles a dozen concerns (tool loop, memory compaction) that the CLIs already solve.

### [30:55](https://youtu.be/KwQ76IvU59M?t=1855) The improvement loop and graduation
After eval, improve exactly one thing: prompt, knowledge, skills, tools, hooks, or shift work from AI into deterministic code (written with AI's help). The stopping rule is cost divided by quality: first prove the task is solvable with the biggest frontier model, then move to smaller models while holding the quality bar. When the loop converges, freeze the judges into a benchmark (inspired by terminal-bench) and the agent "graduates" to production, where runtime monitoring keeps collecting evidence.

### [35:00](https://youtu.be/KwQ76IvU59M?t=2100) Reading the agent's diary
Every agentic CLI writes session files listing every tool call, and Agent Client emits a workflow-aware version of this log that can be re-analyzed months later. Classifying calls (explore, shell, write, build, fix, other) into transition heat maps revealed that a refined prompt plus skills cut explore-to-explore transitions from 150 to 81 and lifted writing plus building from 15% to 23% of classified calls, though cost barely moved ($3.60 vs $3.46). Repeated JaCoCo-report parsing (10 to 15 tool calls per pass) flagged a candidate for a purpose-built tool.

### [42:16](https://youtu.be/KwQ76IvU59M?t=2536) Steward repositories and the full loop
Prompts, research, evals, knowledge bases, and workflows do not belong in the codebase repo. Pollack keeps them in a steward repository: its own git repo with project knowledge, bound to one codebase (one-to-one) or coordinating changes across several (one-to-many, e.g. a portfolio release manager). Stewards become addressable collaborators that can message each other. The closing diagram maps each loop stage to a project: Agent Workflow plus Agent Client (execution), Agent Journal (evidence), Agent Eval (evaluation), ACT analysis (decide and improve), all compared by Agent Experiment. Everything lives at lab.pollack.ai and github.com/markpollack.

### [48:29](https://youtu.be/KwQ76IvU59M?t=2909) Who is in charge, plus Q&A
Pollack warns against handing agent workflows to vendors (Anthropic's built-in workflows lock business logic into one provider) and closes with the Stripe-popularized line: the system runs the model. In Q&A he explains that Anton iterated a full day on the spec itself, talking with AI to draft the EARS and RFC 2119 documents, because the payback is a parseable standard the judge can consume structurally. He also reports turning the RFC judge on his own ACP Java SDK spec conformance: despite PMD, concurrency tests, and a cross-language TCK, it found a real gap (pending permission requests must be answered with cancelled).

## Tools, libraries and specs
- Agent Eval (agent-judge) — JUnit/AssertJ-style LLM judging library with judge, jury, verdict model
- Agent Client — portable Java API over agentic CLIs (Claude Code, Codex, Junie, Grok); AgentApi bridge
- Agent Workflow — Java workflow engine DSL with eval-verdict branching
- Agent Journal — run/evidence ledger for agent workflows
- Agent Experiment — controlled one-variable comparisons with preserved data
- Agent Client Protocol (ACP) — N×M client/CLI integration protocol; Pollack's Java SDK with annotation model
- Jev — text-in/judgment-out model with explicit evidence payload
- EARS requirement syntax and RFC 2119 (must/should/may) for machine-checkable specs
- Terminal-bench — model for freezing evals into a graduation benchmark
- PMD, JaCoCo, ArchUnit, SpotBugs, Error Prone, NullAway, mutation and concurrency testing
- Timefold — scheduling library in the PetClinic pickup-planning example
- lab.pollack.ai and github.com/markpollack — project home and sources

## Who should watch
Java developers and tech leads building or supervising coding agents who want a disciplined eval-and-improve practice rather than vibes. Teams worried about agent cost, vendor lock-in, or merging agent-written code get the most. Skip it if you want Spring AI specifics or hands-on code walkthroughs; this is a framework talk with architecture and results, not a live-coding session.

## Verdict
**9/10**: Original tooling and design rationale for an evaluate-and-improve loop for coding agents, with one A/B experiment and published projects per stage; limited by results shown on slides and a loop never run end to end.

**Novelty 2/2**

- **+** [45:23](https://youtu.be/KwQ76IvU59M?t=2723) The control-theory loop with one dedicated project per stage is the speaker's own design, built on the eval-and-error-analysis loop he credits to Andrew Ng.
- **+** [37:05](https://youtu.be/KwQ76IvU59M?t=2225) The tool-call transition heat maps comparing a simple and a refined prompt are experiments the speaker designed, ran and analyzed himself.
- **+** [47:28](https://youtu.be/KwQ76IvU59M?t=2848) Running the RFC judge on his own ACP Java SDK found a spec gap (pending permission requests must be answered with cancelled) that his tests, PMD and a cross-language TCK had missed.

**Demonstrated 1/2**

- **+** [09:01](https://youtu.be/KwQ76IvU59M?t=541) The locking-violation slide shows eval output from the real PetClinic run, with file references, the rule citation and a proposed improvement.
- **+** [37:05](https://youtu.be/KwQ76IvU59M?t=2225) The heat-map slides display classified tool-call data from real runs of the same task.
- **−** [39:07](https://youtu.be/KwQ76IvU59M?t=2347) The full loop appears as a diagram and pasted outputs; no workflow runs end to end on screen, and the MCP SDK run and the ACP finding are narrated without screen output.

**Measured 2/2**

- **+** [37:36](https://youtu.be/KwQ76IvU59M?t=2256) The prompt comparison states its method on the slide (three runs each, v3) and reports both the footprint shift and the near-identical cost ($3.60 vs $3.46).
- **+** [09:31](https://youtu.be/KwQ76IvU59M?t=571) The PetClinic eval reports exact counts: one abstention among the behavioral criteria and a majority of the 13 architectural rules failing.
- **−** [20:33](https://youtu.be/KwQ76IvU59M?t=1233) The code-quality skill run on the Java MCP SDK is described as "a lot of findings" reduced toward zero, with no counts.

**Depth 2/2**

- **+** [12:40](https://youtu.be/KwQ76IvU59M?t=760) LLM-as-judge is split into collecting evidence and applying logic to it, and numeric scores are rejected as a "magic number" in favor of pass, fail, inconclusive or not applicable.
- **+** [21:05](https://youtu.be/KwQ76IvU59M?t=1265) The principle of least intelligence gives a rule for deterministic tools versus AI, with the complexity-metric example showing why a numeric signal works where "write clean code" does not.
- **+** [31:25](https://youtu.be/KwQ76IvU59M?t=1885) The cost-divided-by-quality stopping rule, with the frontier model run first to prove the task is solvable, says when the loop is done.

**Reusable 2/2**

- **+** [46:27](https://youtu.be/KwQ76IvU59M?t=2787) The projects behind each loop stage (Agent Eval, Agent Client, Agent Workflow, Agent Journal, Agent Experiment) are published at lab.pollack.ai and github.com/markpollack.
