---
title: "AI Doesn’t Click Buttons: Building APIs for the Agentic Age"
talkId: "23519"
conference: devoxx-be-2026
speakers: [Kim Lauwers]
track: Architecture & Modernization
sessionType: Lunch Talk
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=QvyIzP4-OvM
durationMin: 38
slides: null
verdict: 5
frames: 8
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# AI Doesn’t Click Buttons: Building APIs for the Agentic Age

Kim Lauwers · Lunch Talk · Architecture & Modernization

## TL;DR

Lauwers argues the API is becoming a user interface consumed by agents that never see the screen, so workflow knowledge trapped in UIs must move into explicit contracts. Through a bpost stamp-pricing example he builds an "AI-first API": typed schemas, explainable outputs, machine-readable errors, and discoverable next actions.

## Key takeaways

- Treat the API as a product with an explicit contract; build the capability first, then let UIs, integrations, and agents consume it.
- Structure responses in three layers (data, meaning, available actions) so an agent can use the answer, understand it, and continue the workflow.
- Make errors machine-readable: a stable code, the missing inputs with reasons, and the action that unlocks next.
- Never let the model invent valid input: small stable lists inline, large or dynamic ones behind a discoverable reference-data endpoint or schema.
- Keep the business domain deterministic and gate writes behind explicit confirmation; the agent handles intent while the domain owns rules, prices, and transactions.

## Notes

### [00:37](https://youtu.be/QvyIzP4-OvM?t=37) Agents are already a major consumer of the web

Cloudflare CEO Matthew Prince posted in June 2026 that agents took the lead in HTTP requests on Cloudflare's network, 18 months earlier than expected. Lauwers adds nuance (not every bot is an AI agent), but the trend stands: architecture outlives hype cycles, so new APIs should consider non-human consumers. UI-first design leaked workflow knowledge into applications (visibility rules, allowed next actions, error texts); an agent calling the API directly loses that interpretation layer. Hence: stop building applications, start building APIs.

### [11:39](https://youtu.be/QvyIzP4-OvM?t=699) From cryptic endpoint to AI-first response

A 17 April 2026 newspaper article about the bpost chatbot, which fails to answer a simple stamp-price question and then says it is glad it could help. Putting AI in front of a system does not make it AI-ready; the capability behind the interface is what matters. Three stamp-price endpoints on slides: cryptic parameters returning a bare string; then explicit names, units, product code, amount, currency, validity date; then the AI-first version adding an explanation (applied rules such as DESTINATION_BELGIUM, WEIGHT_UP_TO_50G) and available actions (BUY_POSTAGE with href and method).

### [17:42](https://youtu.be/QvyIzP4-OvM?t=1062) Machine-readable errors, then MCP as the bridge

Errors get the same treatment: a stable code (INSUFFICIENT_SHIPMENT_INFORMATION), missing inputs with reasons, and the unlocking action (CALCULATE_PRICE). Lauwers concedes this reinvents HATEOAS; it gets interesting when the consumer is an agent that follows the links. MCP standardizes tool discovery and structured context, but explainability must come from the capability design: MCP around a bad API is still a bad API. Log the concrete interactions (tool called, inputs, outputs, outcome, correlation ID), not the model's private reasoning; grant the agent only the permissions delegated by the user. The stamp scenario then plays as an agent dialogue: the agent calls GET /postal-products/price empty-handed, the domain names the missing inputs so the model never guesses, and BUY_POSTAGE requires confirmation before the domain executes. AI decided the stamp price nowhere.

### [30:47](https://youtu.be/QvyIzP4-OvM?t=1847) Why invest before adoption is certain

One well-designed capability serves UI, integrations, copilots, and agents, cutting duplicated workflow logic and support load. An MCP server can adapt the raw API, but the semantics must be written somewhere. Lauwers closes with interface waves (1995 websites, 2008 mobile apps, 2023 AI interfaces) and a hypothesis: next, APIs as products.

## Tools, libraries and specs

- Model Context Protocol (MCP): standard connection layer for tool discovery and structured context; does not replace domain contract design.
- HATEOAS: acknowledged ancestor of the machine-readable available-actions pattern.

## Who should watch

API designers and architects wondering what "agent-ready" concretely requires of their contracts. Skip if you already ship hypermedia-driven APIs and want production agent metrics or a live demo: the worked example stays on slides in a toy domain.

## Verdict

**5/10**: A design framework (data, meaning and available actions; machine-readable errors; inline-vs-discoverable values; MCP and delegation boundaries) with reasons for each rule, held back by a toy domain shown only on slides, rules that an IETF draft already lists, and no artifact.

**Novelty 1/2**

- **+** [16:38](https://youtu.be/QvyIzP4-OvM?t=998) The stamp-price response is built up in three layers (data, meaning, available actions) and then played as an agent dialogue, which is the speaker's own worked example.
- **−** IETF Internet-Draft `draft-gaikwad-agent-friendly-http-api-profile` (June 2026) already lists next-step links, allowed-value enums, confirmation metadata on high-risk operations and the API-layer/tool-layer split.

**Demonstrated 0/2**

- **−** [26:37](https://youtu.be/QvyIzP4-OvM?t=1597) The end-to-end agent flow (missing-input error, follow-up question, confirmed purchase) is narrated over static slides with no running system or agent visible.
- **−** [16:38](https://youtu.be/QvyIzP4-OvM?t=998) The three-layer JSON responses are displayed, never executed against a real endpoint or consumed by a real agent.

**Measured 1/2**

- **+** [01:09](https://youtu.be/QvyIzP4-OvM?t=69) The Cloudflare agent-traffic milestone is cited with its source and a stated scope (bots against humans in HTML requests), with a warning against over-reading the percentage.
- **−** [30:13](https://youtu.be/QvyIzP4-OvM?t=1813) The claims that clearer errors reduce support questions and speed up exception handling come with no number or comparison.
- **·** [32:24](https://youtu.be/QvyIzP4-OvM?t=1944) The adoption timeline (iPhone 2007, Belgian bank apps 2011 and 2014) illustrates pacing and measures nothing about the proposed design.

**Depth 2/2**

- **+** [19:48](https://youtu.be/QvyIzP4-OvM?t=1188) The inline-vs-discoverable rule for valid values weighs inline lists, a reference-data endpoint and a schema type against response size and freshness, and ends in a decision rule.
- **+** [23:59](https://youtu.be/QvyIzP4-OvM?t=1439) The MCP discussion separates the connection standard from domain explainability and states what MCP cannot fix.
- **+** [26:04](https://youtu.be/QvyIzP4-OvM?t=1564) The delegation rule (AI acts inside the user's authority, never as super-user) grounds the security section in a principle with design consequences.

**Reusable 1/2**

- **+** [18:50](https://youtu.be/QvyIzP4-OvM?t=1130) The machine-readable error shape (stable code, missing inputs with reasons, unlocking action) is shown in full on a slide.
- **−** [35:02](https://youtu.be/QvyIzP4-OvM?t=2102) No repository, sample project, checklist or configuration is published; the patterns must be reconstructed from the slides.
