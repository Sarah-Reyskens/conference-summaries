---
title: The pizza party of the future 🍕 software teams and product value in the age of coding agents
talkId: "8164"
conference: devoxx-be-2026
speakers: [Katie Clark, Simon Rohrer]
track: People, Practices & Career
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=Tc2RFLa0ip8
durationMin: 51
slides: null
verdict: 6
frames: 8
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# The pizza party of the future 🍕 software teams and product value in the age of coding agents

Katie Clark, Simon Rohrer · Conference · People, Practices & Career

## TL;DR

Clark and Rohrer argue that coding agents change what developers do without removing developers, teams, or the need to talk: the new bottlenecks sit around value (what to build) and trust (whether it works). They reach that thesis by walking through past predictions of the programmer's demise, Taylorist versus Druckerist management, and where spec-driven "dark factories" actually fit. The talk closes with context-dependent team sizing: anything from two people prototyping to a stable five-plus on business-critical systems.

## Key takeaways

- Every generation of tooling, from Fortran to low-code platforms, was predicted to end programming; each one instead moved the human contribution up a level, and agents look like the same pattern.
- Developer roles are splitting toward expert generalist builders (domain plus architecture, deciding what to build) and enablers or harness engineers (guardrails, testing, automation around agents).
- Treat the machine like a machine and people like people: juniors are learners to invest in, not transactional output to replace with agents.
- Spec-as-source with lights-out automation works only for local, conventional change; novel or systemic change needs humans reviewing code and tests and judging results.
- Taylorism applied to the work (linearize and automate the repeatable parts) is productive; Taylorism applied to the workers (deskilled executors of specs) repeats the failures of offshoring-by-spec.
- Team size follows context, not a universal rule: two slices for prototyping, about five as a minimum for a stable business-critical team, a single pizza for internal tools.

## Notes

### [01:05](https://youtu.be/Tc2RFLa0ip8?t=65) Three pins to knock down

The framing device is a bowling alley: three claims about the agent era serve as pins. Pin one says developers are no longer needed at all. Pin two says developers should stop talking and thinking and just chat with agents. Pin three says a perfect spec handed to agents finishes the job. A QR code early on points to Substack articles with full-length quotes and sources, described as still work in progress.

### [05:49](https://youtu.be/Tc2RFLa0ip8?t=349) Every tool was supposed to kill programming

A meme traces "the end of programmers" predictions from Fortran (1956) through SQL, Visual Basic, and low-code platforms (2014). The counter-reading: these tools aimed at collaboration, not replacement. COBOL co-inventor Jean Sammet expected novices to write it so business people could read along; object orientation put developers in users' vocabulary; BDD was always about conversations on behavior rather than Gherkin syntax.

### [08:23](https://youtu.be/Tc2RFLa0ip8?t=503) Waterfall was a myth, agile became a process

The talk recaps the SAGE project (1956), the NATO "software factory" (1968), Royce's warning against strict sequence, and the 1983 write-up admitting SAGE was iterative all along. Agile predates the manifesto too (Tom Gilb's iterative work since the 1960s), then hardened from conversations into tooling used to manage developers. Cited critics argue the result is feature factories: Gilb rejects "working software" as the progress measure in favor of value, alongside Melissa Perri's build trap and Jeff Gothelf on agile having no brain for which features deserve building.

### [12:32](https://youtu.be/Tc2RFLa0ip8?t=752) Who counts as a developer

By 1960 more than one in four programmers were women, when the work was low-status; a 1966 psychology paper then sketched the antisocial puzzle-lover stereotype the industry still recognizes. The 10x-developer myth, traced to Sackman et al. (1968), gets a pointer to Laurent Bossavit's The Leprechauns of Software Engineering for the full demolition. Offshoring from around 1989 repeated the "spec 100% right, then hand off" fallacy by classifying coding as tedious work to throw away.

### [20:50](https://youtu.be/Tc2RFLa0ip8?t=1250) Taylor versus Drucker

The talk's central lens contrasts Frederick Taylor's scientific management (1911), with its "oxlike" executor of assigned tasks, against Peter Drucker's knowledge worker (1959), who knows more than their boss about the work and needs a self-managing team. Dark Scrum and SAFe land on the Taylorist side; XP on the Druckerist one. Sociotechnical systems design extends the point: Emery's first design principle (deskilled people, managed tasks) against the second (T-shaped people, team holds the whole task), plus Cal Pava's observation that office work is messy and nonlinear, so progress comes from conversations among different people.

### [26:03](https://youtu.be/Tc2RFLa0ip8?t=1563) The developer role shifts

Anthropic's CEO predicts coding goes first, then software engineering; the speakers counter with Gergely Orosz's reporting that Anthropic's own product builders disagree, and Kent Beck's view that this misunderstands the human core of the job. Swedish miners relocated to offices to joystick-operate underground robots illustrate how roles shift while identities lag (the hi-vis jacket stays on). Adam Tornhill's two emerging paths, expert generalist builder and enabler, structure the rest of the section, alongside reports of apathy and burnout in all-in factory-style agent adoption.

### [30:46](https://youtu.be/Tc2RFLa0ip8?t=1846) Jobs to be done, from syntax to value

Borrowing Theodore Levitt's drill-versus-hole ladder, the talk stacks developer value as syntax knower, systems engineer, problem solver, and value optimizer, urging the audience to locate themselves and their organization on it. Developers confined to typing experience AI as a threat; developers asked to solve problems experience it as leverage. John Cutler's "single-player mode" (one person, fifty agent windows, custom orchestrator) is the anti-pattern; Cat Hicks's cross-functional team of T-shaped people learning together is the goal.

### [34:28](https://youtu.be/Tc2RFLa0ip8?t=2068) Juniors and blurred roles

Charity Majors opens the juniors segment: nobody knows how to quantify any engineer's value, juniors bring fresh ideas, hire them. Daniel Terhorst-North adds the polite version: treat machines like machines and people like people. Anthropic's Boris Cherny sees classic specialist roles dissolving into prototypers, builders, growers, sweepers, and maintainers, echoing Kent Beck's explore-expand-extract and Wardley pioneers, settlers, and town planners.

### [37:34](https://youtu.be/Tc2RFLa0ip8?t=2254) Dark factories, dim factories, and where specs work

The "dark factory" metaphor comes from a January 2026 article; in practice most teams get a dim or gray factory where the lights go back up for review. Dex Horthy reportedly built a lights-off software factory and shut it down after a single primary-key defect threaded the whole codebase beyond what agents or humans could fix. The talk's own 2x2 matrix maps change scope (local versus systemic) against familiarity (conventional versus novel): only local-conventional change earns spec-as-source with tests judging results, while the other three quadrants need people judging, boundaries checked, and progressively more feedback. Supporting theory includes Jack Reeves on programming-as-design, Peter Naur on theory building, and Sam Newman's two sources of truth: the programmer's head and production.

### [45:55](https://youtu.be/Tc2RFLa0ip8?t=2755) How much pizza to order

Three data points anchor the sizing discussion: an unnamed practitioner recommends five people with one seat kept for a junior; Martin Fowler (February 2026) bets same-size teams will do much more; Anthropic's Katelyn Lesse (July 2026) says her teams remain two-pizza despite AI supercharging. The two-pizza rule itself traces to Bezos via Fast Company, August 2004: five to seven people. The synthesis rejects cookie-cuttering any number and sizes by context instead, as listed in the takeaways.

### [49:07](https://youtu.be/Tc2RFLa0ip8?t=2947) Scorecard

Pin one (no more developers) falls: the role shifts rather than disappearing. Pin two (no talking or thinking) falls: conversation was always the mechanism. Pin three (the perfect spec) wobbles: dark factories work in their quadrant only. The closing line separates the two Taylorisms: linearize the work with AI, and stay humane to the workers deciding what is valuable in the remaining mess.

## Who should watch

Team leads, engineering managers, and architects deciding how to organize humans and agents, plus developers wondering where their role is heading, will get the most from the synthesis. Viewers wanting hands-on agent workflows, benchmarks, or tooling comparisons should look elsewhere: this talk contains no demos and no measured results.

## Verdict

**6/10**: A broad, well-sourced argument that agents move the developer's contribution up a level, with a team-size and spec-as-source framework to place yourself in, limited by thin original material, no demonstration, and no measurements.

**Novelty 1/2**

- **+** [43:16](https://youtu.be/Tc2RFLa0ip8?t=2596) The local-versus-systemic by conventional-versus-novel matrix for placing spec-driven work is the speakers' own framework, and no search result restates it.
- **+** [20:50](https://youtu.be/Tc2RFLa0ip8?t=1250) Taylor versus Drucker (1911 versus 1959) is applied to offshoring, dark scrum and XP, and then to agents, bringing several credited sources into one argument.
- **−** [44:19](https://youtu.be/Tc2RFLa0ip8?t=2659) The matrix is asserted quadrant by quadrant and draws on Plur's Wardley map; no team of the speakers' own is run through it.

**Demonstrated 1/2**

- **·** [38:05](https://youtu.be/Tc2RFLa0ip8?t=2285) A strategy and culture talk has nothing to run; the dark-factory shutdown is reported secondhand from Dex Horthy and nothing is shown working.

**Measured 1/2**

- **+** [12:32](https://youtu.be/Tc2RFLa0ip8?t=752) The historical figures (more than one in four programmers women by 1960, one woman per eight men by 1967) and the 1968 Sackman study anchor the stereotypes segment in dated sources.
- **−** [30:15](https://youtu.be/Tc2RFLa0ip8?t=1815) The 8-million-view post and the reports of apathy and burnout are anecdotes with no method or baseline.
- **·** [29:13](https://youtu.be/Tc2RFLa0ip8?t=1753) The show-of-hands poll on which developer role the room sees is audience opinion, not a measurement.

**Depth 2/2**

- **+** [41:42](https://youtu.be/Tc2RFLa0ip8?t=2502) The rebuttal of Anthropic's linear lifecycle uses Reeves on programming as design to explain why software is only partially nonlinear and which parts tools already linearize.
- **+** [43:16](https://youtu.be/Tc2RFLa0ip8?t=2596) Each matrix quadrant gets its own prescription (who judges, what the spec becomes), weighing dark against dim factories by context instead of declaring a winner.
- **+** [48:02](https://youtu.be/Tc2RFLa0ip8?t=2882) Team-shape trade-offs (stable versus fluid, criticality, prototyping versus internal tools) give a beginner audience a when-to-choose-what model.

**Reusable 1/2**

- **+** [02:39](https://youtu.be/Tc2RFLa0ip8?t=159) The QR code points to Substack articles that collect the full-length quotes and sources cut from the talk.
- **−** [02:39](https://youtu.be/Tc2RFLa0ip8?t=159) The articles were unfinished at talk time ("still work in progress"), so the take-home is a reading list, not a checklist, repository or configuration.
