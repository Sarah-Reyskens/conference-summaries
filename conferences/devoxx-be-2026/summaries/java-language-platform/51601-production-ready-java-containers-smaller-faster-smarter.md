---
title: "Production-Ready Java Containers: Smaller, Faster, Smarter"
talkId: "51601"
conference: devoxx-be-2026
speakers: [Albert Attard]
track: Java Language & Platform
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=LPhGSgO5eKE
durationMin: 48
slides: null
verdict: 7
reach: broad
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Production-Ready Java Containers: Smaller, Faster, Smarter

Albert Attard · Conference · Java Language & Platform

## TL;DR

Attard makes Java containers production-ready end to end: reproducible base images, layered builds, jlink runtimes, AOT caches, memory tuning, and hardening. Each technique ships with a measured before/after, and the refrain is to measure every flag because unmeasured tuning becomes folklore.

## Key takeaways

- Tune via `JDK_JAVA_OPTIONS` so one image runs differently per environment without rebuilding; agents need `JAVA_TOOL_OPTIONS`, read earlier by the VM.
- Pin base images by digest: the bytes behind `jdk:25` change with every update.
- Layer the jar (56 MB dependencies cached, 18 KB app code last) so code changes rebuild only the final layer.
- jlink the runtime but keep `jdk.management.agent` and `jdk.jfr`, or lose `jcmd` and Flight Recorder.
- The demo AOT cache cut startup from 3 s to under 1 s, valid only when run-time classpath order matches generation order.
- Set `-XX:MaxRAMPercentage` (75% here): the JVM defaults to 25% of container memory.
- Separate the kernel OOM killer from Java `OutOfMemoryError`; ship `-XX:+ExitOnOutOfMemoryError` with a heap dump path.

## Notes

### [03:09](https://youtu.be/LPhGSgO5eKE?t=189) Passing JVM options into containers

`_JAVA_OPTIONS` overrides the command line. `JDK_JAVA_OPTIONS` applies at run time, so one image runs tuned per deployment. Agents must go in `JAVA_TOOL_OPTIONS`, read at an earlier VM phase. `JAVA_OPTS` is not read by the VM. A `@file` argument file (one option per line) is the last option.

### [06:16](https://youtu.be/LPhGSgO5eKE?t=376) Pin images and layer the application

Floating tags are mutable, so pin the digest: a changed upstream image then fails the build instead of slipping in. A `dive` inspection shows the fat-jar problem: one changed line rebuilds a 56 MB layer. Extracting Spring Boot's four layers keeps dependencies cached and makes the app layer 18 KB; the app layer goes last.

### [12:35](https://youtu.be/LPhGSgO5eKE?t=755) Custom runtimes with jlink

Since Java 9 the JRE is replaced by a jlink runtime with only needed modules; files absent from the image cannot be exploited. The multi-stage build creates the runtime from the Oracle JDK image and copies it onto Oracle Linux, adding back `jdk.management.agent` and `jdk.jfr` for `jcmd` and Flight Recorder.

### [17:16](https://youtu.be/LPhGSgO5eKE?t=1036) Slim the OS and ship multi-arch

The OS layer shrinks from Oracle Linux Slim (~100 MB) to distroless (~28 MB) to `FROM scratch` (~6 MB, only the runtime's native libraries). Both manifests carry AMD64 and ARM64 entries, so one tag plus `--platform` builds for either.

### [22:32](https://youtu.be/LPhGSgO5eKE?t=1352) AOT caches and startup

On the unchanged demo jar: ~3.0 s executable jar, ~2.5 s explicit classpath, under 1 s with the AOT cache. Since Java 25 the flow is two phases: run once to generate the cache, then run consuming it. The catch is classpath order: with split packages, swapping jar order can pick a different class and silently invalidate the cache. The Dockerfile sorts dependencies into one args file used for both runs. `AOTMode=on` fails fast on cache miss; production may prefer it off.

### [29:22](https://youtu.be/LPhGSgO5eKE?t=1762) Compact object headers

Default headers are 12 bytes, compact 8, with 8-byte alignment padding. A fieldless record halves its footprint; with three fields padding erases the gain. On a stress-tested web app the flag raised throughput from ~5400 to ~5680 req/s and cut latency from 15 ms to 14 ms by triggering GC less often. Opt-in on 25, default-on in 27.

### [32:55](https://youtu.be/LPhGSgO5eKE?t=1975) Know the JVM defaults inside a cgroup

A 1 GB container with no flags runs the Serial GC with a 256 MB heap: the JVM takes one quarter of memory by default. `-XX:MaxRAMPercentage=75` makes the heap track the container size, which the speaker calls the most common customer mistake.

### [36:35](https://youtu.be/LPhGSgO5eKE?t=2195) OOMKilled versus OutOfMemoryError

The kernel OOM killer ends PID 1 when the container exceeds its cgroup limit; `OutOfMemoryError` means the heap is exhausted. A 256 MB container with a 256 MB heap starts (the JVM has not touched the memory yet) and dies on first load; `-XX:+AlwaysPreTouch` moves allocation to startup so it fails immediately. The Java-side failure can leave the app alive but unstable, hence `-XX:+ExitOnOutOfMemoryError` with a heap dump path.

### [40:50](https://youtu.be/LPhGSgO5eKE?t=2450) Lifecycle and probes

Readiness and liveness probes gate traffic until the app can serve; shutdown drains in-flight work first (15 seconds in the Spring example).

### [42:24](https://youtu.be/LPhGSgO5eKE?t=2544) Harden the image

Copy files as root with world-readable permissions, run as UID 1001, mount read-only with only `tmpfs` writable, write diagnostics to a separate volume, and drop Linux capabilities.

## Tools, libraries and specs

- jlink (JDK 25) with `jdk.management.agent` and `jdk.jfr` retained
- Java 25 AOT cache (`AOTCache`, `AOTMode`) and CDS
- Compact object headers (`-XX:+UseCompactObjectHeaders`; default-on in 27)
- Oracle Container Registry: `container-registry.oracle.com/java/jdk:25.0.4.1`, Oracle Linux 10 Slim, distroless base
- Spring Boot layered jars, multi-stage Docker builds, `dive`
- `-XX:MaxRAMPercentage`, `-XX:+AlwaysPreTouch`, `-XX:+ExitOnOutOfMemoryError`, `-XX:+HeapDumpOnOutOfMemoryError`

## Who should watch

Beginners containerizing Java who want one checklist for image size, startup, memory, and hardening. Engineers already tuning AOT, headers, and cgroup flags can skim the charts instead.

## Verdict

**7/10**: A beginner production-container checklist with baselined measurements and explanations of the mechanisms, limited by optimization results presented as charts and examples without a published reproduction artifact.

**Reach broad**: Most of the conference audience ships Java services in containers and can apply the image, startup, memory and hardening practices in their own work.

**Novelty 1/2**

- **+** [45:01](https://youtu.be/LPhGSgO5eKE?t=2701) Image pinning, dependency layering, jlink modules, the AOT cache, environment-variable tuning, memory limits and hardening are recapped as one decision flow for a production container.
- **+** [36:03](https://youtu.be/LPhGSgO5eKE?t=2163) Customer visits reveal a recurring deployment mistake: teams enlarge containers instead of adjusting the default heap allocation.

**Demonstrated 1/2**

- **+** [35:25](https://youtu.be/LPhGSgO5eKE?t=2125) The `PrintFlagsFinal` output on screen exposes the heap, memory-percentage and garbage-collector defaults inside the container.
- **+** [39:45](https://youtu.be/LPhGSgO5eKE?t=2385) The container inspection output shows `OOMKilled` true after the worked memory-limit failure.
- **−** [18:18](https://youtu.be/LPhGSgO5eKE?t=1098) The image-size optimization is presented as a comparison chart rather than an end-to-end build and run with its output visible.

**Measured 2/2**

- **+** [23:37](https://youtu.be/LPhGSgO5eKE?t=1417) Startup on the same jar and machine reads about 3.0 s for the fat jar, 2.5 s for the explicit classpath and under 1 s with the AOT cache.
- **+** [11:00](https://youtu.be/LPhGSgO5eKE?t=660) A `dive` inspection compares the 56 MB fat-jar layer with a layered image whose dependencies occupy 56 MB and application layer occupies 18 KB.
- **−** [31:25](https://youtu.be/LPhGSgO5eKE?t=1885) Compact headers lift throughput from about 5,400 to about 5,700 req/s with latency from 15 ms to 14 ms, but "I did a stress test" names no tool, load or machine.

**Depth 2/2**

- **+** [25:12](https://youtu.be/LPhGSgO5eKE?t=1512) Split packages explain why classpath order changes application identity and invalidates the cache of loaded and linked classes.
- **+** [29:53](https://youtu.be/LPhGSgO5eKE?t=1793) Header layout and alignment padding explain when compact headers save space and when padding erases the gain.
- **+** [36:35](https://youtu.be/LPhGSgO5eKE?t=2195) Heap exhaustion and the kernel's container-memory enforcement are separated by mechanism, explaining why a Java `OutOfMemoryError` differs from a killed container.

**Reusable 1/2**

- **+** [12:03](https://youtu.be/LPhGSgO5eKE?t=723) The multi-stage Spring layered Dockerfile is complete on a slide, with the layers extracted and the application layer last.
- **−** [19:20](https://youtu.be/LPhGSgO5eKE?t=1160) The from-scratch Dockerfile omits the library-copying step, and the speaker offers the full example on request rather than pointing to a published artifact.
