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
**6/10**: A diagnose-then-match framework that gives each of six developer patterns a COM-B reason for its wrong and right intervention, with a live self-assessment behind the QR code; the interventions themselves are described in speech for the audience to reconstruct.

**Novelty 1/2**

- **+** [18:42](https://youtu.be/qrtd6svRUnk?t=1122) The six-pattern taxonomy with per-pattern COM-B profiles and matched interventions comes from the speaker's own OWASP project work.
- **·** [11:06](https://youtu.be/qrtd6svRUnk?t=666) COM-B itself is established behavioral science, credited as such rather than presented as new.

**Demonstrated 1/2**

- **·** [38:23](https://youtu.be/qrtd6svRUnk?t=2303) A strategy talk about matching interventions to behavioral barriers has nothing to run on screen; the self-assessment tool appears only as a QR code.

**Measured 1/2**

- **·** [03:46](https://youtu.be/qrtd6svRUnk?t=226) The full-completion-yet-same-incidents story is told without numbers, and no claim in the talk needs one.

**Depth 2/2**

- **+** [20:16](https://youtu.be/qrtd6svRUnk?t=1216) Each of the six patterns gets its COM-B diagnosis plus the wrong intervention and the right one, for example the skeptic's low motivation from distrust calls for evidence of late-fix costs, not fear or training.
- **+** [29:19](https://youtu.be/qrtd6svRUnk?t=1759) One training intervention is traced across the team: it helps the unaware developer, backfires for the resistant one and annoys the skeptic.
- **−** [32:29](https://youtu.be/qrtd6svRUnk?t=1949) The one-budget trade-off between a quick win and the most productive team-wide impact is posed as a question, with no way to choose given.

**Reusable 1/2**

- **+** [40:55](https://youtu.be/qrtd6svRUnk?t=2455) The closing QR code leads to a live SECUR-E developer self-assessment form.
- **−** [31:25](https://youtu.be/qrtd6svRUnk?t=1885) The matched supports per pattern are listed only in speech, and the tool is still in validation ([38:23](https://youtu.be/qrtd6svRUnk?t=2303)), so the practices must be reconstructed from the talk.
