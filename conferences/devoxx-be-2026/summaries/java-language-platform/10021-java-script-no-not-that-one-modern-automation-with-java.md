---
title: "Java Script (No, Not That One): Modern Automation with Java"
talkId: "10021"
conference: devoxx-be-2026
speakers: [Loïc Magnette]
track: Java Language & Platform
sessionType: Tools-in-Action
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=pgVJWp-SjxI
durationMin: 30
slides: null
verdict: 7
reach: broad
frames: 9
reviewedAt: 2026-10-16
---

# Java Script (No, Not That One): Modern Automation with Java
Loïc Magnette · Tools-in-Action · Java Language & Platform

## TL;DR
Modern Java works as a scripting language: single-file execution, compact mains, shebang support, and JBang for dependencies remove the old compile-and-package friction. Through live demos of a `cat` clone called `dog`, the speaker shows each feature running on screen and points to a step-by-step repo so viewers can replay every demo.

## Key takeaways
- Run scripts directly with `java Dog.java`: no `javac` step since Java 11 (JEP 330), and multi-file programs since Java 22 (JEP 458) with dependencies resolved from subdirectories.
- Java 25 drops the ceremony: an instance `void main()` with no class declaration plus the `java.lang.IO` class replaces `public static void main` and `BufferedReader` boilerplate.
- A `#!/usr/bin/java --source 25` shebang plus `chmod +x` turns a Java file into an executable script droppable into `~/bin`.
- JBang adds Gradle-style `//DEPS` dependencies, scaffolding templates (`jbang init`), toolchain provisioning, and `jbang export native` for GraalVM native images.
- GraalVM native images need reflection configuration for libraries like LangChain4j; JBang accepts `//NATIVE_OPTIONS` and a `reflect-config.json` for that.
- PicoCLI's `@Command(mixinStandardHelpOptions = true)` generates `--help`/`--version` output for free, and TamboUI brings full terminal UIs to script-sized Java programs.

## Notes
### [00:34](https://youtu.be/pgVJWp-SjxI?t=34) The scripting problem
Relearning bash twice a year is painful and JavaScript surprises with coercion quirks, so the speaker scripts in the language he uses daily: Java. Every demo reimplements `cat` as `dog`, because no Unix tool is named after a dog.

### [03:12](https://youtu.be/pgVJWp-SjxI?t=192) Running Java without compiling
`java Dog.java` runs a single-file program with no `javac` step (JEP 330, JDK 11). A second demo builds `DogAdvanced.java`, which imports helper classes from a `files/` subpackage in a plain directory with no Maven or Gradle layout; the launcher finds and compiles them in memory (JEP 458, JDK 22). A live typo (`services` vs `files` package) is fixed on stage and the script prints a file with line numbers plus "woof!".

### [08:33](https://youtu.be/pgVJWp-SjxI?t=513) Less boilerplate in Java 25
The class declaration and `public static void main(String[] args)` shrink to a bare `void main()`, still runnable. Reading keyboard input shrinks from a `BufferedReader`/`InputStreamReader` try-catch block to `IO.readln(prompt)` via the new `java.lang.IO` class, which needs no import.

### [11:42](https://youtu.be/pgVJWp-SjxI?t=702) Shebang support
Removing the `.java` extension requirement and adding `#!/usr/bin/java --source 25` plus the execute bit makes the file run as `./dog`. The `--source` flag pins the language level so older runtimes refuse it cleanly.

### [13:46](https://youtu.be/pgVJWp-SjxI?t=826) JBang and native images
JBang runs scripts, resolves `//DEPS` dependencies in Gradle coordinates, runs remote jars, and downloads a JDK when none is installed. The live demo builds `hello.java`, a script calling a local Ollama model through LangChain4j 1.19.0. `jbang export native` then builds a GraalVM binary; the first attempt fails on Jackson reflection until `//NATIVE_OPTIONS` and a reflection config file are added, after which the binary runs.

### [20:35](https://youtu.be/pgVJWp-SjxI?t=1235) Real CLIs with PicoCLI
`jbang init` scaffolds `DogCli.java` with the PicoCLI dependency, annotated parameters (`-n`/`--numbers`, file list with splitting and defaults), and auto-generated `--help` output shown live in the terminal.

### [24:13](https://youtu.be/pgVJWp-SjxI?t=1453) Terminal UIs and Duke Runner
TamboUI (named as a French nod to Rust's Ratatouille) enables full terminal applications. As a fun example, the speaker runs Duke Runner, a game played in the terminal while waiting on an AI coding agent, and notes its separate repo on his GitHub.

### [26:19](https://youtu.be/pgVJWp-SjxI?t=1579) Startup speed and resources
The same script runs in about 0.3 s under plain `java`, then "way way faster" under an unreleased GraalVM fast-startup feature, with timing shown live. The closing slide links slides and code through a QR code to lomagnette.github.io, plus the Duke Runner repo.

## Tools, libraries and specs
- JEP 330 (single-file execution, shebang), JEP 458 (multi-file launch), JEP 512 (compact source files, instance main, `IO` class)
- JBang (script runner, `//DEPS`, `jbang init`, `jbang export native`)
- GraalVM native image (plus unreleased fast-startup work)
- PicoCLI (CLI parsing), TamboUI + jline3 (terminal UI)
- LangChain4j 1.19.0 + Ollama (`llama3.2:latest`, local `localhost:11434`)

## Who should watch
Java developers who reach for bash or Python for small automation and suspect Java could do it with less context switching. Skip it if you already script with JBang daily; the JEP mechanics will be familiar, though the PicoCLI and TamboUI pointers may still be new.

## Verdict
**7/10**: Single-file launch, compact mains and JBang scripts run live end to end with a replayable demo repository; the timing evidence has no method and the explanations stay at usage level.

**Reach broad**: Most Java developers in the audience can use single-file launch, compact mains and JBang for everyday automation in their own work.

**Novelty 1/2**

- **+** [02:39](https://youtu.be/pgVJWp-SjxI?t=159) The speaker's own `dog` example ties source-file launch, compact mains, dependencies and CLI tooling into one progression across several sources.

**Demonstrated 2/2**

- **+** [07:32](https://youtu.be/pgVJWp-SjxI?t=452) After correcting the import, the multi-file script prints file contents with line numbers and a bark.
- **+** [23:41](https://youtu.be/pgVJWp-SjxI?t=1421) The generated PicoCLI help and numbered file output show the script becoming a usable command-line tool.
- **+** [20:35](https://youtu.be/pgVJWp-SjxI?t=1235) The native binary runs after the reflection options are added, completing the recovered native-image demo.

**Measured 1/2**

- **+** [27:15](https://youtu.be/pgVJWp-SjxI?t=1635) The terminal shows the Crema launcher taking 0.359 s then 0.085 s, following the plain-Java baseline for the same directory-listing script.
- **−** [26:50](https://youtu.be/pgVJWp-SjxI?t=1610) The roughly 0.3-second Java baseline and subsequent launcher timings are an informal demonstration without a stated timing protocol or explanation of the repeated-run conditions.

**Depth 1/2**

- **+** [08:03](https://youtu.be/pgVJWp-SjxI?t=483) The launcher is explained as finding helper classes in subdirectories and compiling them in memory, giving beginners a model of why no separate build is needed.
- **+** [19:03](https://youtu.be/pgVJWp-SjxI?t=1143) Jackson's reflection use is identified as the cause of the native-image failure.
- **−** [19:35](https://youtu.be/pgVJWp-SjxI?t=1175) The reflection configuration is supplied with “don't think too much about it,” leaving the main dependency-to-native extension at recipe level.

**Reusable 2/2**

- **+** [27:52](https://youtu.be/pgVJWp-SjxI?t=1672) The closing resources link points to the speaker's demo code, and [LoMagnette/java-script-no-not-that-one](https://github.com/LoMagnette/java-script-no-not-that-one) provides scripts, reflection configuration and a README mapping the progression to `[STEP-N]` commits.


