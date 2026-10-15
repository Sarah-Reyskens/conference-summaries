---
title: CRAcking Compliance - The EU Cyber Resilience Act
talkId: "4051"
conference: devoxx-be-2026
speakers: [Christian Schabetsberger]
track: Security, Trust & Compliance
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=QQcsZNf0eWs
durationMin: 45
slides: null
verdict: 8
frames: 12
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---
# CRAcking Compliance - The EU Cyber Resilience Act
Christian Schabetsberger · Conference · Security, Trust & Compliance

## TL;DR
The EU Cyber Resilience Act makes secure-by-design engineering legally mandatory for most products with digital elements sold in the EU, with full effect from 11 December 2027. The talk maps the act's requirements onto concrete engineering practice: threat-model your risk assessment, generate and verify an SBOM, scan for vulnerabilities continuously, automate dependency updates, and shrink your attack surface.

## Key takeaways
- Treat the CRA as law-backed good practice: risk assessment, dependency tracking, vulnerability monitoring and patching become legal obligations, not optional hygiene.
- Run your own continuous risk assessment as threat modeling (four questions plus STRIDE), document it, and keep it updated through the whole support period of at least 5 years.
- Generate an SBOM in CycloneDX or SPDX, but verify the output: six tools run against the same empty Angular project reported between 6 and 555 components.
- Track transitive dependencies for vulnerability scanning even though the act strictly requires only direct ones, since they ship in your deliverable.
- Automate updates with Renovate or Dependabot using grouped updates and a delay (24 hours, GitHub uses 72) so a compromised release does not land in your tree immediately.
- Reduce what you ship: inline trivial unmaintained code, drop unused dependencies, and use distroless or minimal container images to shrink the attack surface.

## Notes
### [00:36](https://youtu.be/QQcsZNf0eWs?t=36) Intro and disclaimer
Schabetsberger, a freelance software engineer and architect from Linz, Austria, opens with a disclaimer: he is not a lawyer, and legal questions belong to attorneys. He runs a bit for the session: every time he says "it depends", the audience asks "on what".

### [02:38](https://youtu.be/QQcsZNf0eWs?t=158) CRA basics and timeline
The Cyber Resilience Act is an EU act (no national implementation step, unlike NIS2) with the goal of security by design for all digital products. It entered into force on 10 December 2024 with a three-year grace period, so it applies in full from 11 December 2027.

### [04:08](https://youtu.be/QQcsZNf0eWs?t=248) Who is affected
It covers all companies putting products with digital elements into circulation: hardware, software, and remote data processing required for the product to function (such as a mobile app backend). Exemptions are narrow: products under more specific law (lex specialis, e.g. medical devices, cars), non-commercial products, and company size or revenue grant no exemption. Larger open-source organizations must nominate an open-source software steward and comply with a light version; the Apache and Linux Foundations are expected to be affected. Pure SaaS outside these categories may fall under DORA (finance) or NIS2 (energy, water, transport, digital infrastructure at 50 employees or 10M EUR revenue, or essential/important entities regardless).

### [06:45](https://youtu.be/QQcsZNf0eWs?t=405) Core principles
Products must be secure by design and secure by default: no shipping with known vulnerabilities. Manufacturers must monitor actively and ship free security patches for the product lifespan (self-defined, at least 5 years unless the Commission sets other minima), deliver updates securely (signed where the platform supports it), and inform customers of vulnerabilities and updates. Automatic updates with an opt-out are the guideline; B2B products fall back to notification-based maintenance windows.

### [09:22](https://youtu.be/QQcsZNf0eWs?t=562) Product categories and conformity
Default category (~90% of products): self-assessment, then affix the CE mark. Important class I products (OS, database engine, Wi-Fi router): follow the harmonised standards (17 ETSI drafts exist, none finalised) or get a third-party assessment. Important class II (firewall, hypervisor): mandatory third-party assessment. Critical products (smart cards, smart meter gateways): EU Common Criteria certification. Annex 3 lists the classifications; certification bodies opened in June 2026.

### [11:55](https://youtu.be/QQcsZNf0eWs?t=715) Documentation and risk assessment
Annex 2 requires a vulnerability contact point, an EU declaration of conformity, and secure-use instructions; Annex 7 requires technical documentation including the vulnerability-handling process and architecture diagrams. Article 13 requires a cybersecurity risk assessment whose outcome feeds back into design, development, production, maintenance and delivery, kept current over the whole support period. Annex 1 requirements are all prefixed "on the basis of the cybersecurity risk assessment" and "where applicable", so no fixed checklist can make a product compliant, but the assessment itself is the documented reasoning behind each decision.

### [14:31](https://youtu.be/QQcsZNf0eWs?t=871) Threat modeling as risk assessment
The recommendation is threat modeling via Adam Shostack's four questions: what are we building (whiteboard the data flows and trust boundaries), what can go wrong, what are we going to do about it (fix, mitigate, or consciously accept with an owner), and did we do a good enough job (revisit every iteration). STRIDE maps almost one to one onto the Annex 1 essential requirements. Tooling options include OWASP Threat Dragon and the Microsoft Threat Modeling Tool, but a photographed whiteboard checked into the repo beats a perfect model never made.

### [18:05](https://youtu.be/QQcsZNf0eWs?t=1085) SBOM formats
The act requires tracking product dependencies in a machine-readable SBOM. The two formats are SPDX (Linux Foundation, licensing roots) and CycloneDX (OWASP, security roots); either is acceptable and an Excel list is not. The speaker uses CycloneDX mostly, SPDX in one project.

### [20:08](https://youtu.be/QQcsZNf0eWs?t=1208) Vulnerability reporting deadlines
On learning of a vulnerability: an early warning within 24 hours (24/7, weekends included), a full notification within 72 hours, then a final report within 14 days for actively exploited vulnerabilities or one month for severe incidents. Reports go to the ENISA single reporting platform, live since September 2026; these obligations already applied from 11 September 2026. A screenshot shows the notification form's fields.

### [22:13](https://youtu.be/QQcsZNf0eWs?t=1333) What counts as a dependency
Direct dependencies are certain; transitive dependencies ship in the deliverable and must be scanned even though only direct ones are strictly required in the SBOM. Dev-only dependencies are lower risk but worth including if the tooling does it; compilers, operating systems and CI infrastructure form a second, environmental category usually owned by IT teams.

### [24:50](https://youtu.be/QQcsZNf0eWs?t=1490) SBOM tooling landscape
Free options abound: GitHub dependency graph (and a similar GitLab feature), `npm sbom`, the CycloneDX ecosystem (npm CLI, esbuild plugin, .NET tool, Maven/Gradle plugins), Syft, Microsoft's sbom-tool (SPDX only), and Trivy (SBOM as a side product). On a customer .NET project the GitHub graph initially missed transitive dependencies (no lock file without restore) and mishandled Central Package Management, producing a wrong SBOM that needed CI actions to fix.

### [27:59](https://youtu.be/QQcsZNf0eWs?t=1679) SBOM tool comparison on an empty Angular app
Six tools on the same empty Angular project gave: npm sbom 450, CycloneDX npm 423 unique (duplicates multi-version packages), CycloneDX esbuild 6 (only transpiled packages, minus tree-shaking), Syft 32 (package.json only, plus stray GitHub Actions picked up from node_modules), sbom-tool 453 (SPDX root node accounts for the difference), GitHub dependency graph 555 (includes all optional OS dependencies, tested server-side while the rest ran locally). The slide marks all as differing; the lesson is that no tool is a silver bullet, so verify the output and combine tools by stack and purpose. Syft did better on a .NET project, suggesting its JavaScript analyzer is the weak spot.

### [32:08](https://youtu.be/QQcsZNf0eWs?t=1928) Vulnerability scanning
Options: `npm audit` (with fix), `dotnet package list --vulnerable` (runs on every restore, but warnings get ignored), OWASP Dependency-Check (Maven/Gradle plugin or CLI, HTML report for CI), Trivy, Grype, and self-hosted OWASP Dependency-Track (API plus dashboard, CycloneDX only). For a Yocto-based embedded Linux project on SPDX, the team wrote a converter to CycloneDX to feed Dependency-Track and also uses it for license tracking. The advice is a dedicated scanning pipeline with visualization, since developers and CI ignore restore-time warnings.

### [35:47](https://youtu.be/QQcsZNf0eWs?t=2147) Dependency debt and support lifecycles
Dependency debt grows exponentially, and maintainers owe no backported security fixes while manufacturers now owe patches: staying near latest is the only viable default. Support windows keep shrinking (.NET: 2 years standard, 3 years LTS; Spring Boot: 12 months with two releases a year; Angular: 6 months active, 12 months LTS), so components with shorter lifespans than the product belong in the risk assessment. The proposed replacement for periodic modernization projects is continuous "software gardening".

### [38:21](https://youtu.be/QQcsZNf0eWs?t=2301) Automating updates
Renovate and Dependabot scan for outdated dependencies and open PRs with release notes; both run self-hosted or on Azure DevOps. Recommended configuration: grouped updates (all Microsoft, Angular, or internal packages in one PR), a merge delay (24 hours; GitHub moved to 72), and distinct handling of major versus minor versions, possibly security-only PRs. Auto-merge fits teams with strong test suites, at least for patches. Migration helpers: Angular schematics, OpenRewrite (especially Java), and LLMs. The speaker's own team of three and a half seniors treats updates as a no-discussion top-of-board task.

### [41:30](https://youtu.be/QQcsZNf0eWs?t=2490) Reducing dependencies
Every dependency is uncontrolled liability: the speaker inlined two classes from a dependency unmaintained for seven years (after checking the license) and dropped dependencies superseded by the standard runtime. Typical container images carry unneeded shells, package managers and network tools; distroless or minimal images shrink size, startup time and attack surface at some cost to debuggability. Docker Hardened Images have been free since December 2025.

### [43:01](https://youtu.be/QQcsZNf0eWs?t=2581) Recap
Five steps: assess risk and document it; track dependencies and keep an SBOM ready for auditors; scan for vulnerabilities, report and act; stay on supported versions with automated updates; reduce dependencies without reinventing the wheel. Closing argument: these were already good practice, and needing a law to enforce them means the industry failed its customers on quality and security.

## Tools, libraries and specs
- EU Cyber Resilience Act (full application 11 December 2027; reporting live 11 September 2026), Annex 1/2/3/7, Article 13
- ENISA single reporting platform
- NIS2, DORA (finance), CE marking, EU Common Criteria certification, ETSI drafts
- SPDX and CycloneDX SBOM formats
- npm sbom, CycloneDX npm CLI / esbuild plugin / .NET tool / Maven and Gradle plugins, Syft, Microsoft sbom-tool (SPDX only), GitHub dependency graph, Trivy
- npm audit, dotnet package list --vulnerable, OWASP Dependency-Check, Grype, OWASP Dependency-Track (CycloneDX only)
- Renovate, Dependabot (72-hour default delay on GitHub)
- STRIDE, Adam Shostack's four threat-modeling questions, OWASP Threat Dragon, Microsoft Threat Modeling Tool
- OpenRewrite, Angular migration schematics, Yocto, distroless/minimal images, Docker Hardened Images (free since December 2025)

## Who should watch
Engineers and architects whose products sell into the EU and need a first practical map from the CRA to engineering work, especially around SBOMs and dependency management. Viewers already running CRA compliance programs, or seeking legal interpretation rather than engineering practice, can skip it.

## Verdict
**8/10**: The speaker's own six-tool SBOM comparison and practitioner guidance carry a clear beginner CRA talk; no tool is run live and no artifact is published.

**Novelty 2/2**

- **+** [28:29](https://youtu.be/QQcsZNf0eWs?t=1709) Six SBOM tools run against the same empty Angular project report 450, 423, 6, 32, 453 and 555 components, with each discrepancy explained.
- **+** [26:56](https://youtu.be/QQcsZNf0eWs?t=1616) A customer .NET project shows the GitHub dependency graph producing a wrong SBOM through missed transitive dependencies and Central Package Management.

**Demonstrated 1/2**

- **+** [30:20](https://youtu.be/QQcsZNf0eWs?t=1820) The SBOM comparison table shows the actual component counts each of the six tools produced on screen.
- **+** [21:11](https://youtu.be/QQcsZNf0eWs?t=1271) The slide of the ENISA single reporting platform accompanies the speaker's walk-through of how a vulnerability notification is submitted.
- **−** [25:21](https://youtu.be/QQcsZNf0eWs?t=1521) The tooling survey names a dozen scanners and generators but none is run live or shown executing.

**Measured 2/2**

- **+** [28:29](https://youtu.be/QQcsZNf0eWs?t=1709) The six-tool comparison states its method (same empty Angular project, local runs except the server-side GitHub graph) and reports exact counts per tool.
- **+** [29:40](https://youtu.be/QQcsZNf0eWs?t=1780) The slide table breaks the counts down per tool so the disagreement is quantified, not asserted.
- **−** [34:46](https://youtu.be/QQcsZNf0eWs?t=2086) The speaker concedes long-term data across stacks is missing, so the numbers rest on one small experiment.

**Depth 2/2**

- **+** [15:01](https://youtu.be/QQcsZNf0eWs?t=901) The four threat-modeling questions plus STRIDE give beginners a working method for the legally required risk assessment.
- **+** [23:47](https://youtu.be/QQcsZNf0eWs?t=1427) The dependency-scope discussion weighs transitive and dev-only inclusion against strict legal minimums and tooling reality.
- **+** [39:23](https://youtu.be/QQcsZNf0eWs?t=2363) Update automation covers grouped updates, merge delays and major-versus-minor handling with configuration values.

**Reusable 1/2**

- **+** [39:23](https://youtu.be/QQcsZNf0eWs?t=2363) Renovate and Dependabot practices are specified enough to reconstruct: grouping, 24-hour delay, security-only PRs.
- **−** [44:35](https://youtu.be/QQcsZNf0eWs?t=2675) The closing shares contact details but points to no repository, checklist or sample configuration covering the talk's content.
