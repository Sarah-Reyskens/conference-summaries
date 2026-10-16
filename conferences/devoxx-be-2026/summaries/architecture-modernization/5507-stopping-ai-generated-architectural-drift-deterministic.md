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
reach: broad
frames: 7
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16

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

**7/10**: The agent-to-build feedback loop is shown working and the choice of tool and the trade-offs are explained for the short slot; outcome numbers are anecdotal and no sample project or rule set is published.

**Reach broad**: Build-enforced architecture rules and feedback for AI-assisted coding are practices most of the conference's JVM developers and architects can apply.

**Novelty 1/2**

- **+** [18:29](https://youtu.be/K3kD89Y1YCk?t=1109) The team's rule backlog grows from recurring pull-request review comments, giving viewers an experience-based way to choose which agent failures deserve enforcement.
- **+** [16:54](https://youtu.be/K3kD89Y1YCk?t=1014) The team's unsuccessful attempts to control growing comment volume through prose rules and agent memory add a specific adoption experience to the established tools.

**Demonstrated 2/2**

- **+** [08:40](https://youtu.be/K3kD89Y1YCk?t=520) The agent's terminal output identifies architectural test failures and starts converting service-based code to mediator handlers.
- **+** [09:05](https://youtu.be/K3kD89Y1YCk?t=545) The completed run reports passing architecture tests and lists the service deletion and mediator conversion that resolved the violations.
- **−** [13:40](https://youtu.be/K3kD89Y1YCk?t=820) Architectural mutation testing is represented by artifacts from an earlier run rather than the running loop.

**Measured 1/2**

- **+** [00:32](https://youtu.be/K3kD89Y1YCk?t=32) The opening reports one clock-rule violation across three pull requests made with the same agent, task and rules.
- **−** [01:04](https://youtu.be/K3kD89Y1YCk?t=64) The team's hundreds of AI-assisted pull requests per week provide scale context but no measured before-and-after drift reduction.

**Depth 2/2**

- **+** [03:07](https://youtu.be/K3kD89Y1YCk?t=187) The choice among Checkstyle, ArchUnit and Error Prone follows what each can inspect: source text, compiled relationships, or resolved types and method bodies.
- **+** [13:07](https://youtu.be/K3kD89Y1YCk?t=787) Mutation operators target specific blind spots, including name-based enforcement and alternative dependency paths.
- **+** [19:01](https://youtu.be/K3kD89Y1YCk?t=1141) The closing model weighs false positives, build time, extra agent iterations and rules that should remain prose, explaining when to soften enforcement.

**Reusable 1/2**

- **+** [17:40](https://youtu.be/K3kD89Y1YCk?t=1060) The screen exposes the short Checkstyle configuration, providing a fragment viewers can reconstruct.
- **−** [01:34](https://youtu.be/K3kD89Y1YCk?t=94) The talk promises guardrails to try tomorrow but points to no published sample project or complete rule set reproducing it.
