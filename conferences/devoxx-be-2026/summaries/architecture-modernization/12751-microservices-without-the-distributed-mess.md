---
title: Microservices Without the Distributed Mess
talkId: "12751"
conference: devoxx-be-2026
speakers: [Steven Hillaert]
track: Architecture & Modernization
sessionType: Conference
audienceLevel: ADVANCED
video: https://www.youtube.com/watch?v=eFSEg54mwVU
durationMin: 46
slides: null
verdict: 6
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15

# Microservices Without the Distributed Mess
Steven Hillaert · Conference · Architecture & Modernization

## TL;DR
Microservices fail when treated as a technical problem of APIs and brokers; the hard part is designing for autonomy, ownership, and coherent boundaries. Hillaert works through four failure areas (ownership, boundaries, relationships, implementation-first thinking) using Domain-Driven Design as a thinking tool and leasing-industry examples. You leave with concrete questions to ask before creating or splitting a service.

## Key takeaways
- Autonomy and ownership are inputs to microservice design, not outputs: splitting a system into deployable pieces does not create them.
- Give each service exactly one accountable team with decision rights, and require the team to own the failures too; shared ownership means nobody fixes the mess.
- Keep the decisions a service makes and the data it needs to make them inside the same boundary, or independence is fiction.
- A bounded context is not a microservice: risk, performance, legal, and team-size boundaries can legitimately split one bounded context into two services or merge two into one.
- Ask who influences whom before choosing sync, async, or replication: the caller is not always the dependent party, and async messaging keeps the contract dependency.
- A service is as big as it needs to be to stay coherent; a stable interface can even be a read-only database rather than an API nobody has time to build.

## Notes

### [00:32](https://youtu.be/eFSEg54mwVU?t=32) Microservices promise what you must design for
Hillaert opens with the familiar descent: one service calls another, more get added, coupling grows, and a message broker gets slapped on top as if that restores loose coupling. Autonomy and ownership look like promises of microservices, but the causality runs the other way: you must design for them, and cutting a system into pieces never grants them automatically. His definition: a microservice is a cohesive set of capabilities in a clear business context that can be independently deployed and evolved. Technically it is only a deployment boundary, not a solution by itself. He names four failure areas for the rest of the talk: ownership, boundaries, relationships, and implementation-first thinking.

### [06:25](https://youtu.be/eFSEg54mwVU?t=385) Ownership works both ways
Poor ownership creates a paradox: when nobody owns a service, every team bends it to its own needs, and when it breaks, none of the five teams that touched it takes responsibility. The fix is one accountable team per service, responsible for code, design, model coherence, evolution, and operations ("you build it, you run it"), with real decision rights over technology and refused changes. Ownership is given and taken: the team gets the rights and owns the failures. The service itself must also own things: its capabilities, the rules it applies, and the data those rules need. A service that fetches its decision data from elsewhere on every call cannot act independently.

### [10:09](https://youtu.be/eFSEg54mwVU?t=609) Boundaries: DDD helps, but is not the whole answer
Bad cohesion in either direction hurts: related things split apart force coordinated deployments, while unrelated things sharing a service (contracts next to accounting) couple each other's runtime fate. DDD gives the vocabulary: domain (problem space), bounded context (solution space where language and model stay consistent), then implementation as a service. You don't need full DDD adoption; the useful questions are which functionalities change together and where language subtly differs. His leasing example: a "vehicle" in quoting (a configurable offer) means something different from a "vehicle" in contracts (a physical car driving around). Three boundary diagrams make the mapping concrete: one credit domain split into retail and fleet bounded contexts with two services; the same two contexts sharing one service with a shared module because the credit check logic is nearly identical; and one bounded context deliberately split into two services because fleet carries 90% of revenue and a retail bug must not overload its database. Boundaries also come from law, risk, performance, and org size. Overlap between boundaries is inevitable, so allow it deliberately, and duplicate data rather than fight that overlap.

### [20:13](https://youtu.be/eFSEg54mwVU?t=1213) Relationships: who really depends on whom
A calls-B diagrams show runtime calls but not whose success depends on the other. Hillaert explains context-mapping patterns through an extended analogy with his wife: he asks for steak, then changes his mind to chicken, and she cooks steak anyway (he is downstream, she is upstream, regardless of who called); she buys only vegetables and cookies from his steak-vegetables-cookies list (anti-corruption layer: she protects her own model); he buys exactly the tofu, vegetables, and champagne she asked for (conformist). Customer-supplier is the special upstream/downstream case where downstream pays and therefore shapes the model. An advanced diagram shows services C and B sharing a model (shared kernel) while each conforms to a different upstream service, which puts unresolvable stress on the shared model: influence flows from D into C into B, but B cannot move because it answers to A. The advice is to apply context mapping selectively, when reasoning about a specific change, not to map the whole landscape. Event storming and domain storytelling get a passing mention as discovery techniques.

### [30:38](https://youtu.be/eFSEg54mwVU?t=1838) Implementation: monoliths, modules, and deliberate communication
Choosing microservices over a modular monolith is itself a decision to weigh: the monolith has one deployment, in-process calls, and lower operational cost. But the modular monolith's easy-boundaries story is oversold: five in-process calls become five network hops once you extract, so bad boundaries hurt at extraction time either way. Communication options are in-process calls, synchronous APIs, async messaging, and data replication, and the choice should follow the relationship between the services. Heavy synchronous reads from other services signal a wrong boundary; replicate the data to where decisions are made instead. Async messaging removes the direct connection but keeps contract and versioning coupling, so it deserves the same scrutiny as a REST contract.

### [34:50](https://youtu.be/eFSEg54mwVU?t=2090) Choreography vs orchestration
Cross-service processes get two options. Choreography (events, no process owner) avoids a single point of failure but makes it hard to know the process state or locate faults. Orchestration puts one component in charge of executing the workflow without owning the domain knowledge of each step, which makes progress tracking and compensation (there are no distributed rollbacks) easier at the cost of a single point of failure. The slide's bottom line: when the process is explicit, orchestration is easier to reason about.

### [36:29](https://youtu.be/eFSEg54mwVU?t=2189) Don't layer your services
Hillaert confesses to an old habit: layering services so that experience APIs and backends-for-frontend hold no logic and must call domain-aligned services, which in turn call data or orchestration services. That restricts what a service can do and strips its ownership. A backend-for-frontend should be able to fulfill a use case itself, including holding the new capability, and only move it to a domain-aligned service once wider reuse is proven. Calling a domain-aligned service directly from outside is fine; the difference is influence. An experience API is shaped by its consumer, while a domain-aligned service refuses external shaping and follows its business context.

### [39:36](https://youtu.be/eFSEg54mwVU?t=2376) What a service looks like, and how small it must be
The typical service holds APIs, scheduled jobs, message handlers, and a database. Then the provocation: a read-only database can be a microservice if it is independently deployed and evolvable with clear ownership. His example is automotive reference data (VIN checks, factory options, part prices) used by quoting and damage-claim systems alike; building one API to serve every consumer's needs costs more than letting teams query the owned database directly, with the owning team publishing updates and sharing knowledge. On size: "micro" is a bad name, and no line count or endpoint count defines it. A service must be as big as it needs to be to stay coherent and manageable by its team, even with 100 endpoints.

### [44:21](https://youtu.be/eFSEg54mwVU?t=2661) Close: make it deliberate
Before creating a service, ask whose success depends on it, what data must stay coherent, and what transactionality is needed. The closing slide restates the thesis: microservices distribute ownership and responsibility without losing coherence, not merely software. No audience questions followed; the speaker pointed to the Devoxx site for the deck and asked for feedback.

## Who should watch
Architects and senior developers designing or rescuing service landscapes, especially anyone using DDD vocabulary loosely or defaulting to async messaging as a decoupling fix. Skip it if you already apply context mapping and strategic DDD daily; the patterns will be familiar and the talk offers no code or production metrics to study.

## Verdict
**6/10**: A coherent framework for service boundaries, ownership and relationships, carried by the speaker's leasing examples and weighed trade-offs, with no artifact to take home.

**Novelty 1/2**

- **+** [15:24](https://youtu.be/eFSEg54mwVU?t=924) The three retail/fleet boundary diagrams map one credit domain three ways, grounding the claim that a bounded context is not a microservice.
- **+** [21:15](https://youtu.be/eFSEg54mwVU?t=1275) Upstream/downstream, conformist and anti-corruption layer are taught through one sustained analogy of his own rather than recited.
- **−** The context-mapping vocabulary itself (upstream/downstream, shared kernel, customer-supplier, conformist, anti-corruption layer) is the pattern catalogue from Evans' *Domain-Driven Design* and the first DDD context-mapping results a search returns.

**Demonstrated 1/2**

- **·** [34:50](https://youtu.be/eFSEg54mwVU?t=2090) A talk about ownership and boundaries has nothing runnable to show; its diagrams of choreography, orchestration and context maps carry the argument instead.

**Measured 1/2**

- **·** [17:31](https://youtu.be/eFSEg54mwVU?t=1051) The talk makes no quantitative claims; the "90% of our revenue" for fleet is illustrative scenario setup, not a measurement.

**Depth 2/2**

- **+** [18:04](https://youtu.be/eFSEg54mwVU?t=1084) Risk is given as a reason to split one bounded context into two services: a retail bug overloading a database would hit the fleet customers behind most of the revenue.
- **+** [35:56](https://youtu.be/eFSEg54mwVU?t=2156) Choreography and orchestration are weighed on state visibility, fault location, compensation without distributed rollback, and single-point-of-failure risk, ending in a stated rule for choosing.
- **−** [39:06](https://youtu.be/eFSEg54mwVU?t=2346) The claim that domain-aligned services should refuse external shaping is asserted without an example of what that refusal costs a consumer.

**Reusable 1/2**

- **+** [44:21](https://youtu.be/eFSEg54mwVU?t=2661) The closing questions (whose success depends on it, what data must be coherent, what transactionality is needed) can be used in a design review.
- **−** [44:21](https://youtu.be/eFSEg54mwVU?t=2661) The heuristics stay in the talk; no repository, configuration or checklist file accompanies it.
