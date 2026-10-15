---
title: Structured Concurrency Looms
talkId: "29351"
conference: devoxx-be-2026
speakers: [Alan Bateman, Viktor Klang]
track: Java Language & Platform
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=aow56RgptLA
durationMin: 51
slides: null
verdict: 7
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Structured Concurrency Looms
Alan Bateman, Viktor Klang · Conference · Java Language & Platform

## TL;DR
Bateman and Klang, the engineers behind Project Loom's structured concurrency API, argue that ad-hoc fan-out with executors and futures breaks error handling, cancellation, and observability, and that `StructuredTaskScope` fixes this by treating a task and its subtasks as one unit with a single join point. They walk through the API's shape (open, fork, join, close), joiner strategies, exception wrapping, and structured thread dumps, and close with its status: proposed as a permanent API in JDK 28 with a lower-level primitives API as future work.

## Key takeaways
- Put fan-out work inside a `StructuredTaskScope` so that one subtask failing cancels its siblings promptly instead of leaving you blocked in `Future.get()` on results you will throw away.
- Write subtasks to react to interruption, because cancellation in this API is built on thread interruption and an unresponsive subtask blocks `close()` indefinitely.
- Configure timeouts, names, and thread factories when the scope opens via a configuration function; the timeout clock starts at open, not at the first fork.
- Pick a joiner for the completion rule you need: `awaitAllSuccessfulOrThrow` (default), `allSuccessfulOrThrow`, `anySuccessfulOrThrow`, or the predicate-based `allUntil`.
- Attach the `catch` to the try-with-resources that owns the scope rather than nesting try blocks inside the forking or result-processing phases.
- Override the default `ExecutionException` wrapper with your own exception type when you know the subtasks' failure modes, so callers are not forced to catch something that cannot happen.
- Use the JSON thread dump (`jcmd <pid> Thread.dump_to_file -format=json`) to diagnose hangs: it preserves the parent-child structure of scopes instead of flattening threads into a list.

## Notes

### [01:04](https://youtu.be/aow56RgptLA?t=64) Sequential code is easy to reason about
The running example aggregates a `Customer` from a database and an `Order` from a web service into an `OrderSummary` record. Sequential code is readable, produces useful exceptions, shows hung threads plainly in thread dumps, and needs no extra cleanup when callees clean up after themselves. This sets the bar the concurrent version must clear.

### [03:10](https://youtu.be/aow56RgptLA?t=190) Manual fan-out with executors breaks failure handling
Submitting `fetchCustomer` and `fetchOrder` to a virtual-thread-per-task executor looks fine until something fails: a failed second task still makes you wait on the first `get()`, an exception from the first `get()` strands you in `close()` waiting for a result you will discard, and a hang leaves no visible link between the blocked caller and the stuck subtask. A `CompletionService` plus `shutdownNow()` in a catch block restores prompt failure notification but produces convoluted code and still no observability.

### [07:48](https://youtu.be/aow56RgptLA?t=468) Structured concurrency treats related tasks as one unit
The approach: when a task splits into concurrent independent subtasks, all subtasks must complete before the main task continues, and nothing (no threads, no resources) is left behind when the unit finishes, successfully or not. The term traces back through Nathaniel Smith's Python Trio writing and Martin Sústrik's libdill to 1970s architecture literature. The API's goals are fewer resource-leak and cancellation bugs plus better observability, explicitly not a definitive structured-concurrency API.

### [12:31](https://youtu.be/aow56RgptLA?t=751) The API: open a scope, fork, join once, close
A `StructuredTaskScope` is opened in try-with-resources, subtasks are launched with `fork()`, and a single `join()` waits for the whole unit (unlike one-join-per-fork APIs). Results come from `Subtask.get()` after the join; the implicit `close()` guarantees nothing is left running. Each fork starts a virtual thread by default, shown as a child of the calling thread in animated diagrams stepping through fork, block-in-join, completion ticks, and result aggregation.

```java
// from slide at 12:31
try (var scope = StructuredTaskScope.open()) {
    Subtask<Customer> customer = scope.fork(() -> fetchCustomer());
    Subtask<Order> order = scope.fork(() -> fetchOrder());
    scope.join();
    return new OrderSummary(customer.get(), order.get());
}
```

### [16:42](https://youtu.be/aow56RgptLA?t=1002) Nesting, cancellation, and cause chains
Scopes nest: `fetchCustomer` itself opens a scope forking profile, preferences, and account-status fetches, forming a task tree. When one leaf fails, its siblings are cancelled, the parent fails, and the parent's sibling is cancelled in turn; the exception surfaces as a cause-by-cause chain tracing the path to the failed leaf. Cancellation rides on thread interruption, rehabilitated for this purpose, so subtasks that mostly block on I/O must finish promptly when interrupted.

### [24:01](https://youtu.be/aow56RgptLA?t=1441) Configuration and timeouts
Scope configuration (timeout, name, thread factory) is supplied as a function at `open()` that receives and overrides the defaults, keeping future options in one place. The timeout clock starts when the scope opens and bounds forking plus execution up to `join()`; on expiry `join()` throws with a `CancelledByTimeoutException` cause. A timeout still cannot reclaim a subtask that ignores interruption, which makes the stuck task easy to locate.

### [26:07](https://youtu.be/aow56RgptLA?t=1567) Joiners define the rules of engagement
A joiner is the strategy deciding when a scope is done and what `join()` returns. The default `awaitAllSuccessfulOrThrow` requires every subtask to succeed; `allSuccessfulOrThrow` returns the result list (an "execute all"); `anySuccessfulOrThrow` returns the first success and cancels the rest (cache-or-database-or-filesystem racing); `allUntil` takes a predicate, so a never-true predicate plus a 500 ms timeout collects whatever finished in time. Klang warns against leaking business logic into custom joiners and recommends the API's Javadoc.

```java
// from slide at 31:19
try (var scope = StructuredTaskScope.open(
        Joiner.<SearchResult>allUntil(_ -> false),   // do not cancel
        cf -> cf.withTimeout(timeout))) {             // timeout starts here
    scope.fork(() -> searchDocuments(query));
    scope.fork(() -> searchJira(query));
    scope.fork(() -> searchConfluence(query));
    List<Subtask<SearchResult>> subtasks = scope.join();  // all subtasks
    List<SearchResult> results = subtasks.stream()
        .filter(s -> s.state() == Subtask.State.SUCCESS)
        .map(Subtask::get)
        .toList();
}
```

### [32:23](https://youtu.be/aow56RgptLA?t=1943) Exceptions: any throwable, wrapped by default
Because Java lacks union types for a fork's possible failures, subtasks may throw anything checked or unchecked. `join()` throws from the main thread, so every subtask exception is wrapped in `ExecutionException` by default (matching `java.util.concurrent` convention) to preserve where the main task was waiting; joiner factories accept a wrapper function to substitute your own type and avoid mandatory catches for impossible failures. Recommended practice: put the catch on the try-with-resources, and consider result types instead of exceptions for routine service outcomes.

### [38:11](https://youtu.be/aow56RgptLA?t=2291) ScopedValue propagation and structured thread dumps
`ScopedValue` (permanent in JDK 25) implicitly passes context such as a security object to callees, and opening a scope inside a `where(...).call(...)` propagates that binding to every subtask cheaply. For diagnosis, the JSON thread dump from `jcmd <pid> Thread.dump_to_file -format=json` records parent-child relationships (the main thread blocked in `join` plus its virtual-thread children), unlike the flat traditional dump; Bateman demoed rendering it as a tree with under 50 lines using the incubating JSON API.

### [44:25](https://youtu.be/aow56RgptLA?t=2665) Status: permanent API proposed for JDK 28
After several preview rounds slowed by the ecosystem digesting virtual threads, structured concurrency is proposed to go permanent in JDK 28 (JEP proposed to target). Feedback pushed back against `invokeAll`-style combinators that hide structure, and exception handling was the hardest design area. The current API covers independent tasks only; dependent tasks, channels, and workflow engines belong outside the JDK, so future work explores exposing the stable lower-level runtime primitives plus a structured-lifetime `Arena` for the Foreign Function API. No Q&A time remained; the speakers took questions outside.

## Tools, libraries and specs
- Structured Concurrency API (`StructuredTaskScope`, `Subtask`, `Joiner`) — preview, proposed permanent in JDK 28
- Project Loom virtual threads
- `ScopedValue` — permanent in JDK 25
- `jcmd <pid> Thread.dump_to_file -format=json` — structured thread dumps
- Incubating JSON API (for processing thread dumps)
- Foreign Function & Memory API (`Arena`, incl. a possible structured-lifetime arena)
- `ExecutorService`, `CompletionService`, `Future` — the manual patterns being replaced

## Who should watch
Java developers writing fan-out code over blocking I/O (service aggregation, scatter-gather queries) and anyone evaluating the structured concurrency preview before it goes permanent. Framework and library authors curious about the planned lower-level primitives get the roadmap directly. Skip if you already follow the Loom mailing list and preview Javadoc closely, or if you want benchmarks or production case studies rather than API design.

## Verdict
**7/10**: The authors explain why the API is shaped as it is (exception wrapping, interruption-based cancellation, rejected combinators), but fork/join/cancel is shown only in animations and nothing is measured.

**Novelty 2/2**

- **+** [44:57](https://youtu.be/aow56RgptLA?t=2697) The authors explain why `invokeAll`-style combinators were rejected (they hide the structure) and that exception handling was the hardest design problem across the preview rounds.
- **+** [47:32](https://youtu.be/aow56RgptLA?t=2852) The roadmap beyond the JDK API (stable lower-level primitives, structured-lifetime Arena) is laid out with its rationale: every prototype built on the same small set of runtime primitives.
- **+** [08:52](https://youtu.be/aow56RgptLA?t=532) The talk traces the idea from libdill and Python Trio back to 1970s architecture literature, situating the JDK design.

**Demonstrated 1/2**

- **+** [13:34](https://youtu.be/aow56RgptLA?t=814) Animated diagrams step through fork, blocking join, per-subtask completion ticks, and result aggregation on screen.
- **+** [43:22](https://youtu.be/aow56RgptLA?t=2602) A slide shows a real `jcmd Thread.dump_to_file -format=json` dump with the main thread blocked in `StructuredTaskScopeImpl.join` and its virtual-thread children 36 and 38.
- **−** [16:42](https://youtu.be/aow56RgptLA?t=1002) Sibling cancellation and the cause-by-cause exception chain are drawn as slide animations; no fork, join or cancellation code is run live or as a recording.

**Measured 1/2**

- **·** [24:01](https://youtu.be/aow56RgptLA?t=1441) The talk makes no quantitative claims; figures like the 10-second and 500-millisecond timeouts are configured parameters, not measurements.

**Depth 2/2**

- **+** [32:23](https://youtu.be/aow56RgptLA?t=1943) The exception-wrapping design is argued from first principles: no union types, the main-thread throw site, and the dual over/under-catch dilemma.
- **+** [18:47](https://youtu.be/aow56RgptLA?t=1127) Cancellation is set against fork-join tasks and grounded in thread interruption, with the contract that subtasks must respond or `close()` blocks.
- **−** [19:51](https://youtu.be/aow56RgptLA?t=1191) How to write a correctly interruptible subtask is asserted rather than shown; no cancelable-task code appears.

**Reusable 1/2**

- **+** [29:48](https://youtu.be/aow56RgptLA?t=1788) Complete scope snippets for each joiner strategy appear on slides in copyable form.
- **·** [27:10](https://youtu.be/aow56RgptLA?t=1630) The talk recommends the API's Javadoc as its reference material, which is documentation rather than a sample project.
- **·** [50:07](https://youtu.be/aow56RgptLA?t=3007) No repository, sample project, or checklist is pointed to; the patterns must be reconstructed from the slides.
