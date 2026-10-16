---
title: "GraalVM Next: Layers, Crema, and WebAssembly in Action"
talkId: "24212"
conference: devoxx-be-2026
speakers: [Alina Yurenko, Thomas Wuerthinger]
track: Development Practices
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=OLQ98Ko4p3Q
durationMin: 47
slides: null
verdict: 7
reach: segment
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# GraalVM Next: Layers, Crema, and WebAssembly in Action
Alina Yurenko, Thomas Wuerthinger · Conference · Development Practices

## TL;DR
Alina Yurenko and GraalVM project lead Thomas Wuerthinger present three Native Image projects that attack the same observation: in a typical app only about 3% of loaded classes are user code. Native Image Layers shares the other 97% between apps, Project Crema loads new classes at runtime in a native binary, and Web Image compiles JVM apps to WebAssembly; each claim is backed by a live demo with measured numbers.

## Key takeaways
- Only 3% of loaded classes in the Micronaut Pet Clinic sample are user code, so GraalVM now optimizes the shared 97% (JDK, framework, libraries) instead of chasing the next 10% on single images.
- Native Image Layers compiles the shared base once and thin app layers on top; ten Micronaut apps on one base dropped per-app proportional memory from ~100 MB to ~30 MB.
- Project Crema breaks the closed-world assumption: a native binary with a bytecode interpreter plus JIT can load classes that did not exist at build time, including ByteBuddy-generated ones.
- A Crema-built Java source launcher compiles and runs a Java file in ~36 ms, about 7x faster than the regular launcher, which makes script-style Java competitive with Python or JavaScript on startup.
- Web Image transpiles a real Spring Boot app (an 18 MB .wasm music player) to run in the browser, which opens deployment targets where no native binary can run.
- Compatibility work has moved to automation: the reachability-metadata repository now covers ~2,000 libraries (~30k versions) with AI-generated tests, and AI skills teach coding agents to use the Native Image build tools.

## Notes

### [01:05](https://youtu.be/OLQ98Ko4p3Q?t=65) GraalVM recap and release pace
Yurenko recaps the three pillars: Native Image ahead-of-time compilation, the JIT compiler, and the polyglot runtimes (JavaScript, Python, Truffle languages), plus GraalVM JavaScript embedded in Oracle Database. Releases now ship monthly; compiling the same Micronaut Pet Clinic with 25.0 versus 25.4 gave a 33% smaller image and 22% lower RSS with default settings, no GC tuning and no PGO. Wuerthinger adds that 32-bit object headers have been the default for a long time, which is part of the memory advantage.

### [06:43](https://youtu.be/OLQ98Ko4p3Q?t=403) Compatibility: AI skills and the metadata repository
Build times and configuration friction are named as the top complaints. The team ships AI skills (installable in coding agents) that know to use the Native Image build tools and the reachability-metadata repository, a Maven-Central-like collection of reflection/resource/proxy configurations. The repo holds ~2,000 libraries across ~30k versions; AI agents generate tests per library, measure coverage, derive the configuration and verify it in a native image. Missing a library: file an issue with Maven coordinates and the team's agents generate the config.

### [11:53](https://youtu.be/OLQ98Ko4p3Q?t=713) Native Image Layers: share the base
Measuring Pet Clinic showed 3% user classes versus 97% JDK/framework/library classes, so a second app on the same stack recompiles nearly the same code. Layers split the app from its base: the base (JDK, framework, dependencies) is compiled once, and each app is a thin layer on top that maps to Docker image layers. The live demo runs ten Micronaut greeting apps (2 MB each) on one ~200 MB base: a single instance uses ~100 MB proportional set size, while ten instances average ~30 MB PSS each (1.1 GB RSS total, ~291 MB PSS total), since the base pages are shared. Platform teams could ship blessed base images for a company-wide stack.

### [20:19](https://youtu.be/OLQ98Ko4p3Q?t=1219) Project Crema: runtime class loading in native images
User code measured only ~1.72% of CPU time in their samples, so Crema stops compiling it ahead of time: a new experimental flag embeds a bytecode interpreter in the native binary, reusing the open-world compilation machinery built for base layers. Newly loaded classes that get hot are JIT-compiled like on HotSpot, and fast startup is preserved. Three demos run live: a Micronaut app executing ByteBuddy-generated greeting classes with new names per run (~10 ms total); a precompiled `java.base` + `javac` source launcher running `HelloCrema.java` in 35.7 ms mean over 63 hyperfine runs; and a precompiled Micronaut runtime serving a controller supplied as source (edit-to-response ~150 ms) or as a jar (64 ms startup). The jar-on-precompiled-runtime model suits companies that want Docker-base-style deployment without per-app native builds.

### [35:28](https://youtu.be/OLQ98Ko4p3Q?t=2128) Web Image: Spring Boot in the browser
Native Image can emit WebAssembly instead of a native binary for targets that accept only Wasm (browsers, some edge runtimes). The demo shows a plain Spring Boot + Thymeleaf music-player app ("mytunes", written by colleague Patrick) compiled to an 18 MB `.wasm` plus a JS wrapper; it plays music in the browser on stage. The point stressed on screen: this is a full framework app, not a toy example.

### [40:08](https://youtu.be/OLQ98Ko4p3Q?t=2408) Releases, roadmap and community
Stay on the monthly 25.x feature releases for performance and security fixes; a stable 25.0 baseline gets security updates for conservative environments. Upcoming: a new precompiled-Micronaut-runtime framework built with the Micronaut team (script your logic in Java, Python or JavaScript on top of an AOT core), more polyglot and Wasm work, and Amazon's contribution integrating the Shenandoah GC into Native Image (hello-world stage). The public roadmap lives on GitHub, and AI-assisted pull requests are accepted under a policy requiring the author to own the submitted code.

## Tools, libraries and specs
- GraalVM 25.x (Native Image, JIT, Truffle polyglot runtimes)
- Native Image Layers (experimental)
- Project Crema (experimental runtime class loading)
- Web Image (Java to WebAssembly)
- GraalVM Reachability Metadata Repository (~2,000 libraries)
- Native Image build tools (Maven/Gradle plugins)
- ByteBuddy (runtime code generation in the Crema demo)
- Micronaut (Pet Clinic sample, layered and Crema demos)
- Spring Boot + Thymeleaf ("mytunes" Web Image demo)
- hyperfine (live benchmarking)
- Shenandoah GC (upcoming Native Image integration, contributed by Amazon)

## Who should watch
JVM developers tracking where Native Image is headed, teams running fleets of microservices on a shared stack, and anyone blocked by the closed-world assumption (ByteBuddy, plugins, scripting). Skip it if you need production-ready guidance on stable features only: Layers, Crema and Web Image are experimental and fast-moving.

## Verdict
**7/10**: three experimental projects shown running live with a baselined memory measurement for Layers, held at Novelty 1 because the speakers are the project's authors and its design is public, with survey-level Web Image and a reusable artifact for only one of three demos.

**Reach segment**: teams shipping JVM services as Native Images on a shared stack can use Layers, and the subset blocked by the closed-world assumption or targeting browsers can use Crema and Web Image.

**Novelty 1/2**

- **+** [22:23](https://youtu.be/OLQ98Ko4p3Q?t=1343) The authors place Crema in the years of user requests for ByteBuddy with Native Image that it now answers.
- **+** [34:54](https://youtu.be/OLQ98Ko4p3Q?t=2094) The talk frames one decision rule across the projects: stable parts compiled ahead of time and shared, frequently changing parts loaded dynamically and JIT-compiled.
- **−** The public Crema issue oracle/graal#11327 already describes the interpreter built on Native Image Layers and the AOT base with runtime-loaded user code, so a search for the project returns the core of the Crema material.

**Demonstrated 2/2**

- **+** [15:36](https://youtu.be/OLQ98Ko4p3Q?t=936) Ten layered Micronaut apps start on one shared base with per-process RSS and PSS printed on screen.
- **+** [23:28](https://youtu.be/OLQ98Ko4p3Q?t=1408) A native binary loads and runs ByteBuddy classes generated after the build, with new timestamped class names per run.
- **+** [38:33](https://youtu.be/OLQ98Ko4p3Q?t=2313) A Spring Boot music app compiled to WebAssembly plays music in the browser on stage.

**Measured 2/2**

- **+** [04:42](https://youtu.be/OLQ98Ko4p3Q?t=282) The same Micronaut Pet Clinic built with GraalVM 25.0 and 25.4 under default settings gives a 33% smaller image and 22% lower memory.
- **+** [18:45](https://youtu.be/OLQ98Ko4p3Q?t=1125) One layered instance uses about 100 MB PSS against about 30 MB per instance across ten, sampled with system-level tools.
- **−** [29:42](https://youtu.be/OLQ98Ko4p3Q?t=1782) The "7x faster than the regular Java source launcher" and "30x CPU consumption" claims come with no run of the regular launcher, only the 35.7 ms hyperfine result for Crema.

**Depth 1/2**

- **+** [14:00](https://youtu.be/OLQ98Ko4p3Q?t=840) Layers are explained as a base compiled once with thin app layers on top that map onto Docker image layers.
- **+** [21:52](https://youtu.be/OLQ98Ko4p3Q?t=1312) Crema is explained as a bytecode interpreter compiled into the image reusing the open-world machinery built for base layers, with hot classes JIT-compiled.
- **−** [35:58](https://youtu.be/OLQ98Ko4p3Q?t=2158) Web Image gets a what-and-demo treatment with no mechanism or limits beyond naming the browser and Cloudflare as targets.

**Reusable 1/2**

- **+** [39:05](https://youtu.be/OLQ98Ko4p3Q?t=2345) The mytunes Spring-to-Wasm demo app is on GitHub and can be built and run by the viewer.
- **·** [34:23](https://youtu.be/OLQ98Ko4p3Q?t=2063) The invitation to build with Crema names no repository or sample, and none is pointed to for the Layers demos either.
