---
title: Quarkus Meets Leyden at the JVM Performance Edge
talkId: "5510"
conference: devoxx-be-2026
speakers: [Georgios Andrianakis, Ana-Maria Mihalceanu]
track: Java Language & Platform
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=cbSl8UVdMVg
durationMin: 60
slides: null
verdict: 10
frames: 11
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15

# Quarkus Meets Leyden at the JVM Performance Edge

Georgios Andrianakis, Ana-Maria Mihalceanu · Conference · Java Language & Platform

## TL;DR

Project Leyden's ahead-of-time cache composes with Quarkus's build-time optimizations instead of replacing them: a plain Quarkus REST app went from about 350 ms to 80 ms startup in a live demo. Getting there required a special AOT packaging mode, because Leyden only caches classes loaded by JDK class loaders while Quarkus ships its own. The talk pairs the JDK side (workflows, GC-independent object format, training tips) with the framework side (flame-graph-driven fixes, integration design, measured results).

## Key takeaways

- Running an unmodified Quarkus app through Leyden's train-build-deploy workflow roughly halved startup (400 ms to 200 ms) before any Quarkus-side changes.
- Leyden only caches classes loaded by built-in JDK class loaders, so Quarkus's custom class loaders initially blocked most of the benefit; a dedicated AOT jar delegates class loading to the JDK while keeping Quarkus resource and service loading.
- Once class loading disappeared from the flame graphs, millisecond-scale waste became visible and fixable: BigDecimal for startup-time printing, UUID initialization pulling in security providers, gratuitous ServiceLoader use, reflective annotation reads, slow negative class lookups.
- Train with a production-like classpath and smoke tests, not full suites; keep the same JDK, OS, architecture, jar timestamps, and a production classpath that is a superset of training.
- AOT cache size is the price: the sample app's container image grew from 456 MB to 495 MB, and a large synthetic app's from 517 MB to 715 MB.
- AOT-compiled code slated for JDK 28 should bring near-peak performance from the start without retraining when workloads shift.

## Notes

### [02:34](https://youtu.be/cbSl8UVdMVg?t=154) What Quarkus moved to build time

Andrianakis recapped the 2019 Quarkus bet: traditional frameworks scan the classpath, read configuration, and build their metamodel at startup, so Quarkus moved all of that into `mvn package` / Gradle build, leaving runtime startup to little more than opening threads. Annotation scanning across dozens of jars was the dominant cost it eliminated.

### [05:44](https://youtu.be/cbSl8UVdMVg?t=344) Leyden's AOT cache workflows

Mihalceanu described Project Leyden as shifting computation in time through dynamic observation. JDK 24 shipped a three-phase workflow: train the app to record an AOT configuration, assemble the AOT cache, then deploy with it. JDK 25 added automatic early profiling (no flags needed once the cache is in use) and JEP 514, a two-phase flow merging train and build into one step for environments without heap constraints. Last year's normalized benchmarks (mainline 1000, smaller better) showed framework Hello Worlds dropping to 334–412 with the AOT cache, while the class-heavy Spring PetClinic improved less, to 554.
### [11:58](https://youtu.be/cbSl8UVdMVg?t=718) A GC-independent AOT format in JDK 26

The AOT cache stores heap objects in a layout tied to the selected garbage collector, which left ZGC behind. JEP 516 in JDK 26 introduced a GC-independent, streamable object format selected with `-XX:+AOTStreamableObjects`, preferred with ZGC on heaps over 32 GB using compressed oops. The JDK also ships two built-in base caches so the JVM picks a format even without an app-provided cache.

### [15:38](https://youtu.be/cbSl8UVdMVg?t=938) Profiling Quarkus startup: class loading dominates

Startup flame graphs showed class loading as the dominant cost after years of Quarkus optimization, so the team tried stock Leyden on a Quarkus app with zero changes.

### [17:42](https://youtu.be/cbSl8UVdMVg?t=1062) First attempt: 400 ms to 200 ms, then the class-loader wall

One training request cut a simple REST app's startup from about 400 ms to 200 ms, but Leyden logged classes it could not cache: only JDK-loader classes qualify, and Quarkus's own class loaders discarded years of startup tuning. Switching to the plain uber jar dropped the time from 200 ms to 130 ms and confirmed the jackpot was real.

### [19:49](https://youtu.be/cbSl8UVdMVg?t=1189) Millisecond fixes the flame graphs exposed

With class loading gone, the team fixed waste it had never noticed: printing startup time via BigDecimal (whose static initializer costs milliseconds), UUID class loading that spun up security providers for files that should never have been created, lazy ServiceLoader use in the log manager, reflective annotation loading the team pushed Hibernate to fix (about 5 ms), and slow negative class lookups that the original Quarkus loaders had handled smartly.

### [24:55](https://youtu.be/cbSl8UVdMVg?t=1495) AOT cache requirements and training tips

Same JDK version, architecture, and OS across all phases; preserved jar timestamps; classpath as an explicit jar list (no wildcards, directories, or nested jars) with production a superset of training. For training runs: mirror the production class set, use smoke tests instead of full suites, inspect loaded classes via `-verbose:class` or JFR, and use jcmd (JDK 26, backported to 25) to dump the cache on demand from a long run.

### [29:59](https://youtu.be/cbSl8UVdMVg?t=1799) Demo: 350 ms to 80 ms, live

Andrianakis built a trivial Quarkus REST app normally (baseline runs of 385 ms and 333 ms), rebuilt it with AOT packaging enabled (producing a 38 MB `app.aot` file), and ran it with the cache: 80, 84, and 76 ms. The run used JDK 25.0.4 and Quarkus 3.40.1.

### [33:05](https://youtu.be/cbSl8UVdMVg?t=1985) How Quarkus wires Leyden in

One build flag makes Quarkus produce a special AOT jar, then reuse `@QuarkusIntegrationTest` as the training run: the app launches in a separate JVM under the Leyden workflow while tests hit it over HTTP like any client, and Quarkus assembles the final `app.aot` automatically. Quarkus can also bake the cache into its generated container image (Docker, Jib, Podman), at the cost of embedding a large binary some organizations instead mount as a volume.

### [37:46](https://youtu.be/cbSl8UVdMVg?t=2266) A large synthetic app: 3.1 s to under 1 s

On a fictitious CRUD app with a thousand JAX-RS resources and a thousand entities, startup fell from about 3.1 s to under a second, while the container image grew from 517 MB to 715 MB. The sample-app slide charted roughly 370 ms to 80 ms and 456 MB to 495 MB, citing the public sample repo.

### [39:17](https://youtu.be/cbSl8UVdMVg?t=2357) Next: AOT-compiled code in JDK 28

AOT code compilation should deliver faster startup plus adaptive peak performance without retraining when production load shifts, with no new flags for cache users (the speaker named JEP 544; the slide marked the number TBD). Andrianakis showed JIT compilation visibly slowing startup on small core counts and called near-peak performance from the first request the remaining prize. Conclusions: write integration tests now, try both workflows, and track JDK and Quarkus releases.

### [46:04](https://youtu.be/cbSl8UVdMVg?t=2764) Q&A worth keeping

No peak-performance regression from the AOT cache has been observed once peak is reached. On test coverage pressure: start from existing tests, then iterate with profiling and logs to find uncovered hot paths. Recording a running production app as profiling input was deferred to the Ask the Architects session. Most benefits arrive automatically with JDK and framework upgrades. AOT packaging shipped about six months before the talk and is in the 3.40 LTS. JLink is still experimental with no AOT integration yet. Nobody had numbers for CPU time saved at startup.

## Tools, libraries and specs

- Project Leyden (AOT cache, AOT configuration, AOT-compiled code)
- JDK 24 (three-phase workflow), JDK 25 (JEP 514 two-phase flow, JEP 515 early profiling), JDK 26 (JEP 516 GC-independent objects, jcmd cache dump), JDK 28 (AOT code, upcoming)
- `-XX:+AOTStreamableObjects`, `-verbose:class`, JFR class-load events
- Quarkus 3.40 LTS (AOT packaging, `@QuarkusIntegrationTest` as training run, container image support for Docker/Jib/Podman)
- AppCDS, ZGC, JLink

## Who should watch

Quarkus and Spring developers who care about startup time and want a concrete recipe plus measured results, and anyone evaluating Leyden adoption. Skip it if you already run Leyden in production with tuned training runs, or if you want JVM internals deeper than the workflow and object-format level.

## Verdict

**10/10**: the Quarkus team's own startup results are run live end to end with the design reasons behind them and a public sample repository, though the numbers are a few laptop runs and the large-app figures come from a slide.

**Novelty 2/2**

- **+** [17:42](https://youtu.be/cbSl8UVdMVg?t=1062) The Quarkus team's own experiments show a naive Leyden run cutting startup from 400 ms to 200 ms and the uber jar to 130 ms.
- **+** [35:07](https://youtu.be/cbSl8UVdMVg?t=2107) The engineer behind the integration explains the AOT jar design: delegate JDK class loading to the JDK loaders, keep Quarkus resource and service-file loading.
- **·** [05:44](https://youtu.be/cbSl8UVdMVg?t=344) The Leyden workflow segment restates JEP-documented material as setup for the original Quarkus work.

**Demonstrated 2/2**

- **+** [29:59](https://youtu.be/cbSl8UVdMVg?t=1799) The baseline build and runs (385 ms, 333 ms) happen live in the terminal on screen.
- **+** [32:04](https://youtu.be/cbSl8UVdMVg?t=1924) The AOT-enabled runs print 80, 84, and 76 ms in the same terminal, completing the before/after end to end.

**Measured 2/2**

- **+** [32:04](https://youtu.be/cbSl8UVdMVg?t=1924) Live before/after on the sample app with the commands and versions on screen: about 350 ms baseline against 80, 84 and 76 ms cached runs.
- **+** [10:26](https://youtu.be/cbSl8UVdMVg?t=626) The Leyden benchmark slide charts normalized elapsed time against JDK mainline for several frameworks' Hello Worlds and Spring PetClinic, sourced to openjdk/leyden and labelled as last year's snapshot.
- **−** [37:46](https://youtu.be/cbSl8UVdMVg?t=2266) The large-app figures (3.1 s to under 1 s, image 517 MB to 715 MB) are slide claims with no method shown, and the live readings are two baseline and three cached runs on a laptop.

**Depth 2/2**

- **+** [12:31](https://youtu.be/cbSl8UVdMVg?t=751) The GC-dependent heap layout behind the ZGC gap is explained, motivating the new streamable object format.
- **+** [35:07](https://youtu.be/cbSl8UVdMVg?t=2107) The AOT jar design is justified from the negative-class-lookup behavior of universal JDK loaders versus Quarkus's build-time classpath knowledge.
- **+** [43:27](https://youtu.be/cbSl8UVdMVg?t=2607) The JIT compiler firing at startup once methods pass their call threshold, and slowing startup on two to four cores, is the reason given for AOT-compiled code.

**Reusable 2/2**

- **+** [37:15](https://youtu.be/cbSl8UVdMVg?t=2235) The results slide cites the public sample project at github.com/gsmet/quarkus-aot covering the demoed app and the 1k-entity app.
- **+** [24:55](https://youtu.be/cbSl8UVdMVg?t=1495) The AOT-cache requirements and training tips (same JDK, OS and architecture, preserved jar timestamps, jar-list classpath, smoke tests, jcmd cache dump) form a checklist.
- **·** [31:02](https://youtu.be/cbSl8UVdMVg?t=1862) The AOT build property is spoken but never shown on screen, so reproducing the build needs the repo README.
