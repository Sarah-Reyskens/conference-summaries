---
title: Integration patterns for distributed systems
talkId: "8166"
conference: devoxx-be-2026
speakers: [Dirk Fröhner, Sabarish Sekar]
track: Architecture & Modernization
sessionType: Conference
audienceLevel: ADVANCED
video: https://www.youtube.com/watch?v=_CtnBnmYQC0
durationMin: 49
slides: null
verdict: 5
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-15
---

# Integration patterns for distributed systems

Dirk Fröhner, Sabarish Sekar · Conference · Architecture & Modernization

## TL;DR

Two AWS solutions architects argue that integration is an integral part of application architecture, not an afterthought, and walk through four fundamentals: coupling dimensions, control versus data flow, delivery semantics and ordering, and noisy-neighbor fairness in shared queues. Every option carries pain, so the architect's job is to identify the least painful one for the situation. A running ride-booking example ties the patterns together, with AWS services named as the concrete implementations.

## Key takeaways

- Treat coupling as a spectrum across location, format, temporal, and domain dimensions; each decoupling move shifts load somewhere else, usually onto the messaging system.
- Reverse domain coupling by publishing events to a topic instead of sending commands, then fan out to per-consumer queues so each downstream keeps buffering and independent pace.
- Plan for at-least-once delivery on both sides: producer retries after lost acknowledgements and consumer redelivery both create duplicates, so design idempotent consumers.
- Settle for partial order scoped to a partition or message group, and repair order and duplicates after the fact with a helper table keyed on business ids plus a monotonic version.
- Bound noisy-neighbor blast radius with cell-based or shuffle sharding across queues, and check whether the broker already implements the mitigation (SQS fair queues) before building it.

## Notes

### [05:13](https://youtu.be/_CtnBnmYQC0?t=313) Coupling and its dimensions

Larry Constantine's "stable if cohesion is high and coupling is low" opens the chapter. A synchronous REST call from a booking service to a payment service carries four couplings: location (DNS/URL), format (JSON over HTTPS), temporal (availability plus waiting for completion), and domain (understanding the payment API). As synchronous links chain, the coupling compounds. Moving to async APIs only partly reduces temporal coupling; inserting a queue removes the availability dependency and flattens peak load, shifting operational responsibility to a highly available broker. But request-response thinking keeps domain coupling on the producer, which must be touched for every downstream change. Topics reverse this: the producer publishes a `ride booked` event in its own domain, and consumers couple themselves to it. Couple on the producer side for commands with known downstream domains (payment must succeed); couple on the consumer side for events (loyalty reacts as it pleases). Topic-queue chaining (SNS fanning out to SQS queues) keeps both benefits.

### [17:44](https://youtu.be/_CtnBnmYQC0?t=1064) Control flow and flow control

Data flow (what moves) and control flow (who initiates) can point in different directions: producers push into a queue while consumers pull at their own pace, and that pull latency is the price of buffering. Full queues need flow control: TTL discards stale messages (a 10-minute-old booking request against a 5-minute SLA is dead), while back pressure on producers is a technical implementation of a business decision about who slows down. Push systems (webhooks, EventBridge) give the sender routing, filtering, and rate limiting, and suit realtime notifications; pull systems (SQS) give the consumer pacing control, simpler networking, and windowed streaming analytics. A pros-and-cons slide closes with the only architecturally correct preference: it depends.

### [25:02](https://youtu.be/_CtnBnmYQC0?t=1502) Delivery semantics and message order

Customers always ask for exactly-once delivery, so the talk derives why it is impossible from the producer side: the broker must durably store the message and acknowledge it, and a lost acknowledgement forces a retry that duplicates the message. Exactly-once semantics instead comes from broker-side deduplication, which needs a dedup id plus state, and is therefore always bounded: Kafka scopes it to producer id and sequence number, SQS to a 5-minute window. The consumer side redelivers too when its acknowledgement fails, so consumers must handle duplicates. On ordering, concurrent producers plus one network glitch break arrival order; since separate customers' messages have no causal relationship, partial order per producer suffices, and total order would demand infinite state just like unbounded dedup. Partitions (streaming) or message groups (messaging) implement the scope. A helper table storing messages with business ids and monotonic versions (not wall-clock timestamps) re-establishes order and discards duplicates after the fact, shown with a booked-then-cancelled ride at versions v1 and v2.

### [36:26](https://youtu.be/_CtnBnmYQC0?t=2186) Multi-tenancy: noisy neighbors and fairness in queues

One catch-all multi-tenant queue starves everyone when a single tenant's backlog dominates, whether from overproduction or slow/erroring consumers. One queue per tenant is dismissed as too expensive and operationally cumbersome (idle polling, onboarding machinery). Cell-based sharding splits tenants across independent cells so a noisy neighbor hurts only its cell: with four cells the blast radius is 25% of tenants. Shuffle sharding assigns each tenant two random queues from a pool; with 8 queues there are 28 unique pairs, so the chance of sharing both queues with the noisy neighbor drops to about 3.5%, and the talk extrapolates 0.02% at 100 shards. Known noisy neighbors get a hybrid: a dedicated queue for them, shared queues for the rest. Dynamic variants create overflow queues on detection, producer- or consumer-controlled, with consumption priority left to the business side. Both sharding designs are flagged as significant engineering effort, and SQS fair queues are named as the ready-made consumer-controlled overflow implementation, needing only a tenant id per message.

## Tools, libraries and specs

- Amazon SQS (queues, 5-minute dedup window, FIFO, fair queues) and SNS topic-to-queue fan-out
- Amazon EventBridge (push-based message bus with rules-based routing and filtering), Amazon MSK (managed Kafka), Amazon MQ (managed ActiveMQ/RabbitMQ for AMQP/JMS)
- Kafka producer id plus sequence number dedup; message groups and partitions for scoped ordering

## Who should watch

Architects and backend developers designing async or multi-tenant messaging who want the trade-off reasoning behind queues, topics, dedup, ordering, and tenant isolation in one sitting. Viewers already fluent in messaging semantics, or those wanting non-AWS implementations or runnable code, can skip it.

## Verdict

**5/10**: Four distributed-systems fundamentals with the reasoning derived on stage, held back by slides-only delivery, computed rather than measured numbers and no published artifact.

**Novelty 1/2**

- **+** [05:43](https://youtu.be/_CtnBnmYQC0?t=343) The four pillars bring several sources together, opening with Larry Constantine's "a structure is stable if cohesion is high and coupling is low" credited on screen.
- **+** [30:14](https://youtu.be/_CtnBnmYQC0?t=1814) The exactly-once and ordering arguments are built from the producer side, which Dirk Fröhner calls "often neglected".
- **+** [36:26](https://youtu.be/_CtnBnmYQC0?t=2186) The noisy-neighbor chapter runs from a catch-all queue through cell and shuffle sharding to producer- and consumer-triggered overflow queues, with the blast-radius arithmetic worked aloud.

**Demonstrated 0/2**

- **−** [34:51](https://youtu.be/_CtnBnmYQC0?t=2091) The helper-table dedup and reorder pattern is explained in narration only; no consumer code or running queue appears.
- **−** [47:23](https://youtu.be/_CtnBnmYQC0?t=2843) SQS fair queues are named as the ready-made mitigation with no console, configuration or behavior shown.

**Measured 1/2**

- **+** [42:40](https://youtu.be/_CtnBnmYQC0?t=2560) Cell sharding at 12.5% of tenants and shuffle sharding at 3.5% (1 of 28 queue pairs) compare two designs, with the pair counting done aloud.
- **·** [43:11](https://youtu.be/_CtnBnmYQC0?t=2591) The percentages, including the 0.02% extrapolation to 100 shards, are worked combinatorics rather than measurements of a running system.
- **−** [46:52](https://youtu.be/_CtnBnmYQC0?t=2812) "Mitigating this situation without queues would be 10x harder" gives a ratio with no baseline or method.

**Depth 2/2**

- **+** [27:38](https://youtu.be/_CtnBnmYQC0?t=1658) The lost-acknowledgement retry loop explains why exactly-once delivery is impossible, and [28:42](https://youtu.be/_CtnBnmYQC0?t=1722) why dedup state is bounded by time or scope.
- **+** [32:47](https://youtu.be/_CtnBnmYQC0?t=1967) Total order would need infinite state, so partial order scoped to a partition or message group is the working design, argued from two concurrent producers and a network glitch.
- **+** [46:52](https://youtu.be/_CtnBnmYQC0?t=2812) Each sharding option is weighed against its blast radius and engineering effort, ending in a check for broker features such as SQS fair queues before building.

**Reusable 1/2**

- **+** [35:55](https://youtu.be/_CtnBnmYQC0?t=2155) The helper-table pattern with business ids and monotonic versions is described step by step, with discard-or-upsert for duplicates.
- **·** [48:55](https://youtu.be/_CtnBnmYQC0?t=2935) The closing points to LinkedIn and the session survey, not to a repository, sample or checklist.
