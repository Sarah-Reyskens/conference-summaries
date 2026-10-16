---
title: "AsyncAPI in action: OpenAPI for event-driven applications"
talkId: "24234"
conference: devoxx-be-2026
speakers: [Michel Schudel]
track: Architecture & Modernization
sessionType: Tools-in-Action
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=A_fp7RaG5UY
durationMin: 30
slides: null
verdict: 8
reach: segment
frames: 7
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# AsyncAPI in action: OpenAPI for event-driven applications
Michel Schudel · Tools-in-Action · Architecture & Modernization

## TL;DR
AsyncAPI brings the spec-first OpenAPI workflow to event-driven systems: one YAML spec describes channels, messages and schemas, and tooling generates documentation, models and messaging code from it. The live demo builds this end to end with an order service publishing an `OrderCreated` event to a stock service over Kafka, using the speaker's own generator template for Spring Cloud Stream.

## Key takeaways
- Model event contracts with AsyncAPI instead of Confluence pages: the spec is machine-readable, so docs and code stay aligned when the message shape changes.
- Split the spec into a shared file (channels, messages, schemas) plus one small file per service holding its send or receive operation, referencing the shared part.
- Prefer the AsyncAPI Generator with your own templates over the built-in model generator, which emits old-fashioned JavaBeans into a single directory.
- Keep broker specifics out of application code by combining generated Spring Cloud Stream publishers/consumers with protocol bindings in the spec.
- Wire generation into the Maven build with the exec plugin so docs, records and messaging glue regenerate on every build.

## Notes

### [01:02](https://youtu.be/A_fp7RaG5UY?t=62) OpenAPI recap and the running example
An order service exposes `POST /orders` taking a list of order items (product ID plus quantity) and returning a generated order ID. The OpenAPI spec for it defines schemas (order item, order request, order response) and a path referencing them, which Spring Boot turns into a Swagger page with a try-it-out button.

### [03:37](https://youtu.be/A_fp7RaG5UY?t=217) The event-driven gap
A stock service needs to learn about created orders, so the design publishes an `OrderCreated` message (generated ID, original items, a customer/warehouse source enum) to a Kafka topic. In practice teams document such messages on Confluence pages, which drift: nobody knows who consumes what when a breaking change lands. OpenAPI cannot fill the gap because it has no pub/sub or fan-out concept, no protocol bindings beyond HTTP, and its tooling assumes request-response semantics.

### [06:14](https://youtu.be/A_fp7RaG5UY?t=374) AsyncAPI spec structure
Fran Mendez created AsyncAPI in 2016 to bring the OpenAPI approach to message-driven systems in a protocol-agnostic way. A spec has five parts: JSON Schema schemas (identical to OpenAPI), messages (payload type plus example payloads for docs), channels (an abstraction of where the message lives, Kafka topic or Pub/Sub subscription alike), operations (send on the publishing side, receive on the consuming side), and optional server/bindings for executable code generation.

### [10:21](https://youtu.be/A_fp7RaG5UY?t=621) Spec distribution and tooling
Channels, messages and schemas go in a shared YAML file; each service adds its own operation file referencing it, so order service holds the send and stock service the receive. The AsyncAPI CLI takes a spec in and produces validation results plus generated output. The built-in HTML template renders documentation, and the model generator emits DTOs in about 15 languages, but the bundled Spring template is unmaintained and targets the old spec version.

### [12:56](https://youtu.be/A_fp7RaG5UY?t=776) Demo: project and spec walkthrough
The Maven project holds an order service and a stock service built on Spring Cloud Stream (no Kafka annotations in code, broker details in config) with Redpanda as the broker. The shared `order-events.yaml` defines the `OrderCreated` channel, message and schema; the per-service send/receive files add the Kafka server on localhost plus bindings. A Google Pub/Sub bindings example shows topic, subscription, region and retention settings for contrast.

### [18:06](https://youtu.be/A_fp7RaG5UY?t=1086) Validate, docs and models
`asyncapi validate` passes the spec with only a warning that 3.1.0 supersedes the used 3.0.0. Generating the HTML template produces browsable docs with messages and schemas (the example payload is missing because the shared file rather than the send file was used as input). The Java model generator quickly emits working but old-fashioned JavaBeans into one directory.

### [21:44](https://youtu.be/A_fp7RaG5UY?t=1304) Custom generator template and Maven wiring
The speaker's own `asyncapi-kafka-template` (JavaScript template files fed to the AsyncAPI Generator) emits Java records, a StreamBridge-based publisher, a consumer, Spring Cloud Stream config and docs into `target/`, parameterized by package names and source roots. The POM invokes the same commands through the maven-exec-plugin. A full build succeeds and lands generated sources and resources in both services.

### [25:52](https://youtu.be/A_fp7RaG5UY?t=1552) Running it end to end
After starting both applications, a POST with product ID and quantity returns an order ID, and the stock service log shows the received `OrderCreated` event. The hand-written order controller only injects the generated publisher and calls it; everything else came from the spec.

## Tools, libraries and specs
- AsyncAPI 3.0 (3.1.0 noted as latest) with the AsyncAPI CLI (`validate`, `generate fromTemplate`) and HTML docs template
- Speaker's `asyncapi-kafka-template` generator plus the `asyncapi-demo` project at https://github.com/MichelSchudel/asyncapi-demo
- Spring Boot with Spring Cloud Stream (StreamBridge publisher) and springdoc/Swagger for the REST side
- Redpanda (Kafka-compatible broker) over localhost; Google Cloud Pub/Sub bindings shown as an alternative

## Who should watch
Teams documenting Kafka or other event contracts by hand, and Spring developers curious about generating messaging glue from a spec, gain most. Skip it if you already ship AsyncAPI code generation in production; this is an introduction with one demo project, not production war stories.

## Verdict
**8/10**: A live run from one AsyncAPI spec to two Kafka-connected Spring Boot services, with the OpenAPI mismatch and the shared/per-service spec split explained and the demo repository published; the spec concepts and CLI flow are what the AsyncAPI documentation already gives, the build-generated docs were never shown, and the talk has no measurements.

**Reach segment**: Spring Boot teams at the conference who run Kafka or similar event-driven messaging can use the spec-first contracts and generator setup in their own services within the year.

**Novelty 1/2**

- **+** [04:38](https://youtu.be/A_fp7RaG5UY?t=278) The speaker's clients document messages on Confluence pages, where questions like "is quantity always an int?" and mailing consumers about breaking changes go unanswered by any formal contract; that practice is what the talk replaces.
- **+** [12:26](https://youtu.be/A_fp7RaG5UY?t=746) The speaker judges the bundled Spring Boot template unmaintained and unable to run the new spec version, and tells the audience to skip it.

**Demonstrated 2/2**

- **+** [26:53](https://youtu.be/A_fp7RaG5UY?t=1613) Both services start, a POST with a product ID and quantity is submitted from the Swagger page, and the stock service log shows the received `OrderCreated` event.
- **+** [23:17](https://youtu.be/A_fp7RaG5UY?t=1397) The custom template generation runs in the terminal, and the target directory gains the Spring config, the records and the generated publisher.
- **−** [28:56](https://youtu.be/A_fp7RaG5UY?t=1736) The speaker says "I forgot to show the documentation": the docs the Maven build generates are never opened, and the earlier standalone HTML docs lacked the example payload.

**Measured 1/2**

- **·** [28:26](https://youtu.be/A_fp7RaG5UY?t=1706) The talk makes no quantitative claim: the summary slide lists qualitative properties (protocol-agnostic, machine-readable, reusable) and no latency, size or time-saved figure appears anywhere.

**Depth 2/2**

- **+** [05:42](https://youtu.be/A_fp7RaG5UY?t=342) The OpenAPI comparison explains why request-response semantics, HTTP-bound tooling and the missing pub/sub and fan-out concepts call for a separate event contract model.
- **+** [10:21](https://youtu.be/A_fp7RaG5UY?t=621) The spec distribution split keeps shared channels, messages and schemas apart from per-service send and receive operations, showing how two services reference one contract in different roles.
- **+** [21:13](https://youtu.be/A_fp7RaG5UY?t=1273) The built-in model generator's old-fashioned JavaBeans and single output directory are weighed against a custom template, with manual follow-up work as the cost of the built-in route.

**Reusable 2/2**

- **+** [29:27](https://youtu.be/A_fp7RaG5UY?t=1767) The speaker points to the GitHub project where the demo lives (https://github.com/MichelSchudel/asyncapi-demo), which holds both services, the specs, the `asyncapi-kafka-template` generator, a docker-compose file for Redpanda and a README with the CLI commands and run steps.
