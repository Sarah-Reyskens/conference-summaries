---
title: No Country For Old APIs. Wrapping legacy Java services as MCP tools without rewriting them.
talkId: "16426"
conference: devoxx-be-2026
speakers: [Željko Kozina]
track: Architecture & Modernization
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=a5cQAl0g2AM
durationMin: 45
slides: null
verdict: 6
frames: 9
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# No Country For Old APIs. Wrapping legacy Java services as MCP tools without rewriting them.

Željko Kozina · Conference · Architecture & Modernization

## TL;DR

Kozina argues that legacy Java, REST, and SOAP services should reach AI agents through a GraphQL layer exposed as MCP tools, not by pointing models at existing APIs or rewriting everything. He demonstrates the recipe live on Spring PetClinic: add GraphQL, generate tools from curated operations, secure writes with Keycloak scopes, and scale to large schemas with embedding search over the schema.

## Key takeaways

- Put a GraphQL layer between legacy APIs and MCP tools: its typed schema already carries the name, description, input, and output each tool needs.
- Expose curated, reviewed GraphQL operations as tools rather than auto-generating one tool per endpoint, and keep auto-generation off by default.
- Treat prompt/model behavior as a regression suite: run graded question sets across models with a tool like promptfoo, including questions that must not invoke any tool.
- Test writes separately from reads, because an agent mid-evaluation can mutate fixtures and poison every later assertion.
- Secure MCP with per-operation scopes (baseline scope for reads, extra scope for writes) enforced through the identity provider, not the prompt.
- For large schemas, shrink hundreds of tools to three (schema search, type introspection, GraphQL execution) so the model assembles its own queries.
- Adding a GraphQL field is a safe, opt-in operation, which makes expensive legacy-backed fields cheaper to introduce than new REST fields.

## Notes

### [00:34](https://youtu.be/a5cQAl0g2AM?t=34) Legacy APIs and pressure to expose everything to AI

Kozina opens with "architecture shaming": teams call their own stable, secure monoliths awful because other stacks look shinier. Business now wants internal data and processes exposed to AI, while developers answer that everything would need a rewrite. His position is to start experimenting with a small, reversible step instead of rebuilding.

### [04:11](https://youtu.be/a5cQAl0g2AM?t=251) A GraphQL layer instead of models calling APIs

BFFs (one endpoint set per frontend) do not scale, and pointing an LLM directly at production APIs is an architecture he rejects. His proposal: replace the BFF sprawl with one GraphQL API, then expose that to agents as MCP tools. GraphQL suits agents because a client fetches exactly the fields it needs in one round trip.

### [05:46](https://youtu.be/a5cQAl0g2AM?t=346) Demo: adding GraphQL to Spring PetClinic

Working branch by branch on the Thymeleaf-based PetClinic, he adds `spring-boot-starter-graphql`, a typed schema with queries and mutations, and `@QueryMapping`/`@MutationMapping` controllers backed by Java records. GraphQL enforces separated read/write models (CQRS by design). In the GraphiQL editor he builds up an owner query field by field (names, pet names, types, visits, vets), showing precise data fetching.

### [10:04](https://youtu.be/a5cQAl0g2AM?t=604) GraphQL operations map onto MCP tools

An MCP tool needs a name, description, typed input, and output; a GraphQL operation already has all four. Because the agentic ecosystem churns too fast for enterprise release cycles, he wrote his own small library that turns a curated set of reviewed GraphQL operations into MCP tools (and in-process tools). Adding the dependency plus one property exposes the operations; he warns against exposing every read and write automatically.

### [14:46](https://youtu.be/a5cQAl0g2AM?t=886) Testing the plumbing: MCP Inspector and MCPJam

He first checks conformance with MCP Inspector (10 tools: 5 reads, 5 writes; scalar fields returned by default), then asks questions across three local models side by side in MCPJam. The models list pet types and find the vet without a specialty. A write demo shows schema validation doing its job: creating an owner fails until address and 10-digit phone are supplied.

### [17:26](https://youtu.be/a5cQAl0g2AM?t=1046) Curated operations with better descriptions

Auto-generation is switched off in favor of ten hand-written operations with precise descriptions. Trickier questions now work: only Gemma notices that `birthDate` is required when adding a pet, while the other models invent the value. The segment makes the case that tool quality comes from curation, not coverage.

### [21:36](https://youtu.be/a5cQAl0g2AM?t=1296) Regression-testing prompts with promptfoo

Manual testing does not scale, so he grades fixed question sets of increasing difficulty against one model per provider with promptfoo, verifying both the tool called (with arguments) and the answer returned, plus questions that must trigger no tool. The on-screen report lists historic runs of different eval setups with per-assertion pass/fail rows; aloud he describes the results only as "quite good". One cautionary run: an agent updated three pets mid-evaluation and broke later checks, so he now tests reads with writes disabled.

### [24:47](https://youtu.be/a5cQAl0g2AM?t=1487) Live SOAP: Antwerp off-leash dog zones

The legacy proof: a real Antwerp government SOAP service (WSDL-defined, XML request/response) exposing off-leash dog areas with distance, cleanliness, lighting, and surface. He adds one field to the GraphQL `Owner` type backed by two SOAP calls (geocode, then zone lookup) and asks where Mr. Devox can walk his dog; the agents chain the owner lookup and the zone tool against the live API. New GraphQL fields stay opt-in, unlike REST fields that every caller receives.

### [29:00](https://youtu.be/a5cQAl0g2AM?t=1740) Securing tools with Keycloak scopes

The MCP client gets a 401, signs in via Keycloak, and presents a token; all tools require a baseline scope while write operations carry a directive demanding an extra scope. Live login as a read-only user reads fine but is denied the write scope; logging in as a read-write user authorizes and completes the mutation. Configuration is Spring Security plus Keycloak properties.

### [33:18](https://youtu.be/a5cQAl0g2AM?t=1998) Scaling past tool sprawl: RAG over the schema

Integrating more government APIs grows the schema from 5 root fields and 16 types to almost 300 fields, about 13,000 lines of schema code, and 111,000 tokens. Instead of 274 tools, he embeds every field with its description plus its query path and exposes three tools: `searchSchema` (find fields by meaning), an introspect-type tool for complex inputs, and `executeGraphQL`, with the agent instructed to search before writing queries. Embeddings use a GraphQL-specialized model from the GraphQL AI working group; simple questions answer on local models, while harder multi-index comparisons need a stronger model (Claude) after the laptop strains. For scale context: GitHub's public GraphQL schema is ~300k tokens, Netflix's ~4M.

### [42:41](https://youtu.be/a5cQAl0g2AM?t=2561) Curated operations versus dynamic tools

The closing slide contrasts the two modes: curated operations are reviewed in a pull request, small, cheap, and predictable, covering planned questions; the dynamic three-tool mode lets the model write queries across the whole schema for the long tail. His recommendation is both: curated tools for common questions, dynamic search as the override. He also notes MCP tool documentation is still mostly "the tool definition is the docs".

## Tools, libraries and specs

- Spring PetClinic (demo base, branch-per-step repo)
- Spring for GraphQL (`spring-boot-starter-graphql`, `@QueryMapping`, `@MutationMapping`)
- Model Context Protocol (MCP) tool calling; Anthropic tool-search capability
- Speaker's own GraphQL-to-MCP tools library (name inaudible in captions)
- MCP Inspector (spec-conformance testing)
- MCPJam (multi-model side-by-side testing: Qwen, Gemma, GPT-OSS)
- Ollama (local model and embedding runtime)
- promptfoo (graded prompt regression suites)
- Keycloak (OAuth/OIDC login, baseline + write scopes) with Spring Security
- Antwerp government SOAP/WSDL geodata services (geocoding, off-leash dog zones)
- Eurostat public REST endpoints (index comparisons in the scale demo)
- GraphQL-specialized embedding model from the GraphQL AI working group

## Who should watch

Brownfield Java developers asked to connect legacy SOAP/REST estates to AI agents, and architects weighing GraphQL as an agent-facing layer. Skip if you already ship GraphQL-backed MCP servers with scoped auth, or if you want MCP protocol internals rather than an integration recipe.

## Verdict

**6/10**: Live brownfield recipe (Spring GraphQL over a real SOAP service, Keycloak write scopes, dynamic schema search) that runs on screen, limited by techniques with published counterparts, an evaluation report with no stated results, and no linked artifact.

**Novelty 1/2**

- **+** [11:06](https://youtu.be/a5cQAl0g2AM?t=666) The speaker built his own library that turns reviewed GraphQL operations into MCP and in-process tools, because anything agentic is "behaving like a JavaScript framework" against slower enterprise release cycles.
- **+** [24:47](https://youtu.be/a5cQAl0g2AM?t=1487) A live Antwerp SOAP service behind one GraphQL field, secured with Keycloak scopes and checked with promptfoo, is the speaker's own brownfield combination.
- **·** [36:29](https://youtu.be/a5cQAl0g2AM?t=2189) The embedding model and schema-search approach come from the GraphQL AI working group, as the speaker says.

**Demonstrated 2/2**

- **+** [27:59](https://youtu.be/a5cQAl0g2AM?t=1679) The SOAP-backed dog-zone lookup chains the owner tool and the live government service on screen end to end.
- **+** [31:08](https://youtu.be/a5cQAl0g2AM?t=1868) Keycloak login, scope denial for the read-only user, and authorized write for the read-write user all run live.
- **−** [39:07](https://youtu.be/a5cQAl0g2AM?t=2347) In the three-tool large-schema mode two models "just gave up" and the run completes only after switching to Claude.

**Measured 1/2**

- **+** [23:11](https://youtu.be/a5cQAl0g2AM?t=1391) The promptfoo report asserts both the tool called and the answer returned, with per-assertion pass/fail rows visible.
- **−** [23:11](https://youtu.be/a5cQAl0g2AM?t=1391) The report lists historic runs of different eval setups, and the speaker states no pass rate or per-model comparison beyond "quite good".
- **−** [34:22](https://youtu.be/a5cQAl0g2AM?t=2062) "We can do better" than Anthropic's tool search and Spring's implementation of it is claimed without a comparison.

**Depth 1/2**

- **+** [04:11](https://youtu.be/a5cQAl0g2AM?t=251) Rejects pointing the LLM at APIs and per-client BFFs in favor of one GraphQL layer, with scaling as the stated reason for BFFs and preference for the direct case.
- **+** [42:41](https://youtu.be/a5cQAl0g2AM?t=2561) Compares curated operations with dynamic model-written queries on review in a pull request, cost, predictability and coverage.
- **−** [34:54](https://youtu.be/a5cQAl0g2AM?t=2094) The embedding search internals (what is embedded, ranking, the three-step process) are named but not explained.

**Reusable 1/2**

- **+** [30:05](https://youtu.be/a5cQAl0g2AM?t=1805) The Keycloak and Spring Security configuration is walked through on screen: starter dependency, Keycloak properties and the baseline-scope setup.
- **−** [05:46](https://youtu.be/a5cQAl0g2AM?t=346) A step-per-branch demo repository is mentioned, but no URL or library coordinates are given at any point in the talk.
