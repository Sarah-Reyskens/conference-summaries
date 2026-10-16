---
title: Bootiful Spring Boot 4
talkId: "19733"
conference: devoxx-be-2026
speakers: [Josh Long]
track: Architecture & Modernization
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=1PtdpItmzTo
durationMin: 49
slides: null
verdict: 6
reach: segment
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-15
---

# Bootiful Spring Boot 4
Josh Long · Conference · Architecture & Modernization

## TL;DR
Josh Long live-codes a Spring Boot 4.1 animals application from start.spring.io to production optimizations, touching lazy datasource connections, API versioning, declarative HTTP clients, resilient methods, SSRF filtering, OpenTelemetry, Spring gRPC, JobRunr, the new BeanRegistrar, and Project Leyden startup. The thesis: AI assistants can generate Spring code, but you still need to know what good looks like to validate the output. Most features are shown running on screen in one continuous demo.

## Key takeaways
- Set the lazy datasource connection property in Boot 4.1 so `@Transactional` methods acquire a connection only at first actual I/O, which matters once virtual threads let the web tier outrun a finite pool.
- Treat CVE upgrades as urgent: the Spring portfolio went from about 1.5 CVEs per month to a long advisories list, small issues chain with other layers, and fixes ship in releases before disclosure, so keep a fast path to production.
- Use `@Retryable`/concurrency limits from Spring's resilient methods and an `InetAddressFilter` bean to make outbound HTTP calls survive outages and block server-side request forgery.
- Split the old web starter mentally: the REST client now ships separately from the Spring MVC server, and simple clients collapse to an interface with `@GetExchange` plus `@ImportHttpServices`.
- Register beans dynamically with the new `BeanRegistrar` when `@Component` scanning and `@Bean` methods fall short, such as registering beans in a loop or with conditional logic.
- Prefer managed infrastructure over rebuilding it: Spring gRPC for schema-based services and JobRunr for durable recurring background jobs, both wired through Boot starters.

## Notes

### [00:33](https://youtu.be/1PtdpItmzTo?t=33) Intro, Prancer, and why "what good looks like" matters
After the traditional audience selfie (with GDPR-cookie consent joke), Long introduces himself as a Spring developer advocate and plugs a free in-progress Spring Security book plus a joint security session the next day. The demo domain is animals, motivated by Prancer, the "neurotic, man-hating" Chihuahua from a viral 2021 adoption ad. He surveys starting points (start.spring.io, IntelliJ wizard, VS Code Spring Tools, Spring Tools MCP for Claude Code) and argues AI agents make it more important to understand good output: use the tools, but learn to validate them.

### [08:19](https://youtu.be/1PtdpItmzTo?t=499) Project setup: Java 27 and the starter list
The app is generated with Java 27, credited with compact object headers worth roughly 10-20% less RAM, and he demos Java 25 single-file source launch ("run without compiling"). Starters pulled in: Postgres, Spring Data JDBC, devtools, web, HTTP client, OpenTelemetry, actuator, gRPC, and JobRunr. He notes Boot 4.1 shipped a few months ago and 4.2 lands in November on the roughly six-month cadence.

### [10:53](https://youtu.be/1PtdpItmzTo?t=653) Upgrade now: the CVE deluge
Scrolling spring.io/security advisories from August 20, he contrasts the old average of about 1.5 CVEs per month across the portfolio with the current volume. Small CVEs chain with weaknesses in other layers into serious exposure, and fixes land in releases before disclosure, so teams should upgrade immediately rather than waiting for announcements.

### [13:30](https://youtu.be/1PtdpItmzTo?t=810) Virtual threads and lazy connection acquisition
Virtual threads (much improved since Java 24) let the web tier handle far more concurrent requests, which can saturate a fixed-size JDBC pool, especially when `@Transactional` holds a connection for a whole method including non-DB work. The 4.1 answer is a lazy acquisition property that defers fetching the connection until the first SQL I/O inside the transaction.

### [16:05](https://youtu.be/1PtdpItmzTo?t=965) Dogs API with versioning
A `Dog` record, a `ListCrudRepository` with its configured dialect, and a controller returning a shaped map go live at `/dogs`. When requirements change, he keeps both shapes and versions them: v1.0 and v2.0 on the mappings, v2 as default, selected via an `X-Dogs-Version` header, verified with live requests.

### [19:12](https://youtu.be/1PtdpItmzTo?t=1152) Cats client: split starters and interface clients
The REST client starter is now separate from the MVC server starter, so CLI, batch, or integration apps can call HTTP APIs without a server. After building a `RestClient`-based client for the catfacts API, he replaces it with a declarative interface carrying `@GetExchange` on the method, activated by `@ImportHttpServices`, and confirms the same `/cats` output (after fixing a wrong return type live).

### [23:21](https://youtu.be/1PtdpItmzTo?t=1401) Resilient methods and SSRF filtering
Citing the AWS US-East and Cloudflare outages landing weeks apart, he adds `@EnableResilientMethods` and a retrying method that fails five times before succeeding, plus a mention of concurrency limits as a semaphore. Then an `InetAddressFilter` bean (`none()` in the demo) blocks the catfacts call with a "filtered host" error; the filter works across RestClient, RestTemplate, and the reactive clients on every supported engine (JDK, Apache).

### [27:32](https://youtu.be/1PtdpItmzTo?t=1652) Observability out of the box
Adding the OpenTelemetry starter with a collector on the default port streams metrics with no custom code. In Grafana (with HikariCP connection and acquire-time charts visible) he shows pool metrics already flowing from the running demo.

### [29:34](https://youtu.be/1PtdpItmzTo?t=1774) Spring gRPC service
Spring gRPC is now managed by Boot 4. He writes `dogs.proto` (messages with explicit field positions, a `DogService` with a list RPC), runs the Maven build to generate stubs (IntelliJ users must mark `generated-sources` as a source root), implements the service over the repository, and calls it with grpcurl against `localhost:9090`, returning the dog list including Prancer.

### [35:51](https://youtu.be/1PtdpItmzTo?t=2151) JobRunr and the BeanRegistrar
JobRunr, a Belgian distributed job engine, covers the "processor" sidecar most architectures need (image resizing, email) with DB-backed durability. A `Launcher` (`ApplicationRunner`) schedules a recurring "hello Devoxx" job every 10 seconds through `JobRequestScheduler`, handled by a `JobRequestHandler`, with the `jobrunr_*` tables visible in Postgres. This motivates the Framework 7 `BeanRegistrar`: unlike a `@Bean` method it can register beans in loops and conditionals, with either implicit constructor resolution or an explicit supplier. He also shows the carbon-aware interval option that shifts runs by seconds based on local grid data.

### [47:16](https://youtu.be/1PtdpItmzTo?t=2836) Leyden startup and close
A `leiden.sh` script packages the app, extracts the AOT layout, profiles it, and produces the optimized artifact on a stock JDK. Startup drops from about 1.7 s to 0.471 s, on top of the compact-headers RAM savings. He closes by re-inviting the room to the next day's Spring Security session and takes questions.

## Tools, libraries and specs
- Spring Boot 4.1 / 4.2, Spring Framework 7, Spring Data JDBC, Spring MVC
- Java 25 (single-file source launch), Java 27 (compact object headers), Project Leyden, virtual threads
- Spring gRPC (Boot-managed), protobuf + grpcurl
- JobRunr (recurring jobs, carbon-aware intervals), Postgres, HikariCP
- Spring Tools MCP for Claude Code, start.spring.io, Grafana/Prometheus, OpenTelemetry

## Who should watch
Spring developers deciding when to move to Boot 4 gain a fast, demo-driven map of what is new and worth adopting. Beginners get approachable live examples of each feature with the reasoning attached. Teams already deep on Boot 4 or wanting internals-level treatment of any single feature (AOT, gRPC tuning, JobRunr operations) should look for dedicated sessions instead.

## Verdict
**6/10**: A live tour of Boot 4.1/4.2 features where nearly every feature runs on screen, limited by tour breadth, one recalled startup baseline and demo code not yet published.

**Reach segment**: Spring Boot developers can put the lazy datasource connections, API versioning, interface HTTP clients, resilient methods, SSRF filter, and Leyden packaging steps to use in their own services within the next year.

**Novelty 1/2**

- **+** [11:57](https://youtu.be/1PtdpItmzTo?t=717) The upgrade advice comes from inside the team: CVE fixes ship in a release before disclosure, so teams need a fast path to production.
- **+** [48:47](https://youtu.be/1PtdpItmzTo?t=2927) The talk joins Boot 4.1 features, the security advisory volume, and the Java 27 and Leyden material in one pass, which he calls "a smorgasbord of interesting features".
- **−** Each feature on its own is what the Spring Boot 4.1 reference docs and release notes already describe, so the value is the assembled tour rather than new material.

**Demonstrated 2/2**

- **+** [18:40](https://youtu.be/1PtdpItmzTo?t=1120) The versioned dogs endpoint returns the new shape by default and the old shape with the version header, live.
- **+** [35:21](https://youtu.be/1PtdpItmzTo?t=2121) The grpcurl call against the freshly built gRPC service returns the dog list on screen.
- **+** [45:11](https://youtu.be/1PtdpItmzTo?t=2711) The recurring JobRunr job prints its message on schedule from the beans the registrar registered.

**Measured 1/2**

- **+** [48:17](https://youtu.be/1PtdpItmzTo?t=2897) The Leyden-optimized run reports a startup of 0.471 s on screen against a stated 1.7 s without it.
- **−** [48:17](https://youtu.be/1PtdpItmzTo?t=2897) The 1.7 s baseline is recalled rather than run, with no repetition or hardware given.
- **−** [08:19](https://youtu.be/1PtdpItmzTo?t=499) The 10-20% less RAM from compact object headers is stated "depending on how you're measuring", with no measurement shown.

**Depth 1/2**

- **+** [14:32](https://youtu.be/1PtdpItmzTo?t=872) The lazy-connection explanation traces pool saturation to virtual-thread concurrency plus `@Transactional` holding connections through non-DB work.
- **+** [38:26](https://youtu.be/1PtdpItmzTo?t=2306) The bean-registration segment explains `@Component` as a stereotype meta-annotation, contrasts implicit with explicit registration, and gives the cases where `@Bean` or the registrar fits.
- **−** [34:49](https://youtu.be/1PtdpItmzTo?t=2089) gRPC is offered with "blazing fast" as its only reason to choose it, and the generated wiring behind the service class is not explained.

**Reusable 1/2**

- **+** [32:45](https://youtu.be/1PtdpItmzTo?t=1965) The `dogs.proto` schema is typed out on screen, with the generated-sources source-root step for IntelliJ.
- **+** [47:16](https://youtu.be/1PtdpItmzTo?t=2836) The Leyden script's steps (package, extract the AOT layout, profile, run) are narrated so the flow can be reconstructed.
- **−** [02:35](https://youtu.be/1PtdpItmzTo?t=155) The demo code is promised ("the code will be online as well") but is not published yet, so no artifact covers the talk's main content.
