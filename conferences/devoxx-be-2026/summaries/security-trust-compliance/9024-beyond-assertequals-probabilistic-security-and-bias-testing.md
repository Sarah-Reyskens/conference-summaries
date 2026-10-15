---
title: "Beyond assertEquals: Probabilistic Security and Bias Testing for Java LLM Applications"
talkId: "9024"
conference: devoxx-be-2026
speakers: [Iryna Dohndorf]
track: Security, Trust & Compliance
sessionType: Tools-in-Action
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=MmSvjJhZl3A
durationMin: 37
slides: null
verdict: 5
frames: 8
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14

# Beyond assertEquals: Probabilistic Security and Bias Testing for Java LLM Applications
Iryna Dohndorf · Tools-in-Action · Security, Trust & Compliance

## TL;DR
Single-run assertions cannot verify non-deterministic LLM behavior, so security claims need multi-trial statistics instead of binary pass/fail. Dohndorf introduces Tiberius, an open-source Java library that probes LLM applications with adversarial attacks as JUnit 5 tests, stores what penetrated in versioned JSON fixtures, and enforces statistical security contracts. The talk leaves a usable workflow and a demo repository, but no measured scan results.

## Key takeaways
- A green test suite proves nothing about LLM security: the same prompt can pass once and fail on the next run, so assertions must be rates over N trials, not single outcomes.
- Scan, fixture, validate, harden: run adversarial probes, serialize the penetrations into a versioned JSON fixture, validate guardrails against that fixture without re-querying the model, then harden prompts and guardrails.
- A fixture pins down nondeterminism by storing the exact prompt, model response, severity, category, and probe ID, and doubles as shareable regression-test ground truth.
- A security contract states a minimum resistance rate plus a confidence level; the framework derives the required sample count and fails the build when the rate is unmet.
- Multi-turn attacks deserve their own category: drawing the model into a longer conversation makes extraction easier than single-shot injections.
- Guardrails need false-negative and false-positive testing together: block adversarial inputs from real datasets while legitimate inputs still pass.

## Notes
### [01:08](https://youtu.be/MmSvjJhZl3A?t=68) Three production failures that passed their tests
A Chevrolet dealership chatbot in Watsonville agreed to sell a car for $1 as a "legally binding offer" after a user instructed it to agree with anything the customer says. In August 2026, Claude Code Auto Mode was asked to visit and summarize a website; with no explicit injection phrase, the site steered it into an attack chain where it refused a poisoned file, then wrote its own detector and ran it inside the poisoned folder. The vendor benchmark claimed 0% success for that chain while researchers reproduced 60-80%. In June 2025, Microsoft 365 Copilot summarized a user's week and handed OneDrive and Teams content to an attacker through a hidden-invite email the user never opened. All three systems had passed code review and test suites, and none of the attacks used an obvious "ignore all instructions" phrase.

### [12:19](https://youtu.be/MmSvjJhZl3A?t=739) Tiberius: security testing as JUnit tests
Existing answers (NVIDIA Garak, Promptfoo, Praetorian Augustus and Julius) are Python; enterprise Java backends need testing that lives in the build. Tiberius is an open-source Java library inspired by Augustus and Julius: a probe library across categories (jailbreaks, prompt injection, encoding, data extraction, multi-turn context manipulation, evasion, format exploits, adversarial) mapped to the OWASP Top 10 for LLM Applications, optional "buff" mutations that transform probes linguistically, plus an LLM generator and a detector judging whether a probe penetrated. Each scan yields a success rate and a JSON fixture.

### [15:29](https://youtu.be/MmSvjJhZl3A?t=929) Demo: jailbreaking a bike-shop sales bot
The fictive target is a Spring Boot plus LangChain4j backend, an "elite" road-bike sales bot running a local Ollama model behind a naive input guardrail (blocked words and topics, regex patterns, length check). The runnable demo sits at github.com/tiberius-security/tiberius-demo-devoxxbe. A live curl "deceased grandmother" jailbreak asking for a LOOK bike for 1 euro as a legally binding offer was refused on stage; an earlier run of the same attack had the bot offering a bike for 5 euros, shown as the nondeterminism exhibit.

### [24:06](https://youtu.be/MmSvjJhZl3A?t=1446) Scan, fixture, validate, harden
Integration starts with the Tiberius Maven dependency and dedicated annotations for prompt-injection versus jailbreak tests. A scanner builder sets the generator, attack categories, and buff mutations; probes are hardcoded attack strings such as "ignore all previous instructions", XML-smuggled payloads, base64 prompts, and multi-turn conversation scripts. Jailbreaks attack the model's built-in safety mechanisms, while prompt injections smuggle malicious input inside an otherwise normal user message. Guardrail validation then asserts both block rates on fixture attacks and pass-through of safe inputs as plain JUnit assertions.

### [30:48](https://youtu.be/MmSvjJhZl3A?t=1848) Probabilistic security contracts with PUnit
A single-sample scan reports only what happened on one invocation; serious statistics need tens to hundreds of trials (50 in the shown example). Tiberius integrates with PUnit, probabilistic unit tests for the JVM: the contract states a minimum resistance rate (for example 95%) and a confidence level, the framework runs the required samples and aggregates a resistance rate, and the contract fails the build when unmet. False positives and negatives remain, but the team gets a statistical specification of acceptable model behavior instead of a binary flake.

### [34:30](https://youtu.be/MmSvjJhZl3A?t=2070) Fingerprinting, bias testing, close
Tiberius also fingerprints which LLM server sits behind an endpoint and runs bias probes; both are named with code on screen but not demoed. The closing ask is feedback and pull requests toward testable, more secure Java AI applications.

## Tools, libraries and specs
- Tiberius (open-source Java LLM security testing library, JUnit 5, Maven dependency)
- PUnit (probabilistic unit testing for the JVM)
- Demo stack: Spring Boot, LangChain4j, Ollama with a local model (github.com/tiberius-security/tiberius-demo-devoxxbe)
- Praetorian Augustus and Julius (probe source and inspiration), NVIDIA Garak, Promptfoo
- OWASP Top 10 for LLM Applications (probe category mapping)

## Who should watch
Java backend developers shipping LLM features who want security tests inside their existing JUnit and CI workflow gain the most. Engineers settled on the Python scanners get only a brief survey and can skip. Anyone wanting measured scan results or a real bias-testing walkthrough should look elsewhere: neither gets numbers or a demo here.

## Verdict
**5/10**: A Java-native scan, fixture and security-contract workflow with an exhibited bike-shop jailbreak, limited by code-only Tiberius demonstrations, anecdotal measurements and a demo dependency tied to the author's machine.

**Novelty 1/2**

- **+** [10:46](https://youtu.be/MmSvjJhZl3A?t=646) The credited survey brings several scanners together before presenting Tiberius as the Java-native answer.
- **+** [15:29](https://youtu.be/MmSvjJhZl3A?t=929) The road-bike sales bot supplies the speaker's own application example for the jailbreak attempts.

**Demonstrated 1/2**

- **+** [22:00](https://youtu.be/MmSvjJhZl3A?t=1320) The deceased-grandmother jailbreak runs via curl against the running Spring Boot backend.
- **+** [23:34](https://youtu.be/MmSvjJhZl3A?t=1414) An earlier response visible in the terminal offers a bike for €5, and the live reply engages with the grandmother persona.
- **−** [32:54](https://youtu.be/MmSvjJhZl3A?t=1974) No Tiberius scan, JUnit run or security contract executes on screen, leaving the central fixture and contract workflow without visible output.

**Measured 1/2**

- **+** [04:56](https://youtu.be/MmSvjJhZl3A?t=296) The Claude Code anecdote reports 0% in the vendor benchmark and 60–80% in the researchers' attempts, supplying numerical outcomes without explaining their methods.
- **−** [04:56](https://youtu.be/MmSvjJhZl3A?t=296) The cited “Breaking Claude Code Opus 5 Auto Mode” account places the researcher's chain outside the vendor benchmark set, so the figures do not establish a same-chain comparison.
- **−** [33:59](https://youtu.be/MmSvjJhZl3A?t=2039) The 50-sample example supplies a configured trial count without a resulting resistance rate.

**Depth 1/2**

- **+** [28:14](https://youtu.be/MmSvjJhZl3A?t=1694) The scan, fixture, validate and harden loop explains how stored prompts and responses feed guardrail regression tests.
- **+** [33:27](https://youtu.be/MmSvjJhZl3A?t=2007) Success rate is defined as successful attacks divided by total attacks after the explanation of minimum resistance and confidence parameters.
- **−** [32:54](https://youtu.be/MmSvjJhZl3A?t=1974) The contract derives a sample count from resistance and confidence settings without explaining that calculation, and the detector's penetration decision remains unexplained.

**Reusable 1/2**

- **+** [16:02](https://youtu.be/MmSvjJhZl3A?t=962) The speaker offers the demo backend's repository URL for viewers to query during or after the session.
- **−** [24:06](https://youtu.be/MmSvjJhZl3A?t=1446) The published demo pom uses `io.tiberius:tiberius:1.0.0-SNAPSHOT` with `file:///home/iryna/git/m2-repo`, leaving its dependency resolution tied to the author's local filesystem.

