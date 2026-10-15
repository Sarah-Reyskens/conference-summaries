---
title: Expanding Vector Search Beyond Similarity
talkId: "24227"
conference: devoxx-be-2026
speakers: [Alina Yurenko]
track: Agentic Engineering & Tooling
sessionType: Tools-in-Action
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=EnHPYkSAaCo
durationMin: 31
slides: null
verdict: 7
frames: 7
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Expanding Vector Search Beyond Similarity
Alina Yurenko · Tools-in-Action · Agentic Engineering & Tooling

## TL;DR
Yurenko builds a Swiss travel-advisor app that combines semantic vector search with hard business filters (location radius, price cap) instead of trusting the LLM to respect constraints. The thesis: use embeddings to capture meaning, keep factual constraints in queryable application code, and expose the combination to the model through well-defined tools. Everything is demonstrated live: code, running app, database verification, and LLM observability traces.

## Key takeaways
- Treat user constraints like price and location as application-side filters, not prompt instructions: an LLM may reinterpret "near Lucerne" or drop a budget cap, while a 15 km radius default and a price filter are deterministic.
- Embed only stable attributes (hotel name, destination, description); keep volatile data such as prices, offers, and events in structured columns that you filter with SQL.
- Expose the database to the LLM only through tools (LangChain4j `@Tool` methods calling Micronaut repositories), which keeps sensitive columns invisible and the allowed actions deterministic.
- Instrument every tool call from day one: the speaker used Arize Phoenix traces plus LangChain4j listeners after hitting hard-to-debug hallucinated tool calls during development.
- A GraalVM native image runs this kind of assistant app in under 200 MB max RSS, making always-on small services cheap to deploy.

## Notes

### [00:34](https://youtu.be/EnHPYkSAaCo?t=34) No slides, just the app
Yurenko opens by saying she brought no slides at all and will show the application directly. The app is a travel-agency assistant: users ask for hotels, destinations, and activities, and the app grounds semantic search in the agency's own catalog plus business constraints. The stack is Micronaut, LangChain4j, Oracle Database (structured storage plus vector search), OpenAI for embeddings and chat, all compiled to a GraalVM native image. She disclaims this is not a GraalVM talk: the native image is just how the app ships.

### [05:50](https://youtu.be/EnHPYkSAaCo?t=350) Breaking a query into meaning plus constraints
For a query like "recommend a quiet lakeside hotel near Lucerne under 250 francs per night", she splits it into three parts. "Quiet lakeside" is semantic: the catalog may say "peaceful", "waterfront", or "Lake Leman", so vector similarity finds the match. "Near Lucerne" becomes a spatial radius search (default 15 km when the user gives no distance), implemented in business logic rather than trusted to the LLM. The price is a hard filter, since users expect budgets to be respected exactly.

### [08:26](https://youtu.be/EnHPYkSAaCo?t=506) The assistant interface and its tools
The heart of the app is a `SwissTravelAssistant` interface annotated with `@RegisterAiService`, for which Micronaut generates the implementation. It carries a long system message instructing the model to use tools and never answer from memory, plus the tool surface: `searchHotels`, `searchNearbyHotels`, `searchActivities`, `searchNearbyActivities`, `searchDestinations`, `addToWishlist`. She stresses that tools are also a security boundary: the model never sees customer IDs, balances, or credentials, only what the tools return.

### [10:29](https://youtu.be/EnHPYkSAaCo?t=629) What goes into the embedding
On startup the app generates embeddings for new catalog entries, each combining hotel name, destination name, and hotel description. The design rule: embed values that are stable over time (a hotel's spa, kids area, nightlife do not change often) and filter volatile values (price, offers, events) in the application layer. The tool then ranks by cosine similarity against the user's semantic fragment while also applying radius and price filters.

### [14:38](https://youtu.be/EnHPYkSAaCo?t=878) Live demo: native image startup and hotel search
She starts the native image under `/usr/bin/time -v` on Linux: startup is fast and the whole process stays under 200 MB max RSS (Phoenix and the cloud database run separately). In the "Swiss Travel Advisor" UI she asks for a luxury hotel in Lucerne under 500 CHF per night, then lowers the price and drops "luxury" to get different results, asks for fun things to do in Lucerne (a mountain round trip), and saves a hotel plus an activity to the wishlist. She notes an earlier rehearsal typo ("under 50 francs") correctly returned zero documents, which briefly scared her before she realized the constraint was doing its job.

### [19:53](https://youtu.be/EnHPYkSAaCo?t=1193) Verifying results against the database
Back in a database client, she shows the destinations table (Lucerne is destination ID 3) and the hotels table, confirming the recommended hotels map to Lucerne, then re-runs a query with the adjusted price to show the same candidates the app surfaced. The app re-ranks those rows by semantic distance; the database only guarantees they satisfy the hard constraints.

### [22:01](https://youtu.be/EnHPYkSAaCo?t=1321) Tracing the call in Arize Phoenix
In Phoenix she drills from sessions into a per-request trace: `chat gpt-5.6-terra` calls `searchNearbyHotels`, the query fragment "luxury" is embedded, and an "Oracle hotel vector + spatial search" span returns documents with cosine distance scores (e.g. 0.33 for Lake Lucerne Wellness Retreat). The document metadata shows destination ID and price, proving both constraints were applied. She also demonstrates annotation rules that score whether the right tool was selected (e.g. "find/recommend/suggest" should trigger a search tool) as a lightweight eval layer.

### [26:44](https://youtu.be/EnHPYkSAaCo?t=1604) LangChain4j logging listeners
A second observability layer lives in the app itself: LangChain4j listeners log every tool call, successful tool result, user/assistant exchange, and per-operation token usage. She added this 7–8 months into development because the LLM would occasionally hallucinate tool calls or results and the failure point was otherwise invisible. The logs make it possible to see exactly where a run derailed.

### [29:20](https://youtu.be/EnHPYkSAaCo?t=1760) Takeaways and repo
The closing takeaways, shown in a markdown file: capture meaning with embeddings but keep facts queryable; combine semantic relevance with hard constraints; give the model controlled tool access; trace and evaluate model behavior; use native image for fast startup and low memory. The app is on GitHub with build instructions and a linked blog post; a second edition with new features is planned.

## Tools, libraries and specs
- Micronaut (`@RegisterAiService`, generated repositories)
- LangChain4j (`@Tool`, `@SystemMessage`, logging/tracing listeners)
- GraalVM Native Image (`./mvnw package -Dpackaging=native-image`)
- Oracle Database (vector + spatial search, cosine distance)
- OpenAI (embeddings and chat; `gpt-5.6-terra` in the demo traces)
- Arize Phoenix (open-source LLM observability: traces, sessions, annotation rules)

## Who should watch
Java developers building RAG-style or assistant apps who want a concrete pattern for grounding search in business rules, and anyone evaluating LangChain4j with Micronaut. Skip if you already ship tool-based agents with evals, or if you want GraalVM internals: the native image is used but never explained.

## Verdict
**7/10**: Live searches verified in the database and in Phoenix traces back the constraints-plus-tools pattern, but the embeddings stay a black box and the memory figure has no baseline.

**Novelty 1/2**

- **+** [07:55](https://youtu.be/EnHPYkSAaCo?t=475) The 15 km default radius for "near" queries is her own fallback from building the app, used when users give no distance.
- **+** [11:31](https://youtu.be/EnHPYkSAaCo?t=691) The rule to embed stable attributes like a spa or kids area while filtering volatile prices and offers in SQL comes from her own design work.
- **−** The stack walkthrough (`@RegisterAiService`, `@Tool` methods, Oracle vector and spatial SQL) repeats what the Micronaut LangChain4j getting-started guide and the Oracle AI Vector Search documentation already carry.

**Demonstrated 2/2**

- **+** [18:16](https://youtu.be/EnHPYkSAaCo?t=1096) A luxury-hotel search runs live in the UI, then re-runs with a lower price and "luxury" dropped to show different results.
- **+** [23:34](https://youtu.be/EnHPYkSAaCo?t=1414) The Phoenix trace shows the luxury request reduced to the "luxury" fragment and matched against catalog rows whose metadata carries destination ID and price.
- **−** [07:55](https://youtu.be/EnHPYkSAaCo?t=475) The 15 km default is never exercised: the only radius on screen is `radiusKm: 40` in a logged activity search.

**Measured 1/2**

- **+** [28:16](https://youtu.be/EnHPYkSAaCo?t=1696) `/usr/bin/time -v` reports the native-image app process under 200 MB max RSS, with Phoenix and the database running separately.
- **−** [28:50](https://youtu.be/EnHPYkSAaCo?t=1730) The figure comes from a single interactive run with no baseline or comparison, since she sent no bulk load against the app.
- **−** [16:12](https://youtu.be/EnHPYkSAaCo?t=972) Startup is called "quite fast" with no figure; the only time reported is the whole-session elapsed time.

**Depth 1/2**

- **+** [09:58](https://youtu.be/EnHPYkSAaCo?t=598) Tools are presented as a security boundary: the assistant never sees customer IDs, balances or addresses, only what the tools return.
- **+** [12:33](https://youtu.be/EnHPYkSAaCo?t=753) The hotel tool ranks catalog rows by similarity against the semantic fragment while enforcing the radius and price filters.
- **−** [05:19](https://youtu.be/EnHPYkSAaCo?t=319) The vector comparison is "offloaded to the database" with no index type or tuning discussed.

**Reusable 2/2**

- **+** [30:24](https://youtu.be/EnHPYkSAaCo?t=1824) The demo app sits on GitHub with build and run instructions and a linked blog post covering the same build.
