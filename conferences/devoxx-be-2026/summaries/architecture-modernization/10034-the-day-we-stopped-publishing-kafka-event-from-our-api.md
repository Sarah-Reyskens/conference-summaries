---
title: The day we stopped publishing Kafka event from our API...
talkId: "10034"
conference: devoxx-be-2026
speakers: [Virginie Zinck]
track: Architecture & Modernization
sessionType: Tools-in-Action
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=YEy7AgRO7As
durationMin: 30
slides: null
verdict: 5
reach: segment
frames: 6
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# The day we stopped publishing Kafka event from our API...
Virginie Zinck · Tools-in-Action · Architecture & Modernization

## TL;DR
Decathlon's gift-card Order API published Kafka events directly and hit the dual-write problem: rolled-back transactions and consumer races produced inconsistent downstream data. The team fixed it with a simplified outbox pattern where Debezium reads the operational order tables as the outbox, and the talk closes with two Debezium stability practices (heartbeats and write-rate monitoring) that prevent a stalled connector from filling the PostgreSQL WAL and crashing the database.

## Key takeaways
- Publishing to Kafka and writing to the database in the API cannot be made atomic by reordering; compensating messages, retries, and write-DB-first each fail at least one failure mode.
- The classic outbox fix works: save the order and the message in one database transaction, then let a Debezium connector relay outbox rows to Kafka.
- Using the operational tables themselves as the outbox removes the outbox table and its purge job, at the cost of coupling consumers to the table layout and making idempotency harder.
- One Debezium consumer per fulfillment action (activation, mail, wallet update) keeps the architecture easy to extend: a new action is a new consumer with no API change.
- Configure a heartbeat table on every Debezium connector so the replication slot advances even when the watched tables are idle.
- Monitor connector health with the Kafka topic `messages-in rate` metric rather than connector metrics, because connector metrics disappear when the connector stops.

## Notes

### [01:05](https://youtu.be/YEy7AgRO7As?t=65) Context: the gift-card Order API
Zinck is a staff engineer at Decathlon on the e-commerce gift-card team. The Order API validates orders, reserves gift cards, and saves them, then fulfills the rest asynchronously over Kafka: stock activation, notification mails, and wallet updates. The API was kept synchronous only for validation, reservation, and persistence to protect response times.

### [02:39](https://youtu.be/YEy7AgRO7As?t=159) The dual-write issue, two failure modes
First, rollback inconsistency: the API sends a Kafka message, then the database insert fails (unique constraint, null column), the transaction rolls back, but the Kafka message is already out. Consumers act on an order that does not exist; worst case, a mail goes out that cannot be unsent. Second, a race: with large B2B orders of several thousand gift cards, saving takes milliseconds, and the consumer can pick up the message before the order is committed. The team saw more of the timing failures than of the rollbacks.

### [04:15](https://youtu.be/YEy7AgRO7As?t=255) Three fixes that did not work
Compensating messages (send "unactivate" after a failed save) work for activation but not for mails. Kafka error-handler retries fix the timing race but not rollbacks. Writing to the database before publishing reduces errors but still fails because the Kafka send itself can fail. None of the three closes both failure modes.

### [05:50](https://youtu.be/YEy7AgRO7As?t=350) The outbox pattern and its variants
The standard fix: the API writes the order and the outbound message into an outbox table in the same database transaction, and a Debezium connector on a Kafka Connect cluster tails the database logs and publishes outbox rows to a topic. Zinck then compared three variants: reversing the flow (publish first, consumer persists; rejected because lag would hide fresh orders from the webshop), writing messages straight into the PostgreSQL WAL with `pg_logical_emit_message` (no outbox table, no purge job), and using the operational order table as the outbox. The last option decouples the API from fulfillment logic but couples consumers to the table schema and forces idempotency to be tracked per change rather than per message id.

### [12:37](https://youtu.be/YEy7AgRO7As?t=757) The chosen design: order tables as outbox
The API now only books stock and saves the order across three tables (order, order line, gift card). One Debezium connector tails their logs into three change topics, and each fulfillment consumer reads the topic matching its action: order-topic consumers send order mails, gift-card-topic consumers send recipient mails. Gains claimed: the inconsistency bug is gone, the API is simpler and faster, one-consumer-per-action is easy to extend (an SMS or invoice step is just a new consumer), and error handling moves to Kafka error handlers with per-exception retry or dead-letter routing instead of API timeouts.

### [15:47](https://youtu.be/YEy7AgRO7As?t=947) Keeping Debezium from crashing PostgreSQL
Each connector records its position in a replication slot; PostgreSQL deletes WAL segments only up to the oldest slot offset. If a connector watches a rarely updated table or stops (paused, crashed), the WAL grows until disk fills and the database crashes. Two countermeasures: configure a heartbeat (a one-row timestamp table the connector updates every 60,000 ms, included in the connector's watched tables, advice is to add it to every connector) and monitor twice, free disk space plus the heartbeat topic's `messages-in rate`, alerting when it drops below one message per minute.

### [24:04](https://youtu.be/YEy7AgRO7As?t=1444) Q&A
Asked about pushing to Kafka from the API after commit instead of Debezium, Zinck said the essential rule is that the topic write must follow the committed transaction; Debezium is the zero-code, fully decoupled way to do that via YAML configuration. She also confirmed Debezium supports many databases beyond PostgreSQL and that one connector connection against an 800-connection pool was not a concern.

## Tools, libraries and specs
- Apache Kafka (topics, consumers, error handlers, dead-letter topics)
- Debezium connector on Kafka Connect (replication slots, heartbeat table, `messages-in rate` monitoring)
- PostgreSQL (write-ahead log, `pg_logical_emit_message`)

## Who should watch
Beginners fighting database-plus-Kafka consistency bugs, and teams evaluating Debezium who have not yet configured heartbeats or connector monitoring. Skip if you already run outbox plus Debezium in production; the pattern treatment stays introductory and the Q&A audio is partial.

## Verdict
**5/10**: The outbox variants, the WAL retention model and the heartbeat practice are explained clearly for beginners; the central flow is a diagram, the speed claim is unmeasured, and apart from the failed fixes the content is what Debezium's documentation gives.

**Reach segment**: Backend teams combining relational database transactions with Kafka can use the outbox choices and Debezium operating practices in their services.

**Novelty 1/2**

- **+** [04:47](https://youtu.be/YEy7AgRO7As?t=287) The team's compensation and retry fixes failed in different ways: activation can be undone but mail cannot, and retries help the timing race but not a rolled-back order.
- **−** The outbox flow, the heartbeat settings and WAL growth from a stalled replication slot are covered by Debezium's documentation and its outbox-pattern blog posts.

**Demonstrated 0/2**

- **−** [13:07](https://youtu.be/YEy7AgRO7As?t=787) The order-table-to-Kafka flow appears as an architecture diagram without a running connector, committed order or resulting event shown.

**Measured 1/2**

- **+** [04:15](https://youtu.be/YEy7AgRO7As?t=255) Several-thousand-gift-card orders taking a few milliseconds to save give an anecdotal scale for the race condition, without a measured setup or comparison.
- **−** [14:12](https://youtu.be/YEy7AgRO7As?t=852) The claim that the migrated API is simpler and faster has no before-and-after response-time measurements.

**Depth 2/2**

- **+** [07:52](https://youtu.be/YEy7AgRO7As?t=472) The publish-first alternative is rejected against the requirement that customers see a newly placed order immediately, giving beginners a reason to choose between designs.
- **+** [10:32](https://youtu.be/YEy7AgRO7As?t=632) Using operational tables as the outbox is weighed against consumer schema coupling and the difficulty of deduplicating several changes to one order.
- **+** [18:22](https://youtu.be/YEy7AgRO7As?t=1102) The replication-slot explanation connects a stalled offset to retained WAL, disk exhaustion and the need for heartbeats and monitoring.

**Reusable 1/2**

- **+** [19:57](https://youtu.be/YEy7AgRO7As?t=1197) The slide names the heartbeat interval and action-query properties and describes the timestamp table, leaving a configuration to reconstruct.
- **+** [23:03](https://youtu.be/YEy7AgRO7As?t=1383) Monitoring the heartbeat topic's `messages-in rate` is a reusable practice because the metric stays available when the connector stops.
- **−** [27:47](https://youtu.be/YEy7AgRO7As?t=1667) YAML configuration is named as the implementation path, but no complete configuration or sample repository is published to reproduce it.


