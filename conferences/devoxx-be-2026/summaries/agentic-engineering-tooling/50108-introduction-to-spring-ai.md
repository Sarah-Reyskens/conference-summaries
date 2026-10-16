---
title: Introduction to Spring AI
talkId: "50108"
conference: devoxx-be-2026
speakers: [Timo Salm]
track: Agentic Engineering & Tooling
sessionType: Lunch Talk
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=JzFelLDiVJQ
durationMin: 43
slides: null
verdict: 6
reach: segment
frames: 9
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Introduction to Spring AI
Timo Salm · Lunch Talk · Agentic Engineering & Tooling

## TL;DR
Spring AI wraps provider REST APIs in one Spring Boot programming model, and everything advanced (RAG, tool calling, agentic loops) builds on three concepts: ChatClient, advisors, and tools. The talk walks each concept with live code from a recipe-finder sample, then gestures at MCP, observability, and testing as next steps.

## Key takeaways
- Reach for `ChatClient` (fluent API with advisors, templates, structured output) for everyday work; use the low-level `ChatModel.call(Prompt)` only when you need explicit control over every request.
- Spring AI 2.0 requires Spring Boot 4, and provider swaps are meant to be configuration-only thanks to auto-configuration and the starter model on start.spring.io.
- Advisors are RestClient-style interceptors around every ChatClient call, and the built-in `QuestionAnswerAdvisor` plus a vector store is the entire retrieval side of naive RAG.
- Watch advisor order: a logging advisor placed before RAG sees the raw prompt, while one placed after sees everything RAG added.
- Tool calling works by sending method metadata to the model, letting it request calls, and looping results back; Spring AI handles the loop, running any `@Tool`-annotated Java method for you.
- MCP servers are worth building when a capability should be shared across teams or from a platform team to its users; for one-app-only functions, plain `@Tool` methods suffice.

## Notes

### [02:10](https://youtu.be/JzFelLDiVJQ?t=130) Why models need a harness
The on-stage title was "Building AI Agents with Spring AI"; the speaker noted 40 minutes only allowed the fundamentals. He framed the talk around model limitations: token-by-token generation means fluent but possibly wrong answers, models are stateless (ChatGPT-style memory is an external component resending history), they only know their training data, and they cannot act by themselves. RAG, tool calling, and memory mitigate these, but introduce token cost, context-window pressure from provider harnesses, new attack surfaces (an agent deleting a disk was the example), and governance and observability gaps. Spring AI exists to build the harness around the provider REST APIs.

### [09:00](https://youtu.be/JzFelLDiVJQ?t=540) Fundamentals: ChatModel versus ChatClient
Spring AI is Spring Boot based, so starters and auto-configuration do the wiring; the OpenAI starter plus a model name and API key is enough to start. The YAML on screen configured `spring.ai.openai.chat.options.model: gpt-5-mini`, temperature 0.7, and a max-completion-tokens value. Two APIs cover model interaction, shown side by side on one slide:

```java
// from slide at 16:30
ChatResponse response = chatModel.call(
    new Prompt("Tell me about Spring AI"));
String text = response.getResult()
    .getOutput().getText();
```

```java
// from slide at 16:30
String answer = chatClient.prompt()
    .user("Tell me about Spring AI")
    .call()
    .content();
```

`ChatModel` is the low-level, provider-independent wrapper (also available for image and audio models); unlike it, `ChatClient` is not auto-configured, only its builder is, so teams typically expose one preconfigured client bean with default system prompts and advisors. Prompt templates use `{curly-brace}` placeholders by default, and `.entity(Recipe.class)` maps output straight to objects. Structured output has a native mode for providers that support it and a fallback that injects a JSON-schema instruction into the prompt and ObjectMapper-parses the reply; weak local models such as Llama 3.2 sometimes return incompatible JSON.

### [20:59](https://youtu.be/JzFelLDiVJQ?t=1259) RAG and the Advisors API
RAG splits into indexing (load documents, split into chunks, embed, store vectors) and per-request retrieval (embed the query, similarity-search top-K above a threshold, augment the prompt, generate). The slide's summary line: the model itself does not change; RAG only changes what goes into the prompt. In Spring AI both sides hang off the Advisors API, interceptors with a before and an after step chained around each call, in blocking (`CallAdvisor`) and streaming (`StreamAdvisor`) variants, with a shared context map (for example a conversation id). Indexing uses document readers (PDF, Markdown), splitters, and writers, where the vector store itself is the writer. Retrieval is the out-of-the-box `QuestionAnswerAdvisor`, configured with the vector store, a `SearchRequest` (top-K, similarity threshold), and an optional prompt template; the live code used `topK(2).similarityThreshold(0.7)` with a "prefer our own recipe, do not invent" prompt. A more modular RAG advisor exists for custom pipelines. One more advisor type matters for agents: the recursive advisor copies the chain so a sub-loop (an LLM-as-judge rating gate, a structured-output validation retry) can rerun in isolation.

### [32:35](https://youtu.be/JzFelLDiVJQ?t=1955) Tool calling and MCP
Tool calling was presented as the enabler of agents alongside MCP. The flow: the app sends the prompt plus tool definitions, the model replies with a tool-call request and arguments, the app runs the tool and sends the result back, repeating until a final answer is ready. Annotating a method with `@Tool(description = ...)` plus `@ToolParam` details generates the name, description, and input schema from the method signature, and `.tools(this)` registers an instance on the client:

```java
// from slide at 35:20
@Tool(description = "Lists ingredients at home")
List<String> ingredientsAtHome() { ... }

Recipe recipe = chatClient.prompt()
    .user("Suggest a recipe with cheese")
    .tools(this)
    .call().entity(Recipe.class);
```

The MCP section argued for reuse over rebuilding tools per app, citing the GitHub MCP server (read issues, open pull requests) as the canonical example. Spring AI ships first-class MCP support and the team contributes to the MCP Java SDK; consuming a server is configuration plus the auto-configured tool provider as default tools, while exposing one needs the server starter and `@MCPTool` (kept distinct from internal `@Tool` methods) plus prompt-serving annotations. The session's second sample, a nutrition planner, was named as the multi-step, human-in-the-loop agentic demo but not walked through.

### [40:30](https://youtu.be/JzFelLDiVJQ?t=2430) Observability, testing, and next steps
The last minutes compressed the remaining topics: auto-instrumented observability wired through Spring Boot 4 OpenTelemetry support into a Grafana stack, and testing support that uses LLMs as judges because responses are non-deterministic. Both were mentioned, not demoed. The speaker closed by pointing to his free Spring AI course on Spring Academy (registration required for the hands-on labs against a mocked OpenAI API; the experimental-patterns module was still marked coming soon on staging), the recipe-finder and nutrition-planner samples on GitHub, and a follow-up workshop on agentic patterns with Sandra Ahlgrim.

## Tools, libraries and specs
- Spring AI 2.0 (Spring Boot 4 only) with start.spring.io starters
- OpenAI (`gpt-5-mini` chat, `gpt-image-1.5`), Azure OpenAI, Anthropic, Ollama (Llama 3.2)
- MCP (Model Context Protocol) and the MCP Java SDK; GitHub MCP server as example
- Spring Academy Spring AI course; timosalm/spring-ai-recipe-finder and nutrition-planner samples
- OpenTelemetry with Grafana stack for observability

## Who should watch
Spring developers evaluating Spring AI gain a compact map of ChatClient, advisors, RAG, tools, and MCP with real configuration and code. Skip it if you already build with Spring AI or want depth on evaluation loops, MCP servers, or production operations; those get minutes, not demonstrations.

## Verdict
**6/10**: The beginner-level mental models for advisors and tool calling and the published recipe-finder sample earn the score; the API tour shows code without an application run.

**Reach segment**: Spring Boot developers adding LLM features to their applications can use it; Quarkus and Jakarta EE teams in the audience cannot adopt Spring AI directly.

**Novelty 1/2**

- **·** The Spring AI team's tour of its own framework earns the project-author baseline of 1: the official Spring AI reference documentation at docs.spring.io/spring-ai covers these features, and the talk adds no production experience or cross-source synthesis beyond that baseline.

**Demonstrated 0/2**

- **−** [10:02](https://youtu.be/JzFelLDiVJQ?t=602) The start.spring.io walkthrough covers project setup only; no application output appears anywhere in the talk.
- **−** [18:53](https://youtu.be/JzFelLDiVJQ?t=1133) Structured output through `.entity(Recipe.class)` with native and fallback modes is walked through in code without running the recipe finder.
- **−** [30:01](https://youtu.be/JzFelLDiVJQ?t=1801) RAG with `QuestionAnswerAdvisor` is declared implemented after the configuration walkthrough, with no query or answer shown.

**Measured 1/2**

- **·** [05:51](https://youtu.be/JzFelLDiVJQ?t=351) The talk makes no quantitative claim: token-cost and context-window warnings are qualitative, and top-K and similarity threshold are configuration knobs with no effect claim.

**Depth 2/2**

- **+** [27:17](https://youtu.be/JzFelLDiVJQ?t=1637) Advisor order is explained through logging placement: a logger before RAG sees the raw prompt, one after sees the augmented prompt.
- **+** [30:31](https://youtu.be/JzFelLDiVJQ?t=1831) Recursive advisors copy the advisor chain so a sub-loop, such as an LLM-rated evaluation that reruns on a low score, can run without repeating the surrounding advisors.
- **+** [33:39](https://youtu.be/JzFelLDiVJQ?t=2019) The tool-calling round trip is explained end to end: prompt plus tool metadata, the model's tool-call request with arguments, the app running the method, and the result sent back in the next prompt.

**Reusable 2/2**

- **+** [42:02](https://youtu.be/JzFelLDiVJQ?t=2522) The closing slide points to the recipe-finder sample, the project whose code was shown, and the nutrition-planner sample for multi-step and human-in-the-loop patterns.
- **+** [41:02](https://youtu.be/JzFelLDiVJQ?t=2462) The free Spring Academy course covers the capabilities with hands-on labs against a mocked OpenAI API.
- **−** [41:32](https://youtu.be/JzFelLDiVJQ?t=2492) The course's experimental-patterns module was still marked coming soon on staging.
