---
title: Escaping Java's Allocation Gravity with Value Classes
talkId: "17794"
conference: devoxx-be-2026
speakers: [Clément de Tastes, Remi Forax]
track: Java Language & Platform
sessionType: Conference
audienceLevel: ADVANCED
video: https://www.youtube.com/watch?v=lUB15M3mMLs
durationMin: 51
slides: https://github.com/CodeSimcoe/blackhole-devoxx
verdict: 9
reach: broad
frames: 9
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Escaping Java's Allocation Gravity with Value Classes
Clément de Tastes, Remi Forax · Conference · Java Language & Platform
Slides: https://github.com/CodeSimcoe/blackhole-devoxx

## TL;DR
Project Valhalla's value classes give Java classes primitive-like performance: no identity, no header, passed by value. A black-hole ray tracer rendered with identity versus value classes shows the same wall-clock time but allocation dropping from 10.7 GB to 316 MB and GC pauses disappearing once the JIT scalarizes the objects.

## Key takeaways
- Declare small immutable data carriers as `value` classes or records to get encapsulation with tuple-like runtime representation; the VM may scalarize them into registers and skip heap allocation entirely.
- For value objects `==` compares field by field, the default `hashCode()` is derived from the fields, and `synchronized` or `WeakReference` on them throws because there is no identity to lock on or point at.
- Value classes require strict initialization: every field must be assigned before the `super()` call, which Java 25 flexible constructor bodies make possible; existing constructors written the old way will not compile.
- Heap flattening of value fields is limited by atomicity: a flattened reference must fit in 64 bits minus a null marker, so a three-double vector stays a pointer while a three-byte one can flatten.
- JDK 28 retrofits `Integer`, `Long`, `Optional`, and most of `java.time` as value classes, so code that synchronizes on or identity-compares those types will break; heed the value-based-class warnings issued since JDK 16.

## Notes

### [00:35](https://youtu.be/lUB15M3mMLs?t=35) Valhalla: healing the primitive/object seam
Forax frames Valhalla as a language-plus-VM co-evolution led by Brian Goetz and John Rose, started in 2014 and large enough that the first pull request alone spans almost 3,000 commits across 2,000 files. Its three goals are zero-cost abstraction, dense flat memory layout now that cache locality matters more than in 1995, and rehabilitating primitives so `ArrayList<int>`-style code can one day work. The motto to take home: code like a class, work like an int.

### [05:56](https://youtu.be/lUB15M3mMLs?t=356) The cost of the object model
De Tastes walks through the current layout: an array of objects is an array of pointers to headers plus payload, wasting space on headers and padding and forcing pointer chasing with cache misses. The ideal is a flat representation with values encoded inline. Primitives already get that layout but are second-class citizens: no methods, no generics, and the `==` versus `equals()` split that confuses beginners.

### [10:36](https://youtu.be/lUB15M3mMLs?t=636) JEP 401 lands in JDK 28
The first Valhalla brick, JEP 401, introduces value objects as a preview feature in JDK 28 (March release), available now in the 28.30 early-access build with working IntelliJ support. Everything shown is preview or experimental and may still change.

### [13:46](https://youtu.be/lUB15M3mMLs?t=826) The value object mental model
A value class is a class whose instances are used as values, not pointers: think of them as tuples of their fields, passed and returned by value. Giving up the memory address (identity) means giving up mutation, so all fields and the class are implicitly final; `new Point(x, y)` conceptually builds the tuple rather than allocating. The VM is free to use a pointer when the object is large, and only small data structures win.

### [19:37](https://youtu.be/lUB15M3mMLs?t=1177) Live demo: equality, hashCode, synchronization
In the IDE, de Tastes adds `value` to a `Vec3` class and shows `Class::isValue` returning true, then two distinct `new Vec3` instances with equal fields comparing `==` as true because the VM checks field by field (refusing to compile was rejected as not backward compatible). The default `hashCode()` agrees for both instances since HotSpot derives it from the fields when there is no header to stash a random id in. `synchronized` on a value instance fails at compile time and, when smuggled through an `Object` variable, throws an identity exception at runtime; `WeakReference` fails the same way, which threatens `WeakHashMap`-as-cache idioms.

### [28:32](https://youtu.be/lUB15M3mMLs?t=1712) Strict initialization and flexible constructors
Because a value object must never observably change state, all fields must be initialized before `super()` runs; calling `super()` first exposes default values and is a compile error. JEP 513 flexible constructor bodies (Java 25) allow moving the `super()` call after field initialization, and the demo shows the compiler error when the old order is kept. Forax notes this initialization puzzle is a large part of why Valhalla took so long. Value classes can implement interfaces and extend abstract classes marked `value` (meaning value-enabled, with a reordered constructor), as shown in a `Vector`/`AbstractVector` demo.

### [34:46](https://youtu.be/lUB15M3mMLs?t=2086) Fields, arrays, and the atomicity ceiling
Storing a value object in a field or array only flattens when the VM can read and write it atomically in one 64-bit operation, and a null marker eats part of that budget, leaving 56 bits of payload. A `Vec3` of three doubles (192 bits) therefore stays behind a pointer, while a three-byte `Vec3` fits and flattens with a null flag per element. Flattening is a HotSpot optimization decision, not a guarantee.

### [38:29](https://youtu.be/lUB15M3mMLs?t=2309) Black-hole ray tracer and the benchmark
The showcase renders a black hole by casting one ray per pixel (about 2M rays for HD) through ~100 spacetime-curvature steps, creating around 200M `Vec3` instances modeled as `Ray`, `Vec3`, and `Color` records. The JMH benchmark runs identical code with and without `value`: 52,593 ms/op identity versus 48,566 ms/op value, essentially the same wall time. The difference is allocation: 2,022 MB/s and 128 GC events for identity, 4.15 MB/s and zero GC events for value, because G1 reclaims short-lived objects on other threads so efficiently that the single measured thread sees no speedup.

### [42:38](https://youtu.be/lUB15M3mMLs?t=2558) JFR: 10.7 GB versus 316 MB
JFR recordings make the gap visible: the identity run allocates 10.7 GB of `Vec3` (99.8% of all allocation) with the GC constantly reclaiming, while the value run allocates 316 MB almost entirely before the JIT kicks in, then flatlines. Scalarization is a JIT optimization, so interpreted iterations still allocate until compiled code loads the fields straight into registers. The point is not raw speed, which hand-written primitives could match, but readable encapsulated domain code at primitive performance: a three-line vector expression versus a page of `velX`/`velY`/`velZ` arithmetic.

### [47:18](https://youtu.be/lUB15M3mMLs?t=2838) JDK changes and the compiler story
In JDK 28 with preview enabled, `Integer`, `Long`, `Float`, `Double`, `Optional` variants, and most `java.time` classes become value classes, so `==` works for all integers and the `Integer` cache disappears. Compiling a value class only clears the `ACC_IDENTITY` bit and marks fields `ACC_STRICT_INIT`; bytecode is otherwise unchanged, so old compiled callers keep working, with an optional `LoadableDescriptors` attribute asking the VM to load value classes early for better layout. The skipped final demo and the roadmap slides (null-restricted types, enhanced primitive boxing, parametric JVM) point at the later Valhalla stages.

## Tools, libraries and specs
- JEP 401 (Value Classes and Objects, preview in JDK 28)
- JEP 513 (Flexible Constructor Bodies, Java 25)
- JEP 539 (compiler/VM work: ACC_IDENTITY, ACC_STRICT_INIT, LoadableDescriptors)
- JEP 390 (warnings for value-based classes, JDK 16)
- JDK 28 early-access build 28.30 with IntelliJ support
- JMH (avgt mode) and JDK Flight Recorder for the benchmark and allocation recordings
- Demo repository: https://github.com/CodeSimcoe/blackhole-devoxx (sources, slides, JFR files)

## Who should watch
Java developers curious about Valhalla or performance-sensitive numerical code gain a working mental model plus numbers; the ADVANCED internals (flattening limits, strict init, header mechanics) reward experienced JVM users most. Skip if you already follow the Valhalla design notes closely or need stable APIs rather than preview features.

## Verdict
**9/10**: Value-class semantics shown live, compared with JMH/JFR and explained through JVM constraints, with a reproducible demo project; the novelty is an application of the documented model and the timings cover only the benchmarked thread.

**Reach broad**: Most of the conference audience develops Java applications and can use the value-class model when JDK support arrives, including through the planned Integer, Optional and java.time retrofits.

**Novelty 1/2**

- **+** [45:45](https://youtu.be/lUB15M3mMLs?t=2745) The speakers illustrate the known zero-cost-abstraction goal with their own ray-tracer coding choices, contrasting encapsulated vector operations with expanded primitive arithmetic.

**Demonstrated 2/2**

- **+** [19:37](https://youtu.be/lUB15M3mMLs?t=1177) The live IDE session executes the new semantics end to end: `isValue` returns true, equal `Vec3` instances compare `==` as true with matching default hash codes, and synchronization produces compiler and runtime errors.
- **+** [31:09](https://youtu.be/lUB15M3mMLs?t=1869) Moving `super()` before field initialization produces the strict-initialization compiler error in the IDE demonstration.

**Measured 2/2**

- **+** [40:02](https://youtu.be/lUB15M3mMLs?t=2402) The same-code identity/value JMH comparison reports avgt with five observations and error bounds: 52.593 ± 1.389 versus 48.566 ± 1.727 ms/op, alongside allocation-rate and GC-count baselines.
- **+** [42:38](https://youtu.be/lUB15M3mMLs?t=2558) The JFR comparison records 10.7 GB of `Vec3` allocation for identity against 316 MB for value, with the remaining value allocations occurring before JIT scalarization takes effect.
- **−** [41:37](https://youtu.be/lUB15M3mMLs?t=2497) The near-equal elapsed times measure the benchmarked thread and exclude GC work on other threads, so they do not quantify whole-system savings.

**Depth 2/2**

- **+** [35:16](https://youtu.be/lUB15M3mMLs?t=2116) The flattening ceiling follows from atomic reference reads and writes plus space for a null marker, explaining why three doubles remain behind a pointer while three bytes can flatten.
- **+** [31:39](https://youtu.be/lUB15M3mMLs?t=1899) Strict initialization is explained as preventing observation of changing field values during construction, requiring field initialization before the superclass constructor runs.

**Reusable 2/2**

- **+** [50:58](https://youtu.be/lUB15M3mMLs?t=3058) The closing slide links https://github.com/CodeSimcoe/blackhole-devoxx, containing the semantics examples, ray-tracer source, benchmark and identity/value JFR recordings.
