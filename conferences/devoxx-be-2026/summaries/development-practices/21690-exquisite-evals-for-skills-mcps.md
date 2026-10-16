---
title: Exquisite Evals for Skills & MCPs
talkId: "21690"
conference: devoxx-be-2026
speakers: [Christian Tzolov, James Ward]
track: Development Practices
sessionType: Tools-in-Action
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=mebPFAKSpzw
durationMin: 32
slides: https://jamesward.github.io/exquisite_evals/
verdict: 9
reach: segment
reviewedAt: 2026-10-16
frames: 11
---
# Exquisite Evals for Skills & MCPs
Christian Tzolov, James Ward · Tools-in-Action · Development Practices
Slides: https://jamesward.github.io/exquisite_evals/

## TL;DR
Ward and Tzolov frame evals as a task/arm/judge matrix and apply that frame to a real target: Ward's javadocs.dev MCP server, tested against bare-model, shell, and web-search arms. The headline result is honest rather than triumphant: the server changes helped mechanically but the re-run aggregate regressed, exposing eval bias, single-trial variance, and bugs in the harness itself.

## Key takeaways
- Structure evals as tasks (prompt plus verified reference and facts) crossed with arms (system configurations) and judges, and keep every run so before/after is the comparison.
- Combine three judge kinds: deterministic code checks for exact facts, an LLM judge for meaning and completeness, and a typed decision model (Jev) for many cheap parallel verdicts.
- Run the judge on a different model family than the agent under test, or the judge grades its own habits leniently.
- Read the tool-call transcripts, not just the scores: they showed a 155k-character symbol dump, empty search results, and "latest" resolving to a milestone release.
- Fixing the server can expose bias in the eval: one task had encoded the old "latest means last published" behavior, so the corrected server scored worse on it.
- One trial per task/arm cell cannot separate a system change from model and judge variance; the shell arm moved without any server change at all.

## Notes

### [00:33](https://youtu.be/mebPFAKSpzw?t=33) Goal: use evals to improve an MCP server
Ward (AWS, agent experience) and Tzolov (Spring AI lead) set the target: Ward maintains the javadocs.dev MCP server, which gives agents Java/Kotlin/Scala library documentation access, and the session improves it with evals built on Spring AI.

### [04:10](https://youtu.be/mebPFAKSpzw?t=250) The eval loop: task, arm, judge, metrics
A task is the simulated input plus expected output; an arm is one system configuration (model, prompts, tools); judges grade each answer; metrics cover accuracy, tokens, and time. Runs feed back into fixes manually or, for the adventurous, into a self-improving loop with human approval gates on costly actions. Cost warning: their small matrix already cost tens of dollars in tokens.

### [07:49](https://youtu.be/mebPFAKSpzw?t=469) Tasks carry their own verified answers
Each task pairs a prompt with a reference answer and machine-checkable facts (regexes over versions, method names, "says X doesn't exist"). Ward flags his hardcoded versions as brittle: facts should be fetched from an authoritative source instead.

### [09:23](https://youtu.be/mebPFAKSpzw?t=563) Arms: same model and prompt, only tools differ
The harness is the Spring AI chat client with advisors for token tracking and a per-run budget on tool calls and turns. The shell arm runs inside a Docker sandbox, since letting an agent run curl and unzip on the host is dangerous.

### [11:30](https://youtu.be/mebPFAKSpzw?t=690) Three judge kinds, including Jev decision models
Code checks settle exact facts; LLM-as-judge handles meaning but costs more, varies run to run, and answers one question reliably at a time. Jev (System One style decision models) answers many yes/no and score questions in one fast call with confidence values, but has limited general knowledge: one such model failed "is this a plausible temperature" while Jev passed it.

### [18:14](https://youtu.be/mebPFAKSpzw?t=1094) Demo: the javadocs.dev MCP server live
In claude.ai with the server connected, Ward asks for the latest version of the week-old spring-ai-typesafe library and gets a Maven coordinate back, then asks for a summary of its classes, answered from Maven Central sources.

### [20:21](https://youtu.be/mebPFAKSpzw?t=1221) The experiment: 4 tasks, 4 arms, one model
Tasks need a class-name to artifact to version to API chain: a JevJudge lookup confounded by two libraries with that class, Jackson 3's groupId move, a class existing only in Spring AI 2.1.0-M1, and a trap task with a wrong default plus a nonexistent rubric() method. Arms (base, shell, web-brave, mcp) all use Kimi K2.5; the LLM judge uses DeepSeek V3.2 to avoid same-model bias.

### [22:24](https://youtu.be/mebPFAKSpzw?t=1344) Baseline: MCP wins on accuracy, tokens, and time
MCP passes 3/4 on all three judges with 254k tokens in 19 s average; shell passes 1/4 with 812k tokens in 318 s; web 0/4 with 735k; base 0/4, hallucinating coordinates like com.github.h-thurow:jev:0.3.0. Shell concluded two real libraries don't exist; web invented an AGENT_SHELL_COMMAND variable.

### [24:27](https://youtu.be/mebPFAKSpzw?t=1467) Transcripts become the fix list
Ward fed full tool-call transcripts to an AI coding assistant, which proposed server fixes: version-word-tolerant search, case-insensitive symbol lookup, a symbol-list filter, and latest-release (not last-published) semantics, plus richer tool descriptions. He deployed and re-ran instead of hill-climbing locally against a token target.

### [26:29](https://youtu.be/mebPFAKSpzw?t=1589) After: better mechanics, worse aggregate
MCP fell to 2/4 (1/4 on Jev) with 564k tokens, driven by one 407k-token task; the untouched shell arm also moved, confirming single-trial noise. Per-task, three MCP tasks used 32% fewer input tokens, but the milestone task never opted into pre-releases, and the old "latest" bias in the eval punished the fixed server. Five extra hosted-tool trials passed 1/5.

### [29:03](https://youtu.be/mebPFAKSpzw?t=1743) Inspector replay and harness bugs found
The Spring AI Inspector replays runs as sequence diagrams with per-call LLM traffic and Jev verdicts (one shown: grounded 0.48, fail). The eval work also caught harness bugs: token tracking skipped tool-free calls, the LLM judge scored an empty answer 0.67, and a non-breaking hyphen broke a code check.

## Tools, libraries and specs
- Spring AI 2.1 (chat client, ToolCallingAdvisor, TokenTrackingAdvisor) plus spring-ai-agent-utils (ShellTools, TodoWrite) and spring-ai-typesafe (JevJudge)
- Jev / System One decision models as typed judges
- javadocs.dev MCP server (8 tools) over Maven Central; zio-mavencentral 0.14.1 with coursier version ordering
- Kimi K2.5 via Amazon Bedrock (agent), DeepSeek V3.2 (LLM judge), Brave search via Spring AI community library
- Spring AI Inspector (github.com/tzolov/voxxeddays2026-demo) for replaying eval runs
- Full code, results, and slides: github.com/jamesward/exquisite_evals

## Who should watch
Builders of MCP servers, agent skills, or tool-using agents who want a concrete task/arm/judge pattern with real numbers and failure modes. Skip it if you already run graded eval harnesses with transcript review; the framework half will be familiar and only the javadocs.dev case study adds something.

## Verdict
**9/10**: A before/after eval case study with arms compared on three judges, whose rerun exposes the speakers' own reference-answer bias and is published as a repository; the full improvement loop is only partly shown and each cell is a single trial.

**Reach segment**: Attendees adding LLM features or building MCP servers and agent skills can lift the task/arm/judge pattern into their own eval work within the year.

**Novelty 2/2**

- **+** [24:27](https://youtu.be/mebPFAKSpzw?t=1467) Ward fed the full tool-call transcripts to a coding assistant, deployed the server fixes it proposed and reran the eval, an account of the speakers' own attempted improvement that a tour of eval APIs does not give.
- **+** [27:30](https://youtu.be/mebPFAKSpzw?t=1650) The corrective server change exposed an eval that rewarded the old milestone-as-latest behavior, so the fixed server scored worse on that task because the reference was biased.

**Demonstrated 1/2**

- **+** [18:46](https://youtu.be/mebPFAKSpzw?t=1126) The MCP server answers a live version query about a week-old library in claude.ai and then summarizes its classes on screen.
- **+** [31:09](https://youtu.be/mebPFAKSpzw?t=1869) A replay of an actual run in the Inspector shows a Jev verdict with per-question scores on one of the eval answers.
- **·** [29:35](https://youtu.be/mebPFAKSpzw?t=1775) The speakers do not run the eval live because the suite takes about 30 minutes, so the task-to-judges-to-server-fix loop is shown only through the replay.

**Measured 2/2**

- **+** [22:24](https://youtu.be/mebPFAKSpzw?t=1344) The baseline compares four arms on three judges with total tokens and average time (MCP 3/4 at 254k tokens, shell 1/4 at 812k), under a fixed model, system prompt and turn budget.
- **+** [26:29](https://youtu.be/mebPFAKSpzw?t=1589) After the server changes the same setup reruns to MCP at 2/4 with 564k tokens, with per-task token deltas and five extra hosted-tool trials.
- **−** [27:00](https://youtu.be/mebPFAKSpzw?t=1620) Each cell is a single trial, which Ward calls a bad idea, and the untouched shell arm moved anyway.

**Depth 2/2**

- **+** [12:34](https://youtu.be/mebPFAKSpzw?t=754) The speakers weigh generative judges against decision models through output structure, nondeterminism, parallel questions and confidence values, explaining why each fits a different kind of check.
- **+** [15:13](https://youtu.be/mebPFAKSpzw?t=913) Their weather-check example explains why a decision judge needs sufficient context instead of an assumed store of general knowledge.
- **+** [10:26](https://youtu.be/mebPFAKSpzw?t=626) The harness walkthrough connects the Spring AI chat client, tool-calling advisors, token instrumentation and execution budgets to the controlled arms.

**Reusable 2/2**

- **+** [31:39](https://youtu.be/mebPFAKSpzw?t=1899) The closing points to github.com/jamesward/exquisite_evals, which holds the eval code and results that reproduce the experiment.
- **·** [31:39](https://youtu.be/mebPFAKSpzw?t=1899) The Spring AI Inspector used to replay runs lives in Tzolov's multi-demo voxxeddays2026-demo repository rather than a standalone sample.
