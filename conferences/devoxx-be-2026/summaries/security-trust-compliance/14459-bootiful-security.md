---
title: Bootiful Security
talkId: "14459"
conference: devoxx-be-2026
speakers: [Daniel Garnier-Moiroux, Josh Long]
track: Security, Trust & Compliance
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=W-OKVLMtPAw
durationMin: 51
slides: null
verdict: 8
reach: segment
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Bootiful Security
Daniel Garnier-Moiroux, Josh Long · Conference · Security, Trust & Compliance

## TL;DR
Two Spring team members live-code a secure system from scratch: passwords done right, then one-time tokens, passkeys, and multi-factor authentication, then a centralized OAuth2 setup with client, resource server, and gateway, ending with an OAuth2-secured MCP server used from Claude Code. The arc moves from "do passwords correctly" to "stop using passwords" to "centralize identity and reuse it everywhere, including AI agents".

## Key takeaways
- Hash stored passwords with a slow, memory-hard function such as Argon2id, and keep a `DelegatingPasswordEncoder` so old hashes get transparently upgraded to stronger algorithms at login time.
- Prefer phishing-resistant passkeys (WebAuthn) over one-time codes sent over email or SMS, since a code is still a password the user can be tricked into sharing.
- Apply Spring Security's MFA building blocks per endpoint rather than globally, so only sensitive pages demand extra factors or a fresh login.
- Centralize login in an OAuth2 authorization server and hand out short-lived, scoped ID and access tokens instead of spreading passwords across every service.
- Put single-page apps behind a backend-for-frontend gateway that holds the tokens, so the browser never handles OAuth2 credentials or CORS workarounds.
- Secure MCP servers with OAuth2 the same way as any resource server, so an agent like Claude Code logs in as the user before it can call tools.

## Notes

### [02:33](https://youtu.be/W-OKVLMtPAw?t=153) Scaffolding a secure Boot app
Long generates the app on start.spring.io with Web, JDBC, PostgreSQL, Spring Security, plus one-time-token login, passkeys, and the OAuth2 client, server, and resource-server starters. A fresh endpoint is secure by default: navigating to it prompts for login, and a successful login injects a plain `java.security.Principal` rather than a framework type. For the demo they wire a `JdbcUserDetailsManager` against seeded users in Postgres instead of the usual in-memory `UserDetailsService`.

### [05:39](https://youtu.be/W-OKVLMtPAw?t=339) Passwords done right, then abandoned
Garnier-Moiroux walks through why SHA-256 is wrong for passwords (fast, so attackers can try billions of guesses per second) while bcrypt is deliberately slow at roughly 100 ms per check on their machine, and OWASP-recommended Argon2id adds memory-hardness that hurts GPU farms. Spring Security ships Argon2 support but needs Bouncy Castle or password4j on the classpath. The `DelegatingPasswordEncoder` prefixes each hash with its algorithm id so the system can migrate algorithms or raise work factors by re-hashing on the next login, the only moment the cleartext is available. Having shown the best possible password handling, they call passwords a liability and move on.

### [13:26](https://youtu.be/W-OKVLMtPAw?t=806) One-time tokens
Authentication factors come in three kinds: knowledge (passwords), possession (key cards), and inherence (a face). The first possession-based step is one-time tokens, implemented as an `HttpSecurity` customizer so Spring Boot's secure defaults stay intact. The only required customization is where a generated token goes; the demo prints it to the console instead of running a mail server. They flag the weakness immediately: emailed codes are phishable, and anyone who triggers a code for someone else's account can try to talk them out of it.

### [17:31](https://youtu.be/W-OKVLMtPAw?t=1051) Passkeys with WebAuthn
Passkeys replace the shared secret with a challenge-response signature: the OS keychain holds the private key, the server keeps the public key, and login signs a server challenge. The FIDO Alliance backers named include Apple, Google, Microsoft, Amazon, Meta, PayPal, and Samsung, and support is native on macOS, Windows, Linux browsers, phones, hardware keys, and password managers. Long registers a passkey from the live app and logs back in with a fingerprint; biometrics never leave the device, they only unlock the local key. The frame at 19:03 shows the session's link sheet with the code repository and the free Spring Security book.

### [22:11](https://youtu.be/W-OKVLMtPAw?t=1331) Multi-factor authentication
A single annotation enables global MFA, recording each satisfied factor (password, one-time token) as a granted authority. Since whole-app MFA is usually too blunt, they switch to per-endpoint rules through the `access()` configurer and an MFA authorization-manager factory: `/admin` requires the admin role plus both factors, everything else just needs authentication. The live escalation shows the failure modes: Long as a non-admin passes both factors and still gets 403 on `/admin`, while Rob the admin is challenged for the missing factor and then gets in.

### [27:19](https://youtu.be/W-OKVLMtPAw?t=1639) Centralizing login with Spring Authorization Server
Twenty internal apps should not each store users, so they convert the app into a central SSO platform with Spring Authorization Server (now part of Spring Security, in the same category as Keycloak or Entra ID). Configuration registers the known clients, here a `spring` client with its redirect URI, grant types, and requested scopes; the frame at 29:56 shows the `RegisteredClient` with authorization-code, client-credentials, and refresh-token grants. Registration would normally live behind a self-service portal rather than config code.

### [30:27](https://youtu.be/W-OKVLMtPAw?t=1827) OAuth2 client, resource server, and token propagation
A new OAuth2-client app gets login without any local users: the redirect dance exchanges the authorization code for tokens, trading a 100 ms password check for near-instant token validation. A resource server on a second port validates incoming JWT access tokens against the issuer's published keys. Calling it without a token returns 401, and they fix propagation three ways of decreasing verbosity: manually injecting an access-token parameter, a central `OAuth2ClientHttpRequestInterceptor` on the `RestClient`, and a declarative `@GetExchange` HTTP-interface client wired through an HTTP-service-group configurer with the client registration id.

### [40:50](https://youtu.be/W-OKVLMtPAw?t=2450) Backend-for-frontend gateway for SPAs
Citing the roughly 40-page RFC on browser apps with OAuth2, they recommend keeping tokens in the backend: a gateway serves the JavaScript from one path and relays `/api/*` to services with a token-relay filter, so the page never touches tokens or CORS. The gateway defines two functional routes (API relay plus static fallback with lower precedence), a `jwebserver`-served page fetches `/api/message`, and the whole flow works on the first try through the authorization server redirect.

### [45:56](https://youtu.be/W-OKVLMtPAw?t=2756) OAuth2-secured MCP server with Claude Code
The finale applies the same identity stack to AI agents. Garnier-Moiroux turns a roller-skating-class booking app into an MCP server with Spring AI (`@Tool`-annotated methods beside the controllers) and secures it with `spring-ai-community-mcp-server-security-spring-boot-starter`. Adding it via `claude mcp add` prompts for browser login as Alice; Claude Code then lists slots and books every-other-week classes, with the bookings verifiably present in the app afterwards. The closing screen repeats the demo repository, an extended KCDC edition of the material, and the free Leanpub book.

## Tools, libraries and specs
- Spring Security 7 / Spring Boot (one-time-token login, WebAuthn passkeys, MFA authorization-manager factory)
- Spring Authorization Server (now part of Spring Security; OAuth2/OIDC authorization server)
- OAuth2 login client, JWT resource-server validation, `@GetExchange` declarative HTTP clients
- PostgreSQL with `JdbcUserDetailsManager`; bcrypt and Argon2id (via Bouncy Castle or password4j) with `DelegatingPasswordEncoder`
- FIDO2/WebAuthn passkeys (FIDO Alliance; Apple, Google, Microsoft and others)
- BFF (backend-for-frontend) gateway pattern with token relay
- Spring AI MCP server support, `spring-ai-community-mcp-server-security-spring-boot-starter`, Claude Code
- Java 25 (`void main`, `IO.println`, source-file launch), `jwebserver` embedded web server
- Demo code: `github.com/joshlong-attic/2026-10-08-devoxx-secure-all-the-things` (from frame at 50:42)

## Who should watch
Spring developers who secure web apps and want a beginner-friendly tour from password hashing to OAuth2, BFF gateways, and MCP security in one sitting. Skip it if you already run Spring Authorization Server with passkeys and token relay in production; the segments stay introductory and point to the speakers' longer talks for internals.

## Verdict
**8/10**: completed authentication, gateway and agent flows come with beginner-level explanations and reproducible demo code, while the synthesis illustrates known features and the performance figures lack a measurement method.

**Reach segment**: Spring Boot users securing web applications can apply the password, passkey, OAuth2, gateway and MCP examples in their own services.

**Novelty 1/2**

- **+** [45:56](https://youtu.be/W-OKVLMtPAw?t=2756) Bringing passwordless web login, centralized OAuth2 identity, browser gateways and MCP agents into one progression connects material spread across several feature guides.

**Demonstrated 2/2**

- **+** [25:15](https://youtu.be/W-OKVLMtPAw?t=1515) The MFA escalation runs live: a non-admin passes both factors and is forbidden on `/admin`, then Rob the admin is challenged again and reaches the page.
- **+** [44:55](https://youtu.be/W-OKVLMtPAw?t=2695) The gateway, SPA page and authorization-server redirect work on the first attempt.
- **+** [49:40](https://youtu.be/W-OKVLMtPAw?t=2980) Claude Code books every-other-week classes through the OAuth2-secured MCP server, and the bookings appear in the application.

**Measured 1/2**

- **+** [09:18](https://youtu.be/W-OKVLMtPAw?t=558) Bcrypt at work factor 10 is put at about 100 ms per check, anchoring the claim that slow login is by design.
- **−** [08:47](https://youtu.be/W-OKVLMtPAw?t=527) SHA-256 is said to allow billions of guesses per second without a stated hardware setup or measurement method.
- **−** [32:29](https://youtu.be/W-OKVLMtPAw?t=1949) Token validation is called almost instant compared with password checking, but no measurement backs the contrast.

**Depth 2/2**

- **+** [08:17](https://youtu.be/W-OKVLMtPAw?t=497) The password-hashing discussion explains why fast general-purpose hashes help attackers and why password hashing deliberately imposes computational cost.
- **+** [15:58](https://youtu.be/W-OKVLMtPAw?t=958) One-time codes are weighed against passkeys on phishing resistance, with the argument that a code remains a shareable password.
- **+** [40:50](https://youtu.be/W-OKVLMtPAw?t=2450) The BFF gateway choice follows the OAuth2 browser-app guidance: the backend holds tokens and relays authenticated requests for the SPA.

**Reusable 2/2**

- **+** [50:42](https://youtu.be/W-OKVLMtPAw?t=3042) The closing screen points to the session demo repository with the authentication, client, resource-server and gateway examples.
- **+** [02:03](https://youtu.be/W-OKVLMtPAw?t=123) The speakers offer their free Spring Security book alongside the demo code for follow-up reading.
