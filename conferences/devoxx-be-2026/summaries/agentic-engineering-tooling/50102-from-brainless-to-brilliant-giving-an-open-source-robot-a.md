---
title: From Brainless to Brilliant — Giving an Open-Source Robot a Mind of Its Own
talkId: "50102"
conference: devoxx-be-2026
speakers: [Jan Van Wassenhove]
track: Agentic Engineering & Tooling
sessionType: Keynote
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=ZDocIlx7Zvg
durationMin: 17
slides: null
verdict: 7
frames: 7
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# From Brainless to Brilliant — Giving an Open-Source Robot a Mind of Its Own

Jan Van Wassenhove · Keynote · Agentic Engineering & Tooling

## TL;DR

Van Wassenhove assembled a €300 open-source Reachy Mini on his kitchen table and wrote it a "brain", AURA, that runs on a laptop: face recognition, per-person memory, mode-gated access, and an agentic loop that edits code and proposes improvements behind human approval. The keynote argues cheap hardware plus accessible AI moves the floor, not just the ceiling.

## Key takeaways

- Keep the robot empty: run every model on a laptop so a stolen device leaks only motors and servos.
- Separate told facts from learned memories per person; retain only provided facts about minors.
- Gate capabilities by mode so a question in the wrong context gets refused.
- Put every action that leaves the box behind an approval gate, and require a human to accept self-proposed changes.

## Notes

### [01:39](https://youtu.be/ZDocIlx7Zvg?t=99) A €300 robot, one screwdriver

The Reachy Mini (Hugging Face plus Pollen Robotics) ships brainless. Van Wassenhove, no roboticist, assembled it in one evening from a Lego-style guide, versus a ~€40,000 robot mentioned on stage.

### [04:45](https://youtu.be/ZDocIlx7Zvg?t=285) A day with Richie

The laptop-side AURA UI recognizes stand-in colleague Mila by face and greets her; her son Luca is recognized but, as a minor, nothing is memorized beyond provided facts. Asked for the work agenda in home mode, the brain refuses. Later the agent opens VS Code, merges per-skill API calls into one, runs tests green, then asks "Can I commit everything?" and is refused. After 15 briefings with the weather and news always skipped, it drafts an improved briefing; the UI offers Apply rewrite, Edit first, No thanks, and nothing changes without agreement. A QR code and URL point to the speaker's playable physics game "Please Do Not Throw Richie".

### [13:02](https://youtu.be/ZDocIlx7Zvg?t=782) The floor is moving

Sub-€500 robots push the floor down as fast as AI pushes the ceiling up. Architecture and agentic loops are deferred to the noon talk "I Hired a Real Robot as My Junior Dev" (Room 6).

## Tools, libraries and specs

- Reachy Mini (Hugging Face + Pollen Robotics), ~€300 open robot platform
- AURA, the speaker's own laptop-side robot brain; VS Code as the agent's editor

## Who should watch

Beginners curious what a home robotics-plus-AI build looks like end to end. Skip it for internals; those wait for the speaker's noon talk.

## Verdict

**7/10**: Recorded AURA console runs show recognition, mode-gated refusal, code edits and self-proposed changes behind approval gates, each guardrail with a stated reason, but the numbers stay price and count anecdotes and the AURA project itself is never pointed to.

**Novelty 1/2**

- **+** [03:43](https://youtu.be/ZDocIlx7Zvg?t=223) The empty robot plus encrypted laptop brain is the speaker's own AURA build.
- **−** The approval gates and propose-instead-of-apply changes repeat the human-in-the-loop agent pattern in LangGraph's human-in-the-loop docs.

**Demonstrated 2/2**

- **+** [05:05](https://youtu.be/ZDocIlx7Zvg?t=305) The recorded AURA console shows Mila recognized with a confidence label and PersonRecognized entries in the event feed.
- **+** [08:10](https://youtu.be/ZDocIlx7Zvg?t=490) The refusal to read the work calendar in home mode appears as the console's own reply text.
- **+** [09:35](https://youtu.be/ZDocIlx7Zvg?t=575) The console shows the green pytest result and then the "May I run this command?" card over the git commit, with Allow and Deny buttons.

**Measured 1/2**

- **+** [13:02](https://youtu.be/ZDocIlx7Zvg?t=782) The €300 Reachy Mini is set against a robot the speaker heard costs about €40,000, a price comparison whose baseline is hearsay.
- **−** [10:29](https://youtu.be/ZDocIlx7Zvg?t=629) The "15 times in a row" behind the briefing rewrite is self-reported, with no log shown.
- **−** [12:01](https://youtu.be/ZDocIlx7Zvg?t=721) "A couple of hundreds of agents behind the scenes" is a system-scale count with no method.

**Depth 2/2**

- **+** [03:43](https://youtu.be/ZDocIlx7Zvg?t=223) Nothing stays on the robot, so a stolen device leaks only motors and servos.
- **+** [06:21](https://youtu.be/ZDocIlx7Zvg?t=381) Minors are tagged so the brain keeps only the facts the owner provided and memorizes nothing from conversations with them.
- **+** [09:58](https://youtu.be/ZDocIlx7Zvg?t=598) An unguarded agent finds an excuse to run what was forbidden, so everything leaving the box passes a gate.

**Reusable 1/2**

- **+** [15:08](https://youtu.be/ZDocIlx7Zvg?t=908) A QR code and URL open the published physics game "Please Do Not Throw Richie", an artifact unrelated to AURA's content.
- **−** [03:43](https://youtu.be/ZDocIlx7Zvg?t=223) The talk gives no repository, install path or URL for AURA itself.
