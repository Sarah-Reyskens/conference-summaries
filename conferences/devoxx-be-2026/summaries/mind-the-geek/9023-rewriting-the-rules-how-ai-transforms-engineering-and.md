---
title: "Rewriting the rules: How AI transforms engineering and inspiring young minds"
talkId: "9023"
conference: devoxx-be-2026
speakers: [Ayoub Hammou Ahabchane, Kamel Zaraoui]
track: Mind the Geek
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=eSSPOCeoF0c
durationMin: 51
slides: null
verdict: 5
reach: segment
frames: 10
reviewedAt: 2026-10-15
---

# Rewriting the rules: How AI transforms engineering and inspiring young minds
Ayoub Hammou Ahabchane, Kamel Zaraoui · Conference · Mind the Geek

## TL;DR
Two ING Belgium engineers describe how a regulated global bank rolled out AI to its engineers and demo the two learning platforms they built with AI for Devoxx4Kids workshops. The thesis is that AI changes engineering from writing code to specifying intent and reviewing output, while the engineer keeps ownership of what ships.

## Key takeaways
- Rolling out AI in a bank means satisfying regulators, protecting customer trust, and living with mainframes and COBOL; ING sequenced training, a sharing community, and a dedicated AI department before broad agent access.
- ING tracks license engagement in three tiers (active, engaged, dedicated) so paid licenses go to engineers who actually use them.
- The highest-value internal agents target toil: vulnerability triage across scanners, framework migration scans, and scaffolded frontend components that follow the bank's visual identity.
- A backend-only engineer built a full kids' coding platform with Lovable in hours, including an AI-trainer game and a Space Invader easter egg unlocked by a password.
- AI-generated code needs a product owner: the CodeKids Lab duplicated translations in every class instead of centralizing them, which a reviewer caught.
- The working loop the speakers recommend is specify with context and acceptance criteria, let AI generate, then review and test as if you wrote it yourself.

## Notes

### [02:08](https://youtu.be/eSSPOCeoF0c?t=128) A testimonial in three parts
Ahabchane frames the session as a testimonial: how ING adopted AI, what the engineer of tomorrow looks like, and two pet projects built with AI. ING's constraints are regulation (it answers to the national bank) and global scale, which lets one strategy serve nine countries.

### [10:24](https://youtu.be/eSSPOCeoF0c?t=624) Why a bank invests in AI despite the constraints
Challenges: regulation, customer trust, a legacy landscape with mainframes and COBOL, and operational risk such as hallucinations in customer answers. Reasons to invest: productivity, customer experience (one agent swept all repositories for European Accessibility Act gaps), broader-informed decisions, compliance coverage across some 2,200 APIs, and competitive innovation.

### [15:40](https://youtu.be/eSSPOCeoF0c?t=940) The ING adoption timeline
ING skipped the 2022 prompting wave for regulatory reasons. Three engineers trained a week in the Netherlands in March 2025; 180 employees held licenses by May; a sharing community followed in July; an AI-dedicated department opened in January; the group-wide agentic hub of reviewed agents and skills opened in February. Dashboards track active, engaged, and dedicated users.

### [18:47](https://youtu.be/eSSPOCeoF0c?t=1127) Where adoption stands now
All colleagues have M365 Copilot web access, over 4,000 hold M365 licenses with 85% actively using them, and the group holds 8,500-plus GitHub Copilot licenses, doubled in Belgium over the last year. New "nanites" route a request to the right guideline-compliant agent. Engineers get two full days of AI training; the AI department holds a 400-plus-item improvement backlog.

### [21:55](https://youtu.be/eSSPOCeoF0c?t=1315) Three agents: vulnerabilities, API SDK, frontend toolkit
The transversal agent runs three scanners (Prisma base-image, Checkmarx One, GSOC platform overview), proposes version pins or alternatives per CVE, and checks whether an unfixable vulnerability is actually reachable. The backend agent scans code against the API SDK framework's 33 releases and migration guides before upgrades. A sped-up recording shows the frontend toolkit agent turning an empty repo into a three-screen complaint form with tests and Storybook. ING counts 100 to 150 agents, split between validated global ones and an experimental playground.

### [29:45](https://youtu.be/eSSPOCeoF0c?t=1785) Devoxx4Kids: the other stage
Zaraoui presents Devoxx4Kids, volunteer-run workshops for ages 7 to 14 where the two are workshop leads: code is the tool, confidence and curiosity the outcome. Both labs below were built for these workshops.

### [32:57](https://youtu.be/eSSPOCeoF0c?t=1977) CodeKids Lab, built with Lovable
Ahabchane demos codekidslab.lovable.app live: concept cards (program as recipe, variable as labelled box) gate games in a 1-to-2-hour format. Games include a Mastermind rebuilt in two hours with AI, a Caesar cipher, an animated bubble sort, an AI trainer where kids fit "multiply by two and add five" from examples, and a password-unlocked Space Invader. Every class carries its own translations, the talk's example of AI missing product vision.

### [39:40](https://youtu.be/eSSPOCeoF0c?t=2380) CyberQuest, built with Claude Code
Zaraoui demos his security workshop site, built alone in two to three weeks on one Claude Code subscription. Kids accept fake terms, "log in" with social buttons, and watch their typed password travel, opening the lesson on privacy and password strength; nothing is stored anywhere. A backend version meant to demo captive-portal Wi-Fi risks failed to start live.

### [44:54](https://youtu.be/eSSPOCeoF0c?t=2694) The engineer stays in the driver's seat
AI brings speed and alternatives beyond one engineer's experience, but lacks business context and product vision. Success factors: context that sets the scene, rules pinning the stack and standards, and testing against the original acceptance criteria. Engineers move from writing code to a specify, generate, review loop.

## Tools, libraries and specs
- GitHub Copilot (8,500+ group licenses)
- Microsoft 365 Copilot (4,000+ licenses in Belgium, 85% active)
- Lovable (CodeKids Lab scaffold and hosting)
- Claude Code (CyberQuest build)
- Prisma Vulnerability Scanner, Checkmarx One, GSOC platform (the three scanners behind the vulnerability agent)
- API SDK v33 (ING internal backend framework on Spring Boot)
- Nanites and the agentic hub (ING internal agent routing and shared prompt/skill library)

## Who should watch
Engineers curious how AI adoption works inside a regulated enterprise, and anyone running kids' coding or security workshops who wants worked examples to imitate. Skip it if you want agent internals, prompt engineering technique, or measured productivity data; the agents are shown by what they do, not how they are built.

## Verdict
**5/10**: An enterprise-adoption testimonial with live kids'-lab demos, limited by internal agents that are described but not run and by self-reported numbers.

**Reach segment**: Tech leads and teams rolling out AI coding assistants in large or regulated organisations, and Devoxx4Kids or school workshop volunteers, can use the main content; most of the audience gets only the closing specify, generate, review loop.

**Novelty 1/2**

- **+** [15:40](https://youtu.be/eSSPOCeoF0c?t=940) The dated ING rollout sequence (three engineers trained in March 2025, 180 licenses by May, a sharing community, a dedicated AI department, a group-wide agentic hub) is first-hand organizational experience no search gives.
- **+** [32:57](https://youtu.be/eSSPOCeoF0c?t=1977) Kickstarting a full kids' coding platform with Lovable as a spare-time pet project is the speakers' own build experience.
- **−** The closing guidance (set context and rules, test the output) matches GitHub's "Best practices for using GitHub Copilot" docs page.

**Demonstrated 1/2**

- **+** [27:09](https://youtu.be/eSSPOCeoF0c?t=1629) A sped-up recording takes the frontend-toolkit agent from an empty repo through wizard questions to generated files and form screens.
- **+** [41:16](https://youtu.be/eSSPOCeoF0c?t=2476) CyberQuest runs live: a typed password visibly travels after fake terms and social login, opening the privacy lesson.
- **−** [43:20](https://youtu.be/eSSPOCeoF0c?t=2600) The captive-portal backend version fails to start live, and the API SDK agent (docs pages only) and the vulnerability and accessibility agents (described only) never run on screen.

**Measured 1/2**

- **+** [19:19](https://youtu.be/eSSPOCeoF0c?t=1159) License adoption is stated as 4,000-plus M365 licenses at 85% active use and 8,500-plus group GitHub Copilot licenses.
- **+** [34:34](https://youtu.be/eSSPOCeoF0c?t=2074) A Mastermind that took two months as a student was rebuilt with AI in two hours, a self-reported comparison with no method.
- **−** [17:43](https://youtu.be/eSSPOCeoF0c?t=1063) The engagement graphs are shown blurred, so the active, engaged and dedicated tiers have no visible baseline or method.

**Depth 1/2**

- **+** [48:05](https://youtu.be/eSSPOCeoF0c?t=2885) The specify, generate, review loop gives beginners a clear mental model of where engineers add value with agents.
- **+** [37:07](https://youtu.be/eSSPOCeoF0c?t=2227) The code inspection shows translations duplicated in every class, a worked example of AI output missing product vision.

**Reusable 1/2**

- **+** [50:39](https://youtu.be/eSSPOCeoF0c?t=3039) The closing slide links both live labs by QR code, so workshop leaders can run them with kids straight away.
- **−** [42:50](https://youtu.be/eSSPOCeoF0c?t=2570) No repository or configuration is published, as sharing the code is promised for later and the ING agents stay internal.
