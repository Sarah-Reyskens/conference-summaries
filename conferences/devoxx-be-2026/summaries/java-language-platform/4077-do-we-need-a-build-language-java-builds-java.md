---
title: Do We Need a Build Language? Java Builds Java
talkId: "4077"
conference: devoxx-be-2026
speakers: [Rafael Winterhalter]
track: Java Language & Platform
sessionType: Tools-in-Action
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=y9JjxyKc6gU
durationMin: 31
slides: null
verdict: 8
reach: niche
frames: 8
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Do We Need a Build Language? Java Builds Java
Rafael Winterhalter · Tools-in-Action · Java Language & Platform

## TL;DR
Rafael Winterhalter presents Jenesis, his own build tool that uses `module-info.java` as the build descriptor instead of a separate build language, distributed as dependency-free Java source you run with the `java` launcher. Live demos build single- and multi-module projects, run tests, fail a build on a tampered dependency hash, and walk through building plain Maven projects from their poms. The thesis: the module system already describes everything a build needs, and builds should be verifiable artifacts rather than binary downloads.
## Key takeaways
- `module-info.java` already carries the module name, its dependencies (`requires`) and its API surface (`exports`), which covers most of what a pom declares, so a build tool can treat it as the descriptor.
- Distributing the build tool as small, dependency-free Java source removes the wrapper-download attack surface: there is no properties file pointing at a server to spoof.
- Recording a hash pin per dependency artifact and validating OpenPGP signatures at resolve time would have prevented whole classes of supply-chain attacks; both belong in the build by default.
- Test code belongs in its own module with qualified `exports ... to` the test module, which resolves the split-package conflict between Maven-style test sources and encapsulation.
- A module-name-to-Maven-coordinate index (Jenesis scans Central regularly) is sufficient to resolve modular builds against the existing pom-based ecosystem without duplicating declarations.
## Notes

### [01:37](https://youtu.be/y9JjxyKc6gU?t=97) Maven is stagnant; module-info is the better descriptor
Winterhalter argues Maven has barely changed in almost 20 years while platforms are judged harder in the age of agents writing software, and that every Java build tool invents its own descriptor that users must learn and duplicate. `module-info.java` already provides a module name (one coordinate instead of group plus artifact id), `requires` for dependencies, and `exports`, which neither Maven nor Gradle models. Using it as the entry point also removes a learning step: newcomers describe dependencies in a Java-native concept instead of a second language.

### [05:16](https://youtu.be/y9JjxyKc6gU?t=316) Threat model: pins, signatures, source distribution
Running Byte Buddy taught the speaker that publishing keys attract attackers: people sent reproducers with tinkered Maven builds to steer him at malicious locations. Jenesis therefore pins every dependency with a recorded hash and validates OpenPGP signatures of artifacts at resolution, so an update to a new version still verifies against the publisher key. The tool itself ships as a small multi-source Java program (about 24 KB) with zero dependencies that bootstraps from source, avoiding the Maven wrapper's roughly 30 MB and the Gradle wrapper's roughly 158 MB of downloads on every fresh CI machine.

### [10:26](https://youtu.be/y9JjxyKc6gU?t=626) Demo: one module built with the java launcher
In `demo/demo-02-java-modular`, a module requiring the SLF4J API and exporting a sample package builds with `java build/jenesis/Make.java`, producing and validating the jar. Module names resolve to Maven coordinates through the Jenesis modules index on GitHub, which scans Maven Central every 6 hours and can be self-hosted as a proxy. The speaker notes every demo is part of the Jenesis repository and runnable by the audience.

### [14:33](https://youtu.be/y9JjxyKc6gU?t=873) Demo: multi-module build and test modules
In `demo/demo-04-java-modular-multi`, `app` requires `demo.greeter`; Jenesis orders the two modules, parallelizes the rest, and finishes the full pipeline in about 5 seconds, with an incremental rebuild taking 0.56 seconds including skipped tests. Test sources live in a separate test module that the main module opens with qualified exports, sidestepping the split-package problem; he says JUnit runs from there but asks the audience to take the test execution on trust rather than showing it.

### [20:14](https://youtu.be/y9JjxyKc6gU?t=1214) Demo: a tampered dependency fails the build
In `demo/demo-28-pinning`, one module carries a deliberately wrong hash. The build resolves the pinned and unpinned modules, then fails before the jar loads with `Mismatched digest for org.apache.commons/commons-lang3/3.14.0`, shown on screen as a stack trace ending in `build.jenesis.Resolver.validate`. He pairs this with signature validation: the hash proves the bytes never changed, the OpenPGP signature proves an updated artifact still comes from the same publisher, though his claim that no Java tooling validates signatures overlooks Gradle's dependency verification.

### [24:27](https://youtu.be/y9JjxyKc6gU?t=1467) Maven compatibility without adopting modules
Because every transitive dependency on Central is described by a pom, Jenesis parses `pom.xml` directly and builds plain Maven projects (`demo-01`), and it can generate poms for modular projects, so adoption needs no flag day. Maven-style builds stay on the classpath: split-package test layouts cannot go on the module path, and he predicts nobody will use Maven 4's `module-info` patch descriptor language since it repeats the declaration-duplication the module system was rejected for.

### [27:02](https://youtu.be/y9JjxyKc6gU?t=1622) Executables, packaging, Kotlin, close
An `@jenesis.main`-style Javadoc tag on `module-info.java` marks the entry point, so after `java build/jenesis/Make.java` builds the project the tool can run the single executable module with the module path assembled. From the same descriptor Jenesis can drive `jpackage` for a self-contained runtime, emit a zip assembly, or generate a Dockerfile. Kotlin sources are detected and compiled with an auto-downloaded compiler unless pinned, and a compiler plugin is one tag:

```java
// from slide at 29:55
/**
 * @jenesis.plugin kotlinc maven/org.jetbrains.kotlin/kotlin-serialization-compiler-plugin
 * @jenesis.pin kotlinc/maven/org.jetbrains.kotlin/kotlin-serialization-compiler-plugin 2.4.0-RC2 SHA-256/...
 */
module sample.kotlin.serialization {
  requires kotlin.stdlib; requires kotlinx.serialization.core; exports sample;
}
```

He closes by pointing at jenesis.build, noting Claude validated Jenesis against thousands of real projects, and that the tool covers nearly everything his survey of build needs turned up.

## Tools, libraries and specs
- Jenesis (jenesis.build): module-system Java build tool, installable via SDKMAN or curl, runnable from source
- Byte Buddy: the speaker's bytecode library, cited for supply-chain attack experience
- Mockito: cited for the internal-package encapsulation problem modules solve
- Maven / Gradle / Bazel: compared on engine quality, wrapper size, and descriptor design
- Maven Central, pom.xml, JPMS (`module-info.java`, qualified exports), JUnit, `jpackage`, Kotlin compiler plugins (kotlinx.serialization)

## Who should watch
Java developers curious about build tooling, the module system, or supply-chain security gain the most, especially anyone teaching Java or maintaining published libraries. Developers wanting a stable, documented Maven or Gradle replacement should skip it: Jenesis is explicitly a proof of concept.

## Verdict
**8/10**: Live builds and a rejected dependency make the module-first design checkable, with explained trade-offs and runnable examples; the performance and download-size claims lack a controlled comparison.

**Reach niche**: The main content serves developers evaluating Jenesis or specialised module-first build tooling, especially library maintainers and Java teachers.

**Novelty 1/2**

- **+** [05:16](https://youtu.be/y9JjxyKc6gU?t=316) The Byte Buddy maintainer describes people sending bug reproducers with altered Maven builds, firsthand context for the risk of running an unfamiliar project's build.
- **−** The Jenesis README and jenesis.build already cover the feature tour that fills most of the talk, which is the search baseline for a project's own author.

**Demonstrated 2/2**

- **+** [25:30](https://youtu.be/y9JjxyKc6gU?t=1530) A pom-based project builds live with the Java launcher, and the frame at 25:45 shows the completed build.
- **+** [20:46](https://youtu.be/y9JjxyKc6gU?t=1246) The deliberately incorrect dependency pin produces a live mismatched-digest failure naming commons-lang3, visible in the frame at 21:05.
- **+** [27:32](https://youtu.be/y9JjxyKc6gU?t=1652) Jenesis builds and launches an executable module with its dependency path assembled, and the frame at 27:50 shows the program's greeting.

**Measured 1/2**

- **+** [07:49](https://youtu.be/y9JjxyKc6gU?t=469) The speaker reports a 24 KB source bootstrap against the preceding Maven and Gradle download-size estimates, but gives no measurement procedure.
- **−** [16:08](https://youtu.be/y9JjxyKc6gU?t=968) The reported 0.56-second incremental rebuild has no same-project Maven or Gradle baseline.
- **−** [03:44](https://youtu.be/y9JjxyKc6gU?t=224) Building thousands of projects is a self-reported compatibility total without a disclosed corpus or success criteria.

**Depth 2/2**

- **+** [12:29](https://youtu.be/y9JjxyKc6gU?t=749) The module-name-to-Maven-coordinate index explains how a descriptor containing only module names can resolve dependencies in the existing ecosystem.
- **+** [18:40](https://youtu.be/y9JjxyKc6gU?t=1120) Qualified exports to a separate test module connect encapsulation to test access, answering the split-package problem described with Mockito.
- **+** [22:21](https://youtu.be/y9JjxyKc6gU?t=1341) Hashes and publisher signatures address different checks: fixed bytes for a pinned artifact versus a recognised signing key after a version update.

**Reusable 2/2**

- **+** [10:26](https://youtu.be/y9JjxyKc6gU?t=626) The speaker identifies the demonstrated builds as runnable examples in the Jenesis repository, beyond the tool's distribution itself.
- **+** [10:56](https://youtu.be/y9JjxyKc6gU?t=656) The example's tree includes a README and module sources, giving viewers the project structure needed to repeat the build.
