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
verdict: 6
frames: 6
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

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

**6/10**: Production-tested rate-limit and slow-API mechanisms explained in depth, but no pattern is run on screen, the numbers are illustrative and no artifact is published.

**Novelty 2/2**

- **+** [21:21](https://youtu.be/PGpKfdXZrpc?t=1281) Caching the serialized 429 response in Redis and serving it from a requests-level hook to block all workers per provider, tenant, and token is a production technique with its gotchas, not generic advice.
- **+** [12:00](https://youtu.be/PGpKfdXZrpc?t=720) The three-part expired-token UX (broken token, affected feature, exact fix link) comes from multi-day bad-credential sequences found in production logs.
- **+** [18:43](https://youtu.be/PGpKfdXZrpc?t=1123) Checkpointing paginated syncs by retrying the task with the last processed page, against queue conventions, is presented as her own working implementation.

**Demonstrated 0/2**

- **−** [22:23](https://youtu.be/PGpKfdXZrpc?t=1343) The cached-429 hook and the page checkpoint "show results immediately" and "worked beautifully", but no run, recording or output is shown; the slides are code and diagrams.

**Measured 1/2**

- **+** [32:46](https://youtu.be/PGpKfdXZrpc?t=1966) The throughput arithmetic (20 workers at 200 ms versus 8000 ms, 100 down to 2.5 calls per second, queue growth of about 1,000 calls per minute) works a baseline against a degraded case with its method stated.
- **−** [32:13](https://youtu.be/PGpKfdXZrpc?t=1933) Those numbers are explicitly hypothetical, the load-shedding expiries are configured values, and no production metrics or before/after measurements back any claim.

**Depth 2/2**

- **+** [26:01](https://youtu.be/PGpKfdXZrpc?t=1561) The TCP timeout ladder (instant refusal, two-minute SYN retry, 15-minute retransmit, waiting forever) explains why libraries without timeouts hang.
- **+** [33:48](https://youtu.be/PGpKfdXZrpc?t=2028) The 5-second-timeout-against-8-second-responses case shows why timeouts bound waiting without restoring throughput.
- **+** [41:32](https://youtu.be/PGpKfdXZrpc?t=2492) The backfill-quota discussion weighs a trade-off: partitioning API budget between sync jobs and interactive calls costs maintenance against the resilience gained.

**Reusable 1/2**

- **+** [44:08](https://youtu.be/PGpKfdXZrpc?t=2648) A slide carries a copyable diagnostic `logger.error` message template with schema-mismatch hypotheses and the raw payload.
- **−** [45:14](https://youtu.be/PGpKfdXZrpc?t=2714) No repository, sample project or checklist covers the patterns; the closing QR code leads to a list of references.
