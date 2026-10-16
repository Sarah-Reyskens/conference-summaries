---
title: The Hexagonal Hangover
talkId: "8186"
conference: devoxx-be-2026
speakers: [Ties van de Ven]
track: Architecture & Modernization
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=m9viRAIRAUQ
durationMin: 49
slides: https://docs.google.com/presentation/d/1DE-YL-QsrCwZOkDeOtvLLSoiQVoZ26ZnO9MrcqfCtko/edit?usp=sharing
verdict: 6
reach: broad
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# The Hexagonal Hangover

Ties van de Ven · Conference · Architecture & Modernization

Slides: https://docs.google.com/presentation/d/1DE-YL-QsrCwZOkDeOtvLLSoiQVoZ26ZnO9MrcqfCtko/edit?usp=sharing

## TL;DR

Adding layers is not the same as adding quality: every abstraction relocates dependency and raises the cost of understanding the whole. Van de Ven presents a mental model built on cohesion, distance and coupling, ending in the formula Pain = Spaghettification × Volatility, and uses it to show where hexagonal architecture helps and where it charges rent.

## Key takeaways

- Every abstraction layer relocates a dependency instead of removing it, so at some point pick a layer and commit rather than stacking frameworks.
- A mapper between database entities and API models absorbs representational change such as renames, but not information loss such as dropped columns.
- Aim components at functional cohesion: one use case per component, a place-order component rather than an order component.
- Think in state changes with one domain model per state, so the type system rejects calls made in the wrong state.
- A Java interface adds no contract strength beyond its signatures; introduce one only for multiple implementations or dependency inversion.
- Keep fan-in contracts as weak as possible and demand strong contracts from fan-out; that balance decides where change stays cheap.
- No change means no architectural pain, so invest in structure where volatility is highest.

## Notes

### [00:32](https://youtu.be/m9viRAIRAUQ?t=32) Introduction

Van de Ven is a software quality expert at Alliander, where he helps about 200 teams with code quality and security, and volunteers as a coach at the ArnhemJUG. He credits the talk's mental model to his colleague Boyen van Gorp. The talk contains no AI content by design: fundamentals only.

### [02:04](https://youtu.be/m9viRAIRAUQ?t=124) Everything is a trade-off

The opening question is when an architecture is good enough. The answer "it depends" only helps once you know what it depends on, and the talk's answer is trade-offs: understanding begins where tricks end. The Fruittella candy bag makes the point: each wrapper has a purpose (weather protection, sharing, keeping melted sweets apart), yet every wrapper stands between you and the candy. Layers in software behave the same way: useful until you need to understand how something actually works, at which point clicking through interface after interface to single implementations gets in the way.

### [05:40](https://youtu.be/m9viRAIRAUQ?t=340) Why we add layers

Layers exist for two reasons: "I don't want to depend on this" and "I don't want your changes to break me". The dependency story walks a familiar stack: database, JDBC, Hibernate, Spring Data, then a hand-rolled framework on top, each layer added to escape the one below. The lesson is that you never escape a dependency, it relocates, and each shared layer exposes only the common subset, so features get lost (quoting Joel Spolsky on leaky abstractions). The change-protection story maps a database entity to an API model so a column rename stops breaking clients, which also enables local reasoning. But the mapper only guards against representational change; if the column or table disappears, no mapper restores the information.

### [10:50](https://youtu.be/m9viRAIRAUQ?t=650) The Kafka rewrite story

A previous employer inherited a project: tens of thousands of lines, abstractions over abstractions, internal message queues, built over almost a year. After a 90-minute explanation it turned out the application moved two message types from one Kafka topic to another. Van de Ven discontinued it and rewrote both relays in an afternoon on the native Kafka client, duplicating a small amount of business logic. The original optimized for hypothetical change at high cost and complexity; the rewrite was cheap and simple but duplicated logic and did not extend. Neither choice was free, which motivates the need for a way to expose trade-offs.

### [13:28](https://youtu.be/m9viRAIRAUQ?t=808) Cohesion and distance from code

Architecture reduces to three concepts: cohesion, coupling and distance. A Java example grows on screen from reading a file, to posting its first line to a REST endpoint, to writing a summary log, until it stops being readable at a glance. Inserting blank lines restores readability, which reveals two things: the blank lines add distance, and their placement judges that some lines are more cohesive with each other than with the rest. Architecture diagrams generalize this: blocks are cohesion, arrows are coupling. Four cohesion levels follow: accidental (the utils folder), logical (grouped by function, as in MVC or layered architectures), model (working on the same data, such as a user component) and functional (grouped by use case). The recommended route to functional cohesion is thinking in state changes: input to validated input to enriched input to solution, each state a domain model, each transition a component, so the type system enforces valid sequencing.

### [22:22](https://youtu.be/m9viRAIRAUQ?t=1342) Distance and coupling

Distance ranges from the same function to a different company. It buys team parallelism, independent deployability and scaling, plus lower local cognitive load, which is why microservices fit organizations so well. It charges path topology (tracing a request across services and teams) and a higher cost of change: a rename that takes seconds in a monolith can require migration plans or API versioning across distance. Coupling splits into depth (chance of a breaking change) and connectivity (blast radius). Depth has three levels: intrusive (reflection, casting an interface to its implementation, with zero compiler warnings), functional (changes in A silently break B, via shared mutable state or temporal coupling such as files dropped for pickup) and contract (explicit, where conforming changes should not break). A Java interface is not a stronger contract than the signatures inside it; it only serves multiple implementations or dependency inversion, otherwise it adds distance. Contracts also suffer misalignment: the venue that hangs the concert piano from the ceiling honored the letter, the unmodifiable list that throws on add violates the expectation behind List, and performance or security expectations usually sit outside the written contract entirely. For connectivity, fan-in wants the weakest contract possible so the component stays easy to change, while fan-out wants the strongest contracts available; god objects combine high fan-in with high fan-out, and functional cohesion shrinks both.

### [39:29](https://youtu.be/m9viRAIRAUQ?t=2369) The architecture mental model

The concepts combine into four relations, offered as a way of thinking rather than quantities to implement: Coupling = Depth × Connectivity, CohesionDebt = functional cohesion minus actual cohesion, Spaghettification = Coupling + CohesionDebt, and Pain = Spaghettification × Volatility. Depth and connectivity compensate, so a reflection-heavy component nobody depends on is tolerable, while a widely depended-upon component needs tight contract coupling. The bottom line carries the talk: volatility decides whether bad structure hurts. An untouched ball of spaghetti costs nothing; a heavily changed application pays for every bit of spaghettification.

### [41:35](https://youtu.be/m9viRAIRAUQ?t=2495) Hexagonal through the model

Hexagonal architecture gets a quick recap: incoming adapters and anti-corruption layers (mapping plus validation) feed a core domain that knows nothing of the outside world, with ports shielding it from external sources. Through the model it scores well on functional cohesion in the core and contract coupling at the ports, modulo misalignment risk. Its cost is distance: a single request crosses adapter, anti-corruption layer, incoming port, business logic, outgoing port, another anti-corruption layer and the outgoing adapter. Building all of that upfront is expensive when no change ever comes, and genuine breaking changes such as unreliable production data must be fixed in every layer. The closing restates the thesis: nothing is wrong with hexagonal, but more layers are not always better, so avoid dogma and weigh the trade-off each time.

## Tools, libraries and specs

- JDBC, Hibernate, Spring Data: the abstraction stack in the dependency-relocation example.
- Apache Kafka (native client): what the afternoon rewrite used instead of the abstraction-heavy relay.
- IntelliJ IDEA: single-implementation navigation when clicking through interface chains.

## Who should watch

Developers and tech leads who choose or defend layered and hexagonal architectures, or who argue about abstractions with their teams, get a vocabulary for those debates. Teams looking for hexagonal implementation guidance, runnable code, or formal architecture metrics should look elsewhere.

## Verdict

**6/10**: A trade-off framework for architecture decisions with reasoned explanations of contracts, connectivity and hexagonal costs, supported by experience and anecdotal numbers rather than measured comparisons or a reproducing artifact.

**Reach broad**: Most of the conference audience designs, reviews or debates layered service architectures and can use the cohesion, coupling and volatility trade-offs in their own work.

**Novelty 1/2**

- **+** [01:33](https://youtu.be/m9viRAIRAUQ?t=93) The speaker credits a colleague's mental model and their discussions as the basis for the talk's architecture framework.
- **+** [12:27](https://youtu.be/m9viRAIRAUQ?t=747) The Kafka relay experience weighs readiness for hypothetical changes against a simple rewrite that accepts duplicated logic and limited extensibility.

**Demonstrated 1/2**

- **·** [14:32](https://youtu.be/m9viRAIRAUQ?t=872) The on-screen code illustrates readability and distance rather than runnable behavior; as a trade-offs talk, the subject has nothing to run.

**Measured 1/2**

- **+** [11:55](https://youtu.be/m9viRAIRAUQ?t=715) The rewrite comparison puts numbers on the claim: tens of thousands of lines built over almost a year replaced in an afternoon with the native Kafka client.
- **−** [10:50](https://youtu.be/m9viRAIRAUQ?t=650) The year-versus-afternoon comparison is an anecdote with no method: no side-by-side scope and no follow-up on maintenance cost.
- **−** [44:39](https://youtu.be/m9viRAIRAUQ?t=2679) The claims of upfront cost and expensive repairs across layers come without measured costs, while the missing-field frequency is an illustrative example.

**Depth 2/2**

- **+** [30:06](https://youtu.be/m9viRAIRAUQ?t=1806) The interface argument explains why no contract strength is added beyond the signatures, with the rule for when an interface earns its place.
- **+** [34:48](https://youtu.be/m9viRAIRAUQ?t=2088) The connectivity treatment explains why fan-in wants weak contracts and fan-out strong ones, and how that decides where change is allowed.
- **+** [41:35](https://youtu.be/m9viRAIRAUQ?t=2495) Hexagonal is assessed through the model with both sides weighed: functional cohesion and contract coupling against distance and change cost.

**Reusable 1/2**

- **+** [19:48](https://youtu.be/m9viRAIRAUQ?t=1188) The state-changes technique, with one domain model per state, is described as a practice viewers can reconstruct.
- **−** [47:44](https://youtu.be/m9viRAIRAUQ?t=2864) The close points to LinkedIn and the speaker's site, not to a repository, sample or checklist covering the method.
