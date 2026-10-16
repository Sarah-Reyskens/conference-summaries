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
reach: niche
frames: 5
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16

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

**7/10**: A Java-driven LEGO SPIKE project with a working motion demo and a beginner-level account of why a Raspberry Pi bridge is needed; the project story is short and the linked repository does not hold the SPIKE code shown.

**Reach niche**: The main content serves developers who run children's robotics workshops or want to control LEGO SPIKE from Java.

**Novelty 1/2**

- **+** [11:51](https://youtu.be/_VZg6dxlGaM?t=711) Vos recounts the project's silent failure after motion had worked in Python: the Java side caught every error and the robot sent nothing back, which led to rerouting the architecture.
- **·** [05:50](https://youtu.be/_VZg6dxlGaM?t=350) Observations about robots keeping children's attention and the move from Scratch to Java are workshop examples rather than a developed teaching framework.

**Demonstrated 2/2**

- **+** [14:34](https://youtu.be/_VZg6dxlGaM?t=874) A timed drive command is added to the Java program in VS Code before the robot run.
- **+** [15:30](https://youtu.be/_VZg6dxlGaM?t=930) The overhead camera shows the robot on the floor while the editor and hub motor output show the Java-to-bridge run.
- **−** [16:05](https://youtu.be/_VZg6dxlGaM?t=965) Distance-sensor support is unfinished (the terminal prints `Distance: null mm`), so the demonstrated functionality is motion only.

**Measured 1/2**

- **·** [20:02](https://youtu.be/_VZg6dxlGaM?t=1202) The case for teaching children to code makes no quantitative claim about learning outcomes, so measurement is not applicable.

**Depth 2/2**

- **+** [09:41](https://youtu.be/_VZg6dxlGaM?t=581) Putting a JVM on the hub is rejected because it needs custom firmware, which would stop school-owned robots working with the official LEGO software.
- **+** [17:15](https://youtu.be/_VZg6dxlGaM?t=1035) The architecture diagram separates the Java API and TCP commands, the Pi's protocol and BLE bridge, and the hub's MicroPython agent with firmware untouched.
- **+** [14:01](https://youtu.be/_VZg6dxlGaM?t=841) The child-facing API hides the hub's requirement that every drive command carry both speed and duration.

**Reusable 1/2**

- **+** [22:49](https://youtu.be/_VZg6dxlGaM?t=1369) The closing slide points to github.com/devoxx4kids/materials as the place to contribute to the Java + SPIKE code, and Vos says all the code is in that repository.
- **−** [22:49](https://youtu.be/_VZg6dxlGaM?t=1369) The repository's `workshops` directory has no SPIKE entry (`mindstorms` holds only `ev3` and `nxt2.0`), so it does not reproduce the bridge shown in the demo.

