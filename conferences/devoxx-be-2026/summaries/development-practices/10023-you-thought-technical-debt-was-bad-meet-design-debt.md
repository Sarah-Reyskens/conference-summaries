---
title: You thought technical debt was bad? Meet design debt!
talkId: "10023"
conference: devoxx-be-2026
speakers: [Julien Topçu, Josian Chevalier]
track: Development Practices
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=SoWgxHeAPGU
durationMin: 50
slides: https://slides.com/julientopcu/you-thought-technical-debt-was-bad-meet-design-debt
slidesNote: from Devoxx Poland 2026
verdict: 8
reach: broad
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# You thought technical debt was bad? Meet design debt!
Julien Topçu, Josian Chevalier · Conference · Development Practices
Slides: https://slides.com/julientopcu/you-thought-technical-debt-was-bad-meet-design-debt

## TL;DR
Technical debt is only the visible part of a deeper problem: accidental design debt, the coupling and complexity introduced by stretching a domain model past its conceptual integrity. The speakers build a catalog of "model tensions" that signal this debt inside one model, across services, and inside team processes and organization, illustrated end to end with a cruise-booking example.

## Key takeaways
- Challenge the existing model with every new feature instead of reusing it by default; a model is valid for a limited time, and apparent extensibility is often chance.
- Set aside KISS, DRY, YAGNI and refactoring when shaping a model: they push you to keep reusing the current model instead of replacing it with the right one.
- Read "bugs in untouched code, rippling changes, slowing delivery" as model entropy, the interest on unpaid design debt, and locate it through named model tensions.
- Split merged concerns into dedicated models (search, selection, booking) rather than splitting services around a fragmented model, which produces a distributed monolith.
- Treat synchronized releases, feature-flag sprawl, palliative roles and ownership debates as process and organizational tensions that compensate for a design problem instead of fixing it.
- Never act on a single heuristic: several must correlate into a body of evidence before a tension counts as real design debt.

## Notes

### [00:33](https://youtu.be/SoWgxHeAPGU?t=33) A Lord of the Rings skit frames the big ball of mud
The talk opens with a parody prologue: an architect forges one master model to rule every value stream, and the teams bind themselves to a big ball of mud. The skit then follows a developer fixing a search bug (ships departing in the past still listed) who keeps breaking unrelated features: booking history, flexible data, and more. Each fix touches half the service and most of its tests.

### [04:13](https://youtu.be/SoWgxHeAPGU?t=253) Iterative modeling can turn into model sinking
The defender describes his process as iterative modeling: each business need drives exploration with domain experts, which enriches the model, which becomes code. The challenger answers that he only stacked changes onto the old model until it collapsed under its own weight. No model is inherently extensible; whether it absorbs a new feature depends on how the new problem relates to the solved one, and event storming should find the right model rather than confirm the existing one.

### [07:49](https://youtu.be/SoWgxHeAPGU?t=469) Design debt, accidental design debt, model entropy
Citing Ward Cunningham, the speakers define technical debt as the deliberate choice to ship code that does not fully fit, in order to move faster. Design debt is the same choice at model level; accidental design debt is misguided model decisions that introduce coupling, undermine cohesion, and erode reliability. Unpaid debt accrues entropy: the model loses coherence and every change costs more and can break anything. Three symptoms diagnose it: regressions in untouched parts, rippling changes, and slowing delivery.

### [11:27](https://youtu.be/SoWgxHeAPGU?t=687) The spork effect: one model solving several problems
Solving search and booking with one model, glued by a `booked` boolean added "just like" the earlier `selected` boolean, is the talk's central example of intrinsic coupling: several implicit models merged into one. The speakers call this the spork effect, after the utensil that fails as both spoon and fork. A spork model is fragile, so developers stop touching it; it turns rigid, new code stacks on top, and entropy and cognitive load grow. Microservices do not fix this: they are a deployment strategy, not a design strategy.

### [14:08](https://youtu.be/SoWgxHeAPGU?t=848) Model tensions and crystallization
Each `booked` and `selected` boolean is a model tension, a design smell showing the model stretched past its conceptual integrity (each concept staying true to what it represents). Left unresolved, a tension crystallizes into a structuring constraint: the unresolved selection tension already constrains how booking gets built, and fixing it now means a costly redesign.

### [17:49](https://youtu.be/SoWgxHeAPGU?t=1069) The debt starts in analysis: event storming hides the selection
The debt creeps in during analysis. In the team's event storming, "compute the total price of the selected fares" and "check the completion of the selected fares" look natural, but two biases hide the real concept. Silence bias keeps attention on the prominent selected fares; the cognitive binding effect misses that selected fares plus paid ancillaries together mean a selection. Reframed, the workflows yield a priced, complete or incomplete selection. Deriving the selection's lifecycle from other concepts' states is another tension, the implicit lifecycle. The remedy is a first-class selection model: dedicated endpoint, class, and table.

### [22:30](https://youtu.be/SoWgxHeAPGU?t=1350) Code walkthrough: tensions in the search implementation
Walking through the commit that added the `selected` boolean, the speakers show high friction for low complexity: trivial selection rules require streaming every ship and every fare to find selected ones, compute the total, or select a fare. A forced `selected=true` on a second fare of the same bound exposes state infiltration, since the fare cannot stay consistent without knowing the other fares. The select method's unselect-then-select dance is a loss of atomicity, and a "should never happen" exception on multiple selected outbounds proves the structure allows invalid states. Counting selected bounds inside search is a diffusion of responsibility, and the correlated `selectionComplete` and `totalPrice` fields are a disseminated representation.

### [28:44](https://youtu.be/SoWgxHeAPGU?t=1724) Extracting dedicated models fixes the original bug
Pulling every selection field and behavior out of search yields a Selection class organized around a map, reducing the earlier code to about 20 lines: put the fare by bound, stream the map for the total, count it for completion. The same extraction applies to booking (payment mean, finalization status), which lets search refocus on criteria and makes the past-ships bug trivial: past departures show only when the booking is finalized, a status that first had to emerge from the new model.

### [30:49](https://youtu.be/SoWgxHeAPGU?t=1849) Extrinsic coupling: cruising versus post-booking
A second storyline moves up a level. Management created a post-booking team and service for exchange and cancellation because the cruising service had become too slow to change; the two services now break each other in production. The speakers diagnose a distributed monolith: exchange and cancellation are states of the booking lifecycle spread over two services, so duplicated checks are a business logic leak, the back-and-forth lifecycle is a fragmented lifecycle, and the booking's state scattered across services is a distributed state. Contrasted against this, an e-commerce cart, order and parcel each own a lifecycle, so that split is not a fragmented lifecycle.

### [38:33](https://youtu.be/SoWgxHeAPGU?t=2313) From synchronized releases to palliative roles
The travel-insurance incident shows the business impact: insurance sold in cruising was unknown to post-booking cancellations, paying customers went unrefunded, and the fix needed a rollback plus a synchronized redeploy. Feature flags only bandage the coupling: with some 50 flags, management created a full-time "readiness to go engineer" to synchronize them. Unresolved design problems compensated by multi-versioning, double runs and flags are band-aid processes; full-time roles tending them are palliative roles. Both are compensatory countermeasures that can block the real fix, since the role vanishes once the coupling is solved.

### [43:14](https://youtu.be/SoWgxHeAPGU?t=2594) Organizational tensions close the vicious circle
Arguments over whether a seat change is a booking update or an exchange creation show unclear ownership; the post-booking backlog hijacked by cruising's needs is a backlog takeover. The circle runs: model fragmentation forces synchronized evolutions, which breed compensation systems, which fragment the organization, which fragments the model further. Management splitting the teams was itself a manager-as-shadow-designer move, an unconscious architecture decision through an org decision, and therefore Conway's law in action. The speakers stress a generative culture with no blame: the organization charges interest on design debt left unhandled.

### [47:22](https://youtu.be/SoWgxHeAPGU?t=2842) Detect with heuristics, fix with mitosis and reverse Conway
Heuristics are warning signs for detecting tensions, but one is never enough: a body of evidence must correlate before acting. To dismantle a spaghetti model, the speakers point to Model Mitosis, their technique for progressively extracting dedicated models in code, and to the reverse Conway maneuver from Topcu's earlier Conway's law talk for the crystallized org level. The closing slide's QR code links the full heuristics catalog on GitLab.

## Tools, libraries and specs
- Model Tension Heuristics catalog (gitlab.com/beyondxscratch/model-tension-heuristics), linked from the closing slide's QR code
- Model Mitosis, the speakers' technique for progressively splitting a spaghetti model into dedicated models
- Event storming (Alberto Brandolini) as the analysis workshop where linguistic tensions creep in
- Ward Cunningham's definition of technical debt as the deliberate choice to ship an incomplete understanding faster
- Reverse Conway maneuver, from Topcu's earlier Conway's law talk, for the organization-level fix

## Who should watch
Developers and architects maintaining domain models or microservices that keep breaking each other gain a diagnostic vocabulary they can apply immediately. Teams debating a service split around a shared lifecycle also benefit. Viewers wanting DDD mechanics or live code beyond one walkthrough should look for a hands-on session instead.

## Verdict
**8/10**: a cross-layer framework for diagnosing design debt, worked through cruise-booking code and service boundaries, with a published heuristics checklist; execution and outcome measurement are outside this modeling talk's purpose.

**Reach broad**: developers, tech leads and architects building business applications can apply the diagnostic vocabulary to domain models, service boundaries and delivery processes.

**Novelty 2/2**

- **+** [48:24](https://youtu.be/SoWgxHeAPGU?t=2904) The speakers bring model, service, process and organizational tensions into one diagnostic framework, using their cruise example to show how correlated heuristics build a body of evidence for design debt across those layers.

**Demonstrated 1/2**

- **·** [29:16](https://youtu.be/SoWgxHeAPGU?t=1756) The before and after code of the cruise-booking example is shown on slides and nothing runs, which fits a modeling talk with no runnable subject.

**Measured 1/2**

- **·** [03:42](https://youtu.be/SoWgxHeAPGU?t=222) The regression figures belong to the staged example, and the talk makes no quantitative claim requiring an outcome measurement.

**Depth 2/2**

- **+** [45:17](https://youtu.be/SoWgxHeAPGU?t=2717) The closing causal chain runs from model fragmentation through synchronized evolutions and compensation systems to organizational fragmentation and back to the model, with Conway's law named as the mechanism.

**Reusable 2/2**

- **+** [49:28](https://youtu.be/SoWgxHeAPGU?t=2968) The closing QR code links the public Model Tension Heuristics catalog on GitLab, which lists the heuristics the talk covers with further examples.
