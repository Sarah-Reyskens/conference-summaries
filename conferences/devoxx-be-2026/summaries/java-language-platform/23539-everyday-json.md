---
title: Everyday JSON
talkId: "23539"
conference: devoxx-be-2026
speakers: [Viktor Klang, Alan Bateman]
track: Java Language & Platform
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=5y_82lCevHg
durationMin: 51
slides: null
verdict: 6
reach: broad
frames: 13
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Everyday JSON
Viktor Klang, Alan Bateman · Conference · Java Language & Platform

## TL;DR
JEP 540 proposes a small incubating JSON API in the JDK (targeted at JDK 28) for parsing, navigating and generating JSON in simple cases where pulling in Jackson is overkill. Klang covers the API surface and its strict RFC 8259 stance, Bateman shows it querying real JDK-produced JSON such as thread dumps and JFR output, and both frame it as a starting point you graduate from when your needs grow.

## Key takeaways
- JEP 540 offers `Json.parse`, `toString` (compact) and `toDisplayString` (pretty-printed) over an immutable sealed tree of `JsonValue` subtypes, with no coercion between types.
- Absence is handled with `tryGet`/`tryValue` returning `Optional`, while a wrong path fails fast with an exception naming the expected member, the path and the document offset.
- The parser is deliberately strict: RFC 8259 only, no comments, no trailing commas, no duplicate member names, because a document whose meaning depends on the parser is a defect in waiting.
- The API is positioned for initial, small, simple or one-off tasks (config files, test payloads, JShell exploration); growing needs such as comments or object mapping are a signal to move to a library.
- The JDK itself is a consumer: `jfr print --json`, JSON thread dumps and a possible JSON form for `java.util.Properties` all pair with the new API for small diagnostic tools.

## Notes

### [01:04](https://youtu.be/5y_82lCevHg?t=64) Why the JDK needs a JSON API
Klang opens with a show of hands: nearly everyone uses Jackson, and dozens of JSON libraries exist. He argues many everyday tasks (a config file, a probe payload for an HTTP request, a test fixture, extracting data from a file, a prototype's persisted state, JShell exploration) do not need a third-party dependency, just as Go or Python handle them in the platform. The common denominator is work that is initial, small, simple or one-off.

### [07:52](https://youtu.be/5y_82lCevHg?t=472) JEP 540 and its API surface
JEP 540, Simple JSON API (incubator), is proposed for JDK 28, succeeding the broader 2014-era JEP 198 with a narrower design. The API surface is tiny: static `Json.parse` and `toDisplayString` (with an indent parameter), plus `toString` for the compact form. `JsonValue` declares typed accessors (`asString`, `asInt`, `asLong`, `asBoolean`, `asList`, `asMap`) that never coerce: `asString` on a JSON string returns it, and anything else is an error. Navigation uses `get` by index or member name, `tryGet` for optionals, and `tryValue` to distinguish JSON null from absent.

### [12:38](https://youtu.be/5y_82lCevHg?t=758) Three examples in a few lines each
A config file (`port`, `charset`) is read and extracted in about three lines, with `tryGet` plus `orElse(8080)` covering the optional port. An HTTP POST builds a `Json.objectOf(Map.of(...))` payload and sends it through the built-in `HttpClient`. A weather-forecast query parses the response and computes the average temperature with `json.get("properties").get("periods").asList().stream().mapToInt(j -> j.get("temperature").asInt()).average()`.

### [21:00](https://youtu.be/5y_82lCevHg?t=1260) Data-oriented design and fail-fast traversal
The model is a sealed set of interfaces over immutable data, so pattern matching branches cleanly on heterogeneous input such as an id that is sometimes a number and sometimes a string. A misspelled path (`baar` for `bar`) throws eagerly, before any value is inspected, and the exception reports what was sought, the path and the offset.

### [23:36](https://youtu.be/5y_82lCevHg?t=1416) Against Postel's law for parsers
Klang argues the robustness principle breaks down for parsers: two "liberal" parsers accept different malformed inputs (comments in several dialects, trailing commas, duplicate members resolved first, last or at random), so the document's meaning depends on the implementation. JEP 540 therefore supports RFC 8259 strictly, with no extensions.

### [28:14](https://youtu.be/5y_82lCevHg?t=1694) JSON inside the JDK
Bateman takes over with the platform view: JSON beside `HttpClient` invites future body publishers/handlers that skip the string round-trip, marshalling could map structural representations to and from JSON, and JMX-over-REST would avoid RMI and serialization. Serviceability tools already emit JSON today.

### [30:47](https://youtu.be/5y_82lCevHg?t=1847) jfr print and thread dumps as JSON
`jfr print --events jdk.VirtualThreadPinned --json` prints events such as virtual-thread pins as JSON, and `jcmd Thread.dump_to_file` produces thread dumps in plain text or JSON. The thread dump schema (linked from `HotSpotDiagnosticMXBean` javadoc) nests thread containers, threads, stacks and monitors with optionality, explicit nulls and variable structure, which makes it an ideal workout for the API.

### [33:21](https://youtu.be/5y_82lCevHg?t=2001) Thread-dump tooling with the new API
Bateman builds up a tool: list every thread's `tid` and name via nested `asList` traversal, then filter virtual threads with an `isVirtual` helper using `tryGet("virtual")`, then map owned object monitors per stack depth with `tryValue` handling the JSON nulls left by lock elimination. A second example round-trips `java.util.Properties` to pretty-printed JSON and back in a few lines each way.

### [40:37](https://youtu.be/5y_82lCevHg?t=2437) LLMs, TL;DR and how to try it
Klang notes that a simple built-in API also makes one-off JSON tools easy for LLMs to generate. The summary slide: this API is for when you have nothing else; no object mapping, no streaming, just simple things done simply. An early-access release is available and feedback goes to core-libs-dev.

### [43:16](https://youtu.be/5y_82lCevHg?t=2596) Q&A
Values are immutable: a mutable input map is copied into an immutable backing. JSON objects stay unordered, since observable order would invite reliance on something the spec does not define. Nested generation is verbose today; the parse side is more mature than the generation side, record mapping is out of scope for this JEP, and growing needs mean graduating to a library. JSON numbers beyond `long`/`double` are covered in a JEP section on `BigDecimal`, and the parse overloads take `String` and `char[]` rather than `CharSequence` for reasons written up on core-libs-dev.

## Tools, libraries and specs
- JEP 540 (Simple JSON API, incubator, proposed for JDK 28)
- JEP 198 (2014 lightweight JSON API proposal, did not proceed)
- RFC 8259 (JSON specification the API implements strictly)
- Jackson (the library nearly the whole audience uses)
- JDK HttpClient, JShell, JFR (`jfr print --json`), `jcmd Thread.dump_to_file`, `HotSpotDiagnosticMXBean`, `java.util.Properties`
- api.weather.gov gridpoints endpoint (forecast example)
- Early-access JDK 28 build and core-libs-dev mailing list (try-out and feedback)

## Who should watch
Java developers curious about the built-in JSON API coming in JDK 28, and anyone writing small diagnostic or one-off tools against JDK-produced JSON. Readers who only need the API reference can go straight to the JEP text; teams needing object mapping, streaming or lenient parsing should stay with Jackson or a similar library.

## Verdict
**6/10**: JEP 540's rationale presented with the speakers' experience and JDK-internal tooling examples, and the strict-parsing, fail-fast and scope decisions explained with their alternatives; held back by material that a read of the JEP largely gives, one captured run, and code that lives on slides.

**Reach broad**: most Java developers who handle JSON config, HTTP payloads or JDK diagnostic output can use the built-in API for small tasks once it ships.

**Novelty 1/2**

- **+** [28:14](https://youtu.be/5y_82lCevHg?t=1694) Bateman maps JSON consumers inside the JDK, from HttpClient handlers and marshalling to JMX over REST and Properties, as a roadmap beyond the JEP.
- **+** [40:37](https://youtu.be/5y_82lCevHg?t=2437) Klang notes a simple built-in API also lets LLMs generate one-off JSON tools without extra project setup.
- **−** JEP 540 (openjdk.org/jeps/540), which Klang calls very well written and points the audience to, already holds the API surface, the weather example and the strict-parsing policy that fill the first half.

**Demonstrated 1/2**

- **+** [34:55](https://youtu.be/5y_82lCevHg?t=2095) The slide shows the thread-dump printer's `java --add-modules` command line with its printed thread ids and names.
- **−** [19:58](https://youtu.be/5y_82lCevHg?t=1198) The weather-forecast pipeline is presented as code, and the average temperature it computes is never run or read out.

**Measured 1/2**

- **·** [14:14](https://youtu.be/5y_82lCevHg?t=854) The talk makes no quantitative claim, and "three lines of code" describes an example's size rather than a result.

**Depth 2/2**

- **+** [24:38](https://youtu.be/5y_82lCevHg?t=1478) The strictness section weighs comment dialects, trailing commas and first-versus-last duplicate resolution with its streaming consequence before settling on RFC 8259 only.
- **+** [22:03](https://youtu.be/5y_82lCevHg?t=1323) Fail-fast traversal is set against erroring after the whole traversal, shown with a misspelled path whose exception reports what was sought, the path and the document offset.
- **−** [46:58](https://youtu.be/5y_82lCevHg?t=2818) The generation side is acknowledged as less mature than the parsing side, with nested-object verbosity left without a design answer.

**Reusable 1/2**

- **+** [42:45](https://youtu.be/5y_82lCevHg?t=2565) An early-access JDK build and the core-libs-dev feedback channel give a path to try the API immediately.
- **−** [33:21](https://youtu.be/5y_82lCevHg?t=2001) The thread-dump and Properties examples exist only as code on slides, to be retyped.
