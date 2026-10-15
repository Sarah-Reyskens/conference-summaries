---
title: "Prompt It Right: Spring Boot Testing in the AI Era"
talkId: "7006"
conference: devoxx-be-2026
speakers: [Philip Riecks]
track: Development Practices
sessionType: Deep Dive
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=d6D8nef-32c
durationMin: 153
slides: null
verdict: 7
frames: 17
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Prompt It Right: Spring Boot Testing in the AI Era
Philip Riecks · Deep Dive · Development Practices

## TL;DR
A three-hour session split into two blocks: a refresher on Spring Boot testing fundamentals (unit, slice, and integration tests, Testcontainers, context caching) and a set of practices for steering AI coding agents toward a fast, trustworthy test suite. The core argument is that code generation is now cheap and verification is the bottleneck, so teams should encode their testing standards in versioned agent skills and optimize the suite for fast feedback.

## Key takeaways
- Pick the cheapest test that proves the behavior: unit tests for services, slice tests for cross-cutting web/persistence concerns (routing, validation, serialization, security), integration tests for end-to-end user journeys.
- A unit test on a controller proves almost nothing: it cannot verify request mappings, Bean Validation, ObjectMapper behavior, or Spring Security rules.
- Spring's context cache reuses application contexts only when the merged context configuration is identical; aligning profiles, properties, and mocks across integration tests is the biggest build-time lever.
- Never sprinkle `@DirtiesContext` to silence flaky tests: each use destroys a cached context, and on a shared base class it disables reuse for the whole suite.
- Encode testing standards once as agent skills (markdown checked into the repo) instead of repeating prompt templates; the skill frontmatter routes the agent to the right standard on demand.
- Gate context growth in CI: fail the pipeline when the Spring Test Profiler reports more contexts created than the agreed threshold.

## Notes

### [00:34](https://youtu.be/d6D8nef-32c?t=34) Intro, audience poll, and agenda
After a Menti poll (116 participants: most write tests as a human/AI mix, CI builds mostly 10-30 minutes, Friday-deploy confidence averaging 5.9/10), Riecks laid out the two 75-minute blocks: fundamentals first, then agentic testing practices, with a 30-minute break between. The recurring goal was judgment: developers still need to decide whether an AI-written test is valid and why a context fails to start.

### [12:04](https://youtu.be/d6D8nef-32c?t=724) The north star: confidence in every commit
Coverage percentages were rejected as a target after seeing assertion-free tests written to satisfy Jenkins. The proposed north star is subjective: a Renovate PR bumping Spring Boot to a new major on a Friday afternoon shows a green pipeline, and the team merges and deploys without hesitation. Good tests catch bugs, but their larger value is fast feedback and deploy confidence, especially when agents can spawn large volumes of changes in parallel.

### [15:44](https://youtu.be/d6D8nef-32c?t=944) Choosing a test type
The decision tree starts with one question: does the test need an application context? No context means a plain unit test (JUnit, Mockito, assertion library). A full context means `@SpringBootTest`; a partial one means a slice test. Riecks keeps naming pragmatic: `*Test` for unit tests, `*IT` for anything with a context, which also maps to Maven Surefire vs. Failsafe phases so unit failures give fast feedback and parallelization can be tuned separately per phase.

### [21:20](https://youtu.be/d6D8nef-32c?t=1280) The spring-boot-starter-test toolbox
Every Spring Boot project ships with `spring-boot-starter-test`, which cannot be deselected on start.spring.io. It pulls in JUnit, Mockito, AssertJ, Hamcrest, JSONAssert, JSONPath, XMLUnit, and Awaitility, with versions managed by Spring Boot. Awaitility was highlighted for async tests (e.g. a message listener writing to a database): wait at most N seconds for a state instead of `Thread.sleep`. Test-scoped dependencies never land in the production jar, so there is no reason to exclude unused ones.

### [26:33](https://youtu.be/d6D8nef-32c?t=1593) Unit tests and their limits
Unit tests (no Spring imports at all) cover service-level business logic quickly and in high volume. The limits were demonstrated on a REST controller (`POST /api/customers`, Bean Validation, 201 + Location header): a Mockito-based unit test that calls the Java method directly stays green when the mapping changes, when validation breaks, when Jackson serialization drifts (e.g. Java time falling back to timestamps after a version bump), and when security rules change. Controller behavior needs a slice test instead.

### [34:53](https://youtu.be/d6D8nef-32c?t=2093) Slice testing: @WebMvcTest and MockMvc
Slice annotations carve a technical domain (web, persistence, HTTP clients) out of the full context via an include-list ("shopping list") of bean types; anything below the cut, like a service injected into a controller, must be provided as a `@MockitoBean`. `@WebMvcTest` gives a mocked servlet environment plus MockMvc, which acts as both environment and client: tests perform HTTP calls with content types and payloads, and verify status codes, headers, serialization, validation errors, and security. Spring Security integration allows placing an authenticated user with roles into the security context, or faking JWT claims via post-processors, without a running Keycloak. A live demo showed a malformed email producing a 400 with MockMvc's debug output of request and resolved exception. Other slices mentioned: `@DataJpaTest`, `@JsonTest`, `@RestClientTest` (with a mock HTTP server for retry/timeout scenarios), custom slices for messaging, and Spring Cloud AWS's `@SqsTest`. The main pitfall is not knowing the include-list, which makes missing-bean failures confusing.

### [49:05](https://youtu.be/d6D8nef-32c?t=2945) Integration testing with Testcontainers
`@SpringBootTest` starts the entire context, and Testcontainers was presented as the standard answer for infrastructure: a few lines of Java start a version-pinned Postgres (matching production) on an ephemeral port, a pattern that extends to brokers, identity providers, and blob storage. Two web environments matter: the default `MOCK` starts everything except the servlet container (MockMvc again, same-thread security-context overrides still work), while `RANDOM_PORT` starts Tomcat for real local HTTP via `WebTestClient`, `TestRestClient`, REST Assured, or the JDK client. With a real port the thread-local security trick stops working, so tests must supply real authorization (e.g. a Testcontainers Keycloak with a signed JWT). First-test setup is the expensive part; every later test reuses the scaffolding.

### [61:11](https://youtu.be/d6D8nef-32c?t=3671) Context caching
Spring Test keeps a `LinkedHashMap` of size 32 mapping `MergedContextConfiguration` to started contexts, active in every project with no setup. A client build dropped from 26 to 12 minutes on `mvn verify` purely by optimizing cache reuse. The cache key is an exact hash over profiles, initializers, property overrides, mocked/spied beans, and every other customization; even one differing profile forces a new multi-second context start. Reuse can be spotted visually (slow first test, fast followers, Spring Boot banner marking a restart), via `DEBUG` logging on the cache package, or via Riecks's open-source Spring Test Profiler, which renders an HTML report with per-context test assignment, a timeline, and a diff view of which customization points diverge between two contexts.

### [70:39](https://youtu.be/d6D8nef-32c?t=4239) What breaks the cache, plus parallelization
`@DirtiesContext` tells Spring to discard the context after the test; found on one shared abstract base class, it once disabled all reuse in a client project. For parallelization, build-tool forking gives each JVM its own cache (splitting identical contexts across JVMs wastes reuse), while JUnit Jupiter's thread pool shares one thread-safe cache in a single JVM. Start by parallelizing unit tests, then integration tests step by step. Pitfalls for the latter: `findAll` size assertions against concurrently written rows (fix: randomized business keys per test class), broad WireMock stubs, and `@Transactional` data visibility differing between the MOCK and real-port setups.

### [73:46](https://youtu.be/d6D8nef-32c?t=4426) Mutation testing teaser and Q&A
A 100%-covered age/username validation method with weak assertions motivated PIT mutation testing: mutants (e.g. flipping `< 18`, replacing an exception with a magic number) that leave the suite green expose meaningless tests. Q&A covered running black-box tests against a locally started app with REST Assured (fine as a final pipeline stage, but weaker for manufacturing corner-case state) and whether developers or QA own integration tests (the best teams seen had developers own testing and on-call end to end).

### [84:21](https://youtu.be/d6D8nef-32c?t=5061) Why AI changes the testing calculus
Block two opened with the claim that a fast automated suite is now non-negotiable: skipping line-by-line review of generated code without tests means regressions and shortcuts go unnoticed. Citing Google's DORA report, Riecks argued AI amplifies existing practices in both directions, so teams that treated tests as an afterthought now produce weak suites faster. The Formula 1 metaphor framed it: an agent is a faster engine, but on a bumpy road (flaky, slow suite) a faster car hits the wall sooner. Since code generation is nearly free, verification is the new bottleneck, and DORA's fast-flow/fast-feedback capabilities both rest on suite quality.

### [95:52](https://youtu.be/d6D8nef-32c?t=5752) "Write meaningful tests" is not a prompt
Models now produce compiling, green-on-first-run tests, but "meaningful" hides unresolved judgments: fast, parallelizable, deterministic (inject a `Clock` instead of `Instant.now()`), one reason to fail, and failure messages that explain themselves months later (a bare `expected true but was false` costs 20-30 minutes). Repeating these requirements in every prompt does not scale across a team, which motivates writing testing standards down once as skills.

### [100:35](https://youtu.be/d6D8nef-32c?t=6035) Agent skills for testing standards
A skill is a checked-in markdown file (portable across Claude Code, Copilot, Juni, Codex, Cursor, and model providers) that an agent lazy-loads when its description matches the task, keeping the base context lean. Riecks's layout pairs `SKILL.md` (trigger, project knobs, scope, rules, workflow) with `references/testing-standards.md` (a SonarQube-style rule catalog with IDs and severity, e.g. TS-7: a failure message on every assertion) and `references/examples.md` (good/bad assertion pairs). The frontmatter description acts as a routing rule:

```yaml
# from slide at 106:21
---
name: unit-testing
description: Write, review or refactor unit tests for Spring Boot
  classes ... without a Spring context. Use when the user asks for
  a unit test, mentions JUnit, Mockito or AssertJ ... Not for
  "@SpringBootTest, slice tests or Testcontainers ...
---
```

Seven or eight skills cover unit, slice, web-slice (assert every property at least once, block anonymous access), integration, Testcontainers setup, end-to-end, plus a read-only test-setup-review skill that audits a repo's caching and suite health. Project-specific knobs (Maven vs Gradle, naming conventions, how to run one test) get filled in by an onboarding prompt; company-wide skills can live in a shared repo.

### [118:25](https://youtu.be/d6D8nef-32c?t=7105) Fast suites: containers, contexts, and CI gates
Container guidance: prefer the singleton-container pattern over `@Testcontainers` start/stop churn, pin image versions (unpinned Chrome drivers broke Selenium suites), never use fixed ports, match the production database with Flyway/Liquibase instead of H2, and enable Testcontainers reuse locally so morning-started containers stay hot all day. Context guidance: share one abstract integration-test base class and discipline `@MockitoBean` use, since each mock combination is a new context start. Enforcement is automated: the profiler writes `target/spring-test-profiler/results.json`, and a CI step fails the build past a context-count threshold; Docker start events separately reveal whether containers are reused:

```sh
# from slide at 127:50
jq '.contextsCreated' target/spring-test-profiler/results.json
```

Mutation testing with PIT History should be introduced incrementally on new/changed code only (with the history file cached between CI runs), mirroring SonarQube's new-code focus. On TDD with agents, evidence was mixed (Kent Beck in favor with a warning that agents may delete failing tests; Priya Bulusu's Thoughtworks experiment finding no significant difference), so no default recommendation: lean toward it for less experienced teams, skip it when review judgment is already strong.

### [134:08](https://youtu.be/d6D8nef-32c?t=8048) MCP servers and the daily loop
Three MCP servers per project: Context7 for current library docs (used explicitly in prompts when agents emit outdated Spring Boot 3.5 code for a Boot 4 project), the CI provider's MCP (read workflows, wait on runs, re-run flakes, open PRs, read tickets, all without leaving the agent loop), and Playwright for local browser verification of full-stack features with stored login state. The daily loop: agent plus developer plan from a groomed ticket, verify locally against `spring-boot:run` with fast tests and Playwright, push to a feature branch, and let the agent wait on CI before requesting a small human review.

### [140:25](https://youtu.be/d6D8nef-32c?t=8425) Beyond the suite: production will still surprise
Untestable failures cited from experience: a shared third-party API key expiring, a remote SSL certificate lapsing, an RDS instance degraded after a maintenance window. The response is lifecycle practices: shift left, deterministic pipelines without duplicated work (one project compiled three times across stages), small frequent releases, feature flags decoupling deploy from release, monitoring with runbooks linked from every alert (Datadog alert pointing at a GitHub runbook with Kibana deep links and rollback steps), and tested fast rollbacks. For testing LLM/RAG components (Spring AI, LangChain4j), the pointer was Jason's book "Testing AI" for framework-agnostic mental models. The closing line: with AI you can delegate the typing, but ownership still pages you at 3 a.m.

## Tools, libraries and specs
- Spring Boot 4 / Spring Test (context caching, `@SpringBootTest`, `@WebMvcTest`, `@MockitoBean`, MockMvc)
- spring-boot-starter-test: JUnit 5, Mockito, AssertJ, Hamcrest, JSONAssert, JSONPath, XMLUnit, Awaitility
- Testcontainers (singleton container pattern, reuse mode), Flyway / Liquibase, Postgres
- Spring Test Profiler (open-source HTML report by the speaker)
- PIT mutation testing with History feature
- WireMock for HTTP stubbing
- Agent skills (SKILL.md + testing-standards.md + examples.md) for Claude Code, GitHub Copilot, Juni, Codex, Cursor
- MCP servers: Context7, GitHub/GitLab CI, Playwright
- Spring Cloud AWS `@SqsTest`, Spring AI, LangChain4j
- DORA report (fast flow / fast feedback), Menti poll, Devoxx companion app

## Who should watch
Spring Boot developers who review AI-generated tests or want to speed up their suite gain the most; beginners get a compact map of the test types, and experienced teams get the context-caching and skills material. Teams without Spring or without agentic workflows can skip the second block, and viewers wanting ready-made skill files should know the session teaches the pattern while the finished templates ship with the speaker's paid course.

## Verdict
**7/10**: Slice and cache internals plus a published testing-skill and CI-gate sample carry the session, but skill-driven test generation is not demonstrated end to end.

**Novelty 1/2**

- **+** [104:18](https://youtu.be/d6D8nef-32c?t=6258) Each skill pairs its main file with a references folder encoding testing standards with IDs and severity for reportable review.
- **+** [70:39](https://youtu.be/d6D8nef-32c?t=4239) A client project once disabled all context reuse through a `@DirtiesContext` annotation on a shared abstract base class.
- **−** [110:03](https://youtu.be/d6D8nef-32c?t=6603) The assertion-message standard is offered as an adjustable preference without an original comparison establishing when it improves test review.

**Demonstrated 1/2**

- **+** [44:53](https://youtu.be/d6D8nef-32c?t=2693) A live MockMvc trial run shows a malformed email returning 400 with request and exception debug output.
- **+** [116:50](https://youtu.be/d6D8nef-32c?t=7010) Claude Code's skill listing shows the checked-in unit-testing skill available to the agent.
- **−** [117:22](https://youtu.be/d6D8nef-32c?t=7042) The agent loading a skill and writing a test is skipped because the run takes time and is nondeterministic.

**Measured 1/2**

- **+** [61:43](https://youtu.be/d6D8nef-32c?t=3703) A client build reportedly dropped from 26 to 12 minutes on `mvn verify` purely by optimizing cache reuse.
- **+** [68:32](https://youtu.be/d6D8nef-32c?t=4112) The sample Maven profiler report shows 9 contexts created, 11 cache hits, 9 misses and a 55% hit rate.
- **−** [68:32](https://youtu.be/d6D8nef-32c?t=4112) The suggested 21-second saving is a projection rather than a measured before-and-after comparison, and the client timing claim has no stated measurement setup.

**Depth 2/2**

- **+** [66:29](https://youtu.be/d6D8nef-32c?t=3989) Context reuse requires matching `MergedContextConfiguration` keys, so different active profiles prevent sharing even when the resulting contexts might look similar.
- **+** [41:14](https://youtu.be/d6D8nef-32c?t=2474) The slice shopping list is a set of included types in `WebMvcTypeExcludeFilter`, so dependencies outside the slice must be supplied, usually as mocks.
- **+** [58:02](https://youtu.be/d6D8nef-32c?t=3482) With a real-port setup the test and application run on separate threads, so thread-local security-context overrides stop working and tests need real authorization.

**Reusable 2/2**

- **+** [103:47](https://youtu.be/d6D8nef-32c?t=6227) The slide points to the [published sample project](https://github.com/rieckpil/talks/tree/main/prompt-it-right), which includes controller tests and the unit-testing skill with its standards and examples.
- **+** [127:50](https://youtu.be/d6D8nef-32c?t=7670) The public sample includes a context-count checking script and CI workflow implementing the profiler-based build gate shown here.
- **−** [148:47](https://youtu.be/d6D8nef-32c?t=8927) The full seven-skill template library is offered through the speaker's paid course; the public project supplies the unit-testing example.

