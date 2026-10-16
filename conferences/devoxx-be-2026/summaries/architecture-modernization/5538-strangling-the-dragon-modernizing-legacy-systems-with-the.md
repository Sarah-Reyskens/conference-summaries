---
title: "Strangling the dragon: modernizing legacy systems with the Strangler Fig pattern"
talkId: "5538"
conference: devoxx-be-2026
speakers: [Daniel Raniz Raneland]
track: Architecture & Modernization
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=AmL_OCs5F4E
durationMin: 35
slides: https://raniz.se/decks/2026/devoxx-be-26-strangling-the-dragon.pdf
verdict: 5
reach: broad
frames: 8
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Strangling the dragon: modernizing legacy systems with the Strangler Fig pattern

Daniel Raniz Raneland · Conference · Architecture & Modernization

Slides: https://raniz.se/decks/2026/devoxx-be-26-strangling-the-dragon.pdf

## TL;DR

Full rewrites of legacy systems usually fail, so Raneland argues for the Strangler Fig pattern: break out one small part at a time until the old system is replaced or reduced to its good parts. He pairs the pattern with three supports: TDD as a safety harness, Domain-Driven Design for the target architecture, and the Inverse Conway Manoeuvre to align teams with it.

## Key takeaways

- Do not rewrite: stale documentation, the second system effect, forgotten complexity, resurrected bugs, and a moving target make big-bang rewrites fail.
- Strangle instead: identify one small part, break it out or replace it, repeat until the legacy system withers or becomes a supported core.
- Fixate current behavior with tests before touching legacy code, then test-drive the change and keep old and new paths switchable behind a feature flag.
- Build the target architecture first with DDD context mapping (event storming with domain experts), then migrate toward it one bounded context at a time.
- Restructure teams to match the target context boundaries (Inverse Conway Manoeuvre), one bounded context per team, but do not move people until a first small breakout proves the direction.
- Keep the second system effect contained: expect the first breakout modules to be wrong, then refactor them once later modules teach you the real shape.

## Notes

### [01:35](https://youtu.be/AmL_OCs5F4E?t=95) Why most rewrites fail

The impulse with a 10-to-30-year-old codebase is to throw it in a dumpster, light the dumpster on fire, and start over. Raneland lists why that fails: requirements documentation is stale, the second system effect makes you overcompensate for every old flaw (he cites house-building: live in the third house, not the second), complexity is underestimated because old pain is forgotten, old edge cases and bugs resurface, and nobody pauses feature work for years, so the rewrite chases a moving target until it is cancelled. One subtle dilemma: existing bugs must either be fixed (so it is no longer a reimplementation) or consciously reimplemented.

### [06:17](https://youtu.be/AmL_OCs5F4E?t=377) The Strangler Fig pattern

The name comes from Martin Fowler, after the tree whose seeds germinate in another tree's branches, grow down around it, and either strangle the host into a hollow shell or support it against storms. Both outcomes map to software: fully replace the old system, or keep its good parts propped up by new ones. The pattern itself is three steps: identify one small part, break it out or replace it, repeat. The hard part is finding the first small part in a monolith, which the rest of the talk addresses.

### [08:20](https://youtu.be/AmL_OCs5F4E?t=500) Story: strangling an image service, 2016–2019

At a startup, Raneland inherited a prototype image service written in JavaScript that nobody on the team enjoyed. Adding albums created too much cross-talk between services, so in 2016 the team added a Job Service and an Album Service, then moved functionality out of the image service piece by piece, typically when a feature needed changing anyway. The last piece moved in 2019, the empty cluster was decommissioned, and the team celebrated with champagne. The moral for large systems: the same loop works, but needs TDD, DDD, and Conway's law as backup, which he calls the vanguard of the pattern.

### [11:28](https://youtu.be/AmL_OCs5F4E?t=688) TDD as the safety harness

TDD supplies the safety net: write a test, see it fail, make the smallest change that passes, refactor, repeat. In legacy code you cannot test-drive what exists, so you test-drive the change: first add tests that fixate current behavior (breaking the code deliberately to prove each test fails), then change tests and code in the normal loop. Applied to strangling: test the boundary you will cut (network API, interfaces, even hardcoded classes, introducing a seam where none exists), refactor the boundary open, test-drive the new module reusing the old tests, switch paths behind a feature flag with gradual rollout, then remove the old path and the flag. He warns with Knight Capital's 2012 incident, where a stale flag in a bad deployment lost $460 million in 45 minutes.

### [17:16](https://youtu.be/AmL_OCs5F4E?t=1036) DDD and the dragon business context map

DDD provides the destination: model software to match the domain as its experts describe it. The running example maps a dragon business (princess kidnapping, combat operations, treasure hoarding, ransom management, all interacting with a kingdom) into subdomains and event flows, built through event storming with sticky notes on a wall. Migration then starts from the spaghetti monolith by extracting one tiny feature first, the initial ransom demand, deployed to production for real, and grows from there. The new modules need not be microservices; a modular monolith or self-contained systems fit the same map.

### [22:28](https://youtu.be/AmL_OCs5F4E?t=1348) Conway's law and the Inverse Conway Manoeuvre

Conway's law constrains organizations to produce designs mirroring their communication structures: frontend, finance, combat, and database teams will produce a matching SPA, services, and central database, and will drift back to it if forced otherwise. The fix is the Inverse Conway Manoeuvre: restructure teams to follow the context-map boundaries so the desired architecture emerges naturally. Rules: one bounded context belongs to exactly one team, while a team may own several small contexts. Team Topologies and Unfix are named as inspiration for the team design.

### [25:02](https://youtu.be/AmL_OCs5F4E?t=1502) Advantages, pitfalls, and how to start

Advantages over rewrite: small incremental risk, old mistakes stay visible as reference, the system keeps shipping features, modernization can ride on feature work or new business opportunities, the second system effect stays limited to early breakouts, and the effort can pause at any time since a half-modernized system still works. Pitfalls: overambition (think big, work in baby steps), starting too many parallel tracks before the direction is proven, under-budgeting the overhead, and working in isolation instead of trunk-based with feature flags. The startup sequence: map the context, design (but do not execute) the team changes, pick one small trailblazer project with a few people, move teams over gradually once it succeeds, keep re-evaluating the target model, and celebrate milestones. In Q&A he adds that management buy-in is essential (sell faster features and stability, since initiatives usually start at the top) and that juniors should be confined to one side of the old/new split rather than both.

## Tools, libraries and specs

- EventStorming: wall-and-sticky-notes technique for building the domain context map with experts.
- Team Topologies: framework for designing team structures around the target architecture.
- Unfix: second team-design framework; pick ideas from both.

## Who should watch

Developers and architects who own an aging system and need a plan to modernize it without stopping feature work. Readers who already practice strangler-style migrations with DDD and team restructuring will find the framing familiar and can skip to the Q&A and pitfalls.

## Verdict

**5/10**: A migration playbook combining TDD seams, DDD context mapping and team alignment, grounded in a production example but leaving data coexistence unexplained and the practices to reconstruct.

**Reach broad**: Developers, tech leads and architects maintaining business applications can use incremental modernization, tested boundaries and team alignment in their own systems.

**Novelty 1/2**

- **+** [08:20](https://youtu.be/AmL_OCs5F4E?t=500) The 2016–2019 migration of a prototype image service into job and album services, ending with the empty cluster decommissioned, grounds the pattern in the speaker’s own production experience.
- **+** [11:28](https://youtu.be/AmL_OCs5F4E?t=688) TDD, DDD context mapping and the Inverse Conway Manoeuvre are brought together as one migration playbook rather than presented as separate topics.

**Demonstrated 1/2**

- **·** A strategy talk argued through diagrams and architecture sketches has nothing runnable to show, so there is no demo to pass or fail.

**Measured 1/2**

- **·** [15:38](https://youtu.be/AmL_OCs5F4E?t=938) The talk makes no quantitative claim for the method; the Knight Capital $460M-in-45-minutes figure is a cited cautionary incident about stale feature flags, not evidence for the pattern.

**Depth 1/2**

- **+** [02:38](https://youtu.be/AmL_OCs5F4E?t=158) Six failure modes of rewrites are worked through, down to the dilemma of whether existing bugs get fixed or consciously reimplemented.
- **+** [13:02](https://youtu.be/AmL_OCs5F4E?t=782) Legacy TDD is made specific: fixate current behavior first and break the code to prove each test fails, then test-drive the change.
- **−** [20:54](https://youtu.be/AmL_OCs5F4E?t=1254) The extraction sequence reaches production deployment without explaining how data or transactions work while old and new run side by side.

**Reusable 1/2**

- **+** [14:37](https://youtu.be/AmL_OCs5F4E?t=877) The migration sequence describes opening a tested seam, reusing tests for the replacement and switching paths behind a feature flag.
- **·** [32:18](https://youtu.be/AmL_OCs5F4E?t=1938) The closing resource pointer offers slides but no repository or sample project reproducing the migration procedure, so the practices must be reconstructed.
