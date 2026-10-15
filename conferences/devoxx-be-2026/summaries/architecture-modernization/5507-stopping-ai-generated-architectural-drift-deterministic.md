---
title: "Stopping AI-Generated Architectural Drift: Deterministic Guardrails for Agentic Coding"
talkId: "5507"
conference: devoxx-be-2026
speakers: [Sasha Podlesniuk]
track: Architecture & Modernization
sessionType: Tools-in-Action
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=K3kD89Y1YCk
durationMin: 24
slides: null
verdict: 7
frames: 7
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Stopping AI-Generated Architectural Drift: Deterministic Guardrails for Agentic Coding

Sasha Podlesniuk · Tools-in-Action · Architecture & Modernization

## TL;DR

Natural-language rules in AGENTS.md-style files do not reliably stop coding agents from violating architecture, so Podlesniuk's team converts repeat violations into deterministic build checks the agent cannot ignore. The talk demonstrates the full loop live: ArchUnit, Error Prone and Checkstyle rules that fail the build with fixable messages, agents that self-correct against them, and mutation testing that probes the rules for loopholes.

## Key takeaways

- Put the rule in the build: the same task given to the same agent three times produced an `Instant.now()` call once despite a written rule requiring an injected clock.
- A guardrail earns a place in the agent loop only if it is executable code, deterministic across runs, adds seconds at most to the build, and reports the exact class, line and fix.
- Match the tool to what it can see: Checkstyle sees source text, ArchUnit sees compiled classes and relationships, Error Prone sees types and method bodies inside the compiler.
- ArchUnit tests double as exit criteria for fix-at-scale agent loops: tell the agent to iterate until the suite is green.
- Stress-test the rules with architectural mutation testing: have an agent propose rule-violating architectures and check the suite catches them.

## Notes

### [00:32](https://youtu.be/K3kD89Y1YCk?t=32) Written rules fail; checks hold

Three PRs with the same agent, task and rules: two used the injected clock, one called `Instant.now()`. After merging hundreds of AI-assisted PRs per week, the team converts recurring violations into build checks. Each check must be executable code, deterministic (a merge gate cannot rely on model judgment), cheap (seconds at most, since agents re-run the build constantly) and debuggable (class, line, action item). Rules are tested against throwaway fixture snippets.

### [04:41](https://youtu.be/K3kD89Y1YCk?t=281) ArchUnit demo: drift caught and self-corrected

A sample insurance service mixes the old service layer with the new mediator pattern. Two rules go live in a few lines of fluent API each: no classes in `service` packages, and every `@RestController` must inject a `Mediator`, with `because` reasons that become the agent's hints. Asked to add a cancel-policy endpoint, the agent first writes service-based code, hits the JUnit failures, reads the violation output and converts the feature to mediators until green. For drift already merged (unit tests where integration tests were required), three rules define the fixed state and the agent loops until the suite passes.

### [12:04](https://youtu.be/K3kD89Y1YCk?t=724) Mutation-testing the rules

A custom agent command inverts project rules and proposes plausible violating architectures (operators on screen: relabel, retarget, indirection, inversion, cross-talk). A mutant the suite misses, such as a repository injected directly into a controller, is either accepted or closed with a new rule. Results shown come from a previous run; the loop is too slow for the slot.

### [14:45](https://youtu.be/K3kD89Y1YCk?t=885) Error Prone and Checkstyle examples

A custom `BugChecker` flags private handler methods that read an aggregate root's fields with no external dependencies, suggesting the logic move onto the aggregate; severity ranges from suggestion to blocking failure. A Checkstyle `TodoComment` rule forbids comments unless tagged `WHY HERE:`, after AI assistance inflated comment volume beyond what prose rules could control.

### [18:29](https://youtu.be/K3kD89Y1YCk?t=1109) Costs and Q&A

Rules can be too strict, build time grows per rule and per extra agent iteration, some rules belong in prose, adoption starts with warnings or frozen rules, and a stuck agent signals an unclear rule. Q&A: agents write most rules (hooks block edits to rule files); checks ship as a versioned library across services; over-strict rules surface through team feedback.

## Tools, libraries and specs

- ArchUnit (rules run as JUnit tests, including frozen rules)
- Error Prone (custom BugChecker checkers)
- Checkstyle (TodoComment module)
- Spring Boot (`@SpringBootTest`, `@RestController`)

## Who should watch

Teams merging AI-generated code into a Java codebase who want architecture enforced by the build. Viewers outside the JVM stack can keep the four properties and the mutation-testing idea while skipping the tool specifics; anyone wanting measured drift-reduction data will not find it here.

## Verdict

**7/10**: Live demos of agents self-correcting against ArchUnit build checks, explained with a clear model of what each tool sees and what the checks cost; most of the material is in the ArchUnit docs, the numbers stay anecdotal and no repository is published.

**Novelty 1/2**

- **+** [12:04](https://youtu.be/K3kD89Y1YCk?t=724) Architectural mutation testing of the rule set, with named operators such as relabel, retarget and inversion, is presented as the team's own practice.
- **+** [01:34](https://youtu.be/K3kD89Y1YCk?t=94) The four guardrail properties (executable, deterministic, quick and cheap, debuggable) come from the team's experience merging AI-assisted pull requests.
- **−** The ArchUnit User Guide (https://www.archunit.org/userguide/html/000_Index.html) already covers the fluent rule API, JUnit integration and "Freezing Arch Rules", which are the core of the demos and the rollout advice.

**Demonstrated 2/2**

- **+** [05:44](https://youtu.be/K3kD89Y1YCk?t=344) The ArchUnit rule runs live as a JUnit test and the failing output shows the reason and violation locations the agent reads.
- **+** [08:56](https://youtu.be/K3kD89Y1YCk?t=536) Asked to add a cancel-policy endpoint, the agent converts the service-based feature to the mediator pattern until the tests are green.
- **−** [13:40](https://youtu.be/K3kD89Y1YCk?t=820) The mutation-testing run is not shown; only artifacts from a previous run appear, including a surviving mutant that injects a repository directly into a controller.

**Measured 1/2**

- **+** [00:32](https://youtu.be/K3kD89Y1YCk?t=32) The three-PR clock example reports one `Instant.now()` violation in three runs with the same task, rules and agent.
- **−** [01:04](https://youtu.be/K3kD89Y1YCk?t=64) "Hundreds of AI-assisted pull requests every week" is a self-reported total with no baseline.
- **−** [02:04](https://youtu.be/K3kD89Y1YCk?t=124) The "few seconds at most" build budget is stated as a requirement and never measured against a baseline.

**Depth 2/2**

- **+** [03:39](https://youtu.be/K3kD89Y1YCk?t=219) Tools are chosen by what each can see: Checkstyle the source text, ArchUnit compiled classes and their relationships, Error Prone types and method bodies inside the compiler.
- **+** [13:07](https://youtu.be/K3kD89Y1YCk?t=787) Relabel and retarget are explained by the blind spots they probe: over-reliance on names and sneaky alternative dependency paths.
- **+** [19:01](https://youtu.be/K3kD89Y1YCk?t=1141) The close weighs the costs: rules that are too strict, longer builds and more agent iterations, and rules better left as prose.

**Reusable 1/2**

- **+** [17:40](https://youtu.be/K3kD89Y1YCk?t=1060) The `checkstyle.xml` with the `TodoComment` rule is shown in full on screen, next to the short ArchUnit rules at [05:13](https://youtu.be/K3kD89Y1YCk?t=313).
- **−** [20:03](https://youtu.be/K3kD89Y1YCk?t=1203) No repository, sample project or checklist is pointed to.
