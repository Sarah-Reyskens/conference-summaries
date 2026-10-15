---
title: Ask the Architects
talkId: "23536"
conference: devoxx-be-2026
speakers: [Gavin Bierman, Maurizio Cimadamore, Per-Åke Minborg, Viktor Klang, Alan Bateman, Georges Saab]
track: Java Language & Platform
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=ewCPBgOrLAE
durationMin: 51
slides: null
verdict: 6
frames: 5
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Ask the Architects

Gavin Bierman, Maurizio Cimadamore, Per-Åke Minborg, Viktor Klang, Alan Bateman, Georges Saab · Conference · Java Language & Platform

## TL;DR

Oracle's Java engineers take 50 minutes of unscripted audience questions spanning virtual-thread scheduling, API deprecation policy, coding agents, strings, value objects, modules, and ZGC. The recurring message: describe your concrete problem on the relevant OpenJDK mailing list, because several requested features (custom schedulers, string views, module fixes) are blocked on understanding real use cases rather than on will.

## Key takeaways

- Custom virtual-thread schedulers stay unexposed: the runtime cannot safely call out to user scheduling code from locking, timer, and socket paths, and multiple pools would fight each other.
- Report Loom pain to the loom-dev mailing list with the concrete problem; people reflective-hacking scheduler internals is exactly what keeps the experimental API open.
- Deprecation and removal decisions rest on static analysis of hundreds of thousands of Maven artifacts, not on telemetry from your JVM; removals are rare and ship with a standalone migration path.
- Model vendors train mostly on old Java, so generated code skews toward old idioms; use feedback channels and prompt explicitly for modern constructs.
- Java 28 previews value objects (JEP 401) with no layout or flattening guarantees in the spec; VM layout-print flags are the only inspection tooling.
- ZGC gets automatic, dynamic heap sizing (including shrinking when other processes want memory) aimed at JDK 28; ZGC is recommended for most programs but will not become the default soon.

## Notes

### [00:33](https://youtu.be/ewCPBgOrLAE?t=33) Intros and ground rules

The moderator introduces the panel: David Simms (JVM, Valhalla internals, Babylon), Gavin Bierman (Amber, language), Alan Bateman (Loom, libraries), Georges Saab (OpenJDK chair), Viktor Klang, Ron Pressler, and Per-Åke Minborg (performance). Questions come from the floor through two roaming microphones.

### [02:06](https://youtu.be/ewCPBgOrLAE?t=126) Virtual threads: one carrier pool, no custom schedulers yet

Asked whether virtual threads will get separate carrier-thread groups per application area, Bateman says no exposed custom-scheduler feature is planned, though the door is not closed. The obstacle is that locking, timers, and socket operations would have to call out to scheduler code controlled by someone else. Out of the box there is only configuration of carrier-thread counts, which has covered the vast majority of migrations. Klang adds that per-library pools mostly buy expensive handovers: with N pools and fewer cores than threads, the OS still schedules everything and the hoped-for priority never materializes. Francesco (Red Hat, Netty committer) reports from a year of implementing against the experimental API that matching ForkJoinPool behavior is brutally complex, and that his Netty work now converges back toward a single pool. The panel asks for problem reports on the Loom list so any solution fits more than the Netty case.

### [09:22](https://youtu.be/ewCPBgOrLAE?t=562) How the JDK decides what to deprecate and remove

Deprecation is case-by-case, usually once a better API exists to point developers at; for decades only actively harmful APIs qualified, and the bar has relaxed somewhat. Removals are rare because they break builds: some APIs stay deprecated for 20-plus years, Thread.stop was resppecified to throw instead of removed, and the Java EE divorce plus Nashorn shipped with standalone continuations. Impact is quantified by static analysis of Maven Central artifacts, not by runtime telemetry (the one telemetry source is the opt-in VS Code extension). Vector stays untouched because so many early JDK APIs take or return it that the blast radius of any change spans the platform. A suggestion to hide old APIs from compilation while keeping them at runtime goes nowhere: multi-release compilation is precisely why signatures must stay.

### [17:43](https://youtu.be/ewCPBgOrLAE?t=1063) Making Java better for coding agents

On what would help coding agents, one panelist points at build tooling: agents benefit most from a fast build-test cycle, and work is underway there. Javadoc keeps its value both as human documentation and as agent context, with the in-progress `@note` JEP set to make code examples first-class so agents can scrape vetted examples. The panel is skeptical that any single tool (such as wiring the VS Code language server into agents) would be a large improvement, since agents already dig through dependencies and decompile with `javap`. Model vendors told the team they know they train on old Java because good modern code rarely sits on GitHub, and they read every piece of user feedback, so developers should report bad generations.

### [24:00](https://youtu.be/ewCPBgOrLAE?t=1440) Do agents shift priorities from syntax to runtime?

More JDK engineers work on the runtime than the language, and that continues; within the language, pure syntactic sugar loses some priority while semantic features gain, though an internal experiment found Java 25 idioms used about 20% fewer tokens than Java 8 for the same generated programs. The panel argues the shift is small because AI needs align with the existing direction: expressive syntax states intent, which lets the runtime optimize, check integrity, and avoid mistakes (a record gives correct equals and hashCode to silicon and carbon authors alike). Java's historic bet on readability over writability now pays off for review-heavy, agent-assisted workflows.

### [29:12](https://youtu.be/ewCPBgOrLAE?t=1752) Zero-copy string views and the string minefield

A serialization-library author asks for zero-copy String views over memory segments. Minborg and Cimadamore call string internals a minefield: a segment view over a string's bytes handed to native code could scribble on an immutable string, and copying collectors move the backing array. JDK 27 already removed the intermediate allocation when copying strings into segments with a compatible coder. A follow-up asks for a public ASCII/latin fast-path query for HTTP header coding; the panel says charset encoders have been ASCII-optimized for years and asks for the specific use case on the mailing list, noting the C++ optimization playbook does not transfer directly.

### [36:57](https://youtu.be/ewCPBgOrLAE?t=2217) Value objects land, but no timeline for what follows

Asked whether value objects previewing in Java 28 implies a timeline for primitive specialization or reified generics, the answer is a flat no. Class-file API experiments with hand-rolled specialization are possible today, and prototyping cost in calendar time has dropped, but no dates are offered.

### [37:58](https://youtu.be/ewCPBgOrLAE?t=2278) Modules usability work stays quiet for now

Module usability work is confirmed but undisclosed: the team wants something concrete to present before opening the floodgates to conflicting early opinions. The goal is framed as making modules capable enough that developers want them (integrity, security, new capabilities) rather than merely friendlier, with build-tool friction addressed once demand grows. Several discovered vulnerabilities would have been contained by the module system.

### [41:35](https://youtu.be/ewCPBgOrLAE?t=2495) Inspecting value-class layout: VM flags, no API

Flattening and scalarization are deliberately absent from the JEP 401 spec so other VMs are not bound by HotSpot layout choices, and no reliable programmatic layout-introspection API is planned. For analysis, HotSpot offers `-XX` layout-printing flags (PrintInlineLayout or its renamed successor) to dump value-class layouts for benchmarking and verification, just without any layout guarantee.

### [44:14](https://youtu.be/ewCPBgOrLAE?t=2654) String templates: why JEP 465 was pulled

String templates (JEP 465) were withdrawn from the language mainly for lack of compositionality: nested templates were processed eagerly, forcing double processing and blocking the two-pass approach (inspect the template shape and plan validation first, then validate dynamic arguments as they arrive) that string concatenation already enjoys. Nested templates must stay open as templates until final processing so the whole structure can be parsed and validated at once. A more powerful replacement proposal is in progress.

### [46:49](https://youtu.be/ewCPBgOrLAE?t=2809) Builders as the counterpart of deconstruction

Asked about declarative construction support to match record deconstruction (a Lombok-builder replacement for large objects), Bierman says the team is playing with ideas but nothing is ready to describe.

### [47:22](https://youtu.be/ewCPBgOrLAE?t=2842) ZGC: automatic heap sizing and the default question

The panel highlights automatic heap sizing for ZGC, hoped for JDK 28: it removes GC sizing flags by growing or shrinking the heap dynamically from allocation rate and CPU consumption, including shrinking when other processes on the machine want memory ("being a good neighbor", at the cost of CPU). G1 should follow; serial and parallel depend on external OpenJDK contributors. ZGC will likely become the default one day but not soon, since silently changing the GC for everyone who never set one demands certainty of no regressions. (And it was never "zero" GC: Z is for the last collector you will ever need.)

## Tools, libraries and specs

- Project Loom virtual threads and the experimental custom-scheduler API (loom-dev mailing list for feedback)
- JEP 401 (value objects, preview in Java 28)
- JEP 465 (string templates, withdrawn)
- `@note` Javadoc JEP (in progress, code examples as notes)
- ZGC automatic/dynamic heap sizing (targeted at JDK 28), G1 to follow
- `-XX` value-layout printing flags (HotSpot diagnostics)
- Inside Java podcast (follow-up interviews with panelists)

## Who should watch

Java developers who want authoritative yes/no/why answers on Loom scheduling, deprecation policy, strings, value objects, modules, and GC direction, plus teams shaping their agent-assisted Java workflow. Skip it if you want a single deep topic: every answer is a few minutes long by design, and several questions get "we are working on it" instead of details.

## Verdict

**6/10**: Authors explain their own reasoning on Loom schedulers, string internals and JEP 465 across a dozen Q&A topics; the format caps depth and numbers, and the roadmap questions on modules, specialization and builders get no detail.

**Novelty 2/2**

- **+** [03:38](https://youtu.be/ewCPBgOrLAE?t=218) Bateman and Klang explain why custom virtual-thread schedulers stay unexposed: the runtime would call out to foreign scheduler code from locking, timer and socket paths, and N pools mean handover costs without the priority people want.
- **+** [44:45](https://youtu.be/ewCPBgOrLAE?t=2685) Cimadamore gives the post-mortem behind withdrawing JEP 465: nested templates were processed eagerly, which forced double processing and blocked the two-pass validation that string concatenation gets, so any replacement must keep nested templates open.
- **·** [38:29](https://youtu.be/ewCPBgOrLAE?t=2309) The modules, specialization-timeline and builders answers state goals and cost of prototyping but defer details until the work is ready to present.

**Demonstrated 1/2**

- **·** A panel Q&A with the speakers seated and no screen content has nothing to run, so there is no demo to judge.

**Measured 1/2**

- **+** [25:03](https://youtu.be/ewCPBgOrLAE?t=1503) An internal experiment generating the same programs with Java 25 idioms instead of Java 8 used about 20% fewer tokens.
- **·** [25:03](https://youtu.be/ewCPBgOrLAE?t=1503) The figure comes without method or workload detail, and nothing else quantitative is claimed.

**Depth 1/2**

- **+** [31:51](https://youtu.be/ewCPBgOrLAE?t=1911) The string answers weigh the requested view against immutability, native code scribbling on a string, and moving collectors, then state what JDK 27 did instead (copy straight from the string's bytes when the coder is compatible).
- **+** [14:07](https://youtu.be/ewCPBgOrLAE?t=847) The deprecation answers explain the removal calculus: Vector's blast radius across early JDK APIs, the cost of leaving it in place, Thread.stop respecified to throw instead of removed, and Maven-corpus static analysis.
- **·** [29:44](https://youtu.be/ewCPBgOrLAE?t=1784) Each answer runs a few minutes by format, so trade-offs get stated rather than worked through.

**Reusable 1/2**

- **+** [43:12](https://youtu.be/ewCPBgOrLAE?t=2592) Viewers leave with the HotSpot layout-print flags for inspecting value-class layout (the speaker is unsure of the current name).
- **+** [08:49](https://youtu.be/ewCPBgOrLAE?t=529) The loom-dev mailing list is the named place to report scheduler problems.
- **·** No repository, sample, configuration or checklist covering the session's content is pointed to.
