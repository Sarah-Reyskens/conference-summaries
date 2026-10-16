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
reach: niche
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15

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

**7/10**: Three live end-to-end solves and a beginner-complete mental model of constraint solving; held back by estimated brute-force figures, no solver measurements and unpublished demo code.

**Reach niche**: Backend developers whose systems already assign people, vehicles or tasks under rules can apply the modeling, but most of the conference audience will not meet a Timefold-style planning problem within a year.

**Novelty 1/2**

- **+** [20:07](https://youtu.be/lsvVJaigNp8?t=1207) The hard-versus-soft walkthrough carries experience from earlier runs: food preference divides audiences most, and some customers treat it as a hard constraint.
- **+** [36:19](https://youtu.be/lsvVJaigNp8?t=2179) Hallway cases gathered that week, theater seating and golf tee times, extend the pattern beyond weddings.
- **−** The solver mechanics follow the project's documented getting-started path (Timefold docs: entity, variable, solve), and no production deployment story follows.

**Demonstrated 2/2**

- **+** [22:16](https://youtu.be/lsvVJaigNp8?t=1336) The seating chart fills in live and visibly refines as the solver keeps optimizing.
- **+** [29:32](https://youtu.be/lsvVJaigNp8?t=1772) The honeymoon solve renders a day-by-day itinerary of hotels and activities, including the kayak and yoga picks.
- **+** [33:11](https://youtu.be/lsvVJaigNp8?t=1991) Marking a beer out of stock strikes it through and triggers a visible "Planning..." replan of the remaining rounds.

**Measured 1/2**

- **+** [12:22](https://youtu.be/lsvVJaigNp8?t=742) Brute-force timings for 6, 8 and 10 guests (about 0.5 ms, 0.3 s, 27 s) come from the speaker's MacBook Pro.
- **−** [13:22](https://youtu.be/lsvVJaigNp8?t=802) The figures from 16 guests on (5 years, 580,000 years, 11 times the universe's age) are estimations, admitted only when asked.
- **−** [22:47](https://youtu.be/lsvVJaigNp8?t=1367) Solver quality is argued from the score analysis (only two tables mix sides), with no solve time or before/after number.

**Depth 2/2**

- **+** [11:51](https://youtu.be/lsvVJaigNp8?t=711) Factorial growth of seatings explains why enumeration fails and when to reach for a solver instead of hand-rolled search.
- **+** [15:27](https://youtu.be/lsvVJaigNp8?t=927) The entity, variable and solve annotations build the beginner mental model: the solver changes only what is marked changeable.
- **+** [18:03](https://youtu.be/lsvVJaigNp8?t=1083) Constraint filters run up to hundreds of thousands of times per solve, so they stay pure and never call a database.

**Reusable 1/2**

- **+** [31:07](https://youtu.be/lsvVJaigNp8?t=1867) The timefold.beer app is live and usable for planning a five-round Beer Central evening.
- **−** [26:56](https://youtu.be/lsvVJaigNp8?t=1616) The honeymoon domain code is walked through on screen, but no repository or sample URL is given for it or the seating app.
