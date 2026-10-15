---
title: "From a startup stack to 5 microseconds: inside a crypto trading engine"
talkId: "9029"
conference: devoxx-be-2026
speakers: [Oleg Lobanov]
track: Architecture & Modernization
sessionType: Conference
audienceLevel: ADVANCED
video: https://www.youtube.com/watch?v=vcL6eCAwLwY
durationMin: 45
slides: null
verdict: 7
frames: 11
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# From a startup stack to 5 microseconds: inside a crypto trading engine

Oleg Lobanov · Conference · Architecture & Modernization

## TL;DR

Bitvavo, a European crypto exchange processing about half of euro-denominated crypto trades, rebuilt its matching core from a database-centered startup stack into a replicated state machine on Aeron, reaching 5-microsecond in-memory order processing and sub-millisecond p99 end to end. Lobanov walks through why determinism drove every decision, from Raft log replication and SBE encoding to JVM allocation hygiene. The talk leaves a concrete checklist for anyone building low-latency deterministic systems on the JVM.

## Key takeaways

- Determinism is a correctness property for exchanges: replaying the same input log must reproduce the same state, which rules out goroutine-per-request parallelism, wall clocks, unseeded randomness, and unsorted HashMap iteration.
- A replicated state machine (single ordered input log plus a single-threaded transition function) buys determinism, lock-free speed, and replay debugging: copy the production log locally and step through history with breakpoints.
- Reliability does not require TCP: sequence numbers plus NACK-based retransmission of only the missing packet plus heartbeats give a reliable stream over UDP, which is what Aeron implements.
- Feature flags and configuration that affect matching logic must enter through the ingress log as sequenced commands, never as per-node config files, or nodes diverge.
- Upgrades of a stateful cluster need layered protection: CI replays the same ingress on old and new versions and compares output log plus state, and production runs shadow divergence checks.
- Bugs in an immutable-history system are fixed with compensating admin commands (for example, correcting a user balance), never by rewriting history, because downstream systems and regulators already consumed the output log.
- Microsecond processing on the JVM comes from a three-layer checklist: zero allocation after startup, single-writer concurrency, and pinned isolated CPUs with kernel bypass.

## Notes

### [01:38](https://youtu.be/vcL6eCAwLwY?t=98) Bitvavo and why latency matters

Bitvavo is a Amsterdam-headquartered exchange founded in 2018, operating in 27 countries with over 100 billion euro in yearly volume and more than 7 billion in assets under custody. Roughly 50% of euro-against-crypto trades flow through it, and it runs 24/7 with no maintenance windows. Latency predictability matters because market makers (high-frequency firms providing liquidity) build pricing models on expected execution time; a p99 that swings between 5 and 100 ms makes their models lose money.

### [04:48](https://youtu.be/vcL6eCAwLwY?t=288) The startup stack and its limits

The 2018 architecture was textbook: API gateway routes through Redis pub/sub channels to matching engines, all state in a MySQL cluster, with a Debezium CDC feed publishing order and trade transitions to Kafka for post-trade systems and reporting. Four limits forced the rebuild: the system was non-deterministic (parallel goroutines and async operations meant replaying input could not reproduce output); shared MySQL and Redis created locks, contention, and noisy-neighbor effects between markets; tail latency was unpredictable (network hops, GC); and throughput capped out on what was already the largest AWS MySQL cluster available. The target for the new system was 10x throughput, low and flat tail latency, high availability, and provable 100% determinism.

### [11:07](https://youtu.be/vcL6eCAwLwY?t=667) Replicated state machine and Raft

The chosen pattern keeps a single append-only ordered input log feeding a state machine that is just a function of current state plus the next event, producing a state transition. Because it is single-threaded there are no locks and no contention, and because it is replicated across nodes the data survives node loss. Log replication uses the Raft consensus protocol: clients talk to the leader, the leader appends the command to its log and forwards it to followers, followers acknowledge, and once a majority acknowledges the leader commits that position and only then may any state machine touch the event. Leader election on failure takes a few milliseconds.

### [15:47](https://youtu.be/vcL6eCAwLwY?t=947) Rules for staying deterministic

Four pitfalls get concrete examples. Side effects are banned: if the leader gets HTTP 200 from a bank API and a follower gets 400, state diverges, so only the leader may call out and the response re-enters through the input log. Wall clocks are banned: the leader timestamps each event before appending, so a market opening at 08:00 opens on every node at the same logical time. Randomness is banned unless seeded from the input (for example, the event sequence number) so replays reproduce the same values. Iteration over HashMap or HashSet must be sorted first because traversal order is not guaranteed identical across machines.

### [20:30](https://youtu.be/vcL6eCAwLwY?t=1230) From JSON to SBE, from TCP to reliable UDP

JSON became a bottleneck: ASCII parsing to find a field such as the market in a create-order command burns CPU and generates garbage that the collector must reclaim, hurting tail latency. The replacement is SBE (Simple Binary Encoding), a schema-first zero-copy protocol using the flyweight pattern: the parser knows the price sits at a fixed offset, so it reads straight from the buffer without allocating, and the contiguous layout stays cache-friendly. TCP was the next bottleneck: ACK-based slow recovery after loss, one connection per consumer for fan-out, 20 to 32 byte headers, and congestion control. The alternative is user-space reliability over UDP: sequence numbers detect gaps, the receiver NACKs only the missing packet instead of resending the whole stream from that point, and periodic heartbeats cover idle periods and liveness. Rather than building this, Bitvavo adopted the open-source Aeron library (reliable UDP transport plus the Raft-based Aeron Cluster), with enterprise support for the exchange core.

### [28:52](https://youtu.be/vcL6eCAwLwY?t=1732) Exchange 2.0 and its operational price

Users still speak JSON; the API gateway translates JSON to SBE and sends it over Aeron UDP to the cluster, where leader and replica matching engines hold identical in-memory state, each with an archive of the replicated output log. Post-trade systems (settlement, reporting, analytics) tail the archive, and adapters still populate MySQL so the rest of Bitvavo kept working, which made the migration plug and play. Operating the cluster costs discipline: feature flags ride the ingress channel as commands; upgrades are validated by replaying identical ingress on old and new versions in CI and comparing output plus state, with similar checks on production; history is never rewritten, so production bugs are repaired with compensating commands; and divergence detection runs on every environment.

### [36:47](https://youtu.be/vcL6eCAwLwY?t=2207) The low-latency checklist

Memory hygiene means pre-allocating everything at startup with object pools or ring buffers, never using String or boxed objects on the hot path (the gateway maps strings to int or long IDs, for example BTC to 1, and maps back on the way out), and using primitive collections such as Agrona or FastUtil Int2ObjectHashMap. Concurrency means the single-writer principle (business container and networking layer communicate over ring buffers or IPC), wait-free messaging, and no false sharing (pad hot variables, @Contended). OS and hardware means pinning hot threads to isolated cores and bypassing the kernel network stack with Solarflare or DPDK, writing straight to NIC buffers from user space.

### [43:13](https://youtu.be/vcL6eCAwLwY?t=2593) Production numbers

About a year of reimplementation and migration paid off. End-to-end p99 fell from 5-200 ms to under 1 ms, and the latency curve is flat with no spikes. A single order (risk check, balance check, reservations, matching, trade processing) takes 5 microseconds in memory. End-to-end throughput rose 5x from 20k to 100k orders per second, which the speaker stressed is current load rather than the architectural ceiling; 200-500k is reachable by improving known components.

## Tools, libraries and specs

- Aeron (reliable UDP transport, Aeron Cluster Raft consensus, SBE messaging)
- SBE (Simple Binary Encoding, schema-first zero-copy protocol)
- Raft consensus protocol
- Agrona / FastUtil primitive collections (Int2ObjectHashMap)
- Solarflare / DPDK kernel bypass
- Redis pub/sub, MySQL, Debezium CDC, Kafka (legacy stack)

## Who should watch

Backend engineers building latency-sensitive or deterministic systems (trading, fintech, real-time platforms) gain the most, especially JVM developers curious how far allocation discipline and Aeron can go. Architects weighing a rebuild of a database-centered core get a full decision trail with production numbers. Skip it if you want Aeron or SBE tutorials with code; the talk explains why each was chosen, not how to program against them.

## Verdict

**7/10**: A production rebuild with its design reasons and operating rules, limited by a results slide with no stated measurement method and no published artifact.

**Novelty 2/2**

- **+** [06:22](https://youtu.be/vcL6eCAwLwY?t=382) The speaker gives his team's reasons for leaving the 2018 stack: non-deterministic parallel processing, shared MySQL and Redis contention, unpredictable tail latency, and the largest AWS MySQL cluster already in use.
- **+** [32:36](https://youtu.be/vcL6eCAwLwY?t=1956) The operating rules (feature flags as ingress commands, CI replay of old and new versions, compensating commands instead of history rewrites at [34:42](https://youtu.be/vcL6eCAwLwY?t=2082)) come from running the cluster, not from library docs.

**Demonstrated 1/2**

- **·** [28:52](https://youtu.be/vcL6eCAwLwY?t=1732) The subject is a live exchange core that cannot run on a conference stage, so architecture diagrams stand in for a working demo and the evidence lands in Measured.

**Measured 1/2**

- **+** [43:13](https://youtu.be/vcL6eCAwLwY?t=2593) The results slide pairs each figure with its baseline: p99 end-to-end (gateway to engine to gateway) from 5-200 ms to under 1 ms, and throughput from 20k to 100k orders/s at [44:18](https://youtu.be/vcL6eCAwLwY?t=2658).
- **−** [43:44](https://youtu.be/vcL6eCAwLwY?t=2624) The "flat, no spikes" latency and the 5-microsecond order time are stated with no chart, load profile or measurement setup.

**Depth 2/2**

- **+** [23:06](https://youtu.be/vcL6eCAwLwY?t=1386) The TCP section weighs ACK-based recovery, per-consumer connections, header sizes and congestion control against sequence numbers and single-packet NACKs before naming Aeron as the adopted answer.
- **+** [26:45](https://youtu.be/vcL6eCAwLwY?t=1605) The build-vs-buy decision is explained: reimplementing the reliable-UDP concepts would take "maybe like three years to create and polish", so the team adopted Aeron.
- **−** [29:23](https://youtu.be/vcL6eCAwLwY?t=1763) What happens inside the cluster when a message arrives is skipped with "Some magic happens", so the engine's own processing stays closed.

**Reusable 1/2**

- **+** [36:47](https://youtu.be/vcL6eCAwLwY?t=2207) The low-latency checklist names practices and libraries (startup allocation, single writer, Agrona/FastUtil primitives, CPU pinning, DPDK) in enough detail to reconstruct.
- **·** [44:49](https://youtu.be/vcL6eCAwLwY?t=2689) The closing slide shows only QR codes for questions and feedback, with no repository, sample project or configuration for the talk's content.
