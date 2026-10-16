---
title: "Build the Builder: A Java Coding Agent in Your IDE with ACP"
talkId: "24233"
conference: devoxx-be-2026
speakers: [Vadim Briliantov]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=y4F1XBtQeDw
durationMin: 50
slides: null
verdict: 5
reach: segment
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-15
---

# Build the Builder: A Java Coding Agent in Your IDE with ACP
Vadim Briliantov · Conference · Agentic Engineering & Tooling

## TL;DR
JetBrains ACP lead Vadim Briliantov builds a Java/Kotlin coding agent with the Koog framework, connects it to IntelliJ through the Agent Client Protocol, and sketches multi-agent orchestration plus IDE skills that cut wasted agent work. Conference wifi broke the live Gradle build, so parts of the demo land late or unfinished, but the protocol mechanics and the repository survive that.

## Key takeaways
- Build your own coding agent when you need control over context, policy enforcement in code rather than prompts, and your own definition of done.
- Model agents as graphs of typed nodes on the JVM: typed step inputs and outputs act as guardrails that prompts cannot guarantee.
- ACP (Agent Client Protocol, co-developed by JetBrains and Zed) is the standard wire between agents and editors: sessions, streamed updates, permission requests, and a TCK to verify compliance.
- An agent can also be an ACP client, so a thin orchestrator can delegate implement, verify, and repair steps to Claude, Codex, or Gemini.
- IDE intelligence (refactoring engines, JVM debugger logpoints) replaces dozens of agent tool calls; expose it through skills in the Claude-style SKILL.md format.
- Generate a test compatibility kit from your spec first, then prompt agents to comply with the new TCK version instead of describing the change in prose.

## Notes

### [00:41](https://youtu.be/y4F1XBtQeDw?t=41) Why build your own coding agent
Briliantov gives four reasons: you control what context the agent sees and therefore its behavior; you enforce org policies as code with type safety instead of fragile prompts; you define done (which tests must pass) per system; and you can wire the agent into existing SDLC events such as Jira ticket creation, QA delegation, and GitHub pushes. The session plan: build the agent, connect it to the IDE, coordinate external agents (Claude, Codex), and add JetBrains IDE capabilities.

### [04:53](https://youtu.be/y4F1XBtQeDw?t=293) Agent anatomy and typed workflows
An agent is a loop between the agent, one or more LLMs, and an environment: model requests go out, assistant messages, tool calls, and reasoning come back, tools execute, and the workflow decides when to finish. He recommends representing agents as graphs whose nodes have typed inputs and outputs, a natural fit for the JVM. The running example is a three-step graph: inspect code into an issue summary, fix into a solution, verify into a verification result. Koog 1.3 (the Kotlin/Java agent framework he used to tech-lead) supplies the prompt executor, `@Tool`-annotated functions, and graph strategies; Spring AI and LangChain4j are named as alternatives with similar concepts. The key move: guardrail each step with types (a `ChangeSummary` of changed files and added tests, a `Verification` of findings, checks run, and blockers) so the model fills in a data class instead of being asked in prose not to forget fields.

### [10:02](https://youtu.be/y4F1XBtQeDw?t=602) Live vibe-coding the agent with Codex
Switching to IntelliJ with the new JetBrains AIR plugin, he prompts Codex (Astra Medium, full access) to scaffold the coding agent: filesystem and shell tools (read file, edit file, search, execute command), Koog 1.3, OpenAI plus Anthropic models, and the implement/verify/fix graph, pasting the type definitions as a screenshot from his slides. While Codex works he shows AIR's agent picker (Junie, Codex, Amp, OpenCode, installable extras like Droid) and message queueing. Asked in the IDE why `@Tool` methods get re-wrapped in a tool registry, the agent answers that the annotation marks methods for discovery while the registry converts them via reflection into executable tool objects serialized to JSON for the model.

### [13:10](https://youtu.be/y4F1XBtQeDw?t=790) The ACP protocol
ACP connects agents to the places developers write code: 40-plus agents (Codex, Claude Code, Gemini CLI, Junie, Amp among them) and editors including JetBrains IDEs, Zed, Neovim, and now Apple Xcode. The message flow in a nutshell: the IDE sends initialize, the user starts a session, the agent streams session-update notifications (tool calls, edits), may request permissions or form input mid-run, and finally returns a prompt result. Since any agent can also be an ACP client, a super-agent can talk to other agents over the same protocol and expose itself back to the IDE. Compliance is checked with a published TCK (test compatibility kit); he generalizes the advice to any spec-driven work with agents.

### [20:03](https://youtu.be/y4F1XBtQeDw?t=1203) Sub-agents and the actor-like direction
Just-landed ACP sub-agent support lets an agent spawn child agents that each behave as ACP servers the client can observe. The next direction is actor-like agent-to-agent messaging over the same schema: a team lead sends work to a developer agent, QA notifies back, QA can message the developer directly, mirroring human team topology. He positions multi-agent scenarios as the growth area the protocol is preparing for, then notes AIR is built around ACP at its core rather than around chat or model connections.

### [22:39](https://youtu.be/y4F1XBtQeDw?t=1359) Making the agent ACP-compatible
The second live-coding round asks the agent to expose ACP via the ACP Kotlin SDK, streaming tool calls, edits, command runs, and reads, plus instructions for enabling it in IntelliJ IDEA. Walking the pre-built branch, he shows the `observe` function emitting session updates with tool kinds and completion/failure statuses. Enabling means `gradle installDist`, then registering a custom ACP agent in the IDE with the built executable and API keys. The live Gradle build stalls on slow conference wifi, so this segment ends on trust: the agent should stream events like Codex does, but the build never finishes on stage.

### [34:03](https://youtu.be/y4F1XBtQeDw?t=2043) Orchestrating Claude and Codex instead
Pivoting from hand-built harnesses, he proposes using ACP to talk to existing agents and orchestrating from above: Claude implements changes, the custom agent verifies them, Codex repairs failures. He prompts for a strategy in which the Kotlin/Java agent is purely an orchestrator over Claude and Codex via ACP. The workflow is described and prompted but never runs on stage.

### [36:08](https://youtu.be/y4F1XBtQeDw?t=2168) Skills and IDE intelligence
He separates three abstractions: tools define operations the agent can call; skills (SKILL.md) explain how to use tools and handle problem types; guardrails put deterministic logic between steps, via hooks or custom-agent code. Agents waste work for lack of codebase understanding: a 100-file rename costs 100-plus tool calls (search, usages, per-file edits, full Gradle build logs consumed as tokens, rebuild after each fix) where one IDE refactoring would do. The IntelliJ IJ Debugger skill, installed per project and per agent through a skill manager, exposes logpoints on a running JVM over MCP (`xdebug` tools through an `execute_tool` router) so the agent inspects runtime state without rebuilds. JetBrains is working toward a common skills format starting from the Claude-style SKILL.md layout on agentskills.io.

### [45:43](https://youtu.be/y4F1XBtQeDw?t=2743) Late demos and close
The Gradle build finally completes and the custom agent answers in a new session, showing streamed ACP events (file reads with visible output) in the IDE. He then installs the IJ Debugger skill for Codex and invokes it against a real bug in the coding agent; the transcript and frames show MCP `xdebug` calls (debugger status, session control) flowing before time runs out unresolved. The final slide points to the source repository at github.com/Ololoshechkin/build-the-builder-devoxx.

## Tools, libraries and specs
- Koog 1.3 (Kotlin/Java agent framework, ex tech-led by the speaker)
- JetBrains AIR (IntelliJ plugin, ACP-based agent experience) and Junie
- External agents via ACP: Codex (Astra Medium in demos), Claude, Gemini CLI, Amp, OpenCode, Droid
- Spring AI and LangChain4j (named alternatives)
- IntelliJ IJ Debugger skill over MCP (`xdebug` tools, `execute_tool` router); Claude-style SKILL.md / agentskills.io format

## Who should watch
JVM engineers planning to build or buy coding agents, especially anyone integrating agents into IntelliJ or standardizing on ACP, and leads weighing custom harnesses against orchestrating Claude/Codex. Skip if you want ACP protocol reference detail (use the spec and TCK) or a polished uninterrupted demo: the wifi failures eat several live segments.

## Verdict
**5/10**: The ACP lead's own roadmap and a custom agent that streams file reads in the IDE, capped by a stalled build, a failed first run, unmeasured savings claims and a 404 source repository.

**Reach segment**: JVM developers who use IntelliJ and build or integrate coding agents through ACP, a sizable minority of this conference's audience.

**Novelty 1/2**

- **+** [20:03](https://youtu.be/y4F1XBtQeDw?t=1203) The ACP lead describes the just-landed sub-agent support and the planned actor-like agent-to-agent messaging, with his view of where the protocol is heading.
- **−** The agent-anatomy and typed-workflow material, the ACP message flow and the SKILL.md layout match what a search surfaces first: the ACP docs at agentclientprotocol.com and the skills format at agentskills.io.

**Demonstrated 1/2**

- **+** [46:13](https://youtu.be/y4F1XBtQeDw?t=2773) The custom agent answers in a new IDE session with streamed ACP file-read events and their output visible.
- **−** [33:32](https://youtu.be/y4F1XBtQeDw?t=2012) Conference wifi stalls the Gradle build, so the agent-in-IDE segment ends asking the audience to believe it streams events like Codex.
- **−** [46:20](https://youtu.be/y4F1XBtQeDw?t=2780) The first run's turn fails after reading six files with `context_length_exceeded` (311131 of 272000 tokens), and the Codex debugger-skill run ends with no result at [48:53](https://youtu.be/y4F1XBtQeDw?t=2933).

**Measured 1/2**

- **+** [14:14](https://youtu.be/y4F1XBtQeDw?t=854) ACP adoption is backed with a count of more than 40 agents (the captions read "more than 42") and several editors working over the protocol.
- **−** [38:47](https://youtu.be/y4F1XBtQeDw?t=2327) The 105-tool-calls versus one-refactoring comparison is a hypothetical walkthrough with no run, baseline or token counts behind it.
- **−** [41:55](https://youtu.be/y4F1XBtQeDw?t=2515) Logpoints are claimed to bring tremendous token savings with no before/after measurement shown.

**Depth 1/2**

- **+** [16:53](https://youtu.be/y4F1XBtQeDw?t=1013) The ACP message flow is explained stepwise: initialize, session start, streamed updates, permission requests, prompt result.
- **+** [25:17](https://youtu.be/y4F1XBtQeDw?t=1517) The speaker asks Codex in the IDE why `@Tool` methods are re-wrapped, and the answer shows the Koog tool-registry mechanics: discovery via reflection, conversion to executable tool objects, JSON serialization for the model.
- **−** [34:03](https://youtu.be/y4F1XBtQeDw?t=2043) After four reasons to build your own agent at the start, the speaker says there is no reason to build your own harness and switches to orchestrating Claude and Codex, without weighing when each route fits.

**Reusable 1/2**

- **+** [31:11](https://youtu.be/y4F1XBtQeDw?t=1871) The custom ACP agent registration is shown end to end in the IDE: name, command, arguments and environment variables for the API keys.
- **+** [19:00](https://youtu.be/y4F1XBtQeDw?t=1140) For compliance, the talk points to the ACP TCK (github.com/agentclientprotocol/acp-tck) and suggests generating a TCK from any spec before prompting agents.
- **−** [49:24](https://youtu.be/y4F1XBtQeDw?t=2964) The closing slide and QR point to github.com/Ololoshechkin/build-the-builder-devoxx, which returns HTTP 404, so the talk's main content has no published artifact behind it.
