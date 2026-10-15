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
frames: 7
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
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
**8/10**: A live spec-to-running-system demo explains the contract structure and generator choices and supplies the project, with the generated documentation example left incomplete.

**Novelty 1/2**

- **+** [21:13](https://youtu.be/A_fp7RaG5UY?t=1273) The speaker's own generator template (records, StreamBridge publisher, consumer, Spring config) and the order/stock demo project carry the second half beyond a docs walkthrough.
- **−** [12:56](https://youtu.be/A_fp7RaG5UY?t=776) The example establishes a spec-to-code workflow in a small demo project without original comparative results or production findings.

**Demonstrated 2/2**

- **+** [26:53](https://youtu.be/A_fp7RaG5UY?t=1613) Both services start, a POST with a product ID and quantity returns an order ID, and the stock service log shows the received `OrderCreated` event.
- **+** [23:17](https://youtu.be/A_fp7RaG5UY?t=1397) The custom template generation runs live in the terminal, and the target directory gains the Spring config, the records and the generated publisher.
- **−** [19:40](https://youtu.be/A_fp7RaG5UY?t=1180) The generated HTML docs open without the example payload, which the speaker guesses is a wrong input file, and the docs are not shown again after the Maven build.

**Measured 1/2**

- **·** [04:38](https://youtu.be/A_fp7RaG5UY?t=278) The talk makes no quantitative claim: the Confluence drift motive is a told anecdote, and the end-to-end run shows the event arriving with no latency, size or time-saved comparison.

**Depth 2/2**

- **+** [05:42](https://youtu.be/A_fp7RaG5UY?t=342) The comparison with OpenAPI explains why request-response semantics, HTTP-bound tooling and the lack of pub/sub or fan-out concepts require a different event contract model.
- **+** [10:21](https://youtu.be/A_fp7RaG5UY?t=621) The spec distribution separates shared message structures and channels from service-specific send and receive operations, explaining how both services reference one contract while retaining different roles.
- **+** [21:13](https://youtu.be/A_fp7RaG5UY?t=1273) The built-in model generator's JavaBeans and single-directory limits motivate a custom template with records, messaging glue and separate source and resource outputs.

**Reusable 2/2**

- **+** [28:56](https://youtu.be/A_fp7RaG5UY?t=1736) The closing slide points to https://github.com/MichelSchudel/asyncapi-demo, which contains the specs, both services, generator template and instructions for running the demo.
- **+** [24:20](https://youtu.be/A_fp7RaG5UY?t=1460) The POM wiring shown on screen regenerates docs and code on every Maven build through the exec plugin.
