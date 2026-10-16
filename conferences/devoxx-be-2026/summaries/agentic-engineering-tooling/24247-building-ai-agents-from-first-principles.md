---
title: Building AI Agents from First Principles
talkId: "24247"
conference: devoxx-be-2026
speakers: [Adib Saikali]
track: Agentic Engineering & Tooling
sessionType: Deep Dive
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=SC5nO6iadsU
durationMin: 150
slides: null
verdict: 7
reach: segment
frames: 21
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Building AI Agents from First Principles

Adib Saikali · Deep Dive · Agentic Engineering & Tooling

## TL;DR

Saikali builds a dinner-planning agent called Jarvis piece by piece in Spring AI, evolving a plain request/response call into a plan-act-observe-decide loop with intent alignment, tool calling, constraint checking, planning, and memory. The thesis is that agents are software systems to architect (APIs, tool boundaries, control flow, verification), not prompting tricks. Every mechanism is shown live with its HTTP traffic to the model on screen.

## Key takeaways

- Consumer chat apps are agents (tools, memory, a Linux container per Claude session), not models; the models API is the closest thing to a raw model, so calibrate expectations there.
- Two mechanisms turn model nondeterminism into something code can use: structured output converters (free text to JSON to Java records) and tool calling (free text to method invocations the model chooses).
- Acceptance rate, the share of tasks completed without user correction or retry, is the metric that matters; acceptance is a system property owned end to end, improved with user and system feedback.
- Make agents verifiable: pair every model proposal with checkers, deterministic (budget, noise) where possible, hybrid or LLM-judge where judgment is needed, returning pass/fail/maybe.
- There are two loops, not one: the model decides which tools to call and when to stop; the harness decides whether it got what it needs and whether to call the model again.

## Notes

### [00:41](https://youtu.be/SC5nO6iadsU?t=41) Goals, anti-goals, and the repo

The session optimizes for teaching clarity: understand agents from first principles, reason about trade-offs, build them in Spring AI with the focus on patterns any framework user can transfer. Out of scope: production agents, prompt hacks, "best framework", model comparisons, Spring AI tutorials, model training. Code is in the speaker's `asaikali/art-of-building-agents` repo (link shown on the opening slide), organized as `foundations/` mini-apps plus a `meal-agent/` built in cumulative snapshots `01` through `06`, with a Vue.js inspector UI and a traffic "spy" built with Codex the day before.

### [03:48](https://youtu.be/SC5nO6iadsU?t=228) The application capability continuum

Using a restaurant reservation app (OpenTable-style, ~9,400 restaurants in Toronto, ~4,000 taking reservations per a model estimate), the talk layers four stages: CRUD web app (business rules, static logic), ML prediction (recommendations from user data, consumed as a REST API), GenAI Q&A (RAG over restaurant info via a foundation model), and finally a planning agent that reasons over goals and constraints (time, party size, diet, directions API) to plan and book. Applied to other domains (bank loan: web form, credit scoring, document explainer, agentic document checker). Much of AI is framed as a better user interface that reduces friction.

### [15:47](https://youtu.be/SC5nO6iadsU?t=947) The goal: Jarvis, a dinner-planning agent

By the end, the audience will see an agent handle: "organize a business dinner for four at 6 p.m. tonight, office till 5:30, one vegetarian guest, comply with expense policy, plan and book." Open questions the agent must resolve include where office is and what the expense policy contains.

### [16:52](https://youtu.be/SC5nO6iadsU?t=1012) Consumer apps are agents, not models

Two demos reset the audience's mental model. ChatGPT (training cutoff June 2024) correctly names the 2026 Super Bowl winner because it searched the web (visible "searching" indicator), while the raw models API (cutoff August 2025) says it does not know. Claude's desktop app runs `ps aux` and `java -version` (Java 21) inside an attached Ubuntu 24 container with 4 CPUs and 9 GB RAM (4 GB enforced). Conclusion: chat apps hide a model inside an agent system with tools.

### [21:35](https://youtu.be/SC5nO6iadsU?t=1295) What a model actually is

A model is a black box doing math: configuration plus input tokens in, one next token out, wrapped in a loop so it looks like answers. Quality depends on weights and quantization (a GPT-OSS variant at 14 GB vs 65 GB shown), so when an agent misbehaves the fault may be the deployment, not the agent design.

### [23:37](https://youtu.be/SC5nO6iadsU?t=1417) Three products, three ways to build an agent

Labs sell a chat agent (human interaction, built-in tools, memory, skills), coding agents (Claude Code, Codex, IDE plugins), and the API (no built-in tools; you bring them). Correspondingly: write `skill.md`/shell scripts extending an existing agent (fast, limited control), or write application code against the API (full control over reasoning, integrations, governance; higher upfront cost). Build-vs-extend guidance: a build-failure analyzer suits extending Claude Code; deep enterprise integration suits owning the loop. The workshop uses the API directly.

### [27:47](https://youtu.be/SC5nO6iadsU?t=1667) ChatClient basics and the system prompt

Live code: Spring AI's `ChatClient` calls any provider with a prompt and returns content. A fruit-expert system prompt ("only discuss fruits") refuses a carrot-color question but answers a banana one, establishing that every model call needs a purpose set by its system prompt. Parameterized user prompts are shown via a joke REST endpoint. Code takes teaching shortcuts (nullable, non-idiomatic Java) to fit on screen.

### [32:35](https://youtu.be/SC5nO6iadsU?t=1955) Structured output: prompt begging vs native support

Requesting an entity (a `Book` record: author, title) instead of a string yields Jackson-parseable JSON. The spy shows why: Spring AI appends "prompt begging" (JSON-only instructions plus a generated JSON schema for author/title, both required, no extras). Arrays and extra fields (publication year) extend the schema the same way. Providers now also offer native structured output (a `response_format` with the schema on the wire); Spring AI cannot default to it since not every provider supports it, so it is opt-in with retry-on-mismatch behavior.

### [44:38](https://youtu.be/SC5nO6iadsU?t=2678) Module 01: intent alignment with Jarvis

The inspector UI (Vue.js, SSE) chats with Jarvis while rendering agent state as versioned JSON. Saying "hi", then "dinner for two", then "tomorrow, customer dinner, vegan customer" walks revisions 1-3 of a `UserRequirements` POJO (meal date/time/party size/type enum, attendees, budget, cuisine), each turn adding extracted fields. Code: an `AgentHandler` (`getName`, `getInitialMessage`, `onMessage`) retrieves session context, runs a requirements aligner (extractor with a "structured data extractor" system prompt fed today's date plus current-state JSON, returning an updated entity), a missing-fields assessor (date, time, party size gate search), and an alignment status enum (gathering, confirming, confirmed). Confirmation is detected by `equals` between old and new requirements objects. Replies come from a second model call with a "warm executive dining assistant" system prompt, so extraction stays structured while tone stays human. Asking "looks good?" triggers a confirmation summary with a suggested follow-up (budget, neighborhood).

### [67:10](https://youtu.be/SC5nO6iadsU?t=4030) Tool calling: answer a question with a question

Intuition via a bike-shop salesperson and a what-to-wear-in-Amsterdam example: the model responds with a tool request (`getWeather` for Amsterdam), the app invokes it (12 degrees, raining), and the full history plus result goes back so the model can answer (jacket, umbrella). Live demo in `foundations/03-tool-calling`: a `@Tool`-annotated weather service plus an activities tool. The spy shows one turn containing two to three HTTP requests; "Toronto and Paris" yields two parallel weather calls chosen by the model, and "what should I do in Toronto" chains weather (-8.2 C, snowy) into `findActivities` (indoor skating, museum; the speaker notes nobody indoor-skates in Toronto). Takeaway slide: structured output converts language to objects, tool calling converts language to method calls.

### [81:20](https://youtu.be/SC5nO6iadsU?t=4880) The agentic loop, and MCP in one slide

Tool calls turn models into agents; the ChatGPT Super Bowl search was exactly this pattern. An agentic system leverages a model to interact with its environment toward a user task, combining planning (brain, LLM) with actions (body, tools). MCP is positioned as a protocol for out-of-process tools so a Java app can call Python tools and vice versa (PDF extraction, email, IDE control).

### [84:43](https://youtu.be/SC5nO6iadsU?t=5083) Module 02: restaurant search, and the steakhouse failure

Module 02 adds search to the alignment code. Restaurant data is a Claude-generated `restaurants.json` (15 downtown Toronto spots with address, noise, price range, descriptions; the speaker's favorite is an Italian place) plus crawled menus behind `RestaurantService`/`MenuService`, with a scripted availability service (6 p.m. always free, 8 p.m. never, two guests always seated). The `findAvailableRestaurants` tool (date, time, party size, neighborhood, with format hints and a description stating availability says nothing about budget/noise/diet) is exposed to the model via `ChatClient` `.tools()` on a `RestaurantSearcher` whose system prompt forbids inferring suitability from names. The demo books dinner for two with a vegetarian VIP and recommends Black and Blue Steakhouse: search without verification fails, motivating the next module.

### [95:40](https://youtu.be/SC5nO6iadsU?t=5740) Reading the wire: turns of JSON and text

Walking the spy turn by turn: extractor prompts (system prompt plus state JSON plus user message, Spring AI appending schema), reply-composer prompts with suggested follow-ups, then the search turn where the model emits a `findAvailableRestaurants` call (date 2026-10-07, 18:00, party 2) and the full restaurant list returns as the tool result, rendered into prose.

### [102:23](https://youtu.be/SC5nO6iadsU?t=6143) The iron law: acceptance rate

Acceptance rate is the percentage of tasks completed without user correction, override, or retry; every "no, do it the other way" to a coding agent is a rejection. Users trust agents that meet their needs, and no model or tooling matters if output is rejected. Perfection is impossible (probabilistic models, failed plans and tool calls, incomplete context, misunderstood constraints), so the goal is disciplined improvement driven by feedback from users and from the system (latency, tokens, traces; Spring AI's instrumentation dashboards get a mention). Acceptance is a system property, not the model's or the agent's alone.

### [102:53](https://youtu.be/SC5nO6iadsU?t=6173) Module 03: constraint checkers in three flavors

Deterministic: a budget checker compares per-person budget against the restaurant's min/max price (pass/fail/maybe, where a $75 budget against a $50-100 range is "maybe, order carefully"); a noise checker maps quiet/moderate/loud to numbers and compares. LLM judge: a meal-suitability check feeds meal context and restaurant JSON to the model with a judging system prompt and returns a structured pass/fail/unsure record with reasons. Hybrid: a dietary checker filters the menu to mains in code, then asks the model whether those mains satisfy the constraint (per-item judging would cost more). A candidate service runs all checks (noise, budget, travel time, dietary, meal suitability) per restaurant. Framing: verifiability is what lets an agent know it solved the goal, the way tests tell a coding agent its change was good.

### [115:29](https://youtu.be/SC5nO6iadsU?t=6929) Module 04: evaluated planning

Planning tools add `getRestaurantDetails` and `checkRestaurantCandidate` (runs the check service, returns a summary; "if in doubt, convert to JSON and give it to the model") to availability search. The planner's system prompt prescribes the strategy: search, pick the most promising, review pass/fail/maybe results, present only restaurants passing all hard constraints, never mention failures. After a live blooper (wrong app started, steakhouse again, quick restart), the planner recommends Planta Queen (vegetarian-strong), Richmond Station, Cafe Boulud, and Scaramouche for the vegetarian VIP dinner. The spy shows the LLM-judge calls as context engineering: narrow questions stuffed with exactly the details needed (meal context plus restaurant details; mains plus constraint), including a vegetarian pass for "sushi and rolls" the speaker finds questionable.

### [123:22](https://youtu.be/SC5nO6iadsU?t=7402) Module 05: decision support

Recommendations alone leave follow-ups ("Planta versus Richmond Station?") unanswered, so a decision-support call gives the model the planning tools plus confirmed requirements, the shortlist, and the user question. Demo: "canoe versus Richmond station" yields a comparison (Canoe polished, 51st floor, very fancy; Richmond Station warmer, street level). The model answers via `getRestaurantDetails`; a larger system would add review search with RAG over embeddings (pointed to an ING speaker's vector-store session). The handler is effectively a small state machine: align, plan, support.

### [130:24](https://youtu.be/SC5nO6iadsU?t=7824) Crosscutting memory via Spring AI advisors

Remembering "Trattoria is my favorite" across turns is a crosscutting concern, answered the way Spring answers transactions and security: an interception chain. Advisors sit between `ChatClient` and model, transforming outbound messages and inbound responses; tool calling, observability, and the model call itself are all advisors. An advisor can call a model (e.g. "should I remember this?"), which itself can use tools and emit telemetry, so token-cost observability matters ($50 automated interactions vs $10 humans). The trace-advisor demo visualizes the chain order (app, tool-calling advisor, trace advisors, chat-model advisor, then back up), modeled on Christian Tzolov's session. A guardrail question gets an honest answer: jailbreak resistance lives in the model, not Spring AI, though advisors can add checker calls at token cost.

### [141:23](https://youtu.be/SC5nO6iadsU?t=8483) Module 06: user preferences remembered

An in-memory user-to-favorites store plus `rememberFavorite`/`forgetFavorite` tools and a preference advisor that injects user ID and instructions into the prompt. Demo as user Alex: after planning dinner, "Planta is a great restaurant, I love it, remember that" visibly adds the preference to state without touching every model call site.

### [145:09](https://youtu.be/SC5nO6iadsU?t=8709) Wrap-up and Q&A

Closing summary: planning comes from the model, action from tools, joined by the tool-calling loop; the two loops are the model choosing tools and exit, and the harness checking constraints and re-calling. Q&A: a 30-person Barcelona workshop run on a cheap OpenAI mini model cost $1.50 of a $100 budget, and different components can use different models (mini extractor, stronger planner); multi-agent orchestration is "just code that calls multiple things", needing no special framework support beyond what Spring already offers. Books raffled to the most frequent questioners.

## Tools, libraries and specs

- Spring AI (ChatClient, structured output converters, `@Tool`, advisors incl. tool-calling advisor, observability/metrics)
- Spring Boot, Spring MVC (`@RequestBody` analogy), Spring AOP (advisor inspiration), Spring HATEOAS (repo README only)
- OpenAI API (cheap GPT mini model for demos; native `response_format` structured output), ChatGPT (advanced voice mode, projects, skills), Claude/Anthropic (Opus 4.5, Sonnet; desktop app container), Gemini, Mistral, GPT-OSS (14 GB vs 65 GB quantizations)
- Claude Code, Codex (built the demos' spy/inspector; wrote prompts), `skill.md`, MCP (Model Context Protocol, out-of-process tools)
- Repo: `asaikali/art-of-building-agents` (`foundations/01-04`, `meal-agent/01-06`, Vue.js inspector UI); IntelliJ IDEA, Java 21, Jackson, RAG/embeddings/vector stores (mentioned, not covered)

## Who should watch

Java and Spring developers curious how agents work under the hood, especially those evaluating Spring AI or designing tool boundaries and verification for agent systems. Beginners get a complete, patient build-up; experienced agent builders can skip the foundations but may still take the acceptance-rate framing and checker taxonomy. Those wanting production hardening, RAG internals, or non-Java stacks should look elsewhere.

## Verdict

**7/10**: a progressively built dinner-planning agent with visible model traffic, explanatory code walkthroughs and a published teaching repository, limited by an unfinished booking goal and anecdotal cost evidence.

**Reach segment**: Spring developers adding agent or LLM features to their applications can reuse the alignment, tool-calling, checker, and memory patterns directly.

**Novelty 1/2**

- **+** [27:16](https://youtu.be/SC5nO6iadsU?t=1636) The speaker's dinner-planning teaching case brings requirements alignment, evaluation, decision support and memory together beyond isolated Spring AI reference examples.

**Demonstrated 1/2**

- **+** [48:20](https://youtu.be/SC5nO6iadsU?t=2900) Intent alignment runs live, each utterance advancing the versioned requirements JSON to version three.
- **+** [119:40](https://youtu.be/SC5nO6iadsU?t=7180) Evaluated planning runs live and returns vegetarian-suitable restaurants, after a restart from launching the wrong application at [118:34](https://youtu.be/SC5nO6iadsU?t=7114).
- **−** [15:47](https://youtu.be/SC5nO6iadsU?t=947) The stated goal includes booking a reservation under company expense policy, but the running example stops at recommendations and remembered preferences.

**Measured 1/2**

- **+** [146:42](https://youtu.be/SC5nO6iadsU?t=8802) The speaker reports that a 30-person workshop consumed $1.50 on a cheap mini model.
- **−** [147:14](https://youtu.be/SC5nO6iadsU?t=8834) He explicitly says he did no cost analysis, leaving that total without a workload baseline or comparison.

**Depth 2/2**

- **+** [37:47](https://youtu.be/SC5nO6iadsU?t=2267) The wire trace shows how Spring AI turns an entity request into JSON-schema "prompt begging".
- **+** [69:46](https://youtu.be/SC5nO6iadsU?t=4186) Statelessness explains why each tool turn resends the full history, which the wire trace then shows.
- **+** [145:09](https://youtu.be/SC5nO6iadsU?t=8709) The two-loop model (the model decides when to exit the tool-calling loop, the harness decides whether to call it again) states the control flow precisely.

**Reusable 2/2**

- **+** [00:41](https://youtu.be/SC5nO6iadsU?t=41) The opening slide links [asaikali/art-of-building-agents, branch 2026-devoxx-be](https://github.com/asaikali/art-of-building-agents/tree/2026-devoxx-be), a teaching repository containing the foundations applications and cumulative meal-agent examples.
