---
title: The Devoxx Robot Games
talkId: "52103"
conference: devoxx-be-2026
speakers: [Stephan Janssen]
track: Mind the Geek
sessionType: Lunch Talk
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=NT0wyPM58G8
durationMin: 41
slides: null
verdict: 8
frames: 8
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# The Devoxx Robot Games
Stephan Janssen · Lunch Talk · Mind the Geek

## TL;DR
Nine developers each take four minutes to demo an AI-assisted game built for Devoxx's Robot Games challenge, all starring the conference robots Voxy, Droid and Biggy. Every demo pairs live gameplay with the build story: which AI tools did the work, what had to be fixed by hand, and how long it took. The audience is asked to play the games and vote for a favorite.

## Key takeaways
- A playable game is reachable in days or even hours with AI assistance: one builder shipped in 13 hours after a first version appeared in one hour, another found the contest four days before the deadline.
- Describe levels and sprites to the model and import the output instead of authoring them by hand: generated tile-map JSON drops into Phaser, and generated sprite frames import directly.
- When the model keeps misreading reference images, switch to words: room-by-room text descriptions plus a painted overlay showing every wrong wall beat photos, drone video and floor plans.
- Generated chiptune music works well through a tiny in-game sequencer: import a melody and chords, and let the model write arpeggios, bass and drums over the Web Audio API.
- Real Claude Code sub-agent activity can be visualized as a game world by emitting JSON from hooks and streaming it through a broker into Unreal.
- Human playtesting still decides whether the game is fun: daughters, train passengers and hallway volunteers supplied the feedback no model gave.

## Notes

### [00:34](https://youtu.be/NT0wyPM58G8?t=34) Intro: the competition
Stephan Janssen explains he built a game in three weeks, had so much fun he opened a competition, and nine or ten developers submitted entries. Each comes on stage for a four-minute demo; the audience can play every game and clone the repos.

### [01:04](https://youtu.be/NT0wyPM58G8?t=64) Night-before-Devoxx 3D puzzle game
The first builder shows a 3D puzzle game: the night before Devoxx, Stephan lost the venue key, and the three robots must cooperate to get in and prepare the keynote. Gameplay shows robots stacking to reach a high lever, opening doors, fetching tomato soup and carrying a crab sandwich without spilling. Twelve 2D proof-of-concept mechanics were prototyped before committing to 3D. For graphics, a "gauntlet loop" prompted the AI with a Cyberpunk screenshot as target: screenshot the game, compare, improve, repeat. Built with Claude.

### [04:41](https://youtu.be/NT0wyPM58G8?t=281) Hazenbach: a Heisenbug game in 13 hours
David built a game where the power is out ten minutes before the keynote and a random robot has a Heisenbug: a bug that vanishes when observed, diagnosed through on-screen logs. The AI researched the rules and venue material, chose plain JavaScript on canvas with no build and no dependencies, and estimated a full day; the first version was ready in one hour, leaving time for elevator music and Devoxx references (each robot idolizes a speaker: Josh Long, Dr. Venkat Subramaniam, Victor Rentea). Built with Claude Code (Opus) starting the day before the deadline; the trailer video is AI-made too.

### [08:24](https://youtu.be/NT0wyPM58G8?t=504) Devoxx Reboot: Phaser 3 arcade game
Antonio, not a game developer, built a 2D arcade game in four days: the robots restore conference power, each with a power (Voxy jumps high, Droid acts as a bridge and hacks terminals, Biggy throws teammates and pushes boxes). Built with Phaser 3. AI generated tile-map JSON importable into both Phaser and Tiled, generated sprite-frame JavaScript, wrote the follower AI including unsticking logic, and wrote a chiptune sequencer: the builder supplied melody and chords, the model added arpeggios, bass and drums played through the Web Audio API. A QR code offers the playable game.

### [12:08](https://youtu.be/NT0wyPM58G8?t=728) Overclocked: keep Devoxx running
Jessica demos Overclocked: guide the three robots to closing time without draining their batteries, across a five-day week (Monday to Friday) with an attendee-satisfaction meter. The on-screen instructions show charging bases, stairs between two floors, breakdowns and lost attendees. Under the hood it is one web page of plain JavaScript with zero dependencies; behavior emerges from simple per-attendee rules over shared flow fields, and tests read as user stories. Gemini supplied ideas like the espresso boost. Reference photos and plans kept producing wrong walls until the builder described the venue room by room in words and had the model paint its plan over the game so every error showed in yellow.

### [16:17](https://youtu.be/NT0wyPM58G8?t=977) Claude Code sub-agents visualized in Unreal
Daniel, on the Devoxx committee, visualizes his Claude Code sessions as the exhibition floor: an orchestrator at the reception desk spawns sub-agents that walk out, build booths, report back, then die in a graveyard whose stones record name, lifetime and tokens consumed. The demo follows a code-reviewer agent live and shows its task panel. It runs on real sessions: Code Hooks emit and update JSON per sub-agent, a broker reads the files and streams them into an Unreal client. Not a game, but a reusable view of everyday agent work.

### [20:03](https://youtu.be/NT0wyPM58G8?t=1203) Devoxx BBS: a 1990s text adventure
Martin's entry dials into a Kinepolis BBS over a simulated modem connection, complete with PCBoard v15.3 screens and a night bulletin carrying messages from Kristien, Droid and Stephan. An agent scraped the competition rules and co-built a configurable game template with per-robot settings. The game itself is a text adventure starring Voxy: fix the projector, clear popcorn from the aisles, and finish before Stephan arrives. Voxy teleports by flushing the toilet; Biggy sprays popcorn at attendees with unpaid invoices.

### [24:41](https://youtu.be/NT0wyPM58G8?t=1481) Beacon game, desktop and mobile
Richard, a loans developer who started the night before, shows a beacon-activation game built almost entirely with GitHub Copilot in VS Code, exhausting his personal token allowance. He plays the desktop version (activate three beacons against the clock) and a mobile variant rebuilt after his daughters reported the first version unplayable on phones. His point: hallway and train playtests supplied the arrows, hints and fixes the model never suggested, so the human stays in the loop. He also wrote the trailer music himself.

### [29:23](https://youtu.be/NT0wyPM58G8?t=1763) Please Do Not Throw Richie
This 3D entry stars Richie, a legless hopping robot that must cross the venue from the entrance to the opening keynote while Voxy throws him, Biggy hits him, guard droids eject him from wrong chairs, and security throws him out. The frame shows a Duke-themed sponsor booth on the exhibition floor. An 1800-line brief came from ChatGPT brainstorming; Codex with a GPT model built the hopping physics and route; Claude Code with Opus finished robots, venue and security; textures came from Claude and ChatGPT; the music is Sonic Pi code generated by an AI model. The stack is TypeScript, Three.js and Rapier physics on GitHub Pages as a PWA, with a two-player Tekken-style bonus mode (Runtime Rumble). Best run so far: about 90 seconds.

### [34:04](https://youtu.be/NT0wyPM58G8?t=2044) Ghost Light: Devoxx in 2126
The last builder, a Java developer, shows Ghost Light: in 2126 a robot visits a temple of manual coding and travels through Devoxx eras to the present year. The isometric 3D venue hosts chatting robots, collectible stickers, and real people (photographer Dimitris takes your picture in-game). After a week refusing non-Java tooling, he followed Claude Code's advice to use Three.js and TypeScript from the competition description as spec. Recreating the building from plans and photos worked except for the registration desk, bathrooms and the cinema entrance, fixed by describing small zones one at a time. Adding women attendees exposed that the generated crowds were all men.

### [39:50](https://youtu.be/NT0wyPM58G8?t=2390) Play and vote
The session closes by inviting everyone to play the games on the competition portal (QR code on screen), most playable on mobile, and to vote for a favorite.

## Tools, libraries and specs
- Claude / Claude Code (Opus, Opus 5.5) — game code, briefs, textures, venue modeling
- ChatGPT and Codex (GPT models) — brainstorming, 1800-line brief, hopping physics
- GitHub Copilot in VS Code — beacon game generation
- Gemini — Overclocked game ideas
- Phaser 3 + Tiled — Devoxx Reboot 2D engine and tile maps
- Three.js + Rapier physics + TypeScript — two 3D entries
- Unreal Engine + Claude Code hooks broker — sub-agent visualization
- Sonic Pi (AI-generated code) — game music
- Web Audio API — chiptune playback
- GitHub Pages PWA — publishing playable games

## Who should watch
Developers curious what AI-assisted game building looks like in practice, and anyone weighing which tools and workflows to try for a weekend build. Voters in the Robot Games competition get the full lineup in 40 minutes. Skip it for deep engine internals: each entry gets four minutes, so techniques are named and shown rather than taught.

## Verdict
**8/10**: Eight playable games and an agent visualizer premiered with their AI build stories, shown running on screen; each entry has four minutes, so the build numbers are self-reported and most internals stay brief.

**Novelty 2/2**

- **+** [01:04](https://youtu.be/NT0wyPM58G8?t=64) The session premieres eight original games and one agent visualizer built for this competition, each with its own mechanics, art and build story.
- **+** [15:14](https://youtu.be/NT0wyPM58G8?t=914) Photos, drone video and floor plans kept producing wrong walls until the builder described the venue room by room and had the model paint its plan over the game, so every error showed in yellow.
- **+** [16:17](https://youtu.be/NT0wyPM58G8?t=977) The Unreal visualizer renders real Claude Code sub-agents as builders on an exhibition floor, an entry no getting-started page covers.

**Demonstrated 2/2**

- **+** [02:08](https://youtu.be/NT0wyPM58G8?t=128) Robots stack to reach a lever and carry items through puzzles, shown on screen.
- **+** [30:58](https://youtu.be/NT0wyPM58G8?t=1858) The hopping robot crosses the venue on screen, with security switched off for that run.
- **−** [26:14](https://youtu.be/NT0wyPM58G8?t=1574) Richard's run shows stray objects flying around that the model could not explain, and the mobile run does not stop.

**Measured 1/2**

- **+** [06:47](https://youtu.be/NT0wyPM58G8?t=407) A first version was ready in one hour against the AI's estimate of a full day, from a 13-hour window.
- **·** [25:12](https://youtu.be/NT0wyPM58G8?t=1512) Token use is described as "exhausted all my tokens" with no figure.
- **·** [31:58](https://youtu.be/NT0wyPM58G8?t=1918) The 1800-line brief and the best-run time are self-reported with no baseline or method.

**Depth 1/2**

- **+** [14:44](https://youtu.be/NT0wyPM58G8?t=884) The Overclocked builder explains the crowd system: simple per-attendee rules over shared flow fields, with tests written as user stories.
- **+** [18:23](https://youtu.be/NT0wyPM58G8?t=1103) The Unreal visualizer is explained end to end: hooks emit JSON per sub-agent, a broker reads the files and streams them into the Unreal client.
- **·** [00:34](https://youtu.be/NT0wyPM58G8?t=34) Each entry gets four minutes, so most name the tools and show the game without explaining how it works.

**Reusable 2/2**

- **+** [00:34](https://youtu.be/NT0wyPM58G8?t=34) Every game is playable by the audience with its repository available to clone.
- **+** [33:01](https://youtu.be/NT0wyPM58G8?t=1981) The Richie game runs for free on GitHub Pages as a PWA, playable on a phone or a laptop.
- **−** [18:54](https://youtu.be/NT0wyPM58G8?t=1134) The hooks, broker and Unreal setup is offered for your own Claude Code sessions, but no repository is named.
