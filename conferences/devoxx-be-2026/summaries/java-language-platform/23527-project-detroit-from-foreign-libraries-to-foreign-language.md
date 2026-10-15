---
title: "Project Detroit: From Foreign Libraries to Foreign Language Runtimes"
talkId: "23527"
conference: devoxx-be-2026
speakers: [Maurizio Cimadamore]
track: Java Language & Platform
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=JWFZY0aJTjg
durationMin: 50
slides: null
verdict: 9
frames: 11
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Project Detroit: From Foreign Libraries to Foreign Language Runtimes

Maurizio Cimadamore · Conference · Java Language & Platform

## TL;DR

Project Detroit embeds industry-standard language runtimes (V8, CPython) into Java applications through the Foreign Function & Memory API instead of reimplementing them on the JVM, an approach motivated by the maintenance cost that killed Nashorn. The talk pairs a live end-to-end demo with the hard interop problems (cross-runtime object lifetimes, virtual-thread pinning, JNI-to-FFM migration) and head-to-head numbers for each.

## Key takeaways

- Rewriting a foreign language runtime on the JVM demands permanent industrial-scale commitment to track yearly standard updates and ecosystem compatibility; embedding V8 or CPython via FFM sidesteps both.
- Detroit engines are exposed through the familiar `javax.script` API, so existing Nashorn-era code mostly runs unchanged, with a restricted mode that only exposes Java APIs the developer explicitly allows.
- Objects that cross the Java/foreign boundary can form collection cycles neither GC can see; Detroit Python answers with explicit ref-count release plus FFM-inspired arenas.
- Calling a blocking Java callback from a script on a virtual thread pins the carrier because V8 sits on the stack as a native frame; wrapping the callback in a promise and using `async`/`await` on the JS side avoids the pin.
- Moving DetroitJS glue from JNI to FFM (via a flat C API over V8's C++ RAII idioms) cut native code 4x (7.2K to 1.8K lines) and total maintained code 2.5x (13.6K to 5.4K), while also speeding up native-to-Java upcalls.
- Most real-world polyglot use cases the team saw inside Oracle are shallow (call into Python for one library, get a value back), where per-transition overhead matters little.

## Notes

### [00:34](https://youtu.be/JWFZY0aJTjg?t=34) Java reaching outside the JVM

Java already reaches data outside the JVM (JDBC, sockets, files) and, with FFM, native code; Project Babylon may extend that reach to foreign programming models such as GPU kernels. The `javax.script` API covers foreign language runtimes, and it still matters: Rhino shipped in Java 6, Nashorn in 8 through 14, and enterprise software (Ant's JavaScript build action is one example) grew to depend on scriptability. A second driver is AI workloads: Java can run them efficiently, but the ecosystem lives in Python libraries like PyTorch that will not be rewritten overnight.

### [05:16](https://youtu.be/JWFZY0aJTjg?t=316) The Nashorn story

Nashorn, led by Jim Laskey and presented at JVMLS 2011, rewrote Rhino on Java 7's `invokedynamic` machinery and shipped in Java 8 as a complete, fast ECMAScript 5.1 implementation with rich Java interop (`Java.type`, package imports). Two forces killed it: ES2015 and then yearly standard updates made catching up a treadmill for a small team, and Node.js meant bug-for-bug V8 compatibility was needed for the npm ecosystem (6,000 to 50,000 packages in two years). Nashorn was deprecated in JDK 11 and removed in JDK 15 (JEP 372); it survives as a standalone OpenJDK project. Lesson: shipping a foreign runtime on the JVM is possible, but maintaining one is an industrial-scale commitment.

### [11:32](https://youtu.be/JWFZY0aJTjg?t=692) Detroit: wrap, don't rewrite

FFM lowers the cost of reaching native libraries instead of porting them, and a jextract example that drives CPython in about six lines of Java suggested the same pragmatism for runtimes. Detroit wraps V8 and CPython with small interop bridges, staying out of the standards-compatibility loop. The idea dates to a 2017 JVMLS talk by Jim Laskey ("native script engine", JNI-based), stalled, and restarted this year on FFM; it was announced at JavaOne. Two experimental engines exist: DetroitJS (currently JNI, FFM migration in progress, two flavors: full bidirectional Nashorn-style interop and a restricted developer-controlled one) and Detroit Python (jextract plus FFM, no native code). Both surface through `javax.script`.

### [17:19](https://youtu.be/JWFZY0aJTjg?t=1039) Demo: Detroit Python end to end

A terminal demo ran `jpython.sh`, a Python REPL written on Detroit: it refused to start under the system Python 3.10, worked after activating a prepared Python 3.14 virtual environment, and evaluated prints and arithmetic. The main demo ran a Gradio image-classification app (Gradio plus Transformers plus PyTorch, all stock pip packages, with weights pre-downloaded because of flaky conference Wi-Fi) through the standard `ScriptEngineManager` ceremony. The server came up, classified a school bus correctly, and produced onomatopoeic nonsense ("gong", "tam tam") for the title slide, distracted by a mechanical arm. Nothing but standard Python tooling was needed on the machine.

### [25:09](https://youtu.be/JWFZY0aJTjg?t=1509) Performance: pure JS is fast, callbacks are not

Octane 2.0 (one transition into JS, then pure execution) showed DetroitJS at 59,366, far ahead of GraalJS (11,815) and Nashorn (3,303); the speaker flagged the GraalJS figure as likely low because Octane's default warmup suits it poorly (raising warmup caused out-of-memory errors, and ~40K may be attainable). The worst case is a JS array sorted with a Java comparator, forcing a native-to-Java transition per comparison: Detroit scored far below every alternative, while a JS comparator on V8 is very fast, leaving headroom for FFM upcall improvements.

### [28:13](https://youtu.be/JWFZY0aJTjg?t=1693) Lifetimes across two runtimes

Java objects (GC-managed) and foreign objects (V8 GC or CPython refcounting) cross the boundary in both directions, and neither collector sees the whole graph. A worked Java/Python example builds a full cycle: a Python object returned to Java, embedded in a Java callback passed back to Python, then linked onto a field of the Python object itself, which nobody can collect. Detroit Python therefore exposes explicit ref-count decrement plus FFM-inspired arenas (close the arena, all its objects go away); the cycle is broken by explicitly releasing the Python object so each side can collect its part. The 20-year-old `javax.script` API assumes JVM-hosted engines and offers no close method, so Detroit improvises here.

### [31:48](https://youtu.be/JWFZY0aJTjg?t=1908) Virtual-thread pinning and the async fix

A request handler on a virtual thread calls JS, which calls back into a blocking Java lookup (socket read) and parks: V8's `execute` is a native frame on the stack, so the virtual thread pins to its carrier and the server loses the benefit of virtual threads. The fix reuses V8's own async machinery rather than reinventing it: wrap the blocking lookup in an emulated V8 promise on the Java side, mark the JS function `async` and `await` the lookup, so V8 unwinds the Java stack and reschedules the continuation when the promise resolves. No pinning, at the cost of small code changes on both sides.

### [35:27](https://youtu.be/JWFZY0aJTjg?t=2127) Leaving JNI for FFM

Detroit Python is 6K lines of maintained code (95% of the Java generated by jextract against the 3.14 and 3.17 headers, zero handwritten native code), assembled in two to three months; DetroitJS is 14K lines, half of it C++/JNI glue. Direct FFM bindings cannot work for V8 because every JS call needs a C++ RAII dance (Locker, Isolate::Scope, HandleScope, TryCatch) requiring a C++ compiler. The prototype instead exposes a small flat C API (call function, access field, create object) and generates FFM bindings for that: native code fell 4x (7.2K to 1.8K lines) and maintained code 2.5x (13.6K to 5.4K), matching Detroit Python. The qsort comparator benchmark improved for two reasons: FFM upcalls beat JNI upcalls, and marshalling dispatch moved from a C switch to a Java switch where C2 can speculate on the fast path (e.g. int). It still trails GraalJS and Nashorn, which the speaker accepts given V8's pure-JS speed; internal use cases never hit performance problems.

### [40:35](https://youtu.be/JWFZY0aJTjg?t=2435) Wrap-up and call for help

Embedding standard runtimes buys automatic compatibility and competitive performance with small, maintainable bridges, at the price of two runtimes in memory, back-and-forth transition costs, explicit lifetime management in places, and async execution to avoid pinning. These surface in a niche of use cases; casual interop mostly just works through `javax.script`. Detroit is experimental: the speaker asked the audience to try the JavaScript and Python engines (github.com/openjdk/detroit-js, github.com/openjdk/detroit-python) and report gaps to detroit-dev@openjdk.org, crediting Arvind Aprameya, Sundararajan Athijegannathan, Mikael Vidstedt and Jorn Vernee.

### [44:26](https://youtu.be/JWFZY0aJTjg?t=2666) Q&A

DetroitJS uses plain V8, so npm packages work through the normal npm environment with no Detroit wrapper. Most internal Oracle polyglot cases are shallow single calls into Python for an otherwise-unavailable library, needing little back-and-forth. On FFM allocation overhead, JDK 28 pools memory across confined arenas (close recycles into the creating thread; cited numbers reach ~20x for allocate-call-free patterns), and a slicing allocator over a fixed segment already allows bump allocation without malloc per call.

## Tools, libraries and specs

- Project Detroit (experimental): github.com/openjdk/detroit-js, github.com/openjdk/detroit-python, mailing list detroit-dev@openjdk.org
- Foreign Function & Memory API (FFM) and jextract (bindings generated against Python 3.14 and 3.17 headers)
- V8, CPython 3.14, Node.js, npm
- Nashorn (Java 8–14, removed by JEP 372; standalone OpenJDK project), Rhino, GraalJS
- `javax.script` API, `invokedynamic` / `java.lang.invoke` (Project Vinci Machine)
- Octane 2.0 benchmark
- Gradio, Transformers, PyTorch (stock pip packages in the demo)
- Project Babylon (GPU kernels), Vector API

## Who should watch

Java developers who embed scripting (business rules, DSLs, build tooling) or need Python libraries from Java gain the most, especially anyone carrying Nashorn-era `javax.script` code. Viewers wanting stable, production-ready APIs should wait; this is an experimental-project status report, not a how-to for shipping systems.

## Verdict

**9/10**: Authors' design rationale, a live Detroit Python demo and head-to-head Octane and comparator charts, limited by an unquantified FFM speed-up and the experimental status.

**Novelty 2/2**

- **+** [09:59](https://youtu.be/JWFZY0aJTjg?t=599) The Nashorn post-mortem gives the removal rationale from inside the team: yearly ES updates plus bug-for-bug V8 compatibility needed for the Node.js ecosystem.
- **+** [37:30](https://youtu.be/JWFZY0aJTjg?t=2250) The FFM-meets-V8 prototype design (flat C API over RAII idioms, jextract bindings, C2-speculated marshalling) is original engineering from the authors.
- **+** [25:40](https://youtu.be/JWFZY0aJTjg?t=1540) The Octane and comparator head-to-heads across DetroitJS, Nashorn and GraalJS are comparisons the speaker ran himself.

**Demonstrated 2/2**

- **+** [17:19](https://youtu.be/JWFZY0aJTjg?t=1039) The Detroit Python REPL runs live in a terminal, including the Python 3.10 refusal and recovery via a 3.14 virtual environment.
- **+** [20:27](https://youtu.be/JWFZY0aJTjg?t=1227) The Gradio image classifier launches end to end through `javax.script` and classifies a school bus live, with a visible misfire on the title slide.
- **·** [15:12](https://youtu.be/JWFZY0aJTjg?t=912) DetroitJS, the engine behind the Nashorn story and both charts, runs on JNI and is only benchmarked, never run on screen.

**Measured 1/2**

- **+** [25:40](https://youtu.be/JWFZY0aJTjg?t=1540) Octane 2.0 bars put DetroitJS at 59,366 against GraalJS at 11,815 and Nashorn at 3,303.
- **+** [27:12](https://youtu.be/JWFZY0aJTjg?t=1632) The Java-comparator sort benchmark ranks Detroit last by a wide margin, the talk's own worst case shown with its rivals.
- **−** [38:01](https://youtu.be/JWFZY0aJTjg?t=2281) The FFM rewrite is said to make upcalls "a lot faster" and give "a lot better numbers", but no chart or figure follows, and "we never saw performance problem" at [40:04](https://youtu.be/JWFZY0aJTjg?t=2404) is an anecdote.

**Depth 2/2**

- **+** [28:13](https://youtu.be/JWFZY0aJTjg?t=1693) The cross-runtime cycle is built step by step and resolved with explicit ref-count release plus arenas, naming the `javax.script` close-method gap.
- **+** [31:48](https://youtu.be/JWFZY0aJTjg?t=1908) The virtual-thread pin is traced frame by frame down the stack and fixed with promises plus `async`/`await`.
- **+** [36:58](https://youtu.be/JWFZY0aJTjg?t=2218) The V8 RAII dance explains why 1:1 FFM bindings cannot work and why the flat-C-API split wins on both size and speed.

**Reusable 2/2**

- **+** [43:12](https://youtu.be/JWFZY0aJTjg?t=2592) The closing slide points to the detroit-js and detroit-python repositories covering both engines in the talk.
- **·** [43:12](https://youtu.be/JWFZY0aJTjg?t=2592) The project is experimental and its APIs will move with real-workload feedback, so adopters track a moving target.
