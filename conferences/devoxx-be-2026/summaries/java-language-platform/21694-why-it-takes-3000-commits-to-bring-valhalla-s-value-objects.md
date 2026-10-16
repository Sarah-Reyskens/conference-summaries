---
title: Why it takes 3000 commits to bring Valhalla's value objects to the JDK
talkId: "21694"
conference: devoxx-be-2026
speakers: [David Simms]
track: Java Language & Platform
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=D_AmK8-UnZg
durationMin: 51
slides: null
verdict: 7
reach: broad
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Why it takes 3000 commits to bring Valhalla's value objects to the JDK

David Simms · Conference · Java Language & Platform

## TL;DR

JEP 401 value objects reach JDK 28 as a preview, and the feature looks tiny from the outside: one `value` keyword that trades identity for efficiency. The talk then shows why that keyword cost a decade of work, touching javac, the class file format, the interpreter, both JIT compilers, and every HotSpot subsystem along the way.

## Key takeaways

- Adding `value` to a class makes fields implicitly final, drops identity (no locking, no identity hash), and redefines `==` as a field-by-field comparison.
- Fields must be fully initialized before the `super` call, enforced statically by the verifier, so construction needs no runtime checks afterward.
- Enabling preview in JDK 28 silently migrates all primitive wrapper classes to value classes, which can break old code that relies on their identity (weak references are the cited example).
- Flattening and scalarization are implementation choices, not spec guarantees: the VM may store payloads inline and keep fields in registers, or decline to, and other VMs may do neither.
- Do not tag huge or reference-heavy classes with `value` and expect a win; flattening stops paying off past roughly a cache line, and each embedded reference still needs GC barriers.
- Inspect what the VM actually did with `-XX:+PrintFieldLayout` and its two extra Valhalla flags rather than assuming a class was flattened.

## Notes

### [02:07](https://youtu.be/D_AmK8-UnZg?t=127) The rift between primitives and objects

Primitives hold data with no encapsulation while objects carry logic plus a costly header (8 or 16 bytes against an 8-byte payload in the Point example) and a pointer per array element. Modern memory hierarchies made that overhead hurt: a last-level cache miss costs hundreds or thousands of times a register add. Generics erasure is the visible symptom, since `List<int>` cannot exist while primitives and objects stay separate. Inside HotSpot, references ("oops") demand an access API because the GC can move objects or plant trap values in headers at any time.

### [05:44](https://youtu.be/D_AmK8-UnZg?t=344) JEP 401: the `value` keyword and its rules

JEP 401 (Value Objects) plus its construction story target JDK 28 as a preview, enabled with `--enable-preview` and source level 28. The whole user-facing change is the `value` keyword with two extra library calls: fields become implicitly final, identity is gone, non-abstract value classes are effectively final, and `==` compares every field instead of pointers. Flexible constructor bodies (already in the JDK) pair with strict field initialization: writes to fields are legal before `super`, frozen after, and passing `this` out before `super` is rejected.

### [10:50](https://youtu.be/D_AmK8-UnZg?t=650) First numbers and the silent wrapper migration

A contrived microbenchmark on the speaker's cloud instance gains 40% from the keyword alone, with an explicit warning not to extrapolate that to whole applications. More consequentially, preview mode auto-migrates every primitive wrapper to a value class, changing behavior of unmodified programs; the team validated against a large open-source corpus but asks for reports of breakage. Anecdotal upside: a Class-File API tool heavy on `Integer` runs about 20% better.

### [13:26](https://youtu.be/D_AmK8-UnZg?t=806) Timeline: 2014 prototypes to the 2026 merge

Project Valhalla started publicly in 2014 aiming at generic specialization and healing the primitive/object split; the speaker joined around 2015 for active prototyping. The LWorld branch was cut around 2019 with a design the team believed was 90% done, but the construction story (strict initialization, flexible bodies, lifecycle) only settled around 2024, and production-hardening took two more years. The merge into mainline landed right after the JDK 27 fork, in the early hours of July 31: nearly 3000 commits, 64 authors, 14 named reviewers, and far more people behind the scenes. One engineer merged mainline into the project branch weekly for over a decade; some weeks took half an hour, some took three months.

### [17:38](https://youtu.be/D_AmK8-UnZg?t=1058) Blast radius: language, javac, and every HotSpot subsystem

The change spans the language spec, the VM spec, javac, bytecode tooling (the team mid-project moved its own bytecode work from ASM to the Class-File API), class loading and the `Klass` type system, the interpreter, and the C1 and C2 compilers. Meanwhile the ground kept shifting under the branch: modules, application CDS and the AOT cache, virtual threads, and GC churn (CMS was removed mid-project). The merge itself touched essentially all of HotSpot: class loading, execution engine, memory, runtime, GC, serviceability, and CPU backends.

### [26:31](https://youtu.be/D_AmK8-UnZg?t=1591) Heap flattening: inline payloads with null markers

Giving up identity unlocks two VM optimizations: heap flattening (payloads stored contiguously in arrays instead of pointers) and scalarization. Flattening is purely an implementation choice; JEP 401 mandates neither it nor scalarization. A flat `LocalDate[]` stores year, month, day plus a null marker per element, since null stays in the language. Atomicity is the hard constraint: tearing a multi-byte value during a concurrent read is unacceptable, so a 64-bit `Point` plus its null marker already exceeds what plain instructions store atomically, while smaller payloads fit. A `LoadableDescriptors` class-file attribute tells the VM which classes may be values at load time; unknown classes simply do not get flattened, and the attribute can observably reorder class-loader requests.

### [34:53](https://youtu.be/D_AmK8-UnZg?t=2093) What flattening costs: loads, stores, and `if_acmp`

Every field and array load/store bytecode grew more complex, and the interpreter now buffers values in small heap holders (oops reused as containers), so interpreter-only runs can show extra allocation. The smallest example shown is `if_acmp`: once a single pointer comparison, it now sanity-checks that both operands are the same value type, then calls up into Java (`ValueObjectMethods`, heavily optimized by C2 but still an upward call) for the substitutability test. Default `equals` and `hashCode` walk all fields, so very wide value classes pay in proportion to their size. VarHandles ride along with the new load/store paths.

### [36:56](https://youtu.be/D_AmK8-UnZg?t=2216) Why the VM does not flatten everything

With nulls present by default, the current implementation declines to flatten cases like `Point`. Wider atomic instructions (128/256/512-bit) were considered but rejected: their alignment requirements would destroy the density story and add cache traffic. Experiments put the break-even near a cache line in moved bytes. Embedded references add GC barrier work per element, so a reference-heavy value can be cheaper left unflattened, especially when callers never touch most fields. `-XX:+PrintFieldLayout` plus two Valhalla flags reveal the chosen layout per class, including cases like "nullable non-atomic flat" for final fields that are written once.

### [42:11](https://youtu.be/D_AmK8-UnZg?t=2531) Scalarization: values as registers in C2

C2 already scalarizes regular objects but gives up the moment a value might escape or be mutated; value semantics (passed conceptually by value, immutable) let it keep components in registers and on the stack across calls instead. Supporting this took new sea-of-nodes IR, flat-array handling, and an entirely new calling convention that passes components in registers rather than a pointer, an investment so large the compiler team declared it could not be abandoned mid-project. Deoptimization boundaries still need buffered oops, so allocation can reappear where C2 frames meet the interpreter or C1. The Point-motion example shown gains nearly an order of magnitude with allocation fully removed.

```java
// from slide at 42:11
value record Point(int x, int y) {}
```

### [48:23](https://youtu.be/D_AmK8-UnZg?t=2903) Merge night and the road ahead

The final sync started around 1 a.m., the team held off check-ins, and the pull request went through Scarab bots and JCheck before landing. Retirees are credited among the authors. Preview count is open (Loom took about three); the team wants feedback from the JDK 28 early-access build. Possible futures include null-restricted and loosely-consistent value types, cheaper `equals`/`hashCode`, a canonical all-zeros instance, and de-duplication at substitutability tests, with the caveat that the language group may choose different directions.

## Tools, libraries and specs

- JEP 401 (Value Objects, Preview) targeting JDK 28
- Valhalla early-access builds of JDK 28 (`--enable-preview`, source level 28)
- Flexible constructor bodies and strict field initialization
- HotSpot subsystems: template interpreter, C1 and C2 JITs, `Klass` type system, `LoadableDescriptors` class-file attribute
- `-XX:+PrintFieldLayout` with the two Valhalla layout flags; `javap`
- ASM and the Class-File API (bytecode tooling used mid-project)
- OpenJDK PR #31120 (JEP 401 implementation, ~3000 commits)

## Who should watch

Java developers who have heard of Valhalla and want a beginner-friendly grounding in what value objects are, what they cost the VM, and what to try in JDK 28. JVM and performance engineers get the most from the flattening and scalarization internals. Skip it if you want a hands-on migration guide for existing codebases; this is the feature's concepts and construction story, not a porting cookbook.

## Verdict

**7/10**: First-hand Valhalla implementation history and VM design rationale, with partial on-screen demonstration and benchmark comparisons lacking a stated method.

**Reach broad**: Java application developers will meet value objects in a shipping JDK, including the primitive-wrapper migration when preview is enabled.

**Novelty 2/2**

- **+** [44:43](https://youtu.be/D_AmK8-UnZg?t=2683) The compiler team’s investment in the value calling convention made abandoning and rebuilding the project branch impractical, constraining how the team could finish the merge.
- **+** [22:52](https://youtu.be/D_AmK8-UnZg?t=1372) The team deliberately prototyped outside Java compatibility constraints and left null support out to keep exploration affordable.
- **+** [24:57](https://youtu.be/D_AmK8-UnZg?t=1497) The interpreter scalarization experiment failed to deliver useful results, leading the team to abandon that path and focus on C2.

**Demonstrated 1/2**

- **+** [40:35](https://youtu.be/D_AmK8-UnZg?t=2435) Prepared field-layout output is clicked through on screen, showing flattened layouts and their storage accounting.
- **−** [42:11](https://youtu.be/D_AmK8-UnZg?t=2531) The scalarization rewrite that removes intermediate Point allocations is walked through on a slide without an actual run shown.

**Measured 1/2**

- **+** [47:21](https://youtu.be/D_AmK8-UnZg?t=2841) The Point walk slide compares identity objects at 23.04 ms and 152 MiB against value objects at 2.74 ms and zero allocation, but the rough benchmark does not state its measurement method.
- **−** [10:50](https://youtu.be/D_AmK8-UnZg?t=650) The contrived microbenchmark’s 40% gain names only the speaker’s cloud instance as setup and is explicitly not extrapolated to whole applications.
- **−** [12:22](https://youtu.be/D_AmK8-UnZg?t=742) The 20% Class-File API improvement is a secondhand anecdote about an arbitrary tool, with no baseline or setup shown.

**Depth 2/2**

- **+** [37:28](https://youtu.be/D_AmK8-UnZg?t=2248) Wider atomic instructions are rejected as a flattening fix because their alignment would cost data density and add cache traffic.
- **+** [31:13](https://youtu.be/D_AmK8-UnZg?t=1873) Strict initialization is checked statically once by the verifier, so the fast path needs no runtime checks.
- **+** [43:41](https://youtu.be/D_AmK8-UnZg?t=2621) Scalarization is grounded in value semantics: values pass conceptually by value and cannot be mutated, so C2 can keep fields in registers where it gives up on escaping regular objects.

**Reusable 1/2**

- **+** [06:15](https://youtu.be/D_AmK8-UnZg?t=375) Source level 28, preview enabling and the JDK 28 early-access build give viewers a starting point for trying value objects.
- **·** [06:15](https://youtu.be/D_AmK8-UnZg?t=375) The published pointer is the presented project’s own build, rather than a sample project or checklist reproducing the talk’s examples.
