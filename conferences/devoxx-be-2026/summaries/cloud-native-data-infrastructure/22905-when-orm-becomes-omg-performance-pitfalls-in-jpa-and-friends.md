---
title: "When ORM Becomes OMG: Performance Pitfalls in JPA and Friends"
talkId: "22905"
conference: devoxx-be-2026
speakers: [Jos Roseboom]
track: Cloud Native, Data & Infrastructure
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=ePBmAdRYl10
durationMin: 51
slides: https://easingyou.com/whenORMbecomesOMG/
slidesNote: from J-Spring 2025
verdict: 9
reach: segment
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# When ORM Becomes OMG: Performance Pitfalls in JPA and Friends
Jos Roseboom · Conference · Cloud Native, Data & Infrastructure
Slides: https://easingyou.com/whenORMbecomesOMG/

## TL;DR
Roseboom live-debugs JPA performance pitfalls in his own Spring Boot sample app, in two halves: connection-pool leases held too long, and entity fetching that fires too many queries. Every fix is re-run on screen with before/after timings, ending in a set of configuration and mapping defaults plus a public repo with all the code.

## Key takeaways
- Set `spring.jpa.open-in-view=false` on every Spring Boot app; the default keeps the database connection leased through view rendering and external calls.
- Set Hikari `auto-commit=false` (or use Spring Boot 4.1 lazy connection fetch) so Hibernate does not grab a connection at transaction start just to call `setAutoCommit(false)`.
- Mark every `@ManyToOne` and owning-side `@OneToOne` as `FetchType.LAZY`; the eager default loads related entities you never touch.
- Fetch entities only when writing; for reads use a DTO projection so one query returns exactly the fields the screen needs.
- Narrow transactions with `TransactionalTemplate` for small reads instead of wrapping external calls in a `@Transactional` service method.
- Never call `saveAll` after mutating managed entities; Hibernate dirty checking issues the updates at transaction commit.

## Notes

### [04:15](https://youtu.be/ePBmAdRYl10?t=255) Why connection pooling pays
A `ConnectionTimerTest` against Testcontainers Postgres connects 1025 times, discards the first 25, and compares: 1000 pooled connections take under a millisecond, 1000 direct `DriverManager` connections over 4 seconds, roughly 5000x. Setting Hikari's log level to debug reveals the pool config, including the default `maximumPoolSize` of 10.

### [06:51](https://youtu.be/ePBmAdRYl10?t=411) Tracing a connection lease through the shop endpoint
The shop page controller calls a `@Transactional` service that checks an external criminal-registry system, reads the last purchase date, then emails the CEO. A custom metric tracker factory on the pool logs acquire and release: the connection is held 659 ms, released only after the controller returns, while a slow external system could starve all 10 pool connections.

### [10:33](https://youtu.be/ePBmAdRYl10?t=633) Open session in view holds the lease
The late release comes from Spring Boot's default `spring.jpa.open-in-view=true`. Setting it to `false` returns the connection right after the last database access, cutting the lease from 659 ms to 251 ms in the same test.

### [13:10](https://youtu.be/ePBmAdRYl10?t=790) Hibernate acquires early to disable auto-commit
With root logging at debug, the log shows `setAutoCommit(false)` between method entry and acquisition: Hibernate takes the connection early to control commits. Setting Hikari `auto-commit=false` plus Hibernate's assume-disabled-auto-commit (automatic since Spring Boot 3.2) defers acquisition until real JDBC interaction, dropping the lease to 80 ms. Spring Boot 4.1 adds a lazy connection-fetch property that postpones `setAutoCommit`/`setReadOnly` the same way.

### [17:24](https://youtu.be/ePBmAdRYl10?t=1044) Narrowing the transaction
Fixing a planted bug (the criminal check needs the user's email, fetched from the database) reopens the lease across the external call. Wrapping just the two reads in `TransactionalTemplate.execute` instead of annotating the whole method yields two short leases totalling 26 ms.

### [22:43](https://youtu.be/ePBmAdRYl10?t=1363) JPA, Hibernate, and the FunFact entity
JPA (now Jakarta Persistence) is the mapping standard; Hibernate implements it. The `FunFact` entity follows naming conventions so no table or column names are needed, inherits its ID from a mapped superclass, and links to its admin via `@ManyToOne`.

### [26:21](https://youtu.be/ePBmAdRYl10?t=1581) Eager fetching and the first-level cache
`findAll` plus SQL debug logging shows one `select` from `fun_fact` plus three from `app_user`: `@ManyToOne` defaults to eager. Ten facts produce only three user queries because Hibernate's persistence context (first-level cache) returns each admin once; the debugger shows 13 managed entities. The cache also gives application-level repeatable read even with a read-committed data source.

### [31:08](https://youtu.be/ePBmAdRYl10?t=1868) Lazy proxies and the N+1 problem
After adding `FetchType.LAZY`, the admin slot holds a Hibernate proxy with a null target. Calling `getId` needs no query since the ID comes from the foreign key; calling a real method fires the select and fills the target. Sanitizing per admin then produces the N+1 pattern: one query plus one select per distinct admin. Touching a proxy outside its transaction is what throws `LazyInitializationException`.

### [34:17](https://youtu.be/ePBmAdRYl10?t=2057) Join fetch and dirty checking
A custom repository query with `join fetch` loads facts and admins in one statement, confirmed in the log. No `saveAll` is needed: stepping out of the `@Transactional` method in the debugger shows Hibernate issuing the updates itself through dirty checking.

### [36:22](https://youtu.be/ePBmAdRYl10?t=2182) DTO projections for reads
Building purchase DTOs from entities fires one query plus five lazy loads. A JPQL constructor projection collapses it to a single query selecting three columns:

```java
// from slide at 39:40
select new com.easingyou.funfactstore.fact.myfacts.FactDTO(
    purchase.purchaseDate, ff.fact, adm.email)
from Purchase purchase
join purchase.buyer buyer on buyer.username = :username
join purchase.funFact ff
join ff.admin adm
```

Wrong JPQL fails IDE validation or prevents the app from booting, so mistakes never reach production. Hibernate 6 supports the same shape in native queries (for things like Postgres lateral joins); interface-based projections cover pre-6 and spec-pure setups via JavaBean getter matching.

### [42:05](https://youtu.be/ePBmAdRYl10?t=2525) Mappers, mapping minimalism, and tooling
MapStruct works but adds a logic layer where bugs hide, and unmonitored mapping traverses the object tree one select at a time; one project screen fired over a thousand selects that way. The speaker's mapping order of necessity: table/class mapping always, `@ManyToOne`/`@OneToOne` only when behavior needs them (else map the FK column), bidirectional `@OneToMany` only for real domain or cascade needs, never bare `@ManyToMany` (map the join table instead). Tooling: IntelliJ's JPA support and upcoming Hibernate debugger plugin, JPA Buddy, Vlad Mihalcea's Hypersistence Optimizer (with an audience discount code in the repo), and Gatling for load testing, which pairs well with LLMs for generating load profiles.

## Tools, libraries and specs
- FunFactStore sample app (https://github.com/JosRoseboom/funfactstore): all demo code, slides link, Hypersistence discount code
- Spring Boot 3.2 / 4.1, Spring Data JPA, Hibernate 6, HikariCP, Jakarta Persistence
- Testcontainers (Postgres), Thymeleaf
- IntelliJ IDEA (JPA validation, Hibernate debugger plugin in next stable), JPA Buddy (https://jpa-buddy.com/)
- Hypersistence Optimizer (https://vladmihalcea.com/hypersistence-optimizer/), Gatling, MapStruct

## Who should watch
Spring developers shipping JPA or Hibernate code who want a checklist of configuration and mapping defaults with live proof of each fix. Skip it if eager-versus-lazy, N+1, join fetch, and DTO projections are already reflexes; the talk teaches no new Hibernate 7 or Spring 7 features.

## Verdict
**9/10**: JPA connection and fetching pitfalls re-run on screen with timed before/after steps and a published repo of the demo code; the subject is mostly the standard Hibernate performance canon.

**Reach segment**: Spring Boot and Spring Data JPA users in the conference audience can apply the configuration and mapping defaults in their own services within the next year.

**Novelty 1/2**

- **+** [06:51](https://youtu.be/ePBmAdRYl10?t=411) The diagnosis is built on the speaker's own FunFactStore shop endpoint, where a criminal-registry check, a last-purchase read and a CEO email shape each connection-lease trace.
- **+** [43:07](https://youtu.be/ePBmAdRYl10?t=2587) The MapStruct warning rests on freelance project experience, including a single screen that fired over a thousand selects.
- **−** Eager defaults, N+1, join fetch, DTO projections and open-in-view are the standard Hibernate performance canon (Vlad Mihalcea's blog and High-Performance Java Persistence, the Hibernate docs, Spring Boot's own open-in-view startup warning).

**Demonstrated 2/2**

- **+** [08:56](https://youtu.be/ePBmAdRYl10?t=536) The shop-controller integration test runs with acquire and release logging, showing the connection held 659 ms until the controller returns.
- **+** [34:48](https://youtu.be/ePBmAdRYl10?t=2088) The join-fetch query re-runs with the log showing facts and admins loaded in one statement and no further selects on access.
- **+** [39:27](https://youtu.be/ePBmAdRYl10?t=2367) The DTO projection test passes on screen showing a single three-column query replacing six.

**Measured 2/2**

- **+** [04:46](https://youtu.be/ePBmAdRYl10?t=286) The pool benchmark states its method (Testcontainers Postgres, 1025 connects discarding the first 25) with a same-database DriverManager baseline: under 1 ms pooled against over 4 s direct.
- **+** [12:08](https://youtu.be/ePBmAdRYl10?t=728) Turning only open-in-view off in the same test returns the connection right after the last database access, cutting the lease from 659 ms to 251 ms.
- **+** [15:17](https://youtu.be/ePBmAdRYl10?t=917) Setting Hikari auto-commit off in the same test defers acquisition until real JDBC interaction, cutting the lease to 80 ms.
- **·** [20:00](https://youtu.be/ePBmAdRYl10?t=1200) The closing 26 ms total spans two leases over changed code that adds a database email read, so it compares a different path from the 659 ms single lease.

**Depth 2/2**

- **+** [13:42](https://youtu.be/ePBmAdRYl10?t=822) The early acquisition is traced through debug logs to `setAutoCommit(false)`, with why Hibernate needs commit control explained.
- **+** [31:40](https://youtu.be/ePBmAdRYl10?t=1900) Proxy internals are shown live: `getId` served from the foreign key without a query, target filled on first real method call.
- **+** [40:28](https://youtu.be/ePBmAdRYl10?t=2428) JPQL constructor projections are weighed against native-query and interface-based projections, including the JPQL limit on constructs such as Postgres lateral joins.

**Reusable 2/2**

- **+** [07:54](https://youtu.be/ePBmAdRYl10?t=474) The speaker states that all the code shown is in his public GitHub repo.
- **+** [50:28](https://youtu.be/ePBmAdRYl10?t=3028) The closing QR code links the repo, which holds the demo app, the connection-timer and integration tests, the slides link and the Hypersistence discount code.
