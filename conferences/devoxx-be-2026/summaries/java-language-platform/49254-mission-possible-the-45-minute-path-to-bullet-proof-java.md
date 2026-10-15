---
title: "Mission Possible: The 45-Minute Path to Bullet-Proof Java Container Images"
talkId: "49254"
conference: devoxx-be-2026
speakers: [Pasha Finkelshtein]
track: Java Language & Platform
sessionType: Lunch Talk
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=1yndLHw9mbo
durationMin: 43
slides: null
verdict: 6
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Mission Possible: The 45-Minute Path to Bullet-Proof Java Container Images

Pasha Finkelshtein · Lunch Talk · Java Language & Platform

## TL;DR

Chasing zero CVEs in Java container images is a losing game against a daily vulnerability feed, so the goal should be zero unmanaged risk: every CVE either patched or explicitly accepted by a named owner with an expiry date. Five steps get there (limit privileges, shrink the attack surface, classify by context, patch what is left, prove it to an auditor), and the talk closes with a published hardening checklist to run the same process on one production image.

## Key takeaways

- Run containers as a non-root user with all capabilities dropped, no-new-privileges, and a read-only filesystem plus tmpfs on /tmp; it needs no rebuild and shrinks the blast radius of any exploit.
- Ship a JRE, not a JDK, in a multi-stage build on a minimal base: the same app went from 46 CVEs and 1 GB to 7 CVEs and 200 MB on that change alone.
- Triage by context starting from the CVSS score: escalate what is internet-facing, on the hot path, or allows lateral movement, and de-escalate what is unreachable, behind a control you own, or contained.
- Never hide unfixed vulnerabilities with flags like Trivy's --ignore-unfixed; an accepted risk must carry an owner, a reason, and an expiry date.
- Someone must own the base image under a patch SLA, whether an internal team or a vendor; onboarding takes about a month, maintenance takes many hours a week, and backports cost days each time.
- Pin base images by digest, verify signatures with cosign before building on top, ship split SBOMs for OS/runtime versus app dependencies, and let Renovate open the update PRs.

## Notes

### [00:36](https://youtu.be/1yndLHw9mbo?t=36) The CVE flood and what it costs

Most of the room ships Java in containers, but only a handful own their base image. CVE feeds are the water dripping into that room: databases of known vulnerabilities in everything from zlib to Spring. A naive single-stage Dockerfile on Eclipse Temurin 25, scanned in early August 2026, held 46 CVEs (1 critical, 3 high, 18 medium, 24 low): 42 from the base image and 4 from application dependencies, meaning libraries, not hand-written code. None came from Java itself; every major vendor ships a zero-CVE runtime. The offenders were things like libssl 3.0.13 (fixed only in 3.0.14) and zlib 1.3.1. By talk time the Temurin 25 base alone carried 135 CVEs, and the deprecated Docker Hub OpenJDK 21 image had 132. The speaker warned never to use those OpenJDK Hub images in production: they are unofficial preview builds. About 6% of published CVEs were exploited in the wild (2024 data, with AI pushing the rate up), the average breach costs $4.4M ($10M in the US, IBM 2025), and under the EU Cyber Resilience Act the auditors will remember.

### [09:34](https://youtu.be/1yndLHw9mbo?t=574) The mission: zero unmanaged risk

The objective is not zero CVEs but zero unmanaged risk, where each CVE is fixed or accepted by a named owner with an expiry date. The five steps: limit privileges so failures stay small, shrink the attack surface, classify vulnerabilities by context, patch what is left, and prove it all to an auditor, internal or external.

### [11:37](https://youtu.be/1yndLHw9mbo?t=697) Step 1: limit privileges

Add a USER directive (numeric IDs like 1234:1234 are fine), never grant --privileged access to the host, drop all Linux capabilities and add back only needed ones such as net_bind_service, set no-new-privileges, and mount the filesystem read-only with a tmpfs on /tmp since apps like Spring Boot still need to write there. These flags apply to the image shipping today with no rebuild and no code changes.

### [15:17](https://youtu.be/1yndLHw9mbo?t=917) Step 2: shrink the attack surface

A JDK is a build tool: shipping javac hands an attacker a complete programming language, so production should get a JRE (about 40 modules, no compiler or debugger) or a jlink-cut runtime with only the modules the app uses. Use multi-stage builds and minimal bases such as Alpine, Alpaquita, Wolfi, or UBI, noting they are not equally well maintained. Rewriting the naive Dockerfile as a multi-stage JRE build took the example app from 46 CVEs to 7 and from 1 GB to 200 MB, leaving 3 base-image CVEs (1 critical, 1 high, 1 medium) plus the 4 dependency ones.

### [19:29](https://youtu.be/1yndLHw9mbo?t=1169) Step 3: classify by context, not just CVSS

A CVSS score knows neither your code paths nor reachability nor whether a fix exists. Spring4Shell scored 9.8 but was exploitable only for WAR-packaged apps deployed to standalone Tomcat, a setup almost nobody in the room still used, so most teams could accept it outright. Sorting by CVSS alone means sorting by someone else's worst case. The talk's rule set: escalate internet-facing, hot-path, or lateral-movement-enabling findings; de-escalate what is unreachable from outside, behind an owned control, or contained in one service. A libssl CVE at 9.1 with internet-facing TLS termination and an available patch means patch now; lower exposure waits for the next planned update; non-exploitable findings get accepted; and findings with no patch go to step 4.

### [26:20](https://youtu.be/1yndLHw9mbo?t=1580) Step 4: patch what is left, and decide who owns it

Debian Bookworm still ships zlib 1.2.13 with a 2023 critical CVE marked "will not fix", even though upstream fixed it in 1.3.1 in January 2024. The patch chain explains the lag: NVD publication, upstream fix over hours to weeks, distro packaging, base-image refresh on the distro cadence, and only then your rebuild. A free image is a gift, not a commitment. An audience vote showed most would ship and accept the risk. Shift-left does not mean every developer becomes an amateur OS maintainer: the speaker backported one patch with AI help and called it a struggle. Cost estimates per step: non-root plus capabilities takes days (weeks at eBay scale), minimal base plus multi-stage takes days to weeks, CI scanning plus triage costs hours weekly, monthly JDK updates cost about a day with regression tests, signing/SBOM/provenance costs a week to set up plus an hour a week, and each backport costs days. Onboarding runs about a month; maintenance is many hours a week forever. Whoever owns the base layer must show OS plus runtime expertise, ship signed evidence, commit to a patch SLA with a number, and build components from source.

### [36:53](https://youtu.be/1yndLHw9mbo?t=2213) What a hardened base ships

A hardened base is trusted (low-to-zero CVEs by design, patched continuously), transparent (SBOM inside, no shell or package manager, immutable component set), and verifiable (signed and attested, provenance checkable against a public key). From 11 December 2027, the EU CRA obliges vendors to hand over SBOMs on demand. Moving the PetClinic example to a distroless-style JRE 25 runtime stage produced zero OS-scanner CVEs at roughly the same size, with a signed image plus SBOM.

### [38:26](https://youtu.be/1yndLHw9mbo?t=2306) Step 5: prove it, then automate

Answer three auditor questions: image origin via signatures, contents via SBOMs, and build provenance via attestations recording the commit. Pin images by digest because tags move; always using latest gets free patches with untested changes, while pinning ships what was tested but waits for patches, so pin what was tested and automate the update proposal. Run cosign verify before building on any base, keep OS/runtime and application-dependency SBOMs split but stored together, and generate app SBOMs with the CycloneDX Maven or Gradle plugin for fast reproducible scanning. Hardened is not permanent: suppliers keep patching while pipelines sleep, so Renovate watches base-image digests and opens PRs with automated tests. The Monday homework: scan one production image, find its SLA owner, triage instead of counting criticals, and build the process for that one service. The closing slide links the checklist at asm0dey.github.io/docker-hardening-checklist.

## Tools, libraries and specs

- Trivy (image and SBOM scanning, --ignore-unfixed flag discussed)
- Cosign (cosign verify for base-image signatures)
- CycloneDX Maven/Gradle plugins (application SBOM generation)
- Renovate (automated base-image digest update PRs)
- jlink (module-trimmed Java runtimes)
- Eclipse Temurin 25 JDK/JRE (example base, 46 CVEs naive vs 7 multi-stage)
- OpenJDK 21 Docker Hub images (deprecated, unofficial preview builds)
- Spring Boot PetClinic (example application)
- zlib 1.2.13 / 1.3.1, libssl 3.0.x (worked vulnerability examples)
- Debian Bookworm, Alpine, Alpaquita, Wolfi, UBI (base distributions compared)
- EU Cyber Resilience Act (SBOM duty from 2027-12-11)

## Who should watch

Java developers who ship containers without knowing who maintains their base image, and teams drowning in scanner output with no triage process, will get a full playbook plus an ownership cost model to take to management. Leads weighing DIY hardening against a managed image or vendor SLA get the decision arithmetic. Skip it if signed minimal images, contextual triage, and automated base updates are already routine, or if you want hands-on backporting or scanner internals rather than the process view.

## Verdict

**6/10**: before/after scan numbers on one app and a triage-and-ownership model carry it, but nothing runs on screen and the checklist it points to covers only part of the five steps.

**Novelty 1/2**

- **+** [26:20](https://youtu.be/1yndLHw9mbo?t=1580) The Debian Bookworm zlib "will not fix" case, rechecked the day of the talk with upstream fix version and sources on the slide, grounds the ownership argument in a checked example.
- **+** [31:38](https://youtu.be/1yndLHw9mbo?t=1898) A per-step onboarding and maintenance cost account from someone who builds hardened images turns the DIY-versus-vendor question into arithmetic.
- **−** The core practices (non-root user, dropped capabilities, multi-stage builds, minimal bases, signing) are the Docker security docs and CIS Docker Benchmark baseline.

**Demonstrated 0/2**

- **−** [03:44](https://youtu.be/1yndLHw9mbo?t=224) The 46-CVE scan result is reported on a slide; no scanner run appears on screen.
- **−** [18:27](https://youtu.be/1yndLHw9mbo?t=1107) The 46-to-7 CVE and 1 GB-to-about-180 MB multi-stage improvement is stated, not built or scanned live.
- **−** [37:24](https://youtu.be/1yndLHw9mbo?t=2244) The zero-CVE hardened result is claimed on a slide with no visible verification run.

**Measured 2/2**

- **+** [04:49](https://youtu.be/1yndLHw9mbo?t=289) The 46 CVEs come broken down by severity with base-versus-app attribution (42 base, 4 dependencies), and the same base image is later shown at 135.
- **+** [18:27](https://youtu.be/1yndLHw9mbo?t=1107) The same app is compared before and after the Dockerfile change, both Dockerfiles on slides: 46 to 7 CVEs and 1 GB to about 180 MB.
- **−** [08:01](https://youtu.be/1yndLHw9mbo?t=481) The 6% share of published CVEs exploited in the wild is restated as a 6% chance of being hacked with 100 CVEs in an image, which that figure does not give.

**Depth 2/2**

- **+** [22:38](https://youtu.be/1yndLHw9mbo?t=1358) The escalate and de-escalate rules, motivated by Spring4Shell's 9.8 score being exploitable only as a WAR on standalone Tomcat, give a working model for adjusting CVSS with local context.
- **+** [39:00](https://youtu.be/1yndLHw9mbo?t=2340) Pin-by-digest versus latest is weighed as tested builds against free patches, resolved by automating the update proposal.
- **+** [27:53](https://youtu.be/1yndLHw9mbo?t=1673) The five-link patch lifecycle explains why fixes lag and why ownership needs an SLA.

**Reusable 1/2**

- **+** [42:07](https://youtu.be/1yndLHw9mbo?t=2527) The closing slide points to a published hardening checklist (URL plus QR code) with privilege-removal, scanning, patching and maintenance-cadence sections.
- **−** [42:38](https://youtu.be/1yndLHw9mbo?t=2558) The checklist is an Alpine handout for a different talk and has no triage, digest pinning, signing, SBOM or attestation section and nothing on JRE or jlink, though the speaker says every step has a checklist.
