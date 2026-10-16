---
title: Their API Went Down. So Why Is My App on Fire?
talkId: "7035"
conference: devoxx-be-2026
speakers: [Ines Panker]
track: Development Practices
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=PGpKfdXZrpc
durationMin: 46
slides: https://speakerdeck.com/inesp/their-api-went-down-so-why-is-my-app-on-fire
verdict: 5
reach: broad
frames: 7
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15

# Their API Went Down. So Why Is My App on Fire?

Ines Panker · Conference · Development Practices

Slides: https://speakerdeck.com/inesp/their-api-went-down-so-why-is-my-app-on-fire

## TL;DR

External APIs fail in ways outside your control, so the only lever you have is containment: decide in advance how much of your app breaks when they do. Panker walks through patterns learned from integrating 40 APIs into one product, from classifying errors and handling rate limits to circuit breakers, load shedding, and observability basics.

## Key takeaways

- Classify API errors before handling them: faulty code, faulty user data, and remote-at-fault need different responses, and a blanket try/except hides all three.
- Treat expired tokens as a UX problem: tell the user the token is broken, which feature stopped working, and link to exactly where to fix it.
- Handle rate limits in background tasks that retry with the `Retry-After` wait, checkpoint paginated syncs so retries resume instead of restarting, and block all calls to that provider globally for the window.
- A slow API is more dangerous than a dead one: workers pile up waiting, throughput collapses, and the failure cascades into parts of the app that never touch the API.
- Timeouts are mandatory but weak: they bound the wait without restoring throughput, so pair them with fail-fast mechanisms like circuit breakers.
- Give background tasks expiry dates when the work loses value over time and something else covers for it; log every dropped task.

## Notes

### [00:32](https://youtu.be/PGpKfdXZrpc?t=32) Your app inherits every outage it integrates with

Panker integrated about 40 external APIs into one product, and every one needed its own auth flow, payload rules, and response parsing. API resilience means deciding what your app does while an external API is degraded: three plausible outcomes for a homepage chart fed by a flaky API are a dead homepage from poor error handling, a fully down app from piling requests, or a working app that lies by returning zero. Design systems to be cynical: expect bad things and contain them.

### [06:44](https://youtu.be/PGpKfdXZrpc?t=404) Handle errors, then sort them by who is at fault

A try/except around `fetch()` misses 400/500 responses entirely, since those are valid response objects. Moving everything inside the try catches too much (developer bugs like a wrong property name fail silently) and too little (every failure gets the same response). Errors split into faulty code, faulty user data, and remote-at-fault, with the last dividing into failures you cannot affect and failures where the remote tells you to change behavior, usually through status codes and headers that many APIs send incorrectly or not at all.

### [09:53](https://youtu.be/PGpKfdXZrpc?t=593) Expired tokens deserve their own UX

The worst user-data failure is an expired token: the integration worked yesterday and breaks today, usually when whoever set it up leaves the company. Users do nothing when this happens, so the app keeps making doomed calls indefinitely; Panker found multi-day sequences of bad-credential requests in production logs. When a token dies, tell the user three things: the token is broken, which feature stopped working, and a link to exactly where to fix it. Her team combined that nudge with a system that disables features only after collecting enough proof the integration is broken.

### [14:04](https://youtu.be/PGpKfdXZrpc?t=844) Rate limits need retries, checkpoints, and a global stop

Rate limiting arrives sneakily: a long-working script errors for a few minutes, then recovers on its own. Retrying means ending the whole call chain up to a restartable point, which is a strong argument for keeping API calls in background tasks. Propagate the `Retry-After` wait upward (parsing the header defensively, since providers invent their own variants) and retry the task after that delay. For paginated syncs, checkpoint the last processed page into the retried task, or each retry restarts from page one and accomplishes nothing. One retried task is not enough, because the limit blocks all calls to that provider, so her team cached the serialized 429 response in Redis for the window and served it from a requests-level hook, blocking every worker per provider, tenant, and token. Hammering through the limit wastes workers and risks the provider banning the integration; GitHub reserves that right.

### [24:27](https://youtu.be/PGpKfdXZrpc?t=1467) A slow API kills apps through arithmetic, not errors

HTTP defines no default timeouts, most HTTP libraries set none, and TCP recovery ranges from instant refusal to a two-minute SYN retry, a 15-minute retransmit wait, or forever on a connection that looks healthy. Set a read timeout first, then connect timeout, and keep at least one retry for transient errors. Retries still multiply the damage: a 200 ms call timing out three times at 30 s wastes 93 s. Non-blocking I/O only moves the ceiling from threads to file descriptors, memory, or database connections. The arithmetic is brutal: at 20 requests/s against workers slowed 40x, the queue grows by roughly 1,000 calls a minute. Timeouts bound the wait but a 5 s timeout against 8 s responses still runs 25x slower with zero throughput, while automatic retries add even more doomed tasks.

### [34:50](https://youtu.be/PGpKfdXZrpc?t=2090) Containment patterns: circuit breakers, load shedding, bulkheads

A circuit breaker watches for failures and fails fast instead of waiting, but with third-party APIs the hard part is defining what counts as a failure, so accept it stays forever half-built. Load shedding means dropping work deliberately: her team expired nightly syncs after 6 hours, daily reports after 23 hours, and 2-minute metric polls after 4 hours, accepting holes in charts to stay operational. Bulkheads partition workers so one provider cannot starve the rest: separate queues per work type, per provider, or per customer, plus quota caps so a backfill job cannot consume the API budget the interactive path needs.

### [42:03](https://youtu.be/PGpKfdXZrpc?t=2523) Observability is a conscious decision

Every log line and metric exists because someone chose to add it. Two upgrades carry the most weight: attach a request or job ID to every log message, and write log and exception messages that tell the debugger what to check next, including the raw JSON payload. Add custom metrics for the incidents you anticipate, and build small dashboards such as a circuit-breaker state view showing failure counts and which API is blocked and why.

## Tools, libraries and specs

- Python requests (HTTP client her team hooked to serve cached 429 responses)
- Redis (cache for serialized rate-limit responses)
- Retry-After header (carries the rate-limit wait, as seconds or a date)
- TCP keepalive (disabled by default; default wait around two hours)

## Who should watch

Backend developers who integrate third-party APIs and own the resulting incidents will get the most from this. Readers of Release It! or engineers already running circuit breakers with dashboards can skip the containment survey, though the token UX and cached-429 sections may still be new.

## Verdict

**5/10**: Production experience and explanations of API-failure containment carry the talk, but no mechanism is run on screen, the quantitative examples are hypothetical and the takeaways remain fragments.

**Reach broad**: Backend developers building the business applications that dominate this conference can use the API-failure containment, timeout and isolation practices across frameworks and providers.

**Novelty 2/2**

- **+** [13:02](https://youtu.be/PGpKfdXZrpc?t=782) Multi-day bad-credential sequences in production logs led the team to combine customer nudges with evidence-gated feature disabling, while accepting that some doomed requests remained during evidence collection.
- **+** [19:46](https://youtu.be/PGpKfdXZrpc?t=1186) The speaker reports choosing to change retried-task parameters against queue conventions rather than persist checkpoints separately because this worked for their system, with a maintenance cost attached.

**Demonstrated 0/2**

- **−** [22:23](https://youtu.be/PGpKfdXZrpc?t=1343) The cached-429 hook is said to show results immediately, but no run, recording or output demonstrates the mechanism working.
- **−** [44:40](https://youtu.be/PGpKfdXZrpc?t=2680) The circuit-breaker dashboard is a static screenshot of blocker state rather than a run producing output.

**Measured 0/2**

- **−** [32:13](https://youtu.be/PGpKfdXZrpc?t=1933) The throughput example explicitly uses hypothetical inputs that do not describe a realistic system, so its arithmetic supplies no observed performance measurement.
- **−** [32:46](https://youtu.be/PGpKfdXZrpc?t=1966) The claimed fortyfold throughput loss and subsequent queue growth are calculated from those assumptions without a measured system comparison.

**Depth 2/2**

- **+** [26:01](https://youtu.be/PGpKfdXZrpc?t=1561) The TCP failure-state ladder explains why connection refusal, lost handshake packets and a disappearing peer produce different waits when application timeouts are absent.
- **+** [30:40](https://youtu.be/PGpKfdXZrpc?t=1840) The resource-exhaustion explanation connects blocked workers or exhausted descriptors and shared resources to unrelated work stalling and health-check failures spreading load to other instances.
- **+** [41:32](https://youtu.be/PGpKfdXZrpc?t=2492) The backfill-quota discussion weighs the resilience gained by isolating interactive API capacity against the implementation and ongoing maintenance cost.

**Reusable 1/2**

- **+** [44:08](https://youtu.be/PGpKfdXZrpc?t=2648) A slide carries a copyable diagnostic logging fragment with schema-mismatch hypotheses and the raw payload.
- **−** [45:14](https://youtu.be/PGpKfdXZrpc?t=2714) The closing QR code offers references, with no published sample project, complete configuration or checklist reproducing the main content.
