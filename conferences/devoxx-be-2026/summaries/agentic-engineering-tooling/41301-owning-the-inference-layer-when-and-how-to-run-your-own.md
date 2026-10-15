---
title: "Owning the inference layer: When and how to run your own models"
talkId: "41301"
conference: devoxx-be-2026
speakers: [Maarten Vandeperre, Camille Nigon]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=QbA-rs7XLEk
durationMin: 51
slides: null
verdict: 7
frames: 10
reviewedAt: 2026-10-15
---

# Owning the inference layer: When and how to run your own models

Maarten Vandeperre, Camille Nigon · Conference · Agentic Engineering & Tooling

## TL;DR

Two Red Hat architects frame hosted model APIs versus self-hosted inference as buying coffee versus brewing it, then run the same Quarkus coffee-ordering app against OpenAI, a local model in Podman AI Lab, and OpenShift AI model-as-a-service. The argument lands on a hybrid: put an AI gateway in front of every model call for auth, quotas and observability, and move workloads to owned infrastructure where cost, latency or data control justifies it.

## Key takeaways

- Start the self-hosting journey with a gateway in front of external models to gain token metering and per-team quotas, then migrate models behind it gradually.
- Hosted APIs expose you to price changes, shared-key billing with no drill-down, queue latency, silent model upgrades, prompt leakage and access shutoffs.
- Self-hosting trades those risks for upfront GPU cost, idle capacity, peak-demand handling, model selection sprawl and unclear team ownership.
- Small models (4B local, 0.6B on CPU) already handle constrained tasks like order interpretation; start there before buying full GPUs.
- Test every model swap even when the API shape is identical, because LLM behavior is nondeterministic across versions.

## Notes

### [01:37](https://youtu.be/QbA-rs7XLEk?t=97) Setup: three ways to get coffee

After a brief Red Hat product overview, Vandeperre introduces the running analogy: hosted APIs (OpenAI, Anthropic, Gemini) are the coffee shop across the street, self-hosting is buying a Jura machine, and managed platforms (Bedrock, Azure Foundry) are a middle ground with limited choices. The three demo variants keep identical UI and backend; only the model call changes.

### [07:19](https://youtu.be/QbA-rs7XLEk?t=439) Eight risks of hosted APIs

With audience help, the speakers enumerate hosted-API risks: unpredictable pricing, shared API keys with no cost drill-down, queue latency and peak demand outside your control, silent model or engine upgrades, prompt and RAG data leaking past company boundaries, sovereignty exposure (a vendor can cut access), a limited model menu, and pure operational expenditure that never reduces future bills.

### [11:33](https://youtu.be/QbA-rs7XLEk?t=693) Demo 1: the app running on a local model

Vandeperre opens what is announced as the OpenAI variant, but the app on screen is the already-running Podman instance (badged Podman AI Lab, Qwen3 4B) that returns a €14.00 quote, passes human review, and confirms it into an order. The OpenAI backend itself is never run. The speaker keeps a human in the loop because smaller models hallucinate quantities.

### [14:10](https://youtu.be/QbA-rs7XLEk?t=850) Why run your own models

Motivations named are data continuity if a vendor cuts access, portability between providers, and model lifecycle control (customers ask how to freeze a model version that behaves exactly right). On sovereignty, Vandeperre argues data residency is not sovereignty while jurisdiction and kill switches apply, and distinguishes real sovereignty from "marketing sovereignty" of merely running in Europe.

### [18:16](https://youtu.be/QbA-rs7XLEk?t=1096) The costs of brewing it yourself

Nigon walks through self-hosting challenges with the audience: upfront GPU cost, idle capacity overnight, peak demand, model and quantization sprawl on Hugging Face, maintenance churn, missing skills, and ownership ambiguity across app, infra and security teams. Without assigned owners, she recommends a managed platform instead.

### [22:25](https://youtu.be/QbA-rs7XLEk?t=1345) The local-model variant explained

The segment replays the already-running app's backend setup: a 4B-parameter model served by Podman Desktop AI Lab on the laptop (a 9B model was abandoned after it saturated the hotel Wi-Fi during download). Vandeperre shows the AI Lab model catalog, one-click model services with OpenAI-compatible `/chat/completions` endpoints, the temperature playground, and copy-paste curl and Quarkus client snippets.

### [27:08](https://youtu.be/QbA-rs7XLEk?t=1628) Serving concerns: latency, capacity, quantization

Nigon lists what the app needs from a model: the right model for the use case, short time-to-first-token, and enough peak capacity. Capacity tactics include scheduling fine-tuning and agentic jobs overnight and sharing GPUs via NVIDIA multi-instance GPU. Quantization is illustrated with an image analogy: a 2.4 MB original versus a 73 kB compressed copy with barely visible difference, so the choice depends on the use case.

### [31:19](https://youtu.be/QbA-rs7XLEk?t=1879) The serving stack

The stack is presented as separable layers: accelerators (NVIDIA via operators, with AMD as possible future option), the inference server, and the model. vLLM is named the de facto open standard via efficient KV-cache use, with the Neuromagic paper as reference. Red Hat validated models on Hugging Face ship optimized for vLLM with published latency figures, and llm-d adds distributed inference with smart request scheduling across model pods.

### [35:31](https://youtu.be/QbA-rs7XLEk?t=2131) Shadow AI and the AI gateway

Ten developers each deploying their own LLM creates shadow AI: wasted GPUs, no governance, nobody on call. The answer is a model-as-a-service gateway holding authentication, per-team subscriptions with token quotas and rate limits (HTTP 429), usage tracking and chargeback, in front of both local models and registered external ones.

### [39:43](https://youtu.be/QbA-rs7XLEk?t=2383) Demo 3: OpenShift AI model-as-a-service

Nigon deploys from the OpenShift AI model catalog (a validated Gemma model, with per-hardware TTFT and throughput figures guiding GPU choice), then shows the pre-deployed demo: a 600M-parameter Qwen model on CPU, self-service API-key creation bound to a subscription, and dashboards for TTFT, request latency, token usage, success rate and active users. Running out of time, the speakers skip re-running the Quarkus app against this endpoint.

### [45:30](https://youtu.be/QbA-rs7XLEk?t=2730) Takeaways and Q&A

The closing framework: one gateway, an allow-list of services, a named owner, and monitoring in place. Test new model versions even with identical API shapes. In Q&A, asked how to compare costs, Vandeperre concedes it is hard to compare and they have no real sizing data: hosted is pure opex per consumption, self-hosting is upfront capex, and uncontrolled cloud bills plus confidential data already justify investing in hardware.

## Tools, libraries and specs

- Quarkus with LangChain4j (demo app; repo also uses Gradle, React, Vite, Tailwind)
- OpenAI GPT models (hosted variant)
- Podman Desktop with AI Lab (local serving, OpenAI-compatible endpoints)
- Qwen 4B (local) and Qwen 0.6B on CPU (OpenShift AI demo)
- vLLM (inference server; Red Hat AI Inference Server is the supported packaging)
- llm-d (distributed inference, smart scheduling)
- OpenShift AI / Open Data Hub (model catalog, validated models, MaaS gateway, dashboards)
- Red Hat validated models on Hugging Face (vLLM-optimized, published latency figures)
- NVIDIA GPU operator with multi-instance GPU (GPU sharing)
- NVIDIA NeMo Guardrails and TrustyAI (mentioned as platform guardrail options)
- Demo repository: https://github.com/maarten-vandeperre/owning-the-inference-layer (three independent projects `01`/`02`/`03`, one per backend)

## Who should watch

Teams deciding between hosted APIs and self-hosted inference, and Java developers curious how a Quarkus app can swap model backends without changing application code, will get a practical map of the options. Skip it if you already run vLLM or an inference gateway in production, or if you came for measured cost and latency comparisons rather than a qualitative framework.

## Verdict

**7/10**: A beginner framework on hosted versus self-hosted inference, with a local-model demo run end to end and a three-variant demo repository, limited by an OpenAI demo that was never run, a cut final demo and no cost numbers.

**Novelty 1/2**

- **+** [21:21](https://youtu.be/QbA-rs7XLEk?t=1281) The ownership and gateway guidance draws on the speakers' customer work across Western Europe, not only on product docs.
- **+** [16:43](https://youtu.be/QbA-rs7XLEk?t=1003) Personal-risk scenarios (a physician pasting records into ChatGPT, dynamic pay, salary offers shaped by debt) carry the sovereignty argument beyond a vendor lock-in checklist.
- **·** [24:30](https://youtu.be/QbA-rs7XLEk?t=1470) The Podman AI Lab and OpenShift AI model-as-a-service segments tour the products' consoles and show no results of the speakers' own.

**Demonstrated 1/2**

- **+** [13:50](https://youtu.be/QbA-rs7XLEk?t=830) The app, badged Podman AI Lab with a Qwen3 4B model, returns a €14.00 quote for two oat lattes and a cappuccino and is confirmed as an order.
- **−** [12:04](https://youtu.be/QbA-rs7XLEk?t=724) The variant announced as the OpenAI demo is the already-running Podman app; the OpenAI backend is never run.
- **−** [39:10](https://youtu.be/QbA-rs7XLEk?t=2350) The model-as-a-service app run is skipped for time; only the OpenShift AI console, API keys and dashboards appear.

**Measured 1/2**

- **+** [41:00](https://youtu.be/QbA-rs7XLEk?t=2460) The validated-model catalog compares H100 x4 and x2 configurations by TTFT P90 and tokens/s for a stated chatbot scenario (512 input, 256 output tokens).
- **−** [30:16](https://youtu.be/QbA-rs7XLEk?t=1816) Quantization is backed by an image-compression example (2.4 MB versus 73 kB), not by a model measurement.
- **−** [50:22](https://youtu.be/QbA-rs7XLEk?t=3022) The cost comparison behind the central when-to-self-host question has no numbers; the speakers say they have no sizing data.

**Depth 2/2**

- **+** [07:19](https://youtu.be/QbA-rs7XLEk?t=439) Hosted-API risks and self-hosting challenges are weighed against each other with reasons for each.
- **+** [34:27](https://youtu.be/QbA-rs7XLEk?t=2067) The serving stack gets a working mental model: Podman for local use, vLLM for concurrent production load, llm-d routing requests to the pod with the most capacity.
- **+** [38:06](https://youtu.be/QbA-rs7XLEk?t=2286) The migration path is reasoned: a gateway in front of external models first for observability, then gradual moves to owned infrastructure.

**Reusable 2/2**

- **+** [11:33](https://youtu.be/QbA-rs7XLEk?t=693) The talk points to a repository holding all three demo variants as independent runnable projects with Compose files, tests and per-variant READMEs.
- **+** [48:40](https://youtu.be/QbA-rs7XLEk?t=2920) The closing hand-off tells listeners to run the app locally with Podman Desktop and try the OpenShift AI model gateway.
