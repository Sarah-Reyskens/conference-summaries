---
title: "Eval Driven Development: Why you need it to make your Agentic Application survive Production"
talkId: "10038"
conference: devoxx-be-2026
speakers: [Urs Peter]
track: Agentic Engineering & Tooling
sessionType: Lunch Talk
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=4qeUklTLyTs
durationMin: 40
slides: null
verdict: 7
frames: 8
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Eval Driven Development: Why you need it to make your Agentic Application survive Production
Urs Peter · Lunch Talk · Agentic Engineering & Tooling

## TL;DR
Urs Peter argues that agentic apps die in production because teams test probabilistic systems with deterministic habits, and presents eval-driven development: layered evals, golden datasets, calibrated LLM judges, and a production feedback loop. Using the JVM framework Dokimos and a Devoxx conference assistant built for the talk, the evals catch tone drift, hallucinations, and scheduling conflicts on screen, and a production complaint becomes a regression test.

## Key takeaways
- Treat agent quality as a reliability metric with bounds, not pass/fail: the achievable guarantee is that quality stays within limits.
- Build the eval pyramid bottom-up: cheap deterministic checks first, then ground-truth and validity evals, then LLM-judged quality levels, with humans at the top.
- Define what the agent must not do as explicitly as what it must do; that contract seeds the test data.
- Calibrate LLM judges the way you would any instrument: pin model and temperature, check score variance on a frozen set, compare against manual scores.
- Intercept every contact point between the agent and other components: tool trajectories, RAG context relevance, and whether answers stay faithful to context.
- Ship a feedback button and trace everything; convert bad production traces into failing tests and sample the rest to grow the golden dataset.
- Red-team agents before production; Promptfoo is a starting point since most open-source eval frameworks lack security depth.

## Notes
### [01:33](https://youtu.be/4qeUklTLyTs?t=93) The production gap
A stand-up poll shows many attendees built agents, fewer shipped one, and four used evals. Gartner forecasts 40% of agentic projects canceled by end of 2027 for unproven value, uncontrolled risk, and unsafe scale. 89% of companies have production observability but only 52% use evals, so barely half test the software they ship. The Sorcerer's Apprentice frames the talk: unlike the apprentice, no wizard returns to undo your agent's damage.

### [05:08](https://youtu.be/4qeUklTLyTs?t=308) Why agents break traditional testing
Traditional systems are specification-driven and largely deterministic, with finite code paths covered by test pyramids and coverage metrics. Agent systems are behavior-driven and probabilistic, shown by tracing one refund request: ambiguous human context, LLM sampling, conversation history making each request unique, RAG chunking and embedding choices, tool and MCP selection, agent-to-agent calls, and the user's own mood. Traditional systems carry uncertainty at the edges; agent systems carry it at the core.

### [07:43](https://youtu.be/4qeUklTLyTs?t=463) Eval-driven development: the mindset shift
Binary pass/fail gives way to a reliability metric that checks whether quality stays within bounds. EDD goals: measurable quality criteria, statistical regression detection across model and tool changes, production data feeding improvement, and control of cost, latency, security, and risk.

### [09:46](https://youtu.be/4qeUklTLyTs?t=586) Test data and the golden dataset
Before generating data, define the agent's goal including must-not-dos, user profiles, happy flows, edge scenarios, and constraints. Feed those to an LLM to draft test inputs, then manually review them against expected users. Production data later evolves the set into the golden dataset, which reflects real behavior with edge cases and failure modes and serves as the agent's life insurance.

### [11:48](https://youtu.be/4qeUklTLyTs?t=708) Demo app and JVM tooling
The demo agent is a Devoxx assistant: static venue info, semantic search over a chunked and vectorized program schedule, and personalized-track operations. Test users and scenarios are drafted in a Kotlin notebook through a Spring AI chat client. Most eval frameworks are Python or TypeScript and Spring AI's eval support is basic, so the talk uses Dokimos, a JVM framework supporting Spring AI, LangChain4j, Koog, and Embabel, whose Kotlin integration is the speaker's own contribution; its docs live at dokimos.dev.

### [16:24](https://youtu.be/4qeUklTLyTs?t=984) Deterministic evals: the pyramid base
The first eval is a plain unit test in the Dokimos Kotlin DSL: a dataset, an example asking the Devoxx Belgium venue, a task calling the chat controller, and a `contains` evaluator. It passes. Deterministic checks form the pyramid base because they are cheap, binary, and reliable, with ground-truth checks one level up.

### [17:57](https://youtu.be/4qeUklTLyTs?t=1077) LLM-as-judge and the pirate fix
The test engine runs the agent under test, then hands artifacts (history, prompts, context, response, expected output, criteria, tool trajectory) to a judge LLM whose score is compared to a threshold, optionally averaged over grades. The caveat is stated plainly: a probabilistic system tests a probabilistic system, so use a judge model at least as good as the agent's, with pinned version and temperature 0. A pirate-language input scores 0.62 against a formal-tone criterion; a system-prompt fix follows, and a live re-run scores 0.95.

### [23:35](https://youtu.be/4qeUklTLyTs?t=1415) Eval hook points and the parking hallucination
Every agent-component contact is interceptable: RAG retrieval judged for context relevance, precision and recall checked deterministically, context faithfulness verified in both directions, task completion scored, and tool trajectories compared to expectations. The parking demo asks about venue parking the data never mentions; the agent invents available spaces, and tool-correctness (via Spring's tool-call recorder) plus faithfulness and hallucination judges fail it. The faithfulness judge splits input into truths and output into statements and verdicts each one; mostly "I don't know" verdicts produce the low score.

### [28:14](https://youtu.be/4qeUklTLyTs?t=1694) Conversation simulation and judge calibration
The Dokimos conversation simulator pairs a persona-driven simulated user with the app under test, bounded by max turns and a stopping condition. Judges score goal achievement and satisfaction while a deterministic check rejects overlapping sessions. The run scores well on conversation quality but fails the overlap check, a flaw only visible across turns; such suites cost real money in LLM calls. Calibration answers "who evaluates the judges": rerun a frozen set, check score variance, pin model and temperature, score queries manually for comparison, tune prompt and config, and recalibrate as production data arrives.

### [32:51](https://youtu.be/4qeUklTLyTs?t=1971) Security gets a pointer
Security deserves its own talk, so the advice stays brief: red-team agents before production the way traditional apps get penetration tests. Promptfoo, with many checks programmed in, is a good starting point; Dokimos and most open-source frameworks lack depth here.

### [34:23](https://youtu.be/4qeUklTLyTs?t=2063) Production: sitting the agent
Shipping creates a new role, the agent-sitter. Trace everything (prompts, responses, latency, tokens, tool calls, errors) via OpenTelemetry into Langfuse, which is mostly configuration, and give users a feedback button. The demo complaint: asked for parallel sessions still attendable, the agent suggests slots from Monday noon. Monitoring plus random sampling turns bad traces into failing tests, grows the set toward the golden dataset, calibrates judges on real data, and exposes systematic failures. A feedback-sorter notebook classifies Langfuse feedback (one item: medium severity, 96% confidence), a regression test proves past sessions were suggested, and the fix is announced. Humans top the pyramid through high-risk review, calibration, and sample review, closing the loop: Identify, Build EDD Harness, Logging, Refine/Extend Evals.

## Tools, libraries and specs
- Dokimos (dokimos.dev): JVM eval framework with Spring AI, LangChain4j, Koog, and Embabel support, a Kotlin DSL, a conversation simulator, and workflow skills
- Spring AI: chat client for test-data generation and the demo agent; tool-call recorder for trajectory capture
- LangChain4j, Koog, Embabel: supported agent frameworks (named)
- Promptfoo: starting point for security and red-team checks
- Langfuse: trace store fed via OpenTelemetry
- Kotlin notebook: scratchpad for test-data generation and the feedback sorter
- A2A protocol, MCP servers: named as multipliers of agent unpredictability

## Who should watch
JVM developers shipping or about to ship agent apps who need a practical eval workflow from first test to production loop. Skip it if layered evals with calibrated judges and a production-to-regression loop already run in your team, or if you came for LLM security depth, which the talk sends elsewhere.

## Verdict
**7/10**: A full eval lifecycle run on screen with real trade-offs explained, limited by single-run scores without spread and no sample repository.

**Novelty 1/2**

- **+** [11:48](https://youtu.be/4qeUklTLyTs?t=708) The Devoxx assistant demo app, from semantic program search to personalized tracks, carries the talk on the speaker's own example.
- **+** [14:21](https://youtu.be/4qeUklTLyTs?t=861) The JVM framework survey centers Dokimos, whose Kotlin integration is the speaker's own contribution.
- **−** Eval-driven development itself is already covered by the Red Hat eval-driven development article (March 2026) and evaldriven.org, so the concept framing is shared ground.

**Demonstrated 2/2**

- **+** [22:34](https://youtu.be/4qeUklTLyTs?t=1354) The pirate-tone eval fails at 0.62 on screen, a system-prompt fix follows, and a re-run scores 0.95.
- **+** [26:42](https://youtu.be/4qeUklTLyTs?t=1602) The parking hallucination run fails its faithfulness judges with the per-verdict breakdown visible.
- **+** [30:18](https://youtu.be/4qeUklTLyTs?t=1818) The conversation simulation run shows the judges passing while the deterministic overlap check fails.

**Measured 1/2**

- **+** [23:04](https://youtu.be/4qeUklTLyTs?t=1384) The tone score moves from 0.62 to 0.95 after the prompt fix, with the criterion, threshold, pinned model and temperature 0 shown as the method.
- **−** [23:04](https://youtu.be/4qeUklTLyTs?t=1384) Each score is a single judge run with no spread, although the speaker's own calibration advice at [31:20](https://youtu.be/4qeUklTLyTs?t=1880) is to rerun a frozen set and check standard deviation.
- **−** [04:06](https://youtu.be/4qeUklTLyTs?t=246) The 89% observability and 52% eval-use figures are given without a source or method.

**Depth 2/2**

- **+** [05:08](https://youtu.be/4qeUklTLyTs?t=308) The refund-request trace grounds the probabilistic-core argument in each compounding uncertainty source.
- **+** [20:31](https://youtu.be/4qeUklTLyTs?t=1231) Judge design trade-offs are weighed: a judge at least as good as the agent, pinned version and temperature 0, and threshold versus grade-point average at higher cost for more stable results.
- **+** [27:13](https://youtu.be/4qeUklTLyTs?t=1633) The faithfulness internals show truths-versus-statements verdicting, not only the resulting score.

**Reusable 1/2**

- **+** [14:21](https://youtu.be/4qeUklTLyTs?t=861) Dokimos is named with its docs site, supported frameworks, workflow skills and Kotlin DSL shown in use.
- **−** [39:59](https://youtu.be/4qeUklTLyTs?t=2399) The closing offers no repository for the Devoxx assistant, leaving the Kotlin eval code to reconstruct by hand.
