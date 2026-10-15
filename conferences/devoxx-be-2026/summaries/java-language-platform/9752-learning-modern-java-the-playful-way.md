---
title: Learning modern Java the playful way
talkId: "9752"
conference: devoxx-be-2026
speakers: [Marit van Dijk, Piotr Przybyl]
track: Java Language & Platform
sessionType: Deep Dive
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=QBQ11aL2aZc
durationMin: 179
slides: https://speakerdeck.com/mlvandijk/learning-modern-java-the-playful-way-devoxx-deep-dive
verdict: 8
frames: 23
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Learning modern Java the playful way
Marit van Dijk, Piotr Przybyl · Deep Dive · Java Language & Platform
Slides: https://speakerdeck.com/mlvandijk/learning-modern-java-the-playful-way-devoxx-deep-dive

## TL;DR
Two developer advocates spend three hours live-coding their way through twenty Java features, from records and pattern matching to structured concurrency and value objects, inside one running demo application. The thesis: modern Java removed most of the old verbosity and upgrading pays for itself, so learn each feature by playing with it in your IDE.

## Key takeaways
- Replace hand-rolled `CompletableFuture` fan-out with structured concurrency: the scope makes fork, join and cancellation visible instead of spreading cross-cancellation callbacks through the code.
- Treat `parallelStream()` as guilty until proven innocent on IO work; a busy neighbor on the shared pool turned 10 seconds into 30, while `Gatherers.mapConcurrent` isolates the work on virtual threads.
- Upgrade for free performance even off the LTS track: compact object headers in Java 27 shrank 10M small objects from about 190 MB to 114 MB with no code change.
- Keep structured-concurrency subtasks interruptible; cancellation is implemented with interruption, so a CPU-bound task that ignores interrupts blocks the whole scope.
- Prefer one-way immutable scoped values over `ThreadLocal` for request context; their lifetime is visible in the code and they cannot leak one client's data to another.
- Learn to read thread dumps and JFR allocation views for virtual-thread work; the structure of scopes and carriers shows up there, not just in source.
- Play scientist with new features: state a hypothesis, run the experiment in the IDE, and keep what survives instead of trusting blog posts or agents.

## Notes

### [00:42](https://youtu.be/QBQ11aL2aZc?t=42) Opening: meme show and audience poll
The session opens with a meme slideshow run from the IDE. An audience poll finds about half the room on Java 25 (fewer in production), 20 to 30 on 21, a handful on 17 and 8, and one person below 8. The agenda: selected features from recent Java versions, each with live demos, plus upgrade arguments to take back to management.

### [10:05](https://youtu.be/QBQ11aL2aZc?t=605) Java 25 through 28 in ten minutes
The flyover lists what each release brings. Java 25: generational Shenandoah, compact object headers as experimental, scoped values plus structured concurrency, JFR improvements, compact source files. Java 26: Amber, Loom, Panama and Vector API progress, Leyden groundwork. Java 27: compact headers by default, G1 default everywhere. Java 28 (due March): value objects and a simple JSON API.

### [14:17](https://youtu.be/QBQ11aL2aZc?t=857) Compact source files and instance main methods
Java 25 (JEP 512) lets a program be an unnamed class with `void main()` and `IO.println`, shorter than the equivalent Python starter. IntelliJ converts between compact and classic form in both directions, and `import module java.base` arrives implicitly.

```java
// from published slides p.16
import static java.lang.IO.println;
void main() {
    IO.println("Hello World!");
}
```

### [20:31](https://youtu.be/QBQ11aL2aZc?t=1231) The running demo: an image webshop
The demo app is a Java-8-era shop selling 12 stock images. A self-hosted Jina multimodal encoder turns each image into a 768-float embedding stored in Elasticsearch with filename and price. Searches run hybrid: classic text plus kNN vector search, fused with reciprocal rank fusion. All setup runs through bash and HTTP calls, offered as proof that AI features need no language switch. A "fru " query with a typo still finds fruit, plums and apples.

### [30:26](https://youtu.be/QBQ11aL2aZc?t=1826) Records
Records (Java 16, JEP 395) turn the 40-line `QueryWithVector` carrier into a three-line record via an IDE refactoring. The demo overrides `toString` to print only the first and last embedding values. Records suit request and response DTOs but not Hibernate entities, since they are final; Morphia for MongoDB accepts them.

### [33:02](https://youtu.be/QBQ11aL2aZc?t=1982) Module imports
`import module java.base` (Java 25, JEP 511) replaces about twenty import statements, transitively pulling in modules such as `java.xml` through `java.sql`. Name clashes (for example `java.sql.Date`, or `List` under `import module java.se`) still need explicit single imports. Presented as a prototyping convenience, not production style.

### [37:46](https://youtu.be/QBQ11aL2aZc?t=2266) Simple IO
`IO.readln` with an optional prompt string replaces the `Scanner` ceremony for console input. The search loop keeps working after the swap, including a query for "orange" that matches both the fruit name and the color.

### [39:19](https://youtu.be/QBQ11aL2aZc?t=2359) Stream gatherers
Gatherers (Java 24, JEP 485) are custom intermediate operations chained with `.gather()`; the JDK ships `mapConcurrent`, `fold`, `scan`, `windowFixed` and `windowSliding`. A starvation demo shows a noisy neighbor stretching five parallel-stream tasks from 10 to 30 seconds on the shared pool. Rewriting the pipeline with `gather(mapConcurrent(5))` fixes it and reads better. A multilingual run shows semantic matches, including an Apple computer image for "computer".

### [50:12](https://youtu.be/QBQ11aL2aZc?t=3012) Debugging streams and beyond
Log points are non-suspending breakpoints that print to the console, usable remotely and inside library code. The stream debugger plugin visualizes each pipeline stage with a trace view. Evaluate-expression covers ad-hoc fixes, and an upcoming IntelliJ debugger skill will let agents set log points themselves.

### [58:29](https://youtu.be/QBQ11aL2aZc?t=3509) Structured concurrency refactor
The hybrid search fan-out (two subtasks, combine with RRF, all-or-nothing) is the textbook structured-concurrency shape. The `CompletableFuture` version needs manual cross-cancellation that grows quadratically: two futures need two cancellations, three need six. A live-template refactor produces a `StructuredTaskScope` with `Joiner.awaitAllSuccessfulOrThrow`, a name and a timeout, then deletes the callback block.

```java
// from published slides p.32
try (var scope = StructuredTaskScope.open(
    StructuredTaskScope.Joiner.awaitAllSuccessfulOrThrow(), config -> config
        .withName("myStructuredConcurrency")
        .withTimeout(Duration.ofSeconds(5))
        .withThreadFactory(myThreadFactory))) {
    var subtask1 = scope.fork(() -> action(...));
    var subtask2 = scope.fork(this::anotherAction);
    scope.join();
    combineResults(subtask1.get(), subtask2.get());
}
```

### [69:24](https://youtu.be/QBQ11aL2aZc?t=4164) Cancellation rides on interruption
A name-plus-score service demo shows a failing subtask cancelling its sibling in milliseconds. Swapping the work for a CPU-bound loop that ignores interrupts stretches the same failure to a full second: cancellation is interruption, so database, cache and HTTP calls must stay interruptible.

### [74:07](https://youtu.be/QBQ11aL2aZc?t=4447) Lazy constants
`LazyConstant` (preview in Java 27, JEP 531) holds immutable, thread-safe values created on first `get()`, with `orElse` and `isInitialized` helpers. The demo converts an `ObjectMapper` field so class loading no longer pays for objects the first requests may never need. The field itself must stay `final`, or the laziness guarantee breaks.

### [79:18](https://youtu.be/QBQ11aL2aZc?t=4758) Markdown documentation comments
Markdown doc comments (Java 23, JEP 467) replace HTML-flavored Javadoc with a Markdown dialect while keeping `@param`, `@return` and `@throws`. IntelliJ writes the new style by default. A JetBrains Air agent in EAP generates the method docs on stage, and the result renders in the IDE and through the `javadoc` tool.

### [82:58](https://youtu.be/QBQ11aL2aZc?t=4978) Upgrading means learning new idioms
Bumping the Elasticsearch client to version 9 replaces a hand-built configuration with lambda-style setup, environment-sourced secrets, and a Testcontainers integration test with an injected CA. The point generalizes: Spring and the upcoming Maven 4 keep raising their Java floors, so moving a little with every release beats an emergency migration during a vulnerability.

### [89:13](https://youtu.be/QBQ11aL2aZc?t=5353) Compact object headers
Java 27 (JEP 534) shrinks 64-bit object headers from 96 to 64 bits by default: smaller heaps, denser deployments, better locality, zero code changes. The `Tiny` demo allocates 10M empty objects and compares JFR allocation trees: about 190 MB on Java 25 versus 114 MB on Java 27. The speakers flag this as an extreme case, since the objects are nearly all header, and note JetBrains Runtime 25 already enables the flag (IJPL-212987).

### [98:06](https://youtu.be/QBQ11aL2aZc?t=5886) Vector API
The Vector API (incubator in Java 27, JEP 537) expresses SIMD work: a 128-bit register holds four ints, so scalar loops waste three quarters of it. A Junie agent generates vector versions of `MathOps` kernels from a prompt. The vector code runs about twice as fast on some operations and no faster on others. A `docker exec ps` proves the bundled Elasticsearch runs with the incubator vector module on JDK 26.

### [109:09](https://youtu.be/QBQ11aL2aZc?t=6549) Simple JSON API
Java 28 incubates a strict-subset JSON API (JEP 540): parsing and generation for primitives, arrays and objects, with no streaming or custom serializers. It targets tiny services that would otherwise pull a library for three requests. The demo parses a payload, uses `orElse` for missing keys, and matches values with `instanceof` patterns. A Daily WTF story about 12 barges of coal warns that formats stay tricky.

### [115:26](https://youtu.be/QBQ11aL2aZc?t=6926) Value objects
Value objects (preview in Java 28, JEP 401) are immutable classes without identity: equal values compare `==`, locking on them throws, and the JVM may flatten them into array cells. Demos show `LocalDate` gaining `==` equality under `--enable-preview` and inheritance rules (abstract value classes only; concrete subclasses final or value). A substring nuance shows `==` still follows reference identity for embedded identity objects.

### [132:09](https://youtu.be/QBQ11aL2aZc?t=7929) Virtual threads refresher
Few hands go up for virtual-thread use, so the talk recaps them (Java 21, JEP 444): same `Thread` model, cheap to start, unmounting carriers on IO and sleep, daemon by default, thread-per-request without pooling. Virtual threads improve scalability for IO-bound work; they never make the CPU itself faster.

### [139:03](https://youtu.be/QBQ11aL2aZc?t=8343) Pinning: find it and fix it
A legacy Elasticsearch client called inside a `synchronized` method pins virtual threads to carriers. Adding `jdk.tracePinnedThreads=full` to a Testcontainers plus Toxiproxy test pinpoints line 54, and the test fails on Java 21. Switching the container image to Java 24, where synchronized blocks no longer pin (JEP 491), turns it green. Native calls can still pin.

### [145:54](https://youtu.be/QBQ11aL2aZc?t=8754) Scoped values
Scoped values (Java 25, JEP 506) are one-way immutable ThreadLocals with lifetimes visible in the code: no clearing to forget, no cross-client leaks. A nesting demo shows inner scopes shadowing outer ones and out-of-scope reads throwing. A Star Trek demo propagates Voyager security clearance through structured concurrency, drops it to zero in the brig, and restores it after; the same shape gives least-privilege logging.

### [154:11](https://youtu.be/QBQ11aL2aZc?t=9251) Flexible constructor bodies
Constructors (Java 25, JEP 513) may validate and compute arguments before the `super()` or `this()` call, replacing factory methods and argument-wrapping tricks. Legal: static calls, assigning (not reading) instance fields; illegal: instance methods, reassignment, conditional jumps. The same rules cover records and enums. The demo stalls on a wrong module target (27 versus 25) before running.

### [159:53](https://youtu.be/QBQ11aL2aZc?t=9593) Record patterns, unnamed variables, primitive patterns
Record patterns (Java 21, JEP 440) deconstruct records with nesting in `instanceof` and `switch`. Unnamed variables and patterns (Java 22, JEP 456) ignore what does not matter: `Rekord(_)`, unused catch parameters, lambda arguments, try-with-resources handles. Primitive patterns (preview in Java 27, JEP 532) extend `switch` to all primitives with guards and exhaustiveness checks. The pierogi demo switches over Polish plurals (pieróg, pierogi, pierogów, with 11-14 as exceptions and `Integer.MAX_VALUE` in heaven) and insists the word is never "pierogis".

### [172:54](https://youtu.be/QBQ11aL2aZc?t=10374) Quick hits and the LTS rant
Sequenced collections (Java 21, JEP 431) add `getFirst`, `getLast`, `removeLast` and `reversed`. The foreign function and memory API (Java 22, JEP 454) covers the C++ parts of Elasticsearch. The closing rant: the S in LTS stands for support almost nobody pays for, so LTS-only shops get zero support while missing free gains, and they still must rebump quarterly images for CVEs.

### [176:29](https://youtu.be/QBQ11aL2aZc?t=10650) Close
The speakers ask for session ratings, point at a feedback form and a QR code to the talk page, hand webcam covers to the room, and invite everyone to the JetBrains booth.

## Tools, libraries and specs
- JEPs named on screen: 512 (compact sources), 511 (module imports), 395 (records), 485 (gatherers), 533 (structured concurrency), 531 (lazy constants), 467 (Markdown docs), 534 (compact headers), 537 (Vector API), 540 (JSON), 401 (value objects), 444 (virtual threads), 491 (no pinning), 506 (scoped values), 513 (flexible constructors), 440 (record patterns), 456 (unnamed), 532 (primitive patterns), 431 (sequenced collections), 454 (FFM)
- IntelliJ IDEA: log points, stream debugger plugin, evaluate expression, command completion, SDK detection from `.sdkmanrc`, env-file run plugin; EAP items are JetBrains Air agents, the Junie agent and a debugger skill
- Demo code: `github.com/pioorg/modern-playful-Java25`, `github.com/pioorg/modern-playful-Java26` (the talk page's `modern-playful-Java27` link returns 404), `github.com/pioorg/DeepDiveJava21` through `DeepDiveJava28`, `github.com/pioorg/memeshow`
- Elasticsearch 9.x with Kibana and ESQL, bundled JDK 26, `--add-modules=jdk.incubator.vector`; Jina multimodal embedding model self-hosted on CPU
- Testcontainers, Toxiproxy, `jdk.tracePinnedThreads`, Java Flight Recorder allocation views, SDKMAN

## Who should watch
Java developers on 8 through 21 who want a guided tour of what the last six years added, with runnable examples for each feature. Beginners get approachable explanations; experienced developers get the upgrade ammunition (headers, pinning, gatherers). Skip it if you already use structured concurrency, scoped values and the Java 25 starter features daily, or if you want a deep single-topic treatment instead of a survey.

## Verdict
**8/10**: Live Java-feature refactors, paired allocation and starvation measurements, and beginner-level explanations of cancellation and memory layout earn the score; the day's main demo repository remains unavailable.

**Novelty 1/2**

- **+** [28:22](https://youtu.be/QBQ11aL2aZc?t=1702) The speakers' own hybrid-search application carries the Java-feature tour through one working example.
- **+** [141:11](https://youtu.be/QBQ11aL2aZc?t=8471) The Toxiproxy plus Testcontainers pinning test with `jdk.tracePinnedThreads` supplies the speakers' diagnostic recipe alongside the language-feature sources.

**Demonstrated 2/2**

- **+** [64:45](https://youtu.be/QBQ11aL2aZc?t=3885) The structured-concurrency refactor runs the hybrid search end to end after the CompletableFuture callback block is deleted.
- **+** [144:19](https://youtu.be/QBQ11aL2aZc?t=8659) The pinning test fails on Java 21 and passes after the container image is switched to Java 24, with the pinned call identified at line 54.

**Measured 2/2**

- **+** [93:53](https://youtu.be/QBQ11aL2aZc?t=5633) The same ten-million-object program reports about 190 MB on Java 25 versus 114 MB on Java 27, with each run recorded to JFR for allocation inspection.
- **+** [43:57](https://youtu.be/QBQ11aL2aZc?t=2637) Five parallel-stream tasks take 10 seconds alone and 30 seconds after a busy-neighbor stream is enabled, showing the shared-pool effect against a controlled baseline.
- **−** [94:58](https://youtu.be/QBQ11aL2aZc?t=5698) The speakers identify the nearly all-header objects as an extreme allocation case whose savings depend on the application's actual objects.

**Depth 2/2**

- **+** [59:32](https://youtu.be/QBQ11aL2aZc?t=3572) The all-or-nothing hybrid-search requirement explains why sibling cancellation belongs in a task scope rather than an expanding set of cross-cancellation callbacks.
- **+** [73:05](https://youtu.be/QBQ11aL2aZc?t=4385) The cancellation experiment explains interruption as the mechanism and shows why an uninterruptible CPU-bound task delays scope completion.
- **+** [120:35](https://youtu.be/QBQ11aL2aZc?t=7235) The value-object explanation connects possible flattening into array cells with fewer reference indirections and better cache locality.

**Reusable 1/2**

- **+** [55:53](https://youtu.be/QBQ11aL2aZc?t=3353) The speakers point to cloneable GitHub examples, with DeepDiveJava21 through 28 and modern-playful-Java25/26 verified to exist.
- **−** [177:30](https://youtu.be/QBQ11aL2aZc?t=10650) The day's talk-page link to modern-playful-Java27 returns 404, leaving the current running application's code unavailable through that advertised repository.
