---
title: When benchmarks go bad - what we learned from measuring performance wrong
talkId: "14463"
conference: devoxx-be-2026
speakers: [Francesco Nigro, Holly Cummins]
track: Development Practices
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=yePre1hOvHE
durationMin: 54
slides: https://speakerdeck.com/hollycummins/when-benchmarks-go-bad-what-i-learned-from-measuring-performance-wrong-4eb43ba5-37df-4149-ba73-14043a029aa2
verdict: 8
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# When benchmarks go bad - what we learned from measuring performance wrong
Francesco Nigro, Holly Cummins · Conference · Development Practices
Slides: https://speakerdeck.com/hollycummins/when-benchmarks-go-bad-what-i-learned-from-measuring-performance-wrong-4eb43ba5-37df-4149-ba73-14043a029aa2

## TL;DR
The Quarkus team spent a year rebuilding their public benchmark and got almost every step wrong first; this talk turns those failures into a field guide. Its central principle is that you are often not measuring what you think you are measuring, and every design decision in a benchmark can push you there. You leave with concrete failure modes to check for, grouped under reproducibility, realism and relevance.

## Key takeaways
- Never benchmark on a laptop or with load generation sharing resources with the application: thermal throttling and contention alone can swing results by tens of percent.
- Maximizing reproducibility means deliberately slowing the machine down: disable turbo boost and deep idle states, set the scaling governor to performance, drop caches, and pin workloads to isolated cores.
- State is noise: cached container images, primed databases and warm caches make runs differ, and they affect compared systems asymmetrically, which silently corrupts A/B comparisons.
- Most popular load drivers misreport latency under stress through coordinated omission; use drivers that track scheduled send times (Gatling, wrk2, Hyperfoil) instead of JMeter or plain wrk.
- Never measure throughput and memory footprint in the same run: the JVM delays garbage collection to optimize throughput, so the two trade off directly against each other.
- Suspiciously similar results between very different systems mean you are measuring a shared bottleneck (disk, network, scheduler), not the systems.
- Validate every benchmark with active benchmarking: check resource utilization, saturation and errors (the USE method) to confirm the bottleneck is where you think it is.

## Notes

### [01:12](https://youtu.be/yePre1hOvHE?t=72) Why the Quarkus numbers went stale
Cummins explains the premise: the Quarkus website showed performance numbers against an unnamed competitor, which meant the benchmark could not be open sourced without unmasking them. About a year before the talk the team set out to refresh the numbers and open source the benchmark, expecting a small job. The talk is the story of everything that went wrong. A planned live demo of the benchmark script fails immediately because the venue Wi-Fi stalls the container downloads, which becomes the opening example of measuring nothing while appearing to measure something.

### [09:05](https://youtu.be/yePre1hOvHE?t=545) Reproducibility: same measurement, different answers
Reproducibility fails when identical measurements give different results, and the speakers put the noise from small environment problems at around 40%. Running load generation and the application on one machine is the classic anti-pattern (laptops additionally throttle cores to avoid overheating). Even servers vary per core through governors, turbo modes and power limits, so the recipe is to disable turbo boost, deep idle states and speed shift, and pin the performance governor. Caches are a second noise source: the team once benchmarked against a stale container image and primed the database with the wrong data without noticing. Fixing core isolation changed the Quarkus-vs-Spring throughput ratio from 1.8x upward, proving noise hits compared systems asymmetrically rather than cancelling out.

### [18:30](https://youtu.be/yePre1hOvHE?t=1110) Realism: the lab is nothing like production
All the reproducibility fixes make the system slower than any real deployment, which creates the opposite problem. Microbenchmarks strip away the messy context that determines real behavior; measurements need warm-up (except serverless) and a populated database, since an empty database runs gloriously fast and means nothing. Open sourcing the benchmark brought the best feedback from an unexpected source: a Spring engineer reproduced the numbers on a newer Ubuntu scheduler and got 1.4x instead of the lab's 2-3x, a 40% difference attributable to the OS scheduler alone. The lab's old hardware was kept deliberately for year-over-year stability, trading realism for reproducibility.

### [24:41](https://youtu.be/yePre1hOvHE?t=1481) Relevance: define "faster" before measuring it
Performance can mean throughput, response time, memory footprint or start time, and each maps to a different business outcome (hardware cost, user experience, elasticity). A native image starts fast but takes a throughput hit, so "faster" depends on the problem being solved. Cummins frames metrics as leading indicators for the lagging indicator of money. The bulk of this segment is a catalog of mismeasurement: response times demand full distributions (P99, not averages) and a load driver free of coordinated omission; start times must be measured as time to first request with an external polling loop, never from self-reported log lines; memory must be OS-level RSS (heap plus off-heap), measured at startup and never in the same run as throughput.

### [35:13](https://youtu.be/yePre1hOvHE?t=2113) Which load generators to trust
Nigro names names: JMeter is broken on coordinated omission (he filed yearly fix requests for seven years as an Apache member), and plain wrk cannot schedule requests by design. Safe choices are Gatling, wrk2 (by Gil Tene, who named the fallacy) and Hyperfoil, the Red Hat/IBM tool Nigro maintains, which also reports its own health so a load-generator GC pause is not blamed on the system under test. Hyperfoil has wrk2-compatible bindings to hide its complexity.

### [45:39](https://youtu.be/yePre1hOvHE?t=2739) Bottlenecks and active benchmarking
A published Spring-vs-Quarkus comparison showed near-identical throughput (338 vs 390 req/s); re-running with a faster disk multiplied performance, proving the test measured disk speed. Similarly, near-identical Quarkus-vs-Rust numbers only proved a shared bottleneck elsewhere, which usefully tells you a rewrite would buy nothing. Generating load from a second machine usually just measures the network, so the team runs everything on one machine with NUMA-aware core isolation (and podman with host networking, since the default user-space bridge is itself a single-threaded bottleneck). The fix is Brendan Gregg's active benchmarking with the USE method: check utilization, saturation and errors per resource. Errors matter most: Spring's keep-alive connection drops were silently reducing the load pushed, and another three-orders-of-magnitude anomaly traced to a reactive-stack error. The segment runs over time and the last example is skipped.

## Tools, libraries and specs
- Hyperfoil (Red Hat/IBM load generator, wrk2-compatible bindings)
- Gatling, wrk2 (coordinated-omission-free load generators)
- JMeter, wrk (flagged as unsafe for latency measurement)
- Quarkus (JVM and native image) vs Spring (benchmark subject)
- USE method and active benchmarking (Brendan Gregg)
- Coordinated omission (Gil Tene)

## Who should watch
Anyone who runs benchmarks or load tests, compares frameworks, or makes decisions from performance numbers gains directly applicable checks. Teams choosing between runtimes (Spring vs Quarkus, JVM vs native vs Rust) get the failure modes behind most published comparisons. Skip it if you already practice active benchmarking with coordinated-omission-free tooling; the concepts will be familiar, though the war stories still entertain.

## Verdict
**8/10**: First-hand benchmark failures with before/after numbers and two worked mechanisms (coordinated omission, RSS against throughput), limited by the failed live demo and by setup recipes that are spoken rather than published.

**Novelty 2/2**

- **+** [23:07](https://youtu.be/yePre1hOvHE?t=1387) The OS-scheduler story shows the same benchmark giving 1.4x on a new Ubuntu scheduler versus 2-3x on the lab's old kernel, a 40% swing found through the competitor's reproduction of the team's benchmark.
- **+** [17:29](https://youtu.be/yePre1hOvHE?t=1049) Fixing core isolation improved the Quarkus-vs-Spring ratio from 1.8x upward, showing asymmetric noise from their own benchmark.
- **+** [15:56](https://youtu.be/yePre1hOvHE?t=956) The stale-container-image incident, where the database was primed with unknown data, is first-hand failure evidence no search result provides.

**Demonstrated 1/2**

- **+** [46:10](https://youtu.be/yePre1hOvHE?t=2770) The Spring-vs-Quarkus table (338 vs 390 req/s initial test) is shown on screen with its source blog URL; it is a recorded result, not a live run.
- **−** [04:22](https://youtu.be/yePre1hOvHE?t=262) The central live demo never runs: the benchmark script stalls downloading containers over the venue Wi-Fi and is abandoned.

**Measured 2/2**

- **+** [17:10](https://youtu.be/yePre1hOvHE?t=1030) The results chart compares Quarkus and Spring (18,927 vs 10,104 tps, 272 vs 507 MiB RSS) with versions, memory setting and run date in its footer.
- **+** [23:07](https://youtu.be/yePre1hOvHE?t=1387) The scheduler comparison gives both numbers (1.4x vs 2-3x) with the differing setup stated for each side.
- **−** [10:41](https://youtu.be/yePre1hOvHE?t=641) The headline "about 40%" reproducibility noise is stated without a method or baseline.

**Depth 2/2**

- **+** [33:04](https://youtu.be/yePre1hOvHE?t=1984) Coordinated omission is walked through request by request, showing why queued-behind requests must count the full 20 seconds.
- **+** [44:04](https://youtu.be/yePre1hOvHE?t=2644) The RSS-versus-throughput trade-off is explained through JVM GC behavior: the runtime fills all available memory to delay collection.
- **+** [24:10](https://youtu.be/yePre1hOvHE?t=1450) The lab keeps old hardware and an old kernel for year-over-year stability, a reproducibility-over-realism trade-off stated with its reason.

**Reusable 1/2**

- **+** [40:28](https://youtu.be/yePre1hOvHE?t=2428) The time-to-first-request polling loop is shown as a complete shell script on the slide.
- **+** [21:04](https://youtu.be/yePre1hOvHE?t=1264) The benchmark is open source, and its repository quarkusio/spring-quarkus-perf-comparison is named on deck slide 6.
- **−** [14:21](https://youtu.be/yePre1hOvHE?t=861) The reproduction recipe (turbo boost, governor, cache drop, core pinning) is given in speech for the viewer to reconstruct, with no repository walk-through or checklist on video.
