---
title: I Hired a Real Robot as My Junior Dev — and Now My Kids Don't Want to Learn Java Anymore
talkId: "8156"
conference: devoxx-be-2026
speakers: [Jan Van Wassenhove]
track: Mind the Geek
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=P14Fy05Gs38
durationMin: 48
verdict: 7
reach: segment
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-15
---

# I Hired a Real Robot as My Junior Dev — and Now My Kids Don't Want to Learn Java Anymore
Jan Van Wassenhove · Conference · Mind the Geek

## TL;DR
Van Wassenhove built AURA, an open-source agentic "brain" running on a laptop that drives a Reachy Mini desktop robot in his family home, directing coding agents instead of writing code himself. Six subsystems each broke in instructive ways, and every fix landed in the same two places: stating precisely what he wanted, and checking what came back. The thesis: coding is becoming a commodity, while specification, verification and architecture judgment become the senior skills.

## Key takeaways
- Write the security sentence with an attacker in it ("someone who copies this folder gets nothing") instead of accepting "it's encrypted", because his agent happily encrypted records with a passphrase stored next to them.
- Keep told facts and inferred memory in separate stores and never send a minor's inferred profile to a model: the robot once profiled his 11-year-old daughter from background Spotify lyrics and kitchen chatter.
- Draw the room into the architecture diagram, not just the software: a late-night football broadcast fed back through the microphone and made the robot answer questions nobody asked.
- Prefer APIs, CLIs and files over screen control, and keep screenshot-and-mouse automation as an opt-in last resort where every step asks permission.
- Give helper agents read-only tools, a fixed retry budget and no ability to spawn agents, so delegation chains cannot quietly grow into unauthorised work.
- Make fallbacks loud: an echo-mode failure kept the robot answering politely for days with nothing of value behind it, and no test or alert caught any of the six failures, only family members noticing odd behaviour.

## Notes

### [00:35](https://youtu.be/P14Fy05Gs38?t=35) His son ships software without learning Java
His 13-year-old builds and ships apps (a study companion, a gaming crosshair overlay) by describing what he wants instead of typing code, the same way his friends build. Van Wassenhove spent a year assuming this was a shortcut before concluding the boy had skipped ahead to the skill that now matters: specifying precisely and judging results.

### [03:42](https://youtu.be/P14Fy05Gs38?t=222) The robot and the brain it lacked
The body is a Reachy Mini (heard as "Richi Mini" in captions), an open-source desktop robot that ships as a kit with open firmware, simulator and SDK: it moves, speaks, listens and watches, but has no intelligence. The brain is AURA, his own open-source project running on a laptop, which knows who is in the room, remembers what it was told, allows interruptions, drives desktop applications, asks before acting, and revises its own procedures.

### [07:20](https://youtu.be/P14Fy05Gs38?t=440) The thesis: the middle got cheap, the ends did not
An assistant writing one function is cheap to review, but an agent working across 30 files costs more to verify than to do yourself. His workflow: he writes the spec (what it must do, how to tell) and the failing test first, the agent builds one end-to-end fix per commit, and the ledger records each unit. His part is both ends; the machine does the middle.

### [08:56](https://youtu.be/P14Fy05Gs38?t=536) Six containers collapsed into two deployables
The first design was six Docker services (orchestrator, conversation, connectors, memory, identity, robot runtime), which he threw away: six deployables implied an independence that did not exist for one desk robot. The current shape is one brain on the laptop plus one runtime on the robot's Raspberry Pi, with the module boundaries surviving as separately tested packages rather than processes.

### [11:29](https://youtu.be/P14Fy05Gs38?t=689) The trust boundary: steal the robot, get only motors
All keys, profiles and face prints live on the laptop; the robot holds nothing sensitive and every command originates on the laptop. Architecture, in his definition, is naming where trust stops: without named boundaries you have a deployment, not an architecture.

### [12:31](https://youtu.be/P14Fy05Gs38?t=751) Three delegation failure modes
Agents fail faster and quieter than people in three ways: they optimise what was measured rather than meant, verification costs more than the work, and failure is silent. Each of the six chapters maps to one of these, and none of the six failures was caught by tests or alerts.

### [15:04](https://youtu.be/P14Fy05Gs38?t=904) Identity: personas without leaking profiles
A live console demo shows the brain's event stream and configuration. Household members pick a persona (concise assistant, chatty companion) for how the robot addresses them, but the model never receives a profile: a stateless layer builds one short paragraph per turn, with children getting told facts only. Face recognition unlocks personalisation, never decryption; appearance is not a credential.

### [18:11](https://youtu.be/P14Fy05Gs38?t=1091) The passphrase lived next to the lock
After a release wiped the data folder, recognition silently switched itself off because its store had fallen back to unencrypted. A code review then revealed the agent-built design stored the passphrase in a plain settings file above the encrypted records, defeating both the copied-folder and stolen-laptop attacker. The fix: the passphrase moved to the operating system's vault with first-boot self-migration, plus one key per person so forgetting someone means destroying one key.

### [22:22](https://youtu.be/P14Fy05Gs38?t=1342) Told facts versus worked-out memory
Profiles (what somebody said) and memory (what the robot inferred) now live on separate pages and reach the model under different labels. The trigger was a hallucinated personality for his daughter assembled from overheard room audio, including a claim she was "currently in Scandinavia". Nothing inferred about a minor reaches the model unless he opts in.

### [26:30](https://youtu.be/P14Fy05Gs38?t=1590) The loop through the air
Three times the robot answered an empty room at conversational volume; the cause was a televised football match feeding a commentator's fast speech into the microphone, compounded by the robot hearing its own voice. The transcriber emits the most likely sentence, not the true one (his Flemish dialect once came back as Vietnamese). Lesson: the air connecting speaker output back to microphone input is part of the system.

### [29:34](https://youtu.be/P14Fy05Gs38?t=1774) Three loops, three clocks
Seeing never stops, talking runs only when spoken to (interruption is a designed state, not an error path), and upkeep reconnects dropped components every five minutes. Each loop worked alone; the bugs lived between them, including two readers contending for one camera.

### [31:06](https://youtu.be/P14Fy05Gs38?t=1866) The automation ladder
Since most desktop apps lack APIs, the system prompt enforces a six-rung order: API, command line, files, driving the app's own shortcuts (no screenshots), a real browser, and finally screenshot-and-mouse as a fenced, ask-every-step last resort that never touches passwords, payments or terms. A shipped skill may never answer "I can't" without trying; the code sends unattempted refusals back.

### [32:42](https://youtu.be/P14Fy05Gs38?t=1962) Self-improvement gated by a human
After each turn the system asks whether the outcome matched the claim, logs one line per procedure, and periodically drafts skill rewrites, prioritising what keeps failing. It can propose a skill but cannot save one: every change needs his approval of the diff. He once approved a rewrite late at night that silently dropped the never-say-unavailable rule, so shipped skills now get dropped rules restored word for word by code.

### [35:48](https://youtu.be/P14Fy05Gs38?t=2148) Fences around agents that fix the wrong thing
Agents read tirelessly but fix the wrong thing with confidence, so the operative question is what they can reach while wrong. Helpers may look but not touch, get few tries, and cannot spawn sub-agents; per-mode limits (home, work, present) bound the blast radius. A rule only counts as a check in code.

### [38:23](https://youtu.be/P14Fy05Gs38?t=2303) Degraded modes and loud fallbacks
If the internet drops, the robot falls back to a small local model for tool-less chat plus fixed phrases, and keeps retrying the full stack. A subtler failure echoed user input politely for days with only log warnings to show for it. For systems without a visible face, silent fallbacks are bugs that outlast attention, so they must be loud.

### [43:08](https://youtu.be/P14Fy05Gs38?t=2588) Commodity code, scarce judgment
Writing code gets cheap; knowing what to build, how pieces fit, and whether the result is any good does not. He writes almost no code anymore yet builds more than ever, and every robot-built outcome still gets an outcome-level check. The same skills, character and memory settings that serve the household add up to something twin-like per person.

### [45:21](https://youtu.be/P14Fy05Gs38?t=2721) Closing: the first generation of agentic builders
Five days after assembly, his son was already treating the robot as a collaborator. The closing question is whether we are raising the last generation of developers or the first generation of agentic builders; either way, he argues kids should learn to specify, verify and take responsibility for machine-built results. The full brain is open source and runs without the robot hardware.

## Tools, libraries and specs
- Reachy Mini (Pollen Robotics open-source desktop robot: open firmware, simulator, SDK)
- AURA, the speaker's open-source robot brain: `github.com/janvanwassenhove/aura` (runs headless without the robot, pluggable models)
- Raspberry Pi (compute in the robot head, runs the robot runtime)
- OS credential vault holding the data-store passphrase after the settings-file fix
- Fast model for plain turns with escalation to a capable tool-using model on a fixed round budget
- The speaker's blog mityjohn.com (AURA build series, e.g. "AURA 01 · I gave my agents a body")

## Who should watch
Builders of agent systems and tech leads setting agent guardrails get the most: per-person encryption keys, told-versus-inferred memory, the automation ladder and helper-agent fences transfer directly. Viewers wanting reusable code patterns or measured benchmarks should go to the AURA repository or a more technical talk instead.

## Verdict
**7/10**: six household failure post-mortems with design trade-offs weighed, limited by retold demos, self-reported counts, and no artifact beyond the project's own repository.

**Reach segment**: teams building LLM or agent features can use the guardrail rules (threat-model sentences, told versus inferred memory, the automation ladder, helper fences, loud fallbacks) in their own systems.

**Novelty 2/2**

- **+** [23:56](https://youtu.be/P14Fy05Gs38?t=1436) The hallucinated personality for his 11-year-old daughter, including "currently in Scandinavia", assembled from background room audio, motivates the told-facts versus inferred-memory split from his own deployment.
- **+** [28:32](https://youtu.be/P14Fy05Gs38?t=1712) The late-night football broadcast looping through the microphone into empty-room answers, and the lesson that the room belongs in the architecture diagram, come from his household, not from published guidance.
- **+** [40:31](https://youtu.be/P14Fy05Gs38?t=2431) He says none of the six failures came out of a book, and each was discovered while coding the brain and the robot integration.

**Demonstrated 1/2**

- **+** [03:42](https://youtu.be/P14Fy05Gs38?t=222) The Reachy Mini is on stage and, by his account, watching the room, so the body exists and works.
- **+** [15:04](https://youtu.be/P14Fy05Gs38?t=904) The AURA console views (event stream, knowledge, skills, personas) are shown on screen as recordings with fictional data standing in for the household.
- **−** [39:28](https://youtu.be/P14Fy05Gs38?t=2368) The robot-offline view is a recording and the six failures and fixes are retold on slides; none is run on stage to show the before and after.

**Measured 1/2**

- **+** [14:02](https://youtu.be/P14Fy05Gs38?t=842) He reports that none of the six failures was caught by a test or an alert and all were noticed by family members, a self-reported count with no method.
- **−** [07:20](https://youtu.be/P14Fy05Gs38?t=440) The thesis claim that an agent working across 30 files costs more to verify than to do yourself comes with no time or cost figure.

**Depth 2/2**

- **+** [09:56](https://youtu.be/P14Fy05Gs38?t=596) Six Docker services collapse into two deployables because six "implied an independence that did not exist" for one desk robot, with the module boundaries kept as separately tested packages.
- **+** [18:11](https://youtu.be/P14Fy05Gs38?t=1091) The encryption post-mortem works through the threat model (copied folder, stolen laptop), the agent-built flaw, and the per-person-key plus OS-vault fix with its accepted single-copy trade-off.
- **+** [36:20](https://youtu.be/P14Fy05Gs38?t=2180) Helper limits (read-only, few tries, no spawning) are derived from the argument that delegation chains compound into work nobody authorised.

**Reusable 1/2**

- **+** [47:25](https://youtu.be/P14Fy05Gs38?t=2845) The closing slide points to `github.com/janvanwassenhove/aura`, the full brain, runnable without the robot and with pluggable models.
- **·** [47:25](https://youtu.be/P14Fy05Gs38?t=2845) The published material is the presented project's own repository, which the rubric counts as the talk's subject, with no separate sample reproducing the six failure scenarios.
