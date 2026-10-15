---
title: "Codepocalypse Now: LangChain4j vs JetBrains Koog"
talkId: "25027"
conference: devoxx-be-2026
speakers: [Viktor Gamov, Baruch Sadogursky]
track: Agentic Engineering & Tooling
sessionType: Deep Dive
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=GGEmc6eR8c4
durationMin: 180
slides: https://drive.google.com/file/d/1jpwSxTC2LbaF2zVeYSHXfLgtMB6afoSq/view
verdict: 8
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14

# Codepocalypse Now: LangChain4j vs JetBrains Koog
Viktor Gamov, Baruch Sadogursky · Deep Dive · Agentic Engineering & Tooling
Slides: https://drive.google.com/file/d/1jpwSxTC2LbaF2zVeYSHXfLgtMB6afoSq/view

## TL;DR
Gamov (LangChain4j, Java) and Sadogursky (Koog, Kotlin) build the same personal AI assistant, J-Claw, twice on stage across seven rounds: chatbot, tools, memory, skills, multi-agent workflows, guardrails, and observability. Each round ends in an audience vote on which framework fits the job better. The lasting message is that context management and agent harness design matter more than raw model choice.

## Key takeaways
- A weak model with good context performs about as well as a frontier model without it; invest in tools, memory, and skills before paying for bigger models.
- Keep deterministic process steps as code (if statements, fixed workflow graphs) and use LLMs only on the fuzzy edges: drafting, summarization, interpreting tool output.
- Agentic skills are Markdown files with YAML front matter whose descriptions load at boot and whose bodies load only when the description matches the request; this progressive discovery keeps prompts small.
- Compose multi-model strategies deliberately: a cheap classifier (JEV) routes requests, a strong model drafts, another judges, and a human approves before anything sends.
- Both frameworks reached the same functional endpoint in every round; the choice comes down to annotation-driven Java (LangChain4j) versus explicit, strongly typed Kotlin graph composition (Koog).
- Instrument agents from the start with OpenTelemetry-based tracing (Langfuse, LangChain4j agent monitor) because token cost and per-node latency are otherwise invisible.

## Notes

### [01:05](https://youtu.be/GGEmc6eR8c4?t=65) Setup: J-Claw, an excuse factory on the JVM
The speakers frame the session as a response to mandatory corporate AI training: they will build J-Claw, a JVM personal assistant (an OpenClaw-style "claw") whose demo job is generating excuses to skip meetings and sending them. Gamov writes the LangChain4j side in Java, Sadogursky the Koog side in Kotlin. No Spring AI appears, by design. Both share one terminal UI built on Tamboui (Cédric Champeau's JVM TUI library) and one recurring prompt ("get me out of basic proficiency run by Dana, do not reuse an excuse"). Show notes, code, and an agentic skill for chatting with the talk live at speaking.jbaru.ch.

### [11:35](https://youtu.be/GGEmc6eR8c4?t=695) Round 1: the two-line chatbot
Gamov wires a Gemini Flash chat model through LangChain4j's AI Service interface with a `@SystemMessage` persona annotation; Sadogursky builds a Koog agent with a system prompt and a read-eval loop in Kotlin. Both bots draft a plausible excuse but know nothing (neither knows who Dana is) and, when told "send it", admit they cannot act. The audience votes LangChain4j's annotation style over Koog's explicit builder for this round.

### [23:36](https://youtu.be/GGEmc6eR8c4?t=1416) Round 2: tools and MCP
Gamov explains the tool-calling mechanism from first principles: the model never executes anything, it emits a tool-execution intent that the agent harness invokes and feeds back. Both sides gain two tools: a calendar reader and an organizer (contact lookup plus email sender), delivered as MCP servers running in separate JVM processes over stdin/stdout pipes. The tools reveal that Dana has a "touchy" sensitivity rating and that three of her sessions were previously declined, so drafts immediately improve. But follow-ups fail: LLMs are stateless, so "send it" has no draft in context, which motivates the next round.

### [37:47](https://youtu.be/GGEmc6eR8c4?t=2267) Round 3: short-term and long-term memory
Gamov adds a 30-message sliding-window chat memory plus a tool that reads past excuses from a JSON-lines file; Sadogursky adds Koog conversation persistence plus a vector-store-backed long-term memory over the same JSON files. The demo now lists avoided excuses (dentist appointment, customer escalation, family obligation) and drafts something new, then successfully sends it. An audience question leads to a discussion of memory compaction: Anthropic's "dreams" distill daily logs into summaries because context windows force a trade between verbatim recall and essence. Both implementations need the same three lines (model, memory, tools), so voting is a wash.

### [54:02](https://youtu.be/GGEmc6eR8c4?t=3242) Round 4: skills at development time and runtime
Skills are reusable Markdown prompts with a YAML `description` that the agent loads at boot, fetching the full body only when the request matches. The speakers use them on two levels: framework skills (Tessl Koog plugin, LangChain4j agent-module skills) taught their coding agents to write the demos, and a runtime "corporate speak" skill rewrites drafts into jargon on a 1-11 Spinal Tap intensity scale. The Koog skill page shows measured impact: unaided agents write Koog prompts correctly about 20% of the time versus 92% with the skill, a 7x improvement. Koog's framework skills exist precisely because Koog 1.0 (May 2026) postdates most models' training cutoffs.

### [75:05](https://youtu.be/GGEmc6eR8c4?t=4505) Break Q&A: prompt caching, live and unscripted
During the break the speakers attempt to answer how to enable provider-side prompt caching in each framework. Koog exposes it as a one-line Anthropic `cache control` parameter; the LangChain4j path requires digging through per-model modules, Javadoc, and eventually an agent-assisted search that surfaces `cacheSystemMessages` mappings. The segment doubles as an honest look at framework maturity gaps and at using coding agents to navigate unfamiliar APIs.

### [91:36](https://youtu.be/GGEmc6eR8c4?t=5496) Round 5: multi-agent workflows and typed graphs
The core technical round. Both sides route every request through JEV, a classification-only model released two weeks earlier: it decides "chat" versus "decline request" in about 16 ms (observed confidences 74-99%). Decline requests flow through a draft (Claude) and review (Codex) loop, visualized as an explicit strategy graph. LangChain4j had just added a `DecisionModel` primitive for JEV-class models; Koog had no JEV support, so Sadogursky wrapped the public JEV protocol by hand. His graph nodes are strongly typed Kotlin edges checked at compile time. Frames show the Koog workflow (chat/decline router feeding draft, verify, refine, and human-critic nodes) and LangChain4j's `AgenticServices` sequence builder. The speakers stress keeping deterministic steps as code rather than asking an LLM to improvise process, and name Embabel's goal-oriented single strategy as a contrasting opinionated design. Koog wins the vote for free-form graph composition.

### [118:52](https://youtu.be/GGEmc6eR8c4?t=7132) Round 6: guardrails as human-in-the-loop
Each side adds a human approval node after the automated reviewer. Sadogursky's CLI stage offers send, hold, or revise; on stage he revises to a dentist appointment at corporate intensity 11 and the loop redrafts, gets Codex approval, and sends. Gamov's LangChain4j human-in-the-loop node stalls when its judge model rejects six consecutive drafts for instruction non-compliance, an unplanned demonstration of overly picky reviewers and the need to bound refinement loops. Gamov's side then starts failing on upstream API errors, which segues into observability.

### [131:53](https://youtu.be/GGEmc6eR8c4?t=7913) Round 7: observability and cost
Sadogursky plugs Koog's OpenTelemetry module into Langfuse with one install plus custom metadata (stage number, JEV model attribution for the hand-written wrapper). The live trace shows the full graph: calendar read, JEV decision at 100%, draft, verify, human-critic refine, approval, send, with 3,335 tokens and per-node cost on the trace. Gamov shows LangChain4j's `AgentMonitor` with an event listener dumping JSON plus a generated HTML system-topology report (loop, router, sequence nodes with data-flow edges), and notes the Micrometer bridge for Spring Boot backends. A spending screenshot makes the cost case: roughly $20,000 at API prices for a month of agent development, absorbed instead by Claude and Codex subscriptions.

### [148:18](https://youtu.be/GGEmc6eR8c4?t=8898) No-code mirror and wrap-up
Sadogursky rebuilds the identical workflow (identify, draft, judge, critic, human approval, corporate-speak skill) in Port's no-code builder, generated through its MCP server rather than drag and drop, arguing teams should choose code or platform per case. Final votes split across Koog, LangChain4j, and undecided; the closing line is that JVM developers win either way, with Josh Long, James Ward, and others covering more JVM-agentics angles later in the week.

### [157:55](https://youtu.be/GGEmc6eR8c4?t=9475) Q&A: governance, local models, debugging
Three threads are worth keeping. On governance: model bans are usually cost control wearing a security costume, and weaker models with strong context close most of the gap (frontier-without-context versus weak-with-context ends up close). On privacy: open-weight local models are the answer when contracts are not enough, and Apple-silicon-class hardware is making laptop inference practical, though RAM prices bite. On debugging agentic apps on call: the JVM side debugs as usual (breakpoints, Flight Recorder, IntelliJ's MCP server feeding a live debugger to an agent), while the hard part is organizational context (past postmortems, tickets, the Alice who knows the deploy procedure), which is the pitch for context-lake systems.

## Tools, libraries and specs
- LangChain4j (AI Services, agentic module, DecisionModel, MCP, guardrails, AgentMonitor, Micrometer bridge)
- JetBrains Koog 1.0 (agents, tool registry, typed graph workflows, OpenTelemetry module)
- JEV classifier model (routing decisions, ~16 ms)
- MCP (Model Context Protocol, stdio and remote HTTP transports)
- Claude (drafting) and Codex (judge/reviewer), via API and via subscription
- Google Gemini Flash (fast demo chat model)
- Langfuse (OpenTelemetry trace backend for agents)
- Tessl Koog plugin (`tessl install jbaruch/koog`, framework skills with evals)
- Tamboui (JVM terminal UI library)
- Port (no-code agent workflow platform, MCP server)
- Embabel (goal-oriented agent composition, mentioned in passing)
- Anthropic prompt caching (`cache control`, dreams memory compaction)

## Who should watch
JVM developers evaluating LangChain4j or Koog for agent features, or anyone wanting a single end-to-end tour of tool calling, memory, skills, workflows, guardrails, and observability with both frameworks side by side. Python agent builders can skip the code but may still take the strategy and context-management arguments. Viewers short on time can skip the break Q&A's prompt-caching search and the Port sales segment.

## Verdict
**8/10**: A paired JVM-agent build with beginner-level explanations and complete published implementations, limited by an incomplete LangChain4j workflow demonstration and measurements without stated methods.

**Novelty 2/2**

- **+** [07:55](https://youtu.be/GGEmc6eR8c4?t=475) The same assistant is built twice across seven stages from chatbot to observed workflow, a head-to-head comparison no single-framework tutorial offers.
- **+** [105:15](https://youtu.be/GGEmc6eR8c4?t=6315) Koog ships no JEV support, so the speaker wraps the public classifier protocol by hand to route requests in the live workflow.

**Demonstrated 1/2**

- **+** [103:08](https://youtu.be/GGEmc6eR8c4?t=6188) Koog's draft-review loop redrafts after Codex rejects the first candidate and delivers the excuse live.
- **+** [126:09](https://youtu.be/GGEmc6eR8c4?t=7569) After the Koog human-critic revise round, Codex approves the redraft and the excuse is delivered live.
- **−** [128:46](https://youtu.be/GGEmc6eR8c4?t=7726) LangChain4j stops at its six-refinement safety bound with nothing sent, and subsequent upstream rejections leave its final draft-review-send workflow incomplete on stage.

**Measured 1/2**

- **+** [60:52](https://youtu.be/GGEmc6eR8c4?t=3652) The skill page reports about 20% success unaided versus 92% with the Koog skill for prompt-writing tasks.
- **+** [140:51](https://youtu.be/GGEmc6eR8c4?t=8451) The live trace reports 3,335 tokens and per-node costs for the demonstrated workflow.
- **−** [161:33](https://youtu.be/GGEmc6eR8c4?t=9693) The claim that a weaker model with context nearly matches a frontier model without it has no reported evaluation results, while the earlier skill percentages lack a stated method and the trace lacks a comparative baseline.

**Depth 2/2**

- **+** [24:09](https://youtu.be/GGEmc6eR8c4?t=1449) The tool-calling loop is explained from first principles: the model emits an execution intent, the harness invokes the tool and feeds the result back.
- **+** [113:42](https://youtu.be/GGEmc6eR8c4?t=6822) Deterministic process steps stay as code instead of paying a stochastic model to re-decide them, grounding the workflow argument in cost.

**Reusable 2/2**

- **+** [10:00](https://youtu.be/GGEmc6eR8c4?t=600) The published speaking.jbaru.ch page links both complete demo repositories, runbooks, seven chapter checkpoints and the talk's agentic skill.
- **+** [67:04](https://youtu.be/GGEmc6eR8c4?t=4024) The corporate-speak skill is a Markdown file whose YAML description triggers loading when the user asks for a corporate or jargon version.
