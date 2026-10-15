---
title: "Java, LEGO & AI: Teaching the Next Generation to Build, Not Just Prompt"
talkId: "10045"
conference: devoxx-be-2026
speakers: [Eddy Vos]
track: Mind the Geek
sessionType: Lunch Talk
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=_VZg6dxlGaM
durationMin: 24
slides: null
verdict: 7
frames: 5
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Java, LEGO & AI: Teaching the Next Generation to Build, Not Just Prompt

Eddy Vos · Lunch Talk · Mind the Geek

## TL;DR

Teaching children to code still matters in the AI era: prompting is asking, building is understanding. Eddy Vos shows how Devoxx4Kids Netherlands drives LEGO SPIKE robots from Java via a Raspberry Pi bridge, demos it live, and asks Java developers to volunteer.

## Key takeaways

- Judging generated code (a loop turning three times instead of four) requires understanding the constructs.
- A robot driving around the room makes bugs visible in a way screen-only coding does not.
- No JVM fits the SPIKE Prime hub (ARM Cortex-M4, 320 KB RAM): Java is the brain on the laptop, LEGO the body.
- A Raspberry Pi running a Python bridge translating Java commands into hub bytecode unblocked the project after direct Bluetooth from Windows failed.
- Java 25 drops the `public static void` ceremony from `main`, so kids use the same IDEs as their parents.

## Notes

### [01:14](https://youtu.be/_VZg6dxlGaM?t=74) Why teach kids to code when AI exists

Parents, teachers, and colleagues all ask Vos this; his answer is the calculator analogy (we still teach math so we spot 7x8=5600 as wrong). Workshops start ages 8-9 in Scratch, then graduate them to Java, the language most Dutch volunteers write.

### [08:01](https://youtu.be/_VZg6dxlGaM?t=481) Three roads to Java control

The hub's ARM Cortex-M4 has 320 KB RAM: no room for a JVM, and custom firmware would break school-owned robots for official LEGO software. Generated MicroPython uploaded to a hub program slot ran without moving the robot. Live Bluetooth control stalled: the Java libraries found ran only on macOS or Linux, while workshops use donated Windows laptops.

### [11:21](https://youtu.be/_VZg6dxlGaM?t=681) The bridge that worked, and the live demo

Spare Raspberry Pis became the bridge: motion proven in Python first with the Bleak library, then a Python server on the Pi translating Java calls into hub bytecode. Vos demoed in VS Code over SSH against `SpikeRobot`/`SpikeBridgeClient`, with calls like `driveForward()` hiding the hub's demand that every drive command carry speed and duration. An overhead camera showed the robot driving; distance-sensor support was still unfinished.

### [18:53](https://youtu.be/_VZg6dxlGaM?t=1133) Could AI have built this

Vos used Claude for the protocol docs and boilerplate; it once baked a deadlock into delivered code and congratulated itself. He asks developers to volunteer, host a Devoxx4Kids day, or contribute at github.com/devoxx4kids/materials.

## Tools, libraries and specs

- LEGO SPIKE Prime (Mindstorms successor), MicroPython on-hub; Bleak (Python Bluetooth LE library)
- Raspberry Pi as Bluetooth bridge; Java 25 simplified `main`; IntelliJ, VS Code; Claude

## Who should watch

Java developers curious about Devoxx4Kids volunteering or driving LEGO SPIKE from Java; skip for a deep Bluetooth-protocol reference.

## Verdict

**7/10**: A Java-to-LEGO-SPIKE bridge from the speaker's own workshop project, with each design choice reasoned and the robot driven live; the opening argument is common and the linked repo holds no SPIKE code.

**Novelty 1/2**

- **+** [10:13](https://youtu.be/_VZg6dxlGaM?t=613) The three routes to Java control (custom firmware, generated MicroPython, direct Bluetooth) and the failures behind each come from the speaker's own Devoxx4Kids workshop project.
- **−** The opening case for teaching coding despite AI rests on the familiar calculator analogy and need to understand generated code, already covered by [Create & Learn's coding-in-the-AI-era guide](https://www.create-learn.us/blog/should-kids-still-learn-coding-in-the-ai-era-a-parents-guide-for-2026/) and ["The calculator analogy: Epistemic virtues for using LLMs"](https://www.sciencedirect.com/science/article/pii/S0160791X25003884).

**Demonstrated 2/2**

- **+** [14:34](https://youtu.be/_VZg6dxlGaM?t=874) Drive calls with speed 100 for 3 seconds are added live in the editor and sent through the bridge.
- **+** [16:05](https://youtu.be/_VZg6dxlGaM?t=965) The robot moves under the overhead camera while the terminal shows the bridge connection and motor telemetry.
- **−** [16:05](https://youtu.be/_VZg6dxlGaM?t=965) Distance-sensor support is still unfinished and the run prints "Distance: null mm", so only motion is shown working.

**Measured 1/2**

- **·** [08:01](https://youtu.be/_VZg6dxlGaM?t=481) The talk makes no quantitative claim about its own results; the 320 KB hub figure is a spec that rules out a JVM, not a measurement.

**Depth 2/2**

- **+** [09:11](https://youtu.be/_VZg6dxlGaM?t=551) Each rejected route gets its reason: custom firmware would break school-owned robots for the official software, and the Java Bluetooth libraries found ran only on macOS or Linux while workshops use Windows laptops.
- **+** [17:15](https://youtu.be/_VZg6dxlGaM?t=1035) The three-tier design (Java on the laptop, a Pi bridge, an untouched hub with one uploaded agent) is explained, with the Pi named as a stopgap until the new Java Bluetooth library lets it be dropped.
- **+** [18:22](https://youtu.be/_VZg6dxlGaM?t=1102) Java is the workshop language because volunteers and parents write it, and Java 25's simplified `main` keeps kids in the same IDEs.

**Reusable 1/2**

- **+** [22:49](https://youtu.be/_VZg6dxlGaM?t=1369) The talk points to the Devoxx4Kids materials repo for "all our code".
- **−** [22:49](https://youtu.be/_VZg6dxlGaM?t=1369) That repo's workshops folder holds no SPIKE bridge code, so the demo cannot be rebuilt from it.


