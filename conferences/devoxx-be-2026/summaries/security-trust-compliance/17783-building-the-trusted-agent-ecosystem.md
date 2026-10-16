---
title: Building the Trusted Agent Ecosystem
talkId: "17783"
conference: devoxx-be-2026
speakers: [Ivan Petrov, Patrick McGrath]
track: Security, Trust & Compliance
sessionType: Tools-in-Action
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=dWF5HMkKiLg
durationMin: 35
slides: null
verdict: 8
reach: niche
frames: 7
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Building the Trusted Agent Ecosystem

Ivan Petrov, Patrick McGrath · Tools-in-Action · Security, Trust & Compliance

## TL;DR

Agents need personal data to be useful, but users have no verifiable guarantees about where that data goes once tools, model providers, and other agents are involved. Petrov and McGrath present Project Oak's answer: run tools, inference, and agents inside confidential computing environments with remote attestation and binary transparency, and they demonstrate the whole loop live, including a tampered agent being refused connection.

## Key takeaways

- Verifiable trust in agents rests on three mechanisms together: confidential computing (data in use), remote attestation (what code runs), and binary transparency (accountability for releases); any one alone leaves a gap.
- Closed-source code can still be trusted if it runs inside an audited open-source sandbox: users attest the sandbox, not the code.
- Tool descriptions in an attested MCP server become part of the attestation, so a provider that ships a prompt injection in a tool description must publish the attack in a public log first.
- Model behavior claims can be backed by signed evaluation statements: run open-source benchmarks against a closed model inside a TEE and sign the results with the hardware key.
- An agent sandbox that only permits connections to attested tools and models gives transitive trust: attesting the agent covers everything it can reach.

## Notes

### [00:34](https://youtu.be/dWF5HMkKiLg?t=34) The trust gap for agents

Petrov frames the problem: agents get more useful the more personal data they receive, yet users currently rely on asking the agent to behave. The risk compounds across the ecosystem: a third-party MCP tool can exfiltrate data or attack the agent with prompt injections hidden in tool descriptions, model providers can log prompts for training, and connected agents gossip data transitively. Project Oak, a Google research project, is their vehicle for letting users reason verifiably about server-side data processing.

### [03:43](https://youtu.be/dWF5HMkKiLg?t=223) Confidential computing and remote attestation

Encryption covers data in transit and at rest, but cloud data must be decrypted for processing, at which point the provider sees it. Trusted execution environments (TEEs) close this gap: encrypted VMs whose keys live in CPU hardware, so data decrypts only inside the CPU package. Beyond isolation comes remote attestation: the CPU measures the running binary and signs the hash with a hardware-fused key, producing a report the user can verify. Trust rests on the hardware manufacturer protecting the key, plus split trust: the cloud provider holds the data without the key, the manufacturer holds the key without the data, and collusion would be a major reputational risk for both.

### [06:21](https://youtu.be/dWF5HMkKiLg?t=381) Why attestation needs open source and transparency

A bare hash says nothing about what code does, so attestation is meaningful only when the code is open source (auditors check for backdoors) and reproducibly buildable (auditors compile it and compare hashes). Even that leaves the split-view attack: showing auditors one binary while serving users another. Binary transparency, modeled on certificate transparency, answers it: every release goes into a public append-only log, and clients require an inclusion proof before connecting. Developers stay accountable for every version they ever shipped.

### [08:24](https://youtu.be/dWF5HMkKiLg?t=504) End-to-end encryption into the enclave

All of this fails if TLS terminates at the cloud load balancer, exposing plaintext to the provider. The channel must run end-to-end from the client device into the TEE, with the session key signed by the hardware key so users can verify nobody else terminates it.

### [10:00](https://youtu.be/dWF5HMkKiLg?t=600) Trusted tools, models, and evals

Petrov maps the mechanisms onto agent building blocks. Trusted tools run inside TEEs with attestation and transparency; closed-source tools run inside an audited open-source sandbox instead, shifting the trust anchor to the sandbox. Attested MCP servers blunt tool poisoning: the tool description ships in the transparency log. Confidential GPUs extend the trust boundary to inference over an encrypted CPU-GPU channel. For closed models, Oak runs open-source benchmark suites inside the TEE and signs the scores, yielding proof that model hash X scored Y on benchmarks anyone can inspect.

### [13:34](https://youtu.be/dWF5HMkKiLg?t=814) The trusted agent and sandbox

The agent itself runs in an agent sandbox that enforces a strict connection policy: only attested tools and models. The sandbox can also hold credentials out of the agent's reach and run policy filters (prompt-injection detection, guards against destructive actions), all remotely attestable.

### [15:38](https://youtu.be/dWF5HMkKiLg?t=938) Project Oak implementation

McGrath takes over for the implementation. Everything is open source at github.com/project-oak/oak. A WebAssembly tool sandbox runs untrusted modules per request and destroys the sandbox afterward, giving full cross-request isolation; Oak Functions builds private information retrieval on this, with an encrypted in-memory database where even the operator cannot see which records were queried. The agent sandbox compiles agents written with Google's Agent Development Kit to WASM with per-session isolation. Oak Proxy, a TCP proxy below the application layer, handles attestation generation, verification, and the encrypted channel with no agent code changes, and enables attested agent-to-agent communication.

### [20:53](https://youtu.be/dWF5HMkKiLg?t=1253) Demo: signed evals and tamper detection

The first demo shows a signed statement that Gemma was evaluated against the Agent Dojo prompt-injection benchmark, with one case marked resisted:false. Automated verification confirms the Confidential Space signature and expected workload image. The speakers then forge a perfect score; verification fails because the report no longer matches the signed statement, and an agent would refuse the connection rather than leak data.

### [23:02](https://youtu.be/dWF5HMkKiLg?t=1382) Demo: trusted healthcare agent

The second demo runs a sandboxed agent over two trusted MCP servers holding synthetic clinic data, plus the evaluated Gemma model, all on Confidential Space and connected via Oak Proxy. Asked about post-training fatigue before a Devoxx talk, the agent combines walk-in clinic notes with GP baselines, spots declining hemoglobin and ferritin, recalls the 17.0 baseline from earlier in the session, and advises seeing a GP. A new session cannot exfiltrate the old one: asked what was discussed earlier, the agent reports no access to prior history. Attestation logs confirm the Confidential Space root and matching container images.

### [27:13](https://youtu.be/dWF5HMkKiLg?t=1633) Demo: the untrusted agent is refused

The speakers add exfiltration code to the agent, build a new container image with a different hash, and try to connect while the client config still expects the trusted image. The connection fails with an attestation error: the certificate chain is still rooted in Confidential Space, but no session binding exists because the image references do not line up. The client never sends data to the tampered server.

### [29:51](https://youtu.be/dWF5HMkKiLg?t=1791) Q&A

On model providers policing misuse under full encryption: providers can deploy remotely attestable output filters, so both sides attest the same pipeline. Each model version needs evaluating once, not per request, with the proof downloadable by all. TEE overhead in their tests runs roughly 3 to 5 percent. On models malicious from upload: transparency gives accountability rather than prevention, since auditors can benchmark old releases later and publish signed proof of malice. Project Oak already underpins Gemini Private AI Compute, and the sandbox model lets small teams borrow trust from audited open-source components.

## Tools, libraries and specs

- Project Oak (github.com/project-oak/oak): open-source confidential computing framework behind all demos
- Oak Proxy: TCP proxy handling attestation and end-to-end encrypted channels
- Oak Functions: private information retrieval over an encrypted in-memory database
- Google Agent Development Kit: supported agent framework, compiled to WASM for the agent sandbox
- Agent Dojo: prompt-injection resistance benchmark used in the signed-eval demo
- Gemma: evaluated model in the demo
- Google Cloud Confidential Space: TEE platform hosting every demo component
- MCP (Model Context Protocol): tool protocol; attested MCP servers in the demos

## Who should watch

Developers building agents that handle sensitive data, and security engineers evaluating confidential computing for AI workloads, will get the most from it. Viewers wanting a general introduction to AI agents or to prompt injection itself should look elsewhere; the talk assumes that context and spends its time on verification machinery.

## Verdict

**8/10**: The attested healthcare agent, the forged evaluation and the tampered-image refusal run end to end, the trust chain is explained with its limits, and the repository ships the demo scripts; the evaluation numbers have no baseline and the overhead figure is unsupported.

**Reach niche**: Teams building sensitive-data agents on confidential-computing infrastructure and security engineers evaluating TEE-based AI workloads can apply the main content.

**Novelty 1/2**

- **·** [09:28](https://youtu.be/dWF5HMkKiLg?t=568) The speakers present Project Oak's building blocks for trusted agents, a tour of the project they build whose features are covered by the Oak repository's own documentation.

**Demonstrated 2/2**

- **+** [24:36](https://youtu.be/dWF5HMkKiLg?t=1476) The healthcare agent answers using two attested MCP servers, and the following session shows both conversation recall and a fresh session without prior history.
- **+** [28:48](https://youtu.be/dWF5HMkKiLg?t=1728) Connecting to the rebuilt, tampered agent fails with an attestation error because its image does not match the trusted reference in the client configuration.
- **−** [19:19](https://youtu.be/dWF5HMkKiLg?t=1159) Attested agent-to-agent communication over Oak Proxy is described but not run; the demos connect one agent to tools and a model.

**Measured 1/2**

- **+** [21:30](https://youtu.be/dWF5HMkKiLg?t=1290) The signed evaluation displays AgentDojo v1.2.2, Gemma's model and quantization, temperature 0, seed 0 and a run window alongside attack_success_rate 0.0071 and utility_rate 0.85.
- **−** [21:24](https://youtu.be/dWF5HMkKiLg?t=1284) The evaluation result has no baseline model or comparison run to establish the effect of the proposed protections.
- **−** [32:16](https://youtu.be/dWF5HMkKiLg?t=1936) The TEE overhead estimate shifts from roughly 3% to around 5%, with no workload or measurement method supplied.

**Depth 2/2**

- **+** [06:51](https://youtu.be/dWF5HMkKiLg?t=411) The split-view attack explains why audited reproducible builds still need a public append-only release log and client inclusion proofs.
- **+** [10:30](https://youtu.be/dWF5HMkKiLg?t=630) Moving the trust anchor to an audited sandbox addresses the cost of reproducible builds and the wish to keep application code proprietary.
- **+** [32:47](https://youtu.be/dWF5HMkKiLg?t=1967) The malicious-from-upload question establishes the boundary of transparency: later auditing creates accountability but does not prevent the first malicious deployment.

**Reusable 2/2**

- **+** [29:51](https://youtu.be/dWF5HMkKiLg?t=1791) The closing points to the open-source Project Oak repository, whose `oak_trusted_agent/demo` directory has `agent`, `mcp` and `model` examples, including the get, read, run and verify scripts and tamper check for the signed-evaluation bundle.
