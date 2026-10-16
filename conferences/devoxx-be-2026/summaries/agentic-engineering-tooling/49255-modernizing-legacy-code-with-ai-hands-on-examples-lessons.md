---
title: "Modernizing legacy code with AI: hands-on examples & lessons learned"
talkId: "49255"
conference: devoxx-be-2026
speakers: [Koen Vanderkimpen, Wim Lambrecht]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=FvVe9J0Abjg
durationMin: 51
slides: null
verdict: 6
reach: broad
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Modernizing legacy code with AI: hands-on examples & lessons learned

Koen Vanderkimpen, Wim Lambrecht · Conference · Agentic Engineering & Tooling

## TL;DR

Smals Research spent two years applying AI assistants to seven legacy modernization cases, from COBOL dependency mapping to a Java EE to Jakarta EE migration, and reports that AI already handles analysis, documentation, and small translations well while architectural rewrites still need close human supervision. The talk's core message is that migration success comes from the harness around the model: curated context, phased plans, human checkpoints, and audit trails. Wim Lambrecht's deep dive shows the full workflow on a real JBoss EAP 7 to 8 migration driven by training repositories and generated plans.

## Key takeaways

- Treat legacy as a spectrum from stale dependencies to COBOL on ancient infrastructure, and size the AI approach to the case: one-shot rewriting fails on large codebases because the full context never fits or stays relevant.
- Curate context for quality, not just quantity: even million-token windows cannot tell the assistant which part of a large legacy codebase matters for the task at hand.
- Start every migration from a sane codebase: strip secrets and personal data before anything touches a cloud model, confirm test coverage, and isolate the work on a branch or sandbox.
- Run migrations as generated phased plans (plan, progress log, audit trail) with a human approving each phase, and let the assistant flag which phases can run in parallel via subagents.
- Prefer the indirect approach: have the AI build dependency inventories, documentation, and its own guardrails and skills before it touches production code.
- Match the harness to the job: a single big prompt, role-based agents, spec-driven pipelines with JSON contracts and quality gates, or a packaged skill, with reuse across cases as the payoff.

## Notes

### [00:35](https://youtu.be/FvVe9J0Abjg?t=35) Introduction: two kinds of AI development

Koen Vanderkimpen opens by splitting current AI development into vibe coding, where anyone in the business builds an app by prompting, and agentic software development, where professional developers get far more capable tools. Smals is a Belgian non-profit doing ICT services for public institutions, and its eight-person research team tracks upcoming technology on a public blog. The agenda: AI development in general, what legacy means, six brief cases, Wim's Jakarta migration deep dive, and conclusions.

### [04:13](https://youtu.be/FvVe9J0Abjg?t=253) Harness engineering and context

Small apps work with a bare prompt, but as features pile on the agent bogs down in debugging loops until a human tells it to change the data model. The fix is harness engineering: methodologies, CI/CD conventions, standard architectures, instructions, skills, and tools that keep the agent on rails. Context stays king, and curation matters more than window size, since stuffing everything in still leaves the model unable to find the relevant part while burning tokens. Guardrails push outward the codebase size at which quality starts to decline; the best setup today remains an experienced human guiding the AI.

### [07:59](https://youtu.be/FvVe9J0Abjg?t=479) Legacy as a spectrum

No formal definition of legacy code exists, so the speaker lays out a spectrum: COBOL programs against an ancient Natural database at one end, outdated dependencies needing security patches at the other, and same-language migrations such as Struts to a modern stack in the middle. Legacy differs from greenfield AI coding mainly in codebase size, which rules out one-shot rewrites and forces creative decomposition. Translation is optional: searching, dependency mapping, documenting, and building a question-answering chatbot over the old code already helps maintenance teams.

### [10:35](https://youtu.be/FvVe9J0Abjg?t=635) What AI can do for legacy today

Search, analysis, summarization, and small translations (a COBOL fragment to Java poses no problem) already work well. Whole-project architecture changes and business-case changes stay hard and need human guidance, with context drift and context rot as reliability risks. The model is only the building block; the harness around it decides the outcome.

### [12:09](https://youtu.be/FvVe9J0Abjg?t=729) Six cases in brief

Three COBOL cases: AI-written tooling to map dependencies across thousands of interlinked programs; a chatbot over transcribed explainer videos from a retiring expert, with user feedback flowing back into the knowledge base; and an ongoing program-by-program COBOL-to-Java translation blocked organizationally because the dev machines touch production databases, forcing a move-translate-test round trip. A 2024 Java case put old Struts/Java 8 code next to the team's hand-built rewrite and had Claude implement missing features from the old business logic, which worked with babysitting and taught them they needed a harness. A SAS-to-Python ETL translation started ugly with literal transliterations and improved through more context, guardrails, and a skill under construction. A VBA-in-Word shadow-IT case became a mostly non-AI extraction pipeline with AI only analyzing code and writing documentation, compiled back into PDF.

### [18:28](https://youtu.be/FvVe9J0Abjg?t=1108) Preliminary lessons learned

General lessons: iterate and throw away bad first attempts, share lessons across teams, set up AI governance in larger companies, strip secrets and personal data before using cloud AI (a GDPR matter for government), brainstorm with the model and let it push back, have AI build its own tools and guardrails, and keep routine work like builds and report filtering outside the context. Watch for cheating: one model wrote tests that just returned the expected value, so a different model should write the tests. Watch also for training-data bias toward the most popular framework rather than the best one. Legacy-specific lessons: small translations work, new architectures need close supervision, let the AI ask questions instead of guessing, narrow and target the migration, and sort out the test environment early.

### [23:10](https://youtu.be/FvVe9J0Abjg?t=1390) Deep dive: Jakarta EE background and the Odysseus case

Wim Lambrecht takes over for the Java EE to Jakarta EE migration. After Oracle donated Java EE to the Eclipse Foundation, the javax namespace became jakarta, and application servers, Spring Boot, and the JDK line all moved along with it. The case is Odysseus, a social-security application on JBoss EAP 7, Spring 5, and Hibernate 5 deployed on OpenShift, migrating from EAP 7 to 8 as one slice of a company-wide transition plan. A screen capture shows the actual stack lined up for upgrade.

### [28:20](https://youtu.be/FvVe9J0Abjg?t=1700) Prepare and execute phases

Preparation is migration work regardless of AI: isolate on a branch or sandbox, install the assistant with security guardrails, scrub sensitive data (with a tool, never with the AI itself), verify test coverage, and involve the product team from day one through kickoffs and hackathons. Execution starts with /init, which produces a CLAUDE.md-style codebase summary detecting the EAP 7/Spring stack and its OpenShift deployment. The first attempt used one big prompt describing the migration intent and pointing at company training repositories, self-contained Git repos showing the EAP 7 to 8 changes including Dockerfiles. Screenshots show the generated plan with concrete steps (root POM, Hibernate 6.4.4.Final, Spring 6.2.3, Java 21, javax to jakarta), a parallelism map marking sequential and parallel phases for potential subagents, a dependency inventory with a notes column plus a jakarta-dependency-mapping file, and the generated progress.md and audit trail that record each phase and every human correction. Each phase ends by handing control back to the human for testing. Advice: migrate shared common libraries through the full cycle first, then update the inventory and continue with the end products.

### [40:23](https://youtu.be/FvVe9J0Abjg?t=2423) Other approaches: agents, spec-driven, skills

Beyond single-prompt prompting, three later approaches appear. Agentic multi-agent setups define role agents in *.agent.md files (analysis, review) with constrained tools and per-phase model choice left to the human rather than hardcoded. Spec-driven migration centers on a hand-written spec (itself drafted by sparring with an AI) with a spec folder of JSON contracts per phase, quality gates with linters and schema validation, and an orchestrator agent able to spin up phase agents, though the speaker stayed in the loop. A skills-only approach packages the whole EAP 7 to 8 migration knowledge as a skill living in the codebase. Screenshots show a Python analysis-review agent definition and a COBOL-to-Java functional spec with contracts for inventory, Java, and SQL-map schemas.

### [47:47](https://youtu.be/FvVe9J0Abjg?t=2867) Future, economics, and conclusions

Koen returns with two cautions: open-source tooling avoids vendor lock-in but teams risk AI lock-in if providers raise prices to pay off data centers, and the Jevons paradox suggests cheaper software only increases demand, so developers keep their jobs running fleets of agents. Valuable skills become domain knowledge, precise explanation, and criticizing others' work. The closing matrix marks understanding, documenting, small translations, and tooling as working well, with end-to-end migrations of small programs marginal and major rewrites human-led. Recommendations: clean up code, build the right harness, favor the indirect approach (plan in phases, build tools first, ask for input, propose alternatives, review other AIs' work), share practices and skills company-wide, and treat AI as not yet a silver bullet.

## Tools, libraries and specs

- Claude (CLI) and GitHub Copilot as migration assistants; OpenAI Codex named alongside them
- CLAUDE.md / AGENTS.md / Copilot instructions codebase summaries generated by /init
- JBoss EAP 7.4 to EAP 8, Spring 5 to 6.2.3, Hibernate 5 to 6.4.4.Final, Java 21, Maven multimodule builds, OpenShift deployment
- Model Context Protocol (MCP): a backlog-mcp server tracking spec-driven pipeline tasks
- Docker sandboxes for isolated migration work
- SAS to Python, COBOL to Java/Spring Boot, Struts to modern Java, VBA/Word-macro extraction pipelines

## Who should watch

Teams facing framework or namespace migrations (Jakarta EE in particular) and engineers building AI migration harnesses will find directly reusable workflow patterns. Engineering leads get a realistic capability map of what to delegate versus supervise. Viewers wanting measured speedup or cost numbers, or a live coding demo instead of screenshots, should look elsewhere.

## Verdict

**6/10**: A seven-case migration study brings the team's failures, generated artifacts and reasons for its harness choices, with no end-to-end run or measurements backing its speed and profitability claims.

**Reach broad**: Developers, tech leads and architects maintaining business applications can apply the context, planning and review practices to AI-assisted work on their existing codebases.

**Novelty 2/2**

- **+** [12:09](https://youtu.be/FvVe9J0Abjg?t=729) The speakers' COBOL cases show how dependency-analysis tooling and a retiring expert's recorded explanations became aids for teams maintaining unfamiliar code.
- **+** [17:23](https://youtu.be/FvVe9J0Abjg?t=1043) A model wrote tests that "just returned the correct value", a failure encountered in the team's own work.
- **+** [49:50](https://youtu.be/FvVe9J0Abjg?t=2990) The closing synthesis separates the small translations their cases supported from end-to-end migrations and architectural rewrites that still required human guidance.

**Demonstrated 1/2**

- **+** [34:06](https://youtu.be/FvVe9J0Abjg?t=2046) A generated migration plan appears on screen with Hibernate, Spring and namespace changes broken into phases.
- **+** [41:27](https://youtu.be/FvVe9J0Abjg?t=2487) The Python analysis-review agent definition appears on screen as a real *.agent.md file.
- **−** [38:17](https://youtu.be/FvVe9J0Abjg?t=2297) Phase execution is described over static screenshots, without an actual end-to-end run shown on screen.

**Measured 0/2**

- **−** [21:38](https://youtu.be/FvVe9J0Abjg?t=1298) The "couple of $10,000" figure is speculation about an approach the speakers have not used, so it measures none of their results.
- **−** [46:44](https://youtu.be/FvVe9J0Abjg?t=2804) The claim that the approach is "absolutely" profitable comes with no time, cost or before/after numbers.
- **−** [22:40](https://youtu.be/FvVe9J0Abjg?t=1360) The claim that AI lets you "analyze faster" has no measured speed-up behind it.

**Depth 2/2**

- **+** [05:18](https://youtu.be/FvVe9J0Abjg?t=318) Even with a million-token window the AI cannot tell which part of a large legacy codebase matters, so context relevance limits one-shot migration.
- **+** [44:04](https://youtu.be/FvVe9J0Abjg?t=2644) Linters and JSON validation check phase acceptance criteria without relying on the model to grade itself.
- **+** [41:59](https://youtu.be/FvVe9J0Abjg?t=2519) The agent asks the human which model to use per phase instead of hardcoding one because models change all the time.

**Reusable 1/2**

- **+** [43:31](https://youtu.be/FvVe9J0Abjg?t=2611) The spec folder's JSON contracts for inventory and later phases are shown well enough to reconstruct their structure.
- **+** [39:21](https://youtu.be/FvVe9J0Abjg?t=2361) Run the full migration cycle on the shared common library first, update the dependency inventory, then continue with the applications.
- **−** [46:11](https://youtu.be/FvVe9J0Abjg?t=2771) The finished migration skill is shown living in a codebase, but no public repository, link or checklist is supplied.
