---
title: "Teaching an Old Handle New Tricks: From Core Reflection to FFM"
talkId: "21666"
conference: devoxx-be-2026
speakers: [Maurizio Cimadamore, Viktor Klang]
track: Java Language & Platform
sessionType: Conference
audienceLevel: ADVANCED
video: https://www.youtube.com/watch?v=4ck-T2gaMQ4
durationMin: 52
slides: null
verdict: 6
reach: niche
frames: 11
summarizedAt: 2026-10-14
reviewedAt: 2026-10-15

# Teaching an Old Handle New Tricks: From Core Reflection to FFM
Maurizio Cimadamore, Viktor Klang · Conference · Java Language & Platform

## TL;DR
Method handles separate linkage from execution ("link once, execute many"), which is why they outperform core reflection and why the JDK builds string concatenation, the Foreign Function & Memory API, and an experimental marshalling framework on them. Two Oracle engineers trace that one design decision through four generations of platform features and argue it is a model for how to add lasting capabilities to Java.

## Key takeaways
- Core reflection pays for boxing, a caller access check, and unboxing on every call; a method handle does the access check once at creation and `invokeExact` avoids boxing, reaching near parity with a direct call.
- The JVM already splits invocation into linkage (resolve, check access, stash the vtable index) and execution; APIs that respect that split get faster, because work done once never sits on the hot path.
- Java 9+ string concatenation compiles each distinct shape into specialized bytecode behind a method handle (via `makeConcatWithConstants`), roughly doubling its speed over the old `StringBuilder` chains.
- An FFM downcall handle points at generated assembly selected by the platform ABI at creation time, so calling native code from Java is an `invokeExact` with the target address already bound.
- Method-handle combinators compose like Lego but generate bloated bytecode behind the scenes; the JDK teams migrated string concatenation, FFM, and string templates toward generating one specialized class with the Class-File API instead.

## Notes

### [02:39](https://youtu.be/4ck-T2gaMQ4?t=159) Reflection: an easy API with a costly invocation path
Cimadamore opens with the familiar `Class.getMethod("translate", ...)` plus `Method.invoke(point, x, y)` on a `Point` record. Under the hood (as of Java 17), every call boxes the `int` arguments into `Integer`s, packs them into an `Object[]`, runs an access check through the `@CallerSensitive` machinery that asks "who is calling me", then unboxes again before reaching the target. The benchmark chart shows a reflective call at about one third the throughput of a direct call. The diagnosis: reflection blurs linkage and execution, redoing static work per invocation.

### [06:48](https://youtu.be/4ck-T2gaMQ4?t=408) Link once, execute many: method handles
`javac` emits `invokevirtual Point.translate(II)LPoint;`, and the JVM links it once (load classes, resolve, check access, stash the vtable index) so execution stays cheap. A method handle, added in Java 7 alongside `invokedynamic`, is an encapsulation of an already-linked invocation: it carries a type, a kind (static, virtual, special), and access rights established once through a `Lookup` object, which makes it a capability. Creation looks like `MethodHandles.lookup().findVirtual(Point.class, "translate", MethodType.methodType(Point.class, int.class, int.class))`, and `invokeExact` is a polymorphic-signature method: `javac` burns the call-site static types and the return-type cast into the bytecode, so nothing is boxed. The only per-call cost is a type check, usually a pointer comparison against a `static final` handle. The updated chart puts `invokeExact` nearly level with a direct call. Java 18 then rebased core reflection itself on method handles (JEP 416, Mandy Chung), so plain `Method.invoke` reuses the same C2 optimizations and jumps to near parity too.

### [15:08](https://youtu.be/4ck-T2gaMQ4?t=908) String concatenation as specialized bytecode
Pre-9 concatenation compiled to `StringBuilder` chains that mix static recipe text with dynamic arguments and even undersize the default 16-char buffer for a 21-char constant recipe, forcing resizes. Since Java 9, `javac` emits an `invokedynamic` bootstrapped by `makeConcatWithConstants`, passing the dynamic-argument types plus a recipe string marking argument slots. The resulting handle points at bytecode generated for that exact shape: it folds the constant prefix (base length, coder for LATIN1 vs UTF16), adjusts for the dynamic arguments, allocates one right-sized `byte[]`, fills it at statically known offsets, and returns the string. Concatenation got roughly twice as fast from Java 8 to 9 (Aleksey Shipilёv credited). The same recipe idea was meant to generalize into string templates (JEP 456, withdrawn but still hoped for).

### [21:56](https://youtu.be/4ck-T2gaMQ4?t=1316) FFM downcall handles: handles that point at assembly
A downcall handle points at no Java bytecode at all, only a generated assembly trampoline that shuffles arguments into the registers the platform ABI demands. Building one needs the function address (via `SymbolLookup`) and a `FunctionDescriptor` of memory layouts; the linker runs ABI classification once at creation. Most users never touch this directly: `jextract` turns a C header into a wrapper class whose static method just calls `invokeExact` on a cached handle.

```java
// from slide at 25:30
static final MethodHandle TRANSLATE =
    Linker.nativeLinker().downcallHandle(
        SymbolLookup.loaderLookup().findOrThrow("translate"),
        FunctionDescriptor.ofVoid(C_POINTER, C_INT, C_INT));

static void translate(MemorySegment point, int dx, int dy) {
    TRANSLATE.invokeExact(point, dx, dy);
}
```

Inside the handle, a small bytecode stub unwraps the `MemorySegment` parameters to raw addresses ("adapt at the boundary") and jumps to a native `callNative0` whose target address is a linkage-time constant.

### [28:09](https://youtu.be/4ck-T2gaMQ4?t=1689) Marshalling: a serialization successor built on handles
Klang presents his experimental marshalling framework: each type maps to a versioned schema record (a `Point` maps to `PointV1`), and a `Marshaller` learns the schema, then receives the components. Hand-writing marshal/unmarshal pairs for thousands of classes is infeasible, and a naive reflective `marshal()` rediscovers schemas, looks up constructors and accessors, and dispatches on types on every single call. The link-once version derives a marshal handle and an unmarshal handle per type the first time it is seen and caches them in a schema map, keeping the hot path lean while getting finer-grained access control than reflection through lookups. His benchmark chart shows marshalling a `Point` at 173 ops/ms reflective versus 24,068 ops/ms with handles (self-described as not fully scientific). With Project Leyden, the one-time specialization could move to training time, so runtime pays neither the linkage cost nor code for types never marshalled.

### [42:06](https://youtu.be/4ck-T2gaMQ4?t=2526) Q&A: templates, combinators, Babylon, serialization
Asked for the next problem this pattern should attack, Klang points at the method-handles-meets-Leyden intersection unlocking earlier initialization, while Cimadamore names string templates: first pass selects validation logic from the template shape (linkage), second pass applies it to dynamic values. On where handles were not the answer, both say combinator chains: easy to start with, but they hide generated bytecode bloat, and every major user graduated to emitting one specialized class via the Class-File API (ASM before it). Project Babylon may invert handle construction from bottom-up assembly to writing the desired code against a code model and asking for a handle. On serialization's flaws (broken encapsulation, self-describing streams), Klang answers that marshalling demands explicit contracts plus expected-type allowlists, so a reader stating `String.class` up front already removes most of the attack surface.

## Tools, libraries and specs
- Method Handles and `invokedynamic` (Java 7): typed, pre-linked invocation capabilities with `Lookup`-based access control
- JEP 416 (JDK 18): core reflection reimplemented on top of method handles
- `StringConcatFactory.makeConcatWithConstants` (Java 9+): per-shape concatenation bytecode behind `invokedynamic`
- JEP 456: String Templates (withdrawn proposal, same recipe machinery)
- Foreign Function & Memory API: downcall handles, `Linker`, `SymbolLookup`, `FunctionDescriptor`, memory layouts
- jextract: generates Java wrappers with cached downcall handles from C headers
- Class-File API: JDK bytecode generation that replaced combinator chains and ASM in these features
- Project Leyden: training-time linkage to remove specialization cost from production startup
- Project Babylon: code models as a future front end for building method handles

## Who should watch
Java developers who use records, the FFM API, or serialization and want to understand the runtime machinery underneath, plus anyone designing frameworks that do reflective dispatch. Skip it if you already build with method handles and combinators daily; the Q&A's Babylon and Leyden remarks are the only new material for you.

## Verdict
**6/10**: JDK authors' design rationale and mechanism-level explanations carry it; nothing runs on screen and neither benchmark chart shows its setup.

**Reach niche**: Framework and library authors and teams writing FFM or reflective-dispatch hot paths can apply the link-once pattern; typical business-application teams meet method handles only indirectly through string concatenation and generated wrappers.

**Novelty 2/2**

- **+** [46:22](https://youtu.be/4ck-T2gaMQ4?t=2782) Both speakers report that every JDK user of method handles started with combinator chains and graduated to one generated class per use, which is authors' experience no search gives.
- **+** [44:18](https://youtu.be/4ck-T2gaMQ4?t=2658) The withdrawn string-template design gave the JDK hooks that third-party processors could not use, a limit stated by the people who built it.
- **+** [14:37](https://youtu.be/4ck-T2gaMQ4?t=877) Separating static from dynamic parts of a computation is presented as one pattern ("link once, execute many") running through reflection, string concatenation and FFM, a synthesis across features that no single doc page offers.

**Demonstrated 0/2**

- **−** [09:24](https://youtu.be/4ck-T2gaMQ4?t=564) The `findVirtual` plus `invokeExact` construction is walked through on slides and never run.
- **−** [19:19](https://youtu.be/4ck-T2gaMQ4?t=1159) The generated concatenation code is a simplified sketch ("not literally the code that is generated by the JDK"), not output from a run.
- **−** [31:49](https://youtu.be/4ck-T2gaMQ4?t=1909) The marshalling code is shown as "only hypothetical code" and no run follows.

**Measured 1/2**

- **+** [05:45](https://youtu.be/4ck-T2gaMQ4?t=345) The Java 17 chart compares `Method::invoke` at 137 M ops/s with a direct call at 395 M ops/s.
- **+** [37:05](https://youtu.be/4ck-T2gaMQ4?t=2225) The marshalling chart compares reflection-based and handle-based throughput on the same `Point` workload: 173 vs 24,068 ops/ms.
- **−** [36:38](https://youtu.be/4ck-T2gaMQ4?t=2198) The speaker calls the comparison "not super scientific" and says the absolute numbers "are not super important at all"; no benchmark setup is shown for either chart.

**Depth 2/2**

- **+** [09:56](https://youtu.be/4ck-T2gaMQ4?t=596) The `invokeExact` mechanism is explained down to `javac` burning call-site types into the descriptor and the remaining check collapsing to a pointer comparison.
- **+** [23:28](https://youtu.be/4ck-T2gaMQ4?t=1408) Platform ABI classification (which arguments go in registers, in which order, versus on the stack) is given as the reason a downcall handle needs a generated assembly trampoline.
- **+** [27:08](https://youtu.be/4ck-T2gaMQ4?t=1628) Inside a downcall handle, a bytecode stub unwraps `MemorySegment` parameters to raw addresses before jumping to a native target bound at linkage time.

**Reusable 1/2**

- **+** [25:30](https://youtu.be/4ck-T2gaMQ4?t=1530) The downcall slide shows the `downcallHandle` setup with `SymbolLookup` and `FunctionDescriptor` plus the `invokeExact` wrapper, a fragment to adapt for another native function.
- **·** [28:09](https://youtu.be/4ck-T2gaMQ4?t=1689) The marshalling framework is exploratory work with no repository or artifact named, so its half of the talk leaves only the pattern.
