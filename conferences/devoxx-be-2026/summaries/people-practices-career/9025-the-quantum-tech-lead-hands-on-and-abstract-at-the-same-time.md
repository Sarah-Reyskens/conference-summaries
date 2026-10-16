---
title: "The Quantum Tech Lead: Hands-On and Abstract at the Same Time"
talkId: "9025"
conference: devoxx-be-2026
speakers: [Cristian Schuszter]
track: People, Practices & Career
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=Spxl1eDQJKs
durationMin: 47
slides: null
verdict: 5
reach: broad
frames: 8
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# The Quantum Tech Lead: Hands-On and Abstract at the Same Time
Cristian Schuszter · Conference · People, Practices & Career

## TL;DR
Getting promoted past senior engineer replaces fast code feedback loops with slow, ambiguous people problems, and the fix is to lead through influence rather than authority. The speaker lays out how a tech lead zooms between team and org levels, scales impact through writing and delegation, and stays hands-on without becoming the bottleneck. It ends with the observation that delegation, context and review are exactly the skills agentic AI workflows demand.

## Key takeaways
- Treat promotion as a role change, not a reward: coding gave compile-level feedback in seconds, while leadership feedback loops take weeks and run on alignment.
- Lead people who do not report to you through influence without authority: build trust and clarity instead of issuing orders, since you cannot give them raises or orders.
- Match the leadership style to the moment: be authoritative when a deadline is on fire, coach when it is not, and accept that democratic decisions are slow and sometimes need one person to decide.
- Make the written word the compiler: one-screen ADRs and design docs scale a decision across teams in a way code alone cannot.
- Delegate even when it feels slower than doing it yourself, because mentoring grows the team; picking up tasks you cannot finish makes you the bottleneck.
- Build a support circle of fellow tech leads that meets regularly, since the role is lonely and peers have already solved versions of your problems.

## Notes

### [00:33](https://youtu.be/Spxl1eDQJKs?t=33) The promotion paradox
Schuszter, a solutions architect and team lead in CERN's business computing group, opens with the Peter principle: excellent engineers get promoted into roles where they are no longer excellent, the way a good plumber is not automatically good at leading plumbers. The old world had deterministic systems and fast feedback (compile, tests); the new one has ambiguity, priorities and alignment, with feedback loops that take a long time. Longer loops mean less dopamine, which is why stepping away from code feels like withdrawal. He then sketches a career map with three broad paths (deep technical expert, leading teams and multiplying impact, hands-off engineering manager) connected by bridges people cross back and forth, and argues autonomy increases with seniority: nobody will point at the meaningful work, so value delivered to users replaces lines of code as the measure.

### [07:45](https://youtu.be/Spxl1eDQJKs?t=465) Thinking in layers and zoom levels
A tech lead wears many hats at once: architect, people leader, strategist, communicator, explorer, problem solver, mentor. Zoom levels matter because a decision that hurts one team's output can help the whole organisation, illustrated by a DevOps team that stops shipping features to fix its process and then scales delivery for every product team. Titles carry weight across team boundaries in large organisations: a "principal engineer" label gets a hearing a "junior developer" label does not, which also counteracts bias. Context works the same way: outside your team, the role is what signals your capabilities. The recurring point is that output should multiply the output of influenced teams, while the blast radius of mistakes grows with responsibility.

### [11:55](https://youtu.be/Spxl1eDQJKs?t=715) The four tech-lead hats and influence without authority
Day to day the role splits into guiding technical direction through reviews, the broad-view architect, the solver who dives into the mud with the team (which earns credibility, and visible failure earns trust), and the right hand doing strategy and negotiation. Schuszter recommends the book Influence Without Authority: leading people who do not report to you runs on respect, trust and credibility, which create momentum and keep things moving. Cultural differences shape how respect and trust are built, so the approach needs tuning per audience.

### [16:04](https://youtu.be/Spxl1eDQJKs?t=964) Scaling impact beyond code
Technical excellence is not enough, especially as AI-assisted development pushes engineers further from the keyboard. Impact happens at the edges: processes, stakeholder relationships and business analysis, including telling stakeholders what they actually want. The written word is the new compiler. His example ADR fits on one screen: migrate libraries from javax to Jakarta EE first, then move the code, unblocking every team at once. Design docs and RFCs collect feedback before the first line of code, and one-pagers beat five-page PDFs nobody reads without feeding them to an assistant. The section closes on empathy: engineers are historically bad at seeing others' feelings, and people will not trust or follow someone who treats them badly no matter how strong technically. He proposes a listening exercise (ten minutes, one colleague tells a story about their values, no interruptions allowed) and names psychological safety and conflict resolution as skills to study.

### [22:47](https://youtu.be/Spxl1eDQJKs?t=1367) Goleman leadership styles
All six of Daniel Goleman's styles get used at different times: authoritative (deadline crunch, assigns tasks directly, creates stress), coaching (the default outside crunches: lift team members up, praise in public, give constructive feedback in private, never hog credit), affiliative (harmony and friendliness), democratic (great but slow; sometimes one person must finally decide), pacesetting (running in the mud alongside high performers toward a deadline), and coercive (demanding immediate compliance, least used now).

### [26:23](https://youtu.be/Spxl1eDQJKs?t=1583) Organisations as distributed computers
The slide maps distributed-systems concepts onto org life: latency is approval chains and meetings; consensus is expensive alignment; eventual consistency means decisions take time to reach every team; network partition is teams that stopped talking; backpressure is saying no (or "not yet"); Conway's law means architecture mirrors the org chart. The practical consequence is the executive-arm role: a good architectural decision that nobody adopts is worthless, so someone must chase teams across sprints and negotiate adoption.

### [28:56](https://youtu.be/Spxl1eDQJKs?t=1736) Staying hands-on without burning out
The trap is starving for code, grabbing a task, then letting a full calendar delay it a week and becoming the bottleneck that stalls team momentum. The guidance is to be selective: only take hands-on work you can do now, prefer the most impactful tasks over low-hanging fruit, and scratch the itch through side projects or non-critical code in a small time slice without undermining the team. Shipping a quick, dirty, half-finished solution and throwing it over the wall creates long-term resentment, so soliciting feedback matters, even though giving a lead critical feedback is culturally hard. Delegation feels slow (a junior taking long on a task you feel you could have finished yesterday) but it mentors people toward independence, like teaching someone to fish rather than handing them one daily. Invisible glue work (documentation, alignment, onboarding, mentoring) keeps the organisation running and is rarely thanked. Mentoring takes patience: explain the high level first, then descend into detail, and keep hands off the keyboard. Because the role is lonely at the top, he recommends a regular support circle of staff engineers and tech leads (his meets every three to four weeks) as a safe space to trade scenarios.

### [37:17](https://youtu.be/Spxl1eDQJKs?t=2237) Redefining impact: spheres of control
The closing framework is concentric spheres of control, influence and concern: control barely grows with promotion (no extra pair of arms), but influence expands, and influencing one team pushes into another team's sphere of concern, which brings visibility. Done well, the lead multiplies impact through others' better decisions instead of doing everything personally. The best tech leads combine people leadership, strategic thinking, continued technical problem-solving (war stories that warn against attractive short-term ideas), curiosity, decision-making, stakeholder partnership, and concise communication: if the message needs more than a line, write the design doc. Nobody is stuck: moving into hands-off management never blocks bouncing back to a technical track. In Q&A, asked about burnout, he says yes, but it happened earlier, while deep in startup work rather than while leading people.

### [42:57](https://youtu.be/Spxl1eDQJKs?t=2577) Leadership skills map onto agentic workflows
Delegating to people becomes breaking work into tasks an agent can own end to end; giving context becomes context engineering with specs, docs and examples; code review becomes reviewing agent output (tests, evals, diffs); paved roads become guardrails (tools, permissions, CI checks); and the reviewer of everything becomes the bottleneck again, this time as the human proxy over agent output. Recommended books: Staff Engineer, The Staff Engineer's Path, Influence Without Authority, Goleman's emotional-intelligence book, and The Manager's Path, praised for tracing one career from soldier to VP.

## Tools, libraries and specs
- Jakarta EE (javax to Jakarta migration used as the ADR example)
- Voxxed Days CERN (27th edition plug: 5 March 2027 at CERN, CFP open)

## Who should watch
Newly promoted tech leads, staff engineers and senior engineers eyeing a leadership path get the most, especially those feeling the loss of coding feedback loops. Engineers wanting deep technical content or experienced managers well-read in Goleman, Covey and staff-engineering literature can skip it.

## Verdict
**5/10**: a tour of tech-lead practice built on credited sources (Goleman, Covey, the Peter principle), carried by the speaker's own framings and examples; it shows nothing running, measures nothing and stays at the level of described practices.

**Reach broad**: most of the conference audience works in teams and can use the influence-without-authority, listening, ADR and delegation practices in their own work within the year.

**Novelty 1/2**

- **+** [26:23](https://youtu.be/Spxl1eDQJKs?t=1583) The organisation-as-distributed-computer mapping (latency as approval chains, consensus as expensive alignment, backpressure as saying no, Conway's law) is the speaker's own framing of standard organisational advice.
- **+** [42:57](https://youtu.be/Spxl1eDQJKs?t=2577) The closing parallel between leading people and directing coding agents (delegation, context, code review, paved roads, the human as review bottleneck) gives the familiar material a second, current application.
- **+** [04:40](https://youtu.be/Spxl1eDQJKs?t=280) The three-path career map with bridges between paths is the speaker's own construction ("I tried to build something called the career map").

**Demonstrated 1/2**

- **·** A people-leadership talk has no code, system or experiment to run; the slides carry diagrams and frameworks.

**Measured 1/2**

- **·** The talk makes no claim about speed, cost, adoption or effect that needed backing; its only numbers are illustrations or self-reports, such as about 10% of his time on architecture [13:29](https://youtu.be/Spxl1eDQJKs?t=809).

**Depth 1/2**

- **+** [23:17](https://youtu.be/Spxl1eDQJKs?t=1397) Each Goleman style gets a when-to-use rule tied to a team situation (authoritative for a deadline crunch, coaching whenever there is no crunch, democratic accepted as slow).
- **+** [18:09](https://youtu.be/Spxl1eDQJKs?t=1089) The one-screen javax-to-Jakarta ADR (move the libraries first, then the code) shows what a scaled decision record looks like, though the speaker calls it a "dumb ADR" built for illustration [27:25](https://youtu.be/Spxl1eDQJKs?t=1645).
- **·** [31:03](https://youtu.be/Spxl1eDQJKs?t=1863) The overload case is the speaker's own (a quick-and-dirty fix thrown at the team, then he is the bottleneck), and the advice that follows (be selective, ask for feedback) stays general.

**Reusable 1/2**

- **+** [21:15](https://youtu.be/Spxl1eDQJKs?t=1275) The ten-minute no-interruption listening exercise and the tech-lead support circle meeting every three to four weeks [36:15](https://youtu.be/Spxl1eDQJKs?t=2175) are practices described well enough to run, but left for the listener to set up.
- **·** No repository, checklist or template covers the talk's content; the take-homes are the described practices plus a book list.
