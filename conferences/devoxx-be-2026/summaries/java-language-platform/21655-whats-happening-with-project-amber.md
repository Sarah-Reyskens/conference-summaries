---
title: What’s happening with Project Amber?
talkId: "21655"
conference: devoxx-be-2026
speakers: [Gavin Bierman]
track: Java Language & Platform
sessionType: Conference
audienceLevel: ADVANCED
video: https://www.youtube.com/watch?v=Go76-9Q51wU
durationMin: 52
slides: null
verdict: 7
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# What’s happening with Project Amber?
Gavin Bierman · Conference · Java Language & Platform

## TL;DR
Project Amber has finalized 10 language features in 13 releases, most of them building data-oriented programming from records, sealed classes, and patterns. The talk previews two coming themes: polishing that experience (primitive patterns, pattern declarations, constant patterns, record reconstruction) and going beyond it with "data interfaces" that bring record-style patterns to interface-based APIs.

## Key takeaways
- Pattern matching is the right home for primitive conversions because matching is already conditional: an exact conversion matches, a lossy one simply does not match instead of silently dropping information.
- Checking conversion exactness by converting there and back is wrong: `Integer.MAX_VALUE` to float and back lands on the same value through two lossy steps, so the spec needs a stricter definition.
- Equality tests belong inside patterns as constant patterns (`Point(0, 0)`) rather than in `when` clauses, which sit outside the pattern and cannot compose.
- Single-component `withX` methods cannot update records whose invariants span components (two lists constrained to equal length), which motivates a `with` expression that names only changed components.
- A header on an interface (a "data interface") could declare the accessor methods that give meaning to a record-like pattern, letting sealed interface-and-impl APIs such as the JSON and class-file APIs be pattern-matched without exposing their implementation classes.

## Notes

### [00:34](https://youtu.be/Go76-9Q51wU?t=34) Six and a half years of Amber
Amber explores and incubates small Java language features, always through previews before finalizing. The scoreboard across 13 releases: 10 finalized features. Past work falls into themes: strings (text blocks in JDK 15; string templates prototyped in 21/22 then withdrawn over design and performance concerns, with active work on a replacement), paving the on-ramp (the two JDK 25 beginner features, also useful for executable scripts), flexible constructor bodies (the only Amber JEP originating outside Oracle, which fortuitously set up Valhalla work), and data-oriented programming, the largest theme with six shipped features.

### [07:55](https://youtu.be/Go76-9Q51wU?t=475) Data-oriented programming recap
The foundation is records (immutable nominal tuples with compiler-synthesized accessors), sealed classes (compile-time and load-time integrity over permitted subclasses), and patterns (type patterns and record patterns as composable tests). The three working principles: model plain data immutably, model it precisely enough that a domain expert reads the declarations directly, and make illegal values unrepresentable by validating in constructors.

### [13:04](https://youtu.be/Go76-9Q51wU?t=784) Example: modelling web pages
A GitHub crawler's `Page` type starts as a flat class with nullable getters and helper predicates, then becomes a sealed hierarchy of records: `Page` is `SuccessPage` or `ErrorPage`, `SuccessPage` is `GitHubPage` or `ExternalPage`, and so on. Processing collapses to an exhaustive switch over four record patterns with no `default` clause; the compiler reports any forgotten case.

### [19:47](https://youtu.be/Go76-9Q51wU?t=1187) Primitive types in patterns
Today top-level primitive type patterns are a compile-time error and nested ones must exactly match the record component type, an asymmetry since construction freely widens (an `int` literal into a `double` component). The proposal, already in preview, admits conversions under exactness: `16_777_217` fails to match a `float` pattern because the conversion loses information. The JEP also allows switching over any type, including floating point, and bare `instanceof float` checks.

### [28:39](https://youtu.be/Go76-9Q51wU?t=1719) Pattern variable declarations
Patterns currently appear only in conditional positions (`instanceof`, `case` labels), so purely deconstructive uses like `instanceof Triple(var a, var b, var c)` indent the real code for no reason. The sketch: statements and enhanced-`for` headers that take an unconditional pattern and put its bindings in scope for the rest of the block, a multi-way assignment over record components.

### [31:46](https://youtu.be/Go76-9Q51wU?t=1906) Constant patterns
Today testing for `Point(0, 0)` or a `US`/`UK` enum constant requires a `when` clause evaluated after the pattern matches, distant from the pattern and wasteful when the pattern navigates deep into a structure. The proposal lets literals, enum constants, and `null` appear directly in pattern position, restoring compositionality. Type checking, equality semantics, and exhaustiveness checking are flagged as open technical issues.

### [36:29](https://youtu.be/Go76-9Q51wU?t=2189) Record reconstruction
Copying a record with one changed component either repeats every accessor call or needs per-component `withX` methods, which fail against multi-component invariants and explode combinatorially into `withXY` variants. The sketched `with` expression names only changed components and desugars to the canonical constructor call:

```java
// from slide at 40:30
Point newLoc = oldLoc with { x: oldLoc.x()*2 };
```

### [41:42](https://youtu.be/Go76-9Q51wU?t=2502) Beyond: data interfaces
JDK APIs increasingly use the public-sealed-interface plus hidden-implementation style (class-file API, FFM, JSON, Babylon), and client code over them is `instanceof` plus accessor calls, exactly what record patterns desugar to. Adding a header to an interface would implicitly declare abstract accessors and give meaning to a data-interface pattern such as `JsonString(var str)`. A prototype compiler added headers to 110 class-file API interfaces and 18 FFM ones, and `Map.Entry` is named as a JDK-wide candidate. Records today, interfaces next, plain classes after that.

## Tools, libraries and specs
- JEP on primitive types in patterns, in preview (number not stated on screen)
- Class-File API, Foreign Function & Memory (FFM) API, JSON API (in development), Project Babylon API: interface-style APIs used as data-interface examples
- `Map.Entry`: named as a candidate for a data-interface header

## Who should watch
Java developers already using records, sealed types, and pattern matching who want to see where the language is heading and why. Those still learning the shipped features should work through a data-oriented programming introduction first; the recap here moves fast.

## Verdict
**7/10**: Design rationale from an Amber insider with prototype evidence, but unshipped sketches on slides with no demo and no artifact to try.

**Novelty 2/2**

- **+** [23:55](https://youtu.be/Go76-9Q51wU?t=1435) The exact-conversion rule for primitive patterns is argued by its designer as a fit for pattern matching's conditionality, and [27:32](https://youtu.be/Go76-9Q51wU?t=1652) shows why the naive convert-and-compare check fails.
- **+** [48:59](https://youtu.be/Go76-9Q51wU?t=2939) Prototype-compiler results are reported first-hand: headers added to 110 class-file API interfaces and 18 FFM interfaces, with client code rewritten to data-interface patterns.
- **·** [07:55](https://youtu.be/Go76-9Q51wU?t=475) The records, sealed classes, and patterns recap retraces material covered by the JDK 16–21 release notes, credited as background for the new proposals.

**Demonstrated 1/2**

- **·** [19:47](https://youtu.be/Go76-9Q51wU?t=1187) No demo slot: the speaker flags everything shown as unshipped designs that may never appear in the presented form, and the primitive-pattern feature already in preview [20:18](https://youtu.be/Go76-9Q51wU?t=1218) and the prototype refactors are described with slide code, not run on screen.

**Measured 1/2**

- **+** [48:59](https://youtu.be/Go76-9Q51wU?t=2939) The data-interface prototype scope is quantified as 110 interfaces in the class-file API and 18 in the FFM API.
- **·** [48:59](https://youtu.be/Go76-9Q51wU?t=2939) Those counts are anecdotal scope reports with no baseline, method, or before/after comparison.

**Depth 2/2**

- **+** [26:30](https://youtu.be/Go76-9Q51wU?t=1590) The `Integer.MAX_VALUE` to float and back round-trip shows two lossy conversions landing back at the starting value, motivating the stricter exactness spec.
- **+** [38:34](https://youtu.be/Go76-9Q51wU?t=2314) A record constraining two lists to equal length shows why single-component withers cannot substitute for a multi-component reconstruction form.
- **+** [32:48](https://youtu.be/Go76-9Q51wU?t=1968) The argument for constant patterns is grounded in compositionality: `when`-clause tests sit outside nestable pattern positions and run only after matching succeeds.

**Reusable 1/2**

- **+** [47:25](https://youtu.be/Go76-9Q51wU?t=2845) The `JsonString(String asString)` header-plus-pattern sketch is a complete example to copy if the feature ships.
- **+** [50:01](https://youtu.be/Go76-9Q51wU?t=3001) A second before/after refactor, the `Map.Entry` pattern in `ConcurrentHashMap`'s `equals`, comes from JDK source.
- **·** [28:05](https://youtu.be/Go76-9Q51wU?t=1685) No artifact is pointed to: the primitive-patterns JEP and draft spec are mentioned without a number or link, and the prototype compiler is not published.
