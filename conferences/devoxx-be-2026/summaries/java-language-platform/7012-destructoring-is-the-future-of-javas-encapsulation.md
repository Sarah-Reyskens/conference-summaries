---
title: Destructoring is the future of Javas Encapsulation
talkId: "7012"
conference: devoxx-be-2026
speakers: [Richard Gross]
track: Java Language & Platform
sessionType: Lunch Talk
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=wcghmWdu-HY
durationMin: 37
slides: https://speakerdeck.com/richargh/destructoring-is-the-future-of-javas-encapsulation-v1-at-devoxx-be-2026
verdict: 5
reach: broad
frames: 4
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Destructoring is the future of Javas Encapsulation
Richard Gross · Lunch Talk · Java Language & Platform
Slides: https://speakerdeck.com/richargh/destructoring-is-the-future-of-javas-encapsulation-v1-at-devoxx-be-2026

## TL;DR
Both JDK serialization and library deserialization via deep reflection bypass constructors and break encapsulation, so deserialized objects can violate their own invariants. Project Amber's "Derived Record/Class Creation" work proposes making deconstruction a first-class language concept, which would enable safer serialization, pattern matching on classes, and withers for records and classes.

## Key takeaways
- JDK deserialization sets private and final fields directly and never calls the constructor, so an `Adult` class guarding `age >= 18` can deserialize into an object reporting age 17.
- Jackson, Hibernate and similar libraries break encapsulation the same way through deep reflection (`setAccessible` on private final fields, possible since JDK 5).
- JEP 8305968 ("integrity by default") plans to restrict deep reflection so frameworks cannot use it unless application authors opt back in; JDK 26 warns on `setAccessible` on final fields ("prepare to make final mean final", JEP 500).
- Records already do the right thing (serialization calls the canonical constructor), but classes are still needed when stored state differs from the API, when state is derived or cached, or when mutation in place is required.
- First-class deconstruction patterns would let one annotated constructor plus one annotated pattern replace the ~7 magic serialization methods and ~16 Jackson annotations used today.

## Notes

### [01:36](https://youtu.be/wcghmWdu-HY?t=96) JDK deserialization ignores constructors
The opening demo shows an `Adult` class whose constructor rejects birthdates younger than 18. Deserializing it through `ObjectInputStream.readObject()` yields an object whose `age()` prints 17. The serialization API gobbles up all private fields on write and sets them directly on read. Quoting Mark Reinhold, probably a third of all Java vulnerabilities have involved serialization, possibly over half, and removing serialization is a stated goal of Project Amber.

### [03:13](https://youtu.be/wcghmWdu-HY?t=193) Libraries break encapsulation through deep reflection
The same `Adult` deserialized through Jackson with a no-arg constructor also prints 17. The mechanism is deep reflection: `getDeclaredField("birthdate")`, `setAccessible(true)`, then `set`, applied even to private final fields. The history goes back to JDK 5 (JDK-5044412), when the spec requiring `final` to mean immutable broke XML serialization in Sun's own app server, so `setAccessible` on final fields was permitted for compatibility. Reflection itself is fine; deep reflection is the problem.

### [05:51](https://youtu.be/wcghmWdu-HY?t=351) Integrity by default and the missing concept
JEP 8305968 ("integrity by default") states that developers expect code and data to be protected against unwanted or unwise use, and that unsafe APIs will be restricted by default while application authors can override the default. The current APIs cannot simply be switched off: every serialization format (JSON, YAML, Protobuf, Avro, CSV, docx) depends on them, and the APIs are undiscoverable magic (seven serialization methods) plus a thicket of paired Jackson annotations that do not transfer across formats. The talk's central diagram shows the asymmetry: deserialization has the constructor, but serialization has no language-level inverse, the deconstructor.

### [10:33](https://youtu.be/wcghmWdu-HY?t=633) Records help, but classes still matter
For records, the serialization API calls the constructor, `setAccessible(true)` on final fields fails, and accessors stay in sync with constructor parameters. A `Timestamp` example motivates classes anyway: it takes a UTC date string in the constructor but stores a compact `long` internally, decoupling API state from stored state. Records also cannot derive or cache internal state or mutate in place. The advice is to use records where possible and fix classes for the rest.

### [14:12](https://youtu.be/wcghmWdu-HY?t=852) Deconstruction as a first-class citizen
The proposal adds a deconstruction pattern that maps internal state back to the constructor's shape, shown in a strawman syntax that mirrors the constructor. None of the syntax is final; several alternatives are under discussion on the amber-spec-experts list (Carrier Classes, January 2026) and in talks such as "Serialization: A New Hope" (2024).

```java
// from published slides p.25
public class Timestamp {
    private final long rawValue;
    // Constructor
    public Timestamp(String rawUtcDate) {
        this.rawValue = parseUtcDateString(utcDate);
    }
    // Deconstruction pattern
    public pattern Timestamp(String rawUtcDate) {
        rawUtcDate = formatAsUtcDateString(this.rawValue);
    }
}
```

### [16:17](https://youtu.be/wcghmWdu-HY?t=977) What deconstruction unlocks
With `@Deserializer` on the constructor and `@Serializer` on the pattern, one declaration would serve every framework and format, with `@Deserializer(version = 1)` style overloads for versioned formats. The same patterns enable pattern matching on plain classes (`if (obj instanceof Address(var street, var city))`), which matters because every public JDK type available for matching is currently a class, not a record. Deconstruction patterns on static factory methods would collapse verbose `Optional`/`Ball` null-check-and-cast chains into a single `instanceof` against `Optional.of(Ball.of(RED, var count))`.

### [19:59](https://youtu.be/wcghmWdu-HY?t=1199) Withers for classes and records
Reconstruction needs a canonical constructor to target (as Kotlin's primary constructor and records' canonical constructor already define), plus a strawman `with` syntax (`anAddress with { city = "Cool City"; }`) that deconstructs and rebuilds through the constructor so invariants are rechecked. For records this removes handwritten `withStreet`/`withCity` methods; the JDK effort is called Derived Record Creation (JEP 468), and the team is working out classes first so both share one mechanism.

### [25:48](https://youtu.be/wcghmWdu-HY?t=1548) Q&A: Lombok, Jackson, builders
Asked how Lombok creates withers without this machinery, Gross guesses (having never used it) that it leans on the all-args constructor plus name matching, similar to Jackson's constructor inference, which needs the `ParameterNamesModule` and the `-parameters` compiler flag because parameter names otherwise compile to `arg1`, `arg2`. An audience member confirms Lombok requires the all-args annotation and errors otherwise. Gross warns that clone-and-mutate withers, as in C# records, skip the constructor, leaving invariants unchecked and derived state stale. On builders, handwritten ones are preferable because Lombok `@Builder` defaults every field to null or zero, which may violate business rules like the adult age check.

## Tools, libraries and specs
- Project Amber: Derived Record/Class Creation, JEP 468
- JEP 8305968 (integrity by default), JEP 500 (prepare to make final mean final, JDK 26)
- JDK-5044412 (deep reflection origins), JDK-8247517 (setAccessible fails on record final fields)
- Jackson 2 ParameterNamesModule with `-parameters`; unnamed patterns (underscore, JDK 26)
- Code examples: https://github.com/Richargh/encapsulation-java-mvn-sandbox

## Who should watch
Java developers who serialize objects through Jackson, JPA, or the JDK API and want to understand why that breaks encapsulation and where the language is heading. Those already following amber-spec-experts or Brian Goetz's serialization talks can skip the middle; the Q&A on Lombok and Jackson internals is the most original part.

## Verdict

**5/10**: A clear beginner model of the encapsulation problem and the deconstruction fix, with demos that are never run and a proposal half that has nothing to take home yet.

**Reach broad**: most of the conference audience serializes objects through Jackson, JPA or the JDK API and will meet this future JDK feature once it ships.

**Novelty 1/2**

- **+** [12:06](https://youtu.be/wcghmWdu-HY?t=726) The Timestamp example, which takes a UTC string but stores a compact long, comes from the speaker's own project work.
- **+** [26:19](https://youtu.be/wcghmWdu-HY?t=1579) The Q&A works out on the spot how Jackson infers constructors from matching parameter names, reasoning the speaker builds live from admitted ignorance of Lombok.
- **−** The integrity-by-default segment follows JEP 8305968, quoting its rationale rather than adding analysis.

**Demonstrated 0/2**

- **−** [01:36](https://youtu.be/wcghmWdu-HY?t=96) The age-17 JDK result appears as slide code with a `// prints 17???` comment; no program runs on screen.
- **−** [03:13](https://youtu.be/wcghmWdu-HY?t=193) For Jackson, the age-17 result gets the same treatment: slide code ending in `// prints 17???`, never executed.

**Measured 1/2**

- **+** [02:09](https://youtu.be/wcghmWdu-HY?t=129) The quoted Reinhold estimate (a third to over half of Java vulnerabilities) puts a number on serialization's share of the problem.
- **−** [02:09](https://youtu.be/wcghmWdu-HY?t=129) That figure is relayed from a 2018 interview with no method behind it, so it stays an anecdote rather than a measurement.
- **−** [12:39](https://youtu.be/wcghmWdu-HY?t=759) The Timestamp memory claim carries no figures: no allocation numbers or before/after comparison for the long-vs-string storage.

**Depth 2/2**

- **+** [03:44](https://youtu.be/wcghmWdu-HY?t=224) Deep reflection is traced to JDK-5044412, where enforcing final broke Sun's own app server and forced the setAccessible compromise.
- **+** [13:11](https://youtu.be/wcghmWdu-HY?t=791) The records-vs-classes trade-off is spelled out: separate API state from stored state, derive or cache state internally, or mutate in place.
- **+** [20:29](https://youtu.be/wcghmWdu-HY?t=1229) Withers need a single canonical constructor to reconstruct through, because with several constructors "which one do you use" is undefined, and C# clone-and-mutate withers skip the constructor, leaving invariants unchecked and derived state stale ([30:29](https://youtu.be/wcghmWdu-HY?t=1829)).

**Reusable 1/2**

- **+** [26:50](https://youtu.be/wcghmWdu-HY?t=1610) The appendix slide shows the Jackson-without-default-constructor example in full and links its runnable test in the public sandbox repo.
- **+** [28:25](https://youtu.be/wcghmWdu-HY?t=1705) The prerequisites are named: the ParameterNamesModule plus the -parameters compiler flag, without which parameter names compile to arg1, arg2.
- **−** [15:15](https://youtu.be/wcghmWdu-HY?t=915) The sandbox repo covers the problem examples only; the deconstruction patterns are strawman sketches, so that half has nothing to take home.
