---
title: Testing Architecture Made Simple
talkId: "8196"
conference: devoxx-be-2026
speakers: [Gunter Rotsaert]
track: Architecture & Modernization
sessionType: Tools-in-Action
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=asAxisu6EQ0
durationMin: 23
slides: null
verdict: 8
reach: segment
frames: 6
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Testing Architecture Made Simple

Gunter Rotsaert · Tools-in-Action · Architecture & Modernization

## TL;DR

Rotsaert argues architectural rules only survive when they run as tests in the build, then demonstrates ArchUnit for hand-written rules and the Taikai library for ready-made ones. A Java or Spring team leaves with a copy-paste starter test and a playbook for growing its own rule set, including rules that keep AI-generated code inside the team's conventions.

## Key takeaways

- Express layered-architecture boundaries as ArchUnit tests so violations fail the build instead of depending on code review.
- Start from Taikai's pre-built rules rather than a blank ArchUnit test: one dependency plus a builder-style test covers controllers, services and repositories.
- Ban unwanted imports with a one-line dependency rule (his example: Lombok) to force the team discussion explicitly.
- Standardize one sanctioned way to bind Spring configuration into code, then encode it as combined Taikai rules.
- Ship the architecture test in the team's Maven archetype so every new project starts with it.

## Notes

### [00:32](https://youtu.be/asAxisu6EQ0?t=32) Diagrams rot; tests don't

Teams start with documentation and conventions, then take shortcuts and the diagrams stop matching the code. In a layered Spring Boot app this shows up as repositories injected into controllers, framework classes injected into the domain model, indirect cyclic dependencies invisible in review, and a utils class growing into a god class. Reviews miss these in large AI-assisted PRs, so architecture needs automated tests.

### [04:46](https://youtu.be/asAxisu6EQ0?t=286) ArchUnit basics

A JUnit test declares its scope with an analyze-classes annotation, then states rules such as "classes in the repository package should only be accessed by services and repositories"; running it fails with a message listing each violation. ArchUnit ships a pre-built layered-architecture rule, and an import option keeps the rules from applying to test classes.

### [07:52](https://youtu.be/asAxisu6EQ0?t=472) Taikai: pre-built rules on a builder

Starting from a blank ArchUnit test against huge documentation is hard, and hand-written suites grow into unmaintainable rule lists. Taikai adds one dependency (ArchUnit comes transitively) and a `Taikai.builder()` with a namespace plus categories: Spring controllers should be `@RestController`-annotated, end with Controller, and not depend on other controllers or repositories. `check()` stops at the first violation.

```java
// from slide at 08:30
Taikai.builder()
    .namespace(BASE_PACKAGE)
    .spring(spring -> spring
        .controllers(controllers -> controllers
            .shouldBeAnnotatedWithRestController()
            .shouldNotDependOnRepositories()))
    .build()
    .check();
```

### [10:29](https://youtu.be/asAxisu6EQ0?t=629) Config roulette, exclusions, the full suite

Spring Boot offers many equivalent ways to bind configuration into code; a PR stacking four or five config annotations ("configuration roulette") worked but was wrong. His standard is `@ConfigurationPropertiesScan` on the main class scoped to a config package plus an immutable record, enforced by combined Taikai rules. Generic exceptions from Spring Security config are forbidden by rule with a documented exclusion for the class that knowingly throws them. The complete suite also excludes generated OpenAPI code, pins down utility classes and logging, uses `checkAll()` to see every violation, and reuses a company default config through the builder.

### [17:13](https://youtu.be/asAxisu6EQ0?t=1033) Lessons and the adoption question

Plain ArchUnit rules, such as one mirroring a SonarQube rule, drop into the Taikai build when no pre-built rule fits. Start from the documented copy-paste starter test, add rules only as problems appear, and enforce strictly for AI-generated code: his team generated ArchUnit rules from their SonarQube quality gate via its MCP server so AI output passes it. Adoption only stuck once the test shipped in the team's Maven archetype. Taikai has one maintainer but tracks dependency upgrades fast, holds about 250 rising GitHub stars with no open issues, and forks cheaply since it is plain ArchUnit underneath. No audience questions followed.

## Tools, libraries and specs

- ArchUnit (architecture tests for Java)
- Taikai (pre-built ArchUnit rules, Spring categories)
- Spring Boot 3.5, Spring Security
- JUnit, Lombok, SonarQube and its MCP server
- OpenAPI Maven generator plugin, Maven archetypes

## Who should watch

Java and Spring developers who have never written architecture tests, or teams fighting config sprawl and AI-generated code that ignores conventions. Skip it when ArchUnit already runs in your build: the rule catalog and the docs will teach you the rest faster.

## Verdict

**8/10**: Architecture-test failures and passes run on screen, a beginner-level model for choosing and adapting rules, and a published demo project make this usable; the experience is illustrative and the outcome claims lack comparative measurements.

**Reach segment**: Java teams adopting ArchUnit or Taikai, especially Spring Boot teams standardizing their services, can use the rule-building walkthrough directly.

**Novelty 1/2**

- **+** [20:23](https://youtu.be/asAxisu6EQ0?t=1223) Colleagues did not adopt the test until it went into the team's Maven archetype, an adoption lesson beyond the rule catalog.
- **+** [19:21](https://youtu.be/asAxisu6EQ0?t=1161) The team used the SonarQube MCP server to have an AI model generate ArchUnit rules from its quality gate, a practice the Taikai docs do not give.

**Demonstrated 2/2**

- **+** [05:49](https://youtu.be/asAxisu6EQ0?t=349) The IDE shows the repository-access architecture test failing with the controller's violations listed in its output.
- **+** [14:37](https://youtu.be/asAxisu6EQ0?t=877) The Taikai generic-exception rule fails on the Spring Security configuration, then passes once the documented exclusion is added.

**Measured 1/2**

- **+** [20:55](https://youtu.be/asAxisu6EQ0?t=1255) The maintenance assessment supplies descriptive numbers, about 250 GitHub stars and no open issues, with no comparison or method.
- **−** [19:51](https://youtu.be/asAxisu6EQ0?t=1191) The claim that generated code fails the SonarQube quality gate less often has no before/after failure counts or stated measurement method.

**Depth 2/2**

- **+** [02:07](https://youtu.be/asAxisu6EQ0?t=127) Direct repository access can be reasonable for CRUD yet still violate an agreed diagram, so architecture tests enforce a team's decisions rather than a universal layering rule.
- **+** [07:21](https://youtu.be/asAxisu6EQ0?t=441) A blank ArchUnit test is hard to start and hand-written suites fill with near-duplicate rules, which is the reason given for building on a predefined-rule library.
- **+** [21:59](https://youtu.be/asAxisu6EQ0?t=1319) The single-maintainer risk is weighed against Taikai's thin ArchUnit foundation, few dependencies and the option to fork, giving beginners a reasoned basis for choosing the wrapper.

**Reusable 2/2**

- **+** [22:29](https://youtu.be/asAxisu6EQ0?t=1349) The references slide publishes [the demo repository](https://github.com/mydeveloperplanet/archunit), and the speaker explicitly offers its examples to copy.
- **+** [18:15](https://youtu.be/asAxisu6EQ0?t=1095) The Taikai documentation carries a copy-paste starter test, including one for Spring Boot, that a team can add and run the next day.
