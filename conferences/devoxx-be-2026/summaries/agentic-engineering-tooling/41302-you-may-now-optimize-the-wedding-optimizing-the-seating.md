---
title: '"You May Now Optimize the Wedding": Optimizing the Seating, Bachelor Party, and Honeymoon with Constraint AI'
talkId: "41302"
conference: devoxx-be-2026
speakers: [Geoffrey De Smet, Tom Cools]
track: Agentic Engineering & Tooling
sessionType: Lunch Talk
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=lsvVJaigNp8
durationMin: 37
slides: null
verdict: 7
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# "You May Now Optimize the Wedding": Optimizing the Seating, Bachelor Party, and Honeymoon with Constraint AI

Geoffrey De Smet, Tom Cools · Lunch Talk · Agentic Engineering & Tooling

## TL;DR

Two Timefold engineers solve three wedding problems (seating, honeymoon, pub crawl) live with the Timefold constraint solver. Brute force and vibe-coded algorithms fail on combinatorial planning: model with annotations and constraints, then let a solver search.

## Key takeaways

- Seating 20 guests has 20! (~2.4 × 10^18) arrangements; brute force takes 27 s for 10 and ~1 h for 12.
- Annotate the changeable class `@PlanningEntity`, the assignable field `@PlanningVariable`, call `solver.solve()`; the rest is constraints.
- Hard constraints cover physical reality and non-negotiables, soft ones preferences; which is which depends on the customer.
- Constraint filters run hundreds of thousands of times per solve: keep them pure, never call a database from them.
- Itineraries with skippable candidates use a planning list variable with unassigned elements allowed, supporting polymorphic types.

## Notes

### [06:13](https://youtu.be/lsvVJaigNp8?t=373) Requirements and why brute force fails

The Java fix for a vibe-coded wedding app covers seating, honeymoon, and pub crawl; the talk covers only the solver backend. Guests go to seats under audience-gathered rules: family alignment, couples, fixed bride/groom seats, food preferences, toilet and dance-floor distance, wheelchair access, political alignment. Exhaustive search scales factorially (10 guests 27 s, 20 guests ~580,000 years): do not hand-roll search any more than you would hand-roll a web server.

### [14:24](https://youtu.be/lsvVJaigNp8?t=864) Timefold: entity, variable, solve, constrain

Timefold Solver is an open-source Java assignment library: `@PlanningEntity`, `@PlanningVariable` on the changeable field, inject the solver, call `solve`. Constraints are plain Java: filter offenders, penalize each match with a readable name for score explanation. Anything unstated is allowed, so physical reality (one guest per seat) must be encoded. An audience vote classifies each rule: accessibility hard, family and political alignment soft, food preference split (modeled soft), pairing split four ways.

### [22:16](https://youtu.be/lsvVJaigNp8?t=1336) Live solves: seating, honeymoon, pub crawl

The seating chart fills in and refines live; only two tables mix bride and groom sides. For comedy, Cools flips the political constraint from `penalize` to `reward` and the hot-reloaded replan maximizes political friction. The Italy road trip uses a `@PlanningListVariable` with unassigned visits allowed and polymorphic hotel/activity types. The third app, live at timefold.beer, plans a five-round Beer Central evening; marking a beer out of stock replans the rest instantly.

### [34:12](https://youtu.be/lsvVJaigNp8?t=2052) Close: enterprise APIs and agentic webinar

Ready-made APIs cover field-service routing, shift scheduling, and pickup-and-delivery; a webinar will bridge deterministic optimization with gen-AI agents.

## Tools, libraries and specs

- Timefold Solver (open-source Java constraint solver; Quarkus/Spring integration)
- timefold.beer (live pub-crawl planning demo)
- Quarkus (hot reload in the evil-constraint demo)

## Who should watch

Developers curious about constraint solving who learn best from live code, and anyone wondering whether a solver fits their scheduling problem. Skip if you already build on Timefold or OptaPlanner and want internals or tuning.

## Verdict

**7/10**: Three live end-to-end solves and a clear beginner mental model of constraint solving; held back by unmeasured solver claims, no new results and no published code.

**Novelty 1/2**

- **+** [05:43](https://youtu.be/lsvVJaigNp8?t=343) The three apps (seating, honeymoon, pub crawl) were built by the speakers for the talk, with the backend as the focus.
- **+** [20:07](https://youtu.be/lsvVJaigNp8?t=1207) The hard-versus-soft walkthrough carries the speakers' experience from earlier runs: food preference is the rule that divides audiences most, and some customers treat it as hard.
- **−** [22:47](https://youtu.be/lsvVJaigNp8?t=1367) No new results, solver benchmarks or production cases appear, and the speaker notes that Claude gives a decent answer from the same requirement list.

**Demonstrated 2/2**

- **+** [22:16](https://youtu.be/lsvVJaigNp8?t=1336) The seating chart fills in live and visibly refines as the solver keeps optimizing, with the score breakdown shown.
- **+** [29:32](https://youtu.be/lsvVJaigNp8?t=1772) The honeymoon solve produces a visible day-by-day itinerary of hotels and activities in the running app.
- **+** [33:11](https://youtu.be/lsvVJaigNp8?t=1991) Marking a beer out of stock shows the item struck through and a "Planning..." replan of the remaining rounds.

**Measured 1/2**

- **+** [12:22](https://youtu.be/lsvVJaigNp8?t=742) Brute-force timings for 6, 8 and 10 guests (about 0.5 ms, 0.3 s, 27 s) come from the speaker's MacBook Pro.
- **−** [13:22](https://youtu.be/lsvVJaigNp8?t=802) The brute-force method is not shown, and the figures from 16 guests on (5 years, 580,000 years, 11 times the universe's age) are estimations, admitted only when asked.
- **−** [22:16](https://youtu.be/lsvVJaigNp8?t=1336) No solve time or plan-quality number is given for Timefold, only "pretty quickly".

**Depth 2/2**

- **+** [11:51](https://youtu.be/lsvVJaigNp8?t=711) The factorial growth of seatings (20! ≈ 2.4 × 10^18) explains why search beats enumeration and why to reach for a solver instead of hand-rolled code.
- **+** [19:05](https://youtu.be/lsvVJaigNp8?t=1145) The hard-versus-soft exercise builds a decision model for classifying constraints, including customer-dependent answers.
- **+** [18:03](https://youtu.be/lsvVJaigNp8?t=1083) The warning that filters run up to hundreds of thousands of times per solve gives a performance mental model for writing constraints.

**Reusable 1/2**

- **+** [31:07](https://youtu.be/lsvVJaigNp8?t=1867) The timefold.beer app is live and usable, covering the pub-crawl demo end to end.
- **−** [23:50](https://youtu.be/lsvVJaigNp8?t=1430) The seating and honeymoon code appears only on screen; no repository URL is given for it.
