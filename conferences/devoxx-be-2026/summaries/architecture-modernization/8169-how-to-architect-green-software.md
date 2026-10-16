---
title: How to Architect Green Software
talkId: "8169"
conference: devoxx-be-2026
speakers: [Ioannis Kolaxis]
track: Architecture & Modernization
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=bqwtnKLU35E
durationMin: 50
slides: null
verdict: 6
reach: broad
frames: 12
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15

# How to Architect Green Software

Ioannis Kolaxis · Conference · Architecture & Modernization

## TL;DR

Green software means designing applications to cut energy use, carbon footprint, and cloud cost together, and architects should weigh sustainability against the other "ilities" in every hard-to-reverse decision. The talk walks a priority order (devices first, then networks, then data centers), catalogs the trade-off in each practice, and argues AI coding agents are shrinking the effort cost of the green option.

## Key takeaways

- Put device lifetime first: support old OS versions and low-spec hardware, or ship thin or native clients.
- Every green practice has a counter-force: compression trades network bytes for compute, caching for storage, local inference for newer hardware.
- Never pick a data center on PUE alone; a low PUE can hide high water use, so balance PUE, WUE, and grid carbon intensity against cost and latency.
- Question active-standby redundancy: at four nines, the downtime budget covers restarting a failed VM from an infrastructure-as-code script instead of a hot spare.
- Revisit rejected ARM migrations: porting effort was the blocker, and AI coding agents may now make the saving worth it.
- Prompt coding agents explicitly for efficiency, since their training code defaults to inefficient patterns.

## Notes

### [00:36](https://youtu.be/bqwtnKLU35E?t=36) Green software and what architecture means here

Green software means cutting energy, carbon, and cost together through design. Architecture here means the hard-to-reverse decisions with no undo button after implementation. The session promises a catalog of sustainability trade-offs against maintainability, portability, availability, and performance.

### [04:17](https://youtu.be/bqwtnKLU35E?t=257) Footprint ranking: devices, networks, data centers

The quiz answer: devices dwarf networks and data centers (over 30 billion devices against 8 billion people; data centers smallest on the last two years of data). AI growth may reorder this. The priority advice follows: cut device footprint first.

### [07:29](https://youtu.be/bqwtnKLU35E?t=449) Devices: keep phones alive longer

A smartphone carries about 80% of its lifetime carbon in manufacturing, so stretching replacement to four or five years spreads the embodied cost. Software forces upgrades two ways: dropped OS and API support, and apps growing slow and crash-prone. Counter-moves: frugal apps for old specs, thin clients (Facebook Lite renders screens server-side, supporting Android phones back to 2009 over 2G), or native apps. Shopify rewrote its React Native apps natively with AI coding agents and reported 50% faster startup on Android, 23% on iOS, and 10 times fewer crashes. Trade-off: device footprint against development and testing effort, though agents are shrinking that cost.

### [16:56](https://youtu.be/bqwtnKLU35E?t=1016) Networks: compress, cache, process locally

Compress (check the ratio first; both ends pay CPU), cache locally or via a CDN (storage pays), or process at the edge (needs capable hardware, which fights device longevity).

### [22:18](https://youtu.be/bqwtnKLU35E?t=1338) Data centers: PUE, WUE, and carbon intensity

Pick regions on three metrics: PUE (1.0 ideal), WUE, and grid carbon intensity. Azure PUE is near-tied across regions (1.28 Asia Pacific, 1.16 EMEA and Americas), but WUE splits them: EMEA uses far less water. Low PUE can mean high WUE, since water cooling replaces air conditioning; a solar-powered desert site should save water over power. Electricity Maps shows live grid intensity per country, and Google's Cloud Region Picker weights carbon, price, and latency. Moving workloads from Ireland to Sweden is presented as an 87% emissions cut plus 5% lower cost. Trade-off: greener regions can cost more or add latency.

### [34:57](https://youtu.be/bqwtnKLU35E?t=2097) Availability: airliners versus fighter jets

Airliners carry triple redundancy at the price of weight and speed; fighter jets trade it for performance plus an ejector seat. Most software is the airliner: active-standby setups can leave up to 50% of servers idle. The alternative is designing for restart: a Terraform script boots a replacement VM or container on failure. Four nines allows 4 minutes 22 seconds of monthly downtime, covering two failures if a VM takes 2 minutes to start. Trade-off: sustainability and cost against the users' downtime budget.

### [40:48](https://youtu.be/bqwtnKLU35E?t=2448) ARM servers and closing

ARM server processors (AWS Graviton, Google Axion, Azure Cobalt, Ampere) use up to 60% less electricity than comparable x86, and lower heat also cuts cooling load. Adoption lags on porting effort and doubled pipelines for mixed fleets; AI agents change that math. Closing reminders: prioritize devices over networks over data centers, weigh sustainability against the other ilities, and re-check old decisions since agents shift the trade-offs.

### [46:06](https://youtu.be/bqwtnKLU35E?t=2766) Q&A: agent energy payback and efficient code

Agent energy is spent once while savings accrue over years of large-scale use, per the speaker's own bare-metal measurements with open models. Agents default to inefficient code from feature-first training data; the fix is explicit prompting for optimal algorithms and minimal CPU and memory use.

## Tools, libraries and specs

- Electricity Maps (live grid carbon intensity per country)
- Google Cloud Region Picker (cloud.withgoogle.com/region-picker; weights carbon, price, latency per traffic origin)
- Terraform (example: restart replacement infrastructure on failure)
- AWS Graviton, Google Axion, Azure Cobalt, Ampere (ARM server processors)
- Facebook Lite (thin-client precedent for old Android hardware)

## Who should watch

Architects and senior developers who choose regions, redundancy models, or client strategies and want sustainability added to those decisions with explicit trade-offs. Skip it if you already work from Green Software Foundation material and want measurements or code rather than a decision framework.

## Verdict

**6/10**: A trade-off catalog across devices, networks, data centers, availability and ARM servers, with the PUE/WUE and four-nines reasoning explained in depth; the figures are cited from others without method and nothing is run end to end or published.

**Reach broad**: most backend teams deploying to the public cloud can use the region, redundancy, and server choices in their own work within the next year.

**Novelty 1/2**

- **+** [15:54](https://youtu.be/bqwtnKLU35E?t=954) The recurring trade-off framing (device footprint against maintainability and testability) brings several credited sources into one decision catalog.
- **+** [11:41](https://youtu.be/bqwtnKLU35E?t=701) Facebook Lite is brought in as a thin-client precedent for old Android hardware (screens rendered on the server, phones back to 2009, usable on 2G), tying the device-lifetime argument to a shipped product.
- **·** [47:11](https://youtu.be/bqwtnKLU35E?t=2831) The speaker's own bare-metal measurements of agent energy against long-run savings are mentioned in one sentence with no figures or setup shown.

**Demonstrated 1/2**

- **+** [32:15](https://youtu.be/bqwtnKLU35E?t=1935) The Google Cloud Region Picker's recommendation list for Belgium traffic is on screen while the speaker explains how the carbon, price and latency sliders change it.
- **·** [30:44](https://youtu.be/bqwtnKLU35E?t=1844) Electricity Maps is shown in a browser with Belgium's grid mix pointed out, but only as an illustration and not worked through to a region choice, which fits a strategy talk with no demo slot.

**Measured 1/2**

- **+** [14:19](https://youtu.be/bqwtnKLU35E?t=859) Shopify's native rewrite is quoted with before/after figures: 50% faster Android startup, 23% on iOS, 10 times fewer crashes.
- **−** [33:21](https://youtu.be/bqwtnKLU35E?t=2001) The Ireland-to-Sweden move (87% lower emissions, 5% lower cost) is introduced as "a possible scenario" with no method or data behind it.
- **−** [41:21](https://youtu.be/bqwtnKLU35E?t=2481) The "up to 60% less electricity" for ARM servers carries no source, baseline or method.

**Depth 2/2**

- **+** [27:00](https://youtu.be/bqwtnKLU35E?t=1620) The Azure chart shows regions tied on PUE but split on WUE, and the speaker then weighs a low-water against a low-power data center for a sunny desert site.
- **+** [39:09](https://youtu.be/bqwtnKLU35E?t=2349) The four-nines monthly downtime budget is turned into a restart-instead-of-standby design: a two-minute VM start allows two failures a month.
- **−** [18:00](https://youtu.be/bqwtnKLU35E?t=1080) The compression trade-off is left at "check the ratio" with no threshold or way to measure it.

**Reusable 1/2**

- **+** [38:38](https://youtu.be/bqwtnKLU35E?t=2318) The Terraform restart-on-failure pattern is described as a script that starts a replacement instance on failure, a fragment for viewers to reconstruct for standby-free recovery.
- **·** [45:00](https://youtu.be/bqwtnKLU35E?t=2700) The closing gives three reminders, and neither the trade-off catalog nor the book mentioned at [01:39](https://youtu.be/bqwtnKLU35E?t=99) is pointed to as a checklist or repository.
