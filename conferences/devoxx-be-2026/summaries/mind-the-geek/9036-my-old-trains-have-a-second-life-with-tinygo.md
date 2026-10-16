---
title: My old trains have a second life, with TinyGo!
talkId: "9036"
conference: devoxx-be-2026
speakers: [Florian FORESTIER, Justine Bachelard]
track: Mind the Geek
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=LIGVpEuIrrY
durationMin: 40
slides: https://forestier.re/presentations/trainberry/fosdem-2026/index.html
slidesNote: from FOSDEM 2026
verdict: 8
reach: niche
frames: 12
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15

# My old trains have a second life, with TinyGo!

Florian FORESTIER, Justine Bachelard · Conference · Mind the Geek

Slides: https://forestier.re/presentations/trainberry/fosdem-2026/index.html

## TL;DR

Two web developers digitized a family fleet of 1980s HO model trains with TinyGo, moving from a REST-over-WiFi prototype on a Raspberry Pi Pico to Bluetooth LE on a Seeed XIAO nRF52840. The talk is a build log of that migration: fried boards, zombie trains, latency measurements, and a live demo of driving the trains from a web UI.

## Key takeaways

- A per-train REST API over WiFi cost 300+ ms per command; switching to Bluetooth LE with kept-open connections brought writes under 1 ms.
- Powering a microcontroller from model-rail rails needs a step-down converter, reverse-polarity protection, and a capacitor to smooth the micro-cuts the wheels and rails introduce.
- On a single-core board, handling a Bluetooth request can starve motor control; queueing commands through a Go channel and processing them in the main loop removes the deadlock.
- A watchdog (8 s hardware timer, WiFi sanity check every 4 s) recovers trains that lose power and come back unreachable at full throttle.
- Commercial DCC conversion would have cost nearly €2,900 for their fleet and forced an all-or-nothing migration, which motivated the custom open-hardware route.

## Notes

### [01:34](https://youtu.be/LIGVpEuIrrY?t=94) Three generations of analog trains

The trains were bought in the early 1980s, stored in an attic for 25 years, revived in 2005, and expanded after 2011 with a tripled table, a new station, and rewired electrics. HO scale (1:87) runs on 14 V DC through the rails; each train is one lamp and one motor wired in parallel. Analog control modulates rail voltage from -14 V to +14 V, so every train goes the same direction at roughly the same speed, which caps the table at about three simultaneous trains. Sections of track are isolated with switches, at the cost of roughly 4 km of cable under a ping-pong table.

### [06:18](https://youtu.be/LIGVpEuIrrY?t=378) Why not DCC

DCC sends control signals over rail power so each decoder-equipped train moves independently. The catch is all-or-nothing: the layout runs DCC or analog, never both, so all twenty trains would need new motors plus decoders at once, plus command stations. Quoted cost was nearly €2,900, and the market offered only proprietary hardware, so the idea was shelved until a TinyGo talk at Volcamp 2024 restarted the project.

### [09:27](https://youtu.be/LIGVpEuIrrY?t=567) Digitizing the first train

First victim: a BB 9201, with just enough room for a Raspberry Pi Pico W (21 x 51 mm, 264 KB RAM, two cores at 133 MHz, 2 MB flash, WiFi plus Bluetooth). The power chain runs rail 14 V through a step-down converter to 5 V for the Pico, which drives the motor through an Adafruit DRV8871 PWM module. Three hardware lessons followed: reversed polarity fried the first build (fixed with a diode), rail micro-cuts rebooted the Pico in a loop (fixed with a smoothing capacitor), and the wiring no longer fit (fixed with a first custom PCB shield, which worked on the first attempt).

### [14:41](https://youtu.be/LIGVpEuIrrY?t=881) Software v1: REST over WiFi, and zombies

The train firmware is TinyGo: lights on/off, motor speed and direction, and five REST endpoints served to a central Go server on a Raspberry Pi 3 with a Svelte frontend. TinyGo had no Pico WiFi support then, so the stack was hand-rolled. Power loss over about 5 seconds shut WiFi down without restarting it, leaving unreachable trains running at full speed; the fix is a watchdog with an 8 s timer fed by a goroutine that checks WiFi every 4 s.

### [20:24](https://youtu.be/LIGVpEuIrrY?t=1224) Live demo

The Trainberry UI drives the physical loop on stage: the speed slider sets the BB 9201 running, the light toggles respond, and the card shows honk and sound buttons plus an emergency stop. During Q&A the audience can vote every 15 seconds for the next move from their phones.

### [21:28](https://youtu.be/LIGVpEuIrrY?t=1288) Going smaller: Seeed XIAO and Bluetooth LE

HTTP commands took over 300 ms, judged unsafe for emergency stops, and the Pico build (21 x 51 x 20 mm) could not fit the Jouef 8525 draisine (21 x 42 x 12 mm free). Seeed XIAO boards (17.8 x 21 mm) fit, but the RP2040 variant has no wireless and the ESP32-C6 turned out to lack TinyGo support at the time, so the pick was the XIAO nRF52840 (single core 64 MHz, 256 KB RAM, 2 MB flash, BLE only). Supporting parts shrank too: a Pololu 5 V converter (7.6 x 11.4 mm) and a TA6586 motor driver (9 x 6 mm), hand-soldered on both sides of a new PCB over three to four hours.

### [27:16](https://youtu.be/LIGVpEuIrrY?t=1636) BLE architecture and the channel fix

Each train exposes a GATT server: services read like collections, characteristics like items, and read/write maps onto HTTP verbs. The server holds connections open to every train advertising a `Trainberry::` name (eight clients fit), giving sub-1 ms writes, while the frontend-to-server link moved from REST to a WebSocket with multi-client sync. Because the single core sits at 100% during a BLE request, motor updates moved behind a Go event channel consumed by the main loop. Dropping WiFi also removed the dedicated router, the hand-rolled TCP/IP stack, and all SSID and key provisioning.

### [33:27](https://youtu.be/LIGVpEuIrrY?t=2007) Polarity fix, sound, and what is next

The current board adds a diode bridge so trains boot regardless of which way they sit on the rails, plus a DFRobot DFPlayer Pro for sound, which is already straining the size budget again. A PCB mistake fried a XIAO and a DFPlayer (about $25) five days before a conference; the surviving layout resembles a Star Wars U-Wing. Next ideas: station announcements, NFC-triggered stops, a real-time map, onboard webcams, digitized switches, and eventually a fully custom board for 2027. The project is open source and open hardware, and the speakers accept train donations.

## Tools, libraries and specs

- TinyGo (train firmware) and Go (central server)
- Raspberry Pi Pico W, Raspberry Pi 3 (server)
- Seeed Studio XIAO nRF52840; XIAO ESP32-C6 and RP2040 evaluated and rejected
- Adafruit DRV8871 PWM driver, TA6586 motor driver, Pololu 5 V step-down converter, DFRobot DFPlayer Pro
- Bluetooth LE GATT (`tinygo.org/x/bluetooth` on the trains, `github.com/go-ble/ble` on the server)
- Svelte frontend, WebSocket sync, KiCad PCBs, DCC (model-rail standard, rejected)

## Who should watch

Beginners curious about embedded work, web developers wondering how their habits transfer to constrained boards, and model-railway hobbyists weighing DCC against a custom build. Skip it for BLE protocol internals, DCC expertise, or advanced Go: the code stays at the level of calling PWM, GATT, and channel primitives.

## Verdict

**8/10**: Live control of a physical train and a first-hand build log with explained mechanisms carry it; the latency figures have no stated method and no repository is named.

**Reach niche**: Conference-goers working with embedded boards or model railways can reuse the train-digitizing build, a specialised subject few in this audience work on.

**Novelty 2/2**

- **+** [23:33](https://youtu.be/LIGVpEuIrrY?t=1413) The speakers ordered and soldered ESP32-C6 boards before discovering TinyGo did not support the chip, forcing another board search.
- **+** [35:02](https://youtu.be/LIGVpEuIrrY?t=2102) A self-made PCB mistake fried a XIAO and a DFPlayer just days before a conference, a failure only their own build log gives.

**Demonstrated 2/2**

- **+** [20:24](https://youtu.be/LIGVpEuIrrY?t=1224) Live on stage, changing the speed in the Trainberry UI sets the physical BB 9201 running on the table.
- **−** [20:24](https://youtu.be/LIGVpEuIrrY?t=1224) The speaker acknowledges that the interface is broken, although the demonstrated speed control still works.
- **·** [39:46](https://youtu.be/LIGVpEuIrrY?t=2386) The recording ends on the QR-code invitation to vote for the next run, so the audience-driven run is not shown.

**Measured 1/2**

- **+** [20:57](https://youtu.be/LIGVpEuIrrY?t=1257) The superseded WiFi/HTTP prototype had command latency above 200 ms in the accepted deck, with the speaker reporting above 300 ms here and judging it too slow for emergency stops.
- **+** [27:46](https://youtu.be/LIGVpEuIrrY?t=1666) BLE writes over the kept-open connection come in under 1 ms.
- **−** [27:46](https://youtu.be/LIGVpEuIrrY?t=1666) Neither figure comes with a stated measurement method, so the comparison cannot be reproduced from the talk.

**Depth 2/2**

- **+** [27:16](https://youtu.be/LIGVpEuIrrY?t=1636) The GATT mental model (services as collections, characteristics as items, read/write as HTTP verbs) gives beginners a working picture of BLE.
- **+** [29:20](https://youtu.be/LIGVpEuIrrY?t=1760) The single-core deadlock between BLE handling and PWM computation is explained and fixed by queuing events through a Go channel.
- **+** [18:19](https://youtu.be/LIGVpEuIrrY?t=1099) The watchdog design follows from the zombie failure: a hardware timer fed by a periodic WiFi sanity check reboots the board when checks keep failing.

**Reusable 1/2**

- **+** [38:12](https://youtu.be/LIGVpEuIrrY?t=2292) Every code snippet shown is real, compiling TinyGo.
- **+** [37:39](https://youtu.be/LIGVpEuIrrY?t=2259) The project is declared open source and open hardware with an invitation to contribute.
- **−** [39:15](https://youtu.be/LIGVpEuIrrY?t=2315) No repository is named and the closing QR codes lead to the feedback form and the train vote, so rebuilding starts from the snippets.
