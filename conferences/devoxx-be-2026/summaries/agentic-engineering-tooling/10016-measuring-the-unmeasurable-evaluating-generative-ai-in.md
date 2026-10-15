---
title: "Measuring the Unmeasurable: Evaluating Generative AI in Practice"
talkId: "10016"
conference: devoxx-be-2026
speakers: [Erin Pacquetet]
track: Agentic Engineering & Tooling
sessionType: Lunch Talk
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=Qdn-I3q50Ww
durationMin: 41
slides: null
verdict: 5
frames: 8
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Measuring the Unmeasurable: Evaluating Generative AI in Practice

Erin Pacquetet · Lunch Talk · Agentic Engineering & Tooling

## TL;DR

Shipping an LLM demo to production requires trust, and trust comes from an evaluation pipeline that turns manual spot-checking into a repeatable score. Pacquetet builds that pipeline step by step around a client-facing insurance RAG chatbot: simulate inputs across ideal, realistic and adversarial scenarios, write expected answers into an evaluation dataset, and score outputs with layered pass/fail metrics calibrated against human judgment.

## Key takeaways

- Give up controlling LLM inputs and outputs; compensate with system design plus an evaluation pipeline that produces a score at the click of a button.
- Write the evaluation dataset early: drafting expected answers exposes vague or contradictory business rules ("answers must be short") before they cost a week of rework.
- Test realistic and adversarial inputs, not just clean ones: typos, keywords, vague questions, prompt injection and jailbreak attempts.
- Judge free-form answers with narrow, single-criterion checks (e.g. "does the new answer contradict the expected answer?") instead of asking an LLM "is this good?".
- Prefer simple metrics wherever they apply: string matching for a phone number beats an LLM judge on robustness, cost and reproducibility.
- Treat every metric as a proxy for human judgment and calibrate it: a business-approved answer must pass, a rejected one must fail.
- Keep the pipeline alive after launch: new prod risks and threats feed back into the dataset, metrics and thresholds.

## Notes

### [00:33](https://youtu.be/Qdn-I3q50Ww?t=33) The demo-to-prod gap

Pacquetet, senior AI scientist at Paris consulting firm SCIAM, frames the talk: coding agents make an AI proof of concept fast, but shipping to production is hard because LLMs are generative, flexible and difficult to control. Page 5 of the slides (per the frame) puts it as two questions to answer before launch: how do we trust the system, and what counts as "working well"? Her answer to both is a comprehensive evaluation methodology.

### [01:36](https://youtu.be/Qdn-I3q50Ww?t=96) Case study: a client-facing insurance RAG chatbot

The audience joins her fictional engineering team to build an eval pipeline for a Q&A chatbot that retrieves insurance documentation and answers in plain text, with no tool calling. Internal testing went well, but client-facing launch raises the stakes: uncontrollable user inputs, hallucination risk, and no say over what comes out.

### [04:14](https://youtu.be/Qdn-I3q50Ww?t=254) Why LLM products resist evaluation

Teams use LLMs precisely to understand a wide variety of unseen, low-quality inputs and to tailor outputs to them, so uncontrolled inputs and outputs are part of the deal. The creativity-control trade-off follows: unconstrained models hallucinate and leak, over-constrained ones lose the reason to use AI at all.

### [07:22](https://youtu.be/Qdn-I3q50Ww?t=442) The pipeline in three steps

Evaluation means converting manual qualitative checks into a quantitative score through three steps: simulate inputs, feed them through the system to generate outputs, then evaluate the outputs. Run the pipeline continuously during development (a prompt tweak that tanks the score was a bad tweak) and before every deployment, so each version ships with a known score.

### [08:55](https://youtu.be/Qdn-I3q50Ww?t=535) Simulating inputs: ideal, realistic, adversarial

Test questions should span three scenarios. Ideal: grammatical, on-topic questions ("What is the deductible for water damage?") as the baseline. Realistic: typos, bare keywords ("am I covered"), partial context; teams often skip this layer. Adversarial: prompt injection, jailbreaks, bias probes and attempts to elicit a screenshot-worthy failure.

### [12:00](https://youtu.be/Qdn-I3q50Ww?t=720) Architecture and the easy half: constrained output

Output quality is the talk's focus, while operational quality (latency, cost, stability) is monitored like any non-AI product. The chatbot has two agents: a triage LLM outputting only true/false for question validity, and a RAG agent answering valid questions. The triage agent takes an eval dataset of questions with expected true/false labels and plain string matching, yielding a pass/fail score (the worked example lands at 60%).

### [15:36](https://youtu.be/Qdn-I3q50Ww?t=936) What is a good answer?

A good answer must be correct, relevant, complete and safe, plus product-specific rules: a friendly chatbot persona and short responses for a small chat widget. Those rules contradict each other (short yet complete, factual yet chatty). Iterating live on "is renter's insurance mandatory for a tenant in France?", she grows "Yes." into a full answer with coverage details and legal-jargon explanations, then deliberately drops the one-insurance-per-lease exception to protect brevity. The point: several different answers can all be good, so the team must pick a target and a threshold.

### [22:46](https://youtu.be/Qdn-I3q50Ww?t=1366) The dataset as executable contract

The evaluation dataset is the physical form of the specs and the convergence point of business and engineering: business signs the expected outputs as "this is what we mean", developers treat them as targets. Drafting them surfaces implicit and contradictory requirements early, and the resulting one-click score later accelerates every development decision.

### [25:20](https://youtu.be/Qdn-I3q50Ww?t=1520) Four families of metrics

Outputs are scored with deterministic metrics (regex, F1, string matching: exact and reproducible but limited), semantic metrics (ROUGE, BLEU: fast similarity of vector-encoded meaning, though similarity is not quality), probabilistic LLM-as-a-judge (scalable and high-comprehension, but prompt-dependent with variance and bias), and human review (nuanced and close to business expectations, but slow, expensive, and biased too).

### [28:56](https://youtu.be/Qdn-I3q50Ww?t=1736) Why LLM-as-a-judge works

A judge LLM succeeds where the generator stumbles because its task is narrow: read the expected and generated answers, compare key elements, and return true/false on one question such as "are there contradictions?". The slide contrasts this single check against the RAG agent's long chain of duties (understand intent, retrieve documents, locate excerpts, verify sources, satisfy tone and length rules).

### [33:04](https://youtu.be/Qdn-I3q50Ww?t=1984) Combining metrics, then the roadmap

Each dataset entry gets its own metric set: an LLM judge checking contradictions plus string matching for a required phone number, each pass/fail, with the question passing only if all primary metrics pass. Lower-stakes criteria (a closing follow-up question) become tracked secondary metrics. The closing roadmap runs Guidelines → Evaluation Dataset → Metrics + Thresholds → Pipeline Implementation → Human Calibration → Prod, with iteration loops between guidelines and dataset, calibration feedback into judge prompts, and continuous prod feedback into the dataset.

## Tools, libraries and specs

- ROUGE and BLEU scores: embedding-based semantic similarity metrics for comparing generated answers against expected ones.

## Who should watch

Teams moving a first RAG chatbot or Q&A assistant from demo to production gain a complete, ordered method they can copy. Practitioners already running eval datasets with calibrated LLM judges, or anyone wanting eval-harness code, another framework's internals, or adversarial-robustness depth, can skip it.

## Verdict

**5/10**: an ordered evaluation method carried by a worked insurance-chatbot case, with a reasoned account of why narrow LLM judges work, held back by a constructed case, no run on screen, no figures and no published artifact.

**Novelty 1/2**

- **+** [18:41](https://youtu.be/Qdn-I3q50Ww?t=1121) The renter's-insurance answer, grown from "Yes." into the final target response, is the speaker's own example built for this talk.
- **+** [01:36](https://youtu.be/Qdn-I3q50Ww?t=96) The insurance RAG chatbot case study carries the whole pipeline as one continuous worked example.
- **−** The core apparatus (evaluation datasets, LLM-as-a-judge, metric families) is established practice documented in sources such as Zheng et al., "Judging LLM-as-a-Judge" (2023), and the chatbot stays a team exercise rather than a shipped deployment.

**Demonstrated 0/2**

- **−** [07:22](https://youtu.be/Qdn-I3q50Ww?t=442) The pipeline that yields a score at the click of a button is described on slides and in speech; no harness, run or output appears.
- **−** [15:05](https://youtu.be/Qdn-I3q50Ww?t=905) The 60% triage score is a narrated figure for a fictional chatbot, not the visible output of an executed evaluation.

**Measured 1/2**

- **·** [08:24](https://youtu.be/Qdn-I3q50Ww?t=504) The talk makes no quantitative claim: the 93%-versus-91% version comparison is flagged "for instance" and the 60% triage score walks a fictional chatbot, so there is nothing to measure.

**Depth 2/2**

- **+** [29:28](https://youtu.be/Qdn-I3q50Ww?t=1768) The talk explains why a narrow judge task succeeds where "is this a good answer?" fails, contrasting the single contradiction check with the RAG agent's full duty chain.
- **+** [25:50](https://youtu.be/Qdn-I3q50Ww?t=1550) All four metric families are weighed against each other on exactness, cost, bias and coverage, with explicit guidance to prefer deterministic checks wherever they apply.
- **−** [26:20](https://youtu.be/Qdn-I3q50Ww?t=1580) ROUGE and BLEU are described as encoding answers into a vector space and comparing vectors, although they measure n-gram overlap.

**Reusable 1/2**

- **+** [37:12](https://youtu.be/Qdn-I3q50Ww?t=2232) The Guidelines-to-Prod roadmap with roles and iteration loops gives a process teams can reconstruct on their own projects.
- **−** [29:28](https://youtu.be/Qdn-I3q50Ww?t=1768) No repository, sample project, configuration or checklist is published or pointed to; the judge-prompt wording and the triage rules stay fragments on slides.
