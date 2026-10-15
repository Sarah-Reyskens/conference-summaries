---
title: How to survive and thrive as a dev (team) in the exponential age of AI. Real-world AI adoption, smarter ways of working, and lessons from the front lines
talkId: "7008"
conference: devoxx-be-2026
speakers: [Sander Hoogendoorn]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=BLBwQpczk7M
durationMin: 52
slides: null
verdict: 5
frames: 8
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---
# How to survive and thrive as a dev (team) in the exponential age of AI. Real-world AI adoption, smarter ways of working, and lessons from the front lines
Sander Hoogendoorn · Conference · Agentic Engineering & Tooling

## TL;DR
Sander Hoogendoorn, CTO of the e-commerce company iBOOD, describes how his 13-person tech team works in the AI era: seven habits covering prioritization, complexity, autonomy, learning, microteams, continuous delivery, and fun. AI multiplies output, so the bottleneck moves to choosing the right work, shortening feedback loops, and removing process that slows teams down.

## Key takeaways
- Spend capacity against a stated dot on the horizon with a fixed split (his team uses 70% strategic bets, 20% improvements to existing systems, 10% small requests), and park the rest in a someday-maybe list that nobody revisits.
- Treat software work as complex or chaotic in the Cynefin sense, which means progress comes from small experiments run in tiny steps, not from plans that assume the answer is known.
- Remove rules instead of adding them: no sprints, no story points, no branches, no pull requests, no code reviews, with quality carried by pairing, shared ownership, and automation.
- Release many times a day so feedback arrives in minutes; his team pushes to production about 100 times a day with 13 people.
- Keep architectural knowledge explicit (uniform service architecture, templated pipelines, coding skills for the AI tools) because that knowledge is what lets developers judge AI-generated code.

## Notes
### [01:37](https://youtu.be/BLBwQpczk7M?t=97) Technical death at iBOOD
Hoogendoorn joined iBOOD six years ago to find a company grown from one deal on a web page managed in Excel into a tangle of modified open-source ERP, CMS, CRM, and product-information systems with customer data synced everywhere. He calls the end state technical death: everyone in tech is consumed keeping systems alive and nobody can innovate. The root cause, he argues, sits in the organization rather than the tech: competing stakeholders each push their own priorities, and business and developers speak different languages.

### [05:44](https://youtu.be/BLBwQpczk7M?t=344) A sales page rebuilt in two hours without writing code
Two days before the talk, the speaker rebuilt a whole internal sales page, menu, charts and all, in two hours without writing a line of code, and built the presentation tool he is presenting from in a day. These screenshots open the talk's question: with output this cheap, the problem is no longer whether developers keep their jobs but how a team aims that output. He runs up to eight agent sessions in parallel and reports the context switching leaves everyone on the team exhausted by evening.

### [09:18](https://youtu.be/BLBwQpczk7M?t=558) Habit 1: prioritize against a dot on the horizon
Because the team cannot do everything asked of it, iBOOD set a company direction (becoming a multi-country deal site, which implies multiple currencies, languages, and delivery setups) and splits capacity 70/20/10 across strategic work, existing-system improvements, and small requests. Anyone can pitch ideas onto a board; a group filters them with four questions (does it serve the goals, is it actionable, is it small enough, is it the most important thing), and rejects land in a someday-maybe column that functions as a waste bin.

### [15:01](https://youtu.be/BLBwQpczk7M?t=901) Habit 2: complexity, experiments, tiny steps
The Cynefin framework sorts problems into clear, complicated, complex, and chaotic; software lives on the complex and chaotic side, where no good practice exists yet and innovation is the way out. Innovation requires experiments, and an experiment must be allowed to fail, otherwise it is a search for certainty. The escape is tiny steps: start with one chart, check it works, then extend. He also introduces the talk's refrain, via Visa founder Dee Hock: simplify to amplify.

### [20:14](https://youtu.be/BLBwQpczk7M?t=1214) Habit 3: own the work through autonomy
Software is too complex for anyone to know all of it, so the team moved to a single TypeScript stack and collective ownership: anyone may push code into what anyone else was working on. Dee Hock's line anchors the habit, that simple purpose and principles produce intelligent behavior while complex rules produce stupid behavior. Team members pick their own work from the boards. Autonomy had to be learned; one developer who kept asking what to work on now negotiates scope and releases directly with the business.

### [26:55](https://youtu.be/BLBwQpczk7M?t=1615) Everything the team stopped doing
Citing Saint-Exupery (perfection is achieved when there is nothing left to take away), Hoogendoorn lists what the team dropped: Scrum, sprints, retrospectives, a Scrum Master, product owners, stories, estimates, branches, pull requests, code reviews, and blame. Standups survive, except on Thursdays when everyone is in the office. About half the team has since built a personal IDE tuned to their own AI workflow, and they compare notes on the designs.

### [30:34](https://youtu.be/BLBwQpczk7M?t=1834) Habit 4: share knowledge and keep the foundation solid
Knowledge sharing runs on standups, event storming with the business, voluntary pair programming, Thursday in-office sessions for hard problems, and a Tuesday lean-coffee hour (the voting app for it was rebuilt in-house in 90 minutes). A uniform service architecture, templated pipelines, and infrastructure as code mean the team never looks at Kubernetes, and that foundation speeds up AI work. Team knowledge goes into Claude skills, including a push-back skill that stops the model from folding when challenged; the speaker shows a test file the model wrote in his own style.

### [34:41](https://youtu.be/BLBwQpczk7M?t=2081) Habit 5: microteams that form and dissolve daily
Work runs in small ad-hoc groups: somebody picks an item from a board, someone else joins, they talk to the business, build, and usually check in before the end of the day, then regroup differently the next day. Photos of shifting two- and three-person combinations illustrate the pattern. The constant remixing spreads knowledge wider than fixed teams, and the small scope keeps each cycle short enough for fast feedback.

### [36:14](https://youtu.be/BLBwQpczk7M?t=2174) Habit 6: deliver continuously, not in sprints
Sprints are mini-projects that fail in familiar ways (untested leftovers, slow progress, scope creep from the CEO) because progress is not linear, so the team stopped estimating story points entirely. Cycles shrank to hours: a buyer dashboard fix went from a chat request into the pipeline in about 15 minutes. Invoking Jason Gorman's missing-the-bus analogy and Deming on building quality in, he reports roughly 100 production releases a day, trunk-based development, fully automated tests and pipelines, AI-assisted pipeline repair, and testing in production.

### [46:04](https://youtu.be/BLBwQpczk7M?t=2764) Habit 7: fun, Drive, and personal software
The closing habit draws on Dan Pink's Drive: purpose, mastery, and self-direction, which the speaker says the team adopted without aiming at the model, to the point where he manages nothing and on-call issues get picked up voluntarily. Looking ahead, he sees an ecosystem of personal software: own IDEs, a personal assistant, the presentation tool, and iBox, a sandbox exposing limited APIs so business users can build and deploy their own dashboards. The talk ends with Gorman's swimmer quote and a plea to take your mother out to dinner.

## Tools, libraries and specs
- TypeScript (the team's single stack)
- Claude (coding agent; team knowledge captured as skills)
- Kubernetes (runs untouched under the templated pipelines)
- SonarQube (issues triaged toward AI-assisted repair)
- Jira (idea boards), Slack (the 10% request channel)
- JetBrains WebStorm / IntelliJ IDEA (still in daily use alongside self-built IDEs)

## Who should watch
Engineering leads and senior developers rethinking team process around AI coding tools gain the most, especially those weighing trunk-based development, dropping pull requests, or prioritization without estimation. Teams wanting measured before/after evidence or a reusable playbook can skip it; the talk reports one company's practices without baselines or published artifacts.

## Verdict
**5/10**: one team's operating model for the AI era, specific and first-hand, but it leans on credited frameworks, reports its numbers without baselines and publishes no artifact.

**Novelty 1/2**

- **+** [29:00](https://youtu.be/BLBwQpczk7M?t=1740) Half the team built personal IDEs matched to their own agent workflows, the speaker's own in two days, which goes past generic AI-coding advice.
- **+** [49:10](https://youtu.be/BLBwQpczk7M?t=2950) The iBox sandbox lets business users build and deploy their own dashboards on a limited set of company APIs, reported from the speaker's own company.
- **·** [16:34](https://youtu.be/BLBwQpczk7M?t=994) The habits are built on credited published material (Cynefin, Hock, Deming, Gorman, Pink) plus one team's account, and the IDE and iBox examples come without results.

**Demonstrated 1/2**

- **+** [05:44](https://youtu.be/BLBwQpczk7M?t=344) Screenshots show the sales page rebuilt in two hours, grounding the headline claim in visible output.
- **+** [48:40](https://youtu.be/BLBwQpczk7M?t=2920) The speaker presents from a presentation tool he built two weeks earlier with AI, so one built artifact is in use on stage.
- **·** [41:55](https://youtu.be/BLBwQpczk7M?t=2515) The central claim is a team operating model with nothing to run, so no end-to-end live run is fairly asked for.

**Measured 1/2**

- **+** [41:55](https://youtu.be/BLBwQpczk7M?t=2515) The team releases to production about 100 times a day with 13 people.
- **+** [05:44](https://youtu.be/BLBwQpczk7M?t=344) The sales-page rebuild took two hours with no handwritten code.
- **−** [41:55](https://youtu.be/BLBwQpczk7M?t=2515) The numbers are self-reported totals with no baseline, method, or trend, so they read as anecdotes rather than measurements.

**Depth 1/2**

- **+** [43:00](https://youtu.be/BLBwQpczk7M?t=2580) Dropping pull requests and reviews is argued through: late, context-switched reviewers check formatting, so quality moves into pairing plus automation.
- **+** [15:32](https://youtu.be/BLBwQpczk7M?t=932) The Cynefin framing explains why tiny-step experiments fit complex work instead of just asserting it.
- **−** [41:24](https://youtu.be/BLBwQpczk7M?t=2484) Regulated environments are answered with the prediction that "the AI is going to understand" the regulations, so the trade-off of releasing fast there is not weighed.

**Reusable 1/2**

- **+** [12:25](https://youtu.be/BLBwQpczk7M?t=745) The 70/20/10 split, the four board questions, and the someday-maybe column are described precisely enough to copy.
- **+** [33:07](https://youtu.be/BLBwQpczk7M?t=1987) The push-back skill's opening rule is quoted ("do not immediately fold apologize or agree with them"), a starting point for a similar skill.
- **−** [29:00](https://youtu.be/BLBwQpczk7M?t=1740) The self-built IDEs, presentation tool, and iBox are shown but not published, leaving no artifact covering the talk's main content.
