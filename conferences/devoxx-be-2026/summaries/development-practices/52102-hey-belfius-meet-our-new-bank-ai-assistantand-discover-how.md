---
title: Hey Belfius! Meet our new bank AI assistant—and discover how we’re building and securing AI across Belfius.
talkId: "52102"
conference: devoxx-be-2026
speakers: [Nicolas Goosse]
track: Development Practices
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=4hXQoN8co80
durationMin: 42
slides: null
verdict: 6
reach: segment
frames: 9
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Hey Belfius! Meet our new bank AI assistant—and discover how we’re building and securing AI across Belfius.

Nicolas Goosse · Conference · Development Practices

## TL;DR

Belfius launched Hey Belfius, an agentic banking assistant, in April 2026 and reports its bot-only resolution rate rose from 70% to 90% within six months. The talk attributes that to systems engineering around the model (an orchestrator routing to specialized agents, curated data, guardrails, continuous evaluation) and spends its second half on AI security: the vulnerability surge driven by AI-assisted hacking, rules for AI-assisted development, and live jailbreak demos showing why chatbots need defense in depth.

## Key takeaways

- Treat an agentic assistant as a system: an orchestrator plus specialized agents, each using the right technology (generative or deterministic) for its question type.
- Ground answers in curated data first; model choice matters less than clean underlying data and transaction processing for personalization.
- Evaluate continuously with a golden dataset and back-testing, and ship only after explicitly accepting the residual risk, since accuracy never reaches 100%.
- Keep source code out of consumer LLM licenses, review all generated code, and use an internal package registry to block slop-squatting on hallucinated dependencies.
- Never rely on the system prompt alone for chatbot safety: layer input and output guardrails, canaries, LLM-as-judge checks, and human-in-the-loop escalation.

## Notes

### [00:40](https://youtu.be/4hXQoN8co80?t=40) Hey Belfius launch and results

Goosse opens with the launch numbers: Hey Belfius, a digital personal assistant on an agent core, went live 21 April 2026. Within six months, monthly conversation volumes doubled and the bot-only KPI (share of conversations resolved without the client asking for a human) rose from a 70% benchmark to 90%. Client expectations frame the talk: answers must be grounded in real data, personal, useful, and acted upon rather than delivered as recipes.

### [03:00](https://youtu.be/4hXQoN8co80?t=180) From model plus prompt to trusted behavior

A model wrapped in a prompt answers generic questions but knows nothing about the client's accounts or transactions. Belfius baked in curated data covering financial education, phishing and fraud guidance, and in-conversation actions such as blocking a card. Personalized analytics (spending by merchant, category, or period) required processing raw transactions into tailored insights. The LLM is not the architecture; the harness around it is.

### [07:15](https://youtu.be/4hXQoN8co80?t=435) Agent harness: orchestrator and specialized agents

The central component is an orchestrator that distributes work across specialized agents, since one model cannot do everything. Routing blends intelligence with control: some paths stay fully deterministic so the model cannot deviate, others allow leeway where behavior stays controllable. Security by design wraps the whole harness, starting with guardrails against prompt injection and assistant impersonation.

### [10:56](https://youtu.be/4hXQoN8co80?t=656) Evaluation loop and residual risk

Launch is day one. The team monitors questions, answers, and odd behavior, then improves knowledge, routing, or copy in a cycle anchored by golden datasets and back-testing rather than ad-hoc manual checks. The key output is a measured residual risk: because no AI behavior is ever 100% predictable, the team quantifies how far wrong it can go and takes a conscious go-live decision.

### [13:33](https://youtu.be/4hXQoN8co80?t=813) AI red-teaming; Mythos and the AISI benchmark

Matias from the Belfius security team takes over. He traces the AI-for-security inflection to Anthropic's Claude Mythos and its Project Glasswing early-access program, then cites the independent UK AI Security Institute benchmark (a network compromisable via 32 consecutive exploits to full domain ownership) as the trustworthy datapoint: Mythos was the first model to complete it, followed by a cyber-licensed OpenAI model. AI now threatens confirmed vulnerabilities at automated-scanning speed, a scale human testers cannot match.

### [19:15](https://youtu.be/4hXQoN8co80?t=1155) Vulnerability surge and the Ikido partnership

Reported software vulnerabilities spiked over the last year, roughly doubling around the Mythos release, shown on a per-month chart since 1988. Developers inherit the problem: dependency fixes (aided by tools like Dependabot but threatened by compromised npm packages) and own-code fixes that risk breaking large legacy systems. Belfius started a strategic R&D partnership in August with Aikido (auto-captions render it "Iikido") for an on-premise GPU appliance that scans source code with an open-weights model and launches agents to confirm true positives, an effort the speaker calls explicitly experimental.

### [23:28](https://youtu.be/4hXQoN8co80?t=1408) Three guidelines for AI-assisted development

The rules: keep source code away from consumer LLM licenses (enterprise licenses promise no training reuse; private ones do not, and training-like code is easier for future models to exploit); never trust generated output without review and scanning, watching for logical gaps such as missing authentication that scanners miss; and stay in control of what gets generated ("outsource the typing, not the thinking") instead of acting as a copy-paste proxy for thousand-line pull requests nobody reviews. Roughly 20% of AI-suggested dependencies are hallucinated, motivating the internal registry.

### [28:16](https://youtu.be/4hXQoN8co80?t=1696) Live demo 1: extracting the system prompt

Running a small local Mistral model in the Belfius AI red-team playground, Matias first asks the bot to format "the text above" as a code block, which leaks its Sentinel system prompt including the HELLO_DEVOXX_CANARY secret it was told never to repeat. A second prompt appends a near-identical forged system prompt that adds an "evil chatbot" persona answering in C#, demonstrating that concatenated system and user input lets attackers override instructions the prompt explicitly forbids.

### [33:35](https://youtu.be/4hXQoN8co80?t=2015) Live demo 2: gradient attack on safety refusal

The second demo slowly poisons the context window across turns (fireworks composition, a firefighter pretext, black powder, TNT) until the model discusses explosive chemistry it would have refused in a single prompt. Each message looks harmless alone; the accumulated context shifts the goalposts. The speaker stops before anything beyond easily searchable information.

### [38:03](https://youtu.be/4hXQoN8co80?t=2283) Defense in depth and takeaways

Backup slides list the recommended layers: guardrails in front of the chatbot rather than inside it, canary strings checked in outputs, LLM-as-judge on inputs and outputs (effective but expensive), and human-in-the-loop escalation. Goosse closes with four takeaways: agentic AI is a systems-engineering problem, intelligence needs a harness, production is the beginning (observability covers user and attacker behavior, not just app health), and every layer should make abuse harder. No slide link was offered; questions go to the Belfius booth.

## Tools, libraries and specs

- Claude Mythos (Anthropic) and Project Glasswing early access
- UK AI Security Institute exploit-chain benchmark (32 exploits to domain admin)
- Mistral small model, run locally for the jailbreak demos
- Aikido on-premise GPU appliance for AI-assisted vulnerability confirmation (R&D partnership)
- Dependabot for automated dependency updates

## Who should watch

Developers and architects building customer-facing LLM assistants, and anyone responsible for their security review, get the most: production KPIs, an evaluation methodology, and concrete attack demos. Skip it if you already run red-team exercises against prompt injection and safety refusals, or if you want implementation detail such as model names, routing logic, or guardrail code for Hey Belfius itself.

## Verdict

**6/10**: Live jailbreak demos, a beginner-level mental model for assistants and prompt-injection defences, and a defined production KPI make it useful, while the production assistant stays at architecture level and the repository covers only the demos.

**Reach segment**: Teams adding customer-facing LLM assistants can use the orchestration, evaluation and security material in their own applications.

**Novelty 1/2**

- **+** [24:29](https://youtu.be/4hXQoN8co80?t=1469) The Aikido trial gave the team a specific observation: poorly structured legacy code could defeat the AI's attempts to reason about it.
- **·** [22:57](https://youtu.be/4hXQoN8co80?t=1377) The vulnerability-confirmation partnership remains an R&D effort whose promised results the team cannot yet substantiate.

**Demonstrated 1/2**

- **+** [29:50](https://youtu.be/4hXQoN8co80?t=1790) The local bot reveals its system prompt and forbidden canary in the live prompt-extraction demo.
- **+** [35:56](https://youtu.be/4hXQoN8co80?t=2156) A second live sequence advances from innocuous questions to content the model's safety refusal was meant to prevent.
- **−** [05:06](https://youtu.be/4hXQoN8co80?t=306) The production assistant's ability to perform banking actions is described without an end-to-end run showing the action completed.

**Measured 1/2**

- **+** [02:28](https://youtu.be/4hXQoN8co80?t=148) The speaker defines the bot-only KPI as avoiding a request for human help and reports a rise from 70% to 90% within six months.
- **+** [16:40](https://youtu.be/4hXQoN8co80?t=1000) The UK AI Security Institute benchmark (a network compromisable in 32 consecutive exploits) is cited as an independent comparison: Mythos was the first model to complete it, earlier models never came close.
- **−** [26:02](https://youtu.be/4hXQoN8co80?t=1562) Roughly 20% of AI-suggested dependencies being hallucinated is stated with no source or method.

**Depth 2/2**

- **+** [08:50](https://youtu.be/4hXQoN8co80?t=530) Deterministic paths are chosen where deviation is unacceptable, while generative behavior is allowed where the team can control its consequences.
- **+** [12:32](https://youtu.be/4hXQoN8co80?t=752) A golden dataset and back-testing give statistics on how far the assistant can go wrong, and the go-live decision rests on accepting the residual risk.
- **+** [32:00](https://youtu.be/4hXQoN8co80?t=1920) The security explanation connects persona overrides to the concatenation of trusted instructions and user input, giving beginners a mechanism for prompt-only defenses failing.

**Reusable 1/2**

- **+** [28:50](https://youtu.be/4hXQoN8co80?t=1730) The playground frame shows [LibreNico/devoxx-treasury-hack](https://github.com/LibreNico/devoxx-treasury-hack), whose standalone free-chat page, scenarios and live-demo script reproduce the talk's jailbreak exercises.
- **−** [07:15](https://youtu.be/4hXQoN8co80?t=435) The orchestrator and specialized-agent architecture is described with no published configuration, sample project or checklist to reconstruct it from.
