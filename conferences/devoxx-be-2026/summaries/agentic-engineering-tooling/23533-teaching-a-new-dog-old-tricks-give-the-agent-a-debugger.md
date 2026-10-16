---
title: "Teaching a New Dog Old Tricks: Give the Agent a Debugger"
talkId: "23533"
conference: devoxx-be-2026
speakers: [Anton Arhipov]
track: Agentic Engineering & Tooling
sessionType: Tools-in-Action
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=rk22mStXsGU
durationMin: 35
slides: null
verdict: 6
reach: segment
frames: 9
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Teaching a New Dog Old Tricks: Give the Agent a Debugger

Anton Arhipov · Tools-in-Action · Agentic Engineering & Tooling

## TL;DR

IntelliJ IDEA's debugger exposes JVM runtime capabilities (logpoints, method breakpoints, dependent breakpoints, thread suspend policies) that coding agents can drive through the bundled ij-debugger skill over the IDE's MCP server. The talk's thesis is logpoint-first debugging: agents should gather runtime evidence with non-suspending breakpoints instead of editing code to add print statements. Three live agent demos fix a stream bug, trace a reflective call, and reproduce a race condition.

## Key takeaways

- A logpoint (non-suspending breakpoint with evaluate-and-log) gives agents println-style output without touching source, and works in compiled third-party code they cannot edit.
- The ij-debugger skill, bundled in IntelliJ IDEA under Settings > Skills, installs into `.agents/skills/ij-debugger` and instructs the agent to collect logpoint/breakpoint evidence before concluding anything.
- Agents reach the debugger through one MCP router tool, `mcp.idea.execute_tool`, with commands such as `xdebug_set_breakpoints` carrying breakpoint specs as JSON.
- Method breakpoints set on an interface method instrument every implementation, which catches reflective invocations and generated proxies that text search cannot find.
- Dependent breakpoints (a suspending breakpoint disabled until a non-suspending marker breakpoint is hit) isolate one path through diamond-shaped call flows.
- A per-thread suspend policy plus logpoints lets an agent reproduce a race condition: the added evaluation latency alone can widen the interleaving window enough to fail the test.

## Notes

### [00:34](https://youtu.be/rk22mStXsGU?t=34) Debugger features as a runtime protocol

After a recap of basics (inspect state, mutate values live, HotSwap class replacement), the speaker makes the framing point: these are JVM runtime capabilities exposed through a protocol, and the IDE window is only one client. CLI and agent tools can call the same API. A refresher on stream lambda breakpoints and the "trace current stream chain" visualization follows, showing step-by-step how filter/map stages transform elements.

### [06:47](https://youtu.be/rk22mStXsGU?t=407) Demo 1: agent debugs a stream distinct() bug

A stream pipeline should return unique in-stock offers with positive prices but emits "Keyboard" twice (a BigDecimal equality/scale bug). The prompt names the expected result and the duplicate. The agent reads the ij-debugger skill, issues `mcp.idea.execute_tool` calls that install logpoints via `xdebug_set_breakpoints` (log expressions capture product, scale, hashCode, equals-vs-compareTo against 49.90), confirms the duplicate, then removes the breakpoints and applies the fix. Each logpoint also collects a stack trace as evidence of why it fired.

### [12:02](https://youtu.be/rk22mStXsGU?t=722) Demo 2: method breakpoints catch a reflective call

A method breakpoint on an interface method stops in the implementation, and wildcards (`*`) intercept runtime-generated code such as proxies. The example hides a reflective `getMethod(new String(new byte[]{0x66, 0x6f, 0x6f}}))` call (decodes to "foo") that no text search finds. Asked why method `foo` executes, the agent sets a method breakpoint, captures the stack trace showing the reflective invoke frame, and reports the decoded name as evidence.

### [20:20](https://youtu.be/rk22mStXsGU?t=1220) Logpoints, the core technique

On a cache singleton example: a suspending breakpoint plus manual evaluate-expression (`instance = null`) gets tedious, so the same is automated with evaluate-and-log and suspend disabled. That combination is what the talk calls a logpoint. Developers add println lines to locate where to put a breakpoint; agents do the same, so the skill tells them to gather evidence from logpoints instead. Logpoints also work in libraries whose source cannot be modified.

### [25:02](https://youtu.be/rk22mStXsGU?t=1502) The ij-debugger skill and MCP wiring

The skill ships bundled with IntelliJ IDEA and installs per project or globally for Codex and Claude agents (visible in the frame: "ij-debugger", "Debugger-first runtime root-cause analysis for JVM code"). Its text states the logpoint-first principle, mandates `execute_tool` as the exclusive path for debugger calls, and lists safe logpoint-expression rules. Beyond the debugger, the IDE exposes a growing tool list over the same MCP server.

### [26:36](https://youtu.be/rk22mStXsGU?t=1596) Dependent breakpoints for diamond flows

In a step1 -> step2 -> step3/step4 -> output diamond, the goal is to stop in `output` only when reached via step4. A non-suspending marker breakpoint on the step4 path plus a second breakpoint configured as "disabled until" the marker hits does it; the two render with different colors and shapes. The speaker notes most agent value comes from logpoints and stepping, with the rest needing explicit skill instructions to be usable by agents.

### [30:15](https://youtu.be/rk22mStXsGU?t=1815) Demo 3: agent reproduces a race condition

A test has two threads check-then-add to a synchronized collection; it passes locally and in CI but fails intermittently. "Repeat until failure" run configuration is mentioned but too slow to wait for. The agent adds two logpoints; the few milliseconds of evaluation latency shift the interleaving so both threads skip the guard and the test fails on the first run. The manual equivalent is a breakpoint whose suspend policy is set to the hitting thread only, so each thread can be stepped separately.

## Tools, libraries and specs

- IntelliJ IDEA debugger (logpoints, method breakpoints, dependent breakpoints, stream chain tracing, per-thread suspend policy, repeat-until-failure)
- ij-debugger agent skill (bundled; installs to `.agents/skills/ij-debugger`)
- IntelliJ IDEA MCP server (`mcp.idea.execute_tool`, `xdebug_set_breakpoints`)

## Who should watch

JVM developers who pair with coding agents (Junie, Claude, Codex) and want cleaner agent debugging than println edits, plus anyone who uses IntelliJ breakpoints only to suspend on a line. Skip if you already drive the ij-debugger skill daily: the breakpoint tour replays the speaker's earlier debugging talks.

## Verdict

**6/10**: the agent gathers runtime evidence in working debugger demos with reasons for choosing logpoints, but the talk is a feature tour of the speaker's own product, with anecdotal timing and no sample project.

**Reach segment**: IntelliJ IDEA users who pair coding agents with JVM debugging can apply the bundled skill and breakpoint workflows.

**Novelty 1/2**

- **·** [01:06](https://youtu.be/rk22mStXsGU?t=66) The speaker combines his earlier debugger material with agent workflows, a product-feature tour rather than production experience or a tested cross-tool decision framework.

**Demonstrated 2/2**

- **+** [09:28](https://youtu.be/rk22mStXsGU?t=568) The stream example ends with the agent confirming the duplicate, removing its breakpoints and applying the fix for the BigDecimal equality bug.
- **+** [18:46](https://youtu.be/rk22mStXsGU?t=1126) The agent sets breakpoints, captures the runtime stack and confirms the reflective invocation of foo.
- **+** [32:52](https://youtu.be/rk22mStXsGU?t=1972) Agent-installed logpoints reproduce the intermittent concurrency failure.

**Measured 1/2**

- **+** [31:16](https://youtu.be/rk22mStXsGU?t=1876) Repeat-until-failure is reported to take sometimes seven seconds and sometimes minutes.
- **−** [33:22](https://youtu.be/rk22mStXsGU?t=2002) The claimed few milliseconds of logpoint overhead are not timed, and the reproduction has no repeated-run comparison.

**Depth 1/2**

- **+** [22:58](https://youtu.be/rk22mStXsGU?t=1378) The explanation connects println instrumentation to the difficulty of locating a breakpoint, motivating logpoint-first evidence gathering.
- **+** [24:31](https://youtu.be/rk22mStXsGU?t=1471) Runtime instrumentation is useful in library code that agents cannot modify.
- **·** [08:26](https://youtu.be/rk22mStXsGU?t=506) The skill is described as supplying tool order and guardrails, but the walkthrough concentrates on invoking it rather than explaining its investigation decisions.

**Reusable 1/2**

- **+** [25:02](https://youtu.be/rk22mStXsGU?t=1502) The bundled ij-debugger skill can be installed into the project's .agents/skills directory, providing the presented product's own distribution.
- **−** [34:23](https://youtu.be/rk22mStXsGU?t=2063) The talk closes with an invitation to the booth and names no sample project that reproduces the demo programs.
