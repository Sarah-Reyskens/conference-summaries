---
title: "Pragmatic multi-cloud architecture: designing for resilience and portability beyond the hype"
talkId: "4097"
conference: devoxx-be-2026
speakers: [Alexandre Touret]
track: Cloud Native, Data & Infrastructure
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=mOmuF5fDiUM
durationMin: 35
slides: https://speakerdeck.com/alexandretouret/dvxpl26-pragmatic-multi-cloud-architecture-designing-for-resilience-and-portability-beyond-the-hype
slidesNote: from Devoxx Poland 2026
verdict: 6
reach: segment
frames: 7
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Pragmatic multi-cloud architecture: designing for resilience and portability beyond the hype

Alexandre Touret · Conference · Cloud Native, Data & Infrastructure

Slides: https://speakerdeck.com/alexandretouret/dvxpl26-pragmatic-multi-cloud-architecture-designing-for-resilience-and-portability-beyond-the-hype

## TL;DR

Touret argues multi-cloud only pays off with deliberate design: pick a strategy up front, keep one bounded context per provider, and budget for latency, egress and SLA dilution from day one. The talk walks a fleet-tracking example across AWS and GCP through NFRs, compliance, security, data sync and FinOps, ending with a six-question architecture decision checklist.

## Key takeaways

- Host each bounded context with a single cloud provider and keep contexts loosely coupled; treat every cross-cloud call as a remote call between two different systems.
- Challenge SLAs against the weakest link: a 99% app server on a 95% platform yields 95% end to end, so write separate NFRs for cross-cloud transactions.
- Prefer internet over dedicated VPN for cross-cloud links and co-locate landing zones in one region; at 100 TPS the speaker's GCP pricing estimate came out near 20 euros/month versus 1600 euros for dedicated connectivity.
- Validate OIDC tokens with local signature checks plus short-lived tokens instead of per-request introspection calls, which bottlenecked one of his projects.
- Never run bidirectional cache-to-database sync across clouds; a single-writer cache with managed eviction avoids split-brain on failure.
- Hide fragmentation behind one global API gateway with unified error handling, and merge per-cloud metrics into a single observability dashboard.

## Notes

### [00:31](https://youtu.be/mOmuF5fDiUM?t=31) What multi-cloud is and is not

The deck cites 76% of organizations on hybrid or public cloud but only 21% with a multi-cloud strategy, and 81% of multi-cloud users naming complexity their top operational challenge. Multi-cloud is not different teams on different clouds, and not hybrid cloud: it means choosing best-of-breed services per need behind one platform, for redundancy, vendor independence, or compliance.

### [03:09](https://youtu.be/mOmuF5fDiUM?t=189) Why: motives and hard realities

Motives are avoiding lock-in, best-of-breed services, and compliance. Against that: teams must be trained per provider, IaC maintained per provider, and Kubernetes alone does not deliver agnosticism since provider annotations and pod monitoring leak in. Users want one unified service, not a multi-cloud platform. Rather than avoiding all provider-specific features (and missing BigQuery or Spanner), assess reversibility cost and switching risk per choice.

### [06:13](https://youtu.be/mOmuF5fDiUM?t=373) Designing from scratch: strategy and bounded contexts

The worked example is a real-time fleet-tracking platform: vehicle tracking, analytics and reporting, predictive maintenance, customer-facing apps, and payments. Strategy first: best-of-breed managed services, partnerships where needed, no reinvented wheels. The methodology iterates over bounded contexts, business processes, solution choice, NFRs, compliance, security, data ownership, performance, and lock-in. Rule of thumb: one bounded context per provider, loosely coupled. The resulting split puts tracking on GCP IoT Core, analytics on BigQuery, ML on Vertex AI, and the app server plus payments on AWS (EC2/Beanstalk).

### [10:54](https://youtu.be/mOmuF5fDiUM?t=654) Cross-cloud transactions and the API facade

A BPMN diagram with one lane per provider surfaces every cross-cloud transaction, each of which inherits the fallacies of distributed computing: reliability, latency, security, and transfer cost. The C4 diagram shows the AWS app server calling BigQuery over HTTP directly, which couples the two sides on every schema or API change; an API facade in front of BigQuery restores the boundary. Latency mitigations named: timeouts, retries with exponential backoff, circuit breakers, and graceful degradation.

### [13:32](https://youtu.be/mOmuF5fDiUM?t=812) NFRs and the SLA trap

Availability multiplies down to the weakest dependency, so create lower-expectation NFRs for cross-cloud paths, consider caching above a few hundred TPS, and challenge NFRs against the design in both directions. On one project Touret talked a client down from an irrelevant 99.99% availability target, which cut cost.

### [15:36](https://youtu.be/mOmuF5fDiUM?t=936) Compliance as an isolation opportunity

European regimes named include HDS for health data, OIV/KRITIS for critical infrastructure, and PCI DSS for payments. Isolating the payment environment for PCI DSS simplifies audit, delivery, and training scope, so never mix sensitive and non-sensitive workloads.

### [16:37](https://youtu.be/mOmuF5fDiUM?t=997) Security: one SSO and token validation

Technical users stay per-platform, but end users get a single SSO, federating existing IdPs through Keycloak when needed. The RBAC example runs Keycloak on AWS with policies on both the app server and the GCP analytics API. For token validation, per-request introspection calls revoke instantly but bottleneck; local signature validation with short-lived tokens scales, and the speaker's team switched to it after hitting the bottleneck in production.

### [20:48](https://youtu.be/mOmuF5fDiUM?t=1248) Data ownership and synchronization

Each data type needs a declared repository: vehicle data in tracking, user data in SSO or the client app. Sync options are synchronous APIs (simple, with local cache and webhooks possible, but chatty and costly) versus async event streaming over CDC/Kafka (complex, but avoids loss and network coupling). Bidirectional sync is rejected outright for its split-brain risk; user identities reconcile on email. PII can live per provider but needs end-to-end lifecycle visibility through observability.

### [24:58](https://youtu.be/mOmuF5fDiUM?t=1498) Performance and FinOps

For a sub-100 ms API, the sum of per-hop latencies must be measured with observability and benchmarks, not assumed at design time. Guidance: co-locate regions (Paris or Brussels), check SLOs, minimize chattiness, prefer internet over dedicated links, track egress. The worked estimate (100 TPS, 0.5 KB request, 1 KB response, about 260 GB/month) prices near 20 euros on internet versus about 1600 euros on a dedicated channel via the GCP calculator.

### [27:37](https://youtu.be/mOmuF5fDiUM?t=1657) Vendor lock-in assessment

For each managed service, name the migration alternative and its cost: GCP IoT Core to an MQTT broker (HiveMQ Cloud is named as one option) is feasible, BigQuery or Vertex AI to another cloud means rebuilding from scratch, and a plain EC2 VM moves easily. Self-hosting (his team packaged Artemis on Kubernetes from experience) depends on team skills and platform goals.

### [30:11](https://youtu.be/mOmuF5fDiUM?t=1811) The customer perspective

Two public APIs mean poor UX, so front everything with one global API gateway on either provider, unifying error handling, plus backend-for-frontend for web and mobile. Observability merges per-cloud metrics on a cadence (every 2 minutes in the example) into global dashboards and alerts on one provider.

### [31:43](https://youtu.be/mOmuF5fDiUM?t=1903) Pitfalls, checklist, and canvas

Top pitfalls: over-coupling services across clouds with bidirectional sync, ignoring network cost up front, bolting compliance on late, and forgetting the customer during design. The closing checklist asks which workloads stay together, where compliance friction lies, what the network budget is, what NFRs each workload gets, what the sync strategy is (and whether one is needed at all), and how customers get one interface. The canvas orders the work: strategy, bounded contexts, target solutions, NFR challenge, cost and SLO check, then unified API and observability.

## Tools, libraries and specs

- GCP IoT Core, BigQuery, Vertex AI, AWS EC2 / Elastic Beanstalk (example stack split)
- Keycloak (SSO federation, Advanced Claim To Group role mapping)
- OIDC (single SSO, local signature validation vs introspection)
- Kafka / CDC event streaming (async cross-cloud sync)
- Apache Artemis on Kubernetes (self-hosted MQTT alternative)
- GCP pricing calculator (egress cost estimate)
- BPMN (cross-cloud transaction mapping), C4 diagrams (platform views)
- PCI DSS, HDS, OIV/KRITIS (compliance regimes)

## Who should watch

Architects and senior engineers starting or reviewing a multi-cloud design benefit most, especially from the checklist framing. Teams already running multi-cloud with settled IAM, sync, and FinOps practices can skip it; viewers wanting implementation detail on any single area (Keycloak setup, Kafka topologies, gateway config) need dedicated sessions instead.

## Verdict

**6/10**: A multi-cloud design framework argued through reasoned trade-offs and a few project anecdotes, held back by calculator-only numbers, no demo and no published artifact.

**Reach segment**: Architects and tech leads planning or reviewing a design that spans cloud providers can apply the checklist and trade-offs; teams on a single-cloud backend will not use the cross-cloud material within the next year.

**Novelty 1/2**

- **+** [15:04](https://youtu.be/mOmuF5fDiUM?t=904) A client was talked down from an irrelevant and expensive 99.99% availability target, which shows the NFR challenge applied in a real engagement.
- **+** [19:47](https://youtu.be/mOmuF5fDiUM?t=1187) The team hit a token-introspection bottleneck in an existing project and switched to local signature validation with short-lived tokens.
- **+** [10:24](https://youtu.be/mOmuF5fDiUM?t=624) A recent project accepted a direct channel for externally received data because it only served BI and stayed off the transactional path.

**Demonstrated 1/2**

- **·** [11:26](https://youtu.be/mOmuF5fDiUM?t=686) An architecture strategy talk with diagrams and no demo slot has nothing to run, so this criterion does not apply.

**Measured 1/2**

- **+** [26:29](https://youtu.be/mOmuF5fDiUM?t=1589) Internet connectivity is priced from stated inputs (100 TPS, 0.5 KB request, 1 KB response, about 260 GB/month) with the GCP calculator at about 20 euros.
- **−** [27:02](https://youtu.be/mOmuF5fDiUM?t=1622) The 1600 euro dedicated-channel figure comes with no link type or capacity, covers GCP only, and is a calculator projection whose prices "change daily", not observed spend.
- **−** [14:33](https://youtu.be/mOmuF5fDiUM?t=873) The advice to consider caching above 200 to 400 transactions per second gives a threshold with no baseline, source or method.

**Depth 2/2**

- **+** [22:19](https://youtu.be/mOmuF5fDiUM?t=1339) Sync versus async data replication is weighed explicitly: simple but chatty and costly against complex but lossless, with hybrid bidirectional sync rejected for its split-brain risk.
- **+** [28:38](https://youtu.be/mOmuF5fDiUM?t=1718) Each managed service gets a migration alternative with a cost judgment, from rebuilding BigQuery pipelines to moving a plain VM with ease.
- **+** [12:31](https://youtu.be/mOmuF5fDiUM?t=751) The AWS app server calling BigQuery over HTTP stays coupled on every schema change, and the API facade restores the boundary so BigQuery can evolve without touching the app server.

**Reusable 1/2**

- **+** [32:15](https://youtu.be/mOmuF5fDiUM?t=1935) The six-question checklist orders the design questions from workload placement to a unified customer interface, giving practices to reconstruct.
- **·** [33:16](https://youtu.be/mOmuF5fDiUM?t=1996) The canvas is walked through on screen, but the talk points to no repository, sample project or standalone checklist artifact.
