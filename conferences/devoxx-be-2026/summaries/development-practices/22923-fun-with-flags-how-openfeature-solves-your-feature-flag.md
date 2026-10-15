---
title: "Fun with Flags: How OpenFeature Solves Your Feature Flag Headaches"
talkId: "22923"
conference: devoxx-be-2026
speakers: [Simon Schrottner]
track: Development Practices
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=Ij5RsREpjBg
durationMin: 51
slides: https://schrottner.at/openFeatureTalk/
verdict: 6
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Fun with Flags: How OpenFeature Solves Your Feature Flag Headaches
Simon Schrottner · Conference · Development Practices
Slides: https://schrottner.at/openFeatureTalk/

## TL;DR
Feature flags look like glorified conditionals until targeting, multi-language support, vendor lock-in and stale-flag cleanup bury you. OpenFeature answers with a vendor-neutral evaluation API plus swappable providers, layered evaluation context and hooks, so teams keep one flagging standard across every SDK and vendor. The talk is a beginner-friendly tour of that toolbox, grounded in the speaker's Dynatrace production experience.

## Key takeaways
- Define flags as runtime behavior changes: anything needing a redeploy or restart (environment variables included) is configuration, not flagging.
- Always pass a fallback value at evaluation time so an unreachable provider, a missing key or a type mismatch degrades to a known value instead of throwing.
- Put operational attributes (region, runtime, device, tenant) into the evaluation context, not just user identity, so incidents can be contained by switching a flag off for the affected slice.
- Use a targeting key to keep percentage rollouts deterministic; without one, a user can flip cohorts on every page refresh.
- Treat stale flags as measurable tech debt: emit evaluation data through hooks and OpenTelemetry, then delete flags whose evaluations prove them dead.
- Generate typed flag accessors from a manifest (the OpenFeature CLI direction) once string keys and hand-written fallbacks start causing typos and type mismatches.

## Notes

### [00:33](https://youtu.be/Ij5RsREpjBg?t=33) A cautionary tale: Knight Capital
Knight Capital Group lost about half a billion US dollars in one hour in 2012 after repurposing a feature flag and deploying new software to only seven of eight servers, so one node traded against the rest. The lesson the talk draws: the danger is not the flag itself but undisciplined reuse plus uneven rollout.

### [01:34](https://youtu.be/Ij5RsREpjBg?t=94) Speaker and agenda
Schrottner is an OpenFeature maintainer and technical steering committee member, a CNCF ambassador, and contracted by Flagsmith, which funds his open-source work. The talk has three parts: normalize what feature flags are, explain the OpenFeature core concepts, then map three common pitfalls (vendor lock-in, dynamic evaluation, obsolete flags) to OpenFeature solutions.

### [03:07](https://youtu.be/Ij5RsREpjBg?t=187) What flags are for
A flag enables, disables or changes service behavior at runtime. Uses covered: coordinated launches behind one central switch instead of timed deployments; A/B experimentation (the running example nudges a Swedish user's recommendations toward Austrian folk music over a year); targeting releases such as dogfooding and premium tiers; replacing long-lived feature branches with small merges; and reducing risk by decoupling deployment from release, with kill switches and progressive 1%-5%-10% rollouts.

### [06:14](https://youtu.be/Ij5RsREpjBg?t=374) Flag categories and the maturity model
Pete Hodgson's taxonomy on Martin Fowler's blog gives four kinds: release toggles (short-lived, gates a release), ops toggles (e.g. disabling a flaky or expensive payment provider), permission toggles (long-lived, dynamic: beta or premium users, countries), and experiment toggles (short-lived, highly dynamic: button color or placement). The maturity model runs from environment variables (not really flagging: every change restarts the service), to dynamic configuration (central on/off), to dynamic evaluation (context-aware per-user or per-country rules), to operationalized flags (audit trails, evaluation insights, lifecycle ownership). OpenFeature targets that last stage as a toolbox, not a prescribed process.

### [08:56](https://youtu.be/Ij5RsREpjBg?t=536) OpenFeature: status, history, motivation
OpenFeature is a CNCF incubating project on the path to graduation, pending long-lead items like security audits. It started by gathering vendors and library authors at KubeCon Valencia in May 2022 to write the spec together before any implementation; it entered the CNCF sandbox in late 2022 and reached incubating in 2023. Dynatrace pushed the effort because observability needs a standard: with several flagging solutions in-house, nobody could tell how a flag evaluation contributed to an incident, and vendor lock-in made migration painful.

### [12:02](https://youtu.be/Ij5RsREpjBg?t=722) The evaluation API
Application code talks only to the evaluation API; a provider abstraction connects it to the flag management system. The API is a singleton so flags are reachable anywhere without wiring, and the call shape is identical across SDKs (Java, Node.js, Go, PHP, .NET, Ruby, Rust shown on the slide):

```java
// reconstructed from speech
var api = OpenFeatureAPI.getInstance();
api.setProvider(new FlagsmithProvider(...));
var client = api.getClient();
boolean on = client.getBooleanValue("v2_enabled", false);
```

Flags are not just booleans: strings (region codes, algorithm names), numbers (with cross-language pitfalls such as Python treating integer 1 as true) and objects (e.g. threshold bounds) are supported. The fallback value (second parameter) is mandatory by design: OpenFeature catches provider outages, missing keys, type mismatches and rule errors and returns the fallback so evaluation never breaks the caller.

### [15:10](https://youtu.be/Ij5RsREpjBg?t=910) The iceberg: homegrown solutions rot
Citing Hodgson's "feature flagging is an iceberg" piece, the talk argues every team starts with a quick boolean, then needs more languages, a UI, targeting and audit trails until it has accidentally built a flagging platform needing its own team. Vendors remove that burden but each ships a bespoke SDK, so switching vendors rewrites every call site.

### [16:44](https://youtu.be/Ij5RsREpjBg?t=1004) Pitfall 1, vendor lock-in: providers
The provider is a thin wrapper between the OpenFeature SDK and any flag backend. Switching from the in-memory provider to flagd (the cloud-native open-source reference implementation) or to a vendor such as Flagsmith, LaunchDarkly, Unleash or Datadog is a one-line change at initialization; the ecosystem counts over 130 providers. A multi-provider runs several providers in order, which supports migrations and split setups (one source for experiments, one for kill switches). Application code never changes.

### [18:19](https://youtu.be/Ij5RsREpjBg?t=1099) Pitfall 2, dynamic evaluation: context and targeting
Motivating cases: sticky canary cohorts, per-country compliance gating without code changes, QA testing in production where alerts fire on the real system. Targeting rules differ per provider; flagd uses JSON-logic style configuration:

```json
// from slide at 20:30
{
  "flags": {
    "v2_enabled": {
      "state": "ENABLED",
      "variants": { "on": true, "off": false },
      "defaultVariant": "off",
      "targeting": {
        "if": [
          { "ends_with": [{ "var": "email" }, "@domain.com"] },
          "on",
          "off"
        ]
      }
    }
  }
}
```

The evaluation context feeds these rules: arbitrary attributes passed as the third evaluation argument, including operational facts such as hyperscaler, Java runtime, Android version or region. Context can be set at four levels (global instance, transaction/request via a Spring interceptor, per labeled client, per invocation) and merges with invocation winning over global. Percentage rollouts need a targeting key (device id, session id, or anything stable the team defines) so bucketing stays deterministic across refreshes; without it, users bounce between variants.

### [25:06](https://youtu.be/Ij5RsREpjBg?t=1506) Pitfall 3, obsolete flags: hooks and OpenTelemetry
Dynatrace's old system held over 2,000 flags, most unevaluated in years, with the oldest being a "temporary" flag; teams even repurposed dead flags whose names happened to match. Nobody can say when removal is safe, but OpenFeature can supply the data. Hooks attach arbitrary code to the evaluation lifecycle (before, after, error, finally) at invocation, client or instance scope. The OpenTelemetry hook, built with the OpenTelemetry community around a feature-flag semantic convention, records which flag evaluated to which value on which service, with provider, error and reason, plus metrics. The same extension point covers logging (kept out of the hot path deliberately: at Dynatrace ingest scale those milliseconds mattered), alerting on specific resolved values, and enriching context from third-party systems in before-hooks.

### [30:51](https://youtu.be/Ij5RsREpjBg?t=1851) Recap plus two skipped concepts
Recap maps problems to concepts: lock-in to providers, dynamic evaluation to evaluation context, obsolete flags to hooks with OpenTelemetry. Two concepts get only a sketch. The track API records experiment outcome events (e.g. checkout conversion) keyed by targeting key so experiments can be evaluated where the data point lands. Provider events (connect, disconnect, configuration change) can drive listeners; one team used a change listener as an audited remote cache-clear mechanism.

### [34:00](https://youtu.be/Ij5RsREpjBg?t=2040) Adoption, resources and the brittle-API problem
Public adopters named: Google (OpenFeature-compliant solution in public preview), Spotify (Confidence experimentation platform), Dynatrace, Otto, eBay, Ford, Datadog, Booking, Miro and Flagsmith; the core JS SDK sees about 6.2 million npm downloads per week. Entry points: openfeature.dev (spec, docs, provider catalogue), flagd.dev (reference implementation, sidecar or local, no UI), Flagsmith (open-source UI), and the Fun-With-Flags demo repo. The honest caveat closes the talk: string keys, hand-written fallbacks and untyped getters are brittle (typos, wrong type, wrong default), so the project is building manifest-driven code generation through the OpenFeature CLI, currently an npm tool generating typed accessors from a checked-in flag manifest.

## Tools, libraries and specs
- OpenFeature (CNCF incubating): vendor-neutral flagging API, SDKs (Java, JavaScript, Go, Python, .NET, PHP, Ruby, Rust), spec at openfeature.dev
- flagd (flagd.dev): cloud-native open-source reference provider, YAML/JSON flags, OFREP-compatible
- Flagsmith: open-source self-hosted flag management with UI and OpenFeature support
- OpenTelemetry feature-flag semantic convention + OpenFeature hooks: evaluation observability (spans, metrics)
- OpenFeature CLI: flag-manifest driven typed accessor code generation (in progress, npm tool)
- Fun-With-Flags demo: github.com/aepfli/Fun-With-Flags-Demo, multi-language examples using flagd, hooks, OpenTelemetry
- OFREP (OpenFeature Remote Evaluation Protocol): standardized remote evaluation request/response shape
- Pete Hodgson's "Feature Toggles" taxonomy (martinfowler.com) and "feature flagging is an iceberg" (openfeature.dev/blog)

## Who should watch
Beginners adopting feature flags or evaluating OpenFeature, and teams juggling several flagging SDKs or vendors who want one standard. Practitioners wanting Dynatrace-scale numbers or a live demo should watch the speaker's earlier OpenFeature Summit talk with Todd Baert instead; this session sketches the demo and defers its metrics there.

## Verdict
**6/10**: A beginner-friendly OpenFeature tour with real production rationale and a full demo repo, limited by nothing running on screen and numbers without method.

**Novelty 1/2**

- **+** [25:38](https://youtu.be/Ij5RsREpjBg?t=1538) Dynatrace's retired system held over 2,000 flags, most unevaluated in years, with a "temporary" flag as the oldest.
- **+** [29:16](https://youtu.be/Ij5RsREpjBg?t=1756) Logging stays out of the evaluation hot path because milliseconds mattered at Dynatrace ingest scale; a logging hook adds it on request.
- **−** The core concepts (evaluation API, providers, context, hooks) match the published material on openfeature.dev/docs and the spec, and the flag taxonomy comes from Pete Hodgson's feature-toggle article on martinfowler.com.

**Demonstrated 0/2**

- **−** [36:37](https://youtu.be/Ij5RsREpjBg?t=2197) The Fun-With-Flags demo is presented only as a repo link because setting it up live takes too long.
- **−** [17:15](https://youtu.be/Ij5RsREpjBg?t=1035) Provider swapping is shown as a code change on a slide, and no evaluation ever runs on screen to back it.

**Measured 1/2**

- **+** [01:04](https://youtu.be/Ij5RsREpjBg?t=64) Knight Capital lost about half a billion dollars in one hour when a repurposed flag met a 7-of-8-server deploy.
- **+** [35:34](https://youtu.be/Ij5RsREpjBg?t=2134) The core JS SDK sees about 6.2 million npm downloads per week.
- **−** [25:38](https://youtu.be/Ij5RsREpjBg?t=1538) The counts it leans on (2,000 unevaluated flags, over 130 providers, 6.2 million weekly downloads) arrive without a baseline or method.

**Depth 2/2**

- **+** [14:08](https://youtu.be/Ij5RsREpjBg?t=848) The fallback value is mandatory because the SDK catches unreachable providers, missing keys, type mismatches and rule errors and returns it, so evaluation never breaks the caller.
- **+** [24:04](https://youtu.be/Ij5RsREpjBg?t=1444) Percentage rollouts take a user-defined targeting key so bucketing stays deterministic and a page refresh does not flip the user's variant.
- **+** [30:18](https://youtu.be/Ij5RsREpjBg?t=1818) Hooks are weighed against forking a provider: arbitrary code attaches at defined lifecycle points, so extra behavior needs no fork.

**Reusable 2/2**

- **+** [36:37](https://youtu.be/Ij5RsREpjBg?t=2197) The Fun-With-Flags demo repo (github.com/aepfli/Fun-With-Flags-Demo) is, in the speaker's words, the whole presentation as a demo code flow.
- **+** [36:05](https://youtu.be/Ij5RsREpjBg?t=2165) flagd.dev gives a free reference backend to run as a sidecar or locally, and openfeature.dev hosts the spec plus provider catalogue.

