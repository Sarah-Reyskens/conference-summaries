---
title: "Taming Microservice Overload: Our Journey to Modular Monoliths"
talkId: "8153"
conference: devoxx-be-2026
speakers: [Mario Klaver]
track: Architecture & Modernization
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=v86SfHA5ISw
durationMin: 50
slides: null
verdict: 6
reach: broad
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Taming Microservice Overload: Our Journey to Modular Monoliths

Mario Klaver · Conference · Architecture & Modernization

## TL;DR

The Port of Rotterdam grew from one monolith to more than 90 microservices run by 5 teams, and discovered the real problem was never the service count but wrong business boundaries. Klaver walks through how big-picture event storming rediscovered the subdomains, how one deployable per subdomain with Spring Modulith modules inside keeps those boundaries executable, and how the team migrates capability by capability while the 24/7 system keeps running.

## Key takeaways

- Count boundaries, not services: tightly coupled services that always change together are a distributed monolith, whatever the deployment diagram says.
- Run big-picture event storming with every perspective in the room, then cluster domain events around pivotal events to find candidate subdomains.
- Start with one deployable per subdomain and modules per business capability inside it, so uncertain boundaries stay cheap to redraw.
- Enforce module boundaries in code with Spring Modulith: explicit API packages, declared allowed dependencies, cycle and access verification at build time.
- Communicate between modules through the same business-domain events found during event storming, published over the broker, so a later extraction never turns a direct call into a REST call.
- Migrate business capabilities one at a time, not service by service, and let old and new services coexist through events during the years-long transition.
- Extract a module into its own service only for scaling, ownership, deployment-frequency, or technology reasons: modular first, distributed when needed.

## Notes

### [02:05](https://youtu.be/v86SfHA5ISw?t=125) From one backend to 90 microservices

The system started in 2010 as one Java backend plus a Java Swing client (HTML had no offline support then). By 2015 the backend showed classic monolith strain: unexpected side effects, release bottlenecks with all teams in one codebase, and whole-application scaling when only one queue piled up. The team began extracting microservices, enthusiasm tipped into excess (a rule allowed rebuilding any service from scratch within 4 weeks, and old service versions were never removed), and by end of 2024 five teams owned more than 90 services plus micro frontends. Their microservice-to-engineer ratio sat above 4.5, far past the 0.5 sweet spot and the 1.0 proliferation line shown on the slide.

### [07:52](https://youtu.be/v86SfHA5ISw?t=472) What the services cost

Microservices genuinely solved the original problems: independent deployments, independent scaling, team ownership, smaller codebases. The price was slower cross-service feature delivery, repetitive dependency updates across dozens of services (despite Renovate and OpenRewrite), technical debt multiplied per service, harder debugging across logs and network calls, and infrastructure cost multiplied by 4 on-street environments times 2 ports. The application serves the ports of Rotterdam and Amsterdam.

### [09:24](https://youtu.be/v86SfHA5ISw?t=564) Uber and Spotify hit the same wall

Uber reported simple features spanning services and single-issue investigations touching up to 50 services owned by 12 teams; Spotify needed about 8 months and 2,000 pull requests for a Java runtime migration. Uber's published conclusions were better business-domain boundaries, platform engineering, and strong standards. Rotterdam's one-person platform team answered with Spring-style starters (document management, security, inbox/outbox) using convention over configuration.

### [12:30](https://youtu.be/v86SfHA5ISw?t=750) The real problem is boundaries

One business-process diagram showed services calling each other back and forth, including two services Klaver called married. Three ship-clearance services looked well separated on paper (port entry permission, safe berth reachability, berth planning) but constantly called each other, changed together, and even contradicted their documented responsibilities in code. The conclusion: the team had split code into services without splitting business responsibility, so the biggest concern became boundary quality, defined as local change, minimal cross-boundary dependencies, describable responsibility, and high internal consistency.

### [19:13](https://youtu.be/v86SfHA5ISw?t=1153) Event storming to find subdomains

The team ran big-picture event storming: chaotic domain-event capture on stickies, enforcing the timeline with pivotal events, swim lanes and temporal milestones, adding actors, an explicit end-to-end walkthrough, then clustering events into boundary candidates afterward. Their wall yielded subdomains including Declarations, Visit Management, Port Clearances, Nautical Planning, Vessel Traffic, Safety, and Environmental, grouped around pivotal events. Port Clearance covers health, dangerous goods, waste, and security assessments feeding one operational clearance decision.

### [26:59](https://youtu.be/v86SfHA5ISw?t=1619) One deployable per subdomain, modules inside

The architectural decision (explicitly reversible) maps each subdomain to one deployable service with business capabilities as modules inside, because the boundaries may still be wrong and moving code within one service is cheaper than across services. Consolidating capabilities such as health assessment, dangerous goods assessment, and operational clearance into the Port Clearance service without internal structure would just build a smaller monolith, so internal module boundaries carry the event-storming results into the code.

### [30:09](https://youtu.be/v86SfHA5ISw?t=1809) Enforcing modules with Spring Modulith

Each Spring Modulith module owns its logic and exposes only an explicit API package; the frame shows `com.portofrotterdam.port_clearances` with `dangerous_goods`, `health` (api, application, domain, infrastructure), and `operational_clearance` modules, and IntelliJ marking exposed versus locked packages. Spring Modulith verifies the structure (module cycles, internal-access violations) against declared allowed dependencies, making the architecture executable so boundaries survive codebase growth. `@ApplicationModuleTest` with standalone mode starts only one module's Spring context for isolated tests.

### [34:17](https://youtu.be/v86SfHA5ISw?t=2057) Module communication via domain events

Direct bean calls between modules create dependencies that would have to become REST calls on extraction, so modules publish business events such as health declaration assessment completed over Kafka or ActiveMQ, with any module or external service free to listen. The events double as the vocabulary discovered during event storming: each one represents something that actually happened in the business.

### [37:53](https://youtu.be/v86SfHA5ISw?t=2273) Migrating capability by capability

New functionality lands directly in the target architecture: the ISPS assessment module (an ISPS-regulated vessel may only use an ISPS-certified berth) listens for the legacy visit-management movement-updated event and feeds the operational clearance module. Moved capabilities keep working through four patterns of increasing difficulty: relocated code initially keeping its broker communication inside the new service, old services listening to new-service events, splitting one process out of a multi-process service with the old service subscribing back, and finally extracting one capability (nautical planning's capability 3) scattered across services A, B, and C. Full migration is estimated at 4 to 5 years.

### [46:08](https://youtu.be/v86SfHA5ISw?t=2768) Hypotheses to measure, and Q&A

No impact measurements exist yet, so the team framed two hypotheses: clear boundaries cut cross-team coordination and therefore lead time for change, and consolidation cuts services operated and therefore maintenance effort. The closing line: microservices distribute complexity, but good boundaries control it. In Q&A, Klaver said the journey started early 2022, things look better after almost two years, but the landscape is still messy with 2 to 3 years to go, and the improvement still needs measuring.

## Tools, libraries and specs

- Spring Modulith (modules, named/API packages, dependency verification, `@ApplicationModuleTest`)
- Spring Boot starters (in-house: document management, security, inbox/outbox)
- Apache Kafka, ActiveMQ Artemis (module and service events)
- Renovate, OpenRewrite (cross-service dependency updates)
- Event storming (Alberto Brandolini), Domain-Driven Design subdomains and bounded contexts
- IntelliJ IDEA Spring Modulith support (module lock icons)

## Who should watch

Teams drowning in microservices who suspect their boundaries are wrong, and architects evaluating Spring Modulith as the enforcement layer for a consolidation. Viewers wanting Modulith configuration code, verification-test examples, or measured before/after results should look elsewhere: this talk shows concepts and diagrams, and its delivery and maintenance claims are still unmeasured hypotheses.

## Verdict

**6/10**: A 90-service consolidation with reasoned design decisions and migration patterns from a production system, limited by Spring Modulith verification that is only described and by improvement claims that are still unmeasured.

**Reach broad**: Java backend developers, tech leads and architects can apply the boundary diagnosis, event-storming practice and modular-first rules to their own service landscapes.

**Novelty 2/2**

- **+** [13:02](https://youtu.be/v86SfHA5ISw?t=782) Three ship-clearance services with separate documented responsibilities turn out to call each other, change together and decide in code what the documentation assigns elsewhere, a diagnosis taken from the team's own landscape.
- **+** [38:55](https://youtu.be/v86SfHA5ISw?t=2335) The team decides to migrate business responsibilities one capability at a time instead of service by service, because the 24/7 system cannot stop, a decision taken on its own 90-service landscape.
- **−** The Spring Modulith segment (API packages, dependency verification, `@ApplicationModuleTest`) follows the Spring Modulith reference documentation.

**Demonstrated 0/2**

- **−** [33:16](https://youtu.be/v86SfHA5ISw?t=1996) Module dependency verification is only described; no build runs showing a violation caught or a clean verification on screen.
- **−** [36:20](https://youtu.be/v86SfHA5ISw?t=2180) Isolated module testing with `@ApplicationModuleTest` is only described; no test executes and no output is visible.
- **−** [31:12](https://youtu.be/v86SfHA5ISw?t=1872) The only Modulith visual is an IntelliJ package tree with exposed and locked icons, a static picture of the module layout and not a run.

**Measured 1/2**

- **+** [04:47](https://youtu.be/v86SfHA5ISw?t=287) Self-reported scale totals ground the story: 5 teams and 90+ services at roughly 20 each, with infrastructure multiplied by 4 environments and 2 ports at [08:53](https://youtu.be/v86SfHA5ISw?t=533).
- **−** [46:40](https://youtu.be/v86SfHA5ISw?t=2800) The faster-delivery and lower-maintenance claims are stated as unmeasured hypotheses with no baseline, method or timeline.
- **−** [49:18](https://youtu.be/v86SfHA5ISw?t=2958) After almost two years the answer to whether the problems went away is "we think it helped, but we have to measure it".

**Depth 2/2**

- **+** [28:00](https://youtu.be/v86SfHA5ISw?t=1680) One deployable per subdomain is argued as reversible: uncertain boundaries stay cheap to move inside one service until scaling, ownership or deployment pressure justifies extraction.
- **+** [34:17](https://youtu.be/v86SfHA5ISw?t=2057) Event-based module communication is weighed against direct bean calls on coupling grounds and because a direct call would become a REST call on extraction, reusing the event-stormed business vocabulary.
- **+** [36:51](https://youtu.be/v86SfHA5ISw?t=2211) Four triggers for turning a module into a service (independent scaling, a different owner, deployment frequency, a different runtime or technology) give the rule for modular first, distributed when needed.

**Reusable 1/2**

- **+** [39:26](https://youtu.be/v86SfHA5ISw?t=2366) The ISPS walkthrough (new module listens to the legacy movement-updated event and feeds operational clearance) describes the event wiring in enough detail to replay on another landscape.
- **+** [41:31](https://youtu.be/v86SfHA5ISw?t=2491) The three later migration scenarios (relocated packages keeping AMQ, old service subscribing to new events, extraction of one capability from services A, B and C) are each described with their event direction.
- **·** [48:12](https://youtu.be/v86SfHA5ISw?t=2892) The talk ends with two book recommendations and points to no repository, sample project or checklist, so the module layout and patterns are reconstructed from diagrams and narration.
