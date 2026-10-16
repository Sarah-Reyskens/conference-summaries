---
title: Will Valhalla Fix Tony's Billion-Dollar Mistake?
talkId: "15354"
conference: devoxx-be-2026
speakers: [José Paumard, Rémi Forax]
track: Java Language & Platform
sessionType: Deep Dive
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=vLDbzmiT7Xs
durationMin: 161
slides: https://speakerdeck.com/josepaumard/will-valhalla-fix-tonys-billion-dollars-mistake
verdict: 8
reach: broad
frames: 11
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Will Valhalla Fix Tony's Billion-Dollar Mistake?
José Paumard, Rémi Forax · Deep Dive · Java Language & Platform
Slides: https://speakerdeck.com/josepaumard/will-valhalla-fix-tonys-billion-dollars-mistake

## TL;DR
Valhalla's value classes arrive as a preview in JDK 28: classes that give up object identity so the JVM can scalarize them into registers and flatten them in arrays. Across live demos, JMH benchmarks and JFR traces, Paumard and Forax show what changes in the language (reversals of `==`, constructors, synchronization) and where the performance wins and trade-offs really are. The answer to the title question is no: null survives, and null-restriction had to be spun out as future work.

## Key takeaways
- A value class is declared with a `value` modifier and used exactly like a class; the JVM may then scalarize instances into registers (no allocation, no GC) and flatten them in arrays.
- `==` on value objects compares field by field recursively, so it is no longer cheap; stop using it as a fast path, including inside `equals`.
- You cannot `synchronized` on or create a `WeakReference` to a value object; audit libraries that synchronize on `Integer` or cache through `WeakHashMap` before running JDK 28 with preview enabled.
- Heap flattening only applies to value payloads of 56 bits or less (8-bit null marker plus a 64-bit atomic read), and flattened arrays can be slower for small sizes because every read pays shift-and-mask decoding.
- Value classes are a JIT optimization over unchanged bytecode, so existing binaries benefit without recompiling; recompiling only adds the `LoadableDescriptors` attribute that helps the JVM flatten fields earlier.
- Type erasure hides value types from the JIT inside generics, so streams of value objects get none of the scalarization benefit until generics are specialized.

## Notes

### [00:46](https://youtu.be/vLDbzmiT7Xs?t=46) Tony's mistake and the JDK 28 early-access builds
Tony Hoare's 2009 apology for the 1965 null reference frames the session: null violations cost on the order of a billion dollars, and the talk asks whether Valhalla repairs that. The practical news is that JEP 401 (value objects) is a preview feature in the JDK 28 early-access builds on jdk.java.net, rebuilt weekly, which supersede the stale standalone Valhalla early-access builds from March 2026. A companion JVM-side JEP 539 covers strict field initialization. The JEP 401 merge itself was 2,934 commits, roughly twice the size of the Loom integration, and motivated a separate Devoxx talk by Doug Lea's colleague David Simms on Friday.

### [09:10](https://youtu.be/vLDbzmiT7Xs?t=550) The primitive/object divide and Valhalla's goals
Java keeps primitives (used directly, CPU and GPU friendly) strictly apart from objects (used through references, with pointer chasing and cache misses on every hop). JEP 401 aims to bring primitive benefits to classes: flatter, denser memory layouts, user-defined primitive-like types such as float16/float8 for GPU and AI work, and compatible migration of value-based classes like `Integer`, `LocalDate` and `Duration`. Healing the reference/primitive divide and specializing generics (`List<int>`) are explicitly longer-term goals, not part of this delivery.

### [18:00](https://youtu.be/vLDbzmiT7Xs?t=1080) Identity is an address; no address means no mutation
The core derivation: an object's identity is its address in memory, only one copy of an object can exist, and mutation requires knowing that address. Giving up identity therefore means giving up the 64-bit object header (class pointer, GC info, locking, identity hash code) and giving up mutability entirely: fields and the class are effectively final without needing the keyword. A `Song` record diagram walks through references, string headers and padding, including the note that compact headers (JEP 450, default in JDK 27) already shrank every object's header. The payoff preview: an identity-free object starts behaving like a primitive value such as `3`.

### [35:18](https://youtu.be/vLDbzmiT7Xs?t=2118) Declaring a value class
A value class is an ordinary class with `value` in front, usable as a record too, and instantiated with plain `new`:

```java
// from published slides p.27
value record Song(String title, short duration) {}
var beatIt = new Song("Beat it", 256);
```

The programming model is unchanged, but `new` no longer promises a heap allocation: the JVM may keep several copies, one copy, or no copy at all. Two consequences follow: value objects have no header, and every address-based operation (`==`, identity hash code, locking, weak references) needs reinterpreting.

### [38:25](https://youtu.be/vLDbzmiT7Xs?t=2305) Live demos: ==, hashCode, synchronized, weak references
Running on JDK 28 EA in IntelliJ, Forax shows that two equal value records compare `==` as true because the operator now recurses field by field (and returns false when the `title` fields are distinct `String` instances). The default `hashCode` becomes field-derived, so two playlists over the same array hash identically. `synchronized` on a value record fails compilation for lack of header lock bits, and casting through `Object` to dodge the compiler throws `IdentityException` at runtime (to be renamed). A `WeakReference` to a value record compiles but throws the same exception, which endangers the `WeakHashMap`-as-cache idiom found in many libraries.

### [53:09](https://youtu.be/vLDbzmiT7Xs?t=3189) Strict initialization and flexible constructors
Java constructors expose field mutation mid-construction (printing `this` before assignment shows `Title: null`, even for final fields), which value objects forbid since there is no address to mutate. The fix is strict initialization: all fields assigned before `super()`, with the compiler appending the `super()` call at the constructor's end and rejecting any `this` reference before it. JEP 513 flexible constructor bodies (final since JDK 25) already allow this style, and the speakers recommend writing all constructors that way to stop leaking partially initialized `this`, especially in concurrent code. Value classes carry no field-type restrictions: a field may be another value object, a primitive, an identity object, or even a mutable one, though that weakens the design.

### [68:51](https://youtu.be/vLDbzmiT7Xs?t=4131) Abstract value classes
A value class may only extend an abstract value class or `Object`; extending a plain abstract class is a compiler error cured by adding `value` to the parent. For abstract classes the keyword means value-enabled: its constructors follow the strict-initialization protocol so subclass state stays optimizable. `Record` and `java.lang.Number` are already abstract value classes, which is how `Integer` and friends can migrate later. Identity classes remain free to extend abstract value classes.

### [74:36](https://youtu.be/vLDbzmiT7Xs?t=4476) Scalarization on stack: the mixtape benchmarks
The benchmark setup pairs `ValueSong`/`ValuePlayList` records against identical identity records, summing song durations three ways over 100-song arrays: V1 imperative over shorts, V2 allocating a new song per loop iteration, V3 `Stream.reduce`. For identity classes the scores are V1 33, V2 190, V3 191 ns/op; switching to value classes (no array flattening yet) gives 33, 33 and 196 ns/op, so object allocation becomes exactly as cheap as primitives. The JMH GC counters explain the hidden win over 500 ms runs: identity V1/V2/V3 trigger 70/138/122 collections costing 43/110/93 ms, while value V1/V2 trigger zero collections and zero milliseconds because the JIT destructures songs into register-held `(String, short)` tuples, including parameters and return values. Streams keep their 19 collections and 16 ms.

### [87:09](https://youtu.be/vLDbzmiT7Xs?t=5229) Why streams don't benefit: erasure
Generics erasure replaces every `T` with `Object`, so the JIT sees a stream of `Object` rather than a stream of songs and none of the value optimizations apply. Discovering the type late in generated assembly is not enough; the optimization must hold along the whole pipeline. True specialized generics would fix this, but the speakers warn that retrofitting them onto twenty years of user casts is far off, with only prototypes existing.

### [90:52](https://youtu.be/vLDbzmiT7Xs?t=5452) Flattening on heap: layout and the 56-bit limit
Where scalarization explodes objects into registers, flattening packs values inline in heap arrays: a `Song[]` stores each title reference, short duration, padding and a `1` marker per cell instead of pointers to headed objects. The 8-bit null marker records whether each cell is null, since references to value objects stay nullable. Two constraints then bite: heap reads and writes must be atomic, and 64-bit CPUs read 64 bits at once, leaving 56 bits of payload. That is why the demo uses `short` durations: a 32-bit reference plus a 32-bit `int` exceeds the budget and disables flattening (scalarization still applies).

### [103:22](https://youtu.be/vLDbzmiT7Xs?t=6202) Flattened benchmarks: denser but not always faster
With array flattening forced on, the same 100-song runs score V1 49, V2 53 and V3 2611 ns/op: slower than the unflattened 33/33/196 because each read must shift-and-mask the packed 64 bits, and the stream case additionally boxes every song back to `Object`. Scaling the array size flips the picture: flattened wins clearly from 100,000 songs upward (51.3 vs 79.9 µs/op) and dominates at one million (507 vs 2710 µs/op), as pointer chasing and cache pressure overwhelm decode cost. The deck's guidance is that flattening guarantees denser storage and no extra dereferencing, but the last two benefits are muted on the JVM because moving collectors already colocate hot objects.

### [110:19](https://youtu.be/vLDbzmiT7Xs?t=6619) JFR on a real application; value classes as JIT optimization
A wall-clock JFR comparison shows identity objects allocating almost 2 GB of `Song` data with frequent red GC pauses, against under 3 MB for value objects with allocation and GC stopping entirely after warmup (the flattened array itself doubles from 76 MB of 32-bit pointers to 64-bit cells). The mechanism: the interpreter still uses pointers, and only the JIT (C1/C2) removes allocation and indirection when lowering bytecode. Because the bytecode for using a value class is identical to using an identity class, existing compiled code benefits without recompilation.

### [117:12](https://youtu.be/vLDbzmiT7Xs?t=7032) Classfile mechanics and retrofitted JDK classes
`javac` marks a value class by clearing the class file's `ACC_IDENTITY` bit and setting `ACC_STRICT_INIT` on every field. One subtlety is lazy class loading: a field's type class may never load (it could stay null), so the JVM cannot know it is a value class when laying out the object. The compiler therefore emits a `LoadableDescriptors` attribute listing classes to preload, which is the only benefit recompiling buys. Under `--enable-preview` on JDK 28, `@ValueBased` JDK classes are already value classes: `Optional`, most of `java.time`, and all primitive wrappers. That breaks code synchronizing on an `Integer` (warned since JDK 16, now an error), and `Optional` only optimizes when passed method-to-method rather than stored in fields or collections.

### [125:23](https://youtu.be/vLDbzmiT7Xs?t=7523) Preparing your code
Four rules close the JEP 401 part: write constructors with `super()` last per JEP 513, never use `==` on objects (it also poisons branch prediction in modern `equals` overrides), never synchronize on objects you do not own, and never build weak references to objects you do not own. The mantra for the whole feature is code like a class, works like an int. A library author in the audience asks when not to use value classes; the answer is when published instances escape to user code that might synchronize on them, which is harder to control than in an application.

### [130:19](https://youtu.be/vLDbzmiT7Xs?t=7819) Future: null-restricted types and primitive classes
HotSpot internally supports four flat layouts (atomic/non-atomic crossed with null-marker/null-free), and the expert group explored two ways to unlock the larger ones. Exploration 1, a `Song!` bang suffix for null-restricted fields, died: it needs new array-initialization syntax, breaks overload resolution at a distance when libraries add `!`, and conflates a storage decision with API types (a prototype branch with the bang still exists in the Valhalla repository). Exploration 2, primitive classes, would give up encapsulation so fields become independent: fully flattened, non-null on heap with a zero default value, though still nullable on stack for compatibility with null-returning APIs like `Map.get`. The open problem is the field/class handshake: turning an existing class primitive or back is a silently incompatible change, so both value and primitive classes would have to coexist permanently.

### [157:26](https://youtu.be/vLDbzmiT7Xs?t=9446) So will Valhalla fix the mistake?
Short answer: no. The JDK 28 roadmap is JEP 513 constructors (final in 25), JEP 401 value objects (preview) and JEP 539 strict initialization (preview); later come primitive classes with non-null fields, JEP 402 enhanced primitive boxing, type classes with operator overloading restricted to value/primitive classes, and a parametric JVM. The closing slide links the deck and the benchmark repository, and the last audience question (could primitive classes fail like the bang?) gets an honest yes: every exploration is an exploration.

## Tools, libraries and specs
- JDK 28 early-access builds (jdk.java.net) with `--enable-preview`: the only build containing the JEP 401 preview
- JEP 401 (value objects), JEP 539 (strict field initialization in the JVM), JEP 513 (flexible constructor bodies, final in 25), JEP 450 (compact object headers), JEP 402 (enhanced primitive boxing), JEP 218 (generics over primitive types)
- JMH (benchmark scores with GC profiler counters) and JDK Flight Recorder (allocation and GC traces)
- IntelliJ IDEA (already supports value classes, with strict-init diagnostics still lagging `javac`)
- Vector API incubator (already carries a float16 class awaiting Valhalla) and `github.com/forax/valhalla-demo` (slides, IDE demos and all mixtape benchmarks)

## Who should watch
Java developers deciding what Valhalla means for their code, performance engineers who want scalarization and flattening numbers with their trade-offs, and library authors who must audit synchronization and weak-reference usage before JDK 28. Viewers wanting usable `List<int>`, stable APIs, or a null-free Java should skip this: specialization is prototypes only, value classes are preview, and the talk's own answer is that null survives.

## Verdict
**8/10**: Live IDE demos of the `==`, synchronization and constructor changes, JMH series with baselines and error bars, an explained flattening budget and a published demo repository carry it; the optimization itself is never run on screen and the value-class core follows what the JEPs already say.

**Reach broad**: Most Java developers in the audience will meet value classes once JDK 28 ships, so the migration rules and flattening trade-offs transfer directly to their own code.

**Novelty 1/2**

- **+** [145:15](https://youtu.be/vLDbzmiT7Xs?t=8715) The expert group's outcome for null-restricted types is that `!` will not ship with value classes and may return later as a separate feature, a status a viewer would not get from the JEP pages.
- **−** The value-class semantics in the first half (identity, `==`, headers, strict fields) follow JEP 401 and JEP 539, and the speakers work on the project, so those pages are the search baseline.

**Demonstrated 1/2**

- **+** [41:01](https://youtu.be/vLDbzmiT7Xs?t=2461) Two equal value records compare `==` as true in the IDE on a JDK 28 early-access build and false once the titles become distinct `String` instances, with the console output visible.
- **+** [49:30](https://youtu.be/vLDbzmiT7Xs?t=2970) A `synchronized` block on a value record fails to compile, and a cast through `Object` to dodge the compiler throws `IdentityException` when the code runs.
- **−** [85:32](https://youtu.be/vLDbzmiT7Xs?t=5132) The VM's scalarized view of the code is a pseudo-code slide, so the central optimization claim is never run on screen.

**Measured 2/2**

- **+** [82:53](https://youtu.be/vLDbzmiT7Xs?t=4973) The JMH tables report identity against value versions of all three mixtape computations on 100-song arrays over 500 ms runs, with GC profiler counters at 70/138/122 collections for identity against none for value V1 and V2.
- **+** [106:37](https://youtu.be/vLDbzmiT7Xs?t=6397) Scaling the array from 100 to 1,000,000 songs sets flattened against pointer arrays with error bars: 54 against 33 ns/op at 100 songs, 51.3 against 79.9 µs/op at 100,000 and 507 µs against 2.71 ms at one million.
- **−** [78:44](https://youtu.be/vLDbzmiT7Xs?t=4724) Hardware and JVM flags go unstated since the runs are introduced only as done "on the machine".

**Depth 2/2**

- **+** [24:47](https://youtu.be/vLDbzmiT7Xs?t=1487) Identity derives from the object's memory address, which yields no address, no header and no mutability in one chain.
- **+** [100:47](https://youtu.be/vLDbzmiT7Xs?t=6047) The flattening budget drops from 64 to 56 bits because of the 8-bit null marker beside the single atomic 64-bit read, which is why an `int` duration disables flattening.
- **+** [118:47](https://youtu.be/vLDbzmiT7Xs?t=7127) Classes load lazily because a null field never needs them, so the VM cannot know a field's class is a value class at layout time, which motivates the new `LoadableDescriptors` attribute emitted on recompilation.

**Reusable 2/2**

- **+** [160:05](https://youtu.be/vLDbzmiT7Xs?t=9605) The closing slide points to github.com/forax/valhalla-demo, which holds the IDE demos, the mixtape benchmark sources and the JFR files.
