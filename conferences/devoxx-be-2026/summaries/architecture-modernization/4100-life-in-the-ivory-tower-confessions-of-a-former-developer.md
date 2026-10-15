---
title: "Life in the Ivory Tower: Confessions of a Former Developer Who Turned Into an Architect"
talkId: "4100"
conference: devoxx-be-2026
speakers: [Robin Custers]
track: Architecture & Modernization
sessionType: Lunch Talk
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=nhVRKv8VHKU
durationMin: 35
slides: null
verdict: 5
frames: 7
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Life in the Ivory Tower: Confessions of a Former Developer Who Turned Into an Architect

Robin Custers · Lunch Talk · Architecture & Modernization

## TL;DR

A developer turned enterprise architect at a government organization tells how he talked the CIO out of a one-size-fits-all Salesforce rollout by diagnosing the organization's operating model, and shares the governance habits that followed. The thread across every story: architects earn their place by translating between business goals and delivery reality, starting change small, and staying technical enough to keep credibility.

## Key takeaways

- When someone proposes one central system for every department, check the operating model first: departments with different processes and shared data need per-department solutions, not a single platform.
- Argue technology choices in the language of the person deciding: the CIO was convinced by an organization-fit model, not by technical objections to Salesforce.
- Connect corporate strategy to team decisions with three habits: architecture principles, recurring advisory forums with architects and team leads, and decision records kept visible to everyone.
- Treat standards as best practices with documented deviations: a Java and Angular default survived a Python AI proof of concept because the exception went into a decision record.
- Start organizational change as a small experiment with a limited blast radius: one person, one platform capability, one consuming application, rolled out only after it proved itself.

## Notes

### [01:06](https://youtu.be/nhVRKv8VHKU?t=66) A tractor, a parking brake, and a new architect

Custers opens with his old tractor, which he failed to dig out of the mud for a full day before noticing he had left the parking brake on. He draws the parallel to starting as an enterprise architect in a government organization with no prior experience in the role. His first week brought an email asking him to inspect a broken window (wrong kind of architect) and a CIO presenting a consultant-built IT strategy: principles such as reuse over buy over build, privacy and security by design, and cost/risk-based decisions, plus a roadmap calling for better reporting, security and compliance, data quality, and efficiency.

### [07:19](https://youtu.be/nhVRKv8VHKU?t=439) "Can't we do it all with one central solution?"

The CIO noticed that every department's system looked alike: the prisons department, the family-violence department, and law enforcement all stored client data, sent notifications, processed documents, and integrated with outside systems. The consultants still on site pitched Salesforce as the system checking every box: CRM for client data, marketing for notifications, platform for integrations, data for documents, analytics and commerce for the roadmap goals. It also complied with every IT principle, and objections about fit were waved away with low code (today, he notes, the answer would be AI agents).

### [12:31](https://youtu.be/nhVRKv8VHKU?t=751) An operating model for IT decisions

From *Enterprise Architecture as Strategy*, Custers takes a model plotting organizations on business-process standardization against business-process integration. The four quadrants get examples: McDonald's (same process everywhere, little data sharing), airlines (same check-in process, heavy data exchange), Sony (different products, different customers, no sharing), and coordination (different processes, valuable data exchange). His organization sat in coordination: prison work differs from family-violence work, but all departments deal with people touching the law, so exchanging that data matters. That placement meant per-department solutions with sharing limited to non-core concerns like security and infrastructure, and once the CIO followed the reasoning, Salesforce was off the table.

### [18:14](https://youtu.be/nhVRKv8VHKU?t=1094) James Watt and the translator role

James Watt failed to sell mine owners a steam engine on piston sizes until he asked what they wanted to know (horses saved) and invented horsepower. Custers presents this as the architect's most valuable position: a translator between what the organization wants and the IT delivery side.

### [19:47](https://youtu.be/nhVRKv8VHKU?t=1187) Governance without blocking

Rhyming corporate strategy (data-driven, cheaper, secure, compliant) with team decisions (buy vs build, API contracts) rests on three ingredients from *Facilitating Software Architecture*: architecture principles for direction, architecture advisory forums for recurring discussion with architects and team leads, and architectural decision records kept open so everyone sees each decision. Standardization gets the same pragmatic treatment: he set Java and Angular as the default stack for custom applications but let a short-lived AI proof of concept use Python, recording the deviation in a decision record. AI agents and shared AI skills, he adds, can help teams keep making that strategy-to-decision bridge.

### [25:28](https://youtu.be/nhVRKv8VHKU?t=1528) Platform ambitions meet Larman's Laws

Seeing real duplication in security and compliance code across systems, Custers prepared a central-platform proposal mapped to team topologies, booked a two-hour meeting, and was rejected five minutes in as too much change. He answers with Larman's Laws of Organizational Behavior: organizations are optimized to avoid change, change initiatives reinforce the status quo, imposed change kills morale, change agents don't work, culture follows structure. The restart framed the platform as an experiment with a limited blast radius (one person, one capability, one application), expanding only after success.

### [29:43](https://youtu.be/nhVRKv8VHKU?t=1783) Should architects still code?

As a student in 2000, Custers wrote his father a Java 1.3 application optimizing steel-cutting layouts; it ran unnoticed on a second office PC for 25 years until the machine died. He rebuilt it over a weekend with AI agents in Java and React, showing screenshots of the MaterialWise app: steel profiles with trading lengths, construction projects, cutting-size lists, order and waste calculations, plus a shopping-cart icon and Excel export the agents added unprompted. Pet projects like this keep him current enough to avoid claims like "Salesforce solves everything", while he stays honest about what he doesn't know and leans on peers and network for the rest.

### [33:59](https://youtu.be/nhVRKv8VHKU?t=2039) Wrap-up

Translate between business and technology, start small and experiment before scaling, stay technical and admit the gaps. Technical decisions, he closes, are often business decisions in disguise.

## Tools, libraries and specs

- Salesforce (CRM, marketing, platform, data, analytics, commerce modules)
- Java + Angular (default stack for custom applications); Java 1.3 (original 2000 steel-cutting app)
- Python (AI proof of concept); Jython (mentioned as a suggestion from Gemini, not used); React (rebuilt app frontend)
- Books: *Enterprise Architecture as Strategy* (Ross, Weill, Robertson); *Facilitating Software Architecture* (Andrew Harmel-Law); Larman's Laws of Organizational Behavior (Craig Larman); *Team Topologies* (mentioned in passing)

## Who should watch

Developers moving toward architecture or working with architects gain the most, especially anyone in or around government and enterprise IT. Viewers wanting Salesforce evaluations, platform engineering internals, or AI-agent implementation detail should look elsewhere.

## Verdict

**5/10**: A practitioner story that applies published frameworks to the speaker's own decisions, limited by anecdotal evidence and nothing to take home.

**Novelty 1/2**

- **+** [07:19](https://youtu.be/nhVRKv8VHKU?t=439) The CIO's "one central solution" question and the consultants' module-by-module Salesforce pitch come from the speaker's own first weeks in a government organization.
- **+** [17:12](https://youtu.be/nhVRKv8VHKU?t=1032) Placing that organization in the operating model's coordination quadrant, and using it to take Salesforce off the table, applies the framework to a case no source already covers.
- **·** [12:31](https://youtu.be/nhVRKv8VHKU?t=751) The operating model comes from *Enterprise Architecture as Strategy* and the change laws from Craig Larman, both credited published sources.

**Demonstrated 1/2**

- **·** [31:50](https://youtu.be/nhVRKv8VHKU?t=1910) A strategy and culture talk with nothing central to run; the nearest thing to a demo is screenshots of the rebuilt steel-cutting app, shown to make a point about staying technical.

**Measured 1/2**

- **·** [31:18](https://youtu.be/nhVRKv8VHKU?t=1878) The talk makes no outcome claim that needs a number; its figures (a 25-year-old app, a two-hour meeting cut short after five minutes, one person with one capability in one app) are story details, and "I never had an incident, never had a bug" is a self-reported punchline with no baseline.

**Depth 1/2**

- **+** [16:42](https://youtu.be/nhVRKv8VHKU?t=1002) The four operating-model quadrants are explained with worked examples (McDonald's, airlines, Sony), and the coordination quadrant's rule against one central solution carries its reason: different business processes would put "a lot of complexity in this one central solution".
- **+** [21:19](https://youtu.be/nhVRKv8VHKU?t=1279) The governance bridge names its three mechanisms and what each carries: principles give direction, forums give discussion, public decision records give visibility.
- **−** [17:44](https://youtu.be/nhVRKv8VHKU?t=1064) Salesforce is argued down on organization fit "not in technical language on what Salesforce could do or not do", after the speaker says he was unsure it could support the departments' processes, so the alternative is never weighed on capability.

**Reusable 1/2**

- **+** [21:19](https://youtu.be/nhVRKv8VHKU?t=1279) The principles, advisory forum and public decision-record trio is described plainly enough to copy into another organization.
- **+** [24:26](https://youtu.be/nhVRKv8VHKU?t=1466) The standardization rule (Java and Angular as the default for custom applications, deviations recorded in decision records, integration standardized rather than IDEs) is stated in a form another team could adopt.
- **−** [21:19](https://youtu.be/nhVRKv8VHKU?t=1279) No template, checklist or repository backs any of the practices.
