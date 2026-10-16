---
title: Deterministic by Design - Achieving Reproducible Builds with Maven
talkId: "4096"
conference: devoxx-be-2026
speakers: [Maarten Mulders]
track: Development Practices
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=9vtYvAI2Dtk
durationMin: 48
slides: https://speakerdeck.com/mthmulders/deterministic-by-design-achieving-reproducible-builds-with-maven-devoxx-be-2026
verdict: 7
reach: segment
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-15

# Deterministic by Design - Achieving Reproducible Builds with Maven
Maarten Mulders · Conference · Development Practices
Slides: https://speakerdeck.com/mthmulders/deterministic-by-design-achieving-reproducible-builds-with-maven-devoxx-be-2026

## TL;DR
A build is reproducible when the same sources always produce bit-identical artifacts, and Mulders argues this is now a business requirement driven by supply-chain attacks and European regulation, not an engineering puzzle. He walks through diagnosing non-determinism with Maven's artifact plugin and diffoscope, fixing the five usual causes, and getting independent verification through Reproducible Central.

## Key takeaways
- Define `project.build.outputTimestamp` in the POM so archive entries carry a fixed timestamp; the Maven Release Plugin updates it automatically at release time.
- Never use dependency version ranges such as `[2.0.0,)`; pin exact versions and let Dependabot or Renovate propose upgrades under your control.
- Pin every Maven plugin version explicitly, since unpinned plugins resolve differently per Maven version (Maven 4 warns about this).
- Run `mvn artifact:check-buildplan` to list reproducibility blockers and `mvn artifact:compare` against a reference build, then inspect diffs with diffoscope.
- Publish a buildspec to Reproducible Central so a third party rebuilds your Maven Central artifacts and proves anyone can reproduce them.
- Reproducibility complements PGP signatures: a signature proves who uploaded the bits, while a reproducible build proves the bits match the sources.

## Notes

### [02:42](https://youtu.be/9vtYvAI2Dtk?t=162) What "reproducible" means
Reproducibility here means the same source code produces the same artifact bit by bit, which for software amounts to determinism. Mulders notes biologists distinguish repeatability (same samples) from reproducibility (different samples), but source code in version control makes that distinction moot. Common sources of non-determinism: file timestamps, file and directory ordering, floating dependencies, environment leakage, and stale files or directories, illustrated by his own story of once publishing a JAR to Maven Central with a stray empty directory inside.

### [05:49](https://youtu.be/9vtYvAI2Dtk?t=349) Demo: two builds, different bits
A live demo builds a near-empty POM twice, seconds apart, and the SHA-256 checksums differ. Nothing exotic is configured (just groupId, artifactId, version), which sets up the rest of the talk: if even this fails, ordinary projects certainly do.

### [08:29](https://youtu.be/9vtYvAI2Dtk?t=509) Why it matters: quality and compliance
Three quality arguments follow: reproducible builds let you verify third-party libraries against their published artifacts amid rising CI/CD attacks; artifact caching only pays off when builds are predictable; and hot-fixing an older release requires rebuilding exactly what runs in production plus one fix. On compliance, Mulders (with a non-lawyer disclaimer) paraphrases four EU acts as pointing at build traceability: the Cyber Resilience Act, DORA for financial institutions, NIS2, and the Medical Device Regulation. Audits already ask teams to prove control over what they ship, and bit-level proof beats assumptions.

### [16:25](https://youtu.be/9vtYvAI2Dtk?t=985) Diagnosing with artifact:compare and diffoscope
The first tooling demo runs `mvn artifact:compare` against a reference copy in the local repository. It fails: the POM matches but the JAR differs, and the buildcompare file points at diffoscope. The diffoscope output reveals environment leakage: `config.properties` inside the reference JAR contains an injected API key (`correct horse battery staple`) while the local build has it undefined. Mulders notes such a leak should mean immediate key revocation. A follow-up `mvn artifact:check-buildplan` reports no `project.build.outputTimestamp`, an outdated plugin, and dependency version ranges (SLF4J resolving to 2.0.20 locally versus 2.0.19 in the reference, then shaded in).

### [23:56](https://youtu.be/9vtYvAI2Dtk?t=1436) Fixes: pin versions, freeze timestamps
Three fixes map to the report. Pin dependency versions to one exact number and stay current with Dependabot or Renovate. Pin plugin versions too, because Maven picks defaults per Maven version; the slide quotes the Maven 4 warning naming resources, compiler, surefire, and jar plugins. Set `project.build.outputTimestamp` (shown as `2026-09-17T15:11:57Z`) so JAR, WAR, and EAR entries stop carrying the wall-clock time of each run. Finally, upgrade maven-jar-plugin to 3.2.0 or later, since older versions ordered archive entries unpredictably; check-buildplan names the minimum version per plugin.

```xml
<!-- from published slides p.31 -->
<properties>
  <project.build.outputTimestamp>2026-09-17T15:11:57Z</project.build.outputTimestamp>
</properties>
```

### [32:18](https://youtu.be/9vtYvAI2Dtk?t=1938) Verifying: local compare and Reproducible Central
After the fixes, check-buildplan reports no known issues in seven plugins and artifact:compare passes with both files OK. Mulders is candid that this demo misfired slightly: he had expected one remaining failure from the unaddressed environment leak, and an expected timestamp difference never appeared, so he narrates the intended teammate-debugging beat instead of showing it. The stronger proof is Reproducible Central (`jvm-repo-rebuild/reproducible-central` on GitHub), which rebuilds Maven Central artifacts from a buildspec file. He shows his own Clocky project's buildspec (Maven 3.9.15, JDK 11, exact command), runs its Docker-based isolated rebuild locally with all three files (POM, JAR, sources JAR) verified good, and explains that listing there triggers GitHub Action rebuilds on every future release, plus a badge for the README.

### [42:09](https://youtu.be/9vtYvAI2Dtk?t=2529) Recap, badges, and PGP signatures
The recap table pairs five causes with resolutions: floating dependencies, floating plugins, unset archive timestamps, environment leakage ("It Depends"), and stray files (build and publish from a clean checkout; `mvn release:prepare release:perform` already clones fresh). A closing extra covers the Verify PGP Signatures plugin, which pins the keys you expect dependencies like JUnit to be signed with, so a release signed by an unfamiliar key raises a flag. References: his blog series "The Road to Reproducible Builds on the JVM" at maarten.mulders.it and the demo projects at bit.ly/deterministic-by-design-demos.

## Tools, libraries and specs
- Apache Maven artifact plugin 3.7.0 (`check-buildplan`, `compare` goals)
- maven-jar-plugin 3.2.0 (minimum for ordered archive entries)
- Maven 4.x unpinned-plugin warning; Maven Release Plugin (auto-updates `project.build.outputTimestamp`)
- diffoscope (archive-aware diffing, originating from the Debian project)
- Reproducible Central (`jvm-repo-rebuild/reproducible-central`), Docker-based isolated rebuilds
- Verify PGP Signatures plugin (Maven plugin for dependency signature checks)
- Dependabot, Renovate (automated version upgrades)
- SLF4J 2.0.19 / 2.0.20 (version-range example); Clocky (speaker's demo project, Maven 3.9.15, JDK 11)

## Who should watch
Maven-based Java developers who own releases, pipelines, or audit evidence gain a practical end-to-end workflow. Teams under CRA, DORA, NIS2, or MDR scrutiny get arguments to take to management. Skip it if you already run reproducible Maven builds verified through Reproducible Central.

## Verdict
**7/10**: A Maven reproducibility workflow with the failure shown, the checks run and a published demo repository, limited by an official-guide core and a post-fix demo beat that did not behave as the speaker expected.

**Reach segment**: Java teams that build and release with Maven can apply the POM-level fixes and Reproducible Central listing directly, while Gradle-only teams cannot within a year.

**Novelty 1/2**

- **+** [13:15](https://youtu.be/9vtYvAI2Dtk?t=795) The compliance case paraphrases four EU acts (CRA, DORA, NIS2, MDR) into one traceability argument.
- **+** [39:03](https://youtu.be/9vtYvAI2Dtk?t=2343) The Reproducible Central walkthrough draws on the speaker's own listings, including a stray-directory failure that flipped to 3/3 good on the next release.
- **−** The Maven mechanics (outputTimestamp, version pinning, artifact:compare, check-buildplan, diffoscope) follow the official guide at https://maven.apache.org/guides/mini/guide-reproducible-builds.html rather than adding new techniques.

**Demonstrated 1/2**

- **+** [20:39](https://youtu.be/9vtYvAI2Dtk?t=1239) The diffoscope output on screen exposes the leaked API key inside config.properties.
- **+** [37:00](https://youtu.be/9vtYvAI2Dtk?t=2220) The Docker-based Reproducible Central rebuild of the speaker's Clocky project reports the POM, JAR and sources JAR all good.
- **−** [33:19](https://youtu.be/9vtYvAI2Dtk?t=1999) The post-fix compare passes where the speaker expected one remaining environment-leak failure, and the timestamp differences he expected at [21:41](https://youtu.be/9vtYvAI2Dtk?t=1301) never appear, so the intended fix-then-verify beat is narrated instead of shown.

**Measured 1/2**

- **·** The talk makes no quantitative claim its argument rests on: the show of hands at [01:08](https://youtu.be/9vtYvAI2Dtk?t=68) and the unquantified remark on growing attacks at [09:33](https://youtu.be/9vtYvAI2Dtk?t=573) are scene-setting, and the SHA-256 and artifact:compare outputs are pass/fail verification.

**Depth 2/2**

- **+** [29:05](https://youtu.be/9vtYvAI2Dtk?t=1745) The timestamp fix is explained at the mechanism level: ZIP entries carry modification and creation times, so every rebuild stamps the current time unless outputTimestamp freezes it.
- **+** [40:35](https://youtu.be/9vtYvAI2Dtk?t=2435) The independent rebuild is justified by what it rules out: malware injected at build time fails the comparison, and malware in the sources stays visible in the tagged code.
- **−** [42:41](https://youtu.be/9vtYvAI2Dtk?t=2561) Environment leakage, the one cause the talk shows leaking a secret, gets no general resolution beyond "it depends".

**Reusable 2/2**

- **+** [47:55](https://youtu.be/9vtYvAI2Dtk?t=2875) The demo projects covering the talk's main content are published on GitHub via bit.ly/deterministic-by-design-demos.
- **+** [47:24](https://youtu.be/9vtYvAI2Dtk?t=2844) The speaker's blog series "The Road to Reproducible Builds on the JVM" at maarten.mulders.it is pointed to for revisiting the material.
