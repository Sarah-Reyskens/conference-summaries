---
title: "Green Maven builds: sustainable CI in practice"
talkId: "24244"
conference: devoxx-be-2026
speakers: [Jan Boonen]
track: Development Practices
sessionType: Lunch Talk
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=Mdu5_gndYn0
durationMin: 40
slides: null
verdict: 6
reach: segment
frames: 9
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Green Maven builds: sustainable CI in practice

Jan Boonen · Lunch Talk · Development Practices

## TL;DR

Jan Boonen shows how to cut the energy use of Maven builds and their CI pipelines with a set of small, immediately applicable techniques: parallel JUnit tests, quiet Maven logging, artifact reuse across jobs, and pipelines that skip work they do not need. The talk closes with ways to measure CI energy use (EcoCI, Kepler) so optimizations can be verified instead of assumed.

## Key takeaways

- Enable JUnit 5 parallel test execution with five lines in `junit-platform.properties`; the live demo cut a 6-second suite to about 3 seconds.
- Set a staleness grace period (`lastModGranularityMs`) via `MAVEN_CLI_ARGS`/`MAVEN_OPTS` in CI so jobs that reuse compiled artifacts do not trigger a full Maven recompile and retest.
- Pass only the needed `target` output between GitLab jobs with `artifacts` plus `needs`, and keep unit-test and integration-test report paths separate so one does not overwrite the other.
- Run unit and integration tests as parallel jobs, run quality gates only on merge requests, and package only on release; use `rules`/`workflows` so feature-branch pushes do not trigger pipelines at all.
- Drop Maven log verbosity in CI (error level, no transfer progress); Boonen reports 10 to 20 seconds saved per build on large projects.
- Add EcoCI `before_script`/`after_script` hooks to jobs to get per-job energy and carbon estimates on a dashboard, and consider Project Kepler for Kubernetes-hosted runners.

## Notes

### [00:35](https://youtu.be/Mdu5_gndYn0?t=35) Why green software, and what this talk covers

Boonen opens with the personal motive (his daughters asking what he does about emissions at work, wildfire damage seen while hiking in Belgium) and scopes the talk: energy used while producing software (local builds, CI servers, data centers), not hardware manufacturing or hosting. Three segments follow: sustainable Maven, efficient CI/CD pipelines (GitLab examples, applicable to GitHub Actions), and measuring carbon emissions. One tip outside the scope: reuse decommissioned hardware for pipeline runners.

### [06:46](https://youtu.be/Mdu5_gndYn0?t=406) Parallel JUnit 5 tests

Create `junit-platform.properties` with parallel execution enabled, concurrent mode, and a fixed thread count. The live demo runs a Kotlin project with three 2-second tests serially (over 6 seconds), then switches branch to the parallel config and reruns in about 3 seconds. Caveat from Boonen's own Spring Boot project: parallel integration tests can mix application contexts, so some suites need annotations pinning methods to one thread, found by trial and error.

```properties
# reconstructed from speech
junit.jupiter.execution.parallel.enabled=true
junit.jupiter.execution.parallel.mode.default=concurrent
junit.jupiter.execution.parallel.mode.classes.default=concurrent
junit.jupiter.execution.parallel.config.strategy=fixed
junit.jupiter.execution.parallel.config.fixed.parallelism=4
```

### [11:34](https://youtu.be/Mdu5_gndYn0?t=694) Quieter Maven logging

Nobody reads green-pipeline logs, so a `.mvn/jvm.config` sets error-level logging, timestamps, and `--show-version` (to catch CI running a different Maven version than local). A GitLab job view shows the result: only test output, no Maven INFO lines. Claimed saving on large projects: 10 to 20 seconds per build.

### [14:45](https://youtu.be/Mdu5_gndYn0?t=885) Preventing recompilation across CI jobs

The core diagnosis: each CI job checks out sources fresh, so in a second job the sources are newer than any transferred binaries and Maven recompiles and retests everything. The fix is a last-modified grace period so Maven treats near-equal timestamps as unchanged, safe because all jobs run on the same commit. Combined with skipping unneeded plugins, never installing, and quiet mode, these flags go at the top of the pipeline definition via `MAVEN_CLI_ARGS` and `MAVEN_OPTS`.

### [18:23](https://youtu.be/Mdu5_gndYn0?t=1103) Pipeline design: fail fast, minimize work

Two principles: stop the pipeline at the first failure (but report all test failures at once), and run only necessary work. The recommended shape compiles once, runs unit and integration tests in parallel jobs (each on its own agent), checks quality (SonarQube) only on merge requests, and packages only on release. Artifacts carry compiled classes forward; each downstream job declares `needs` on the compile job.

### [23:32](https://youtu.be/Mdu5_gndYn0?t=1412) GitLab demo: YAML, cache, and job graph

On screen: pipeline variables with the granularity setting, build/test/package/deploy stages, Maven repository caching keyed on `pom.xml`, a compile job exporting `target`, test jobs exporting Surefire/Failsafe plus JaCoCo reports, and a reporting job that only computes coverage while skipping test and compile. The GitLab job-dependency graph shows compile feeding two parallel test jobs feeding coverage and package.

### [26:14](https://youtu.be/Mdu5_gndYn0?t=1574) Rules and workflows: skipping jobs

`rules` select when a job runs (example: never run QA on merge-request events when QA happens on main); `workflows` apply to the whole pipeline (example: run on merge requests, pushes to main, and tags, so plain feature-branch pushes run nothing). Boonen admits GitLab's rule logic is confusing enough that he leaned on AI assistance to write it. An unsolved exercise for the audience: reuse compile artifacts across pipelines by commit ID (a lookup job that downloads artifacts from the main-branch build for the same commit when tagging a release).

### [31:30](https://youtu.be/Mdu5_gndYn0?t=1890) Measuring the footprint

Carbon intensity (grams of CO2 per kWh) converts energy into emissions; maps shown are the 2024 world picture and the last-24-hours European picture, with France notably green through nuclear power. EcoCI integrates into pipelines with a hidden base job (`before_script`/`after_script`, optional JSON output, optional public dashboard): the demo dashboard lists per-job energy, time, CPU utilization, and grid intensity. Boonen notes these are estimates without an Electricity Maps API key and an assumed runner type. For self-hosted Kubernetes runners, Project Kepler measures node energy from CPU telemetry and suits production workloads too.

### [38:20](https://youtu.be/Mdu5_gndYn0?t=2300) Conclusions

Recap of the six practices (artifacts with `needs`, no recompilation, less logging, parallel tests, workflow rules) plus pruning unneeded Maven plugins. Greener pipelines are faster pipelines, which keeps developers happy.

## Tools, libraries and specs

- JUnit 5 (parallel execution via `junit-platform.properties`)
- Maven (`.mvn/jvm.config` logging, `MAVEN_CLI_ARGS`/`MAVEN_OPTS`, compiler `lastModGranularityMs` staleness grace)
- GitLab CI (`needs`, `artifacts`, `cache`, `rules`, `workflows`)
- GitHub Actions (techniques stated to transfer, different syntax)
- SonarQube (merge-request quality gate example)
- JaCoCo (coverage reports)
- EcoCI (per-job energy/carbon pipeline plugin with dashboard)
- Project Kepler (Kubernetes energy monitoring from CPU telemetry)
- Electricity Maps (carbon-intensity data behind EcoCI estimates)

## Who should watch

Teams running Maven builds on GitLab CI or GitHub Actions who want faster, cheaper pipelines this week, and anyone curious how to measure CI energy use. Gradle-only shops get partial value since the Maven specifics do not transfer, and viewers wanting rigorous carbon accounting or production/hosting optimization should look elsewhere: both are explicitly out of scope.

## Verdict

**6/10**: Maven and CI energy-saving practices a team can apply directly, with a live parallel-test before/after and an explained recompilation mechanism, but the main fix is never shown working and no energy saving is measured.

**Reach segment**: Maven teams building on GitLab CI or GitHub Actions, a sizable minority of the JVM audience, can apply the pipeline and Maven practices; Gradle or other-CI shops get the JUnit parallelism and the pipeline-shape ideas only.

**Novelty 1/2**

- **+** [14:45](https://youtu.be/Mdu5_gndYn0?t=885) The speaker reports seeing the verify-then-Sonar double build "a lot" in projects, an observation from his own work rather than from documentation.
- **·** [06:46](https://youtu.be/Mdu5_gndYn0?t=406) The individual techniques live in the JUnit 5, GitLab CI and EcoCI documentation, and the speaker says some of it you might already know; the value is the assembly around his own examples.

**Demonstrated 1/2**

- **+** [13:43](https://youtu.be/Mdu5_gndYn0?t=823) A real GitLab job view shows the quiet-logging result: only test output, no Maven INFO lines.
- **−** [17:53](https://youtu.be/Mdu5_gndYn0?t=1073) The recompilation fix is configured on screen but never shown skipping a rebuild, since it only works inside a pipeline.

**Measured 1/2**

- **+** [09:59](https://youtu.be/Mdu5_gndYn0?t=599) The same three-sleep suite runs live serially and then concurrently after a branch switch, with the IDE timer dropping from over 6 seconds to about 3.
- **−** [14:15](https://youtu.be/Mdu5_gndYn0?t=855) The 10-to-20-second saving from quiet logging is reported from practice with no baseline, project size or measurement shown.
- **−** [36:46](https://youtu.be/Mdu5_gndYn0?t=2206) No optimization gets a before/after energy figure; the EcoCI dashboard values are estimates for an assumed runner type, as the speaker notes.

**Depth 2/2**

- **+** [15:16](https://youtu.be/Mdu5_gndYn0?t=916) The recompilation segment explains the mechanism (each job's fresh checkout is newer than the transferred binaries, so Maven reruns the full lifecycle) and why the grace period is safe when all jobs run on one commit.
- **+** [10:30](https://youtu.be/Mdu5_gndYn0?t=630) The parallel-testing advice names the Spring Boot dirty-context failure mode and the thread-pinning remedy, found by trial and error in the speaker's own project.
- **−** [26:14](https://youtu.be/Mdu5_gndYn0?t=1574) The rules and workflows logic is shown by example but not explained; the speaker calls it not very clear and says he leaned on AI to write it.

**Reusable 1/2**

- **+** [07:52](https://youtu.be/Mdu5_gndYn0?t=472) The five-line parallel-test configuration is stated in full, and the logging and pipeline snippets are shown complete enough to copy.
- **−** [08:24](https://youtu.be/Mdu5_gndYn0?t=504) The demo project is described as built for the conference, but the talk points to no repository for it, so every fragment has to be reconstructed by hand.
