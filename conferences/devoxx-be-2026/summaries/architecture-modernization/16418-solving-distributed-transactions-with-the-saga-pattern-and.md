---
title: Solving Distributed Transactions with the Saga Pattern and Temporal
talkId: "16418"
conference: devoxx-be-2026
speakers: [Andrei Sulyz]
track: Architecture & Modernization
sessionType: Tools-in-Action
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=c45C2wNSZFc
durationMin: 29
slides: null
verdict: 8
reach: niche
frames: 11
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Solving Distributed Transactions with the Saga Pattern and Temporal
Andrei Sulyz · Tools-in-Action · Architecture & Modernization

## TL;DR
The talk debugs the official Temporal saga sample against a synchronous money-hold operation from the speaker's fintech, finding four cancellation defects and fixing each live on stage. It leaves you with a working recipe: register compensation before each step, compensate in a detached cancellation scope, wait for in-flight activities to finish, and rethrow cancellation explicitly.

## Key takeaways
- Register saga compensation before the protected call, not after: a lost response after the remote system persisted means an unregistered hold never gets released.
- Run compensation in a detached cancellation scope, or a cancelled workflow cannot execute the compensation activities at all.
- With the default TRY_CANCEL type, cancelling a workflow races the in-flight activity, so a fast unhold can land before the slow hold it should reverse.
- WAIT_CANCELLATION_COMPLETED plus an explicit `CancellationScope.throwCanceled()` after the steps makes the workflow wait for in-flight work and still reach its compensation.
- Cancelling a Temporal workflow stops the orchestration; it says nothing about whether the external HTTP operation stopped, so fintech systems still need a periodic reconciliation service.

## Notes

### [00:35](https://youtu.be/c45C2wNSZFc?t=35) Context: synchronous holds at Skyro
The speaker leads the processing team at Skyro, a fintech whose credit platform orchestrates business services through one Temporal-based operations service. The focus is the hold operation, which freezes money across customer balances and services and needs confirmation from all of them. It is synchronous: a customer waits at a payment terminal, so timeouts must cancel the operation and release the money.

### [03:16](https://youtu.be/c45C2wNSZFc?t=196) Temporal primer
Workflows are business processes, activities are their steps, and a worker executes both while all communication runs over the network via gRPC. The network can fail between the remote system persisting a change and the response arriving, which motivates the whole talk.

### [04:21](https://youtu.be/c45C2wNSZFc?t=261) The saga sample under test
Starting from the official Temporal Java SDK saga example (written 2020, refactored 2024), the speaker rebuilds it in his domain: hold money in a credit system and a debit system via plain HTTP activities, with unhold compensations, executed both sequentially and in parallel.

### [07:27](https://youtu.be/c45C2wNSZFc?t=447) Defect 1: compensation registered too late
The sample adds each compensation after its activity returns. If the remote system saved the hold but the response was lost, the workflow throws with no compensation registered and the hold leaks. Fix: add the compensation first and make unhold tolerate reversing an operation that never landed.

### [08:30](https://youtu.be/c45C2wNSZFc?t=510) Defect 2: cancellation breaks compensation
Cancelling the workflow surfaces a Temporal UI error, but only with parallel compensation: that path wraps activity failures into a CompensationException that Temporal does not expect from a cancelled workflow. Sequential mode silently rethrows CancelledFailure, the valid "move to cancelled" signal, so the workflow cancels with no compensation at all.

### [11:10](https://youtu.be/c45C2wNSZFc?t=670) Fix: detached cancellation scopes
Cancellation propagates through a tree of scopes rooted at an implicit main scope. Creating a detached scope with `Workflow.newDetachedCancellationScope(() -> saga.compensate()).run()` disconnects compensation from that propagation, matching the current official sample.

### [13:45](https://youtu.be/c45C2wNSZFc?t=825) Defect 3: compensation overtakes the in-flight hold
Cancelling while a hold with 8s mock latency is in flight runs compensation immediately: the unhold arrives at a server that never saw the hold. Switching activities to WAIT_CANCELLATION_COMPLETED makes the workflow wait for the in-flight step instead of throwing CancelledFailure at once.

### [18:31](https://youtu.be/c45C2wNSZFc?t=1111) Defect 4: waited cancellation never throws
WAIT_CANCELLATION_COMPLETED throws no exception by itself, and plain HTTP activities never heartbeat, so cancelling during the second hold ends the workflow with no compensation. The fix is an explicit `CancellationScope.throwCanceled()` after the steps when the scope saw a cancellation request. Alternatives named: activity heartbeats or signals instead of the cancellation mechanism.

### [22:43](https://youtu.be/c45C2wNSZFc?t=1363) Residual race and reconciliation
Cancelling exactly as the workflow finishes can still slip through, so the team runs a reconciliation service a few times a day as the last guardian of consistency. Real stability comes from reliable workflows, not from the reconciler.

### [23:46](https://youtu.be/c45C2wNSZFc?t=1426) Driving the workflow from a synchronous caller
The business service starts the workflow with a static workflow ID, so a client retry joins the running execution instead of starting a duplicate. It blocks on `getResult` with a timeout, sends cancel on timeout, and surfaces domain errors to clients through ApplicationFailure details.

### [27:40](https://youtu.be/c45C2wNSZFc?t=1660) Takeaways and demo
Three closing points: cancellation does not mean the external operation stopped, compensation must be designed with cancellation and activity semantics in mind, and Temporal does not remove distributed-systems problems. The final slide links a demo repository with the naive saga plus local-activity, parallel, and synchronous variants.

## Tools, libraries and specs
- Temporal Java SDK 1.38.0 (version visible in the demo's Temporal UI)

## Who should watch
Temporal users implementing sagas or cancellable workflows gain the most, especially anyone wiring synchronous APIs to workflow executions. Viewers wanting general saga theory or a comparison of orchestration engines should look elsewhere.

## Verdict

**8/10**: four cancellation defects of the Temporal saga sample debugged and fixed on a live Temporal UI with the mechanics explained and a demo repository linked; the talk measures nothing and part of the material is in the official sample and docs.

**Reach niche**: only teams already running Temporal can apply the cancellation-scope and cancel-type fixes that fill most of the slot.

**Novelty 1/2**

- **+** [04:52](https://youtu.be/c45C2wNSZFc?t=292) The speaker rebuilds the official sample in his own domain, holding money in a credit and a debit system over plain HTTP activities, which gives the known material a fintech setting.
- **+** [23:15](https://youtu.be/c45C2wNSZFc?t=1395) Skyro keeps a reconciliation service running a few times a day as the last guard of consistency in a fintech system, a production choice a getting-started search does not give.
- **−** The ordering fix and the detached cancellation scope are already in the official temporalio/samples-java bookingsaga sample, and cancellation scopes are covered on the Temporal Java SDK cancellation docs page.

**Demonstrated 2/2**

- **+** [17:24](https://youtu.be/c45C2wNSZFc?t=1044) After switching to WAIT_CANCELLATION_COMPLETED, the rerun in the Temporal UI waits out the 8s in-flight hold before the compensation executes.
- **+** [20:35](https://youtu.be/c45C2wNSZFc?t=1235) The rerun with the explicit throwCanceled fix compensates where the second-hold cancellation at [18:31](https://youtu.be/c45C2wNSZFc?t=1111) had left none.
- **−** [08:30](https://youtu.be/c45C2wNSZFc?t=510) The error from cancelling with parallel compensation appears only as a still screenshot from the Temporal UI and is never rerun.

**Measured 1/2**

- **·** The talk makes no quantitative claim: the 8s latency is a configured mock parameter, and the reconciler schedule is stated without any effect claim.

**Depth 2/2**

- **+** [11:41](https://youtu.be/c45C2wNSZFc?t=701) Cancellation scopes are explained as a tree that propagates to all children, which is why a detached scope keeps compensation alive.
- **+** [14:48](https://youtu.be/c45C2wNSZFc?t=888) TRY_CANCEL and WAIT_CANCELLATION_COMPLETED are compared with their reasons: the first throws at once and signals activities that, being plain HTTP calls without heartbeats, never see it.
- **−** [20:04](https://youtu.be/c45C2wNSZFc?t=1204) Heartbeats and signals get one sentence ("better than nothing"), and the cost of a workflow waiting on a slow activity is not weighed.

**Reusable 2/2**

- **+** [27:53](https://youtu.be/c45C2wNSZFc?t=1673) The closing "Try the Demo!" QR points to github.com/AndreiSulyz/temporal-synchronous-saga-devoxx-example, whose README documents the naive saga and the local-activity, parallel and synchronous variants with configuration and run steps.
