---
title: The Importance of HITL to Avoid Chaos and EU Regulations for AI
talkId: "7017"
conference: devoxx-be-2026
speakers: [Juan Antonio Breña 🇪🇸🇪🇺]
track: Agentic Engineering & Tooling
sessionType: Tools-in-Action
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=t9e9FtHB-48
durationMin: 20
slides: https://jabrena.github.io/plinth/dvbe26/
verdict: 4
frames: 5
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# The Importance of HITL to Avoid Chaos and EU Regulations for AI
Juan Antonio Breña 🇪🇸🇪🇺 · Tools-in-Action · Agentic Engineering & Tooling
Slides: https://jabrena.github.io/plinth/dvbe26/

## TL;DR
AI coding agents accelerate change in brownfield systems where knowledge lives in engineers' heads, so pull requests need human reviewers who check consequences, not just green builds. The talk maps this human-in-the-loop discipline onto EU regulation (AI Act, GDPR, CRA, NIS2, DORA) and closes with a checklist of PR and pipeline practices teams can adopt immediately.

## Key takeaways
- A green pull request is not evidence of safety; the PR must document consequences (contracts, consumers, data, rollback plan) for a qualified reviewer to approve.
- Reviewers need standing to decide: route high-impact changes to accountable owners who can stop the merge and demand a tested rollback.
- Classify the deployed system before claiming AI Act compliance; using a coding agent does not by itself make the changed software a high-risk AI system.
- Label AI-generated PRs and add risk triggers for GDPR, CRA, NIS2 and DORA to the PR template so pipeline gates can produce audit evidence.
- Protect data changes with contract tests, the parallel-change pattern for database migrations, and checks that data removals propagate to downstream services.
- Give agents wider context with monorepos per subsystem and shared team skills instead of one repo per microservice.

## Notes

### [00:33](https://youtu.be/t9e9FtHB-48?t=33) Problem: small changes, fragmented context
Breña, an engineering manager at the London trading firm IG, frames the talk around senior engineers using AI agents on brownfield projects. The core problem: people rotate, knowledge stays in engineers' heads, and a small change that passes CI can still break production by altering a contract, a database, or a downstream consumer. He invokes Conway's law: fragmented team context plus agent-driven velocity lets independent teams change coupled parts of the system without coordination, and a cursorily reviewed PR becomes a cosmetic review.

### [04:41](https://youtu.be/t9e9FtHB-48?t=281) Improving the pull request
A good PR carries evidence, not just a green build. The PR should describe the blast radius, show it does not break consumers, match applicable regulation, and state how to roll back if the change fails. The reviewer must have the authority to accept or stop the change, and rollback capacity has to be designed and tested per change, since not every change is reversible.

### [07:49](https://youtu.be/t9e9FtHB-48?t=469) Governance: the EU regulation stack
The EU AI Act (Regulation (EU) 2024/1689) requires effective human oversight for applicable high-risk AI systems under Article 14; whether a mandatory human review applies depends on the classification of the deployed system and use case. The speaker walks through the adjacent regulations teams already face: GDPR data minimization and propagation of deletions (in force since 2018); the Cyber Resilience Act with checks for secrets, insecure defaults, SBOMs and unsafe deserialization; NIS2 incident reporting, third-party SDK review and access control (EU transposition deadline 17 Oct 2024); and DORA resilience, failover drills with recorded RTO/RPO, gated ICT changes and asset inventories (applicable from 2025). A DORA slide maps six Java-issue examples to fixes and articles (Art. 8, 9, 11, 24-25).

### [14:48](https://youtu.be/t9e9FtHB-48?t=888) What a team can do next Monday
The closing checklist: label agent-created PRs and record generated artifacts; add GDPR/CRA/NIS2/DORA risk triggers to the PR template; route high-impact changes to specialist owners; require explicit limits, rollback and monitoring evidence. On the engineering side: keep contract tests for REST and messaging, use the parallel-change pattern for database evolution, consider monorepos per subsystem so agents see the whole context, build common team skills, and evaluate whether squads use SDD (slide wording) or need training.

## Who should watch
Engineers and leads adding AI coding agents to enterprise Java estates who need a compact map from PR discipline to EU compliance obligations. Skip it if you want AI Act legal detail, measured results, or a demo: the talk stays at the level of practices and regulation pointers.

## Verdict
**4/10**: PR review discipline mapped onto five EU regulations through the speaker's own Java examples, but nothing is shown running and no deployed system is classified.

**Novelty 1/2**

- **+** [03:07](https://youtu.be/t9e9FtHB-48?t=187) The speaker ties a small change to a contract or database (deck: renaming `customerId` to `clientId` across six consumers) to Conway's-law fragmentation under agent-driven velocity, his own framing of why a green PR can still be wrong.
- **+** [13:39](https://youtu.be/t9e9FtHB-48?t=819) Each regulation comes with Java issue tables that map a risk to a fix and an article hook (the DORA slide on screen: failover drills recording RTO and RPO, gated ICT change pipeline, inventory from the SBOM), the speaker's own translation of the obligations.
- **−** [02:36](https://youtu.be/t9e9FtHB-48?t=156) The opening failure is a hypothetical ("I am not inventing this particular case") rather than an incident from the speaker's teams, and no later segment adds one.

**Demonstrated 0/2**

- **−** [14:48](https://youtu.be/t9e9FtHB-48?t=888) Pipeline gates, AI-PR labels and rollback evidence are described in speech and on slides, with nothing shown running.
- **−** [10:56](https://youtu.be/t9e9FtHB-48?t=656) The CRA checks (secrets, insecure defaults, SBOM, unsafe deserialization) appear as table rows and speech, with no repository or scan output shown.

**Measured 1/2**

- **·** [03:37](https://youtu.be/t9e9FtHB-48?t=217) No quantitative claim is made: the agent-velocity warning is qualitative, and the regulation dates state applicability rather than backing a measurement.

**Depth 1/2**

- **+** [06:15](https://youtu.be/t9e9FtHB-48?t=375) The reviewer is chosen by the change's risk and needs the authority to stop and roll back (deck routing: API, event and schema changes to domain owners, auth and secrets to security).
- **+** [16:56](https://youtu.be/t9e9FtHB-48?t=1016) Parallel change is explained by its reason: the service keeps the old shape while the database change is prepared, so production sees no breaking change.
- **−** [07:49](https://youtu.be/t9e9FtHB-48?t=469) AI Act oversight is said to depend on the system's classification, but no system is classified as an example.

**Reusable 1/2**

- **+** [14:16](https://youtu.be/t9e9FtHB-48?t=856) The closing practices are listed to reconstruct: AI-PR labels, PR-template risk triggers, contract tests, parallel change, monorepos, shared skills.
- **−** [19:03](https://youtu.be/t9e9FtHB-48?t=1143) The only repository linked, Plinth, covers none of the HITL or regulation content, and no PR template, gate configuration or checklist for it is published.
