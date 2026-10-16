---
title: Don’t burn your fingers in the heat of the AI (r)evolution. (And get an OpenClaw).
talkId: "7032"
conference: devoxx-be-2026
speakers: [Maarten Vandeperre]
track: Agentic Engineering & Tooling
sessionType: Deep Dive
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=zDqS1U5Gnk8
verdict: 7
reach: segment
frames: 14
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Don’t burn your fingers in the heat of the AI (r)evolution. (And get an OpenClaw).

Maarten Vandeperre · Deep Dive · Agentic Engineering & Tooling
Slides: https://github.com/maarten-vandeperre/presentations/tree/main/20261006%20-%20devoxx%20belgium%20deepdive%20%5Bpresentation%5D
## TL;DR

Calling an LLM is the easy part; running AI in production takes model choice, guardrails, sandboxes, trusted delivery, fresh data, traffic control and agent observability. Vandeperre walks that full arc around a coffee-ordering app, one layer per segment, most with a working live demo. The through-line is control: keep hosting and provider options open so no single vendor owns your AI.
## Key takeaways
- Start every AI feature with a direct model call and add RAG, tools or agents only when the task needs them; each step up adds infrastructure and cost.
- Validate on both sides of the model (input scope, size and injection; output scope and size) and enforce tool denials in platform policy, not in the prompt.
- Data residency is not sovereignty: an EU region says where data sits, while access, keys, jurisdiction and the ability to leave decide who controls it.
- Coding agents get a scoped sandbox without production credentials, and their output travels through signed commits, SBOM checks and GitOps before it reaches runtime.
- Feed retrieval stores with CDC plus an outbox table so derived data stays in sync without corruption, and treat freshness as an explicit requirement per decision.
- Put a service mesh in front of model traffic for identity, mTLS and path enforcement, then reuse it for canary, blue-green and mirrored model releases.
- Metrics and logs cannot explain a 60-second agent call; trace retrieval, tool and model spans with prompt versions in MLflow.

## Notes

### [00:37](https://youtu.be/zDqS1U5Gnk8?t=37) Introduction and the reality check

Vandeperre, a Red Hat senior specialist solution architect, frames the session as a coffee shift: a PoC tasted good, and now the organization must serve the same quality at scale. The deck's reality-check slides cite an MIT NANDA preliminary study (95% of GenAI pilots with no measurable return), a Gartner forecast (30% of PoCs stopped), a Replit coding agent deleting a live database, Veracode research (45% of AI-generated samples failing security tests), an exposed DeepSeek database holding prompts and logs, and questions over US access to EU-hosted data.
### [08:32](https://youtu.be/zDqS1U5Gnk8?t=512) Vocabulary, model access and sovereignty

Training is the barista learning the recipe, inference is brewing, tokens are the order going in and out. Three serving options follow: hosted APIs (OpenAI, Anthropic), managed platforms (Azure AI Foundry, AWS Bedrock), and a self-operated stack (Ollama, Podman AI Lab, OpenShift AI). Open-weight models such as Qwen and Gemma now handle bounded jobs, quantization and runtimes like vLLM and llm-d shrink hardware needs (some models run on CPU), and agentic workloads split work into small tasks where foundation models are overkill. Reasons to investigate local serving: data control, continuity if a provider cuts access, model lifecycle control (no forced upgrades that invalidate testing), and portability. Sovereignty gets its own test: marketing sovereignty says "it runs in Europe" or "it is open", while real sovereignty shows data paths, keys, licences and a rehearsed exit with time and cost. Two hypotheticals make it personal: a physician pasting records into ChatGPT with the data reaching insurers, and personal data deciding per-worker pay. A model-as-a-service gateway in front of the models adds a catalog, access requests, quotas and usage monitoring.

### [19:29](https://youtu.be/zDqS1U5Gnk8?t=1169) AI architectures, with a Quarkus demo

Three friends illustrate the options: Retrieval knows the pubs by heart, Fine-Tuna looks them up on her phone, Agent Gaga autonomously visits bars and texts an order, which raises the responsibility question when the wrong beer arrives. Guidance per pattern: direct calls suit one-off questions over a small document; RAG suits repeated questions over approved documents, with access checks on retrieval; fine-tuning suits repeated behaviour and style, at the cost of datasets and GPU training, without live data; tool calling and MCP suit live stock and actions; agents suit multi-step goals, bounded by time, cost and tool limits. The live Quarkus LangChain4j demo (Open WebUI front end) answers "what is in an Espresso Martini" through a direct call, then through RAG over a local cocktail menu, then through an agent with stock tools where adding vodka to the file hot-reloads the answer, then through an MCP toolbox backed by a Node server where raising gin stock changes the reply. RAG documents load at startup, so editing them needs a restart. All demo code is in the speaker's quarkus-ai-styles-demo repository.

### [36:40](https://youtu.be/zDqS1U5Gnk8?t=2200) Application guardrails, with a NeMo demo

Orders need checks on both sides: validate identity, scope, size, context, injection and data policy on input, and scope plus size on output, since every processed token costs money or hardware. Chevrolet and Tesla dealer bots praising Mercedes show why output scope matters. The guardrail lasagna stacks platform controls (identity, quotas, isolation), application code (business rules), the TrustyAI operator, and NeMo Guardrails for programmable policies. In the live demo, a NeMo proxy exposing an OpenAI-compatible API accepts a valid coffee order, refuses a poem request as out of scope, blocks an oversized request, and refuses an afternoon cappuccino per an Italian colleague's rule implemented as a Colang flow plus a Python time-check action. An audience question about guarding tools gets an honest answer: tool authorization belongs partly at platform level (identity control) and partly in NeMo, and the cappuccino business rule arguably belongs in application code rather than the guardrail chain.

### [52:06](https://youtu.be/zDqS1U5Gnk8?t=3126) Sandboxed development and the OpenClaw

The apprentice gets a training counter: useful tools inside, production keys outside, a visible boundary. Options named are OpenShift Dev Spaces (Eclipse Che), Kaiden for agent workspaces, and NVIDIA OpenShell for policy-controlled execution. Red Hat's developer sandbox hosts an OpenClaw assistant on OpenShift, and the audience is invited to try crossing its boundaries and report back, since agentic sandboxing is still R&D. In the Dev Spaces demo, VS Code runs in a Kubernetes pod, the Continue plugin talks to a Qwen model served on the cluster behind a model-as-a-service gateway, generated rock-paper-scissors Python is inserted and played live, and the resulting pod carries no confidential data, no editors like vi, and Kubernetes network policies on top.

### [60:12](https://youtu.be/zDqS1U5Gnk8?t=3612) Trusted supply chain and GitOps

A checked recipe needs trusted ingredients: review the source (SonarQube, SAST), test, build with an SBOM, sign and verify. Each check answers a different question: acceptance tests ask whether it does the job, signatures ask who built it, the SBOM asks what is inside. Analysis must cover the container image too, since shells and download tools inside it widen the attack surface; curated base images such as the Red Hat Universal Base Images plus pinned digests and fast security updates close that gap. GitOps turns changes into team decisions: anyone including an AI agent can propose via pull request, subject-matter experts review instead of implementing every ticket, and Argo CD applies only the approved artifact, splitting the development boundary from runtime. Signed commits record who did what and who accepted it.

### [68:36](https://youtu.be/zDqS1U5Gnk8?t=4116) Platform engineering and Backstage

Developers once threw WAR files over the wall, then the cloud-native shift-left piled security and operations onto them, raising cognitive load (wildcard policies shipped with TODO comments as exhibit A). The fix is a platform team treating the internal developer platform as a core product with dedicated owners, plus a portal such as Backstage in front of it. The live demo scaffolds a RAG application from a software template: the developer picks a use case and data classification while the AI team maps those to curated models, sizing and credentials behind the scenes. The trusted-pipeline half of the demo broke that morning, so screenshots carry it: signature verification, SBOM extraction, CVE listing with severity counts, and pipeline gates blocking on criticals.

### [84:09](https://youtu.be/zDqS1U5Gnk8?t=5049) Fresh data with CDC, with a Debezium demo

AI needs secondary stores (vector databases, lakes) beside application databases, and distributed transactions cannot keep them in sync. The pattern: Debezium tails the database journal into Kafka topics, consumers project into derived views, offsets and acknowledgements prevent loss, and delivery stays eventually consistent. An outbox table written in the same transaction keeps the event contract small (an order ID plus the action rather than full snapshots), avoids duplicating security policy across database and Kafka, and carries the schema version so migrations do not break the flow. Consumers must handle duplicate delivery with idempotent updates, late events, deletions, and schema drift. Freshness is decided per decision: reference answers tolerate lag, stock checks read current inventory, order commitments use transactions. The live demo creates an account and a coffee order in Postgres and shows both landing in the MongoDB view, driven by a Kafka connector definition of a few dozen lines.

### [94:41](https://youtu.be/zDqS1U5Gnk8?t=5681) Service mesh and controlled releases, with live demos

Sidecars intercept all pod traffic so the mesh can apply mTLS, identity-based access and routing without code changes; sidecarless options (Cilium, Istio ambient) get a mention. A request carries user identity, app permissions, workload identity and tool authorization, and mesh policy can force the browser through the guarded backend so nobody reaches the model directly or skips NeMo. The Kiali demo runs a probe showing 403 from the frontend to the model router, adds the frontend service account to the authorization policy, and re-runs the probe to a 200. Release patterns follow: mirror (duplicate safe requests to a candidate, keep the stable answer, never grant the shadow path write credentials), canary (per-request percentages, unlike Kubernetes pod-count increments), and blue-green. The canary demo shifts the RAG service to 90/10 and observes a 93/7 split over a 10-second window. Argo Rollouts automates the rest: a Rollout object with active and preview services, pre-promotion analysis running a PromQL query that fails above five 500-errors per minute under synthetic load, and auto-promotion to production on success.

### [115:46](https://youtu.be/zDqS1U5Gnk8?t=6946) AgentOps with MLflow

A 200 OK says nothing about which retrieval, tools, models, reasoning steps and prompt versions produced an answer, so metrics, logs and traces from OpenTelemetry need an agent layer on top. The mortgage demo (one FastAPI deployment, five LangGraph persona workflows) asks for denial trends as the CEO, then drills into an MLflow trace that took 3.5 seconds: inputs, tool calls, identities, model spans and outputs per step. Prompt versions sit beside their traces so an alias can move while the recorded version stays identifiable. Evaluation closes the loop with tasting sets: deterministic checks (a dairy-free request stays dairy-free), tool-call assessment, human rubrics, and versioned comparisons, with reviewed production failures returning to the dataset. Traces are another copy of the conversation, so collection stays deliberate, access restricted, and retention bounded.

### [121:38](https://youtu.be/zDqS1U5Gnk8?t=7298) Camel abstraction and the complete picture

A Camel adapter keeps the application's contract stable while providers change: a YAML route reads the provider from the request and dispatches to OpenAI, Qwen or others, with auth and message shaping inside maintained routes instead of boilerplate Java. The live demo calls the chat provider through this router, including a GPT-4o mini path. Switching models still needs evaluation every time, since each model and version behaves differently. The closing architecture slide assembles all layers: Developer Hub and Git plus trusted pipeline feeding a sandboxed runtime under the mesh, guardrailed workflows calling stable and candidate models through the Camel adapter and gateway, Debezium and Kafka feeding the context store, MLflow tracing execution, Argo Rollouts gating releases. Final advice: clear application boundaries, a maintained platform path, evidence for each change, tested portability, and a rich toolbox with options kept open.

## Tools, libraries and specs

- Quarkus + Quarkus LangChain4j (demo app; Java 25 services in the platform repo)
- Open WebUI, Ollama, Podman Desktop AI, Continue (VS Code plugin)
- vLLM, llm-d, Qwen, Gemma (local serving stack)
- NVIDIA NeMo Guardrails, TrustyAI operator
- OpenShift Dev Spaces / Eclipse Che, Kaiden, NVIDIA OpenShell, OpenClaw
- Backstage / Red Hat Developer Hub (software templates), Argo CD, Argo Rollouts, Tekton
- SonarQube, SBOM, Sigstore-style artifact signing, Red Hat Universal Base Images
- Apache Kafka, Debezium (PostgreSQL connector, outbox router), PostgreSQL, MongoDB
- Istio / OpenShift Service Mesh, Kiali, Kuadrant (MaaS gateway)
- MLflow (tracing, prompt registry, evaluation), OpenTelemetry, Tempo, Prometheus/PromQL, Loki, Grafana
- Apache Camel (camel-ai demo, Kaoto, Hawtio), MCP protocol, LangGraph, FastAPI
- OpenShift AI 3.4, KServe, Keycloak, GitLab CE

## Who should watch

Architects and platform engineers carrying AI pilots into production, and Java teams curious how Quarkus, guardrails and GitOps fit around models, will get the most. Viewers wanting model training, fine-tuning mechanics or evaluation mathematics should look elsewhere; this session stays on the platform surrounding the model. Red Hat practitioners gain concrete product mappings, while others can translate the patterns to their own stack.

## Verdict

**7/10**: Most layers of the production-AI stack run live, two published repositories reproduce the demos and the choices are argued against alternatives; the layers follow their projects' docs, the pipeline demo runs on screenshots and the few numbers have no baseline.

**Reach segment**: teams adding LLM features to business applications, and the platform engineers who serve them, can use the guardrail, delivery and observability patterns directly.

**Novelty 1/2**

- **+** [13:45](https://youtu.be/zDqS1U5Gnk8?t=825) The speaker's sales experience (customers asking how to stop a model upgrade from forcing a full retest) drives the model lifecycle argument.
- **+** [15:22](https://youtu.be/zDqS1U5Gnk8?t=922) His RFP and RFI work shows that buyers ask vendors for sovereignty claims but never for proof of portability.
- **−** The NeMo guardrails proxy setup and the Debezium outbox pattern follow the projects' own documentation (NeMo Guardrails docs, Debezium outbox event router docs), and the reality-check statistics are the MIT NANDA, Gartner and Veracode reports.

**Demonstrated 1/2**

- **+** [44:42](https://youtu.be/zDqS1U5Gnk8?t=2682) The NeMo proxy accepts a valid coffee order live and refuses the oversized request and the afternoon cappuccino.
- **+** [100:33](https://youtu.be/zDqS1U5Gnk8?t=6033) The mesh probe flips from 403 to 200 after the frontend service account joins the authorization policy, with no application code touched.
- **−** [78:58](https://youtu.be/zDqS1U5Gnk8?t=4738) The trusted-pipeline demo runs on screenshots of another talk's application because the environment broke that morning, the automated Rollouts promotion is skipped ([110:57](https://youtu.be/zDqS1U5Gnk8?t=6657)) and the Loki log query fails on screen ([118:52](https://youtu.be/zDqS1U5Gnk8?t=7132)).

**Measured 1/2**

- **+** [106:45](https://youtu.be/zDqS1U5Gnk8?t=6405) The canary run reports an observed 93/7 split against the configured 90/10 over a stated 10-second window.
- **−** [119:55](https://youtu.be/zDqS1U5Gnk8?t=7195) The MLflow trace shows one 3.5-second request with no comparison or baseline.

**Depth 2/2**

- **+** [22:08](https://youtu.be/zDqS1U5Gnk8?t=1328) Direct call, RAG, fine-tuning, tool calling and agents are each tied to the task that justifies them and the cost they add (a one-off PDF needs no retrieval infrastructure), which gives a beginner the rule for when to choose which.
- **+** [88:52](https://youtu.be/zDqS1U5Gnk8?t=5332) The outbox pattern is argued against alternatives: one security policy instead of two on database and Kafka, smaller events, and the schema version carried in the same transaction.
- **−** [12:09](https://youtu.be/zDqS1U5Gnk8?t=729) Quantization and the vLLM and llm-d serving runtimes are named as the reason local models work, with a promise to "touch them later on in the session" that the talk never keeps.

**Reusable 2/2**

- **+** [35:38](https://youtu.be/zDqS1U5Gnk8?t=2138) The public Quarkus demo repository implements direct calls, RAG, agents and MCP as `/ai/plain`, `/ai/rag`, `/ai/agent` and `/ai/mcp` endpoints of one coffee-ordering app.
- **+** [91:28](https://youtu.be/zDqS1U5Gnk8?t=5488) The speaker says the entire platform application is in the GitHub repository, deployed with all the operators; its README installs OpenShift AI, MLflow, Kafka with Debezium, Service Mesh and Argo CD with `./deploy.sh stack` and the demo applications with `./deploy.sh app all`.
- **·** [116:48](https://youtu.be/zDqS1U5Gnk8?t=6948) The MLflow mortgage demo is a workshop asset with no repository offered, so that slice stays unrepeatable from the talk.
