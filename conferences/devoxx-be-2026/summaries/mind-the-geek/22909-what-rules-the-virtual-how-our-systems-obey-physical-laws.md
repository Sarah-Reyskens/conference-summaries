---
title: What rules the virtual? How our systems obey physical laws.
talkId: "22909"
conference: devoxx-be-2026
speakers: [Marianne Hoornenborg]
track: Mind the Geek
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=yB6FIQPgsWE
durationMin: 49
slides: null
verdict: 5
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# What rules the virtual? How our systems obey physical laws.

Marianne Hoornenborg · Conference · Mind the Geek

## TL;DR

Words like cloud, wireless and serverless hide that computing is a physical process: electrons move, atoms get excited, and erased information leaves as heat. The talk walks down the stack from circuits and data carriers through semiconductors to qubits, and ends by celebrating the abstractions that let programmers ignore all of it.

## Key takeaways

- Current is the coordinated movement of charge toward vacancies: a full row of electrons only shifts when a hole gives them somewhere to go.
- Data carriers are physical while information is a discernible state: a punch card gets lighter as holes add data, and a hard disk arm still seeks fragments across the platter.
- Erasing data destroys access, not matter: Landauer's principle says the lost discernibility spreads into the environment as heat, part of why machines need fans and radiators.
- A transistor switches by applying voltage to an isolated middle layer, toggling it between conducting and isolating; NAND and NOT gates built this way compose into AND logic and SRAM cache loops.
- Quantum systems behave as waves until observed: any interaction, even a photon bumping into the system, collapses superposition into a classical state (decoherence).
- Entangled qubits are one system whose joint state defines both particles, not two particles communicating faster than light.
- Quantum computers in use today need millikelvin cooling, repeated runs over interference patterns, and have no mature abstraction layers yet; IBM offers a free tier to run a first quantum program.

## Notes

### [00:34](https://youtu.be/yB6FIQPgsWE?t=34) Virtual words for physical things

The speaker opens by collecting audience words that frame computing as untangible: cloud, wireless, serverless, no-code, virtual memory, virtual machines. She advances her own slides through a Makey Makey board wired to her body, so she is literally part of the circuit, and briefly plays a game by conducting through herself. The plan for the session: start at the virtual interpretation, descend through physical devices to the elementary and sub-elementary level, then resurface.

### [07:22](https://youtu.be/yB6FIQPgsWE?t=442) How current moves

Electrons in a wire are compared to a conference row: if every seat is taken and someone new arrives, nothing moves, but with one free seat the whole row can shift one chair and admit the newcomer at the end. Applying current is that coordinated shift. Everything digital rests on current that is encoded somewhere and interpreted by a receiver.

### [09:28](https://youtu.be/yB6FIQPgsWE?t=568) Inside a laptop

On stage sits her brother's disassembled laptop: motherboard, processor, fans, radiators, and a plug-in memory card (a daughterboard). Taking it apart made concrete why machines are noisy (fans), why radiators absorb heat, and how abstractions hide components someone once designed. About two thirds of the audience had taken a computer apart before.

### [12:06](https://youtu.be/yB6FIQPgsWE?t=726) Data carriers and erasure

Information itself is an imaginary mathematical state; only the carrier is physical, and it must let us discern two states, like the faces of a coin. A punch card loses mass as data is added. The hard disk photo's fine print warns that rattling is normal and breathing holes must stay uncovered. Defragmenting (grouping a file's scattered blocks so the arm seeks less) is still needed, but the OS now does it silently. Erasure means losing the ability to discern 0 from 1; per Landauer, the entropy spreads into the environment as heat, like a burnt book whose matter persists while its pages become unreadable.

### [18:27](https://youtu.be/yB6FIQPgsWE?t=1107) From keystroke to photon

Tracing a 0 and 1 to the projector crosses intent, keyboard encoding, OS handlers, HDMI encoding across the cable's 19 pins, and photonic display. Photons come from excited atoms: an atom fed current enters an excited state and emits a photon as it returns to neutral. "Wireless" still needs a medium (air carrying electromagnetic waves); a slide shows the frequency bands used by Ethernet, HDMI and radio links.

### [23:12](https://youtu.be/yB6FIQPgsWE?t=1392) Silicon, doping and the transistor

Silicon Valley is named for semiconductors made from silicon, essentially sand; one grain of sand can yield billions of transistors. Slides show the rigid silicon grid with impurities: phosphorus adds an excess electron (N-type, negative), boron leaves a hole (P-type, positive). Applying current moves holes and electrons toward or away from each other. A transistor adds an isolated middle layer: with no voltage it isolates, and adding electrons makes current flow, forming a microscopic on/off switch.

### [28:27](https://youtu.be/yB6FIQPgsWE?t=1707) Gates and memory

Three schematics: a NAND gate plus a NOT gate forming an AND gate (NOT-AND is easier to build in transistor logic than AND directly), DRAM main memory as one transistor plus one capacitor per cell, and SRAM cache as two NOT gates in a loop continuously agreeing "this is something, this is the opposite". The speaker skips DRAM internals and invites the audience to research them.

### [30:02](https://youtu.be/yB6FIQPgsWE?t=1802) Wave-particle duality and decoherence

The double-slit experiment: even single particles fired one at a time build up an interference pattern, behaving as waves through both slits until measurement collapses the wave function into a particle dot. Observation means any state-sharing with the environment, including a stray photon, which is how the classical world continuously agrees on reality. The qubit Bloch sphere visualizes superposition (amplitude and relative phase on X, Y, Z axes) collapsing to 0 or 1 on measurement.

### [36:12](https://youtu.be/yB6FIQPgsWE?t=2172) Entanglement

Two qubits manipulated into one joint quantum state follow rules where the state of one defines the state of the other, even light years apart. This is one system in a state, not faster-than-light communication. Information here is shared between qubits rather than leaked to the environment. The speaker flags she is not a physicist and invites corrections.

### [37:52](https://youtu.be/yB6FIQPgsWE?t=2272) Quantum computing, Jamie Oliver style

Framed as a three-course recipe: Build (create qubits as superconducting circuits or trapped ions held by optical tweezers, stabilize and cool below outer-space temperatures into the millikelvin range with cryogenics, connect and control), Manipulate (create superposition, steer evolution with precise lasers or microwaves to shape interference patterns, repeat runs for reliability), Measure (couple a detector, convert the signal, record a binary outcome). Each fridge level exists to move heat away from the qubits, since any heat destroys the quantum state. Scaling is unsolved, and the comfortable abstraction layers of classical computing do not exist yet.

### [44:08](https://youtu.be/yB6FIQPgsWE?t=2648) Access today and resurfacing

Developers mostly meet quantum through post-quantum encryption concerns. IBM has a free plan for running first quantum programs; Java libraries for quantum circuits exist but cannot yet execute on quantum hardware, a lag the speaker compares to Python's early AI lead. The close: abstractions are worth celebrating because they let us work at human scale without holding all this detail at once. Final slide lists sources (The Science of Everything, From First Principles, Khan Academy, 3Blue1Brown, Kurzgesagt, ShindenGen, IBM) and invites the audience to play the jumper-cable game at the front.

## Tools, libraries and specs

- Makey Makey: board used live to wire the speaker's body into the slide-advance circuit and a game.
- IBM quantum free tier: lets anyone run first quantum computing programs.

## Who should watch

Developers curious what happens below their programming language, especially self-taught or career-switching engineers who never studied hardware or physics. Skip it if you already know semiconductor and qubit basics and want implementation detail or benchmarks instead.

## Verdict

**5/10**: A physics tour from circuits to qubits with a live body-circuit slide advance, held at survey depth with no measurements and no artifact of its own.

**Novelty 1/2**

- **+** [12:06](https://youtu.be/yB6FIQPgsWE?t=726) Punch cards losing mass, the hard disk's breathing-hole warning and Landauer heat are combined into one argument about physical carriers that a single search result does not give as a whole.
- **+** [10:30](https://youtu.be/yB6FIQPgsWE?t=630) The teardown of her brother's laptop and her retraining as a programmer at 40 carry standard material with first-hand experience.

**Demonstrated 1/2**

- **+** [01:07](https://youtu.be/yB6FIQPgsWE?t=67) She advances her slides by completing a Makey Makey circuit with her own body ("Yes, there we go"), a working live demo of current through a circuit.
- **−** [06:50](https://youtu.be/yB6FIQPgsWE?t=410) The game controlled through the same circuit is announced, but the projector still shows the physics slide, so it is described rather than shown.
- **·** [26:52](https://youtu.be/yB6FIQPgsWE?t=1612) The transistor, gates, Landauer heat and qubits are explained on slides only, with nothing run.

**Measured 1/2**

- **·** [24:14](https://youtu.be/yB6FIQPgsWE?t=1454) The talk makes no claim about speed, cost or effect; figures such as billions of transistors per grain of sand are stated facts with no measurement behind them.

**Depth 1/2**

- **+** [27:23](https://youtu.be/yB6FIQPgsWE?t=1643) The transistor switch is explained causally: voltage on the isolated middle layer toggles it between conducting and isolating, which is how 0s and 1s arise.
- **+** [33:07](https://youtu.be/yB6FIQPgsWE?t=1987) Decoherence is explained as the quantum state being shared with the environment and becoming classical, which gives a mechanism for how classical states emerge.
- **−** [36:12](https://youtu.be/yB6FIQPgsWE?t=2172) Entanglement is stated as "one system" with no mechanism, and she says she may not be explaining it correctly.

**Reusable 1/2**

- **+** [44:39](https://youtu.be/yB6FIQPgsWE?t=2679) She points to IBM's free plan for running a first quantum program.
- **−** [47:50](https://youtu.be/yB6FIQPgsWE?t=2870) The closing slide lists source names with no URLs, and no repository, checklist or configuration covers the talk's main content.
