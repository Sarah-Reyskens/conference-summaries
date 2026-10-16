---
title: "The Magic of OpenTelemetry: Rewriting Your App in Production"
talkId: "5519"
conference: devoxx-be-2026
speakers: [Bruce Bujon]
track: Java Language & Platform
sessionType: Tools-in-Action
audienceLevel: ADVANCED
video: https://www.youtube.com/watch?v=Lf_m5dIjjqw
durationMin: 30
slides: null
verdict: 8
reach: segment
reviewedAt: 2026-10-16
frames: 9
---

# The Magic of OpenTelemetry: Rewriting Your App in Production

Bruce Bujon · Tools-in-Action · Java Language & Platform

## TL;DR

The OpenTelemetry Java agent instruments applications without code changes by intercepting class loading and rewriting bytecode before classes are defined. Bujon demonstrates this end to end, then exposes exactly what the agent injects using a meta-agent that diffs classes before and after transformation. The talk closes with the production cost: allocation and contention overhead plus a 50 to 75 percent startup penalty, with measurements and mitigation options.

## Key takeaways

- The OTel Java agent needs no code or dependency changes: adding `-javaagent` plus configuration is enough to get traces, metrics and logs from libraries that never heard of OpenTelemetry.
- Instrumentation works through `premain` and a `ClassFileTransformer` that receives each class as a byte array and returns rewritten bytes; the code that runs is no longer the code that was compiled.
- OTel rewrites even JDK internals: the demo shows injected code in the JDK HTTP server and in `ForkJoinPool`, and 38,000 added lines on the 5,000-line Jedis client.
- Expect a startup penalty around 50 to 75 percent from class-pattern matching at load time, which matters most for serverless workloads.
- Of the startup technologies, GraalVM Native Image removes the penalty and Project Leyden looks promising, while AppCDS starts but gives no gain and Leyden currently crashes the OTel agent.

## Notes

### [01:07](https://youtu.be/Lf_m5dIjjqw?t=67) What OpenTelemetry is and where the Java agent fits

OpenTelemetry defines vendor-neutral APIs and conventions for traces, logs, metrics and profiles; backends from Prometheus and Jaeger to commercial products consume them. Java applications emit OTLP messages either through the OTel SDK used by libraries and frameworks, or through the Java agent attached to an already packaged application. Everything flows through the OTel Collector, which receives, aggregates and filters signals before exporting them to one or more backends.

### [04:16](https://youtu.be/Lf_m5dIjjqw?t=256) Demo: traces from an app with zero OTel dependencies
The demo application is a plain web server using the JDK HTTP server and client plus the Jedis Redis client, none of which depend on OTel. The only change is mounting the agent jar into the container and setting `JAVA_TOOL_OPTIONS` with `-javaagent`, a service name and the collector endpoint. After redeploying and making three requests, the backend shows three traces whose spans cover the HTTP server (route, client, status, plus automatically captured resource attributes like JDK version and command line), the downstream HTTP client call, and Jedis `get`/`set` operations.

### [09:03](https://youtu.be/Lf_m5dIjjqw?t=543) How Java agents rewrite classes at load time

Java agents are programs that start before `main` via a `premain` method receiving an `Instrumentation` instance, the same mechanism profilers and JaCoCo use. Calling `addTransformer` registers a `ClassFileTransformer` whose single `transform` method runs for every loaded class, receiving the class bytes and returning replacement bytes. Getting this right means parsing the class-file format (JVM specification chapter 4), locating method bodies and code attributes, and emitting valid bytecode, in practice with ASM, ByteBuddy or the JDK 24 Class-File API. OTel stays on the older libraries for Java 8 compatibility.

### [15:23](https://youtu.be/Lf_m5dIjjqw?t=923) Meta-agent: watching OTel rewrite bytecode live

To reveal the actual injections, Bujon forked Johannes Bechberger's public meta-agent (an agent that hooks `transform`, captures differing byte arrays, and serves `javap`/decompiler diffs over HTTP) with an improved UI, loading it ahead of the OTel agent. It lists the transformed classes with before/after diffs (the 10,437 figure visible on screen counts all loaded classes, not just transformed ones). The JDK HTTP server gains a registered filter that starts and ends spans around each request. `ForkJoinPool` receives extensive additions to `execute` and task-submission paths. The Jedis client grows from 5,046 to 43,711 decompiled lines per the diff header, roughly 8 to 9 times its original size, a page so heavy the browser loads it slowly.

### [21:14](https://youtu.be/Lf_m5dIjjqw?t=1274) Production cost and startup-time measurements

Runtime costs apply to SDK users too: short-lived span and attribute objects pressure the GC, sampling and filtering burn cycles on already hot paths, and moving signals from business threads to OTel exporter threads can add contention. Agent-specific cost is startup: every loaded class is matched against hundreds of instrumentation patterns. The benchmark, Spring PetClinic 4 measured from start to first response, shows about 2 seconds baseline versus about 3.5 seconds with OTel and 3 seconds with Datadog, a 50 to 75 percent penalty. Native Image removes the overhead, AppCDS runs but yields no gain, and Leyden gives Datadog baseline-equivalent startup while OTel currently crashes under it.

### [27:59](https://youtu.be/Lf_m5dIjjqw?t=1679) Recap: four things the agent does for you

The agent adds the OTel SDK as a dependency, scans every loaded class for known patterns, patches matches to emit signals, and configures the SDK, all from one `-javaagent` line. Bujon notes the OTel Java agent descends from a Datadog donation, so Datadog's Leyden and Native Image work may eventually benefit OTel and the JDK itself.

## Tools, libraries and specs

- OpenTelemetry Java agent and SDK, OTel Collector, OTLP
- `java.lang.instrument` (premain, ClassFileTransformer), bootstrap classpath
- ByteBuddy, ASM, Class-File API (JDK 24), javap, FernFlower (IntelliJ's bundled decompiler)
- JaCoCo, Jedis, Spring PetClinic 4, Project Leyden, AppCDS, GraalVM Native Image, Datadog Java agent

## Who should watch

Java engineers running the OTel agent in production, or anyone weighing zero-code instrumentation against manual SDK use, will get the most from the bytecode diffs and the startup numbers. Skip it if you already build ByteBuddy instrumentations; the agent mechanics will be familiar and only the measurements add anything.

## Verdict

**8/10**: Zero-code tracing and the bytecode diffs run on screen, a start-to-first-response comparison covers two agents, and the transformation pipeline and startup cost are explained; the examples are not published as a reproducible project.

**Reach segment**: Java backend teams using or evaluating the OpenTelemetry Java agent can apply the startup trade-offs and the picture of what the agent does to their classes.

**Novelty 1/2**

- **+** [26:25](https://youtu.be/Lf_m5dIjjqw?t=1585) A Datadog agent engineer reports where Native Image and AppCDS stand with a production agent (Native Image removes the startup penalty, AppCDS can be kept from crashing but gains nothing), which the OpenTelemetry docs do not cover.
- **+** [25:54](https://youtu.be/Lf_m5dIjjqw?t=1554) The speaker places the OTel Java agent as a Datadog donation and hopes Datadog's Leyden and Native Image work transfers to OTel and the JDK, a practitioner view stated as hope, not as an outcome.
- **·** The basic agent setup and the `java.lang.instrument` API follow the OpenTelemetry Java agent documentation and the JDK `java.lang.instrument` package docs.

**Demonstrated 2/2**

- **+** [05:54](https://youtu.be/Lf_m5dIjjqw?t=354) Redeploying the unmodified application with the agent produces three traces with HTTP server, HTTP client and Redis spans.
- **+** [17:29](https://youtu.be/Lf_m5dIjjqw?t=1049) The meta-agent lists the classes OTel transformed and the walkthrough opens the JDK HTTP server's before/after code.

**Measured 2/2**

- **+** [26:57](https://youtu.be/Lf_m5dIjjqw?t=1617) A Spring PetClinic 4 comparison measures start to first response and shows about 2 seconds without an agent, 3.5 seconds with OTel and 3 seconds with Datadog.
- **+** [20:43](https://youtu.be/Lf_m5dIjjqw?t=1243) The diff header counts 5,046 decompiled Jedis lines before transformation and 43,711 afterward, a before/after size of the same class.
- **·** [27:27](https://youtu.be/Lf_m5dIjjqw?t=1647) The Leyden comparison is a single-application chart without a stated run count or variance.

**Depth 2/2**

- **+** [12:09](https://youtu.be/Lf_m5dIjjqw?t=729) The explanation follows class bytes through method-body modification, validation and replacement, and says why Java 8 support rules out the JDK 24 Class-File API.
- **+** [24:20](https://youtu.be/Lf_m5dIjjqw?t=1460) Startup overhead is derived from matching every loaded class against every instrumentation, with cheap name checks set against inheritance and method inspection and the extra work when a match is rewritten.
- **+** [23:19](https://youtu.be/Lf_m5dIjjqw?t=1399) Moving telemetry from business threads to exporter threads is named as a source of locks and contention that depends on the application profile.

**Reusable 1/2**

- **+** [18:30](https://youtu.be/Lf_m5dIjjqw?t=1110) The inspector UI shows a GitHub button, a lead for reconstructing the bytecode-inspection workflow.
- **−** [29:36](https://youtu.be/Lf_m5dIjjqw?t=1776) The closing offers no demo project or configuration that reproduces the application, collector and meta-agent setup.
