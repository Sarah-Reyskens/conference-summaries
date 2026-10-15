---
title: "10 Billion Records vs. The Regulator: An Architectural Post-Mortem of an 11TB Exadata Failure"
talkId: "16408"
conference: devoxx-be-2026
speakers: [Martin Ladecky]
track: Architecture & Modernization
sessionType: Conference
audienceLevel: ADVANCED
video: https://www.youtube.com/watch?v=TB45qqp-OxM
durationMin: 49
slides: https://github.com/martin-ladecky/devoxx-belgium-2026
verdict: 7
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# 10 Billion Records vs. The Regulator: An Architectural Post-Mortem of an 11TB Exadata Failure

Martin Ladecky · Conference · Architecture & Modernization
Slides: https://github.com/martin-ladecky/devoxx-belgium-2026

## TL;DR

A Commerzbank tech lead walks through a real outage where an 11TB Oracle Exadata system holding 10 billion transaction records slowed to a crawl after a disaster-recovery test, locking users out while every monitor stayed green. The thesis is that recovery comes in ordered layers: ship good-enough first aid, apply a tactical fix before the next DR test, redesign read-side deduplication into the write path, then migrate off Oracle with dual writes and pilot users instead of a big bang.

## Key takeaways

- Ship first aid before root cause: raising a frontend timeout recovered 90% of users within 15 minutes and bought room to investigate.
- A system can return HTTP 200 everywhere with zero errors and still be a full outage; latency distributions matter more than error counters.
- After a failover to a cold replica, warm caches are the system: first logins took minutes, repeat logins were instant, and waiting beat intervening.
- Deduplication on every read collapses at scale; the fix is checking pending-against-booked once at write time and reducing reads toward a plain select.
- A single deleted date predicate silently removed the query window and forced full scans, so guard time-window filters as load-bearing code.
- CDC is not always an option: without admin privileges on a vendor-managed Exadata box, app-owned dual writes plus percentage rollouts with instant fallback are the controlled migration path.

## Notes

### [03:42](https://youtu.be/TB45qqp-OxM?t=222) Monday morning: the bank is down, everything is green

The speaker opens with a Monday-morning call that already holds 200 people, which in a large enterprise means a severe incident. "Bank is down" turns out to mean users cannot log in: the database is still answering, but normal 20-40 ms responses have stretched to anywhere between 100 ms and 20 minutes. Monitoring shows no errors at all, only HTTP 200s, while database CPU and IO run hot. The lockout comes from a hardcoded 30-second frontend timeout that logs users out for security reasons. Banks count as EU critical infrastructure, so the outage also means self-reporting to the BaFin regulator, with prolonged downtime escalating to government level.

### [08:31](https://youtu.be/TB45qqp-OxM?t=511) First aid: raising the timeout in a 15-minute deploy

Observation showed 90% of users got responses within 3 minutes, so the team raised the frontend timeout and deployed the hardcoded change to production in 15 minutes, a record against a normal two-week cycle. That recovered 90% of clients at the cost of multi-minute waits and took the pressure off. The lesson drawn is explicit: ship the good-enough fix first, then investigate with a cool head.

### [12:10](https://youtu.be/TB45qqp-OxM?t=730) Cold caches after a DR test, and the decision to do nothing

A weekend disaster-recovery test had restarted one replica for a security patch, shifting load to hardware with cold caches. The database kept slowly improving, execution plans were unchanged, and colleagues confirmed the signature: a first login took minutes, the next was instant. Exadata carries four cache layers (the speaker suspects the column cache but admits he cannot prove it), and years of powerful hardware had masked bad SQL. Switching back was pointless since the restarted primary was cold too, and reheating the cache under 600 requests per second of production load was judged reckless. The team chose to sit, wait, and observe with business colleagues validating recovery, the hardest decision to defend in front of management and the regulator.

### [20:04](https://youtu.be/TB45qqp-OxM?t=1204) The real defect: dedup-on-read across three tables

The read path merges three sources on every request: booked transactions (the 10-billion-row giant), an imported pending table that behaves like an audit log with every state change kept, and a real-time pending feed from another team exposed as a database view whose rows are never deleted. Each read merges the two pending sources, picks the newest state per transaction with `ROW_NUMBER()`, then anti-joins against booked rows to drop anything already settled, all to return about 40 transactions. One table holds 700 million rows, the main index alone is 700 GB, and the resulting select runs to roughly 10 KB. The core pattern on the slide:

```sql
-- reconstructed from speech and slide at 23:50
ROW_NUMBER() OVER (PARTITION BY id ORDER BY valid_from DESC) AS rn
...
WHERE rn = 1
  AND NOT EXISTS (SELECT 1 FROM booked_transactions b WHERE b.id = p.id)
```

Scale context: 20 million reads and 40 million writes per day, 11 TB then (14 TB now, heading toward 25 billion records), with small-business accounts holding up to a million transactions each explaining the 20-minute worst cases.

### [27:28](https://youtu.be/TB45qqp-OxM?t=1648) Tactical fix: restoring the 10-day query window

The incident had never struck before because the previous DR test ran a year earlier on fewer customers. A refactor three years prior had deleted a one-line date predicate limiting the scan to recent transactions, and restoring it as a parameter (10 days, chosen against settlement delays over weekends and holidays) removed the full scan. The execution plan looked identical, and the 10,000-account test environment could not reproduce cache-cold behavior at 20 million accounts, so the fix shipped on trust; the next DR test passed with everyone watching.

### [31:08](https://youtu.be/TB45qqp-OxM?t=1868) Strategic fix: write-side integrity and fewer tables

The long-term redesign moves deduplication from read to write: since the team's importers are the sole writers to their schema across 15 data sources (databases, Kafka, CSV and JSON files, APIs), each insert can check pending-against-booked once, adding about 20 ms nobody notices. Colleagues overruled the speaker's one-table dream in favor of two tables (pending and booked share only 5 of 20 attributes each), and a Kafka feed is on the way to absorb the never-deleted third source. Half the traffic already reads from the simplified path.

### [39:04](https://youtu.be/TB45qqp-OxM?t=2344) The exit: dual-write migration to Cloud PostgreSQL

Powerful hardware let "does it work?" win over "is it designed well?" for years, so the bank now plans off Exadata. CDC tools such as Debezium were rejected: they need sys-admin privileges Oracle's SLAs forbid on the managed box, and a mistake could touch the whole database rather than one schema. Instead, from 1 January 2027 the importers will dual-write Oracle and PostgreSQL simultaneously, with the 11 TB of history migrated by an in-house application on the team's own Kubernetes cluster (the only thing with access to both sides) over an estimated four months; a straight network copy was estimated at 30 uninterrupted days, and unofficial GitHub tools fail bank security review. Rollout goes through pilot users and percentage ramps (1, 2, 5, 10, 20, 100) with instant fallback to Oracle, all under a 99.998% availability budget of 10 minutes per year.

## Tools, libraries and specs

- Oracle Exadata and Oracle Database (managed box under vendor SLAs)
- PostgreSQL on cloud (migration target)
- Debezium (CDC option considered and rejected)
- Apache Kafka (feed planned for the third pending source)
- Dynatrace (APM that showed zero errors during the outage)
- Kubernetes (hosts the team's importers and planned migration job)

## Who should watch

Architects running large Oracle estates, teams planning an Oracle-to-PostgreSQL migration under regulatory constraints, and engineers who want a realistic incident-response playbook (first aid, tactical fix, strategic redesign). Skip it if you want an Exadata internals deep dive or a hands-on migration tutorial: caches are sketched, the SQL is anonymized, and partitioning is explicitly deferred to hallway conversation.

## Verdict

**7/10**: A bank-outage post-mortem with production experience and reasoned design trade-offs, limited by an unmeasured central fix and fragments as the only takeaway.

**Novelty 2/2**

- **+** [08:31](https://youtu.be/TB45qqp-OxM?t=511) The timeout first aid and the 15-minute production deploy come from the speaker's own incident, not from any guide.
- **+** [40:36](https://youtu.be/TB45qqp-OxM?t=2436) The CDC rejection rests on bank-specific constraints (sys-admin access, Oracle SLAs, schema-wide blast radius) no vendor tutorial covers.

**Demonstrated 1/2**

- **·** [23:18](https://youtu.be/TB45qqp-OxM?t=1398) An incident narrative with nothing to run live; the SQL and architecture appear as static slides rather than executed output.

**Measured 1/2**

- **+** [06:20](https://youtu.be/TB45qqp-OxM?t=380) Normal 20-40 ms responses are set against incident latencies of 100 ms to 20 minutes from production monitoring.
- **−** [08:31](https://youtu.be/TB45qqp-OxM?t=511) The 90% of users answered within 3 minutes is the speaker's own observation, with no method shown.
- **−** [29:34](https://youtu.be/TB45qqp-OxM?t=1774) The 10-day window fix shipped without a before/after measurement: the execution plan is identical and the 10,000-account test environment could not reproduce the cold cache.

**Depth 2/2**

- **+** [21:40](https://youtu.be/TB45qqp-OxM?t=1300) The three-source merge, newest-state selection and booked anti-join are explained step by step with row counts.
- **+** [40:36](https://youtu.be/TB45qqp-OxM?t=2436) CDC, vendor migration tools, network copy and in-house dual writes are weighed with reasons for each rejection.
- **−** [14:48](https://youtu.be/TB45qqp-OxM?t=888) Which of the four Exadata cache layers caused the slowdown is an admitted bet, though the cold-cache cause itself is shown at 17:27.

**Reusable 1/2**

- **+** [23:18](https://youtu.be/TB45qqp-OxM?t=1398) The anonymized SQL is shown on a slide and can be zoomed, specific enough to study the dedup pattern.
- **·** [42:42](https://youtu.be/TB45qqp-OxM?t=2562) The write-side dedup and the dual-write migration are described in speech, so the design has to be reconstructed from the description.
