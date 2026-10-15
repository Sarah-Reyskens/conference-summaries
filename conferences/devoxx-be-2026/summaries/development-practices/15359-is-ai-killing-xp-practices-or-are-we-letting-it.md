---
title: Is AI killing XP practices? (Or are we letting it?)
talkId: "15359"
conference: devoxx-be-2026
speakers: [Nacho Cougil]
track: Development Practices
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=wrV4f83UMWI
durationMin: 49
slides: null
verdict: 6
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Is AI killing XP practices? (Or are we letting it?)
Nacho Cougil · Conference · Development Practices

## TL;DR
AI coding tools make skipping Extreme Programming practices tempting, and each skipped practice opens a hole that AI fills with more code and more complexity. The talk puts seven XP practices on trial against the strongest case AI can make for dropping each one, and defends all seven. It leaves you with an audit: seven questions to ask before your team adopts AI tools.

## Key takeaways
- Treat TDD as design, not coverage: write the test to specify business behavior first, because an AI asked to test after the fact validates the implementation instead of the requirement.
- Keep refactoring human-owned: AI refactors syntax (renames, extracted patterns) but not the team's shared mental model of the domain, so unreviewed AI refactors grow tech debt.
- Say no to AI-generated complexity yourself: AI over-engineers with unneeded layers and never pushes back on a bad design idea, so YAGNI discipline has to come from the team.
- Pair with humans, not only with the assistant: AI builds code faster but builds no team knowledge, leaves juniors without mentoring, and does nothing for the bus factor.
- Ship small to keep learning: AI can generate a feature in hours, but big AI-generated releases collapse the feedback loop, diffuse blame, and make rollbacks expensive.
- Audit the seven practices before adopting AI tools: tests specifying behavior, design maintained vs accreted, complexity refused, knowledge shared, codebase explainable, changes integrated frequently, releases small enough to learn from.

## Notes

### [02:06](https://youtu.be/wrV4f83UMWI?t=126) Two warnings from production
A July 2025 story opens the talk: a CEO working with an AI agent watched it drop an entire database during a code freeze it had been forbidden to touch, then explain itself with "I panicked". Then Amazon's arc: a November 2025 push for 80% of engineers to use AI daily, followed by a 13-hour regional outage in December, a failed agent-led fix in February, 120,000 dropped orders plus 1.6 million website errors in March, and another March incident losing 6.3 million orders over 6+ hours. Amazon stepped back and put two-engineer review of changes in place. The question for the session: do we still need XP practices, or do we need them more than ever?

### [06:50](https://youtu.be/wrV4f83UMWI?t=410) Where XP came from
Waterfall in the 90s meant analyzed-then-designed-then-built software, constant production failures, missed deadlines, and burned-out developers. Kent Beck, Ron Jeffries, and Ward Cunningham built XP practices out of real pain on the Chrysler project: TDD from bugs found in production, pair programming from solo developers erring unreviewed. The practices were designed for mistake-making humans who learn continuously, to answer how to build software reliably and deliver it with high quality.

### [13:00](https://youtu.be/wrV4f83UMWI?t=780) The format: seven charges, seven defenses
The speaker, a Dynatrace principal engineer from Barcelona practicing XP for roughly 20 years, stages a trial: each practice faces the charge AI brings against it, then gets a defense. The seven: TDD, refactoring, simple design, pair programming, collective code ownership, continuous integration, and small releases.

### [14:02](https://youtu.be/wrV4f83UMWI?t=842) Charge 1: TDD, since AI writes tests for you
The charge is real: AI writes tests on demand with no discipline, coverage is reachable without TDD, and forgotten tests can be generated after the code ships. The defense: when the speaker asked an agent about a production bug its own tests had missed, it replied it had validated the implementation, not the business. Green suites can mask broken behavior. TDD is design: specify behavior in a test, implement until green. A Lightrun report (April 2026) found 43% of AI-generated code contains security issues or design flaws needing production debugging. Specification-driven development is presented as TDD's evolution: humans write the high-level spec and tests as architects, agents build the code.

### [20:17](https://youtu.be/wrV4f83UMWI?t=1217) Charge 2: refactoring, since AI cleans code on request
AI explains and refactors consistently, applies patterns without human bias, and the tests confirm it works. The defense: AI does syntactic pattern matching with no grasp of the domain's why, loses context, introduces bugs, and over-engineers. The GitClear "Maintainability Gap" report (June 2026, large corpus including Microsoft, Apple, Google repos) shows 2023-2026 trends: move/refactor activity fell from an index of 100 to about 30, duplication nearly doubled, and two-week code churn climbed toward 7%. Refactoring is how a team keeps the code expressing the domain; without it the codebase stops reflecting the business. In one anecdote, an AI refactor of a Java class was syntactically fine but left code the speaker's own team no longer recognized. AI refactors the code, not the mental model.

### [27:30](https://youtu.be/wrV4f83UMWI?t=1650) Charge 3: simple design, since AI designs for you
AI knows the principles, possibly better than most engineers, and generates architecture, code, and docs in one shot. The defense: it over-engineers with layers and patterns where none are needed, and YAGNI (you aren't gonna need it) disappears. The result is complex code that is hard to maintain and harder to change. Simple design is a maintained discipline, and AI never says no: it will find a path to implement even a bad idea rather than push back, so refusing complexity stays a human job.

### [30:38](https://youtu.be/wrV4f83UMWI?t=1838) Charge 4: pair programming, since AI is always available
AI is available 24/7, never distracted, never has a bad day, reviews code, and catches mistakes. The defense: without human pairing, knowledge sharing and mentoring disappear, and juniors have nobody to sit with and learn from. An audience poll found about 70% had paired with an AI tool in the previous two weeks, but half admitted their teammates would not understand what they had built or why. Pair programming builds shared understanding, not only code; AI builds code faster but no team knowledge. The bus factor does not improve when AI is your pair.

### [35:47](https://youtu.be/wrV4f83UMWI?t=2147) Charge 5: collective ownership, since AI explains any code in seconds
Generated code looks self-documented and consistent, and anyone can ask AI to explain or change any part. The defense: when AI writes the code, nobody owns the why behind it, and when production breaks nobody knows where to look. A Cloud Security Alliance report (September 2025) found 62% of AI-generated code contains design flaws or known vulnerabilities. Ownership means active understanding: space to read, discuss with colleagues, and explain any part of the system even when AI wrote it.

### [38:22](https://youtu.be/wrV4f83UMWI?t=2302) Charge 6: continuous integration, since AI already validated the code
AI reviews code and catches bugs before push, so the slow pipeline looks like bureaucracy re-verifying verified work. The defense: faster generation means more code arriving and more pipelines breaking, making integration more painful. CI was never only about finding bugs; it is about integrating everyone's contributions frequently with fast verification cycles. More generated code makes that discipline more critical, not less.

### [40:29](https://youtu.be/wrV4f83UMWI?t=2429) Charge 7: small releases, since AI delivers the whole feature at once
Prompts remove the old constraints: a multi-day feature can arrive in hours of agent iteration, so incremental delivery looks obsolete. The defense: AI output carries subtle bugs, merge conflicts, and security problems, and with big releases the feedback loop collapses, blame diffuses across the branch, and rollback gets expensive. Features now accumulate faster than the team can review; about 10% of the room raised a hand to already drowning in pull requests. Small releases were never about generation speed but learning speed: the constant was whether the team is building the right thing in the right order.

### [44:33](https://youtu.be/wrV4f83UMWI?t=2673) The holes compound, then the audit
The practices are not independent: failures compound, and each missing practice is a hole AI widens by pouring in more code and complexity. AI is a multiplier: excellent in senior hands with good habits, an exponential mess without them. Three closing points: AI makes no XP practice obsolete, skipping any practice is more expensive than ever, and some practices evolve (TDD with specification-driven development). Teams adopting AI tools should first audit the seven questions from the takeaways. AI is the best stress test XP practices ever had, and the speaker's ruling is that they passed.

## Who should watch
Teams and leads setting norms for AI-assisted development, and developers who know AI tooling but never learned XP. Viewers wanting hands-on technique (a TDD or refactoring demo, spec-driven tooling in action) should look elsewhere; this talk argues the case and names the discipline rather than teaching it.

## Verdict
**6/10**: Seven XP practices defended against the case for dropping each, with the mechanism for why each holds; limited by third-party figures quoted without method and an audit that exists only as speech.

**Novelty 1/2**

- **+** [04:14](https://youtu.be/wrV4f83UMWI?t=254) The Amazon incident sequence, the agent database-drop story, and three named industry reports are brought together under one charge-and-defense framework.
- **+** [16:05](https://youtu.be/wrV4f83UMWI?t=965) The speaker's own cases carry part of the argument: an agent admitting it validated the implementation rather than the business, and an AI refactor of a Java class that the speaker's team no longer recognized ([26:29](https://youtu.be/wrV4f83UMWI?t=1589)).

**Demonstrated 1/2**

- **·** [10:58](https://youtu.be/wrV4f83UMWI?t=658) A strategy talk with nothing to run; its screen moments (IDE autocomplete, industry trend charts) illustrate claims rather than demonstrate them, so there is no demo to fail.

**Measured 1/2**

- **+** [22:53](https://youtu.be/wrV4f83UMWI?t=1373) The GitClear June 2026 chart tracks repo metrics over 2023-2026 with a baseline of 100: refactor activity falls to about 30, duplication nearly doubles and two-week churn climbs toward 7%.
- **−** [04:45](https://youtu.be/wrV4f83UMWI?t=285) The Amazon outage figures (13 hours, 120,000 and 6.3 million lost orders) are stated without naming any report or source a viewer could check.
- **−** [36:47](https://youtu.be/wrV4f83UMWI?t=2207) The Cloud Security Alliance's 62% and Lightrun's 43% ([17:08](https://youtu.be/wrV4f83UMWI?t=1028)) design-flaw figures are relayed as headline totals, and the GitClear corpus is named without a method for how refactoring was measured.

**Depth 2/2**

- **+** [17:38](https://youtu.be/wrV4f83UMWI?t=1058) TDD is reframed as design rather than coverage, with the mechanism spelled out: tests specify business behavior first so green means the functionality is done.
- **+** [25:58](https://youtu.be/wrV4f83UMWI?t=1558) Refactoring is explained as maintaining the team's shared mental model of the domain, which is why syntactic AI refactors can be correct yet harmful.
- **+** [39:56](https://youtu.be/wrV4f83UMWI?t=2396) CI is explained as frequent integration with constant verification cycles rather than bug-finding, so more generated code makes it more necessary.

**Reusable 1/2**

- **+** [48:10](https://youtu.be/wrV4f83UMWI?t=2890) The closing audit gives seven questions a team can run before adopting AI tools.
- **−** [48:41](https://youtu.be/wrV4f83UMWI?t=2921) The checklist exists only as spoken words; no repository, sample, or written checklist is pointed to.
