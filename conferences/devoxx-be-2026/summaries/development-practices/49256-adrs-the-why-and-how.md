---
title: "ADRs: The Why and How"
talkId: "49256"
conference: devoxx-be-2026
speakers: [Venkat Subramaniam]
track: Development Practices
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=wzN6qq08w0U
durationMin: 50
slides: null
verdict: 5
frames: 7
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---
# ADRs: The Why and How
Venkat Subramaniam · Conference · Development Practices

## TL;DR
Code captures decisions but loses the reasoning behind them, so teams end up doing software archaeology instead of architecture. Architectural Decision Records fix this with short, immutable, plain-text documents that record the context, options, and consequences of each significant decision. The talk makes the case through consulting stories and ends with concrete rules: supersede rather than edit, keep each record short and numbered, and store them in version control.

## Key takeaways
- Treat architecture as the set of decisions with high impact, not the set that is hard to change; plenty of hard-to-change code deserves no celebration.
- Judge every decision by its reversibility: the harder it is to back out of, the more deliberate the choice needs to be.
- Give every technical decision and corporate standard an expiration label and revisit it on schedule instead of following it forever.
- Consider at least three options with pros and cons before settling on a decision, and record the consequences you accept.
- Keep each ADR immutable once decided; when reality changes, write a new ADR that supersedes the old one instead of editing history.
- Store ADRs as short, sequentially numbered plain-text files in version control so they diff, get reviewed in pull requests, and stay searchable.

## Notes

### [01:34](https://youtu.be/wzN6qq08w0U?t=94) Design versus architecture
Martin Fowler defines architecture as the decisions that are hard to change; Subramaniam counters that he can create many things that are hard to change without that counting as architecture. His definition: architecture is the set of decisions that have high impact. Design and architecture sit on one continuum rather than in separate boxes. Which XML parser to use is a design decision because a facade can contain the library's surface area; which language, database, or framework to use is architectural because a framework grows around you and locks you in, like buying a house versus renting one.

### [11:58](https://youtu.be/wzN6qq08w0U?t=718) Reversibility and trade-offs
Reversibility is the ability to back out of a decision, illustrated with 24-hour free airline cancellation versus paying more for a refundable ticket. Architecture work is constant trade-off evaluation: list the characteristics you want, pick which to favor and which to lower this time, and accept the compromise consciously. Code conveys implementation and abstraction (the tactical layer) but almost never the reasoning, which is the strategic layer ADRs exist to capture.

### [16:36](https://youtu.be/wzN6qq08w0U?t=996) Why is the question nobody can answer
Subramaniam calls himself a "why" person: without a valid reason to do something, he looks for a way not to do it. A consulting visit showed a team expecting a two-week change that actually needed three months because of past decisions, and the architect who had joined eighteen months earlier could not explain why the code was built that way. Cave paintings whose meaning is lost forever draw the parallel: the code is still there, but what its author meant is gone. Comments are too low-level and annoying to carry strategic reasoning.

### [24:24](https://youtu.be/wzN6qq08w0U?t=1464) Documentation, but short
"Agile means no documentation" is dismissed as a misreading of agile, while documentation for its own sake gets mocked through a client practicing death by documentation and a boss who files unread weekly reports without opening them. Large documents go unread and unmaintained, so the rule is to keep records short. The point is illustrated with the $50-bill experiment: hide one on page 25 of a team document and collect it unread three weeks later.

### [28:06](https://youtu.be/wzN6qq08w0U?t=1686) The document nobody wanted, then needed
Early in his career, a supervisor refused to let him move on until he documented a hard-won design, then reviewed and corrected it before it went into version control. Months later he remembered nothing of the details, but a colleague who called the implementation weird read the document and concluded he would otherwise have changed the code only to rediscover the same problem. The trail of why decisions were made paid for itself within months.

### [32:48](https://youtu.be/wzN6qq08w0U?t=1968) Writing exposes weak reasons
The number one reason to write ADRs: excuses that slip by in verbal discussion ("this is all I know", "everybody else is doing it", "corporate standard") look indefensible once someone has to write them down and get them approved. Technical decisions are like cartons of milk and need expiration labels; standards should be re-certified every few months rather than rinsed and repeated across teams unchallenged. Recorded reasons also protect future changes: if the original reasons still hold, a rewrite rediscovers them expensively, and if they no longer hold, the team can justify moving on.

### [42:34](https://youtu.be/wzN6qq08w0U?t=2554) What goes into an ADR
An ADR holds a title, the context being evaluated, a status (introduced, under review, approved, rejected, parked), the decision itself, the options considered with pros and cons, and the consequences of the choice (scalability, performance, security, restricted environments). Code-level detail stays out: these are strategic records, not tactical documentation. The screen notes list the same structure: title, context, status, decision, options with pros and cons, consequences.

### [45:13](https://youtu.be/wzN6qq08w0U?t=2713) Tenets for keeping ADRs
ADRs are immutable once decided; only the status and typos change afterward, because editing destroys the original reasoning. A new ADR supersedes an outdated one and links back to it like a linked list. Keep each record short, in plain text (easy to search, edit, and diff, as the Pragmatic Programmers argued), sequentially numbered, and in version control, ideally reviewed through pull requests. ADR tools with a UI are fine since they persist plain text underneath. One person taking the initiative is enough to start the practice on a team.

## Who should watch
Developers and architects on teams that keep rediscovering why old decisions were made, and anyone trying to introduce lightweight documentation without reviving big-design-up-front habits. Skip it if you already write and maintain ADRs routinely; the format and tenets will hold no surprises.

## Verdict
**5/10**: A story-driven case for ADRs with tenets a team can adopt as policy, but the format and tenets are the standard ADR playbook and the how-to part is short and thinly reasoned.

**Novelty 1/2**

- **+** [33:49](https://youtu.be/wzN6qq08w0U?t=2029) The expiration-label argument for technical decisions and corporate standards, with the seventh-team rinse-and-repeat anecdote, frames ADRs as living records rather than write-once paperwork.
- **+** [30:42](https://youtu.be/wzN6qq08w0U?t=1842) The speaker's own early-career document, which kept a colleague from changing code and rediscovering the same problem, is the production experience that carries the case.
- **·** The ADR format and tenets follow the well-known adr.github.io conventions, so the value comes from the speaker's stories and framing, not from new material.

**Demonstrated 1/2**

- **·** A strategy and culture talk about a writing practice with nothing to run on screen, so there is no demo to judge.

**Measured 1/2**

- **·** The talk makes no quantitative claim: "a lot of time, a lot of money" ([37:25](https://youtu.be/wzN6qq08w0U?t=2245)) names no amount, and its figures (two weeks versus three months, three weeks tracing house wiring) are anecdotes.

**Depth 1/2**

- **+** [45:44](https://youtu.be/wzN6qq08w0U?t=2744) Immutability comes with its reason ("if you modify the ADR, the original decisions are gone"), and superseding is explained as a linked list of records.
- **+** [06:18](https://youtu.be/wzN6qq08w0U?t=378) The high-impact definition of architecture sets which decisions deserve deliberate records and which can be taken lightly.
- **−** [43:07](https://youtu.be/wzN6qq08w0U?t=2587) The ADR fields (title, context, status, decision, options, consequences) are listed with short glosses and only the consequences section gets a reason, with just a one-line NoSQL example at [43:38](https://youtu.be/wzN6qq08w0U?t=2618).

**Reusable 1/2**

- **+** [45:13](https://youtu.be/wzN6qq08w0U?t=2713) The tenets (immutable, supersede, short, plain text, numbered, version-controlled) are specific enough to adopt directly as team policy.
- **·** [47:49](https://youtu.be/wzN6qq08w0U?t=2869) ADR tooling is mentioned without a name, and no template, repository or sample ADR is pointed to, so each team reconstructs the format from the talk.
