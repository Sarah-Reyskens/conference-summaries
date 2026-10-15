---
title: "AI in the Dark: Running LLMs in Air-Gapped Production Environments"
talkId: "9017"
conference: devoxx-be-2026
speakers: [Mihaela Gheorghe-Roman]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=kaT6UpLrzhU
durationMin: 51
slides: null
verdict: 7
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# AI in the Dark: Running LLMs in Air-Gapped Production Environments
Mihaela Gheorghe-Roman · Conference · Agentic Engineering & Tooling

## TL;DR
Wiring an agent from a cloud API is easy; trusting one in production with no internet, no cloud APIs and no external services is a different problem. The speaker shows how her team runs a Spring AI agent with local models behind an air gap for defence resource management: reads run freely, every state-changing write waits on a human approval, and tool descriptions are engineered as prompts. Two recorded on-screen demos show the pattern working: grounded tool-calling answers "not found" where the ungrounded run invents a unit, and the approval gateway shows approve-then-execute plus a rejection (the timeout-default case is described, not run).

## Key takeaways
- Split every agent capability into read operations (free, fully logged) and write operations (blocked on explicit human approval); when in doubt, classify as write.
- Behind an air gap, a model upgrade means a formal re-accreditation cycle, so architect for frozen model versions and make switching models a configuration change, never a rewrite.
- The tool `description` field is the prompt the model reads when choosing a tool; on a local model with no frontier knowledge to fall back on, a vague description produces confidently wrong answers.
- A good tool description states what it returns, when to use it, the ID format, and a negative instruction naming the similar tool to use instead.
- Default an unanswered approval to rejected, and log the agent's reasoning (score breakdowns, confidence levels) so a 2 a.m. incident can be reconstructed the next day.

## Notes

### [01:04](https://youtu.be/kaT6UpLrzhU?t=64) Trusting an agent in production is the hard part
Anyone can wire an API key and have something that looks like a functional agent within hours, but demos rarely survive real users, real data, or bad input. Building the same agent with no internet and no cloud API is not a harder version of that problem but a completely different one: not a request out, not a token out. A hand-count of the room sets up the talk: nearly everyone has tried Spring AI, fewer have wired MCP tool-calling, and only two people have shipped an agent that runs unattended against real data.

### [08:24](https://youtu.be/kaT6UpLrzhU?t=504) The scenario: battalion resource management
The talk builds on one simplified defence scenario: a battalion headquarters with six units (ALPHA-7, BRAVO-3 and others) spread across three sectors A, B and C, plus one active priority-one reconnaissance mission, T-42. The agent recommends how units get allocated across the map. Every recommendation is a claim a real person may act on immediately with no undo: pulling a unit out of a mission that blows up a bridge has consequences no return policy covers. Grounding, oversight and audit trails are not best practices here; without them the team does not ship.

### [10:32](https://youtu.be/kaT6UpLrzhU?t=632) What "no internet" actually removes
Losing cloud inference is the obvious part. Less obvious: losing the ability to pull a newer model the day it ships, because upgrades require a formal re-accreditation cycle with legal review and documentation; losing external registries and every form of calling home (telemetry, updates, threat feeds). Every dependency must already sit inside the boundary before day one, because nothing arrives later. The field name for this is DIL: disconnected, denied, intermittent, low-bandwidth. A cloud-versus-air-gap comparison makes the trade concrete: elastic scale, newest models and vendor-owned uptime on one side; fixed hardware, frozen model versions and every 3 a.m. failure being your own on the other.

### [17:20](https://youtu.be/kaT6UpLrzhU?t=1040) Read versus write: the agent's permissions
The most important architectural decision, taken before a line of code: reads (querying unit and equipment status, detecting scheduling conflicts) run with no gateway and full logging, while nothing on the write side executes unilaterally. The agent may propose reallocating a unit and even prepare the API call, then it stops and waits. The rules: anything changing a state a human must know about is a write, and anything ambiguous is a write too.

### [22:38](https://youtu.be/kaT6UpLrzhU?t=1358) Underneath: local models, the advisor chain, MCP
Running a local model, whether a third-party one like Mistral or fine-tuned in-house, is standard practice in this setting; every model passes the same accreditation regardless of source. Requests flow through a Spring AI advisor chain in a fixed order, logging, approval, audit, which wraps the whole call so the audit write happens on the way back out after everything resolves. Below it sits the chat model plus tool schemas; the only thing ever touching the real system is an annotated tool method, some discovered over MCP from servers owned by other teams (units, logistics, intelligence, ammunition), all local processes on the same box. Every model, cloud or local, hides behind the same chat-client interface, so swapping models is a configuration change.

### [31:30](https://youtu.be/kaT6UpLrzhU?t=1890) The loop and why descriptions matter
Each turn runs thought (what do I need), check (do I have it), then either act (call a tool, observe, loop back) or answer. Every tool is an internal REST call or a query against the operational data store, the same data a human operator reaches through a UI, now exposed through MCP instead. The model picks tools by reading exactly one field: the description. With several similarly named tools nearby, a frontier cloud model can compensate from world knowledge; a local model with nothing to fall back on guesses wrong silently.

### [35:07](https://youtu.be/kaT6UpLrzhU?t=2107) Anatomy of a good tool description
The `getUnitStatus` example carries four sentences, each earning its place: what it returns (status, grid reference, readiness, commander), when to use it, the ID format (ALPHA-7, BETA-3, DELTA-6), and a negative instruction ("Do NOT use for mission info, use getMissionDetails instead") that cut the wrong-tool error rate sharply. The method itself is a plain lookup with a not-found branch; all the intelligence sits in the docstring.

```java
// from slide at 36:00
@Tool(description = """
    Returns operational status, grid reference, readiness level,
    and commander for a specific unit. Use when asked about unit
    availability, position, or readiness. Unit IDs follow the
    format ALPHA-7, BETA-3, DELTA-6.
    Do NOT use for mission info - use getMissionDetails instead.
    """)
public String getUnitStatus(String unitId) {
    return unitService.getById(unitId)
        .map(u -> "Unit: %s | Status: %s | Readiness: %s ...")
        .orElse("Unit " + unitId + " not found. Cannot provide status.");
}
```

### [37:46](https://youtu.be/kaT6UpLrzhU?t=2266) Demo 1: hallucination versus grounded answer
The same question, "What is the status of PHANTOM-9?", is asked twice via a pre-recorded run (local models are slow). With tool-calling off, the agent invents a convincing reconnaissance unit at grid A421 with 92% readiness; PHANTOM-9 does not exist. With tool-calling on, it calls the tool and answers "Unit PHANTOM-9 not found in system." A third call shows a real unit in the same format, proving the fabrication was indistinguishable by shape. Running on your own hardware does not make a model more truthful, and a bigger model would not fix a missing tool description.

### [42:00](https://youtu.be/kaT6UpLrzhU?t=2520) Demo 2: the approval gateway
The agent tries to move ALPHA-7 to mission M-01 and does nothing until the operator approves; after approval it executes and reports the new assignment. When the agent then tries to reassign the unit again to M-03, the operator rejects it because the unit must finish its current mission, and the response reads "Operation denied by operator. No changes were made." The third case is timeout: if nobody approves or rejects within the configured window, the operation counts as rejected.

### [46:45](https://youtu.be/kaT6UpLrzhU?t=2805) Limits and the ship checklist
The constraints generalize beyond defence to finance and healthcare data that legally cannot leave a boundary. The closing checklist has four groups: model (benchmarked on your tool-calling workload, accredited then frozen, hardware sized for worst-case concurrent load), supply chain (every dependency inside before day one, pinned weights and libraries, internal mirror built early), safety (read/write boundary in code, versioned and CI-tested system prompts, approval timeout defaulting to rejected), and observability (self-hosted tracing, append-only audit tables, an on-call runbook). One prototype logs a score breakdown behind each proposal so the operator sees why the agent reached 90% versus 50% confidence before approving.

## Tools, libraries and specs
- Spring AI (ChatClient, ChatModel, advisors: logging, approval, audit)
- MCP (Model Context Protocol) over JSON-RPC; Spring AI generates tool schemas from Java method signatures
- Llama 3.2 (local demo placeholder; production models undisclosed)
- Mistral (named as a third-party local-model option)

## Who should watch
Engineers shipping AI agents into regulated or disconnected environments (defence, finance, healthcare, on-prem) who need the production patterns: permission boundaries, approval flows, auditability. Spring AI users get concrete tool-design and advisor-chain guidance. Skip if you want model-serving internals (quantization, GPU sizing, inference servers), which stay at architecture level, or if your agents only ever call cloud APIs.

## Verdict
**7/10**: Defence-environment constraints and two recorded demos that show grounding and a human approval gate working, limited by generic core design, an effect claim with no number, and no published artifact.

**Novelty 1/2**

- **+** [10:32](https://youtu.be/kaT6UpLrzhU?t=632) The speaker names what no internet removes from her own setting: model upgrades behind a formal re-accreditation cycle, registries, telemetry and threat feeds, with DIL as the field term.
- **+** [23:10](https://youtu.be/kaT6UpLrzhU?t=1390) A production constraint behind the local-model mandate: Anthropic's terms of service bar use with defence technology.
- **·** [19:58](https://youtu.be/kaT6UpLrzhU?t=1198) The read/write split, human approval and append-only audit ([26:19](https://youtu.be/kaT6UpLrzhU?t=1579)) are established practice applied to the air-gap setting, and the demo model is a placeholder for the undisclosed production one.

**Demonstrated 2/2**

- **+** [39:54](https://youtu.be/kaT6UpLrzhU?t=2394) The hallucination demo shows both outputs on screen: a fabricated 92%-readiness unit profile versus "Unit PHANTOM-9 not found in system."
- **+** [44:04](https://youtu.be/kaT6UpLrzhU?t=2644) The approval demo shows approve-then-execute followed by a visible "Operation denied by operator. No changes were made."
- **−** [45:09](https://youtu.be/kaT6UpLrzhU?t=2709) The timeout-means-rejected case is described, not run, and the audit trail and MCP delegation are drawn on slides without a run.

**Measured 1/2**

- **+** [38:48](https://youtu.be/kaT6UpLrzhU?t=2328) The same PHANTOM-9 question asked with tool calling off and on gives a visible before/after: invented unit details versus a correct not-found, from one pair of runs.
- **−** [36:11](https://youtu.be/kaT6UpLrzhU?t=2171) The negative instruction is said to have reduced the wrong-tool error rate "with a very high percentage", with no number, baseline or method.
- **·** [48:51](https://youtu.be/kaT6UpLrzhU?t=2931) The 90% and 50% confidence levels are illustrative outputs of a prototype, not a measurement.

**Depth 2/2**

- **+** [24:44](https://youtu.be/kaT6UpLrzhU?t=1484) The advisor chain order (logging, approval, audit) is explained with its reason: the audit write happens on the way back out.
- **+** [35:07](https://youtu.be/kaT6UpLrzhU?t=2107) Each of the four description sentences is justified, including why the negative instruction stops wrong-tool selection and why a local model has no world knowledge to compensate.
- **+** [12:39](https://youtu.be/kaT6UpLrzhU?t=759) The cloud-versus-air-gap trade-off weighs elastic scale and newest models against fixed hardware and self-owned failures.

**Reusable 1/2**

- **+** [36:00](https://youtu.be/kaT6UpLrzhU?t=2160) The full `@Tool` method with its four-sentence description is on screen and can be reconstructed directly.
- **−** [37:46](https://youtu.be/kaT6UpLrzhU?t=2266) The demos run from a local prototype with no repository or published artifact covering the main content.
