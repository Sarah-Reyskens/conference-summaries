---
title: AI Made Building Cheap. Now Decisions Are the Bottleneck.
talkId: "4086"
conference: devoxx-be-2026
speakers: [Dave Sammut, João Rosa]
track: People, Practices & Career
sessionType: Conference
audienceLevel: ADVANCED
video: https://www.youtube.com/watch?v=2pSyF44THEc
durationMin: 42
slides: null
verdict: 7
reach: segment
frames: 9
summarizedAt: 2026-10-14
reviewedAt: 2026-10-15

# AI Made Building Cheap. Now Decisions Are the Bottleneck.

Dave Sammut, João Rosa · Conference · People, Practices & Career

## TL;DR

AI accelerates building faster than most organisations can decide, so the bottleneck moves from execution to decision-making. Two consultants present a field-tested method (lenses, signals, hypotheses, reversible moves) and show it working on an insurer's sales platform and claims migration.

## Key takeaways

- Treat AI adoption as an organisational-design problem first: map how work actually happens before scaling pilots, or faster execution produces worse consequences.
- Run decisions as hypotheses with reversibility in mind: a past decision that proved wrong deserves reversal, not loyalty disguised as discipline.
- Feed interviews, workshop photos and event-storming artefacts to an LLM to surface pain points and domain maps in a couple of hours.
- Analyse architects' invisible work (jobs-to-be-done) before automating their toil: some toil is a learning opportunity the LLM should not take away.
- Plan for AI success costs early: one team's refactoring agents scaled across 249 teams drove token spend up until FinOps attribution and model guidance reined it in.
- Keep business and tech deciding together on migrations: AI-generated storytelling artefacts (specification by example, use cases, logic locations) let subject-matter experts apply the four Rs (replace, replatform, remove, rearchitect).

## Notes

### [01:08](https://youtu.be/2pSyF44THEc?t=68) Thesis: faster building exposes the organisation

Rosa and Sammut frame the talk as field learnings, not recipes. Sammut's clients apply AI, get some wins and some burns, then face a first decision: take time to understand the organisation or keep rushing. The talk argues for the pause.

### [03:11](https://youtu.be/2pSyF44THEc?t=191) The method: lenses, signals, hypotheses, reversible moves

Overwhelmed by client questions, the pair wrote a paper (peer-reviewed by banks and telecom providers) built on one thesis: AI makes everything faster, and organisations that cannot respond face new consequences. The method reads an organisation through diagnostic lenses that surface signals from the same body of information, turns observations into hypotheses, and proceeds on assumptions that get validated or invalidated before scaling. Sammut borrows the Mikado (pick-up-sticks) effect from refactoring: check consequences across the whole cube before moving. Ground truth (interruptions, invisible work, handovers) always differs from the documented org chart.

### [07:52](https://youtu.be/2pSyF44THEc?t=472) Case setup: a 200-year-old insurer

The running example is a global insurer shaped by mergers: legacy estates, reorganisations, stable teams now forming around services. Executives ask why modernisation money still leaves them slow while new competitors move fast, and whether AI regains leadership or just burns more millions.

### [11:06](https://youtu.be/2pSyF44THEc?t=666) Sales and distribution: an AI refactoring pipeline that scaled

For the distribution platform (external agents plus direct digital sales), the team mapped work on the Accelerate visible/invisible value 2x2 and hypothesised AI could clear tech-debt items that never survived sprint planning: a plugin model rewrite and class/cyclomatic-complexity rule compliance flagged by SonarQube and CodeScene. Their pipeline mixes deterministic steps with LLMs: tools score the code, scripts create backlog actions, an LLM prioritises the refactoring plan and refactors with tests (reusing open-source agents and skills), then humans re-analyse and close the item. It worked, and 249 teams wanted in. Team Gamma moved the capability into the DevEx platform (v2) in a collaboration interaction mode, which stabilised into as-a-service consumption. Victim-of-success followed: token costs exploded as teams used the agents for unplanned cases, so a middle AI platform emerged applying FinOps attribution, model guidance, and experiments with post-trained open models for the bounded problem.

### [21:35](https://youtu.be/2pSyF44THEc?t=1295) Claims migration: lenses that find where it hurts
Sammut's advice is to start where it hurts. A 15–20 minute guided conversation, distilled by an LLM and mirrored in Miro, yields an event-storming board with pain points: claim assessment takes 5 days lead time, approval takes three days, A/B testing is weak. Acting on "it's legacy" alone risks regretful decisions, so curiosity drives deeper lenses. An SDLC lens (Imagine, Model, Make, Move, Maintain) locates untouchable logic, excessive lead time in Make, no data parity, and poor A/B testing. An architect-jobs-to-be-done lens at a Dutch bank split work into firefighting, operational and strategic; automating 58% of operational toil revealed some toil was valued learning. Domain and Team Topologies lenses showed SMEs absent from decisions and an awkward implementation-team handover, distilled in two to three hours.

### [34:02](https://youtu.be/2pSyF44THEc?t=2042) Claims decisions: AI archaeology and the four Rs

The insurer funded an enabling team doing AI archaeology: analysing source, schemas, usage data and journeys to produce business-readable outputs (specification by example, storytelling, use cases, logic locations). With business and tech finally talking the same language, SMEs could apply the four Rs to each legacy part instead of parroting a lift-and-shift. Sammut adds a culture caveat via the Westrum model: pathological or bureaucratic organisations that punish mistakes will not get value from hypotheses. Every hypothesis must answer whether it moves the dial: pivot, scale, or stop.

### [37:08](https://youtu.be/2pSyF44THEc?t=2228) Takeaways: diffusion, learning, commitment

Rosa closes with three points for large enterprises: knowledge must travel across hundreds of teams through existing communities of practice, internal conferences and informal networks; organisations must keep learning (the Broadcom/VMware licensing shock punished those that stopped innovating on workloads); and budget holders must stay committed without falling for sunk cost: pivot when it fails, but expect no magic. The final slide offers the Equal Experts "AI in the SDLC Transformation" whitepaper via QR code.

## Tools, libraries and specs

- SonarQube and CodeScene: rule-based code scoring feeding the refactoring backlog.
- Miro plus LLM: guided-conversation notes synthesised into shared event-storming and domain maps.
- FinOps principles and tooling (unnamed): attributing LLM token spend per team.

## Who should watch

Architects, transformation leads and engineering managers pushing AI past pilots in large organisations gain the most, especially anyone planning a legacy migration. Skip it if you want prompt techniques, agent frameworks or code: the AI mechanics stay at pipeline-shape level.

## Verdict

**7/10**: Two client cases carry the speakers' own decision method, backed by a published white paper, but the figures lack baselines and the AI mechanics stay at pipeline-shape level.

**Reach segment**: Architects, transformation leads and engineering managers driving AI adoption or legacy migration in large organisations can use the method within the year; most developers meet it only when their own team enters such a change.

**Novelty 2/2**

- **+** [19:01](https://youtu.be/2pSyF44THEc?t=1141) The insurer's refactoring capability, moved onto the DevEx platform as a service, became a victim of its own success when token spend blew up until FinOps attribution and model guidance reined it in, which is production experience no search gives.
- **+** [29:22](https://youtu.be/2pSyF44THEc?t=1762) At a Dutch bank, Sammut built his own jobs-to-be-done lens from conversations with a room of architects, synthesised it with an LLM into firefighting, operational and strategic work, and used it to pick where to apply AI, a field-tested framework no single source offers.

**Demonstrated 1/2**

- **·** [01:08](https://youtu.be/2pSyF44THEc?t=68) The talk presents field learnings and explicitly not recipes, an organisation-design subject with nothing runnable to show, so no demo is due.

**Measured 1/2**

- **+** [25:15](https://youtu.be/2pSyF44THEc?t=1515) Claims pain is quantified as signals on the event-storming slide: assessment lead time of 5 days, approval of 3 days, and no A/B testing, with no baseline or counting method.
- **−** [17:28](https://youtu.be/2pSyF44THEc?t=1048) The pipeline's success is claimed through enterprise-rule alignment and demand from 249 teams, a self-reported total with no before/after outcomes.
- **−** [31:26](https://youtu.be/2pSyF44THEc?t=1886) The architect intervention's effect is deferred to a six-month revisit, so the method's payoff is still future work.

**Depth 1/2**

- **+** [26:48](https://youtu.be/2pSyF44THEc?t=1608) The guided-conversation plus LLM plus Miro technique comes with its reasons: designed conversations avoid blank-page paralysis, and mirroring the synthesis back lets people confirm "you said this, this is what you meant".
- **+** [30:24](https://youtu.be/2pSyF44THEc?t=1824) The toil-automation trade-off is weighed with evidence: the team automated part of the architects' operational work, then kept some toil back when architects said handing it over would cost them learning.
- **·** [34:32](https://youtu.be/2pSyF44THEc?t=2072) The AI archaeology analysis itself is never opened: its business-readable outputs are listed, but an advanced practitioner cannot reconstruct how source, schemas and usage become business rules.

**Reusable 2/2**

- **+** [41:50](https://youtu.be/2pSyF44THEc?t=2510) The closing QR points to the published "AI in the SDLC Transformation" white paper, which documents the talk's signals, lenses and reversible-moves method.
- **−** [16:24](https://youtu.be/2pSyF44THEc?t=984) The refactoring pipeline's scripts, agents and skills are neither published nor named beyond "open source repositories", so the pipeline has to be rebuilt from the description.
