---
title: Big Runtimes Make Efficient Programs
talkId: "49252"
conference: devoxx-be-2026
speakers: [Ron Pressler]
track: Java Language & Platform
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=vhDwy1eCXbs
durationMin: 50
slides: null
verdict: 8
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Big Runtimes Make Efficient Programs
Ron Pressler · Conference · Java Language & Platform

## TL;DR
Pressler argues the JVM's large runtime exists to make large, evolving programs fast: the JIT removes abstraction costs C++ pays per call, and generational moving collectors turn spare RAM into cheaper memory management. He backs it with a Java Caffeine vs Rust Moka caching experiment and closes with advice to write natural Java code and profile it rather than follow JVM folklore.

## Key takeaways
- Judge a language by the speed of the programs you can actually write and maintain, not by what a hypothetical optimal program could achieve.
- Evolvability needs runtime-known information while AOT optimization needs compile-time-known information; compiling at runtime after profiles are known resolves the conflict.
- Generational moving collectors free memory in bulk instead of object by object, so extra heap headroom buys lower CPU use under high allocation rates.
- A caching experiment (30M strings, 90% hit rate) showed Java/Caffeine on ZGC beating Rust/Moka on latency at 5K and 10K RPS with less memory-management CPU.
- Moving GCs cannot share a heap directly with native code because pointers are unstable, so low-levelness (direct hardware access) and the fastest memory management are mutually exclusive.
- Profile in production with JFR (~1-2% overhead); write the most natural code and let the JVM adapt to it.

## Notes

### [01:35](https://youtu.be/vhDwy1eCXbs?t=95) Why a C++ developer stopped fearing big runtimes
Pressler spent years on large performance-sensitive C++ software: green-field code was elegant and fast, but after about five years of evolution it became hard to keep fast without high maintenance cost. He was skeptical of HotSpot's vision until his team adopted Java and programs stayed fast at lower maintenance cost. The skepticism he hears today comes from programmers who never maintained large low-level programs through years of evolution.

### [04:09](https://youtu.be/vhDwy1eCXbs?t=249) What runtimes are
A runtime is any code in the program that is not a direct compilation of application or library code; every language has one. In C and C++ the runtime looks like a library, while in Java a layer sits between program code and hardware/OS. Big-runtime languages (Java, Python, C#, JavaScript, Erlang) vary far more in goals and performance characteristics than low-level languages do, so treating them as one category confuses more than it explains: Java's JIT resembles LLVM more than V8.

### [06:15](https://youtu.be/vhDwy1eCXbs?t=375) What language performance means
The rigorous definition ("for every program in Y an equivalent program in X exists that is at least as fast") is useless because it ignores the cost of the reduction: the program must be writable with the resources at hand. Abstraction keeps changes local, but optimization needs implementation specifics, which breaks abstraction boundaries. The C++ circle/shape example shows the cost: generalizing `double_area` to a virtual call adds vtable dispatch, and template monomorphization to remove it virally rewrites every caller.

### [10:22](https://youtu.be/vhDwy1eCXbs?t=622) Zig's vtable boundary states the same trade-off
Pressler quotes Andrew Kelley's talk on Zig std changes: keep hot paths "north of the vtable boundary" because runtime-known function pointers are a black box to the optimizer, while moving logic above the boundary makes interfaces less flexible. Kelley calls it a fundamental deal with the laws of physics; Pressler agrees it is well known to low-level programmers and offers Java's answer: compile after the runtime information is known.

### [13:59](https://youtu.be/vhDwy1eCXbs?t=839) Benchmarks do not generalize
Since the Pentium era, performance depends on global context: the same code compiles differently per call site, malloc/free speed depends on history, and caches and branch prediction vary with program state. Benchmarks generalize worst of all because their unnatural CPU/RAM/IO mix triggers statistical optimizations oddly. Only the author of the measured mechanism can learn from a benchmark. Language designers therefore reason about design trade-offs (speed vs memory, latency vs throughput, average vs worst case) instead of benchmark scores.

### [19:49](https://youtu.be/vhDwy1eCXbs?t=1189) The JIT removes abstraction cost by speculating
The Java version of the shapes example keeps the virtual call but pays no vtable cost: HotSpot profiles the running program, speculates a call site always sees Circle, and inlines accordingly. Wrong guesses deoptimize back to the interpreter and recompile. The same speculation applies to if/else and switch branches (a colleague's C++-to-Java rewrite ran 20x faster on one switch). Trade-offs: warm-up time (mitigated by caching generated code across runs) and worse worst cases than C++ when speculation fails. HotSpot still misses specialization opportunities through profile pollution and array cases.

### [25:00](https://youtu.be/vhDwy1eCXbs?t=1500) Profile-guided AOT is converging but distinct
AOT compilers with profile-guided optimization also feed runtime profiles back into compilation, and some emit fast/slow dual paths, but they cannot speculate as aggressively as a JIT because AOT machine code must always work and binary size would explode. Low-level languages also still expose virtual, static, and specialized dispatch as separate constructs with different intended costs.

### [27:06](https://youtu.be/vhDwy1eCXbs?t=1626) Memory management: bulk freeing beats static knowledge
Objects outlive the routines that allocate them, so lifetime changes in C++ and Rust demand non-local edits (Rust makes them safe, not local). Paradoxically, knowing statically when an object dies is worse: freeing one object at a time is inefficient compared to generational moving collectors that free in bulk, making both allocation and freeing cheaper. Extra headroom scales with allocation rate, not data size, so moving collectors compensate CPU pressure with RAM when RAM is the less scarce resource.

### [28:39](https://youtu.be/vhDwy1eCXbs?t=1719) Caffeine vs Moka: 20% GC CPU beats 40%+ manual CPU
A GC-team colleague compared Java Caffeine (ZGC) with Rust Moka on the same workload (30M strings, 90% hit rate). Java used 40GB vs 38GB RAM but won every latency percentile at both 5K RPS (p99 1.148ms vs 2.063ms) and 10K RPS (p99 0.953ms vs 9.935ms), using 18% vs 57% CPU at 10K RPS. Java spent 20% of CPU on memory management, visible in JFR; the Rust program spent over 40% just deciding when it is safe to free objects, excluding malloc/free. Pressler stresses the numbers are not generalizable; the point is how much hidden CPU manual memory management costs.

### [32:47](https://youtu.be/vhDwy1eCXbs?t=1967) Why low-level languages cannot have moving GCs
Moving collectors relocate objects and store metadata in address bits, so heap pointers are not stable machine addresses and an FFI layer must separate the heap from hardware and OS. Low-level languages live at that level by definition, so they are excluded by domain constraint, not performance. The same applies to code pointers under a deoptimizing JIT. Stack pointers in low-level languages similarly block efficient user-mode threads like virtual threads.

### [36:27](https://youtu.be/vhDwy1eCXbs?t=2187) Fast runtimes are big everywhere
ZGC is about 50K SLOC including shared GC code, versus 3.5K for glibc ptmalloc; but TCMalloc (32K) and jemalloc (43K) show C-world runtimes also grow large to perform. Pressler admits he asked an AI agent for these numbers without checking them. The remaining structural handicap is memory layout: Java object arrays are pointer arrays with poor locality, which Project Valhalla addresses by letting programmers declare semantics (no identity, non-null) while the JVM decides flattening.

### [39:02](https://youtu.be/vhDwy1eCXbs?t=2342) JFR, advice, and Q&A
JFR emits deep runtime telemetry at about 1-2% production overhead, far deeper than eBPF on C++ (a malloc probe reports size but not object type). Tips for new runtime authors: know types at runtime, keep pointers out of the FFI, disallow pointers into the stack, ship deep low-overhead telemetry. For Java programmers: distrust JVM folklore since it rots as the JVM changes, and write natural code the JIT is tuned for. In Q&A, amortized JIT cost means paying full price at most twice before matching C++ speed, and pooling objects to avoid allocation backfires because mutating old-generation objects costs more than fresh allocation.

## Tools, libraries and specs
- HotSpot JIT (C1/C2 compilers, speculative inlining, deoptimization)
- ZGC (generational moving collector) and Serial GC
- Caffeine (Java caching library) vs Moka (Rust caching library)
- TCMalloc, jemalloc, glibc ptmalloc (native allocators)
- JFR (Java Flight Recorder), eBPF
- Project Valhalla (value flattening in arrays)
- Zig, Andrew Kelley's vtable-boundary talk

## Who should watch
Java developers who want the performance rationale behind the JIT, GC, and JFR from the OpenJDK team, and anyone choosing between the JVM and a low-level language for a large evolving service. Skip if you already work on JVM internals (much of the mechanism will be familiar) or need hands-on tuning steps rather than design reasoning.

## Verdict
**8/10**: Design rationale from the OpenJDK side and a Java-vs-Rust measurement with its workload shown; held back by no live demonstration and nothing to take home.

**Novelty 2/2**

- **+** [28:39](https://youtu.be/vhDwy1eCXbs?t=1719) A GC-team colleague's Caffeine-vs-Moka experiment gives head-to-head numbers that a search for the subject does not return.
- **+** [33:19](https://youtu.be/vhDwy1eCXbs?t=1999) The FFI argument explains from the designers' side why low-level languages are structurally barred from moving collectors.
- **+** [48:29](https://youtu.be/vhDwy1eCXbs?t=2909) The Q&A explains from the runtime team's view why pooling objects backfires: mutating promoted old-generation objects costs the GC more than allocating fresh ones.

**Demonstrated 1/2**

- **·** [28:39](https://youtu.be/vhDwy1eCXbs?t=1719) An argument talk presenting a finished benchmark on slides has nothing to run live, so no on-screen demonstration was due.

**Measured 2/2**

- **+** [28:39](https://youtu.be/vhDwy1eCXbs?t=1719) The cache comparison slide states the workload (30M strings, 90% hit rate) and gives RAM, RPS, p50/p90/p99 and CPU for Java and Rust at 5K and 10K RPS.
- **·** [21:23](https://youtu.be/vhDwy1eCXbs?t=1283) The 20x speedup from a C++-to-Java switch rewrite is a colleague's report, and the 1-2% JFR overhead at [40:06](https://youtu.be/vhDwy1eCXbs?t=2406) comes with no method; neither carries the score.
- **−** [36:59](https://youtu.be/vhDwy1eCXbs?t=2219) The allocator SLOC table rests on AI-supplied numbers the speaker says he did not check.

**Depth 2/2**

- **+** [19:49](https://youtu.be/vhDwy1eCXbs?t=1189) Speculative inlining with deoptimization is explained end to end, including warm-up cost and worse worst cases than C++.
- **+** [30:41](https://youtu.be/vhDwy1eCXbs?t=1841) Bulk freeing, headroom that scales with allocation rate rather than data size, and the RAM-for-CPU exchange explain why moving collectors win.
- **+** [25:33](https://youtu.be/vhDwy1eCXbs?t=1533) Profile-guided AOT is weighed against JIT speculation on correctness guarantees and binary size.

**Reusable 1/2**

- **·** [43:46](https://youtu.be/vhDwy1eCXbs?t=2626) The four tips for runtime authors are practices to reconstruct, and the talk points to no repository, sample or checklist.
