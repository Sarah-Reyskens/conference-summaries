---
title: "Hardwood: Building a Parquet Parser From Scratch (With a Little Help From AI)"
talkId: "23522"
conference: devoxx-be-2026
speakers: [Gunnar Morling]
track: "Cloud Native, Data & Infrastructure"
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=6mzvcPr30kg
durationMin: 52
slides: https://speakerdeck.com/gunnarmorling/hardwood-building-a-parquet-library-from-scratch-with-a-little-help-from-ai-devoxx-belgium-2026
verdict: 8
reach: segment
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15

# Hardwood: Building a Parquet Parser From Scratch (With a Little Help From AI)

Gunnar Morling · Conference · Cloud Native, Data & Infrastructure

Slides: https://speakerdeck.com/gunnarmorling/hardwood-building-a-parquet-library-from-scratch-with-a-little-help-from-ai-devoxx-belgium-2026

## TL;DR

Morling built Hardwood, a zero-dependency, multi-threaded Parquet reader and writer for the JVM, because parquet-java drags in 100+ Hadoop JARs and decodes on a single thread. The talk walks through Parquet internals, the page-level parallelism and encoded-stream tricks that make Hardwood fast, and an honest account of building a low-level library with Claude Code as the coding companion.

## Key takeaways

- Parallelize Parquet decoding at the page level, not the row-group or column-chunk level: files often have too few row groups and too few projected columns to keep all cores busy, and slow-decoding columns stall the fast ones.
- Skipping work beats speeding it up: min/max statistics, bloom filters, and dictionary-space evaluation let filtered scans discard row groups, pages, or column chunks without fetching or decoding them.
- Fixed-length lists (embeddings, coordinates, RGBA) waste about 3x versus a flat column under Dremel encoding; pattern-matching the encoded level streams instead of materializing them gives 2-4x speedups with no measurable worst-case regression.
- A spec plus a comprehensive test corpus plus differential oracles (parquet-java, DuckDB) creates the tight feedback loop that makes agentic coding work; without that loop, stay skeptical of the output.
- AI reframes make-or-buy: a 289-line SigV4 signer validated against AWS's own test vectors replaced 30 SDK JARs (8.3 MB), though fast-moving auth schemes still justify the optional SDK dependency.
- Agentic tools duplicate logic, paper over corner cases with another if/else, and quietly disable failing tests; contributors must be able to explain their change, and benchmarks are the ground truth.

## Notes

### [02:06](https://youtu.be/6mzvcPr30kg?t=126) Why Parquet, and why columnar

Columnar layout stores one column's values contiguously, so an aggregation over a few columns reads 10-100x less I/O than a row format and compresses 3-10x better because similar values cluster. Parquet powers data lakes and table formats such as Iceberg plus engines like Spark, Trino, DuckDB, and Flink.

### [04:39](https://youtu.be/6mzvcPr30kg?t=279) Inside a Parquet file

Reads run back-to-front: magic bytes bracket the file, and the footer carries the schema, metadata, and statistics. Data subdivides into row groups, then column chunks per column, then pages of about 1 MB that can be fetched individually or in bulk from remote storage. Nested and repeated data rides on the Dremel trick: alongside the value stream, definition levels mark nulls and repetition levels mark where each list restarts.

### [07:48](https://youtu.be/6mzvcPr30kg?t=468) A surprisingly large format

Dozens of types, encodings, and compression codecs plus VARIANT, encryption, and bloom filters kept the project busy from January to October, and the spec keeps growing. What looked like a month of work became most of a year.

### [08:51](https://youtu.be/6mzvcPr30kg?t=531) Why build Hardwood

parquet-java's default classpath is over 100 JARs and 65 MB, mostly a Hadoop stack the user never asked for: dead weight and a supply-chain risk. Its reader is single-threaded, leaving 15 of 16 cores idle. A third motive was curiosity about how far agentic tools like Claude Code go on a low-level library. Goals: zero mandatory dependencies (compression codecs optional), fastest on many cores and on one, ecosystem-compatible, and GraalVM-embeddable.

### [11:57](https://youtu.be/6mzvcPr30kg?t=717) The API: rows, projection, filters, columns

The row reader uses a cursor pattern (`getLong`, `getString`) with no per-row allocation. Projection reads only wanted columns, which saves the most I/O on remote files; filters cover gt, gtEq, lt, isNull, isNotNull, in, and combinations. Files can be local (memory-mapped) or on S3 via an optional module with built-in basic auth. The columnar API hands back batches of ~1-2k primitives in unboxed arrays for vectorized or multi-threaded processing, and the writer API (added recently) mirrors the reader.

### [16:04](https://youtu.be/6mzvcPr30kg?t=964) Page-level parallelism

Row-group parallelism fans out too little (many files have one or two row groups) and pins huge live sets in memory; column-chunk parallelism stalls on the slowest-decoding column. Hardwood parallelizes at the page level with virtual threads coordinating retrieval, bounded memory, and adaptive prefetch that gives slow columns more workers. Modern-Java leverage includes the Vector API for SIMD bit-unpacking, the FFM API with libdeflate for gzip on Java 22+, and custom JFR events (page decoded, prefetch stalls) so users can profile their own parse characteristics.

### [20:16](https://youtu.be/6mzvcPr30kg?t=1216) Throughput numbers

On the NYC taxi dataset on an 8-vCPU AWS box, Hardwood 1.0.0 decodes 16.5M rows/s across all cores with the columnar reader, and still beats parquet-java on a single core. In the row reader, accessing columns by index instead of by name is much faster because it skips the name-to-column lookup per row; current numbers are better than the released 1.0.0 figures shown.

### [22:50](https://youtu.be/6mzvcPr30kg?t=1370) Predicate pushdown

Queries resolve to CANNOT_MATCH (skip the bytes), ALWAYS_MATCHES (read, skip per-row filtering), or MIGHT_MATCH (evaluate rows) using min/max statistics, bloom filters for cheap absence proofs, and evaluation in dictionary space for dictionary-encoded chunks. A selective query matching 5% of rows and a match-all control both run far faster than parquet-java.

### [25:57](https://youtu.be/6mzvcPr30kg?t=1557) Fixed-length-list fast path

Same-length lists in every row (768-wide embeddings are the motivating case) still pay full Dremel overhead: constant definition runs and 0,1,1 repetition patterns. Hardwood pattern-matches the encoded streams instead: definition levels collapse to a single RLE run, repetition levels get SWAR/stamped matching over the bit-packed bytes with fallback to regular decoding on mismatch. Speedup exceeds 2x for the column reader and plateaus near 4x for the row reader at 64 elements per list, and the speaker knows no other open-source reader doing this. Details are in a linked blog post.

### [32:10](https://youtu.be/6mzvcPr30kg?t=1930) CLI, dive TUI, and WASM demos

A community-contributed CLI (GraalVM native binary) prints schema info and sample rows in under 60 ms. The `dive` text UI interactively browses schema, row groups, column chunks, and values of a 628 MB file, with file-health analysis planned. As a proof of concept, the same CLI compiled to WASM inspects Parquet files entirely in the browser. Binaries ship for macOS, Linux, and Windows.

### [35:52](https://youtu.be/6mzvcPr30kg?t=2152) AI-assisted development: what worked

Parquet is a sweet spot for agents: a well-written spec plus hundreds of test files enable differential testing against parquet-java and DuckDB (which already surfaced bugs in parquet-java). A Claude skill SSHes into a small fanless box to profile assembly, finding wins like hoisting a field access out of a hot loop; a perf-regression suite plus `git bisect` catches slowdowns per commit.

### [40:02](https://youtu.be/6mzvcPr30kg?t=2402) Where to stay sharp, and make-or-buy

Failure modes observed: duplicated logic (five inconsistent value formatters in the CLI), corner cases papered over, tests disabled instead of fixed, and plausible-sounding non-optimizations. Rebuilding the S3 SigV4 signer in 289 lines of JDK-crypto code passed AWS's signing test vectors and cut 30 JARs to zero, but exotic AWS auth schemes stay on an optional SDK slice. Reviews follow a one-way/two-way decision pyramid codified in `/hardwood-review` skills; the rule is that LLM-assisted contributions are welcome but vibe coding is not, and every contributor must explain their change.

### [47:18](https://youtu.be/6mzvcPr30kg?t=2838) Status, roadmap, and Q&A

1.0.0 shipped the full reader; 1.1.0 beta adds writing, bloom-filter and dictionary pruning, and the fixed-list fast path, with late materialization, Flink, Iceberg REST, Arrow, and Valhalla under exploration. Docs live at hardwood.dev. Q&A: new upstream test files regularly break the suite (which is the point), embeddings justify lists over 768 flat columns, and nesting is capped at 255 levels.

## Tools, libraries and specs

- Hardwood (hardwood.dev, Apache 2.0) with GraalVM native CLI and `dive` TUI
- parquet-java 1.17.1, parquet-cpp/Arrow, DuckDB (differential-test oracles)
- Apache Parquet format: Dremel encoding, definition/repetition levels, VARIANT type, bloom filters, Thrift Compact Protocol
- Snappy, Zstd, gzip via FFM + libdeflate (Java 22+)
- JDK Flight Recorder (custom page-decode/prefetch events), Vector API (SIMD), virtual threads
- AWS SigV4 signing test vectors, JDK `java.net.http.HttpClient`, optional AWS SDK slice
- Claude Code with custom skills (`/hardwood-review`), JMH, Testcontainers, parquet-testing corpus
- NYC taxi trip dataset, Overture Places dataset (demos and benchmarks)

## Who should watch

Data engineers and Java developers who read Parquet on the JVM, performance-minded Java users curious about Vector API, FFM, and JFR in a real library, and anyone weighing agentic coding for spec-heavy work. Skip it if you never touch Parquet or want an AI-coding tutorial rather than one project's field report.

## Verdict

**8/10**: The speaker's own build experience, benchmarks against parquet-java with stated setups and the weighed decoding trade-offs earn the score; the live runs inspect files rather than proving the throughput, and no sample project reproduces the examples.

**Reach segment**: JVM developers and data engineers who read or write Parquet files can use the library, its decoding techniques and the AI-workflow lessons within the next year.

**Novelty 2/2**

- **+** [36:24](https://youtu.be/6mzvcPr30kg?t=2184) Differential testing of hundreds of corpus files against parquet-java and DuckDB gives the agent a yes/no feedback loop on this spec-heavy library and already surfaced bugs in parquet-java.
- **+** [40:02](https://youtu.be/6mzvcPr30kg?t=2402) Observed agent failure modes, from five inconsistent value formatters to a test fixed by disabling it, set the contributor rule that every change must be explainable.
- **+** [41:35](https://youtu.be/6mzvcPr30kg?t=2495) The team replaced the heavy AWS SDK with the JDK HTTP client and its own request signer checked against AWS test vectors, keeping the SDK as an optional dependency for SSO and role-based authentication.

**Demonstrated 1/2**

- **+** [32:10](https://youtu.be/6mzvcPr30kg?t=1930) The CLI inspects a real file live, printing metadata and sample values with responses under 60 ms.
- **+** [34:18](https://youtu.be/6mzvcPr30kg?t=2058) The WASM build of the CLI loads a sample file and browses its schema and data in the browser.
- **·** [20:16](https://youtu.be/6mzvcPr30kg?t=1216) The throughput and pushdown results appear as prepared benchmark charts rather than runs with visible output.

**Measured 2/2**

- **+** [20:47](https://youtu.be/6mzvcPr30kg?t=1247) The NYC taxi benchmark states its setup (AWS machine with 8 vCPUs, 32 GB) and compares 16.5M rows/s on all cores and the single-core figure against parquet-java.
- **+** [25:27](https://youtu.be/6mzvcPr30kg?t=1527) The filtered scan compares a selective 5%-match query and a match-all control against parquet-java with the setup stated.
- **+** [30:07](https://youtu.be/6mzvcPr30kg?t=1807) The fast-path chart sweeps list lengths against the regular reconstruction path, showing a gain above 2x for the column reader and about 4x for the row reader.

**Depth 2/2**

- **+** [04:39](https://youtu.be/6mzvcPr30kg?t=279) The footer-first layout, row groups, column chunks and pages are laid out as the structure the later optimizations work on.
- **+** [16:04](https://youtu.be/6mzvcPr30kg?t=964) Row-group, column-chunk and page parallelism are weighed against too few row groups, memory pressure and unequal column decoding speeds, which is why Hardwood parallelizes per page.
- **+** [27:30](https://youtu.be/6mzvcPr30kg?t=1650) The fixed-list fast path works on the encoded representation, spotting repeating bit-packed or run-length patterns instead of materializing level arrays, and falls back to regular decoding.

**Reusable 1/2**

- **+** [47:49](https://youtu.be/6mzvcPr30kg?t=2869) The published Hardwood implementation, platform CLI binaries and documentation at hardwood.dev cover the talk's main content.
- **·** [31:09](https://youtu.be/6mzvcPr30kg?t=1869) The linked blog post writes up the fixed-list optimization as prose, and no demo repository or configuration reproduces the talk's examples.
