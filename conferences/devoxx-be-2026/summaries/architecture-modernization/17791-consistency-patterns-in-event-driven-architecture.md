---
title: Consistency Patterns in Event-Driven Architecture
talkId: "17791"
conference: devoxx-be-2026
speakers: [Emanuel Trandafir]
track: Architecture & Modernization
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=8JuQaWFKk4w
durationMin: 45
slides: null
verdict: 7
reach: segment
frames: 9
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Consistency Patterns in Event-Driven Architecture

Emanuel Trandafir · Conference · Architecture & Modernization

## TL;DR

Distributed systems cannot update two systems atomically, so consistency has to be designed: undo failed work with sagas, coordinate with orchestration or choreography, and publish reliably with outbox/inbox plus idempotent consumers. A live demo shows why I/O inside a database transaction degrades the whole service.

## Key takeaways

- One database transaction cannot cover external calls (broker publish, HTTP, email): the external effects cannot roll back.
- I/O inside a transaction holds connections open, so a slow downstream dependency exhausts the pool and slows even unrelated read-only endpoints.
- On failure, run compensations undoing each completed step (e.g. cancel the order when stock reservation fails), and make them idempotent.
- Orchestrate complex workflows needing robust error handling in one place; choreograph where services should evolve independently.
- Exactly-once delivery does not exist; aim for at-least-once publishing (outbox) with idempotent consumers (inbox plus idempotency key).
- If sagas and inbox/outbox feel like too much machinery, a well-built modular monolith (Spring Modulith was named) may be the better answer.

## Notes

### [03:15](https://youtu.be/8JuQaWFKk4w?t=195) The dual-write problem

The running example is an e-commerce `createOrder` that inserts an order row, updates products, publishes a Kafka event, writes a file, POSTs to a loyalty service, and sends an email. If the email fails, the database rolls back but the Kafka message and the loyalty POST are already out. Even two databases hit the same wall, since no atomic commit spans them.

### [08:23](https://youtu.be/8JuQaWFKk4w?t=503) Sagas: compensate instead of rolling back

Since the broker cannot be rolled back, recovery means compensation: inventory publishes "stock unavailable" and the order service cancels the order. Trandafir quotes Chris Richardson's definition from Microservices Patterns: a saga is a sequence of local transactions, each updating its database and publishing a message triggering the next, with compensating transactions on failure.

### [12:34](https://youtu.be/8JuQaWFKk4w?t=754) Orchestration vs choreography

Orchestration adds a central coordinator sending commands ("create order", not the "order created" event) that owns the workflow and error handling; all coupling moves into the orchestrator, and adding a service means changing and redeploying it. Choreography drops the coordinator: each service runs its logic and publishes domain events, so new services just subscribe, at the cost of error handling spread across every participant. The advice at [16:10](https://youtu.be/8JuQaWFKk4w?t=970): orchestrate complex workflows, choreograph where evolution speed matters, or mix both with the choreographed side reaching the orchestrated side only via its orchestrator.

### [19:46](https://youtu.be/8JuQaWFKk4w?t=1186) Demo: the cost of I/O inside a transaction

The naive fix, wrapping save-then-publish in `@Transactional`, fails twice: a slow external call starves the connection pool, and a commit failure after a successful publish still loses consistency. The live demo injects downstream latency with Toxiproxy: baseline GETs take about 20 ms and stay flat with 300 ms injected, but at roughly 1 second the read-only GETs degrade too because every pool connection is stuck waiting.

### [24:55](https://youtu.be/8JuQaWFKk4w?t=1495) Delivery guarantees and the outbox pattern

Publish-without-a-transaction is at-most-once: fine for a promotional message, unacceptable in the financial-markets systems Trandafir worked on. Exactly-once is unachievable, so the target is at-least-once: one transaction saves the order row and an event row in an outbox table, then a background poller (or CDC) publishes pending events, retrying until it succeeds. The poller itself dual-writes (publish, then mark-as-published), so a crash between the two yields duplicates; the mitigation is an idempotency-key header plus an observed-at timestamp for reordering. Spring was named as having support that automates much of this.

### [34:09](https://youtu.be/8JuQaWFKk4w?t=2049) The inbox pattern and idempotent consumers

The consumer mirrors the split: save the incoming event into an inbox table first, then a poller runs business logic and marks it processed. The idempotency key becomes a unique-constrained inbox column, so duplicates fail fast; the handler must catch that violation and acknowledge rather than retry forever. Skip the inbox when the consumer is naturally idempotent via a unique business field, and consider retry topics plus a dead-letter queue for poison messages.

### [38:56](https://youtu.be/8JuQaWFKk4w?t=2336) Recap and Q&A

The closing maps every pattern onto the three axes from Software Architecture: The Hard Parts: consistency, coordination, communication. Q&A covered one table per queue vs shared (Spring uses a single shared table with a blob payload, per the speaker) and why Kafka transactions were left out (two commits still cannot be atomic).

## Tools, libraries and specs

- Apache Kafka (message broker in the examples)
- Spring Modulith (suggested path toward a modular monolith)
- Toxiproxy (latency injection in the live demo)
- Spring's outbox support (named as automation for the pattern, no version stated)

## Who should watch

Developers moving from a monolith to event-driven services who keep dual-writing the database and the broker in one transaction, and anyone choosing between saga orchestration and choreography. Practitioners already running outbox/inbox will find the patterns familiar and can skip to the demo and the trade-off guidance.

## Verdict

**7/10**: A patterns tour whose live demo shows I/O inside a transaction starving the connection pool with a measured baseline and comparison, limited by textbook-level synthesis, outbox and inbox shown only as diagrams, and no published artifact.

**Reach segment**: Backend teams who write to a relational database and publish to a message broker can apply the saga, outbox and inbox patterns in their own services; teams without an event-driven or broker-based design have little to apply.

**Novelty 1/2**

- **+** [38:56](https://youtu.be/8JuQaWFKk4w?t=2336) The recap maps dual write, saga, orchestration, choreography, outbox and inbox onto the consistency, coordination and communication axes from *Software Architecture: The Hard Parts*, bringing the book's taxonomy together with the talk's patterns.
- **+** [26:27](https://youtu.be/8JuQaWFKk4w?t=1587) The at-least-once recommendation is grounded in the speaker's financial-markets work, where the team could not afford to miss a single message.

**Demonstrated 1/2**

- **+** [20:17](https://youtu.be/8JuQaWFKk4w?t=1217) The live demo runs a two-endpoint app with an artificial downstream delay added on screen, the control page, dashboard and sequence diagrams visible while load runs.
- **−** [27:29](https://youtu.be/8JuQaWFKk4w?t=1649) The outbox and inbox the talk recommends are shown only as flow diagrams after "let's see how to implement it", never running.

**Measured 2/2**

- **+** [20:47](https://youtu.be/8JuQaWFKk4w?t=1247) GETs take about 20 ms at baseline and stay flat with 300 ms of injected downstream delay, while at about 1 s the dashboard at [22:35](https://youtu.be/8JuQaWFKk4w?t=1355) shows GET latency climbing too as the pool exhausts, with the injected delay as the stated method.
- **−** [30:36](https://youtu.be/8JuQaWFKk4w?t=1836) The outbox's cost is stated as "a bit of extra latency" through another table, with no number.

**Depth 2/2**

- **+** [13:05](https://youtu.be/8JuQaWFKk4w?t=785) Orchestration and choreography are weighed on where coupling lives ("moved to the right, to the orchestrator") and deployment friction, against choreography's spread-out error handling at [15:07](https://youtu.be/8JuQaWFKk4w?t=907).
- **+** [29:05](https://youtu.be/8JuQaWFKk4w?t=1745) The outbox is shown to keep a residual dual write mitigated by an idempotency key, and the inbox turns that key into a unique-constrained column with acknowledge-on-duplicate at [35:12](https://youtu.be/8JuQaWFKk4w?t=2112).
- **−** [25:26](https://youtu.be/8JuQaWFKk4w?t=1526) Exactly-once delivery is declared impossible through a Santa Claus story, with no argument about the commit and acknowledge window.

**Reusable 1/2**

- **+** [03:30](https://youtu.be/8JuQaWFKk4w?t=210) The `createOrder` code on screen and the outbox and inbox flow diagrams (also [35:00](https://youtu.be/8JuQaWFKk4w?t=2100)) give enough to reconstruct each pattern.
- **−** [41:00](https://youtu.be/8JuQaWFKk4w?t=2460) The closing points only to slides on LinkedIn and a feedback QR: no repository, sample project or checklist for the demo app or the patterns.
