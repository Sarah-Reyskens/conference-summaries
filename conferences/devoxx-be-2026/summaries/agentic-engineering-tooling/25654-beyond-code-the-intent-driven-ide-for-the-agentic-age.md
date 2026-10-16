---
title: "Beyond Code: The Intent-Driven IDE for the Agentic Age"
talkId: "25654"
conference: devoxx-be-2026
speakers: [Bruno Borges]
track: Agentic Engineering & Tooling
sessionType: Tools-in-Action
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=sexe_tnhAOI
durationMin: 35
slides: null
verdict: 5
reach: niche
frames: 18
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Beyond Code: The Intent-Driven IDE for the Agentic Age

Bruno Borges · Tools-in-Action · Agentic Engineering & Tooling

## TL;DR

Borges argues the IDE is becoming a place where developers state intent and orchestrate agents instead of writing code, and demonstrates it live with the GitHub Copilot app: a spec for a Spring Boot to-do app becomes GitHub issues, a fleet of parallel agents implements them, and a custom canvas extension profiles the JVM. The demo lands end to end, including honest failures, and leaves the message that developers stay relevant as system designers who own requirements, flow, and outcomes.

## Key takeaways

- State intent in a spec file first and let agents derive parallel work items from it, rather than prompting for code directly.
- Commit and review the spec before launching parallel agents: Borges launched his fleet against an unmerged SPEC.md and had to unwind the ordering.
- Run coding agents as a fleet with one orchestrator session per workstream so they coordinate and avoid merge conflicts, instead of one long chat.
- Assign brownfield issues straight to an agent from the issue tracker ("assign to agent") for well-scoped fixes; the demo triages a setup-java JDK normalization bug this way.
- Extend the agentic environment with custom canvases (UI plugins driven by the Copilot SDK) for workflows like JFR/GC profiling dashboards.
- Keep the code reviewable outside the agent UI: sessions open in VS Code, IntelliJ, or a terminal, and every change still lands through a normal PR with CI.

## Notes

### [00:37](https://youtu.be/sexe_tnhAOI?t=37) From punch cards to intent

Borges opens with the lineage punch cards (1950s) to the VT100 terminal (60s-80s) to Xerox/Smalltalk IDEs (late 70s), plus a joke about an 80 MB washing-machine-sized hard drive his father brought home. The point: developers have written code in IDEs for nearly five decades, and the next transition is orchestrating agents that write the code. He frames this as good news for engineers, since the job was always turning requirements into predictable, scalable software, not typing. Developers become system engineers and architects who think ahead and design.

### [05:20](https://youtu.be/sexe_tnhAOI?t=320) Tour of the GitHub Copilot app

The demo tool is the GitHub Copilot app, described as a parallel universe to VS Code plus Copilot Chat (comparable to Cursor or Codex-style agent harnesses). The sidebar shows My Copilot, pull requests, issues, Automations (e.g. daily issue triage), and Customize. Sessions run in Interactive, Planning, or Autopilot modes (Autopilot asks the fewest questions) with model choice including GPT-6 Astra, an Auto router, and HydroFusion, GitHub's advanced model router. Extensions cover the usual MCP plugins, connectors, and skills, plus Canvas: custom UI plugins for the environment. A workshop link on screen points to a deeper Copilot app workshop.

### [09:27](https://youtu.be/sexe_tnhAOI?t=567) Initializing a repo without writing code

Starting from a bare Spring Boot (Web + Thymeleaf) to-do app scaffold with only a main method, Borges prompts: do not write code yet, just check the tech stack already in the repo. The agent inspects the tree and writes `copilot-instructions.md` (equivalent to `AGENTS.md`) documenting toolchain, Maven commands, app structure, and task conventions. He reviews the diff and creates a PR for it from the session, then merges it. A brief voice-control attempt fails (transcription model still downloading) and he moves on.

### [13:11](https://youtu.be/sexe_tnhAOI?t=791) Spec-driven development: SPEC.md

In a new session he asks for a specification in SPEC.md for a basic to-do app: name, description, date/time due, category, manage categories. The agent inspects the repo state and drafts scope, data model, and behavior; Borges skims it ("sounds reasonable") rather than auditing line by line. He then prompts "create issues for what can be done in parallel" and the agent files five GitHub issues (persistence foundation, timezone/due-time rules, to-do CRUD, category management, safe category deletion), each self-contained with goal and dependency notes.

### [17:26](https://youtu.be/sexe_tnhAOI?t=1046) Fleet of agents plus a second repo in parallel

The prompt "fleet work to implement the issues in parallel" spawns parallel agent sessions, one orchestrator with child sessions that message each other to coordinate. He also spawns a child session to commit and push SPEC.md. Meanwhile he context-switches to a real bug in the setup-java GitHub Action (used by 1M+ public repos): Temurin `jdk-27+35` rejected by version normalization, where the agent diagnoses that `27+35` is treated as a range and plans shared-normalizer support for JDK-prefixed numeric versions. He is candid that he sequenced this wrong: the fleet started implementing before the spec was merged, and agent workflows need the same flow discipline as code workflows.

### [26:23](https://youtu.be/sexe_tnhAOI?t=1583) Custom canvas: JVM Pulse profiling

Borges installs a canvas extension from a URL and opens JVM Pulse, a custom canvas he built that uses the Copilot SDK to find generated profiling files and chart them. Prompted to "run the Spring Boot, show my JVM, analyze memory usage," the agent picks the Spring Boot example out of a multi-framework repo, enables telemetry, runs the app, and generates a script to collect JFR and GC logs. The live run overruns the slot, so he shows a screenshot of the dashboard instead: 98.89% GC throughput, p99 pause 14.9 ms, allocation rate 232 MB/s (~25.2 GB churned), peak heap 300 MB of 528 MB max, verdict "Garbage collection is healthy."

### [33:45](https://youtu.be/sexe_tnhAOI?t=2025) The fleet lands, with a bug

The to-do implementation completes (+3296/-2 changes across the fleet) and the Spring MVC/Thymeleaf app runs locally: task list, categories, and a new-task form with due date 2026-10-05. Creating a task fails validation on the due-time field ("Invalid value"), which Borges leaves as the closing beat: the next intent is "fix this thing," and that is another talk.

## Tools, libraries and specs

- GitHub Copilot app (Interactive / Planning / Autopilot session modes)
- Copilot SDK (drives custom canvas extensions)
- GPT-6 Astra, HydroFusion model router
- JVM Pulse (speaker-built canvas extension; JFR + Microsoft GCToolkit)
- Spring Boot with Spring MVC + Thymeleaf, Maven
- setup-java GitHub Action, Temurin JDK builds
- VS Code, IntelliJ (open-session targets)

## Who should watch

Developers curious what spec-driven, multi-agent development feels like in practice, and Java developers interested in GitHub's Copilot app and canvas extensions. Skip it if you want Copilot internals or model evaluation; this is a workflow demo with beginner-level framing, not an architecture talk.

## Verdict

**5/10**: A spec-to-fleet workflow with a sequencing mistake shown on screen and a published extension, limited by a failing central demo, unbaselined figures and a basic account of agent coordination.

**Reach niche**: The main content is operating and extending the GitHub Copilot app, so its users and evaluators can use it; the spec-first framing applies elsewhere but takes little of the talk.

**Novelty 1/2**

- **+** [22:46](https://youtu.be/sexe_tnhAOI?t=1366) The speaker launched the agent fleet before the specification was reviewed and merged, and concludes that agent work needs the same flow discipline as code work; this is one live incident and a general lesson.

**Demonstrated 1/2**

- **+** [33:45](https://youtu.be/sexe_tnhAOI?t=2025) The fleet produces a locally running Spring Boot app after the specification and parallel implementation issues are created on screen.
- **−** [34:16](https://youtu.be/sexe_tnhAOI?t=2056) Creating a task fails due-time validation, so the central spec-to-working-application claim is incomplete.
- **−** [31:37](https://youtu.be/sexe_tnhAOI?t=1897) The profiling run is stopped for time and the dashboard is shown as a screenshot instead of a live result.

**Measured 1/2**

- **+** [33:13](https://youtu.be/sexe_tnhAOI?t=1993) The example dashboard reports 98.89% GC throughput, 14.9 ms p99 pause and 232 MB/s allocation, with no baseline or stated method.
- **·** [24:17](https://youtu.be/sexe_tnhAOI?t=1457) The claim that at least one million public repositories use setup-java has no counting method and does not back the talk's workflow claims.

**Depth 1/2**

- **+** [31:06](https://youtu.be/sexe_tnhAOI?t=1866) An orchestrator coordinates child sessions to prevent merge conflicts and overlapping work, which gives a basic reason for the fleet structure.
- **+** [29:00](https://youtu.be/sexe_tnhAOI?t=1740) The canvas uses the Copilot SDK to locate session-generated JFR and GC files and plot their contents, which outlines the extension's data flow.
- **·** [21:40](https://youtu.be/sexe_tnhAOI?t=1300) Sessions messaging each other and reusing a child session's context are mentioned, but the coordination design stops at an orchestrator assigning work.

**Reusable 1/2**

- **+** [26:23](https://youtu.be/sexe_tnhAOI?t=1583) JVM Pulse is installed from a GitHub URL, so the presented extension itself is a reusable distribution.
- **·** [05:51](https://youtu.be/sexe_tnhAOI?t=351) The linked Copilot app workshop gives more instruction, but it is a separate resource that does not reproduce the spec-to-fleet example shown here.
