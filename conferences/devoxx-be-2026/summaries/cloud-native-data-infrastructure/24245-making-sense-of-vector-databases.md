---
title: Making sense of vector databases
talkId: "24245"
conference: devoxx-be-2026
speakers: [Balkrishna Rawool]
track: "Cloud Native, Data & Infrastructure"
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=knE4uy7IYXY
durationMin: 48
slides: https://speakerdeck.com/balkrishnarawool/making-sense-of-vector-databases
slidesNote: from an earlier Dec 2024 delivery
verdict: 7
frames: 8
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Making sense of vector databases

Balkrishna Rawool · Conference · Cloud Native, Data & Infrastructure

Slides: https://speakerdeck.com/balkrishnarawool/making-sense-of-vector-databases

## TL;DR

Rawool builds the ideas behind vector databases from first principles: vectors and embeddings, similarity metrics, embedding models, indexing, and RAG, with every concept backed by a live Java demo that grows in complexity. The arc runs from one-dimensional gray-color vectors to an image search engine and a live audience-member celebrity lookalike, closing the loop on the opening question of how Google Lens finds similar pictures. Viewers leave with a working mental model of similarity search plus a repository containing each demo.

## Key takeaways

- A good embedding places items with similar meaning close together in vector space, and "closeness" is whatever similarity or distance function you choose.
- Cosine similarity measures the angle between vectors, so normalizing first separates direction (meaning) from magnitude.
- Word vectors preserve relations as well as meanings: king − man + woman lands near queen because the arithmetic survives embedding.
- HNSW answers nearest-neighbor queries by descending a layered graph from coarse to fine granularity, reusing each layer's best hit as the next layer's entry point.
- PostgreSQL becomes a vector database with the pgvector extension: store embeddings in a column, add an HNSW index, and run similarity search through SQL.
- RAG grounds an LLM by retrieving relevant passages first: without it the model invented a return policy, with it the model quoted the FAQ's 15-day, unopened, in-person terms.
- Image search is similarity search on image embeddings: upload a Taj Mahal photo and Taj Mahal photos come back.

## Notes

### [00:33](https://youtu.be/knE4uy7IYXY?t=33) The goal: rebuild Google Lens from scratch

Google Lens takes an uploaded picture and returns similar pictures; over 70% of the room had used it. The talk promises one route to the same feature: build understanding piece by piece, from vectors to a working image search.

### [02:38](https://youtu.be/knE4uy7IYXY?t=158) Vectors, embeddings, and what vector databases store

A vector is an array of numbers, equivalent to the magnitude-and-direction view. Embedding models turn data into vectors, placing similar meanings near each other; similarity or distance measures that togetherness. Vector databases store vectors and support insert, update, delete, indexing, and search.

### [06:14](https://youtu.be/knE4uy7IYXY?t=374) A tiny VectorDB on the Java Vector API

The Vector API's single-instruction-multiple-data operations suit embedding arithmetic. The in-memory store wraps a `double[]` in a record, implements vector operations through the API, and keeps entries in a HashMap. Its key method is k-nearest-neighbors under a supplied similarity or distance calculator.

### [11:59](https://youtu.be/knE4uy7IYXY?t=719) Example 1: one-dimensional gray colors

Ten gray shades map to the numbers 0–9, a valid embedding because neighbors stay neighbors. Clicking a shade returns it plus the shades above and below by Euclidean distance; white and black return just their two available neighbors.

### [15:04](https://youtu.be/knE4uy7IYXY?t=904) Similarity and distance, with the math

Four measures: Manhattan sums per-axis gaps, dot product multiplies and adds components, Euclidean is the straight-line gap, cosine is the angle's cosine, computed as dot product over magnitudes. Magnitude and normalization get their own derivations first.

### [17:39](https://youtu.be/knE4uy7IYXY?t=1059) Example 2: RGB colors and cosine similarity

Colors from RGB(1,1,1) to RGB(255,255,255) become normalized 3-D vectors. Seven neighbors by cosine similarity return visually adjacent shades, the color itself first at similarity 1; the score column shows the 1-to-−1 range directly.

### [21:52](https://youtu.be/knE4uy7IYXY?t=1312) Embedding models and Example 3: word2vec

Text (word2vec, GloVe, BERT), image (CNN, img2vec), and multimodal (GPT, CLIP) models all convert input into meaning-carrying vectors. Four Wikipedia pages vectorized with 300-dimensional Google News word2vec yield a few thousand stored words. Querying "king" returns kings, queen, monarch; king − man + woman ranks queen second.

### [28:09](https://youtu.be/knE4uy7IYXY?t=1689) Indexing: from k-d trees to HNSW

Tree-based (k-d tree, R-tree, Annoy), hash-based locality-sensitive hashing that deliberately collides similar inputs, graph-based HNSW, and hybrid ScaNN. HNSW layers a vector graph by granularity: each layer's nearest hit becomes the next layer's entry point down to maximum granularity.

### [31:19](https://youtu.be/knE4uy7IYXY?t=1879) Example 4: semantic search over math articles with pgvector

Ten math Wikipedia pages become embedded sentences in a Postgres table with an HNSW index on the embedding column. Queries like "what is algebra" or "tell me about Newton" each return five related sentences. Full-sentence queries pay off once an LLM consumes the results.

### [35:58](https://youtu.be/knE4uy7IYXY?t=2158) RAG and Example 5: the Epic Comic Co. assistant

A chat service fronts the open-weight gpt-oss model with a `useRag` flag; the knowledge base is a FAQ for a fictitious Amsterdam comic-book store in Elasticsearch. With RAG off, the return-policy question gets hallucinated fiction; with RAG on, the reply matches the FAQ: 15 days, unopened items only, in person.

### [41:10](https://youtu.be/knE4uy7IYXY?t=2470) Examples 6 and 7: image search and the live celebrity lookalike

World-wonder photos vectorized with img2vec into a Weaviate class answer near-image queries with six hits: Taj Mahal in, Taj Mahal out; same for pyramids. The finale photographs a volunteer, crops to the face, and matches it against ~300 celebrity pictures; the speaker's own photo returns George Clooney.

## Tools, libraries and specs
- Java Vector API (incubator): SIMD vector operations behind the tiny VectorDB
- jlama: single-file Java LLM inference engine, cited as a Vector API showcase
- Spring Boot: back ends for the demo applications
- Deeplearning4j: word2vec implementation loading the Google News vectors
- Google News word2vec model: 300-dimensional word embeddings
- PostgreSQL with pgvector: sentence store with an HNSW index on the embedding column
- nomic-embed-text: sentence embeddings for the wiki and RAG examples
- Elasticsearch: FAQ vector store for the RAG example
- gpt-oss: open-weight LLM answering with retrieved context
- Weaviate with img2vec module: image store queried through near-image GraphQL search

## Who should watch

Java developers who want the foundations of vector search before adopting a managed service, and anyone deciding where embeddings, indexes, and RAG fit in their stack. Skip it if you already operate vector search in production: there are no benchmarks, recall-versus-latency trade-offs, or scaling numbers. Python-first ML engineers get the concepts, but every line of code is Java.

## Verdict

**7/10**: Seven live demos carry the arc from vectors to image search and the repository publishes them, but the talk has no performance numbers, no guidance on choosing metrics or indexes, and its finale match missed.

**Novelty 1/2**

- **+** [06:14](https://youtu.be/knE4uy7IYXY?t=374) The in-memory VectorDB built on the Vector API's SIMD operations anchors standard concepts in the speaker's own code.
- **+** [41:10](https://youtu.be/knE4uy7IYXY?t=2470) The progression from 1-D color vectors to a working img2vec image search is the speaker's own curriculum rather than one source retold.

**Demonstrated 2/2**

- **+** [42:43](https://youtu.be/knE4uy7IYXY?t=2563) Searching with a Taj Mahal photo returns Taj Mahal photos from Weaviate, and a pyramid photo returns pyramids, live on screen.
- **+** [40:40](https://youtu.be/knE4uy7IYXY?t=2440) With `useRag` on, the model quotes the FAQ's 15 days, unopened items, in person, after the same question produced an invented return policy with it off.
- **−** [46:23](https://youtu.be/knE4uy7IYXY?t=2783) The live celebrity lookalike returns a volunteer match the speaker calls "not the best", and his own result, George Clooney, is one he disowns.

**Measured 1/2**

- **·** [09:52](https://youtu.be/knE4uy7IYXY?t=592) The talk makes no quantitative claim of its own: the Vector API speedup is stated without a number, and figures like 300 dimensions or k = 7 are configuration, not results.

**Depth 1/2**

- **+** [15:04](https://youtu.be/knE4uy7IYXY?t=904) The four similarity measures are written out as formulas on 3-D vectors, with magnitude and normalization built up before cosine similarity.
- **+** [30:16](https://youtu.be/knE4uy7IYXY?t=1816) HNSW is motivated by the small-world property (if A is friends with B and C, B and C are probably friends) and searched by descending layers from a fixed entry point.
- **−** [28:09](https://youtu.be/knE4uy7IYXY?t=1689) The four metrics and six index algorithms get a line each and no when-to-use-which comparison; only HNSW is explained beyond its definition.

**Reusable 2/2**

- **+** [46:55](https://youtu.be/knE4uy7IYXY?t=2815) The closing slide points to github.com/balkrishnarawool/vectordb-talk, which holds the VectorDB, all seven example apps, docker-compose files, the DDL and setup steps.
- **−** [46:55](https://youtu.be/knE4uy7IYXY?t=2815) The README leaves the large image data out of the repository and asks readers to contact the speaker for it, so the image demos cannot be rerun from a clone.
