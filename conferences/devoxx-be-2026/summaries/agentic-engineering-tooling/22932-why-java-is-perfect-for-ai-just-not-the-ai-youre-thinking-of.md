---
title: Why Java Is Perfect for AI - Just Not the AI You’re Thinking Of
talkId: "22932"
conference: devoxx-be-2026
speakers: [Trisha Gee, Andrey Santrosyan]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=hHu3rLsbYog
durationMin: 46
slides: null
verdict: 7
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Why Java Is Perfect for AI - Just Not the AI You're Thinking Of

Trisha Gee, Andrey Santrosyan · Conference · Agentic Engineering & Tooling

## TL;DR

Enterprise AI means embedding intelligence as a component inside existing Java systems: the deterministic application calls agents for narrow uncertain steps, then validates their output through business rules it already owns. The talk leaves a set of integration patterns (boundaries, scope, in-app agents, per-step model benchmarking) backed by one production case study, plus an open-source platform pointer with no URL given.

## Key takeaways

- Call agents from your application for narrow uncertain steps instead of exposing your system for agents to call.
- Treat model output as a guess, and validate it through existing business rules before acting on it.
- Put guardrails and authorization checks on the tools, and scope multi-step work so agents cannot drift across loop iterations.
- Run agents inside your application to keep data local, hold state, and avoid shipping records through agent-to-agent handoffs.
- Benchmark every agentic step on real data and route each step to the cheapest model that handles it.
- Manage model tokens like database connections: pool and schedule them rather than retrying with backoff.

## Notes

### [00:33](https://youtu.be/hHu3rLsbYog?t=33) Intros and the other AI

Trisha Gee (independent consultant, Java Champion) presents with Andrey Santrosyan (25 years of scientific Java applications, founder of Redouble AI, which builds multi-agent systems for regulated industries). Their presenter notes were lost, so they drive from the slides. The thesis: the AI work that matters for this room is integrating AI into business software, which runs where Java already runs.

### [02:09](https://youtu.be/hHu3rLsbYog?t=129) Are Java engineers being left behind?

Many Java engineers wonder whether their skills are still relevant next to Python, deep learning, and ML mathematics. Gee reframes the room as the people maintaining the applications that make businesses money, then asks whether it is time to move on and whether Java is dead. Answering that requires asking what AI development actually looks like.

### [04:12](https://youtu.be/hHu3rLsbYog?t=252) Three kinds of AI work, and legacy as an asset

AI work splits into training models, building AI tools such as chatbots, and integrating AI into business software. The third kind lives in enterprise Java systems: wiring in a model resembles wiring in a data source. Legacy systems hold decades of business rules, edge cases, regulatory requirements, integrations, and validations. "Your legacy system is the business," encoding how the enterprise works and what it forbids.

### [06:16](https://youtu.be/hHu3rLsbYog?t=376) The cloud analogy

Around 2011 every Devoxx talk was about cloud, which changed deployment and working practices (DevOps, automation, cattle instead of pets) while applications kept encoding the same business knowledge somewhere else. AI in 2026 may follow the same shape: a new tool that changes some practices while mature systems keep running.

### [08:21](https://youtu.be/hHu3rLsbYog?t=501) The system is in charge, and an agent taxonomy

The "drop a company into a prompt" vision fits consumer apps, where a person delegates authority and checks results. Enterprise systems work the other way: the system directs the employee, and a bank teller cannot deploy a self-written tool to process a credit application. No model intelligence changes that. Santrosyan then splits agents into interactive ones (chat clients with fixed tools; coding agents that invent tools) and synchronous non-interactive ones: headless event- or schedule-driven workflows with an enumerated tool set. Back-office style, non-interactive agents with fixed tools are the enterprise future. Grants of invent-and-run-tools power in production are, in his words, the path to Skynet.

### [13:05](https://youtu.be/hHu3rLsbYog?t=785) Non-chat uses, and containing uncertainty

Useful targets include spreadsheet imports with randomly named columns and mixed European/American date formats, and free-text-to-form filling. Uncertainty is routine in software (dead networks, bad input, odd error codes); letting it propagate is an architectural choice. Gee's example: Ford's year-2000 attempt to sell cars online, where the team had to codify every undocumented bank API behavior deterministically, since nobody hands over a car on an assumed £30,000 payment.

### [17:13](https://youtu.be/hHu3rLsbYog?t=1033) "The AI thinks" is not a fact

A pizza-ordering AI may guess that messy input means a large Diablo, but that guess is not an order. The existing ordering system still checks the menu, availability, toppings rules, delivery area, and payment. Likewise, a guessed €1,870 invoice is not an approved €1,870 expense. The architecture must separate the guess from the acted-upon fact: deterministic software hands a step to the agent and takes the output back into validated flow.

### [20:52](https://youtu.be/hHu3rLsbYog?t=1252) The same boundary as with humans, plus scope

Systems already validate human input and authorize human actions; agents get the same treatment, with guardrails and authorization checks placed on the tools. Observed failure modes are boundaries in the wrong place and holes no human ever poked. Authorization alone does not cover scope: in a loop over items with nondeterministic steps, an agent told it is on step 17 may act on step 23 while authorized for the whole loop.

### [24:29](https://youtu.be/hHu3rLsbYog?t=1469) Who calls whom, and where agents run

Gee argues the integration direction is backwards: the ordering system needs access to the agent the way an application calls an in-process JSON parser, rather than opening the application over MCP for agents to call. Managed agents running elsewhere force data shipping, extra security, scope handling, and state across stateless calls. The agentic telephone game follows: passing results between agents risks hallucination, while passing record IDs gives every agent database access and too many tools. Tool and system errors should tell agents exactly what failed and how to fix it, the way good error messages guide users.

### [29:42](https://youtu.be/hHu3rLsbYog?t=1782) L3 support at scale, tokens, and model benchmarking

A German industrial-networks manufacturer sends level-3 support cases as gigabytes of nested archives in mixed, unseen log formats: too irregular for deterministic code, too large for one prompt. Parsing them line by line into a database took hundreds of thousands of agents and millions of tool calls per ticket. Token limits add a scarce resource the industry mostly handles with wait-and-retry backoff, which Santrosyan compares to a connection pool that says "come back later": pool and schedule instead. Virtual threads get praise as made for these workloads, with internals deferred. The cost lever is deterministic-first parsing with per-row model fallback on exceptions (the unparseable row is usually the interesting one), using AWS Nova Micro: $3,000 per ticket on a frontier model became $126, and cheaper or locally runnable models now go further.

### [35:28](https://youtu.be/hHu3rLsbYog?t=2128) Why Java, and an open-source release

The case for Java: decades of embedded business rules, compiler and type safety instead of a black box, performance, and engineers practiced at designing for failure. No rewrite, retraining, or parallel stack is needed. Santrosyan announced that Redouble AI's core platform, written for Java engineers and holding solutions for the problems described, was released open source the day before; no repository URL was given on stage.

### [39:04](https://youtu.be/hHu3rLsbYog?t=2344) Q&A

On competing with "AI superstars" who prototype in an afternoon: let them fail outside production, and expect tooling to close the gap the way Spring Boot did for Java against Node and MongoDB around 2011. People see AI's limits on their own job but overestimate it on others' jobs; the edge cases and nuance in the code are the engineering. On whether this is self-reassurance: fundamentals (specifications, definition of done, edge cases) decide whether assistant output is rubbish, and even a perfect model needs an engineered specification, illustrated with a computer mouse's curve, weight, click, and surface.

## Tools, libraries and specs

- Redouble AI core platform (announced as open source on stage; no URL given)
- AWS Nova Micro (cheap model used for fallback parsing)
- MCP (named as the protocol for exposing application tools to external agents)
- Project Loom / virtual threads (praised for agent workloads; internals deferred)

## Who should watch

Java and enterprise engineers deciding how to add AI to existing systems, and architects drawing boundaries around agents, gain the most. Viewers wanting code, live demos, or model internals can skip it, as can anyone focused on Python-first model training.

## Verdict

**7/10**: Agent-integration patterns from the speakers' own production work, with a cost comparison and an open-source runtime behind them, argued entirely on slides with no demo.

**Novelty 2/2**

- **+** [29:42](https://youtu.be/hHu3rLsbYog?t=1782) The L3 support case (gigabytes of nested logs, hundreds of thousands of agents per ticket) is presented as something the speakers implemented recently at Redouble AI.
- **+** [11:30](https://youtu.be/hHu3rLsbYog?t=690) The synchronous non-interactive agent class is offered as one that "does not even have a good name in the industry yet", and with the who-calls-whom inversion at [24:29](https://youtu.be/hHu3rLsbYog?t=1469) it forms a decision framework no single source gives.
- **−** [02:09](https://youtu.be/hHu3rLsbYog?t=129) The opening reassurance that Java skills stay relevant is familiar conference positioning before the original material starts.

**Demonstrated 0/2**

- **−** [29:42](https://youtu.be/hHu3rLsbYog?t=1782) The L3 pipeline, per-row model fallback and token handling are described, with no code, run or output on screen.
- **−** [38:03](https://youtu.be/hHu3rLsbYog?t=2283) The open-source platform is announced with an invitation to try it, but nothing from it is shown.

**Measured 1/2**

- **+** [34:56](https://youtu.be/hHu3rLsbYog?t=2096) A frontier-model cost of $3,000 per ticket is set against $126 after deterministic-first parsing with a cheap-model (AWS Nova Micro) fallback per unparseable row.
- **−** [31:15](https://youtu.be/hHu3rLsbYog?t=1875) The figures are self-reported: the $3,000 is conditional ("if we use the top line frontier model"), no ticket size or benchmark setup is shown, and "hundreds of thousands of agents and millions of tool calls" has no baseline.
- **−** [36:31](https://youtu.be/hHu3rLsbYog?t=2191) "Java performance is very very good" is asserted with no number or comparison.

**Depth 2/2**

- **+** [27:38](https://youtu.be/hHu3rLsbYog?t=1658) The telephone-game segment weighs passing results (hallucination risk) against passing record IDs (every agent needs database access) against tool sprawl.
- **+** [26:36](https://youtu.be/hHu3rLsbYog?t=1596) Managed agents elsewhere versus in-app agents is argued through data shipping, authorization, scope and state across stateless calls.
- **−** [35:28](https://youtu.be/hHu3rLsbYog?t=2128) The Java-specific case (compiler and type safety, performance) is two minutes of assertion with no mechanism, and virtual-thread internals are deferred at [32:52](https://youtu.be/hHu3rLsbYog?t=1972).

**Reusable 2/2**

- **+** [38:03](https://youtu.be/hHu3rLsbYog?t=2283) Redouble AI's core platform was released open source the day before, with "everything we mentioned here there are solutions in there"; its Nucleo repository (github.com/redouble-ai/nucleo) has Scope, Guardrail, Artifact and virtual-thread JobDispatcher modules for the problems described.
- **−** [38:03](https://youtu.be/hHu3rLsbYog?t=2283) No repository URL or product name was given on stage; the company name at [01:04](https://youtu.be/hHu3rLsbYog?t=64) is the only lead.
