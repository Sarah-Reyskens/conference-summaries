---
title: "AI without spaghetti: Clean architecture in the age of AI"
talkId: "5503"
conference: devoxx-be-2026
speakers: [Maarten Vandeperre, Lutske van der Meer]
track: Development Practices
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=E--oDq3X74E
durationMin: 46
slides: https://github.com/luma-repositories/presentations
verdict: 7
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# AI without spaghetti: Clean architecture in the age of AI
Maarten Vandeperre, Lutske van der Meer · Conference · Development Practices
Slides: https://github.com/luma-repositories/presentations

## TL;DR
Two speakers vibe-coded a recipe app from a static page into an AI chatbot over a year, watched the generated code turn into spaghetti, then refactored it into clean architecture enforced by ArchUnit tests. The talk argues that dependency-free domain cores, per-use-case boundaries, and CI-level architecture validation matter more, not less, when AI writes the code.

## Key takeaways
- Vibe coding defaults to service-oriented layering where ORM entities and AI clients leak into business logic; budget a deliberate refactor to ports and use cases afterward.
- One use case per user action avoids the shared-service trap where extending one endpoint risks breaking the 500 others that call the same update method.
- Treat every model or runtime swap as a dependency change: the Java contract stays identical, but prompts and behavior shift, so revalidate.
- Split guardrails by layer: size limits and prompt-injection protection belong in infrastructure, business rules like "no pineapple on pizza" belong in the domain.
- Keep architecture tests, schema migrations, and end-to-end tests somewhere the coding agent cannot edit, for example a Git submodule pulled in at CI time.
- A multi-agent pipeline (OpenAI as product owner, Claude as architect, local Qwen as junior implementer) cut their token costs, but only when the small model got reasoning disabled and precise tasks.

## Notes

### [02:44](https://youtu.be/E--oDq3X74E?t=164) Leo and the vibe-coding experiment
The framing story: Leo, a non-developer, wants to cook his Italian grandmother's spaghetti from a recipe he cannot read. The speakers built the app for him by vibe coding since late 2025, one Git branch per evolution stage, with the prompts published in a prompts folder so viewers can replay them. Early tooling lessons: they settled on OpenCode after trying several CLIs, burned through $20/month model subscriptions into 7-hour token waits, and once discovered at branch five that copied agent skills had generated the whole codebase in Kotlin instead of Java.

### [04:49](https://youtu.be/E--oDq3X74E?t=289) Static site, Quarkus backend, and a database
Branch 01 served a scraped 90s-style static recipe site through a Python HTTP server. Branch 02 added a Quarkus and Java REST backend. Branch 03 added Postgres, and the live code walk showed the first smell: Hibernate Panache entities leaking from the persistence layer through the codebase. An unreviewed styling prompt had also painted the UI red because the Italian flag contains red, which cost hours of confused debugging.

### [12:08](https://youtu.be/E--oDq3X74E?t=728) From Tesseract OCR to AI extraction
Leonito junior gained recipe upload via Tess4J with Italian language files; on stage it produced unreadable gibberish from the photographed recipe. Leonito senior replaced OCR with LangChain4j model calls, and the same recipe came back as structured English ingredients and steps. The AI client landed in the infrastructure layer next to persistence. Twice the agent rewrote the Flyway scripts and dropped the database, which motivated the later CI protections.

### [21:03](https://youtu.be/E--oDq3X74E?t=1263) Clean architecture, use cases, and sovereignty
The center is a dependency-free domain (only the language itself, and not even its filesystem access), wrapped by use cases that each map one user action, then ports and infrastructure on the outside. Services get reused across endpoints and break them; use cases duplicate incidentally instead. A thin wiring layer over open standards such as Jakarta lets the same core ship on Quarkus, Spring Boot, or Open Liberty. Sovereignty got the same treatment: independence from vendors and technology, where data residency alone does not qualify because jurisdiction still applies.

### [26:12](https://youtu.be/E--oDq3X74E?t=1572) Branch 7: models refactor to clean architecture
OpenAI produced a reasonable domain, ports, and use-case split, while Claude misplaced ports inside the domain and, worse, both outputs were a single Gradle module following the package shape with nothing enforced at compile level. Token costs forced a rethink: a multi-agent OpenCode setup with OpenAI writing user stories, Claude turning them into minimal technical tasks, and a local Qwen implementing them. A fresh overnight run with Qwen3, GPT-5-class, and Claude models had only produced the Gradle structure after an hour, partly because reasoning was left enabled on the implementer model.

### [33:34](https://youtu.be/E--oDq3X74E?t=2014) Leonardo the chatbot and its guardrails
Branch 08 added a chat UI backed by a ChatModelProducer that builds OpenAI-compatible models with configurable endpoint, temperature, and token limits, keeping model choice a swappable infrastructure detail. The live demo answered a cheese question with recipe suggestions. Guardrails covered input and output validation, rate limiting, and output token caps, with the BMW-chatbot-recommending-a-Tesla anecdote as the warning, and NeMo Guardrails named as a proxy option in front of OpenAI-compatible endpoints.

### [38:54](https://youtu.be/E--oDq3X74E?t=2334) ArchUnit: enforcing the layers in CI
Branch 09 added ArchUnit tests such as "domain must not depend on any framework". On stage the suite ran green, then a planted domain class using an application-scoped annotation turned it red with the violated rule named. The speakers recommended injecting these tests via Git submodule so agents and CI drift cannot silently rewrite them, and applying the same protection to integration tests and migration schemas.

## Tools, libraries and specs
- Quarkus 3.32 (backend runtime, dev mode on stage)
- LangChain4j (AI client integration)
- Tess4J / Tesseract with Italian language data (original OCR path)
- Postgres via Hibernate ORM with Panache, Flyway migrations, Podman for local DB
- OpenCode with multi-agent setup (OpenAI, Claude, Qwen 3.8 running locally)
- ArchUnit (layer dependency tests)
- NeMo Guardrails (mentioned as guardrail proxy for OpenAI-compatible endpoints)
- React frontend, Gradle multi-module builds, vLLM / Ollama / Podman Desktop (mentioned inference runtimes)

## Who should watch
Developers who let AI assistants generate application code and want a concrete refactoring target plus enforcement tactics will gain most. Viewers fluent in ports-and-adapters or hexagonal architecture can skim the middle segment, and anyone wanting guardrail implementation detail should watch the companion talk the speakers linked instead.

## Verdict
**7/10**: A year-long vibe-coding experiment with a published branch-per-stage repo and a working ArchUnit enforcement demo, held back by an unfinished multi-agent refactor and anecdotal cost figures.

**Novelty 1/2**

- **+** [28:15](https://youtu.be/E--oDq3X74E?t=1695) The speakers ran the same clean-architecture refactor through OpenAI and Claude and report how the outputs differed: OpenAI's domain/ports/use-case split was reasonable, Claude put the ports inside the domain.
- **+** [29:51](https://youtu.be/E--oDq3X74E?t=1791) Their multi-agent OpenCode pipeline (OpenAI as product owner, Claude as architect, local Qwen as junior implementer) comes from their own experiment.
- **−** The clean-architecture explanation is the ports-and-use-cases material that the hexagonal and clean-architecture literature gives in a first search.

**Demonstrated 1/2**

- **+** [41:01](https://youtu.be/E--oDq3X74E?t=2461) The ArchUnit suite runs green, then fails with the violated rule named once a domain class using an application-scoped annotation is planted ([42:04](https://youtu.be/E--oDq3X74E?t=2524)).
- **+** [20:00](https://youtu.be/E--oDq3X74E?t=1200) The same photographed recipe comes out as gibberish through Tesseract ([15:47](https://youtu.be/E--oDq3X74E?t=947)) and as structured English through the AI path, though with an odd "three and a half" mozzarella quantity.
- **−** [31:28](https://youtu.be/E--oDq3X74E?t=1888) The refactor to clean architecture is never run: branch 7 appears as static code, and the refreshed multi-agent run was unfinished, with only the Gradle structure generated after an hour.

**Measured 1/2**

- **+** [06:25](https://youtu.be/E--oDq3X74E?t=385) The speakers quote their spend: $20/month subscriptions running into 7-hour waits.
- **·** [26:43](https://youtu.be/E--oDq3X74E?t=1603) The "$300 lost" on one API-key run is a self-reported anecdote with no usage baseline or per-model breakdown.
- **−** [44:08](https://youtu.be/E--oDq3X74E?t=2648) The claim that clean-architecture boundaries shrink the context and "really reduce your costs" comes with no figure or before/after comparison.

**Depth 2/2**

- **+** [22:04](https://youtu.be/E--oDq3X74E?t=1324) The use-case-versus-service distinction is argued through the failure mode it prevents (one update method reused by 500 endpoints), with the accidental-duplication trade-off named at [22:34](https://youtu.be/E--oDq3X74E?t=1354).
- **+** [37:47](https://youtu.be/E--oDq3X74E?t=2267) Guardrails are split by architectural layer, with size and prompt-injection checks in infrastructure and business rules like "no pineapple" in the domain.
- **+** [44:08](https://youtu.be/E--oDq3X74E?t=2648) Isolation lets an architect model name which files change, which shrinks the context sent to the LLM and lets a smaller model make small edits.

**Reusable 2/2**

- **+** [10:03](https://youtu.be/E--oDq3X74E?t=603) Every demo branch plus the prompts folder is published under github.com/luma-repositories for replay with other models.
- **+** [39:27](https://youtu.be/E--oDq3X74E?t=2367) The ArchUnit rules that enforce the talk's architecture are shown in the branch 09 code on screen.
- **−** [32:31](https://youtu.be/E--oDq3X74E?t=1951) The refreshed overnight multi-agent branch was unpublished at talk time ("I will push it on this repository").
