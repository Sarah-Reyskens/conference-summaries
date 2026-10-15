---
title: MCP 2.0 - Stateless, New Auth (CIMD), and Exciting Extensions
talkId: "21691"
conference: devoxx-be-2026
speakers: [James Ward]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=fShgG3jtkXQ
durationMin: 51
slides: null
verdict: 6
frames: 11
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# MCP 2.0 - Stateless, New Auth (CIMD), and Exciting Extensions
James Ward · Conference · Agentic Engineering & Tooling

## TL;DR
MCP spec 2026-07-28 ("MCP 2.0") makes the transport stateless, replaces Dynamic Client Registration with Client ID Metadata Documents (CIMD), and turns extensions into a first-class mechanism with official Apps, Tasks, and Skills entries. The talk walks through each change with live demos in MCP Inspector, a Spring AI secured server, and an MCP App rendering EC2 instances inside Claude, and closes with a migration checklist for server developers.

## Key takeaways
- Put MCP servers in stateless mode now and replace session state with explicit resource handles (IDs passed per call), so the 2026-07-28 upgrade is painless.
- Turn on OAuth audience-claim validation and move clients to CIMD, where the client_id is a URL serving a JSON metadata document, instead of Dynamic Client Registration.
- Serve both protocol eras during the transition: route on `initialize` (legacy 2025-11-25) versus `meta.protocolVersion` / `server/discover` (modern 2026-07-28).
- Elicitations still work without server push: the server returns result type `input_required` with a JSON schema, and the client makes a second request with the answers.
- Distribute agent skills as Skills JARs (Maven dependencies served over MCP) and give every MCP App a text fallback for terminals and clients that cannot render HTML.
- Move long-running tool work to the Tasks extension (`tasks/call`, `tasks/get`, `tasks/update`, `tasks/cancel`) and stop using the deprecated roots, sampling, and logging features.

## Notes

### [01:21](https://youtu.be/fShgG3jtkXQ?t=81) What changed in MCP 2.0
The talk covers spec version 2026-07-28, released a couple of months before the talk. Official deprecations: roots, sampling, logging, Dynamic Client Registration (DCR), and the HTTP+SSE transport. Sampling was rarely implemented by clients, so its removal is presented as pruning dead weight. Ward works on agent experience at AWS and sits on the Agentic AI Foundation technical committee.

### [03:28](https://youtu.be/fShgG3jtkXQ?t=208) Stateless transport
The old Streamable HTTP flow required an `initialize` returning an MCP session ID, plus a separate SSE stream the server had to correlate with POST requests, which forced sticky load balancing on the session ID and made horizontal scaling hard. In the new transport every request carries metadata (protocol version, client info, client capabilities), so any instance can serve any request. Clients should also send MCP method and name headers so routers can route on them. Tool listing moves to a `server/discover` call that servers must support (clients may skip it), every response carries a result type (complete, input requested, or task), and list/read responses carry cache TTLs the client applies itself. Lost session state is replaced with explicit handles: REST-style resource IDs passed per call. Spring AI's server already offers a stateless mode that disables the push-based features (sync request context, sampling), and servers built in that mode should upgrade without changes.

### [09:49](https://youtu.be/fShgG3jtkXQ?t=589) Multi-round-trip requests and elicitations
Without server push, elicitations (a tool asking the user for more input mid-call, e.g. a missing preferred airline in a flight search) become a request/response round trip: the first response returns result type `input_required` with the JSON schema of what is needed, and the client sends a second request with the answers. Tool-author code should not change; the framework maps the elicitation API onto this flow. Ward showed the end-user code in his Scala zio-http-mcp library (`context.elicit(...)` with a map over the answer).

### [14:32](https://youtu.be/fShgG3jtkXQ?t=872) Legacy vs modern era negotiation
Servers must handle both the legacy era (2025-11-25) and the modern era (2026-07-28). Negotiation markers: a request to `initialize` means a legacy session; a `meta.protocolVersion` field means modern; client and server also exchange supported versions. In MCP Inspector against his zio-http-mcp server, auto-negotiation sent `server/discover` (modern-only) and connected as 2026-07-28, while forcing legacy showed the old `initialize` first and connected as 2025-11-25.

### [18:40](https://youtu.be/fShgG3jtkXQ?t=1120) Elicitation live demo
Calling a "book a flight to Denver" tool popped an elicitation dialog (confirm the booking); submitting it completed the tool call. The protocol view showed the first response as `input_required` with the request schema, then a second request carrying the filled-in input responses. The same tool code serves both eras unchanged.

### [20:46](https://youtu.be/fShgG3jtkXQ?t=1246) CIMD authentication
MCP auth recap: the MCP server is an OAuth 2.1 resource server that never issues tokens. An unauthenticated call gets a 401 pointing at the protected resource metadata; the client discovers authorization servers, registers, and retries with a bearer token. The new spec requires validating the issuer. DCR is deprecated because it hands every unknown client an opaque ID with no notion of client identity. With CIMD the client_id is a URL (e.g. on his test site cimd.now) that serves a JSON document repeating the client_id plus name, redirect URIs, and grant types; the authorization server fetches it instead of requiring a registration call, and identity becomes the portable HTTPS origin. Server-side the only change for spec compliance is validating the audience claim; the Spring client just sets its client_id to the CIMD URL.

### [27:10](https://youtu.be/fShgG3jtkXQ?t=1630) Secured Spring AI server demo
A Spring AI MCP server (issuer `login.james.dev`, audience validation on) exposed a `whoami` tool. Connecting from MCP Inspector redirected to the login page, returned with a token, and the tool call echoed the authenticated principal. One honest stumble: the first connection silently used DCR, and Ward had to flip on the Inspector's CIMD toggle and supply the CIMD URL before the CIMD path was exercised. Both DCR and CIMD work transparently in the Java SDK and Spring AI.

### [31:20](https://youtu.be/fShgG3jtkXQ?t=1880) Extensions become first-class
Extensions are now negotiated via `capabilities.extensions` on both sides, keyed by `{vendor-prefix}/{name}`, with official ones under `io.modelcontextprotocol/*` living in `ext-*` repos with their own SEPs and release cadence, so the core stays small. The table on screen: MCP Apps (`.../ui`), Tasks (`.../tasks`), Skills over MCP (`.../skills`), plus OAuth client credentials / enterprise-managed auth (`ext-auth`).

### [33:28](https://youtu.be/fShgG3jtkXQ?t=2008) MCP Apps
A tool can return a rendered HTML UI (built on MCP resources) inside agents with rich surfaces; the loaded app can call back into the server and pre-fill prompts. Setup is resources plus stock tools plus metadata, and every app needs a text fallback for clients that cannot render. Demo: asking Claude to list EC2 instances rendered a sortable 16-instance table, and a "launch" button auto-filled the follow-up prompt in the agent. Supported in claude.ai and ChatGPT web, not in terminal agents.

### [37:08](https://youtu.be/fShgG3jtkXQ?t=2228) Tasks
Tasks, now official, standardize long-running work behind `tasks/call`, `tasks/get`, `tasks/update`, and `tasks/cancel` tools once both sides advertise the extension. This segment stayed at the API-list level with no demo.

### [37:40](https://youtu.be/fShgG3jtkXQ?t=2260) Skills over MCP and Skills JARs
Agent skills suffer a distribution problem (installing, updating, sharing in enterprises); serving them over MCP (`skills/list`, `skills/get`, skills as resources) fixes that, though the agent must support the extension (Codex was named as an early supporter). Ward's skillsjars.com packages skills into JARs published on Maven Central, consumed as ordinary dependencies two ways: extracted to the filesystem for project builds (via sbt/Gradle/Maven extract plugins), or served straight off the classpath by an MCP server with the skills extension. Demo: an MCP server with one dependency skill (Anthropic brand guidelines) plus one local skill (flight booking) served both, loaded live in Inspector's Skills tab. Audience Q&A confirmed skill-bundled code/scripts ride along in the JAR and run after filesystem extraction (or straight off the classpath for self-built agents).

### [43:58](https://youtu.be/fShgG3jtkXQ?t=2638) Migration checklist and implementations
Checklist for server developers: run stateless with explicit handles; drop sampling/roots/logging (use tool params, direct LLM calls, OTel); validate OAuth audience with a CIMD-capable authorization server; move long work to Tasks; ship Skills; add Apps where UI helps; serve both 2025-11-25 and 2026-07-28 during transition. Implementation status: Spring AI 2.1.0-M1 (MCP Java SDK 2.0.0) with 2026-07-28 in progress, MCP Security 0.1.14 for CIMD, Tachyon MCP (Java, virtual threads, both eras), zio-http-mcp 0.8.3 (dual-era, MRTR, Tasks, Skills, Apps), cimd.now for localhost testing, and the spec at modelcontextprotocol.io. Demo code and slides were said to be on his GitHub, but no URL was spoken or shown.

## Tools, libraries and specs
- MCP specification 2026-07-28 (modern era) and 2025-11-25 (legacy era) — modelcontextprotocol.io
- MCP Inspector (era selection, elicitation and skills testing)
- Spring AI 2.1.0-M1 / MCP Java SDK 2.0.0 (stateless mode; 2026-07-28 support in progress)
- org.springaicommunity mcp-*-security 0.1.14 (CIMD client/server support)
- Tachyon MCP — tachyonmcp.dev (Java, virtual threads, both eras)
- zio-http-mcp 0.8.3 — com.jamesward (Scala; dual-era, MRTR, Tasks, Skills, Apps)
- cimd.now (CIMD test documents for localhost clients)
- skillsjars.com (skills packaged as Maven Central JARs, with sbt/Gradle/Maven extract plugins)
- Claude/Claude Code, ChatGPT web, Codex (extension support varies by client)

## Who should watch
MCP server developers, especially on the JVM or Spring, who need to plan the 2026-07-28 migration or adopt CIMD, Tasks, Skills, or Apps. Skip it if you only consume MCP tools as an end user, or if you want agent-framework or client-side guidance beyond Inspector-level testing.

## Verdict
**6/10**: The transport redesign, CIMD and extensions are explained from protocol internals with most segments demoed live, but the title-billed CIMD handshake never runs and the takeaways stay library pointers plus a spoken checklist.

**Novelty 1/2**

- **+** [40:19](https://youtu.be/fShgG3jtkXQ?t=2419) Skills JARs, the cimd.now test site and the zio-http-mcp demos carry the talk on the speaker's own projects and migration experience.
- **−** The core material (stateless transport, CIMD, extension IDs, deprecations) follows the public modelcontextprotocol.io/specification/2026-07-28 closely.

**Demonstrated 1/2**

- **+** [19:11](https://youtu.be/fShgG3jtkXQ?t=1151) The elicitation flow runs end to end in MCP Inspector with the input_required response and the follow-up request visible in the protocol view.
- **+** [35:35](https://youtu.be/fShgG3jtkXQ?t=2135) In Claude, the MCP App renders a sortable 16-row EC2 table and auto-fills a launch prompt.
- **−** [29:45](https://youtu.be/fShgG3jtkXQ?t=1785) The CIMD handshake never runs on screen: the toggle goes on, setup is deferred, and the whoami call uses the DCR-authenticated session.

**Measured 1/2**

- **·** [05:04](https://youtu.be/fShgG3jtkXQ?t=304) The talk makes no quantitative claim: statelessness is presented as a design property (any instance serves any request), so there is nothing for numbers to back.

**Depth 2/2**

- **+** [03:59](https://youtu.be/fShgG3jtkXQ?t=239) The stateless design is motivated from the old transport's internals: correlating POSTs with a separate SSE stream forced session-sticky load balancing.
- **+** [23:26](https://youtu.be/fShgG3jtkXQ?t=1406) CIMD is weighed against pre-registration and DCR (opaque per-client IDs with no identity) and reduced to a mechanism: client_id URL, fetched JSON document, audience validation.
- **−** [37:40](https://youtu.be/fShgG3jtkXQ?t=2260) The Tasks extension gets only its four tool names, with no lifecycle or trade-off discussion.

**Reusable 1/2**

- **+** [46:38](https://youtu.be/fShgG3jtkXQ?t=2798) The speaker names implementations that already support the new spec (Tachyon MCP, his zio-http-mcp) and cimd.now for localhost CIMD tests, which a reader can look up.
- **−** [47:09](https://youtu.be/fShgG3jtkXQ?t=2829) Demo code is only said to be "up on my GitHub", with no repository named in speech.
