---
title: "SIMD for Java: how Elasticsearch already benefits from the Panama Vector API"
talkId: "17556"
conference: devoxx-be-2026
speakers: [Piotr Przybyl]
track: "Cloud Native, Data & Infrastructure"
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=adFS-_sCTQ4
durationMin: 52
slides: https://przybyl.org/pres/SIMD4Java/DevoxxBE.html
verdict: 8
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# SIMD for Java: how Elasticsearch already benefits from the Panama Vector API

Piotr Przybyl · Conference · Cloud Native, Data & Infrastructure

Slides: https://przybyl.org/pres/SIMD4Java/DevoxxBE.html

## TL;DR

Dot product over hundreds of embedding dimensions is the hottest loop in vector search, and Lucene plus Elasticsearch run it through SIMD: first via the incubating Panama Vector API with runtime CPU detection and scalar fallback, then, where that was not enough, through hand-tuned native `simdvec` kernels called over Panama FFI. The talk pairs the mechanism (species, lanes, instruction-level parallelism, bit-plane scoring for quantized vectors) with the speaker's own measurements on Intel and Apple Silicon, and a warning that the fastest instruction sequence is platform dependent.

## Key takeaways

- Compare SIMD against an unrolled scalar baseline with instruction-level parallelism, not a naive loop, or the speedup number is fiction.
- Let the runtime pick the vector width (`FloatVector.SPECIES_PREFERRED`) and always ship a scalar fallback; Lucene enables the Vector API path only on HotSpot plus C2 with the vector module present and registers of at least 128 bits.
- FMA is not universally faster than separate multiply plus add: on an Apple M3 Pro the split sequence was about 45% faster, on an Intel i9 both tied, so Lucene carries a platform heuristic that avoids FMA on Apple Silicon.
- Quantize before optimizing arithmetic: Better Binary Quantization stores 1 bit per dimension for documents with 4-bit queries, cutting a 768-dimension vector from 3072 bytes to 96 bytes while keeping recall above 90%.
- Reorganize quantized data into bit planes so scoring becomes AND plus bit-count plus shift with zero multiplications, which maps directly onto vector instructions (POPCNT on x86, CNT on ARM).
- When the Vector API still leaves performance on the table, Elasticsearch bypasses the JIT with per-ISA C++ kernels behind one symbol (`vec_dotf32`), selected at startup; the FFI call penalty is small enough that the win survives.

## Notes

### [00:33](https://youtu.be/adFS-_sCTQ4?t=33) Two meanings of "vector"

The talk is about CPU SIMD registers and about embedding dimensions in vector search, not `java.util.Vector`. Elasticsearch today is a vector store with multiple quantization tiers (scalar quantization, BBQ, HNSW graph search wired to SIMD) and has been open source since August 2024.

### [04:45](https://youtu.be/adFS-_sCTQ4?t=285) Dot product is the hot loop

A crash course: dot product sums per-dimension products, higher means more similar. Production embeddings run 384 to 3072 dimensions, and a query over a million documents means millions of dot products. HNSW avoids brute force at scale, but scoring candidates still dominates. The naive loop is readable, correct, and the bottleneck.

### [09:26](https://youtu.be/adFS-_sCTQ4?t=566) SIMD in one sentence

One instruction, many lanes: the same operation applied to multiple primitives at once. A 512-bit register holds 64 byte lanes, 16 float lanes, or 8 long lanes. Lanes are not threads; they cannot take different branches. Apple Silicon NEON registers are 128 bits, x86 AVX2/AVX-512 are 256/512.

### [13:39](https://youtu.be/adFS-_sCTQ4?t=819) Live demo: scalar versus Vector API

The speaker runs a dot product demo live: naive scalar against a Vector API version with four accumulators for instruction-level parallelism. The first runs show 6x to 10x speedups, then he flags the comparison as apples to oranges (only the vector side uses ILP) and re-runs against an unrolled scalar version, which roughly halves the speedup. Deck table: 13x on an Apple M3 Pro (128-bit NEON), 16x on an Intel i9-9980HK (256-bit AVX2), where C2 had auto-vectorized the scalar loop anyway.

### [17:19](https://youtu.be/adFS-_sCTQ4?t=1039) How Lucene implements it

Lucene's scalar dot product unrolls 4x with `fma` accumulators so the CPU overlaps the FMA latency chain with data fetches. The Vector API version (`PanamaVectorUtilSupport`) does the same with four `FloatVector` chains, a vector tail loop for sizes that are not exact register multiples, and a lane reduction. Vocabulary: species (type plus shape), shape (128/256/512), lane (one primitive). Activation is guarded at runtime: HotSpot plus C2, vector module present, width of at least 128 bits, Panama provider available; any failure falls back to scalar with no user impact. He shows the "Java vector incubator API enabled; preferredBitSize=128" line in local Elasticsearch logs.

### [23:31](https://youtu.be/adFS-_sCTQ4?t=1411) When SIMD is the wrong tool

Bad fits: pointer chasing, data-dependent branches, short loops dominated by setup, and serial-carry algorithms such as the hash mixing Elasticsearch uses for auto-generated document IDs. SIMD also composes with threads rather than multiplying their speedup, since both compete for cache, bandwidth, and frequency budget.

### [29:10](https://youtu.be/adFS-_sCTQ4?t=1750) Quantization and Better Binary Quantization

A 768-dimension float32 vector costs 3072 bytes per document; int8 takes 768, int4 takes 384, and 1 bit takes 96. At a million embeddings that is 3 GB versus 96 MB, and memory bandwidth is usually the real bottleneck. Search runs in two phases: fast approximate retrieval over quantized vectors, then accurate re-scoring of the shortlist. BBQ thresholds each dimension at the data centroid (not zero) to preserve signal, stores documents at 1 bit per dimension, and keeps queries at 4 bits (asymmetric encoding, two values packed per byte).

### [34:52](https://youtu.be/adFS-_sCTQ4?t=2092) Bit planes remove multiplication

The worked example transposes the int4 query into four bit planes, ANDs each plane with the document bits, counts ones, shifts by the plane index, and sums: 1 + 4 + 4 + 16 = 25. The scalar Java version walks set bits one query component at a time; the Vector API version (`ipByteBin256`) loads four query planes plus document bits as 256-bit vectors and reduces `and` plus `BIT_COUNT` across four independent chains.

### [37:29](https://youtu.be/adFS-_sCTQ4?t=2249) Proof in generated assembly

With `-XX:+PrintAssembly` and hsdis, the speaker shows the JIT emitting NEON `and`/`cnt`/`uaddlp` sequences on ARM and `vpand`/`vpshufb` popcount idioms on AVX2 YMM registers, confirming the Vector API calls really compile to SIMD. Gains: 32x smaller storage than float32 with typical recall above 90%. Costs: correction terms, two-phase latency, and cache pressure from scoring many documents.

### [39:01](https://youtu.be/adFS-_sCTQ4?t=2341) Why Elasticsearch went native with simdvec

Three reasons for ES carrying its own SIMD code: Lucene releases too slowly for new quantization formats, ES reads from `MemorySegment` while Lucene is built around `byte[]`, and bulk scoring (one query, many documents per pass) is tuned for HNSW traversal. The `simdvec` C++ library ships three tiers (AVX2/NEON, AVX-512/SVE, AVX-512-BF16), is called through Panama FFI, and is probed per CPU at startup; it does not work on Windows. The ES 9.5 decision chain is HotSpot plus C2, then vector module, then JDK 22 heap segments, then native simdvec availability, degrading from Native22 to Panama22 to Panama21 to scalar.

### [42:08](https://youtu.be/adFS-_sCTQ4?t=2528) FMA versus MUL+ADD, Intel versus ARM

A second live demo plus deck table: on the M3 Pro, FMA averages 0.050 ms against 0.034 ms for separate multiply plus add; on the Intel i9 both sit near 0.025 ms. The disassembly shows `fmla` versus `fmul`/`fadd` on NEON and `vfmadd231pd` versus `vmulpd`/`vaddpd` on AVX2. Lucene exposes FMA control (auto/true/false) because the fastest choice is platform dependent. The simdvec sources show per-ISA kernels (NEON `vfmaq_f32`, AVX2 `_mm256_fmadd_ps`, AVX-512 `_mm512_fmadd_ps`) all exporting `vec_dotf32` with the same throughput contract.

### [48:24](https://youtu.be/adFS-_sCTQ4?t=2904) ES|QL GROUP BY and SwissHash

At high group cardinality, ES|QL aggregation is bottlenecked by hash table probing, not the aggregation itself. The SwissHash fast path compares 16 control bytes against the target in one `ByteVector.eq` instruction and only fully checks matching lanes, with scalar fallback preserved. Other SIMD sites in Lucene and Elasticsearch: float and quantized scoring, posting decoding, byte scanning.

## Tools, libraries and specs

- Panama Vector API (incubating, JEP 529): species, lanes, `FloatVector.fma`, `reduceLanes`, `BIT_COUNT`
- Panama Foreign Function API: `@Function` FFI calls from Java into native `simdvec` kernels
- Apache Lucene 10.5.1: `DefaultVectorUtilSupport`, `PanamaVectorUtilSupport`
- Elasticsearch 9.5.0 `simdvec` library: `ESVectorizationProvider`, `PanamaESVectorUtilSupport`, `Native22ESVectorizationProvider`, per-ISA C++ kernels (`vec_f32_1.cpp`, `vec_f32_2.cpp`)
- Elasticsearch SwissHash (`LongSwissHash`) for ES|QL GROUP BY probing
- Better Binary Quantization (BBQ) and DiskBBQ quantization tiers; HNSW graph search
- Demo sources: https://github.com/pioorg/vectorapi-demos (javazone branch)
- `-XX:+PrintAssembly` with hsdis for verifying JIT SIMD emission

## Who should watch

Java developers working on search, vector workloads, or performance-sensitive numeric code gain the most, especially anyone considering the Vector API or running Elasticsearch vector search. Viewers wanting an introduction to vector search itself should watch one of the speaker's other talks first; hard-core SIMD programmers may find the lane basics familiar but still get value from the Lucene and Elasticsearch internals.

## Verdict

**8/10**: A self-run FMA head-to-head and live Vector API demos, with the Lucene and Elasticsearch design reasons explained; limited by benchmark numbers without a stated method and a demo repository that covers only the two micro-demos.

**Novelty 2/2**

- **+** [42:08](https://youtu.be/adFS-_sCTQ4?t=2528) The FMA versus MUL+ADD comparison on Apple M3 Pro and Intel i9 is a head-to-head the speaker ran himself: the split sequence wins by about 45% on the M3 Pro and ties on the Intel i9.
- **+** [37:29](https://youtu.be/adFS-_sCTQ4?t=2249) The speaker checks generated assembly himself, showing NEON and AVX2 SIMD instructions emitted for the Vector API BBQ scoring.
- **+** [39:01](https://youtu.be/adFS-_sCTQ4?t=2341) The reasons Elasticsearch moved past the Vector API to its own native kernels come from inside Elastic.

**Demonstrated 2/2**

- **+** [15:44](https://youtu.be/adFS-_sCTQ4?t=944) The scalar versus Vector API dot product runs live with visible speedups, then re-runs against a corrected unrolled baseline.
- **+** [28:07](https://youtu.be/adFS-_sCTQ4?t=1687) Local Elasticsearch logs on screen show the Vector API path activating with preferred bit size 128.
- **−** [48:24](https://youtu.be/adFS-_sCTQ4?t=2904) The simdvec FFI path and the ES|QL SwissHash fast path are shown as source and slide code only and never run.

**Measured 1/2**

- **+** [42:39](https://youtu.be/adFS-_sCTQ4?t=2559) FMA versus MUL+ADD average milliseconds are tabulated for both CPUs, with the instruction sequences shown.
- **−** [15:44](https://youtu.be/adFS-_sCTQ4?t=944) The live speedup runs are single ad-hoc executions that the speaker calls "not a benchmark", and the deck's speedup and FMA tables state no run count, warm-up or variance.
- **−** [46:20](https://youtu.be/adFS-_sCTQ4?t=2780) The native FFI win is claimed with "the penalty is like 5 milliseconds" and no baseline or setup.

**Depth 2/2**

- **+** [17:51](https://youtu.be/adFS-_sCTQ4?t=1071) The four-accumulator pattern is explained as overlapping FMA latency with fetches, applied to both scalar and vector paths.
- **+** [35:23](https://youtu.be/adFS-_sCTQ4?t=2123) The bit-plane transposition is worked by hand to the same score of 25, showing why scoring needs no multiplication.
- **+** [39:01](https://youtu.be/adFS-_sCTQ4?t=2341) The decision to bypass the Vector API with native kernels is justified through release cadence, `MemorySegment` layout, and bulk scoring.

**Reusable 1/2**

- **+** [15:44](https://youtu.be/adFS-_sCTQ4?t=944) The demo sources repository reproduces the scalar, Vector API, and FMA comparisons run on stage.
- **+** [45:17](https://youtu.be/adFS-_sCTQ4?t=2717) The Lucene and Elasticsearch files walked through are pinned upstream sources with paths and line numbers.
- **−** [34:52](https://youtu.be/adFS-_sCTQ4?t=2092) The BBQ bit-plane scoring has no runnable artifact: the repository's README lists only `dotproduct` and `fmavsmuladd`.
