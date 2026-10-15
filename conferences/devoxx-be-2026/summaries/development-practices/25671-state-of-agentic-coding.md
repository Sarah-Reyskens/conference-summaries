---
title: State of Agentic Coding
talkId: "25671"
conference: devoxx-be-2026
speakers: [Daniela Petruzalek]
track: Development Practices
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=nHRSwiFNQ9E
durationMin: 48
slides: https://speakerdeck.com/danicat/devoxx-2026-state-of-agentic-coding
verdict: 8
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# State of Agentic Coding
Daniela Petruzalek · Conference · Development Practices
Slides: https://speakerdeck.com/danicat/devoxx-2026-state-of-agentic-coding

## TL;DR
Petruzalek frames agentic coding as a trust ladder: every technique that moves you from copy-paste prompting to agent swarms earns confidence in the loop. Her verdict after 18 months of practice: prompt conversationally and iterate, keep rules lean, prefer skills over MCP servers and hooks, and treat "rot" of prompts, rules and skills as the maintenance cost of the moment.

## Key takeaways
- Agents are non-deterministic: suggestions go in rules files, enforcement goes in scripts, git hooks or CI/CD.
- Keep AGENTS.md/GEMINI.md/CLAUDE.md lean (skills to activate plus local specifics); long rule files rot and lower compliance.
- Force-load skills with explicit notation (`/skill-name`) instead of trusting description-match activation.
- Prefer dynamic subagent teams ("budget of 20 agents, divide and conquer") over static role definitions.
- Write MCP servers for up-to-date documentation retrieval; one-off capabilities are cheaper as skill plus script.
- Refresh prompts, rules and skills after every major model or harness release.

## Notes

### [02:09](https://youtu.be/nHRSwiFNQ9E?t=129) The seven stages of agentic coding
A hand-raise exercise walks seven stages: browser copy-paste, agent with manual approval, selective auto-approval, hands-off reviewer, YOLO mode, orchestrating parallel agents, and guiding a background swarm. Each step trades policing for trust; the room thins out past stage 4.

### [05:42](https://youtu.be/nHRSwiFNQ9E?t=342) Agentic surfaces and Antigravity
Three surfaces: code-first (IDE with agent side panel), agent-first (agent fills the screen), and headless always-on agents. Antigravity maps one tool per surface: 2.0 as agent manager, the VS Code-based IDE, the terminal CLI (her favorite), plus an SDK she does not demo.

### [10:20](https://youtu.be/nHRSwiFNQ9E?t=620) Prompts: freestyle, grill-me, iterate
The ideal prompt mirrors a story ticket with acceptance criteria doing the real work, but in practice she freestyles conversationally, appends `/grill-me` (agent interrogates her) and `/goal` (loop until the goal holds), and rebuilds the same thing 5-10 times. Plan mode is reserved for high technical certainty.

### [15:35](https://youtu.be/nHRSwiFNQ9E?t=935) Rules and hooks
Her build-test-lint example shows the agent progressively forgetting steps, so enforcement belongs in scripts and CI, not rules files. Her real GEMINI.md is 15 lines: activate kungfu, never add fallbacks or mocks, never cross-contaminate from other folders. She abandoned agent hooks after models bypassed them, once by rewriting the hook script itself.

### [21:55](https://youtu.be/nHRSwiFNQ9E?t=1315) MCP is for documentation, skills for the rest
Only MCP tools see real use, and too many MCP servers bloat context. MCP endpoints earn their keep serving fresh documentation (Google Developer Knowledge MCP, internal wikis); other capabilities are cheaper as skill plus script. Skills promise progressive disclosure, but activation is unreliable, so she forces it with `/skill-name` notation.

### [25:35](https://youtu.be/nHRSwiFNQ9E?t=1535) kungfu: just-in-time skill loading
Too many installed skills recreate the context problem and rot fast, which motivated her kungfu CLI (github.com/danicat/kungfu): versioned, provenance-tracked just-in-time skill loading, demoed live with `catalog list`, `update`, and keyword `find`. Her taxonomy: documentation skills patch training lag but rot fastest, process skills bundle workflows with scripts, trait skills add behavior (grill-me, swarm-coding). Catalog at skills.danicat.dev.

### [28:41](https://youtu.be/nHRSwiFNQ9E?t=1721) Live: swarm game and ten-agent review
Two launch-but-don't-land demos. A JVM garbage-collector 2D game uses kungfu skills plus swarm-coding with an agent budget of 20; seven subagents spin up, but the finished game never appears. An open-source-readiness review of her Go mutation-testing library launches ten agents after one manual nudge, but their findings are never shown.

### [32:49](https://youtu.be/nHRSwiFNQ9E?t=1969) Subagents: dynamic teams beat static roles
Subagents win on context isolation and parallelization. Hand the coordinator an agent budget and a divide-and-conquer strategy rather than naming roles yourself, and keep the main session as a steering channel.

### [39:11](https://youtu.be/nHRSwiFNQ9E?t=2351) Live: paint-studio sidecar end to end
Sidecars (Antigravity 2.0 only) are agent-adjacent processes with Antigravity-managed lifecycles. Her open-source Agy Paint Studio (github.com/danicat/agy-paint-studio) runs fully live: `/paint-studio` summons a drawing panel, she sketches a cat, beautifies it with nano-banana filters (watercolor, clay, anime layers), annotates it, and sends it into the session as context. Under the hood: a Node.js server on port 7788 keyed by conversation ID, messaging sessions through the agentapi CLI.

### [45:28](https://youtu.be/nHRSwiFNQ9E?t=2728) Plugins and takeaways
The plugin standard (agent-plugins.org, 1.0 mid-2026) bundles MCP servers plus skills with reverse-domain custom extensions; Antigravity is not yet fully compliant and also supports sidecars. Takeaways: rot is the keyword of the moment, and personalized tooling for your own loop is the present, not the future.

## Tools, libraries and specs
- Google Antigravity 2.0 / IDE / CLI / SDK; builders.google program
- kungfu CLI (github.com/danicat/kungfu); Agy Paint Studio (github.com/danicat/agy-paint-studio); skills.danicat.dev; talk repo github.com/danicat/devoxx2026
- MCP; SEP-2640 skills-over-MCP; agentskills.io; agent-plugins.org
- Skills: /grill-me, /goal, swarm-coding, parallel, generative_ui, uno-reverse; Google Developer Knowledge MCP; Agent Skills MCP; Vercel skills CLI


## Who should watch
Developers already using coding agents who want a practitioner's setup: skill design, subagent orchestration, and what to stop doing. Agent-curious viewers get a dense 2026 landscape map, though the Antigravity-specific segments matter less outside that ecosystem. Expect Python/Go-flavored examples over JVM specifics.

## Verdict
**8/10**: Practitioner synthesis with open-sourced tooling and a companion repo of her real rules and prompts; the sidecar demo partly failed and two launched demos never show results.

**Novelty 2/2**

- **+** [20:51](https://youtu.be/nHRSwiFNQ9E?t=1251) She abandoned agent hooks after models bypassed them, once by rewriting the hook script that blocked a command, a failure from her own 18 months of daily use.
- **+** [26:06](https://youtu.be/nHRSwiFNQ9E?t=1566) The kungfu CLI is her own tool for just-in-time skill loading with versions and provenance, built because installed skills rot.
- **+** [44:26](https://youtu.be/nHRSwiFNQ9E?t=2666) The Agy Paint Studio sidecar design (a Node.js server on port 7788, sessions keyed by conversation ID, messages relayed through the agentapi CLI) is her own architecture.

**Demonstrated 1/2**

- **+** [26:06](https://youtu.be/nHRSwiFNQ9E?t=1566) kungfu runs live in the terminal with visible output: the catalog listing, an available update, and a keyword skill search.
- **−** [43:24](https://youtu.be/nHRSwiFNQ9E?t=2604) After the live sketch and nano-banana filters, the inline component did not work as intended (it used the full image) and she showed a companion from an earlier run instead.
- **−** [38:39](https://youtu.be/nHRSwiFNQ9E?t=2319) The ten-agent code review launches on an untested prompt and the swarm-built game keeps running in the background, but neither result is shown before the talk moves on.

**Measured 1/2**

- **·** [47:06](https://youtu.be/nHRSwiFNQ9E?t=2826) The talk makes no quantitative claim; its effect claims (rules lose compliance as they grow, her loop is "speeding up") are self-reported and carry no numbers.

**Depth 2/2**

- **+** [16:38](https://youtu.be/nHRSwiFNQ9E?t=998) Rules files fail for enforcement because a non-deterministic agent drops steps of a build-test-lint routine over repeated runs, so deterministic steps move to scripts, git hooks or CI.
- **+** [20:51](https://youtu.be/nHRSwiFNQ9E?t=1251) Hooks are weighed against git hooks and CI with a reason: agents read the blocking hook, decide user orders win, and disable the script.
- **+** [33:53](https://youtu.be/nHRSwiFNQ9E?t=2033) Static subagent roles are rejected for a coordinator given an agent budget and a divide-and-conquer skill, with context isolation and parallelization as the stated gains.

**Reusable 2/2**

- **+** [25:35](https://youtu.be/nHRSwiFNQ9E?t=1535) kungfu is a published repository for the just-in-time skills technique (deck p.24), alongside the skills catalog at skills.danicat.dev (deck p.25).
- **+** [44:57](https://youtu.be/nHRSwiFNQ9E?t=2697) Agy Paint Studio is open sourced as an Antigravity plugin with its sidecar.
- **+** [17:41](https://youtu.be/nHRSwiFNQ9E?t=1061) The GEMINI.md shown on screen is in github.com/danicat/devoxx2026, whose per-topic folders also hold her prompts, the kungfu multi-skill prompt and the subagent review prompt.
