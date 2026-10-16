---
title: Modern Java in Practice - The Features That Matter
talkId: "23524"
conference: devoxx-be-2026
speakers: [Nicolai Parlog, Falk Sippach]
track: Java Language & Platform
sessionType: Deep Dive
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=zC2tbq7S5UE
durationMin: 161
slides: https://slides.nipafx.dev/java-17+/
verdict: 7
reach: broad
frames: 12
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Modern Java in Practice - The Features That Matter
Nicolai Parlog, Falk Sippach · Deep Dive · Java Language & Platform
Slides: https://slides.nipafx.dev/java-17+/

## TL;DR
Parlog (Oracle Java Developer Advocate) and Sippach (embarc) survey Java 18 through 28 in a three-hour Deep Dive, going deep on data-oriented programming, virtual threads with structured concurrency, and new APIs, and wide on performance, security, and tooling. The recurring message: upgrade first for free performance and security gains, then simplify code with the new abstractions. The deck is published online and matches the talk slide for slide.

## Key takeaways
- Model closed data with records plus sealed types, operate on it with exhaustive pattern-matching switches, and skip `default` so the compiler flags every switch when a new variant arrives.
- Treat a JDK upgrade as the first performance move: compact object headers, generational ZGC, and the AOT cache cut heap, pauses, startup, and warmup without code changes.
- Use virtual threads plus structured concurrency as the default for new backends: blocking code, fan out with `fork`, rejoin with `join`, and let `Joiner` policies handle results and cancellation.
- Share request-scoped data with `ScopedValue` instead of (inheritable) thread locals: one-way flow, automatic cleanup, and free inheritance into child threads of a structured scope.
- Reach for the new JDK APIs before hand-rolled code or libraries: sequenced collections for encounter order, stream gatherers for custom intermediate operations, the HTTP client with opt-in HTTP/3, and `jwebserver` for local previews.
- Stay current for security: post-quantum TLS 1.3 ships in JDK 27, supported versions get the patches, and Oracle plans to move Oracle JDK security updates from quarterly to monthly.

## Notes

### [00:34](https://youtu.be/zC2tbq7S5UE?t=34) Scope and audience poll
The speakers widen the usual "what is new" format to Java 18 through 28, alternating deep segments with fast overviews, and take questions at any time. A show of hands put the audience mostly on recent versions: Java 8 around 15-20%, 11 near 10%, 17 around 20-25%, 21 the largest group, 25 close behind, and only scattered hands for 26 or 27. Parlog plugs the Inside Java podcast and Sippach's heise article on JDK 27.

### [04:42](https://youtu.be/zC2tbq7S5UE?t=282) Data-oriented programming: records, sealed types, pattern matching
Sippach builds the whole segment on a medication-plan example (a `Drug` enum, a sealed `Dosage` with `Tablet` and `Infusion` record variants, `Medication` and `MedicationPlan` records), inspired by the "Data Modeling with Sums and Products" post on funktionale-programmierung.de. Switch expressions (Java 14) return values with no fall-through; records (16) carry transparent state with compact-constructor validation, while `List.copyOf` in the compact constructor compensates for shallow immutability; sealed types (17) close the variant set so switches over `Dosage` are exhaustive without `default`. Pattern matching for `instanceof` (16) collapses test-cast-assign into one step with flow-scoped bindings; pattern matching for switch plus record patterns (21) add type patterns, nested deconstruction, `when` guards with dominance ordering (specific before general, else a compile error), `case null`, and unnamed `_` patterns (22). Primitive patterns are still in preview in 27 (JEP 532); Parlog adds they are held back partly because the related constant patterns are not yet firmly designed. The segment closes by contrasting Goetz's 2022 DOP principles with Parlog's 2024 "DOP v1.1" (data immutable *and transparent*, separate operations from data): adding an operation is one new function, while adding an alternative produces a compile error in every switch that needs a case. A post-break Q&A answer clarifies that dominance also applies across multi-level sealed hierarchies, so matching an interface and then its subtypes is flagged as dead code.

### [37:30](https://youtu.be/zC2tbq7S5UE?t=2250) Performance: compact headers, GC, AOT cache
Parlog's headline is that a newer JDK is a faster JDK. Compact object headers (Project Lilliput) shrink the 96-bit header to 64 bits: 5-30% smaller heaps, fewer collections, usually better performance with rare regressions, so measure. The flag is `-XX:+UseCompactObjectHeaders` on 25 and the default on 27. G1 is now the true default collector with no exceptions, virtual-thread pinning and ZGC improved across the board, and crypto intrinsics speed up handshakes. A cited Netflix chart shows maximum GC pause times collapsing to near zero after enabling generational ZGC. The AOT cache (Project Leyden) records a training run (class data, method profiles, optionally native code) and reuses it as initial state: 50-70% faster startup without compiled code, further gains with it, and optimal throughput after roughly 5 iterations instead of 10-20 on the shown warmup chart. Constraints include same JDK release, architecture, OS, classpath, and module options (plus same CPU features and GC for compiled code) and limited JVMTI agent use; mismatches just yield an ignored cache. A Q&A answer reports recording overhead around a handful of percent on Netflix canary deployments, but recording and consuming a cache cannot happen simultaneously.

### [47:51](https://youtu.be/zC2tbq7S5UE?t=2871) On-ramp: compact source files and scripting
Sippach traces the beginner path from the classic `HelloWorld` class through the single-file (11, JEP 330) and multi-file (22, JEP 458) source launchers to compact source files with `void main()`, module imports (25, JEP 511), and the `java.lang.IO` helpers plus implicit `java.base` imports (25, JEP 512). Parlog's "fast lane" turns this into automation: a `java-scripts` folder on `PATH`, executable files with a `#!/usr/bin/env -S java --source 25` shebang line, `Files` and `HttpClient` for local and remote data, and Adam Bien's zero-dependency `zeeds` project for ideas. The preview JSON API in JDK 28 parses with `Json.parse` into `JsonValue`, traverses known shapes with chained `get` calls that fail with informative errors, and explores unknown shapes with pattern matching over `JsonString`, `JsonNumber`, and siblings; it deliberately omits configuration, streaming, and data binding, leaving those to Jackson-style libraries. Dependencies still need third-party tools such as jbang or jpm, and shebang scripts cannot take a `-cp` flag, so the workaround is a small shell wrapper with an absolute path.

### [62:50](https://youtu.be/zC2tbq7S5UE?t=3770) Security, removals, and deprecations
Quantum computers can barely factor 35 today, but "harvest now, decrypt later" motivates post-quantum crypto: ML-KEM for keys (FIPS 203) and ML-DSA for signatures (FIPS 204), standardized by NIST, with IETF hybrid TLS 1.3 schemes (RFC 9954). The JDK added the algorithms in 24 and hybrid key exchange in 27, placing `X25519MLKEM768` first so it is negotiated by default when both sides support it; order is tunable via `jdk.tls.namedGroups` or per socket, and Oracle announced backports to Oracle JDKs 25 down to 8. The PEM API (final in 28) encodes and decodes keys, certificates, CRLs, and friends through `PEMEncoder`/`PEMDecoder` and the `BinaryEncodable` interface, decoding either to a known class or via a switch; the interface is sealed with one unreachable implementation so user switches stay non-exhaustive on purpose. Integrity by default now blocks JNI, final-field mutation, and dynamic agents unless opted in, `Unsafe` memory access is deprecated and disabled by default, `keytool` warns about weak PBE algorithms, and Oracle intends monthly Oracle JDK security updates starting in 2027, likely pulling other distributions along. Already removed: macOS/x64 (28), applet API (26), 32-bit x86 (25), Security Manager (24), biased locking, RMI activation, Nashorn, and CMS; finalization and `Unsafe` memory access are deprecated for removal, and a command-line flag lets you preview finalization-free behavior. A Q&A answer notes algorithms are rarely removed outright, just made harder to reach, since stored data may still need them.

### [77:32](https://youtu.be/zC2tbq7S5UE?t=4652) Virtual threads and scoped values
Virtual threads are plain `Thread` instances with a few hundred bytes of footprint that hold no OS thread while waiting, so waiting is free. Parlog stresses they raise throughput, not single-task latency: when work is not CPU-bound and downstream services scale, waiting on more things at once serves more requests. Adoption tips: never pool them, consider a platform-thread pool for CPU-heavy stretches, and cap concurrency with semaphores or locks instead of pools (the deck shows a 16-permit `DB_SEMAPHORE` guarding database calls). Caveats are pinning inside native calls, file-I/O capture, `jdk.virtualThreadScheduler.maxPoolSize`, and `InheritableThreadLocal` copying its value into every new thread. `ScopedValue` fixes the thread-local mess with `where(...).run(...)`: one-way data flow, automatic removal at scope exit (`get` outside throws `NoSuchElementException`), and free inheritance into child threads, at the cost of a less flexible flow that cannot express every inheritable-thread-local pattern.

### [92:06](https://youtu.be/zC2tbq7S5UE?t=5526) Structured concurrency
Structured concurrency borrows structured programming's answer to goto: concurrent flows must rejoin in the same block. The core idiom opens a `StructuredTaskScope` in try-with-resources, `fork`s subtasks onto virtual threads, `join`s explicitly, then reads results from non-blocking `Subtask.get()` calls; `close()` waits for every child thread, so cancellation via interrupts only shortens the wait if tasks honor `InterruptedException`.

```java
// from published slides (Structured Concurrency section)
try (var scope = StructuredTaskScope.open()) {
	Subtask<String> a = scope.fork(this::taskA);
	Subtask<String> b = scope.fork(this::taskB);
	scope.join();
	return a.get() + b.get();
} catch (ExecutionException ex) {
	// TODO: handle task errors
} // waits until all tasks/threads complete
```

A `Joiner` decides result collection, cancellation, and what `join` returns or throws: `awaitAllSuccessfulOrThrow` (the default), `allUntil` predicates, `allSuccessfulOrThrow` returning a result list, and `anySuccessfulOrThrow` returning the first success and cancelling the rest. Joiners accept exception-mapping functions (e.g. `IOException::new`), custom joiners implement `onFork`/`onComplete`/`onTimeout`/`result`, and scopes take a name, timeout (the clock starts when the scope opens; expiry surfaces as `CancelledByTimeoutException`), and thread factory. `ScopedValue` and structured scopes compose because both are lexically scoped (the deck's example forks two readers of 42 and prints 84), while legacy carriers like Log4j2's MDC travel via a custom `ThreadFactory` or its inheritable-thread-local flag. The "elephant in the room" is Reactive Streams: virtual threads absorb the non-blocking and event-driven machinery, some operators map to language constructs, queues, or libraries like Resilience4j, but the streaming API itself has no counterpart, and Parlog advises against rewriting working reactive applications. Version-wise: virtual threads in 21, no `synchronized` pinning plus scoped values in 25, structured concurrency in its fifth preview on 25 and final in 28 with minimal changes.

### [116:31](https://youtu.be/zC2tbq7S5UE?t=6991) New APIs: collections, gatherers, lazy values, HTTP/3
Sippach presents four everyday APIs. Sequenced collections (21, JEP 431) add `SequencedCollection`/`SequencedSet`/`SequencedMap` with `getFirst`/`getLast`, `addFirst`/`addLast`, and a `reversed()` view that writes through to the original; calling `addLast` on a `TreeSet` answers the on-stage quiz by throwing `UnsupportedOperationException`. Stream gatherers (24, JEP 485) are custom intermediate operations: built-ins `windowFixed`, `windowSliding`, `scan` (running totals), `fold`, and order-preserving `mapConcurrent`, plus hand-written ones built from an initializer, an `(state, element, downstream)` integrator, and optional combiner and finisher. The deck's `distinctBy` example keeps a `HashSet` of seen keys and pushes only each key's first element, and gatherers compose in a single pipeline. Lazy constants (preview, JEP 531) replace double-checked-locking singletons with `LazyConstant.of(Model::load)`, which initializes at most once successfully, reads as a true constant to the JVM for constant folding, retries after failures, rejects `null`, and throws `IllegalStateException` on cycles; `List`/`Map`/`Set.ofLazy` extend the idea to collections. HTTP/3 support (26, JEP 517) is opt-in per client or per request over QUIC/UDP with integrated TLS 1.3, with four negotiation strategies trading first-request delay against unused connections. Bonus items: the `jwebserver` one-liner for local previews and Marc Hoffmann's Java Almanac for diffing APIs across releases.

### [148:25](https://youtu.be/zC2tbq7S5UE?t=8905) JFR, Javadoc, and tooling
Parlog calls JFR heavily underutilized: roughly 1% overhead with defaults, record with `-XX:StartFlightRecording` or `jcmd $pid JFR.start`, analyze in JDK Mission Control, `jfr view`, or `jfr print` to XML/JSON. Shown examples trace `HashMap::resize` calls, time class initializers (`HBShaper.<clinit>` at 32.50 ms tops the sample table), and sample CPU time into flame graphs; the JDK ships almost 200 events (`jfr metadata` lists them), with 27 adding in-process redaction of sensitive properties. Javadoc gains Markdown (`///` lines, CommonMark 0.30, `[text][element]` links) in 25 and `{@snippet}` regions pulled from compiled and tested source files in 21, so documentation examples cannot silently rot. Nearly every CLI tool improved; the version table highlights `jfr view`, snippets, and `jwebserver` for 21, method timing/tracing, CPU-time profiling, cooperative sampling, and Markdown Javadoc for 25, and JFR redaction for 27. The close points at slides.nipafx.dev, the speakers' and Java team's channels, and embarc's cheat sheets at embarc.de/en/cheat-sheets.

## Tools, libraries and specs
- Project Amber: switch expressions (JEP 361), records (JEP 395), `instanceof` patterns (JEP 394), sealed types (JEP 409), pattern matching for switch (JEP 441), record patterns (JEP 440), unnamed patterns (JEP 456), primitive patterns preview (JEP 532)
- Compact object headers, Project Lilliput (`-XX:+UseCompactObjectHeaders`, default in 27)
- Generational ZGC, G1 (true default), FFM API, Vector API
- AOT cache, Project Leyden (`-XX:AOTCacheOutput` / `-XX:AOTCache`)
- Compact source files, instance main, `IO` (JEP 512), module imports (JEP 511), source launchers (JEP 330, JEP 458)
- JSON API preview in JDK 28 (`Json.parse`, `JsonValue`)
- jbang, jpm, Adam Bien's zeeds scripts
- ML-KEM (FIPS 203), ML-DSA (FIPS 204), hybrid TLS 1.3 (RFC 9954), `jdk.tls.namedGroups`, PEM API (`PEMEncoder`, `PEMDecoder`, `BinaryEncodable`)
- Structured concurrency (`StructuredTaskScope`, `Joiner`, `Subtask`), `ScopedValue`, virtual threads (`jdk.virtualThreadScheduler.maxPoolSize`), Resilience4j, Log4j2 MDC, Reactive Streams
- Sequenced collections (JEP 431), stream gatherers (JEP 485), lazy constants (JEP 531), HTTP/3 client (JEP 517), `jwebserver`
- JDK Flight Recorder and JDK Mission Control (`jfr view`, `jfr print`, `jfr metadata`), Javadoc Markdown and `{@snippet}`
- Java Almanac (API diffs), Inside Java podcast, Sippach's JDK 27 heise article

## Who should watch
Java developers on 17 or older who need both the upgrade case and the coding patterns, and intermediate developers on 21+ who want one coherent tour of data-oriented programming, virtual threads, and structured concurrency. Teams weighing reactive against virtual threads get a clear statement of the trade. Skip it if you already ship 25/27 idioms (records, sealed types, gatherers, structured concurrency) or want depth on any single topic: each segment compresses a full talk into 20-40 minutes.

## Verdict
**7/10**: a Java upgrade and programming-model survey with comparative performance charts and detailed concurrency trade-offs, limited by slide-bound examples rather than an end-to-end execution of the core patterns.

**Reach broad**: most of the conference's Java backend developers can put the upgrade case, the language idioms, and the concurrency and tooling practices to use in their own services within the next year.

**Novelty 1/2**

- **+** [05:16](https://youtu.be/zC2tbq7S5UE?t=316) The medication-plan example brings a credited sums-and-products article together with the speakers' selected Java features into one domain-modeling walkthrough.
- **+** [03:10](https://youtu.be/zC2tbq7S5UE?t=190) The survey connects language features, runtime upgrades, security and tooling into an upgrade-oriented selection spanning multiple Java releases.

**Demonstrated 1/2**

- **+** [55:00](https://youtu.be/zC2tbq7S5UE?t=3300) A slide pairs the executable shebang script's source with a terminal transcript in which `hello` prints "Hello, scripts!".
- **+** [151:01](https://youtu.be/zC2tbq7S5UE?t=9061) A slide pairs the JFR method-trace command with `jfr print` output: start time, duration, method and thread for a `HashMap::resize` call, with the stack trace cut.
- **−** [93:07](https://youtu.be/zC2tbq7S5UE?t=5587) The central structured-concurrency example is narrated line by line from on-slide code and never executed.

**Measured 2/2**

- **+** [41:08](https://youtu.be/zC2tbq7S5UE?t=2468) A Netflix chart shows maximum GC pause times collapsing to near zero after enabling generational ZGC.
- **+** [43:44](https://youtu.be/zC2tbq7S5UE?t=2624) A bar chart (Linux/x64, 2 cores) compares five frameworks without an AOT cache, with one, and with AOT code: 50-70% faster startup without AOT code, further gains with it, and a warm-up chart with the same three configurations.
- **−** [147:22](https://youtu.be/zC2tbq7S5UE?t=8842) Overhead for the AOT training run ("a handful of percent") comes from a recollected conversation with Martin Chalupa of Netflix rather than a shown measurement.

**Depth 2/2**

- **+** [39:35](https://youtu.be/zC2tbq7S5UE?t=2375) The compact-headers segment turns on the decompression trade-off: compressed bits cost CPU that can outweigh the savings, so adopters must measure.
- **+** [103:03](https://youtu.be/zC2tbq7S5UE?t=6183) The Joiner contract is walked through method by method, with onFork registering each subtask, onComplete deciding whether to continue, and result returning or throwing.
- **+** [112:25](https://youtu.be/zC2tbq7S5UE?t=6745) Reactive streams are weighed against virtual threads: back pressure maps to language constructs and queues, resilience4j works on the thread model, and old applications are not worth rewriting without a maintenance horizon.

**Reusable 1/2**

- **+** [84:48](https://youtu.be/zC2tbq7S5UE?t=5088) The semaphore snippet provides a pattern for capping database concurrency while using virtual threads.
- **+** [149:28](https://youtu.be/zC2tbq7S5UE?t=8968) The JFR launch and attach commands are available to reconstruct a recording workflow.
- **·** [130:41](https://youtu.be/zC2tbq7S5UE?t=7841) The custom gatherer is presented as a code fragment to reconstruct rather than a linked sample project reproducing the talk's main examples.
