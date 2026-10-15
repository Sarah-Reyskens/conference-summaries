---
title: Say Goodbye to LLM API keys with Workload Identity Federation
talkId: "16443"
conference: devoxx-be-2026
speakers: [Siarhei Biarozkin]
track: Security, Trust & Compliance
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=xEAYnXyt3L4
durationMin: 44
slides: https://github.com/sberyozkin/slides-devoxx-be-2026/blob/main/SayGoodbyeToApiKeysWithWIF.pdf
verdict: 8
frames: 8
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Say Goodbye to LLM API keys with Workload Identity Federation

Siarhei Biarozkin · Conference · Security, Trust & Compliance

Slides: https://github.com/sberyozkin/slides-devoxx-be-2026/blob/main/SayGoodbyeToApiKeysWithWIF.pdf

## TL;DR

Static LLM API keys are bearer secrets with no identity, no intent, and usually no expiry, which makes them a poor fit for agentic AI. The talk replaces them with Workload Identity Federation: workloads authenticate with short-lived OIDC tokens and exchange them for provider-issued tokens, and a live demo shows a Quarkus LangChain4j app calling Claude with no API key configured anywhere.

## Key takeaways

- Keep API keys for dev mode, test profiles, and simple single-call apps; use short-lived federated tokens for multi-agent or machine-to-machine LLM flows.
- A federated token carries issuer, subject, and audience claims, so the provider evaluates identity and intent per request instead of only checking a shared secret.
- The WIF exchange exists so the LLM provider controls token lifecycle and audience: the workload's own OIDC token authenticates to the federation endpoint, which returns a short-lived provider token.
- SPIFFE (SPIRE server plus agent, SVIDs over the Workload API) gives one identity framework across clusters and clouds; Kubernetes projected service-account tokens are the simpler choice for a single self-managed cluster.
- Application developers only read or fetch the issued token from a file path or client library; deploying SPIRE is the platform team's job.

## Notes

### [01:05](https://youtu.be/xEAYnXyt3L4?t=65) What an LLM API key is, and where it still fits

An API key is an opaque string allocated in the provider dashboard: static, usually long-lived, and kept safe by the developer or the organization. Every major provider puts the key option front and center, so it is the fastest way to start. The one architecture where keys stay warranted is the simple linear chatbot that forwards a query to one model.

### [03:11](https://youtu.be/xEAYnXyt3L4?t=191) Why keys fail zero trust

Zero trust means least-privilege access decisions evaluated per request. In agentic flows (users calling agents, agents calling tools, agents calling agents) static keys cannot represent who calls or why: they prove possession of a shared secret, not identity, context, or current trustworthiness. A key can authorize traffic long after the original intent changed, shared keys destroy auditability, and only 20% of organizations have formal key offboarding processes, per the Non-Human Identity Management Group guide. The speaker found two of his own OpenAI keys still active after two years because he had left expiry on "never".

### [09:28](https://youtu.be/xEAYnXyt3L4?t=568) Two realistic leak stories

John Doe joins a team, gets the org key for a kernel project, gets moved off, and keeps using the key because nobody revoked it. Separately, a hardcoded `openai.key=123` slips past a GitHub pre-commit check on a feature branch; anyone scanning GitHub for active keys now owns it.

### [11:38](https://youtu.be/xEAYnXyt3L4?t=698) The token-spec landscape

Transaction Tokens, the Identity Assertion Grant (under MCP enterprise authorization), and the AI Agent Authentication draft (now the WIMSE working group, with seven drafts open) all authenticate agents with tokens that identify caller, target, and permissions, exchanged at each hop of the flow. A decoded federated token names the Anthropic API, the issuing provider, and the subject workload: incomparably richer than checking whether key `123` is expired. The IETF draft's verdict: static API keys are an antipattern for agent identity.

### [16:18](https://youtu.be/xEAYnXyt3L4?t=978) Why user login is not enough

The OAuth authorization-code flow (log in with Entra ID or Google, authorize the workload to call Azure OpenAI or Gemini) introduces tokens but only fits providers that double as login providers, and user authorization says nothing about decisions an agent makes mid-flow. Machine-to-machine traffic needs workload identity instead.

### [17:56](https://youtu.be/xEAYnXyt3L4?t=1076) Workload Identity Federation, step by step

The workload gets an OIDC token from its own provider, presents it at the LLM provider's federation token endpoint, and receives a short-lived provider token bound to a service account. The indirection is deliberate: without it the LLM provider would neither control issuance and lifecycle nor appear as the token audience. Anthropic's docs (seven supported platforms, including Kubernetes, SPIFFE, and GitHub Actions) get praised as the clearest explainer; OpenAI and Gemini document their own variants.

### [22:07](https://youtu.be/xEAYnXyt3L4?t=1327) SPIFFE and SPIRE internals

A SPIFFE ID (`spiffe://example.org/ns/default/sa/frontend-service`) names the workload, SVIDs (JWT or X.509) prove it, and the Workload API delivers them. Eight build-up diagrams trace the chain: the SPIRE server attests each node, the agent attests the workload at process level, the server signs and issues the SVID, and verifiers fetch public keys from the server's OIDC endpoint. New WIT SVIDs add proof of private-key possession to align with WIMSE.

### [27:52](https://youtu.be/xEAYnXyt3L4?t=1672) SPIFFE vs Kubernetes projected tokens

SPIFFE spans clusters, clouds, and bare metal; WIF with Kubernetes just exchanges a projected service-account token, which suits a single self-managed cluster and is far easier to set up. The session's combination is WIF with SPIFFE: the SPIRE server plays the OIDC provider, and the workload exchanges its JWT SVID for the federated token. Workloads fetch SVIDs through a sidecar script that writes the token to disk, or directly over the Workload API via java-spiffe and the upcoming `quarkus-spiffe-client` (Quarkus 4.0.0.Beta1).

### [30:28](https://youtu.be/xEAYnXyt3L4?t=1828) Live demo: keyless Claude from Quarkus on OpenShift

A Quarkus LangChain4j chat service runs on OpenShift with SPIRE deployed via the Red Hat Zero Trust Workload Identity Manager operator. Its `application.properties` names a model and a token path, with no key:

```properties
# from slide at 34:07
quarkus.langchain4j.anthropic.chat-model.model-name=claude-sonnet-4-6
quarkus.langchain4j.anthropic.model-auth-provider.token-path=/var/run/secrets/tokens/spiffe-jwt-svid
quarkus.oidc-client.token-path=https://api.anthropic.com/v1/auth/token
```

A `ModelAuthProvider` exchanges the SVID with the jwt-bearer grant, using federation-rule, organization, and service-account IDs. On screen: the repo file tree, the sidecar deployment, the running SPIRE pods, the Claude console's "connect workload" custom-OIDC form, and a live question ("what is better, API keys or workload identity federation?") answered with a federation event arriving in the console in the same hour. A follow-up question exposed the sample bot as stateless: it had lost conversation memory.

### [41:21](https://youtu.be/xEAYnXyt3L4?t=2481) Q&A: will SPIFFE become the standard

Asked whether SPIFFE will win identity the way OpenTelemetry won observability, the speaker predicted SPIFFE stays the main practical protocol for years (every major provider uses it for WIF) while WIMSE politics try to keep the standards SPIFFE-neutral.

## Tools, libraries and specs

- Quarkus LangChain4j 1.15.0.CR1 WIF samples (`workload-identity-federation-spiffe`, `workload-identity-federation-kubernetes`)
- `quarkus-spiffe-client` (coming in Quarkus 4.0; try 4.0.0.Beta1), java-spiffe
- Anthropic Claude Workload Identity Federation (custom OIDC issuer, federation rules, service accounts); OpenAI and Gemini WIF variants
- SPIRE (server, agent, CSI driver, OIDC discovery provider) via Red Hat Zero Trust Workload Identity Manager operator on OpenShift
- IETF drafts: draft-klrc-aiagent-auth-03, Transaction Tokens, Identity Assertion Grant, WIMSE working group; jwt-bearer grant (RFC 7523)
- Non-Human Identity Management Group (nhimg.org) guide to NHIs

## Who should watch

Java developers taking LangChain4j or Quarkus LLM apps toward production, platform engineers evaluating SPIFFE for workload identity, and security engineers responsible for agentic AI. Skip it if you only prototype single-user chatbots with dev keys, or if you want the Kubernetes-only setup in depth: the talk points at that sample without walking through it.

## Verdict

**8/10**: a live keyless Claude call through SPIFFE tokens, an attestation walkthrough, and published Quarkus samples; Novelty is held to 1 because the exchange flow is in the Anthropic docs, and Measured to 1 because the only statistic is borrowed.

**Novelty 1/2**

- **+** [12:09](https://youtu.be/xEAYnXyt3L4?t=729) Transaction Tokens, the Identity Assertion Grant, and the aiagent-auth draft are brought together into one map of token-based agent authentication.
- **+** [33:35](https://youtu.be/xEAYnXyt3L4?t=2015) The demo and its sample project are the speaker's own Quarkus LangChain4j WIF implementation work, not a docs walkthrough.
- **−** Anthropic's workload-identity-federation docs page already explains the exchange flow the middle of the talk teaches, and the speaker recommends it at [20:00](https://youtu.be/xEAYnXyt3L4?t=1200).

**Demonstrated 2/2**

- **+** [34:07](https://youtu.be/xEAYnXyt3L4?t=2047) The properties, sidecar deployment, and token path are shown on screen with no API key anywhere.
- **+** [38:16](https://youtu.be/xEAYnXyt3L4?t=2296) The deployed chat app answers a live question through Claude over the federated token.
- **+** [40:18](https://youtu.be/xEAYnXyt3L4?t=2418) The Claude console shows the federation event arriving as the live query runs.

**Measured 1/2**

- **+** [07:52](https://youtu.be/xEAYnXyt3L4?t=472) Cites the NHI Management Group figure that only 20% of organizations have formal key offboarding, plus two of his own keys left active for two years.
- **−** [07:52](https://youtu.be/xEAYnXyt3L4?t=472) The 20% figure ships without method or sample, which the speaker flags before moving on.
- **·** [12:39](https://youtu.be/xEAYnXyt3L4?t=759) The seven open WIMSE drafts and the seven supported platforms are counts of the landscape, not measurements backing a claim.

**Depth 2/2**

- **+** [19:29](https://youtu.be/xEAYnXyt3L4?t=1169) Explains why the extra exchange step exists: the LLM provider keeps control of token lifecycle and audience.
- **+** [24:43](https://youtu.be/xEAYnXyt3L4?t=1483) Walks the SPIRE attestation chain from node attestation to SVID issuance to key verification through the server's OIDC endpoint.
- **+** [27:52](https://youtu.be/xEAYnXyt3L4?t=1672) Weighs SPIFFE (laptop, bare metal, multi-cluster) against Kubernetes projected tokens (simple, single self-managed cluster), and at [16:54](https://youtu.be/xEAYnXyt3L4?t=1014) explains why user auth-code login falls short for agent flows.

**Reusable 2/2**

- **+** [43:26](https://youtu.be/xEAYnXyt3L4?t=2606) The closing slide links the WIF-plus-SPIFFE and WIF-plus-Kubernetes Quarkus sample projects covering the demo end to end.
- **+** [34:39](https://youtu.be/xEAYnXyt3L4?t=2079) The federation properties (rule, organization and service-account IDs) and the sidecar deployment are walked through from the linked sample.
- **·** [30:28](https://youtu.be/xEAYnXyt3L4?t=1828) Reproducing the SPIRE setup needs an OpenShift cluster with the Zero Trust Workload Identity Manager operator, which the speaker says may not be available to everyone.
