---
title: Faster Development with Java, Python, and Micronaut
talkId: "16444"
conference: devoxx-be-2026
speakers: [Graeme Rocher, Thomas Wuerthinger]
track: Java Language & Platform
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=zo6L7bxn4OY
durationMin: 48
slides: null
verdict: 8
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Faster Development with Java, Python, and Micronaut
Graeme Rocher, Thomas Wuerthinger · Conference · Java Language & Platform

## TL;DR
Micronaut creator Graeme Rocher and GraalVM lead Thomas Wuerthinger launch Pyronaut 0.1.0: a precompiled native base of JDK plus Micronaut plus GraalPy that runs Python (and Java) application code as scripts, with sub-second startup and build-time validation intact. Live demos move from single-file services through pytest and JUnit functional tests to IDE stubs for humans and agents, closing with throughput ahead of the fastest Python frameworks and the GIL named as the current ceiling.

## Key takeaways
- Only about 3% of loaded classes in a framework app are user code, so precompiling the other 97% once and scripting the rest dissolves the velocity-versus-performance dilemma instead of balancing it.
- Java annotations imported into Pyronaut Python become decorators, and the framework emits identical build-time metadata, which keeps OpenAPI, validation, and serialization behaving exactly as in Java Micronaut.
- Generated IDE stubs plus Pylance configuration expose the whole API to coding agents, giving agent-written Pyronaut code the same completion humans get.
- Peak Python throughput here is GIL-bound rather than I/O-bound: Java and I/O already parallelize while interpreted paths serialize, so GIL removal leads the performance roadmap.
- Shipping means packaging scripts onto a shared PGO-tuned base image instead of building a native image per app, and colocated instances share the base's memory pages.
- Existing Maven projects gain the fast loop unchanged: `pyronaut install` reads the pom classpath and dev mode then starts in about 80 ms.

## Notes
### [02:07](https://youtu.be/zo6L7bxn4OY?t=127) The server-side dilemma
Wuerthinger frames the talk as a choice developers face: scripting languages (Python, Ruby, JavaScript) restart instantly after an edit, while compiled stacks (Java, further still GraalVM Native Image) trade slower edit-to-run cycles for better peak performance and efficiency. Coding agents face the same trade-off, since they also want fast confirmation that tests still pass after a small edit. Build tools can stretch a JVM compile-test cycle into minutes, and a native image build costs minutes by itself.

### [04:09](https://youtu.be/zo6L7bxn4OY?t=249) Only 3% of your app is yours
The motivating measurement: running Micronaut PetClinic loads 12,433 classes, of which 3.1% are user code while 96.9% come from framework and JDK in roughly equal thirds (Micronaut, JDK packages, third-party libraries such as Reactor and Netty). CPU time skews even further toward framework code. Rocher notes this shape holds for any framework, with Spring and Quarkus looking similar. Dependencies barely change over a project's life while user code churns, so the proposal is to ahead-of-time compile the 97% once and keep the 3% dynamic and scriptable.

### [09:17](https://youtu.be/zo6L7bxn4OY?t=557) Precompile the base, script the rest
The building blocks are GraalPy (a Python 3 implementation on GraalVM: embeddable, interoperable with Java, JIT-compiled) running on a precompiled native base of JDK plus Micronaut plus GraalPy, extended with dynamically loaded classes via Crema. The combination shipped as Pyronaut 0.1.0 days before the talk, announced October 2, 2026. The pitch is that Python gains Java's structure, tooling, and native performance without losing its simplicity.

### [10:18](https://youtu.be/zo6L7bxn4OY?t=618) Demo: hello world in Python
Rocher's `main.py` declares a GET endpoint with a decorator imported from `micronaut.http.annotation`, except that import is actually a Java annotation converted into a Python decorator at processing time. Any JVM annotation works this way; at runtime the decorators are identity markers and the same framework internals serve the endpoint. `pyronaut dev main.py` starts the app in 290 ms with Swagger UI generated from Micronaut's build-time OpenAPI integration, and pytest runs full functional tests (server start, injected HTTP client, real request) with a rendered report.

```python
# from slide at 10:18
from micronaut.http.annotation import Get

@Get("/")
def index() -> dict[str, str]:
    return {"Hello": "World"}
```

### [15:00](https://youtu.be/zo6L7bxn4OY?t=900) Structured projects and PetClinic
Beyond single scripts, a `pyproject.toml` carries metadata, toolchain choice (native or JVM), and dependencies, while `pyronaut install` resolves everything and generates IDE stubs. Those stubs give completion, hover docs, and test visualization in VS Code. The full PetClinic port adds Flyway, Oracle Database with its JDBC driver, a Testcontainers-managed database on first run, Jinja2 templates, Micronaut Data JDBC entities with compile-time-checked repositories, and Micronaut Serialization DTOs. Java code can live in the same project for hot spots, with bidirectional Java-Python interop and both library ecosystems importable.

### [23:56](https://youtu.be/zo6L7bxn4OY?t=1436) Throughput against FastAPI
Maximum sustained request rate meeting every latency SLA on an OCI E4.Flex instance (3 OCPUs, 24 GB, HTTPS plus HTTP/2, Hyperfoil harness, best of two runs): Pyronaut at 35,351 requests per second against FastAPI with Granian at 13,576 (2.6x) and Flask with Gunicorn at 5,453 (6.5x), with 13x lower p99 latency than FastAPI (0.51 ms vs 6.62 ms at 11.7k req/s). The speakers state the caveat openly: Python paths still serialize on the GIL, so executor threads bottleneck there while Java and I/O run in parallel. GIL removal, virtual threads, and Shenandoah lead the roadmap. On turnaround, Pyronaut keeps script-like speed where JVM Micronaut is slower and native image demands full rebuilds.

### [26:33](https://youtu.be/zo6L7bxn4OY?t=1593) Java as a scripting language
Since javac was already in the base for the Python processing, `pyronaut dev app.java` compiles Java sources on the fly and serves them: 75 ms end to end including compilation, class loading, and server start, faster than plain javac compiles the file. `pyronaut test` runs the JUnit 5 plus Micronaut Test functional test in a blink. Kotlin and Groovy are named as future scripting languages on the same base. `pyronaut build app.java docker --native-base` packages the file into a small container on the precompiled Crema base image, so production starts in 78 ms with no native image build.

### [32:20](https://youtu.be/zo6L7bxn4OY?t=1940) Demo: Java, MySQL, and Maven projects
A larger Java example in IntelliJ declares extra dependencies inline (Micronaut Data JDBC, HikariCP, MySQL driver) with create-drop schema config, a Book entity, a repository, and a controller. `pyronaut dev` pulls the MySQL container image and serves count and create endpoints, while a second window runs persistence tests against the already-running database. `pyronaut install` generates IDE configuration so completion works with no build tool at all. For existing projects, running it on a plain Micronaut Maven project reads the pom's classpath, and dev mode then starts in 81 ms.

### [38:40](https://youtu.be/zo6L7bxn4OY?t=2320) Shared memory and a PGO-tuned base
The precompiled runtime is shared: one base Docker image serves many Pyronaut apps, and the operating system shares the mapped executable pages between colocated instances, so the 97% costs memory once. The base ships with profile-guided optimization applied by the Pyronaut team, which answers the classic criticism that ahead-of-time code lacks JIT profiling feedback. The claim is near-JIT peak throughput on hot paths such as the JSON parser.

### [41:44](https://youtu.be/zo6L7bxn4OY?t=2504) Try it: site, guides, samples
Installation is `pip install pyronaut`, after which `pyronaut setup` provisions GraalPy and the needed GraalVM version with its SDKs, so nothing else must be installed. The pyronaut.io site carries getting-started docs, a performance page with latency detail, and the full Micronaut guide catalog ported to Pyronaut. Samples include a DevOps AI scheduler using LangChain4j, Micronaut Cache, and tool calling, plus a port of the FastAPI full-stack template that drops the Docker Compose sprawl for Flyway, runs end-to-end tests from one script, and posts 6x profile-page and 3x create throughput while still GIL-limited, with server-side rendering on GraalJS so Python, JS, and Java share one VM.

## Tools, libraries and specs
- Pyronaut 0.1.0 (`pip install pyronaut`), pyronaut.io
- Micronaut (HTTP, Data JDBC, Serialization, Security, Cache, Test, Test Resources, OpenAPI)
- GraalVM Native Image, GraalPy (Python 3), GraalJS, Crema
- Netty HTTP server, pytest, JUnit 5
- Flyway, Oracle Database and JDBC driver, MySQL and JDBC driver, HikariCP
- Jinja2 templates, LangChain4j
- Testcontainers, Docker
- FastAPI, Gunicorn, Granian (benchmark baselines)
- Profile-guided optimization (PGO), Shenandoah GC, virtual threads, GIL
- Maven (Gradle mentioned), VS Code with Pylance, IntelliJ

## Who should watch
Python developers curious about a faster production framework gain the most, as do Micronaut and Java developers who want script-speed iteration (including on existing Maven projects) without leaving the ecosystem. Tooling watchers get a concrete pattern for generated stubs that teach coding agents an API. Viewers wanting framework internals should skip the middle: how Crema extends a native image is asserted rather than explained.

## Verdict
**8/10**: A days-old framework launched by its creators with live end-to-end demos, an installable release, and a throughput benchmark with its setup on the slide; the development-turnaround baselines are unmeasured "TO MEASURE" placeholders and the Crema mechanism is not explained.

**Novelty 2/2**

- **+** [09:48](https://youtu.be/zo6L7bxn4OY?t=588) Pyronaut 0.1.0 was announced days before the talk, so the launch and design rationale come straight from the Micronaut creator and the GraalVM lead.
- **+** [04:40](https://youtu.be/zo6L7bxn4OY?t=280) The 3.1%-user-classes measurement on Micronaut PetClinic is the speakers' own result motivating the architecture.
- **+** [23:56](https://youtu.be/zo6L7bxn4OY?t=1436) The head-to-head run against FastAPI with Granian and Flask with Gunicorn is the speakers' own comparison work.

**Demonstrated 2/2**

- **+** [12:20](https://youtu.be/zo6L7bxn4OY?t=740) `pyronaut dev` serves the Python hello endpoint live in 290 ms, with a working Swagger UI try-out on screen.
- **+** [13:23](https://youtu.be/zo6L7bxn4OY?t=803) A pytest functional test with server start, injected client, and a real HTTP request runs live with its rendered report visible.
- **+** [28:06](https://youtu.be/zo6L7bxn4OY?t=1686) A Java file compiles and serves live in 75 ms end to end, compile, load, and server start included.

**Measured 1/2**

- **+** [23:56](https://youtu.be/zo6L7bxn4OY?t=1436) The throughput chart shows Pyronaut at 35,351 req/s against 13,576 for FastAPI with Granian and 5,453 for Flask with Gunicorn, with its setup in the footer: OCI E4.Flex, 3 OCPUs, 24 GB, HTTPS plus HTTP/2, Hyperfoil, best of two runs, latency SLAs.
- **−** [03:38](https://youtu.be/zo6L7bxn4OY?t=218) The "cost of the wait" slide that frames the turnaround claim shows "N s" for the JVM and "N min" for native image, both tagged "TO MEASURE", so the 75 ms start has no measured JVM or native-image counterpart.
- **−** [45:53](https://youtu.be/zo6L7bxn4OY?t=2753) The "six times their throughput on the profile page" and "three times … on creating" claims against the FastAPI template come with no workload or method on screen.

**Depth 1/2**

- **+** [07:14](https://youtu.be/zo6L7bxn4OY?t=434) The precompile-the-base design is argued from the fact that dependencies stay fixed over a project's life while user code churns.
- **+** [24:58](https://youtu.be/zo6L7bxn4OY?t=1498) The GIL bottleneck is named precisely (serialized Python paths while Java and I/O run in parallel), with its removal plus virtual threads and Shenandoah as the roadmap.
- **−** [09:17](https://youtu.be/zo6L7bxn4OY?t=557) Crema, the mechanism that lets dynamic classes extend the closed native base, gets one sentence and is never explained.

**Reusable 2/2**

- **+** [41:44](https://youtu.be/zo6L7bxn4OY?t=2504) Release 0.1.0 installs from PyPI with one command and self-provisions GraalPy and GraalVM.
- **+** [45:23](https://youtu.be/zo6L7bxn4OY?t=2723) The talk points to the ported Micronaut guide catalog and the pyronaut fullstack template repository, which cover its arc.
