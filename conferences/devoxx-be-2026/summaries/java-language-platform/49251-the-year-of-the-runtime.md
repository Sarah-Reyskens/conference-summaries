---
title: The Year of the Runtime
talkId: "49251"
conference: devoxx-be-2026
speakers: [Ron Pressler]
track: Java Language & Platform
sessionType: Keynote
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=tle2mA7EwWU
durationMin: 15
slides: null
verdict: 6
reach: broad
frames: 6
summarizedAt: 2026-10-14
reviewedAt: 2026-10-15
---

# The Year of the Runtime

Ron Pressler · Keynote · Java Language & Platform

## TL;DR

AI agents write all mainstream languages about equally well, which shifts importance from syntax to what the runtime provides. Pressler argues the JVM resolves the tension between maintainability and performance by moving compilation to runtime, then tours ZGC, Valhalla, Leyden, integrity by default, and JFR telemetry.

## Key takeaways

- Java is about 5% syntax tooling and 95% runtime; JDK upgrades bring speed and observability gains without changing the programming model.
- Generational ZGC removes GC pauses; a Netflix plot shows latency dropping exactly at switchover.
- Leyden's AOT cache cuts startup and warmup; the upcoming code cache starts programs near peak performance.
- Ship a jlink-built minimal runtime (~35 MB) instead of the full JDK.
- AI agents already know how to use JFR telemetry and analyze recordings, which makes its depth more valuable.

## Notes

### [00:35](https://youtu.be/tle2mA7EwWU?t=35) AI writes every language, but software must evolve

Programs are mechanically verifiable to a degree, yet never ship on tests alone: they must evolve, and no procedure verifies evolvability. javac and jshell are ~5% of the JDK; the rest is the runtime, a layer between code and hardware that keeps programs fast and secure as they evolve by compiling at runtime.

### [05:13](https://youtu.be/tle2mA7EwWU?t=313) GC, memory, and Leyden

Generational ZGC (JDK 21) removed pauses; the Netflix error-rate plot (current vs. 24h prior) drops at switchover. Upcoming JEP 546 auto-sizes the heap. JDK 27 cut object headers to 64 bits; Valhalla flattens objects into arrays, removing pointer chasing. Leyden caches profiling data (JDK 27) and soon compiled code: first-iteration warmup drops from ~1.35 s to ~0.3 s, and startup time to first request falls to 0.19–0.33 of baseline across five frameworks.

### [09:53](https://youtu.be/tle2mA7EwWU?t=593) jlink, integrity, JFR, and the AI case

Ship a jlink-built minimal runtime (~35 MB). Integrity by default (e.g., reflection can't mutate final fields) blocks vulnerabilities and enables optimizations. JFR telemetry, now with CPU profiling, cross-machine context, and CLI views, is used and analyzed well by AI agents. Agents handle self-contained tasks but falter at evolving large programs; the runtime's local-change evolution, security, and telemetry serve them as well as people.

## Tools, libraries and specs

- Generational ZGC (JDK 21), JEP 546, JDK 27, Valhalla, Leyden, jlink, JFR with views and CLI

## Who should watch

## Verdict

**6/10**: Roadmap keynote with production ZGC evidence and Leyden benchmark charts that state setup and baseline, but nothing runs on screen and jlink and JFR views come as slide fragments with no walkthrough.

**Reach broad**: most Java developers in the audience can use the JDK upgrade, jlink, and JFR gains in their own services within the year.

**Novelty 1/2**

- **+** [13:05](https://youtu.be/tle2mA7EwWU?t=785) Pressler reports his own year of heavy AI use: strong on self-contained tasks, weaker at evolving large programs while keeping them fast.
- **+** [14:08](https://youtu.be/tle2mA7EwWU?t=848) The keynote argues that if AI makes the language less important, runtimes become more important, which is his own case for the JVM.
- **−** The Leyden warmup and startup charts are the JEP 544 AOT code figures, the Netflix error-rate plot is from Netflix's 2024 Tech Blog post on Generational ZGC, and the Valhalla, JEP 546 and object-header items are public JEP and release material.

**Demonstrated 1/2**

- **·** A 15-minute morning keynote with no demo slot, whose argument rests on production and benchmark evidence, and whose headline items (Valhalla, the Leyden code cache, JEP 546) are not in a released JDK.

**Measured 2/2**

- **+** [06:16](https://youtu.be/tle2mA7EwWU?t=376) The Netflix plot overlays a service's error rate against the same metric from an earlier period (24 hours prior in the speaker's words), with the drop aligned to the ZGC switchover.
- **+** [09:04](https://youtu.be/tle2mA7EwWU?t=544) The Leyden charts state "Linux/x64 (2 cores)" and compare no AOT, AOT cache and AOT cache plus code across 20 warmup iterations and five framework startups.
- **−** [02:39](https://youtu.be/tle2mA7EwWU?t=159) The "5% of the JDK is syntax tooling, 95% runtime" figure comes with no counting method or JDK version.

**Depth 1/2**

- **+** [03:41](https://youtu.be/tle2mA7EwWU?t=221) The talk states the tension between maintainability and performance and why GCs and JITs act as optimizers, resolved by moving compilation to runtime.
- **+** [10:27](https://youtu.be/tle2mA7EwWU?t=627) Integrity by default carries its rationale: reflection cannot mutate final fields by default, so the compiler can assume certain properties always hold.
- **−** [06:48](https://youtu.be/tle2mA7EwWU?t=408) JEP 546's automatic heap sizing, the 64-bit object header and Valhalla's flattening are stated as outcomes without the mechanism or the trade-offs involved.

**Reusable 1/2**

- **+** [09:53](https://youtu.be/tle2mA7EwWU?t=593) The jlink advice is a specific practice: build a runtime with only the JDK modules you need, with a java.base-only runtime at about 35 MB.
- **+** [12:03](https://youtu.be/tle2mA7EwWU?t=723) Slide 22 shows the command `jfr view allocation-by-site recording.jfr` with its allocation-by-site output.
- **−** [09:53](https://youtu.be/tle2mA7EwWU?t=593) No jlink invocation, repository or checklist is pointed to, so the viewer reconstructs the practice.

