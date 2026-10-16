---
title: "From User Prompt to JPA Query: Comparing Tool Calling, Structured Output & Hybrid Approach"
talkId: "50106"
conference: devoxx-be-2026
speakers: [Sebastian Kühnau]
track: Agentic Engineering & Tooling
sessionType: Lunch Talk
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=-2vEfnB2mRw
durationMin: 39
slides: null
verdict: 8
reach: segment
frames: 11
summarizedAt: 2026-10-14
reviewedAt: 2026-10-15
---

# From User Prompt to JPA Query: Comparing Tool Calling, Structured Output & Hybrid Approach

Sebastian Kühnau · Lunch Talk · Agentic Engineering & Tooling

## TL;DR

Kühnau replaces complex filter forms over a Vaadin customer grid with a natural-language text field, implementing the prompt-to-query step three ways in Spring AI (tool calling, structured output, and a hybrid) and benchmarking all of them on local Ollama models. Structured output wins as the default: a typed filter object passes every capability test in a single LLM round trip at a fraction of the hybrid's token cost, and the approach matters more than the model choice.

## Key takeaways

- Make structured output the default for prompt-to-query: one typed filter object expresses multi-value, negation, and range conditions in a single LLM round trip.
- Reach for tool calling when the model needs extra runtime context (such as the current date), and budget for it: every tool round trip re-sends context and measurably adds input tokens and latency.
- A well-defined target structure beats a bigger model: qwen3:8b with structured output passed 97% of cases while larger models on flat tool calling fell below 50%.
- Precompute relative dates in Java and inject them into the system prompt instead of asking the model to do date arithmetic.
- Never show the model the rows: extract filter values only, build the JPA Specification in Java, and keep customer data out of the prompt entirely.
- Stay filter-only until guardrails exist: the prompt-injection test case is disabled because nothing yet stops injected instructions from clearing the filter.

## Notes

### [00:35](https://youtu.be/-2vEfnB2mRw?t=35) Filtering is the hard part of data grids

Vaadin renders a customer table in three lines of code, and column sorting comes free. Filtering is where it breaks down: per-column text fields allow only one value per column, while a full filter form turns into an unusable wall of inputs with unsolved questions like how to enter several cities or prefix versus suffix matching. The talk's goal is a text field accepting sentences like "show me all customers from Berlin with an order this year".

### [03:43](https://youtu.be/-2vEfnB2mRw?t=223) LLM options in Java

LangChain4j is the most established framework, Spring AI covers Spring applications, and Koog targets Kotlin. The demo uses Spring AI throughout, and every concept transfers to the others. A Spring AI prompt combines a system prompt (constraints, roles, rules) with the user prompt; plain calls return strings. Annotating a Java method with `@Tool` gives the model access to dynamic data such as database content without stuffing it into the prompt.

### [06:50](https://youtu.be/-2vEfnB2mRw?t=410) The naive approach, and why it is unacceptable

The first attempt hands the whole database table to the model and asks it to return the relevant customer IDs. It works and is simple, but it leaks every secret on the table into the prompt, burns tokens in proportion to data size, and ships sensitive rows to a commercial provider's future training data. Since every filter form ends in a SQL query anyway, the better design extracts filter values from the prompt and keeps the database behind the application.

### [08:55](https://youtu.be/-2vEfnB2mRw?t=535) Approach 1: tool calling with flat parameters

The system prompt frames the task ("filter the customers, extract values, call searchCustomers once and then stop"), each filter field becomes a `@ToolParam` with a short description, and the current date-time is injected so the model stops guessing dates. The `searchCustomers` method carries `returnDirect = true`, which ends the conversation when called instead of making another model round trip. Returned values land in a `CustomerCriteria` DTO that becomes a Spring Data JPA Specification. AI calls run on a background thread so the UI never freezes during the one-to-five-second round trip.

### [15:39](https://youtu.be/-2vEfnB2mRw?t=939) Flat parameters hit a wall, then get extended

Single values, German queries ("München"), and exact dates ("yesterday") work. Multiple values ("Berlin or Hamburg"), negations ("all customers except those from Berlin"), and periods ("the last 6 months") fail because each field holds one scalar. Adding an operator and a negate flag per field fixes negation and periods, but triples the parameter count and its `@ToolParam` descriptions, slowing the model down, and still cannot express two values for one field.

### [18:44](https://youtu.be/-2vEfnB2mRw?t=1124) Approach 2: structured output

The prompt carries the system prompt, the precomputed date, and the user query, and Spring AI's provider structured output contracts the answer to be a `CustomerFilter`: a record holding a list of conditions, each with field name, operator enum, value list, and negate flag, documented through Jackson annotations.

```java
// reconstructed from speech at 21:00
public record CustomerFilter(List<Condition> conditions) {}
public record Condition(String field, Operator operator, List<String> values, boolean negate) {}
```

One round trip returns the whole filter, and multi-value, negation, and range queries all pass. The price is rigidity: the answer must be a `CustomerFilter`, so no tool can be attached.

### [22:22](https://youtu.be/-2vEfnB2mRw?t=1342) Approach 3: the hybrid

The hybrid keeps the `CustomerFilter` target type but delivers it through a tool call with the current date attached as a tool, dropping the structured-output contract. The model usually returns the filter but is no longer bound to, so the implementation must validate the return type. It answers the same queries as structured output.

### [23:54](https://youtu.be/-2vEfnB2mRw?t=1434) Benchmark 1: the approaches against each other

Integration tests send prompts like "show all customers in Munich" and verify the returned rows: 6 warmup tests plus 9 capability tests, 10 repetitions on qwen3:8b with low temperature and thinking mode off. Structured output and hybrid pass all 15; flat tool calling passes 9, extended 11. Per request, structured output uses 812 tokens at 1,588 ms against the hybrid's 2,103 tokens at 2,594 ms, with spreads under ±5% except extended tool calling at ±11%.

### [28:33](https://youtu.be/-2vEfnB2mRw?t=1713) Benchmark 2: which local model

With 12 filter parameters and 59 cases (a 60th prompt-injection case stays disabled for lack of guardrails), six Ollama models each run 2,020 executions on a MacBook M2 Pro with Ollama 0.35.1. Qwen3:8b totals 1,980/2,020 (97% on structured output and hybrid) at 6.2 GB RAM; gemma4:26b-mlx matches it on structured output but needs 15.9 GB, leaving no room for an IDE. Llama3.1:8b collapses on the hybrid (27%). Response times on qwen3:8b run about 1.6 s median (P95 3.6 s) for structured output and 2.8 s (P95 5.8 s) for hybrid.

### [31:43](https://youtu.be/-2vEfnB2mRw?t=1903) Takeaways

Approach beats model choice: a precise prompt plus a well-defined target structure lets small local models win. Structured output is the default; tools are for extra context. Token cost comes from the extra round trips. The full project, demo, and benchmarks live at https://github.com/SebastianKuehnau/vaadin-grid-ai-filter.

### [33:16](https://youtu.be/-2vEfnB2mRw?t=1996) Live demo, fully offline

With Wi-Fi disconnected and everything on the laptop, queries across nine filter parameters narrow a hundred-row grid: Berlin only, Berlin with last year's orders, and last year alone return the expected rows. One multi-city attempt returns Munich and Cologne rows for a Berlin-and-Munich query and is replaced live with a Berlin-only query; the last-quarter query returns a September row plus a June row the speaker flags as wrong for the quarter.

### [35:50](https://youtu.be/-2vEfnB2mRw?t=2150) Source walkthrough and Q&A

The structured-output service method shows the long system prompt with precomputed relative dates (yesterday, last week, last month, last year) because deterministic Java date math beats model arithmetic. Asked about updates and aggregation, Kühnau says both are out of scope: no data manipulation, no group-by, and local models stay close to the predefined examples.

## Tools, libraries and specs

- Spring AI (ChatClient, `@Tool` / `@ToolParam` with `returnDirect`, provider structured output)
- Spring Data JPA Specifications, Vaadin Grid / Flow
- Ollama 0.35.1 with qwen3:8b (chosen), qwen3 MoE variants, gemma4 MoE variants, llama3.1:8b
- LangChain4j, Koog (mentioned as alternatives); Jackson annotations for structured-output metadata

## Who should watch

Java and Spring developers adding natural-language filtering to data-driven UIs, especially Vaadin users, and anyone choosing between tool calling and structured output for small local models. Skip it if you need LLM-driven updates or aggregation (declared out of scope) or already run this pattern in production with guardrails.

## Verdict

**8/10**: Benchmarks of four approaches and six local models with a stated setup, a clear mental model of when to pick structured output, and a repository covering each approach earn the score; the comparison is the speaker's own measurement rather than novelty a search lacks, and the live demo missed on the multi-city and last-quarter queries.

**Reach segment**: Spring developers adding natural-language filtering to data grids can put the prompt-to-query pattern to use.

**Novelty 1/2**

- **+** [03:43](https://youtu.be/-2vEfnB2mRw?t=223) The talk brings LangChain4j, Spring AI and Koog together and says the prompt-to-query concepts transfer across all three, more than any single framework's docs give.
- **+** [31:43](https://youtu.be/-2vEfnB2mRw?t=1903) The takeaways state a decision framework tested on the speaker's own cases: approach beats model choice, structured output by default, tools when extra runtime context is needed.
- **−** Spring AI's reference docs already cover both tool calling and structured output, so the mechanism knowledge is search baseline and the novelty rests on the synthesis above.

**Demonstrated 1/2**

- **+** [34:49](https://youtu.be/-2vEfnB2mRw?t=2089) Natural-language queries filter a hundred-row customer grid in the live app with Wi-Fi disconnected: Berlin with last year's orders and last year alone return the expected rows.
- **−** [33:46](https://youtu.be/-2vEfnB2mRw?t=2026) The Berlin and Munich query returned Munich and Cologne rows and was replaced by Berlin-only queries, so multi-value filtering was not shown working live.
- **−** [35:20](https://youtu.be/-2vEfnB2mRw?t=2120) The last-quarter query returned a June row alongside the September one, which the speaker flags as wrong.

**Measured 2/2**

- **+** [26:00](https://youtu.be/-2vEfnB2mRw?t=1560) The cost table reports tool calls, tokens and latency per request with median, range and spread: structured output at 812 tokens and 1,588 ms against hybrid at 2,103 tokens and 2,594 ms.
- **+** [29:45](https://youtu.be/-2vEfnB2mRw?t=1785) The model table pairs success rates with RAM and states the setup: 10 runs per case, MacBook M2 Pro, Ollama 0.35.1.
- **−** [27:01](https://youtu.be/-2vEfnB2mRw?t=1621) The spread runs to ±11% on extended tool calling, so that approach's numbers are less stable than the ±5% elsewhere.

**Depth 2/2**

- **+** [15:39](https://youtu.be/-2vEfnB2mRw?t=939) Flat tool parameters hold one scalar per field, which is why multiple values fail, and adding an operator and a negate flag per field triples the parameter count and slows the model.
- **+** [18:44](https://youtu.be/-2vEfnB2mRw?t=1124) Tool calling re-sends the full context on every round trip while structured output answers in one, which is why the token bills differ.
- **+** [36:22](https://youtu.be/-2vEfnB2mRw?t=2182) Relative dates are precomputed in Java because models are unreliable at date arithmetic.

**Reusable 2/2**

- **+** [38:55](https://youtu.be/-2vEfnB2mRw?t=2335) The closing slide gives the public repository github.com/SebastianKuehnau/vaadin-grid-ai-filter, named as holding the whole project with its demo and benchmarks.
- **+** [35:50](https://youtu.be/-2vEfnB2mRw?t=2150) The source walkthrough runs from that repository's code, whose four runnable apps cover each approach compared in the talk.
