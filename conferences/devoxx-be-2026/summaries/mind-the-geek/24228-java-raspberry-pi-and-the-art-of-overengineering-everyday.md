---
title: "Java, Raspberry Pi, and the Art of Overengineering Everyday Life"
talkId: "24228"
conference: devoxx-be-2026
speakers: [Matti Tahvonen]
track: Mind the Geek
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=5W4o_aYOaIY
durationMin: 44
slides: null
verdict: 8
frames: 10
reviewedAt: 2026-10-14
---

# Java, Raspberry Pi, and the Art of Overengineering Everyday Life
Matti Tahvonen · Conference · Mind the Geek

## TL;DR
A Java web developer with one year of Raspberry Pi hobby experience shows how to build real home automation (a BBQ smoker controller, a jetty server with camera and water-level sensing) in pure Java with Pi4J, Quarkus, and Vaadin. The core deliverable is an opinionated recipe: develop on the laptop against simulated hardware, deploy with an rsync script as a systemd service, and expose services securely through a Cloudflare Tunnel with passkey login.

## Key takeaways
- Put hardware behind interfaces and develop on the laptop with simulated implementations, then deploy to the Pi with a script that explodes the fat jar, rsyncs only changed files, and installs a systemd service.
- Prefer Quarkus over Spring Boot on small Pis: startup is roughly twice as fast, which matters on constrained devices.
- Reach for microcontrollers instead of a full Pi plus OS plus JVM when the job is reading one sensor; push the data to a Java server.
- Skip breadboards for real builds: lever connectors (Wago-style) accept any wire type, and solder the final installation.
- Run a single Cloudflare Tunnel on the strongest home Pi to give every service HTTPS; that unlocks PWA push notifications, and passkeys cover login without another identity service.
- Buy a case with active cooling: a Pi Zero 2 rendering timelapse movies from stills overheated and crashed without a heatsink.

## Notes

### [00:34](https://youtu.be/5W4o_aYOaIY?t=34) A web developer's year with Raspberry Pi
Tahvonen has 20 years of Java web apps and about one year of Raspberry Pi tinkering. His route in was updating a Vaadin demo for Frank Delporte onto a Pimoroni-style demo board, then buying every Pi the local electronics store had. Practical advice up front: Pis sell out (now also as AI-agent containers), so buy three times what is needed; start on a Pi 5 in the official case with heatsink and fan rather than a 512 MB Zero 2.

### [04:43](https://youtu.be/5W4o_aYOaIY?t=283) Jetty server: sunsets, water level, fishing alerts
Living on an island, he built a birdhouse-housed Pi 5 with a camera for sunset timelapses and a wireless water-level sensor, since wind-driven level changes in the Turku archipelago move the fish. The birdhouse Pi exposes a REST API and publishes to a bigger machine. The first version ran the same software on a Zero 2, which crashed rendering movies for lack of cooling.

### [06:50](https://youtu.be/5W4o_aYOaIY?t=410) BBQ smoker controller
His main project automates a low-and-slow smoker (fish, venison) so checks drop from every 15 minutes to wood refills every 1.5 to 2 hours. Inputs: MEATER Bluetooth probes (newer model read via cloud API after he reverse-engineered the old model's BLE protocol), a wired iBBQ thermometer through the door, and a thermocouple in the firebox surviving around 900 C for early warnings when the apple wood runs out. The controller runs a P algorithm over the airflow. A 12 V battery backup carries a full day of cooking through island power cuts.

### [07:53](https://youtu.be/5W4o_aYOaIY?t=473) Start gate and meat cooler
Two more builds: an orienteering start gate (a Pi Zero reading competitor cards over USB serial, opening a servo-driven barrier of fishing rod plus tape, buzzing early or late starters across ~2000-competitor races) and a hunting club meat-cooler monitor reading Ruuvi Air Bluetooth sensors into a cloud app that pages his phone when readings stop.

### [13:41](https://youtu.be/5W4o_aYOaIY?t=821) Air control and the chainsaw carburetor
The smoker regulates fire through a pipe drilled into the firebox. A solenoid valve passed too little air at that pressure difference, so the fix was a butterfly valve from an old chainsaw carburetor driven by a micro servo. Lesson: non-industrial builds need creativity, not bulletproof parts. The UI was a progressive web app from day one so the smoker can be watched from a boat or a dog walk.

### [16:17](https://youtu.be/5W4o_aYOaIY?t=977) Stack: Quarkus, Vaadin PWA, software PWM
Both Spring Boot and Quarkus were tried; Quarkus starts in less than half the time, which counts on small devices. Vaadin renders the PWA, installable on desktop and iPhone, with a system-monitor view (added after busy loops ate the CPU) and actuator controls. The fan runs on software PWM with a 10-second period since its speed cannot be adjusted directly. The j-smoker source is on GitHub.

### [18:54](https://youtu.be/5W4o_aYOaIY?t=1134) Hardware-access lessons
Pi4J is a low-level GPIO/I2C API; prefer the ready drivers in the Pi4J driver project (e.g. the BME280 temperature sensor) and contribute drivers back. Beyond Pi4J: Bluetooth sensors, USB-serial devices, the camera serial port (he vibe-coded a Java driver on libcamera rather than shelling to Python), and Java's FFM API to wrap C drivers. Wiring advice: lever connectors over breadboards, buy soldering equipment, and ignore the HDMI port since these boxes are managed over SSH and web UI.

### [25:42](https://youtu.be/5W4o_aYOaIY?t=1542) Develop on the laptop, ship with boot2vm
Never develop on the Pi: build and simulate on the workstation, then run his boot2vm script, which explodes the fat jar, rsyncs only changed files instead of a ~100 MB artifact, tunes JVM flags for the Pi, adds the service user to the needed groups (Bluetooth and friends), and installs and restarts a systemd service. Reboot and restart buttons in the web UI recover a wedged smoker from the iPhone.

### [28:16](https://youtu.be/5W4o_aYOaIY?t=1696) Pi Starter demo: simulation and Proto Tools
The live demo ran the pi-starter app (Quarkus plus Vaadin, from github.com/viritin/pi-pwa-starter) locally with a "hardware is simulated" banner: a climate view plotting BME280 readings, a Blink-a-LED actuator view, a system monitor with interface status and enable commands, and Proto Tools (GPIO board, I2C browser, PWM with wiring instructions, Bluetooth LE scanner). Against the stage Pi over Wi-Fi he drove a servo live, scanned the room's phones over Bluetooth, and showed temperature and humidity climbing on the dashboard.

### [32:29](https://youtu.be/5W4o_aYOaIY?t=1949) Live deploy in seconds
He edited a view title in IntelliJ, checked it on localhost, ran boot2vm (rsync output and `systemctl restart` visible in the terminal), and the Pi-served page auto-reloaded with the change seconds later. Simulations are plain CDI alternative implementations of the hardware interfaces, so no simulation code ships to the device.

### [36:45](https://youtu.be/5W4o_aYOaIY?t=2205) HTTPS, push notifications, passkeys
HTTPS is mandatory for PWA install and web push; a recorded phone demo showed notifications arriving with the app closed. He prefers Cloudflare Tunnel over ngrok: one tunnel on the jetty Pi 5 exposes every home service over HTTP/3 with encryption handled for him. For auth he ranks options from none (his smoker has only a cryptic URL) through VPN and app-wide passwords up to OpenID Connect, but recommends the starter's passkey branch (face or fingerprint) as the default.

### [42:31](https://youtu.be/5W4o_aYOaIY?t=2551) Recipe and warning
The closing recipe: Pi 5 for development, clone pi-starter and run simulated, hardware behind interfaces, deploy with boot2vm, explore wiring with Proto Tools, add HTTPS then passkeys and notifications. The final slide warns the hobby hijacks nerdy brains and advises setting limits.

## Tools, libraries and specs
- Raspberry Pi 5 / Pi Zero 2, Pimoroni demo board
- Pi4J (GPIO/I2C) and Pi4J drivers (BME280 sensor)
- Quarkus and Spring Boot (fat-jar deploy compared on startup time)
- Vaadin (Flow UI, installable PWA)
- github.com/viritin/pi-pwa-starter (pi-starter, pi-helpers, pi-helpers-simulation), mstahv/boot2vm, mstahv/j-smoker, mstahv/heisala-jetty
- Java FFM API, libcamera-based Java camera driver
- MEATER and iBBQ cooking thermometers, Ruuvi Air Bluetooth sensors, Bluetooth LE
- PWM (software and hardware), 1-Wire, I2C, USB serial (USB On-The-Go)
- Cloudflare Tunnel, ngrok, systemd, rsync, web push, passkeys/WebAuthn, OpenID Connect

## Who should watch
Java developers curious about Raspberry Pi automation, and anyone weighing Pi4J against Python for hobby hardware. Experienced Pi or embedded developers will find the hardware shallow; viewers wanting rigorous benchmarks or production security practice should look elsewhere.

## Verdict
**8/10**: A live simulate-then-deploy loop on a real Pi, the speaker's own builds and a documented starter repo earn the score; the numbers are anecdotes and most hardware topics get a sentence.

**Novelty 2/2**

- **+** [11:36](https://youtu.be/5W4o_aYOaIY?t=696) The smoker reads MEATER probes over Bluetooth LE after the speaker reverse engineered the old model's protocol, and the same build adds a chainsaw-carburetor butterfly valve [15:16](https://youtu.be/5W4o_aYOaIY?t=916), a P controller and a 12 V battery backup.
- **+** [22:03](https://youtu.be/5W4o_aYOaIY?t=1323) He wrote a pure-Java camera driver on top of libcamera so nothing shells out to Python.
- **+** [27:47](https://youtu.be/5W4o_aYOaIY?t=1667) The recipe slide packages his own projects' stack (starter, simulation, boot2vm, Proto Tools, tunnel, passkeys) as one workflow, with Home Assistant rejected up front because it "was built with Python. I couldn't extend it" [04:12](https://youtu.be/5W4o_aYOaIY?t=252).

**Demonstrated 2/2**

- **+** [33:01](https://youtu.be/5W4o_aYOaIY?t=1981) An edited view title ships through boot2vm and the Pi-served page auto-reloads seconds later while the temperature and humidity graphs climb.
- **+** [31:25](https://youtu.be/5W4o_aYOaIY?t=1885) The Bluetooth scanner runs on the stage Pi against the room and lists the audience's phones.
- **+** [37:17](https://youtu.be/5W4o_aYOaIY?t=2237) A recorded phone run shows a web push notification arriving with the app closed and reopening the PWA full screen.

**Measured 1/2**

- **+** [33:05](https://youtu.be/5W4o_aYOaIY?t=1985) The boot2vm terminal prints rsync's "speedup is 34.30" (1,298,978 bytes sent for a 45,515,265-byte tree), which backs the changed-files-only claim.
- **·** [13:09](https://youtu.be/5W4o_aYOaIY?t=789) Checks drop from "every 15 minutes" to adding wood every "1 and a half or 2 hours", reported from memory with no log.
- **−** [16:17](https://youtu.be/5W4o_aYOaIY?t=977) Quarkus starting "bit more than double" faster than Spring Boot has no versions, timings or method.

**Depth 1/2**

- **+** [19:25](https://youtu.be/5W4o_aYOaIY?t=1165) The microcontroller-versus-Pi and Pi4J-versus-driver-versus-FFM choices each come with a when-to-use rule.
- **+** [37:15](https://youtu.be/5W4o_aYOaIY?t=2235) The HTTPS slide gives three routes (Cloudflare Tunnel for remote, own domain with DNS-01 for LAN only, Caddy's internal CA with no domain), and the talk picks Cloudflare Tunnel over ngrok because one tunnel serves every home service [38:49](https://youtu.be/5W4o_aYOaIY?t=2329).
- **·** [19:55](https://youtu.be/5W4o_aYOaIY?t=1195) Pi4J is called "quite low-level" and skipped in favour of drivers, and the FFM wrapper gets one sentence, so how either talks to the hardware is not explained.

**Reusable 2/2**

- **+** [27:47](https://youtu.be/5W4o_aYOaIY?t=1667) The recipe slide points to github.com/viritin/pi-pwa-starter ("Fully documented"), covering the Quarkus + Vaadin starter, simulation modules, Proto Tools, system view and passkey login.
- **+** [34:40](https://youtu.be/5W4o_aYOaIY?t=2080) The boot2vm deploy script, step 4 of the recipe, is the speaker's own tool, adapted for Pis with JVM flags and service-user groups.
- **·** [18:22](https://youtu.be/5W4o_aYOaIY?t=1102) The smoker's source is only said to be "in the internet"; j-smoker and heisala-jetty are not named in the talk.
