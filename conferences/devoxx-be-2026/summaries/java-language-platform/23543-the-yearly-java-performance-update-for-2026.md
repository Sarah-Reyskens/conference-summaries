---
title: The Yearly Java Performance Update for 2026
talkId: "23543"
conference: devoxx-be-2026
speakers: [Per-Ake Minborg]
track: Java Language & Platform
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=rNOzf12RORI
durationMin: 42
slides: null
verdict: 6
reach: broad
frames: 9
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# The Yearly Java Performance Update for 2026
Per-Ake Minborg · Conference · Java Language & Platform

## TL;DR
Minborg, from Oracle's Java core library team, surveys the performance work across JDK 26 and 27 (plus a peek at 28): cheaper GC barriers, G1 everywhere, compact object headers by default, library fast paths, smarter vectorization, AOT caches, and lazy constants. The throughline is that most of the gains arrive automatically on upgrade, while a few (headers, collectors, AOT) repay deliberate measurement on your own workload.

## Key takeaways
- Upgrade first, tune second: reference-store barriers, stable String hashes, HashMap copy reuse, and record hash shapes speed up existing code with no changes.
- JDK 27 turns on compact object headers by default (12 to 8 bytes per header); test your app with them on and off, since smaller heaps mainly buy better cache locality.
- G1 is now the default collector in every environment, including single-CPU instances; serial GC stays available via flag and has no removal plan.
- Use an AOT cache for short-lived processes: training runs capture class state, profiles, and (coming) compiled code so startup skips warm-up work.
- Optimize where time is actually spent: a 4x gain on 10% of the work cuts only 7.5% of total time, so profile before chasing any single improvement.
- For FFM users, JDK 28's pooled arena allocation removes malloc/free from the hot path (over 10x on temporary allocations) with no API change.

## Notes

### [00:34](https://youtu.be/rNOzf12RORI?t=34) From bytecode to machine code: a JIT primer
The first twelve minutes, delivered without slides after a projector failure, walk through how the JVM executes code: interpretation with profiling, then C2 compilation of hot methods into machine code via an intermediate representation (IR) graph. Optimizations covered include intrinsics (handwritten machine code for encryption, index checks), bounds-check hoisting (128 checks down to 2 for a 64-byte loop), auto-vectorization with SIMD (one load, one vector add, one store), load/store reordering within the Java memory model, stable-field constant folding, loop unrolling with its code-cache trade-off, devirtualization of monomorphic calls (a Map that is always a HashMap), escape analysis that can stack-allocate non-escaping objects, and speculation guarded by uncommon traps that deoptimize when an assumption breaks. Limits get equal time: aliased pointers and flow-control breaks defeat vectorization, and float/double reassociation is restricted.

### [13:13](https://youtu.be/rNOzf12RORI?t=793) What performance means, and the roadmap
Performance splits into startup (deploy to serving), warm-up (time to reach compiled steady state), steady-state throughput under an SLA, and footprint. The talk then follows the speaker's inside.java per-release performance articles (co-written with Ana-Maria Mihalceanu and Claes Redestad), picking highlights from JDK 26 (barriers, allocation, vectorization, AOT) and JDK 27 (new defaults, library fast paths, runtime work), closing with a JDK 28 preview.

### [14:51](https://youtu.be/rNOzf12RORI?t=891) Three things carried over from JDK 25
AOT profiles add a train phase between compile and run: a training run records class initialization and profiles so the next start is faster and leaner. Compact object headers, opt-in in 26, become the default in 27. Stable cached String hash codes (marked with the internal stable annotation in JDK 25) let the JIT constant-fold through String-keyed lookups; for a String-to-MethodHandle map the VM can see through the whole lookup chain to the native call.

### [17:28](https://youtu.be/rNOzf12RORI?t=1048) JDK 26 and 27: barriers, GC defaults, headers, libraries
Reference stores got cheaper: the GC coordination moved from heavy per-store semantics to a dual-card scheme where application threads do less and a worker thread does more, worth around 5% or more on reference-heavy workloads. G1 is now default everywhere; `-XX:+UseSerialGC` still opts out. Compact headers shrink the header from 12 to 8 bytes, so a field-free object drops from 16 to 8 bytes; the bigger win is locality across L1/L2/L3. Library items: FFM native-memory-to-String drops one intermediate copy (19 down to 14 microseconds for five ASCII chars); generated record `hashCode` now carries the concrete key type so the JIT skips devirtualization; the HashMap copy constructor reuses precomputed hashes from a HashMap or unmodifiable-wrapped source instead of recomputing them, a large win shown on a 150-entry benchmark chart; URL formatting avoids intermediate strings and speeds up even interpreted mode.

### [25:47](https://youtu.be/rNOzf12RORI?t=1547) Vectorization: cost model, casts, Vector API
Auto-vectorization is not always profitable: alignment preambles and cleanup tails cost more than they save on tiny loops, so a heuristic cost model now skips those cases. Superword vectorization (wider than a long) now works through narrowing casts such as long-to-int and int-to-short. The incubating Vector API gains a see-through optimization when lane species have equal total size (e.g. 128-bit int species vs 64-bit short species).

### [28:26](https://youtu.be/rNOzf12RORI?t=1706) AOT caches, GC startup work, virtual threads
AOT object caching gains a streaming format usable with any collector, removing the same-GC restriction between training and production runs. Startup work shrinks: JDK 26 raises the default initial heap to avoid repeated expansion, and JDK 27 defers concurrent-mark structures and threads until needed, which helps start-compute-exit programs. Virtual threads blocked on class initialization now unmount from their carrier threads instead of pinning a scarce resource.

### [31:00](https://youtu.be/rNOzf12RORI?t=1860) Lazy constants and runtime robustness
Lazy constants (`java.lang.LazyConstant`, JEP 526 second preview in 26, JEP 531 third preview in 27) give single lazy initialization backed by the internal stable annotation, so the JIT can constant-fold a value that is computed once on demand. Semantics tightened between releases: JDK 26 allowed retry after failure, JDK 27 invokes the supplier exactly once and a failure stays failed. Also covered: a GC more robust under heavy allocation pressure, and the Object Monitor Table that takes over inflated locking now that compact headers leave no room for it, including a fixed locking regression.

### [34:13](https://youtu.be/rNOzf12RORI?t=2053) Peek into JDK 28: Valhalla, FFM arenas, AOT compilation
Valhalla value classes (identity given up, components compared) remain preview-only; flat arrays are still future work. The headline item is pooled allocation in FFM arenas: temporary native segments for errno-style out-parameters are sliced from pre-allocated 64-byte pools held directly on the thread, returning the slab to the thread pool on close, which beat malloc/free (often slower than the native call itself) by more than 10x with no API change. Other arena shapes vary too much in usage for one scheme. AOT compilation extends AOT caches to compiled machine code, collapsing warm-up on identical machines; differing platforms simply fall back to normal compile-on-statistics behavior.

### [37:58](https://youtu.be/rNOzf12RORI?t=2278) How to benchmark, and where to start
JDK work is validated with JMH microbenchmarks and workload measurements from the pull requests, illustrated with a String hashCode benchmark that can fold to a sub-nanosecond constant; all of it is synthetic, so it shows the effect in isolation rather than in your application. The closing "Where I would start" table maps workloads to first experiments: reference-heavy services try G1 on both releases and inspect CPU and pauses; many small objects toggle JDK 27 headers; short-lived processes compare default startup against an AOT cache; frequent map copies test real source wrappers and key types; numeric loops get their C2 output inspected on the deployment CPU.

## Tools, libraries and specs
- JDK 26 / 27 / 28 (preview): compact object headers, G1 default, AOT profile/cache/compilation, stable String hashes, lazy constants
- JEP 526 (Lazy Constants, second preview), JEP 531 (Lazy Constants, third preview)
- JMH (benchmarks behind the quoted numbers)
- Foreign Function and Memory (FFM) API: native-to-String path, pooled arena allocation
- Vector API (preview): species size matching for the see-through optimization
- Project Valhalla: value classes (preview)
- inside.java "Performance Improvements in JDK 26 / JDK 27" articles

## Who should watch
Java engineers deciding whether a JDK 26 or 27 upgrade is worth measuring, and anyone who wants a compact mental model of what the JIT and GC do for them. Skip it if you already read the inside.java performance articles in full; regular JVM-conference attendees will find the JIT primer familiar.

## Verdict
**6/10**: A survey of JDK 26 and 27 performance work by a JDK library author, with mechanism-level explanations of the JIT and the GC barrier, limited by numbers quoted without setups, nothing run on screen and material that is mostly a digest of his inside.java articles.

**Reach broad**: Most Java developers weighing a JDK 26 or 27 upgrade can use its defaults, header, AOT and measurement guidance in their own work.

**Novelty 1/2**

- **+** [35:51](https://youtu.be/rNOzf12RORI?t=2151) The FFM arena pooling design (four pre-allocated pools on the thread, slab returned on close, other arena shapes left out as too varied) comes from the speaker's own implementation work.
- **·** [12:41](https://youtu.be/rNOzf12RORI?t=761) The release-by-release roadmap explicitly picks highlights from the inside.java performance articles the speaker co-wrote, so most of it is also in those articles.

**Demonstrated 1/2**

- **·** [24:45](https://youtu.be/rNOzf12RORI?t=1485) A 42-minute survey of twenty-plus changes has no single claim to run end to end; evidence appears as benchmark charts on slides, such as the HashMap copy bars.

**Measured 1/2**

- **+** [22:08](https://youtu.be/rNOzf12RORI?t=1328) The FFM native-to-String path is quoted before and after: 19 down to 14 microseconds for five ASCII characters.
- **−** [36:21](https://youtu.be/rNOzf12RORI?t=2181) The pooled FFM allocation gain is given as "more than 10 in most cases" over malloc/free with no workload, unit or setup.
- **−** [18:29](https://youtu.be/rNOzf12RORI?t=1109) The dual-card barrier payoff is given as "maybe 5% or even more in some cases", with no baseline or setup.

**Depth 2/2**

- **+** [03:14](https://youtu.be/rNOzf12RORI?t=194) The JIT primer explains the IR graph, inlining, and a dozen optimizations with their mechanisms, not just their names.
- **+** [09:00](https://youtu.be/rNOzf12RORI?t=540) Loop unrolling is weighed against the larger code in the execution cache, with a "goldilocks" limit on how far to expand.
- **+** [17:59](https://youtu.be/rNOzf12RORI?t=1079) The GC barrier change is explained through its mechanism: dual cards that shift work from application threads to a worker thread.

**Reusable 1/2**

- **+** [40:36](https://youtu.be/rNOzf12RORI?t=2436) The closing table maps five workload shapes to a first experiment each, usable as a measurement checklist.
- **·** [40:05](https://youtu.be/rNOzf12RORI?t=2405) The experiments are described on one slide and left for the viewer to reconstruct; the talk points to articles, not a repository or config.
