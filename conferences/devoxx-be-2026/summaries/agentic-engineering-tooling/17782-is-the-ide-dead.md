---
title: Is the IDE dead ?
talkId: "17782"
conference: devoxx-be-2026
speakers: [Martin Lippert]
track: Agentic Engineering & Tooling
sessionType: Lunch Talk
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=jFxR6YYWdmI
durationMin: 35
slides: null
verdict: 4
reach: broad
frames: 7
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Is the IDE dead ?
Martin Lippert · Lunch Talk · Agentic Engineering & Tooling

## TL;DR
Lippert argues the IDE will not die but split into three kinds of tooling: review tools for agent output, managers for fleets of agents, and headless language smartness that serves agents instead of developers. The talk traces this prediction back to why IDEs were built (fast feedback, staying in flow) and shows a live Spring Tools experiment for reviewing agent changes at a Spring-concept level.

## Key takeaways
- Judge dev tools by the original IDE job: fast feedback and keeping the maker in flow, whether the maker is a developer or an agent.
- Reviewing line-level diffs does not scale to agent output; review tooling needs higher-abstraction views (components, framework concepts) over raw changes.
- For review, keep language and framework understanding, navigation, and validations; autocompletion, quick fixes, and snippets lose their value.
- Language servers built for editors can be plugged headless into coding agents (e.g. via the Claude Code marketplace) to give agents fast, precise feedback.
- Tool builders face agents that build their own throwaway tools; plan for the agent as a user with different needs than a developer.

## Notes

### [03:13](https://youtu.be/jFxR6YYWdmI?t=193) Where the IDE came from
The modern IDE traces back to Smalltalk-80's system browser: a graphical interface onto classes and methods where developers inspected and manipulated the system. Smalltalk differed (editing a running system from inside), but the idea of a graphical interface that helps implement software carried through.

### [05:15](https://youtu.be/jFxR6YYWdmI?t=315) What IDEs actually do for developers
Modern IDEs rest on language smartness (frameworks included), used for two things: fast feedback (squiggles, errors while typing, no compiler round-trip) and keeping the developer in flow (completion, hover help, refactoring, no context switch to docs). Source-level debugging and the integration of tests, version control, and builds extend the same no-context-switch idea.

### [10:26](https://youtu.be/jFxR6YYWdmI?t=626) How engineering changed
Many developers moved back to the terminal (Claude Code is the example), with code largely machine-written, many parallel sessions, and constant context switching. The new work is harnesses, guardrails, feedback loops, and tool connections for agents. Even Claude Code is regrowing IDE traits such as a diff panel.

### [14:38](https://youtu.be/jFxR6YYWdmI?t=878) The prediction: the IDE splits three ways
Transferring the original "help create software" idea to the agent era, Lippert predicts IDEs fall apart into: tools to review agent-produced code, small tools to manage fleets of agents and their harnesses, and language tooling that serves the coding agent rather than the developer. A small classic IDE may survive alongside for some tasks.

### [18:15](https://youtu.be/jFxR6YYWdmI?t=1095) Reviewing code, and a Spring Tools demo
Review practice sits on a continuum from reviewing every line to fully autonomous spec-driven runs; the right tooling depends on the stakes (a drug-dosing calculation versus a prototype). The slide lists what review tools need (language and framework understanding, navigation, find-references and call hierarchies, validations, structural overviews, diff views, higher-level review) and what they drop (autocompletion, quick fixes, snippets, new-project wizards). The live demo runs Claude Code in auto-approve mode on Spring PetClinic inside VS Code while the Spring Tools "Logical Structure" view shows only changes at Spring-concept level (new request mapping, query method, repository, entity), so the reviewer tracks direction instead of reading every line.

### [25:28](https://youtu.be/jFxR6YYWdmI?t=1528) Managing fleets of agents
Emerging tools put the agent perspective front and center instead of source code: JetBrains Air, a VS Code Copilot agents mode, and the terminal-based herdr (github.com/herdrdev/herdr), shown as screenshots.

### [27:02](https://youtu.be/jFxR6YYWdmI?t=1622) Language smartness that serves the agent
IDE internals (indexing, navigation, validations) can give agents millisecond feedback without compiler round-trips, keeping agents in flow with fewer tokens. Spring Tools feeds Spring-aware diagnostics and fixes, matched to the project's Spring version, to the agent. Language servers originally built for VS Code are being plugged into Claude Code via the same Language Server Protocol, and debuggers are being opened so agents can steer them directly. Agents still need to learn these tool calls since they were not trained on them.

### [31:40](https://youtu.be/jFxR6YYWdmI?t=1900) Agents building their own tools
Lippert notes agents increasingly write, compile, and run their own throwaway tools instead of using the provided language smartness: personal software for the agent, not the developer. Every future tool must also cope with agents generating vast amounts of code at high speed.

## Tools, libraries and specs
- Claude Code (terminal agent; marketplace language-smartness plugins; auto mode in the demo)
- Spring Tools (VS Code extension; Logical Structure view; Spring-aware diagnostics for agents)
- Language Server Protocol (LSP; reused to plug language servers into agents)
- JetBrains Air (agent-front-and-center IDE)
- VS Code Copilot agents mode
- herdr (https://github.com/herdrdev/herdr; terminal fleet manager)
- Spring PetClinic (demo project); Java language server (Red Hat)

## Who should watch
Tool builders and Spring developers curious where IDE investment is going, and anyone drowning in agent diffs looking for a review strategy. Skip it if you want a hands-on agent-workflow tutorial or measured comparisons of agent tools; this is a direction-setting talk, not a benchmark.

## Verdict
**4/10**: A three-way prediction from a Spring Tools builder, with a live review demo that stops before a verdict; no measurements and no artifact for the thesis.

**Reach broad**: Most of the audience uses AI coding assistants daily and faces the same question of how to review agent output and where tooling goes next.

**Novelty 1/2**

- **+** [14:38](https://youtu.be/jFxR6YYWdmI?t=878) The three-way split (review tools, fleet managers, smartness for agents) is the speaker's own synthesis, carried through the rest of the talk.
- **+** [31:40](https://youtu.be/jFxR6YYWdmI?t=1900) Agents writing and running their own throwaway tools, as personal software for the agent, is his own observation from tool-builder practice.

**Demonstrated 1/2**

- **+** [23:55](https://youtu.be/jFxR6YYWdmI?t=1435) Claude Code runs live on Spring PetClinic while the Logical Structure view surfaces the resulting Spring-concept changes on screen.
- **−** [24:56](https://youtu.be/jFxR6YYWdmI?t=1496) The live run stops after about 90 seconds ("enough auto mode for today"), before any review verdict is reached.
- **−** [25:28](https://youtu.be/jFxR6YYWdmI?t=1528) The fleet-management direction is shown only as screenshots of JetBrains Air, VS Code, and herdr, with nothing running.

**Measured 0/2**

- **−** [13:10](https://youtu.be/jFxR6YYWdmI?t=790) The "Traditional IDE vs. Agent Usage" slide plots IDE usage falling from 100% to about 5% as agent usage rises to 100%, with no data or method behind it.
- **−** [27:34](https://youtu.be/jFxR6YYWdmI?t=1654) Feedback "in milliseconds" and agents that use "less tokens and be faster" are speed and cost claims with no number or comparison.

**Depth 1/2**

- **+** [06:47](https://youtu.be/jFxR6YYWdmI?t=407) The fast-feedback and stay-in-flow principles explain why IDEs succeeded and set up the transfer of those principles to agents.
- **+** [28:35](https://youtu.be/jFxR6YYWdmI?t=1715) The LSP-reuse mechanics (same protocol, headless server, agent needs to learn the tool calls) explain how the third direction works.
- **−** [28:05](https://youtu.be/jFxR6YYWdmI?t=1685) How Spring Tools hands its Spring-aware diagnostics and fixes to the agent is stated in one sentence, with no mechanism shown.

**Reusable 1/2**

- **+** [26:31](https://youtu.be/jFxR6YYWdmI?t=1591) The herdr repository URL is shown on the agents-perspective slide for the fleet-management direction.
- **+** [19:48](https://youtu.be/jFxR6YYWdmI?t=1188) The review-tool keeps-and-drops list (language and framework understanding, navigation, validations kept; autocompletion and quick fixes dropped) is described but left to reconstruct.
- **·** No published artifact covers the talk's main thesis; herdr and Spring Tools each cover one direction only.
