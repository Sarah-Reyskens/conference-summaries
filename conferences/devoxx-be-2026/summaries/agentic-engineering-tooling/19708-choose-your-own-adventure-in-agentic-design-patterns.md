---
title: Choose your own adventure in agentic design patterns
talkId: "19708"
conference: devoxx-be-2026
speakers: [Guillaume Laforge]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: ADVANCED
video: https://www.youtube.com/watch?v=w2RTFWet_6c
durationMin: 52
slides: https://speakerdeck.com/glaforge/choose-your-own-adventure-in-agentic-design-patterns
slidesNote: from Devoxx France 2026
verdict: 7
frames: 8
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Choose your own adventure in agentic design patterns

Guillaume Laforge · Conference · Agentic Engineering & Tooling

Slides: https://speakerdeck.com/glaforge/choose-your-own-adventure-in-agentic-design-patterns

## TL;DR

Laforge tours seven agentic patterns (programmatic planning, RAG, progressive disclosure, hierarchical decomposition, LLM-as-judge, GOAP, coding-agent loops), each presented as an ID card with problem, solution, and pros/cons, and each implemented live in Java with LangChain4j or ADK for Java. The throughline: reach for deterministic code before agency, feed agents information progressively, and evaluate with judges so multi-agent systems reach their goals instead of wandering.

## Key takeaways

- When a workflow can be drawn as a flowchart, program it instead of giving an agent full autonomy: it is easier to debug and more deterministic.
- Agent Skills implement progressive disclosure (metadata in context first, full instructions only on demand), which keeps the context window lean and reduces tool-choice confusion.
- Decompose big tasks into specialized sub-agents with small prompts rather than one monolithic agent with a giga-prompt; parallelize independent steps to cut latency.
- A batch of cheap small-model outputs plus an LLM judge can rival a big model at lower cost ($1.20 vs $2.00 per million tokens in the demo's price table), so price the judge into the design.
- Goal-oriented action planning (GOAP) replaces hardcoded pipelines: declare each agent's inputs and outputs and let a planner find the path to whatever goal is requested.
- A working coding-agent loop needs little code (a supervisor, file/system/web specialists, and a `while` loop); robustness and sandboxing are where the real work hides.

## Notes

### [00:34](https://youtu.be/w2RTFWet_6c?t=34) Agent basics and the problems patterns solve

Laforge (Google Cloud developer advocate, LangChain4j and ADK for Java committer, Groovy co-founder) defines an agent as brain (LLM), memory, tools, planning, and a loop that runs until the goal is met. He maps the concerns the patterns address: planning and agency, context engineering (avoiding "context rot" from overstuffed windows), tool management (too many tools confuse tool choice), evaluation, multi-agent orchestration, security and observability (sandboxing, OpenTelemetry; explicitly out of scope), and harness engineering. Each pattern gets an ID card: name, problem and context, solution and implementation, consequences.

### [07:54](https://youtu.be/w2RTFWet_6c?t=474) Programmatic planning: deep research without a framework

Full agent autonomy is close to an anti-pattern when the steps are known in advance. The demo is a deep-research app built directly on the Gemini Interactions API: Gemini Flash expands a subject into selectable sub-topics, a managed deep-research agent writes a long grounded report in the background (the shown run took 43 minutes, so only the fast topic step ran live), then model calls produce a one-page executive summary and a Nano Banana sketchnote illustration. The API is stateful, so calls reference a conversation ID instead of resending history. Point: many AI features need no agent framework at all.

### [14:40](https://youtu.be/w2RTFWet_6c?t=880) RAG and progressive disclosure: the deslopify skill

RAG gets a brief recap as the first context-engineering pattern (cut-off dates, chunking, vector/BM25 retrieval, prompt augmentation) with no demo. The new material is progressive disclosure via Agent Skills: the context window first holds only each skill's name and description; the full SKILL.md loads when relevant; referenced scripts and files load last. The LangChain4j demo chains a hype-style draft agent (with Google Search) into a refiner agent carrying a "deslopify" skill that strips AI slop (superlatives, emojis) into plain human prose, both versions shown side by side on Devoxx Belgium 2026 themes.

### [24:10](https://youtu.be/w2RTFWet_6c?t=1450) Hierarchical decomposition: comic trip agent

Monolithic agents with giant prompts underperform teams of specialists. The Comic Trip app (ADK for Java) runs a sequential flow: a picture-analyzer agent (Gemini 3 Flash) guesses each photo's location and writes a description into shared state, then a parallel flow fans out to a points-of-interest agent (Gemini 2.5 Flash with the Google Maps tool) and a comic illustrator (Nano Banana). Live-uploaded Antwerp photos came back as captioned vintage comic panels with nearby POIs clickable beside them.

### [30:26](https://youtu.be/w2RTFWet_6c?t=1826) LLM-as-judge: parallel summarization contest

Humans become the review bottleneck, so a second model can grade whether the goal was reached, with the caveat that repeat judgments are non-deterministic. The LangChain4j demo batches three small-model summaries (Gemini 3.5 Flash Lite) of a Quanta article in parallel, then a judge picks the winner with reasons; a second judge compares that winner against a big-model (Gemini 3.1 Pro) summary. The on-screen price table frames it as cost engineering: three $0.30 summaries plus a $0.30 judgment totals $1.20 per million tokens against $2.00 for the big model, and Laforge reports the small models win roughly one run in three.

### [39:17](https://youtu.be/w2RTFWet_6c?t=2357) GOAP: the content specialist that plans its own path

Goal-oriented action planning, borrowed from game AI via Rod Johnson's Aimable work and now in LangChain4j and ADK for Java, inverts the pipeline: instead of coding the path, declare five agents' inputs and outputs (content collector, topic researcher, summarizer, infographic artist, YouTube-shorts creator) plus the desired goal, and an A*-style planner finds the invocation chain. Switching the goal from "infographic of the latest AI news" to "shorts script for this article URL" reuses the same team over a different path, shown live including the generated infographic.

### [45:34](https://youtu.be/w2RTFWet_6c?t=2734) Coding-agent loop and wrap-up

After naming the verify-until-done feedback loop without demoing it (that material went to his Tuesday deep dive), Laforge shows "nanocode", his LangChain4j coding agent: a supervisor delegating to file, system, and web-search specialists inside a plain read-eval loop, in a bit over 300 lines. The audience picks the agentic variant; asked live for the main Devoxx Belgium 2026 themes, it delegates to web search and summarizes the agenda. He closes by mapping every pattern onto planning, orchestration, context, evaluation, tooling, and harness engineering, and takes questions at the front.

## Tools, libraries and specs

- LangChain4j (`@Agent`, `AgenticServices` sequence/batch/supervisor builders, `ClassPathSkillLoader`, typed keys)
- ADK for Java (`LlmAgent`, `SequentialAgent`, `ParallelAgent`, `PlannerAgent` with `GoalOrientedPlanner`, shared-state output keys)
- Gemini Interactions API (stateful `ModelInteractionParams` / `AgentInteractionParams`, background and streaming runs)
- Gemini models: 3.8 Flash, 3.1 Pro, 3.5 Flash Lite, 2.5 Flash, Nano Banana image generation
- Agent tools: Google Search, Google Maps, URL context; Agent Skills (`SKILL.md` with scripts, references, assets)
- MCP, OpenTelemetry, JBang (named in passing)

## Who should watch

Java developers building multi-agent features who want a pattern vocabulary plus working LangChain4j and ADK for Java examples to copy. Skip it if you already ship hierarchical agents with judges and planners, or if you want Python-framework specifics, agent security, or observability: sandboxing is named as its own pattern and explicitly not covered.

## Verdict

**7/10**: Six agentic patterns shown running in Java with reasoned trade-offs per pattern, but the cost comparison is list-price arithmetic backed by an anecdotal win rate, and no demo app ships with a repository.

**Novelty 1/2**

- **+** [42:27](https://youtu.be/w2RTFWet_6c?t=2547) One team of five agents reaches two different goals (an infographic, then a YouTube short from an article URL) by letting a goal-oriented planner choose the path, in ADK for Java.
- **+** [33:34](https://youtu.be/w2RTFWet_6c?t=2014) The small-models-plus-judge experiment is the speaker's own, run live with the current Gemini price table.
- **·** [14:40](https://youtu.be/w2RTFWet_6c?t=880) RAG gets a recap with no demo, and GOAP is credited to Rod Johnson ([39:17](https://youtu.be/w2RTFWet_6c?t=2357)); the talk's added value is the Java implementations and the survey.

**Demonstrated 2/2**

- **+** [42:58](https://youtu.be/w2RTFWet_6c?t=2578) The GOAP content specialist returns a summary and then an infographic for an article URL, live.
- **+** [49:17](https://youtu.be/w2RTFWet_6c?t=2957) The nanocode agentic supervisor, picked by the audience, delegates to its web-search specialist for the Devoxx Belgium 2026 themes.
- **−** [19:55](https://youtu.be/w2RTFWet_6c?t=1195) The deslopify demo does not show the progressive-disclosure mechanism, as the speaker says himself.

**Measured 1/2**

- **+** [34:10](https://youtu.be/w2RTFWet_6c?t=2050) The slide prices three small-model summaries plus one evaluation at $1.20 against $2.00 for one big-model summary, per million tokens.
- **+** [11:00](https://youtu.be/w2RTFWet_6c?t=660) The pre-run deep-research report took 43 minutes 34 seconds.
- **−** [36:40](https://youtu.be/w2RTFWet_6c?t=2200) The quality side rests on one live run that the big model won and a recollection that the small models win "maybe one out of three times or something".

**Depth 2/2**

- **+** [19:24](https://youtu.be/w2RTFWet_6c?t=1164) Progressive disclosure is explained as three levels (metadata, full SKILL.md, then referenced files), tied to context rot and tool-choice confusion.
- **+** [41:57](https://youtu.be/w2RTFWet_6c?t=2517) GOAP is walked through from goal to required summary to the agents that can supply it, using each agent's declared inputs and outputs.
- **+** [08:24](https://youtu.be/w2RTFWet_6c?t=504) Programmatic planning is weighed against full agent autonomy: easier to debug and more deterministic, but more maintenance and less adaptable.

**Reusable 1/2**

- **+** [44:30](https://youtu.be/w2RTFWet_6c?t=2670) The GOAP agent-metadata setup for ADK is shown as code, with input and output keys per agent.
- **−** [50:20](https://youtu.be/w2RTFWet_6c?t=3020) The nanocode agent ("a bit more than 300 lines") and the other demo apps come with no repository URL.
