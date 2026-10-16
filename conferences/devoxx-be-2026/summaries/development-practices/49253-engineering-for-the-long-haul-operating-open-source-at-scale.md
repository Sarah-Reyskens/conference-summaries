---
title: "Engineering for the Long Haul: Operating Open Source at Scale"
talkId: "49253"
conference: devoxx-be-2026
speakers: [Sven Sellen]
track: Development Practices
sessionType: Lunch Talk
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=Pg5kS8l9CpI
durationMin: 33
slides: null
verdict: 4
reach: niche
frames: 9
summarizedAt: 2026-10-14
reviewedAt: 2026-10-15
---

# Engineering for the Long Haul: Operating Open Source at Scale

Sven Sellen · Lunch Talk · Development Practices

## TL;DR

TuxCare's enterprise sales director pitches the company's open-source security portfolio: SecureChain for supported packages, Extended Lifecycle Support for end-of-life systems, and rebootless kernel and library patching. Nothing is shown running; every product is described over marketing slides.

## Key takeaways

- Vendors that backport security fixes after upstream support ends exist because production systems outlive their upgrade windows.
- SecureChain rebuilds packages from source, scans for malware, and ships CVE fixes with SBOM and VEX artifacts for JavaScript, Python, and Java, transitive dependencies included.
- Stated fix SLAs are 7 calendar days for critical CVEs on supported packages and 14 under ELS; typical critical delivery is claimed at 48 to 72 hours.
- KernelCare and LibraryCare patch kernels and libraries in memory without reboots for systems that cannot take maintenance windows.
- AlmaLinux, built by CloudLinux (TuxCare's parent) and transferred to a community foundation, gets enterprise support tiers including FIPS-oriented hardening.

## Notes

### [02:08](https://youtu.be/Pg5kS8l9CpI?t=128) Patching statistics as a quiz

Audience members guess figures from the TuxCare 2026 Enterprise Linux and Open-Source Landscape Report (the YoY vulnerability-growth card is sourced to StackWatch): 48% of open-source-using organizations suffered an incident in 12 months, 69% of incidents traced to unapplied patches, 93% knew they were vulnerable beforehand, 43% cannot take systems offline to patch.
### [06:21](https://youtu.be/Pg5kS8l9CpI?t=381) Threat landscape

One vulnerability lived 25 years in production undetected; AI-discovered flaws are already exploited in the wild. End-of-life patterns: calendar-driven LTS, latest-only moving targets, abandonment by silence. Supply-chain points: a self-replicating npm worm from stolen maintainer tokens, 455,000 new malicious packages in a year, EU CRA and PCI DSS pressure landing on the user.

### [11:04](https://youtu.be/Pg5kS8l9CpI?t=664) SecureChain for supported packages

SecureChain verifies packages before install, rebuilds from source, and ships fixes with SLSA Level 3 SBOMs and VEX data; EOL packages roll into ELS. Adopters point Artifactory, Nexus, or GitHub Packages at it with no agent and no CI/CD rewrites. JavaScript, Python, and Java are live; Go, Rust, and PHP were planned for the following quarter.

### [18:55](https://youtu.be/Pg5kS8l9CpI?t=1135) Extended Lifecycle Support

ELS covers operating systems (CentOS, RHEL, Oracle, Amazon, Debian, Ubuntu), runtimes (Java, PHP, .NET), libraries, and applications, transitive dependencies included, verified via OVAL definitions and OpenSCAP. Anything open source but unlisted can be requested; one customer is still carried on CentOS 6.

### [24:10](https://youtu.be/Pg5kS8l9CpI?t=1450) Rebootless patching

Kernel patches apply in memory with zero downtime; LibraryCare extends this to userspace libraries. Supported: AlmaLinux, RHEL 6-9, CentOS, Oracle, Amazon, Ubuntu, Debian, Alpine, CloudLinux OS, Rocky, Proxmox VE. Headline anecdote: a CentOS server ran 8 years until the hardware went end of life.

### [29:27](https://youtu.be/Pg5kS8l9CpI?t=1767) Why TuxCare, by the numbers

TuxCare split from 17-year-old CloudLinux into its own company on 1 January. Closing claims: 2,700+ enterprise clients, 36,000+ packages curated, 420,000+ patches delivered, 14,000+ vulnerabilities fixed, 11,000+ kernels continuously patched, 70+ distro versions supported. Ends 8 minutes early.

## Tools, libraries and specs

- TuxCare SecureChain, ELS, KernelCare, LibraryCare
- AlmaLinux, CloudLinux OS
- SBOM, VEX, SLSA Level 3, OVAL/OpenSCAP, FIPS

## Who should watch

Managers evaluating commercial EOL support or live-patching vendors get a compact catalog of one vendor's offering. Engineers wanting internals, self-serve hardening, or comparisons can skip it: the material stays at brochure level.

## Verdict
+
**4/10**: A vendor tour with a usable pipeline model and on-screen survey figures, nothing running, and a lineup a search already returns.
+
**Reach niche**: Only audience members whose organizations would buy commercial EOL support or live patching from this vendor can use its main content within the next year.
+
**Novelty 1/2**
+
- **+** [21:31](https://youtu.be/Pg5kS8l9CpI?t=1291) A customer is still carried on CentOS 6 because the server is too important to upgrade, one of the speaker's own cases of a system outliving its upgrade window.
- **+** [27:51](https://youtu.be/Pg5kS8l9CpI?t=1671) A customer never rebooted a CentOS server until the hardware reached end of life after 8 years.
- **−** The SecureChain pipeline, SLA table, and ELS lineup match what a search for TuxCare SecureChain, ELS, and KernelCare returns from tuxcare.com/securechain-for-oss and docs.tuxcare.com/securechain.
+
**Demonstrated 0/2**
+
- **−** [11:04](https://youtu.be/Pg5kS8l9CpI?t=664) The SecureChain pipeline is narrated over slides, with no package, scan result, or patched install appearing on screen.
- **−** [24:10](https://youtu.be/Pg5kS8l9CpI?t=1450) Rebootless patching is claimed for systems that must run around the clock, with no live patch run or before/after kernel state shown.
+
**Measured 1/2**
+
- **+** [02:08](https://youtu.be/Pg5kS8l9CpI?t=128) The quiz puts survey percentages on incidents, unapplied patches, and downtime constraints on screen.
- **−** [02:08](https://youtu.be/Pg5kS8l9CpI?t=128) No method, sample size, or baseline accompanies the percentages.
- **−** [31:01](https://youtu.be/Pg5kS8l9CpI?t=1861) The closing totals are self-reported, and the spoken "more than 5,000 CVE patched to date" disagrees with the slide's 14,000+.
+
**Depth 1/2**
+
- **+** [13:09](https://youtu.be/Pg5kS8l9CpI?t=789) The SecureChain pipeline (trusted catalog, malware scan, rebuild from source, SLSA Level 3 SBOM and VEX) gives a beginner-level mental model of how a package moves through the product.
- **+** [24:44](https://youtu.be/Pg5kS8l9CpI?t=1484) Reboots interrupt services that must run around the clock and need maintenance windows, which gives the case for choosing rebootless patching.
- **−** [25:45](https://youtu.be/Pg5kS8l9CpI?t=1545) LibraryCare's userspace live patching is named as "rebootless live in memories" with no mechanism beyond the label.
+
**Reusable 1/2**
+
- **+** [16:20](https://youtu.be/Pg5kS8l9CpI?t=980) The integration is one stated step: point Artifactory, Nexus or GitHub Packages at SecureChain, with no agent and no CI/CD rewrite.
- **+** [19:26](https://youtu.be/Pg5kS8l9CpI?t=1166) The fixes are hosted in the vendor's own repository, which subscribers can reach: the presented product's distribution.
- **−** [20:30](https://youtu.be/Pg5kS8l9CpI?t=1230) "Our website" and "CVE trackers" are mentioned without a URL or name, and no trial, sample configuration or checklist is offered.
