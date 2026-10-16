---
title: Java Next - From Valhalla to Leyden, from Babylon to Panama, from Amber to Detroit
talkId: "52101"
conference: devoxx-be-2026
speakers: [Nicolai Parlog]
track: Java Language & Platform
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=ufhs9THbYZI
durationMin: 52
slides: https://slides.nipafx.dev/java-next/2026-10-09-devoxx-be/
verdict: 6
reach: broad
frames: 5
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Java Next - From Valhalla to Leyden, from Babylon to Panama, from Amber to Detroit

Nicolai Parlog · Conference · Java Language & Platform

Slides: https://slides.nipafx.dev/java-next/2026-10-09-devoxx-be/

## TL;DR

Oracle developer advocate Nicolai Parlog tours the OpenJDK projects shaping Java's next years: Amber, Leyden, Valhalla and Babylon in depth, then Loom, Panama, Lilliput and Detroit in a closing speedrun. Each segment pairs the project's motivation and mechanics with a concrete timeline of what shipped in which JDK and what is still open. The talk leaves a working roadmap: value classes preview in JDK 28, AOT code compilation in JDK 28, structured concurrency likely finalizing in 28.

## Key takeaways

- Primitive patterns (JEP 530) let `instanceof` match primitives with lossless-conversion semantics, and they unblock constant patterns such as `case Point(0, _)`.
- Leyden's AOT cache is safe to try because a mismatched cache is ignored or partially used; the worst realistic outcome is a small deoptimization cost, never wrong behavior.
- Canary deployments are an ideal training-run source for the AOT cache since the profile comes from a real live run.
- Value classes trade identity for guaranteed immutability and optimization freedom; choose them when the type is value-ish in the domain, not to chase performance.
- The JVM cannot routinely flatten a `Long` because the null bit plus 64 value bits exceeds atomic write limits; null-restriction and generic specialization are the envisioned fixes.
- Compact object headers are default since JDK 27 and shrink heap use by roughly 10%, but watch for the rare case where decompression cost outweighs the gain.

## Notes

### [00:34](https://youtu.be/ufhs9THbYZI?t=34) Project Amber: expressive language features

Amber attacks Java boilerplate caused by missing expressiveness. Delivered work runs from local-variable type inference through records, sealed types and pattern matching, up to JDK 25 additions: unnamed variables and patterns, multi-file source launcher, simplified `main`, module imports and flexible constructor bodies. Current work centers on pattern matching: primitive patterns in preview (JEP 530), where `x instanceof float f` asks whether the conversion is lossless (16,777,217 is the smallest positive int that is not exactly representable as float); constant patterns, still strawman syntax with no JEP draft; and derived record creation ("withers", JEP 468):

```java
// from published slides ("Withers")
record Point(int x, int y) { }

var p0 = new Point(0, 0);
var p1 = p0 with { x = 1; };
```

Withers are blocked on the broader deconstruction story: deconstructible classes would widen the gray area between records and behavior-only classes via a state description in the class header, with interfaces possibly landing first since reconstruction questions disappear there. String templates remain an endeavor, and the speaker points to Inside Java podcast conversations with Maurizio Cimadamore and Gavin Bierman for depth.

### [10:24](https://youtu.be/ufhs9THbYZI?t=624) Project Leyden: shifting work ahead of time

Leyden splits slow Java launch into startup (launch to first useful work) and warmup (first work to peak performance), and shifts early work (class loading, linkage, interpretation, profiling, JIT compilation) ahead of time via training runs. A training run observes the JVM and captures decisions in an AOT cache; production runs start from it, falling back to live optimization where the profile does not match. The shortcut workflow skips the separate assembly phase:

```sh
# from published slides (AOT workflow)
$ java -XX:AOTCacheOutput=app.aot -cp app.jar com.example.App ...
$ java -XX:AOTCache=app.aot -cp app.jar com.example.App ...
```

Cache contents and their effects: class loading and linking (up to ~40% startup reduction on Spring PetClinic, ~130 MB cache), method profiling (~20% runtime reduction on a 100,000-iteration stream loop), GC-agnostic streaming of cached objects (JDK 26, any collector), and code compilation in JDK 28 (~15% startup reduction, ~75% fewer warmup iterations on javac). A normalized bar chart (Linux/x64, 2 cores) shows Helidon, Micronaut, Quarkus, Spring Boot and PetClinic all scoring far below the 1000 no-cache baseline with cache and cache-plus-code; a 20-iteration javac warmup curve shows the first iteration dropping from ~1.4 s without AOT to ~0.9 s with cache and ~0.3 s with compiled code, all converging to the same peak. Limits: same JDK, architecture and OS between training and production, plus same CPU features and GC for code compilation; JVMTI agents that weave bytecode at load time get the cache discarded, so prefer build-time weaving. Netflix's usage is cited with the caveat that Netflix scale is not required to benefit.

### [24:24](https://youtu.be/ufhs9THbYZI?t=1464) Project Valhalla: unifying the type system

Java's primitive/class split grew worse with generics, boxing and lambdas. Every class carries identity (header memory, mutability, locking) and every instance is a reference (indirection, nullability, since all 2^64 `long` bit patterns are taken and null needs the reference). Value classes, previewing in JDK 28, drop identity: `==` compares state recursively, synchronization throws, serialization needs a proxy, and null stays the default. JDK value classes out of the box include the primitive wrappers, `Number`, `Record`, the `Optional` family and the `java.time` classes. Custom ones need only the `value` modifier, with implicitly final fields and restricted superclasses. Optimizations stay the JIT's choice: escape analysis trivially succeeds so scalarization can pass fields in registers, while flattening encodes fields in the reference but needs a null bit and 64-bit atomic writes, which is why `Long` cannot flatten and why `Optional<T>` erasure blocks it. Follow-ups in flux: null-restriction (`ComplexNumber!`), specialized generics so `ArrayList<ComplexNumber>` backs onto a flat array, universal generics (`List<int>`), and type classes for operator use with user types (existing operators only, no custom symbols). The guidance is to let performance emerge from domain decisions rather than picking value classes for speed.

### [39:56](https://youtu.be/ufhs9THbYZI?t=2396) Project Babylon: Java for foreign programming models

Babylon extends Java to GPUs, FPGAs, SQL and differentiable programming without one-off per-target projects. Its mechanism is code reflection: an API that reaches into methods and lambdas to expose symbolic code models, designed as compiler-style intermediate representations (influenced by MLIR) sitting between the AST (too syntactic) and bytecode (too little information). The compiler stores the model in the class file, runtime code reads it via reflection and transforms it, and the ecosystem provides the back ends (OpenCL/CUDA kernels, Triton). A Triton vector-add kernel written in Java shows the payoff: debuggable, testable Java with familiar tooling that only becomes a GPU kernel when performance is needed, though the code must still bend to the accelerator's model. HAT (Heterogeneous Accelerator Toolkit) co-evolves as the GPU test bed. Status: a code-reflection incubator JEP is being polished, with no date given.

### [45:39](https://youtu.be/ufhs9THbYZI?t=2739) Project Speedrun: Loom, Panama, Lilliput, Detroit

Loom: virtual threads final in 21, scoped values final in 25, unpinning from object monitors (25) and class initialization (26); structured concurrency is in its seventh preview in 27 with a JEP proposed to finalize it in 28, making JDK 29 a plausible LTS-to-LTS jump for the full stack. Panama: foreign function and memory APIs final in 25, vector API still incubating (12th incubation in 27) because it waits on Valhalla value types to replace custom optimizations, with possible API revamps on the preview transition. Lilliput: 64-bit compact object headers opt-in since 25, default in 27, cutting heap use by about 5-20% (10% as a median) with possible GC and cache benefits against small decompression costs; 32-bit headers are an open JEP draft facing diminishing returns. Detroit (reestablished 2026): `javax.script` implementations for JavaScript on Chrome V8 and Python on CPython, with promising early prototypes and a dedicated Devoxx talk by Maurizio Cimadamore to watch instead.

## Tools, libraries and specs

- JEP 530 (primitive types in patterns), JEP 468 (derived record creation), JEP draft 8357464 (deconstruction assignment)
- JEP 483 (AOT class loading and linking), JEP 515 (AOT method profiling), JEP 516 (AOT with any GC), JEP 544 (AOT code compilation)
- JEP 401 (value classes and objects), JEP draft 8361105 (code reflection incubator)
- JEP 444 (virtual threads), JEP 499/533 (structured concurrency previews), JEP 506 (scoped values), JEP 491 (unpinned object monitors)
- JEP 454 (foreign function and memory API, final), JEP 537 (vector API, 12th incubator), jextract
- JEP 519/534 (compact object headers), JEP draft 8349069 (32-bit headers)
- Inside Java podcast, HAT (Heterogeneous Accelerator Toolkit), Triton

## Who should watch

Java developers who want a single current map of where the platform is heading, including which release trains to track for their next upgrade. Beginners get accessible mental models; experienced developers get status details (JEP numbers, preview rounds, limitations) worth checking against their own plans. Skip it if you already follow the individual projects closely or need a deep dive on any one of them; each segment ends with links to papers, JEPs and talks for that.

## Verdict

**6/10**: An OpenJDK roadmap supported by comparative Leyden benchmarks and runtime design explanations, limited by status-report novelty and runnable claims presented only on slides.

**Reach broad**: Most of the Devoxx BE audience develops Java applications and can use the language-feature and runtime-upgrade roadmap as these JDK changes ship.

**Novelty 1/2**

- **+** [02:39](https://youtu.be/ufhs9THbYZI?t=159) The survey combines project updates with pointers to the speaker's recorded Inside Java conversations with Cimadamore and Bierman.
- **+** [35:18](https://youtu.be/ufhs9THbYZI?t=2118) He revises his earlier expectation that almost all records would become value records and advises choosing value classes by domain meaning.
- **+** [45:39](https://youtu.be/ufhs9THbYZI?t=2739) The closing roadmap brings Loom, Panama, Lilliput and Detroit alongside the four projects covered earlier.

**Demonstrated 0/2**

- **−** [43:34](https://youtu.be/ufhs9THbYZI?t=2614) The Java-to-GPU claim is illustrated with Triton slide code without showing compilation, execution or output.

**Measured 2/2**

- **+** [18:43](https://youtu.be/ufhs9THbYZI?t=1123) The Linux/x64 two-core comparison uses framework hello-world workloads and PetClinic, normalizing each no-cache baseline to 1,000 against cache-only and cache-plus-code runs.
- **+** [19:46](https://youtu.be/ufhs9THbYZI?t=1186) A twenty-iteration javac warmup curve compares seconds per iteration without AOT, with cached profiles and with cached compiled code, showing first-iteration time fall from about 1.4 seconds to 0.9 seconds and then about 0.3 seconds.
- **−** [16:38](https://youtu.be/ufhs9THbYZI?t=998) The figures are introduced as disconnected benchmarks intended to suggest possible benefits, without run counts or variance.

**Depth 2/2**

- **+** [13:31](https://youtu.be/ufhs9THbYZI?t=811) Leyden's training-run explanation connects dynamic runtime decisions to cache reuse and explains why mismatches cause fallback or deoptimization rather than incorrect behavior.
- **+** [31:08](https://youtu.be/ufhs9THbYZI?t=1868) The flattening explanation connects nullability's extra bit to atomic-write limits and shows why a nullable Long cannot routinely flatten.
- **+** [42:01](https://youtu.be/ufhs9THbYZI?t=2521) Babylon's intermediate code model is justified against the AST's syntax dependence and bytecode's missing information, drawing on compiler IRs and MLIR.

**Reusable 1/2**

- **+** [15:05](https://youtu.be/ufhs9THbYZI?t=905) The AOT training, assembly and production workflow includes command fragments and a shortcut suitable for adapting to a build or canary pipeline.
- **+** [03:09](https://youtu.be/ufhs9THbYZI?t=189) Primitive-pattern slide code provides a preview-feature example, followed by proposed constant-pattern and wither syntax.
- **·** [50:17](https://youtu.be/ufhs9THbYZI?t=3017) The closing dev.java and Inside Java pointers provide further reading without a sample repository or checklist reproducing the examples.
