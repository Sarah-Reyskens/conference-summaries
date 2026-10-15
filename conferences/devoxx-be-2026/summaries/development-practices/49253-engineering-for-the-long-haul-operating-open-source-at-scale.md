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
verdict: 2
frames: 9
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
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

**2/10**: A sales catalog of one vendor's portfolio with self-reported totals and nothing running on screen, useful only as a buyer's overview.

**Novelty 0/2**

- **−** The lineup, SLA table, and pipeline match what a search for TuxCare SecureChain, ELS, and KernelCare returns from tuxcare.com/securechain-for-oss and docs.tuxcare.com/securechain.
- **−** [27:51](https://youtu.be/Pg5kS8l9CpI?t=1671) The only first-hand examples, a CentOS server never rebooted in 8 years and an unnamed customer's legacy server still under support, carry no names or detail.
- **·** [02:08](https://youtu.be/Pg5kS8l9CpI?t=128) The survey figures are credited on the slide to TuxCare's 2026 landscape report (the YoY-growth card to StackWatch), which is credited background and no fault.

**Demonstrated 0/2**

- **−** [11:04](https://youtu.be/Pg5kS8l9CpI?t=664) The SecureChain pipeline is narrated over slides; no package, scan result, or patched install appears on screen.
- **−** [24:10](https://youtu.be/Pg5kS8l9CpI?t=1450) Rebootless patching is claimed for 24/7 systems, but no live patch run or before/after kernel state is shown.

**Measured 1/2**

- **+** [02:08](https://youtu.be/Pg5kS8l9CpI?t=128) The quiz puts survey percentages on incidents, unapplied patches, and downtime constraints on screen.
- **−** [02:08](https://youtu.be/Pg5kS8l9CpI?t=128) No method, sample size, or baseline accompanies the percentages.
- **−** [31:01](https://youtu.be/Pg5kS8l9CpI?t=1861) The closing totals (2,700+ clients, 420,000+ patches, 14,000+ vulnerabilities fixed) are self-reported, and the spoken "more than 5,000 CVE patched to date" disagrees with the slide's 14,000+.

**Depth 1/2**

- **+** [13:09](https://youtu.be/Pg5kS8l9CpI?t=789) The SecureChain pipeline (trusted catalog, malware scan, rebuild from source, SLSA Level 3 SBOM and VEX) gives a beginner-level mental model of how a package moves through the product.
- **+** [24:44](https://youtu.be/Pg5kS8l9CpI?t=1484) Reboots interrupt services that must run 24/7 and need maintenance windows, which gives the case for choosing rebootless patching.
- **−** [24:10](https://youtu.be/Pg5kS8l9CpI?t=1450) Why an in-memory kernel patch avoids a reboot goes unexplained beyond "live in memory".

**Reusable 0/2**

- **−** [16:20](https://youtu.be/Pg5kS8l9CpI?t=980) The integration segment gives one line ("Point your repository manager or package manager at secure chain") and no repository, sample configuration, trial, or checklist.
- **−** [20:30](https://youtu.be/Pg5kS8l9CpI?t=1230) "Our website" and "CVE trackers" are mentioned without a URL or name.
