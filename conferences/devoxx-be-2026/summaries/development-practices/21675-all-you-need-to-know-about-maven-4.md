---
title: All you need to know about Maven 4!
talkId: "21675"
conference: devoxx-be-2026
speakers: [Matthias Bünger]
track: Development Practices
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=TgkY2UmWtBo
durationMin: 47
slides: https://speakerdeck.com/runningjava/all-you-need-to-know-about-maven-4
verdict: 5
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# All you need to know about Maven 4!

Matthias Bünger · Conference · Development Practices
Slides: https://speakerdeck.com/runningjava/all-you-need-to-know-about-maven-4

## TL;DR

Maven 4's headline change is the split between a build POM (new model 4.1.0, free to evolve) and a generated consumer POM (kept at 4.0.0 so IDEs and tools built on the old schema keep working). Around that split come reactor fixes, automatic versioning, lifecycle changes and smaller usability improvements, plus a migration path that mostly amounts to updating to the latest Maven 3, fixing warnings, and switching the runner.

## Key takeaways

- The consumer POM unlocks Maven 4: the repository POM can use model 4.1.0 features while consumers still receive a 4.0.0 POM, so the ecosystem of IDEs and build tools does not break.
- Java 17 is required only to run Maven 4 itself; projects can still target any JDK through the compiler plugin or toolchains.
- Prefer `mvn verify` over `mvn clean install` for regular builds, since installing unfinished artifacts into the local repository causes side effects that a new project-local repository now helps avoid.
- Prepare for migration on Maven 3.9 or later by fixing every build warning (use `-fos WARN` to surface them); duplicate declarations tolerated by Maven 3 fail under Maven 4's stricter validation.
- Stay on the latest 3.x plugins for now; the 4.x plugins use a new plugin API that is still experimental.

## Notes

### [02:40](https://youtu.be/TgkY2UmWtBo?t=160) Why a major version took 15 years

Maven 1.0 shipped in 2004 and Maven 3.0 in October 2010; the team maintains about 100 artifacts (core, components, plugins) alongside more than 6,000 community plugins. The POM schema has been compatible since Maven 2 (2005) and serves two purposes: building the project and describing it for consumers via Maven Central. Every proposal to change the POM or drop old plugin APIs threatened the ecosystem of IDEs (Eclipse, IntelliJ, VS Code) and tools (Gradle, Ivy) that read and write POMs. Bünger quoted PMC chair Hervé Boutemy: with the build schema preserved in amber, Maven was stuck on minor releases. Maven 4 clears that blockage, and at talk time it was at release candidate 7 with Maven 3.10.0 just released.

### [08:23](https://youtu.be/TgkY2UmWtBo?t=503) Java 17 and code cleanup

The one breaking change is that running Maven 4 requires Java 17 (a move to 21 was voted down during the RC phase). The speaker stressed this is the JDK that runs Maven, never the JDK the application targets. Core code is being modernized to Java 8+ idioms continuously rather than in one rewrite, old Maven 1/2 plugin APIs are deprecated with warnings in 3.9 that become failures in 4.0, and the default plugin versions in the super POM were updated.

### [12:00](https://youtu.be/TgkY2UmWtBo?t=720) Build POM versus consumer POM

The build POM in the repository moves to model version 4.1.0 and keeps everything needed to build: plugins, their configuration, full parent and subproject declarations. During the build Maven generates a reduced consumer POM at model 4.0.0 containing dependencies, properties and metadata, and deploys both (the build POM supports reproducible builds). All later feature changes in the talk require model 4.1.0.

### [16:39](https://youtu.be/TgkY2UmWtBo?t=999) Subprojects, bom packaging, alternate syntaxes

Modules are renamed to subprojects to align with the Maven project concept and to stop colliding with Java modules; the old `<modules>` tag still works but is deprecated. Bill-of-materials POMs get an explicit `bom` packaging type instead of overloading `pom`. A new model parser SPI lets anyone define a project in another syntax, with the Mason extension (by Maven PMC members Tamas Cservenak and Guillaume Nodet) already offering YAML, JSON5, TOML and HOCON; the Maven team itself stays on XML for its schema and tooling.

### [21:50](https://youtu.be/TgkY2UmWtBo?t=1310) Reactor and repository handling

A bug present since Maven 2 is fixed: resuming a failed multi-module build with the printed `--resume-from` command used to fail because it could no longer find the already-built modules. A project-local repository now holds only the artifacts produced by the current build, so unfinished work no longer pollutes the user repository. The advice follows directly: `mvn verify` suffices for regular builds including tests, `install` is reserved for cases like testing a library locally, and `clean` wipes caches so it should be a deliberate choice. For the internals, Bünger pointed to Cservenak's "Never say never" article.

### [27:01](https://youtu.be/TgkY2UmWtBo?t=1621) Project root, versioning and strictness

The project root is now declared explicitly via the `.mvn` folder or a `root` attribute on the parent POM, exposed through `project.rootDirectory`, `session.rootDirectory` and the always-available `session.topDirectory`; several oddly named internal properties are deprecated or removed. Multi-module builds gain consistent timestamps across subprojects, `installAtEnd`/`deployAtEnd` defaulting to true (all or none), and automatic versioning: parent versions and versions of project-owned dependencies no longer need declaring, as the before/after XML comparison showed. CI-friendly variables such as `${revision}` now resolve without the flatten plugin. The `-fos WARN` (fail on severity) flag turns warnings into failures, which makes a good migration rehearsal because Maven 4 rejects POM constructs that Maven 3 only warned about. Profiles can be made optional with `-P?profilename`, logging at info level when absent.

### [35:21](https://youtu.be/TgkY2UmWtBo?t=2121) Lifecycle becomes a tree

The build lifecycle changes technically from a fixed list of phases to a tree, while the default lifecycle stays unchanged. Custom lifecycles can skip phases (integration tests without unit tests was the example) subject to constraints such as compiling after sources exist. This lays the groundwork for Gradle-style scheduling where a dependent project starts once a specific phase of its dependency completes; an experimental concurrent lifecycle builder demonstrates it. Every phase now has `before:` and `after:` hooks, plus new `all` and `each` phases at project level, with names borrowed from testing frameworks.

### [40:04](https://youtu.be/TgkY2UmWtBo?t=2404) Migrating and a look at 4.1

Migration has three steps: build successfully on Maven 3.9+ (3.10 was current) with up-to-date 3.x plugins, prepare the environment for Java 17, then run Maven 4 and fix any errors. The team validates against many open-source projects plus crawler-built GitHub projects, but asked for feedback on unusual setups such as 5,000-module builds. A built-in upgrade tool (Maven Up) can rewrite a project to Maven 4-compatible or full 4.1-model form. Maven 4.1 will bring model 4.2.0 with mixins (combining plugin configurations like multiple parent POMs, aimed at clashes such as Spring versus company parents), continued plugin API work, better Java module system support, and a `-Tmax` flag using all cores minus one. The release answer was "when it's done", with RC7 hoped to be the last. In Q&A, the Maven Daemon was described as a separate project that will support Maven 4 once it goes final.

## Tools, libraries and specs

- Maven 4.0.0-rc-7, Maven 3.10.0, Maven 3.9.x; POM model versions 4.0.0, 4.1.0, upcoming 4.2.0
- Java 17 (minimum to run Maven 4)
- Mason extension (Maven project definitions in YAML, JSON5, TOML, HOCON)
- Maven Flatten Plugin (partly obsoleted by native CI-friendly variable resolution)
- Maven Daemon (separate project, Maven 4 support planned after final)
- Build flags and properties: `-fos WARN`, `-P?profile`, `-Tmax`, `project.rootDirectory`, `session.topDirectory`, `session.rootDirectory`, `installAtEnd`/`deployAtEnd`

## Who should watch

Maven users planning the move to Maven 4, and anyone curious why the major release took so long, get the full picture in one sitting. Plugin authors learn which APIs are going away and why 4.x plugins are not production-ready. Maven internals experts and teams already testing the release candidates can skip to the deck's link collection instead.

## Verdict

**5/10**: A beginner tour of Maven 4 from a PMC member, with the reasoning behind the consumer POM and the verify-over-install advice, but nothing is run on screen and the feature list is the speaker's own what's-new article.

**Novelty 1/2**

- **+** [08:23](https://youtu.be/TgkY2UmWtBo?t=503) The PMC explains why Maven 4 requires Java 17 and not 21: the move to 21 was proposed during the release-candidate phase and "we voted against this".
- **+** [41:35](https://youtu.be/TgkY2UmWtBo?t=2495) The team validates Maven 4 with a crawler that builds GitHub Maven projects and builds all Apache Maven plugins with it, and relies on user feedback for cases such as 5,000-subproject builds.
- **·** [39:30](https://youtu.be/TgkY2UmWtBo?t=2370) The feature tour follows the official what's-new article, which the speaker wrote and which the talk points to for "a bit more context and examples".

**Demonstrated 0/2**

- **−** [22:22](https://youtu.be/TgkY2UmWtBo?t=1342) The fixed resume-from failure is described from a slide with no build run on screen.
- **−** [32:11](https://youtu.be/TgkY2UmWtBo?t=1931) Automatic versioning is shown only as static before/after XML, never executed.

**Measured 1/2**

- **·** [03:12](https://youtu.be/TgkY2UmWtBo?t=192) The talk makes no performance or effect claims; figures such as 100 maintained artifacts and 6,000 community plugins set the scene rather than back an argument.

**Depth 2/2**

- **+** [04:14](https://youtu.be/TgkY2UmWtBo?t=254) "The POM fulfills two purposes. To build the project and to consume the project" gives beginners a mental model for why the consumer POM exists.
- **+** [24:56](https://youtu.be/TgkY2UmWtBo?t=1496) The verify-over-install advice is grounded in the reactor bug and in how installing project A publishes an unfinished project to the user repository.
- **−** [13:32](https://youtu.be/TgkY2UmWtBo?t=812) The consumer POM is presented as always generated reduced, and the talk never mentions the `maven.consumer.pom.flatten` switch that the official page documents as off by default.

**Reusable 1/2**

- **+** [40:04](https://youtu.be/TgkY2UmWtBo?t=2404) The three-step migration path (latest 3.x and plugins, Java 17 environment, run Maven 4 and fix errors) is a procedure viewers can follow.
- **+** [42:41](https://youtu.be/TgkY2UmWtBo?t=2561) The talk points to an official migration guide and the Maven Up tool, which rewrites a project to Maven 4 or full 4.1 model compatibility.
- **·** [32:11](https://youtu.be/TgkY2UmWtBo?t=1931) Beyond the migration segment, takeaways are fragments (XML snippets, flags, property names) left to reconstruct in the viewer's own build.
