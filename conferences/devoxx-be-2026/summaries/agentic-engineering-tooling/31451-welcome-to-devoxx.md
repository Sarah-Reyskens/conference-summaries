---
title: Welcome to Devoxx
talkId: "31451"
conference: devoxx-be-2026
speakers: [Stephan Janssen]
track: Agentic Engineering & Tooling
sessionType: Keynote
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=aup9tNzQu7c
durationMin: 26
slides: null
verdict: 5
reach: broad
frames: 7
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Welcome to Devoxx
Stephan Janssen · Keynote · Agentic Engineering & Tooling

## TL;DR
Devoxx founder Stephan Janssen opens the conference with the theme that developers are becoming builders: natural language is the new abstraction layer, and the work is shifting from writing code to specifying, supervising, and observing agents. The keynote mixes an AI-trend survey (agentic engineering stages, token economics, local models) with a live multi-agent coding demo of groma.md on the DevoxxGenie codebase.

## Key takeaways
- Treat natural language as the new programming abstraction and reposition from writing code to specifying intent, supervising agents, and reviewing output.
- Look at decision APIs (TypeSafe Jev-style constrained, probabilistic responses) for tool selection and harness control; Spring AI and LangChain4j already support them.
- Budget for token economics explicitly: subscriptions are heavily subsidized versus per-token pricing, and local models lag frontier models by about a year.
- Adopt spec-driven development for traceability and deterministic, repeatable agent workflows.
- Watch agent work at the architecture level, not just the diff level: a live architecture map with architecture diffs shows what parallel agents changed.

## Notes

### [01:05](https://youtu.be/aup9tNzQu7c?t=65) Robot opening skit
A humanoid robot on stage performs a scripted bit as a visitor from 2200 interrupting the keynote, then dances. Janssen welcomes the audience and jokes the robots are not fully ready to replace developers yet.

### [04:30](https://youtu.be/aup9tNzQu7c?t=270) Interview with the robot's builder
Thomas, visiting from Germany, explains the team started by learning the robot, then used reinforcement learning with NVIDIA tooling, and is now doing robot foundation model work aimed at real-world useful tasks. The robot costs around 40,000 euros, down about 10,000 since purchase. The team gives a lunch talk the same day on how the dance was programmed.

### [06:06](https://youtu.be/aup9tNzQu7c?t=366) Excited and frightened: developers become builders
Janssen describes his mental state as a superposition of excitement and fear. His non-developer son built a full wine-collection website with Claude without touching code, deployed to Firebase in an evening. There is no moat in that kind of work, which is why Devoxx changed its baseline from developers to builders. He draws the line at safety-critical code (hospitals, nuclear plants), where humans must still develop and review.

### [09:12](https://youtu.be/aup9tNzQu7c?t=552) Stages of agent engineering
He walks through the stages: copy-paste prompting, context engineering, agentic engineering with tools (file system, grep, fetch page), and now harness engineering plus loop engineering (agents running overnight; he jokes about a 500-euro token bill in one hour). The newest stage is decision engineering: TypeSafe Jev-style decision APIs return probabilities over constrained JSON responses, useful for selecting tools and checking whether a tool call is disruptive. OpenAI released a decision API, Spring AI and LangChain4j added support, and he urges the audience to attend the related talks.

### [12:19](https://youtu.be/aup9tNzQu7c?t=739) Nine-stage lifecycle and token economics
A slide maps nine stages from 2020 search-and-documentation through AI code assistants, chatbots, first agents, orchestration at scale, and agentic engineering (stage 6, where we are) to persistent AI workers, autonomous software factories, and self-optimizing systems in 2029. Most companies are still back at stage 3. On cost: roughly 70% of the room uses a fixed subscription and 5% pays per token. He calls the subscription a gym-style subsidy (pay $100, consume far more) and says real per-token prices would change the picture entirely.

### [14:56](https://youtu.be/aup9tNzQu7c?t=896) Local models and hardware
Janssen has not written code by hand since July 2025, using coding agents for everything. Local models trail frontier models by about a year; he recommends Qwen 3.8 as an orchestrator. He cites AMD burning model weights into silicon for 1,400 tokens per second, notes Gemini 4 may appear soon, and welcomes Mistral 4 open weights (needs 2 TB of RAM). A 512 GB Mac Studio costs 26,000 euros this October, which he presents as the price of serious local inference.

### [17:31](https://youtu.be/aup9tNzQu7c?t=1051) DevoxxGenie, CLIs, spec-driven development
DevoxxGenie, his open-source Java project for local models in the IDE, passed 100,000 downloads. He now works mostly in CLIs (about a third of the room agrees) and keeps IntelliJ for code review. Spec-driven development gives traceability and deterministic workflows; Rod Johnson covers Embabel Agent v1.5 on Friday. Observability of agent work is the open problem, which motivates the guest demo.

### [19:36](https://youtu.be/aup9tNzQu7c?t=1176) Live demo: groma.md multi-agent run
Guest Alex demos groma.md, an open-source CLI that keeps a live 3D architecture map of a codebase so developers stay over the loop. Six Codex agents on GPT-6 Astra Ultrafast (credits sponsored by OpenAI) implement six DevoxxGenie backlog tasks in parallel; the map shows tasks progressing and four of six finishing within minutes, each with acceptance criteria and code review attached. He then shows the architecture diff: which components were added, modified, or removed. The tool works offline with local models via per-language scanners. A rehearsal run cost $60; the live run likely over $100, versus an estimated five days of manual work.

### [24:48](https://youtu.be/aup9tNzQu7c?t=1488) Wrap-up
Janssen plugs the Robot Games lunch talk (9 AI-built open-source games, Thursday Room 10), asks attendees to rate talks in the mobile app, and closes on the theme: the glass is half full, and developers need to get on the train.

## Tools, libraries and specs
- groma.md (open source, MIT) with backlog.md, its spec/task companion
- DevoxxGenie (open source Java, 100,000+ downloads)
- TypeSafe Jev / decision APIs: OpenAI decision API, local-inference decision API, Spring AI and LangChain4j support
- Claude, Codex, GPT-6 Astra Ultrafast, Qwen 3.8, Mistral 4 open weights, Gemini 4 (rumored)
- Java 27, Firebase, NVIDIA robot reinforcement-learning stack

## Who should watch
Attendees and remote viewers who want the conference theme and Janssen's read on where agent engineering is heading, plus a genuinely live multi-agent demo. Viewers wanting depth should skip to the follow-up sessions instead: the Friday groma.md talk, the robot-programming lunch talk, Rod Johnson on Embabel, or the Java track talks.

## Verdict
**5/10**: Personal experience gives the builders theme substance and the live architecture map shows agent work in progress, while costs remain anecdotal and the explanations are introductory.

**Reach broad**: AI-assisted development, token budgets and supervising coding agents apply to most of this conference's developers, leads and architects.

**Novelty 1/2**

- **+** [07:06](https://youtu.be/aup9tNzQu7c?t=426) Building and deploying his non-developer son's wine site gives the builders theme a personal example beyond a feature tour.
- **+** [18:02](https://youtu.be/aup9tNzQu7c?t=1082) His move from IDE-based development to several coding CLIs while retaining IntelliJ for review adds his own working practice to the trend survey.
- **·** [12:19](https://youtu.be/aup9tNzQu7c?t=739) The lifecycle survey mentions his company-workshop experience only briefly, with no cases of what failed and changed.

**Demonstrated 1/2**

- **+** [21:40](https://youtu.be/aup9tNzQu7c?t=1300) The live groma.md run displays agent task progress, acceptance criteria and an attached code review.
- **+** [22:42](https://youtu.be/aup9tNzQu7c?t=1362) The architecture diff visibly distinguishes removed, modified and added components.
- **−** [22:11](https://youtu.be/aup9tNzQu7c?t=1331) Four of six tasks are finished when the presentation moves on, so the whole job is not shown completing.

**Measured 1/2**

- **+** [23:45](https://youtu.be/aup9tNzQu7c?t=1425) The rehearsal run has a reported cost of $60, giving the token-economics warning a real expenditure figure.
- **−** [24:16](https://youtu.be/aup9tNzQu7c?t=1456) The live-run cost and five-day manual-effort comparison are estimates, without a measured manual baseline or a stated costing method.

**Depth 1/2**

- **+** [10:46](https://youtu.be/aup9tNzQu7c?t=646) Decision APIs receive a short explanation of constrained responses and probabilities, tied to tool selection and disruptive-call checks.
- **+** [23:14](https://youtu.be/aup9tNzQu7c?t=1394) Language-specific scanners explain how the architecture tool can work deterministically and offline.
- **·** [09:12](https://youtu.be/aup9tNzQu7c?t=552) The progression from prompting to context and agent tools supplies introductory orientation, with little discussion of how to choose among the approaches.

**Reusable 1/2**

- **+** [25:19](https://youtu.be/aup9tNzQu7c?t=1519) The architecture tool is available as an MIT-licensed project that viewers can clone and fork.
- **·** [17:31](https://youtu.be/aup9tNzQu7c?t=1051) DevoxxGenie is another presented project, so its distribution is a tool to try rather than an artifact reproducing the keynote's examples.
