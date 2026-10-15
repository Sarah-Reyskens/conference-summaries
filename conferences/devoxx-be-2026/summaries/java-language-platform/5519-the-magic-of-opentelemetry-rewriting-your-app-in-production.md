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
verdict: 7
frames: 9
reviewedAt: 2026-10-14
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

**7/10**: Zero-code tracing demo, live bytecode diffs of OTel's injections and a baselined startup chart; the injections and the Leyden/AppCDS incompatibilities go unexplained and the demo app is unpublished.

**Novelty 1/2**

- **+** [18:01](https://youtu.be/Lf_m5dIjjqw?t=1081) The speaker's own run of Bechberger's meta-agent shows what OTel injects into the JDK HTTP server, `ForkJoinPool` and Jedis, with line counts a search does not return.
- **−** The `premain` and `ClassFileTransformer` pipeline is the documented `java.lang.instrument` API (package docs), and the injections themselves live in the public opentelemetry-java-instrumentation modules.

**Demonstrated 2/2**

- **+** [05:54](https://youtu.be/Lf_m5dIjjqw?t=354) An unmodified containerized app produces three traces with HTTP server, HTTP client and Jedis spans after only the agent flag is added.
- **+** [20:43](https://youtu.be/Lf_m5dIjjqw?t=1243) The meta-agent UI renders the transformed-class diffs live, including the Jedis page with its `@@ -1,5046 +1,43711 @@` hunk header after a slow load.

**Measured 2/2**

- **+** [26:57](https://youtu.be/Lf_m5dIjjqw?t=1617) The Spring PetClinic 4 chart compares start-to-first-response across baseline (about 2 s), OTel (about 3.5 s) and Datadog (about 3 s), with the metric stated.
- **+** [20:43](https://youtu.be/Lf_m5dIjjqw?t=1243) The Jedis class goes from 5,046 to 43,711 decompiled lines in the diff header, a before/after count of what the agent injects.
- **−** [26:57](https://youtu.be/Lf_m5dIjjqw?t=1617) The chart states no run count, environment or variance, and the Native Image, AppCDS and Leyden outcomes that follow have no numbers behind them.

**Depth 1/2**

- **+** [12:09](https://youtu.be/Lf_m5dIjjqw?t=729) The transform pipeline is explained: class bytes in, rewritten bytes out, a verify error if the bytecode is invalid, and the Class-File API skipped because OTel supports Java 8.
- **+** [24:20](https://youtu.be/Lf_m5dIjjqw?t=1460) The startup cost is traced to per-class pattern matching: name lookups are cheap, inheritance and method patterns need byte-array analysis, repeated for every class times every instrumentation.
- **−** [25:22](https://youtu.be/Lf_m5dIjjqw?t=1522) The AppCDS and Leyden incompatibilities are conclusions with at most a clause of mechanism, and the `ForkJoinPool` injections ([19:41](https://youtu.be/Lf_m5dIjjqw?t=1181)) are shown without the reason they are needed.

**Reusable 1/2**

- **+** [18:30](https://youtu.be/Lf_m5dIjjqw?t=1110) The meta-agent UI has a GitHub button leading to the public inspector, and the demo's compose file and agent flags are visible on screen.
- **−** [05:10](https://youtu.be/Lf_m5dIjjqw?t=310) The demo project is unpublished and no repository URL is spoken, so the viewer must rebuild the app.
