---
title: "Knocking on the Wrong Door: The Six Developers You’ll Meet in Security"
talkId: "12758"
conference: devoxx-be-2026
speakers: [Enrique Larios Vargas]
track: People, Practices & Career
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=qrtd6svRUnk
durationMin: 41
slides: null
verdict: 6
reach: broad
frames: 6
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Knocking on the Wrong Door: The Six Developers You’ll Meet in Security
Enrique Larios Vargas · Conference · People, Practices & Career

## TL;DR
Most security programs fail because they prescribe one-size-fits-all interventions (training, tools, policies) without diagnosing which behavioral barrier actually blocks secure development. Vargas presents six developer patterns mapped to the COM-B model (capability, opportunity, motivation) and a recipe from the OWASP Security Culture project: diagnose the pattern first, then match the support to the blocker.

## Key takeaways
- Before prescribing any security intervention, diagnose which barrier blocks the behavior: ask "can I do it, can I do it here, will I do it?"
- Mandatory training only works when the blocker is a skill or knowledge gap; aimed at time pressure, distrust, or lack of autonomy it changes nothing.
- One intervention lands six different ways on one team, so a program designed without knowing the team's predominant patterns is guessing.
- Treat resistance as feedback on the program, not defiance: making resistant developers co-authors of a control turns them into its advocates.
- Pattern labels describe current conditions, never people: using them for hiring, reviews, or discipline destroys the trust the method needs.

## Notes

### [01:06](https://youtu.be/qrtd6svRUnk?t=66) Keys, doors, and the wrong-door metaphor
Security teams hold keys (mandatory training, policies, tools) and try them on a hallway of doors, where each door is a barrier to behavior change. When the key does not fit the door in front of them, the intervention fails no matter how well it is executed. The familiar symptom: full training completion with green compliance dashboards, then the same pentest findings and incidents six months later. Vargas asks the audience to confirm nearly everyone has sat through mandatory training this year, then argues the default reaction to persistent failures (more training, more tools, stricter checklists) repeats the mistake. Knowing differs from doing, and behavior change does not transfer automatically from knowledge.

### [11:38](https://youtu.be/qrtd6svRUnk?t=698) COM-B: capability, opportunity, motivation
Behavioral science frames any behavior through three questions: can they do it (capability: skills, knowledge, confidence), does the environment support it (opportunity), and do they believe it is worth doing, especially under pressure (motivation). Training fits only a capability blocker; aimed at a time, trust, or autonomy blocker it knocks on the wrong door. The slide deck renders this as "Can they? Can they here? Will they?" The method starts with the individual developer acknowledging their own profile, then moves to a team conversation, since behavior is social and teams show predominant patterns.

### [18:42](https://youtu.be/qrtd6svRUnk?t=1122) The six developers
Six behavioral patterns, each with a COM-B profile, a wrong door, and a right door. The Skeptic ("Nobody's ever attacked us") lacks motivation through distrust and needs evidence such as late-fix costs, not fear. The Enthusiast ("I'm already on it") is capable and motivated but unsupported, and needs time, recognition, or a champion role instead of extra tasks. The Compliant ("I do it because that's what the process requires") mistakes compliance for quality and needs compliance connected to craft. The Unaware ("I didn't know that mattered") needs foundations, and pairing with an enthusiast spreads good habits socially. The Resistant ("This slows everything down") is often highly capable with negative motivation, and needs to co-design the control. The Embedded ("Security is part of how I build") is the ideal others should see as a role model, and must not be taken for granted. Patterns can mix and shift over time.

### [30:54](https://youtu.be/qrtd6svRUnk?t=1854) Diagnose before prescribing
The recipe: recognize your pattern individually, discuss predominant patterns openly with the team, then design support together. The summary slide pairs each pattern with its match: skeptic with evidence, enthusiast with support, compliant with meaning, unaware with foundations, resistant with autonomy, embedded with amplification. With a single intervention budget, teams must trade off quick wins against the most productive impact across diverse patterns. AI-generated code makes diagnosis harder and human judgment more of a bottleneck, raising the cost of the wrong door.

### [33:33](https://youtu.be/qrtd6svRUnk?t=2013) The SECUR-E tool, trust, and closing
The OWASP Security Culture project is building SECUR-E, a self-assessment tool that walks teams through the diagnose-then-match recipe and predicts what backfires when the wrong door is knocked. The tool is in a validation phase and the speaker asks the audience to try it and report whether it reflects their real workflows. Because pattern data tempts misuse in hiring, reviews, or discipline, assessments should stay anonymous and team leads should see only predominant team patterns. The closing slide asks the audience to name one security intervention they have seen knocking on the wrong door.

## Tools, libraries and specs
- OWASP Security Culture project (SECUR-E framework): the behavioral playbook and team self-assessment this talk presents
- COM-B model (capability, opportunity, motivation): the behavioral-science model behind the diagnosis

## Who should watch
Team leads, engineering managers, and security champions deciding where to spend a limited security-improvement budget gain a practical diagnostic vocabulary. Developers curious why training never seems to stick get an explanation that points away from blame. Skip it if you already work with COM-B or the OWASP Security Culture material, since the talk surveys the framework rather than extending it.

## Verdict
**6/10**: A beginner-level model explains why different security barriers call for different support; the self-assessment remains a project resource rather than a worked team intervention.

**Reach broad**: Developers, tech leads and architects can use the barrier-first questions in their own teams' security discussions.

**Novelty 1/2**

- **+** [02:42](https://youtu.be/qrtd6svRUnk?t=162) The speaker brings behavioral science into software-team security through his OWASP Security Culture project work.
- **·** [18:42](https://youtu.be/qrtd6svRUnk?t=1122) The six-pattern overview presents the project's framework without an account of applying and revising it in a particular team.

**Demonstrated 1/2**

- **·** [14:19](https://youtu.be/qrtd6svRUnk?t=859) This security-culture talk teaches a diagnostic conversation and has no central claim that needs running software.

**Measured 1/2**

- **·** [03:46](https://youtu.be/qrtd6svRUnk?t=226) Training completion followed by recurring incidents is an illustrative scenario, with no quantitative effectiveness claim needing a measurement.

**Depth 2/2**

- **+** [20:47](https://youtu.be/qrtd6svRUnk?t=1247) The skeptic's distrust explains why evidence of costs fits the motivational barrier while more awareness training misses it.
- **+** [26:36](https://youtu.be/qrtd6svRUnk?t=1596) Treating resistance as feedback and involving developers in control design explains how co-authorship can turn opposition into advocacy.
- **+** [35:43](https://youtu.be/qrtd6svRUnk?t=2143) Anonymous assessment and team-level patterns address the trust risk created when diagnostic information becomes hiring or performance-review data.

**Reusable 1/2**

- **+** [40:55](https://youtu.be/qrtd6svRUnk?t=2455) The final slide points to the SECUR-E diagnostic self-assessment through a QR code.
- **·** [38:23](https://youtu.be/qrtd6svRUnk?t=2303) The assessment is the presented project's own tool, still being validated, rather than a separate worked example reproducing a team's diagnosis and intervention.
