---
title: Kubernetes for Developers
talkId: "17759"
conference: devoxx-be-2026
speakers: [Alain Regnier]
track: Cloud Native, Data & Infrastructure
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=AxhLQZqZdIg
durationMin: 47
slides: null
verdict: 5
reach: segment
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Kubernetes for Developers
Alain Regnier · Conference · Cloud Native, Data & Infrastructure

## TL;DR
The talk surveys the Kubernetes surface a developer should know without becoming a specialist: local clusters, image builds, resource requests, graceful shutdown, probes, debugging, security and observability. Each topic comes with concrete YAML, commands and defaults to copy, plus newer features such as pod-level resources, in-place resize, image volumes and CEL admission policies. Pre-recorded demo runs illustrate kind, image volumes, kubectl debug and a validating admission policy end to end.

## Key takeaways
- Replace Docker Compose with kind plus a declarative Flox/Nix environment so local development matches production tooling and versions.
- Handle graceful shutdown explicitly: a 10-second preStop sleep, a generous terminationGracePeriodSeconds, PID 1 in exec form, and a SIGTERM handler in your language.
- Give every container requests (even small ones) and use separate liveness and readiness probes that log nothing and avoid external calls.
- Debug shell-less or crashing pods with kubectl debug ephemeral containers, including --target process-namespace sharing and the /proc/1/root filesystem trick.
- Start observability with OpenTelemetry auto-instrumentation, then switch hot paths to manual SDK spans once the agent overhead shows.
- Enforce team rules inside the cluster with CEL validating admission policies (minimum replicas, no :latest, allowed registries) rather than wiki pages.

## Notes

### [02:07](https://youtu.be/AxhLQZqZdIg?t=127) Local development with Flox and kind
The speaker argues Docker Compose drifts from production and presents kind (Kubernetes-in-Docker nodes, with ingress and gateway support via cloud-provider-kind) as the closer alternative, alongside miniKube and K3s. Reproducible tooling comes from Flox and Nix: `flox init`, install packages such as kubectl and kind into the environment, pin versions, and `flox activate` to get the pinned kubectl instead of the stale laptop one. The walkthrough creates two kind clusters (a single-node and a three-node one) from a YAML file describing versions, then runs pods and deployments against them like a real cluster.

### [08:19](https://youtu.be/AxhLQZqZdIg?t=499) Building container images
A quick refresher: trusted base images, non-root users, small images, multi-stage Dockerfiles. Docker is not required to build: Kaniko builds from a Dockerfile inside a container (suited to CI/CD and in-cluster builds; ex-Google, now maintained by Chainguard), Jib is a Maven/Gradle plugin for Java developers, and Buildpacks and Buildah get a mention. Usage is one `docker run` of the Kaniko executor or a Jib plugin block plus `jib:build`.

### [09:51](https://youtu.be/AxhLQZqZdIg?t=591) Requests, limits and in-place resize
Requests are reservations and limits are ceilings; pods without requests are first in line for eviction, so set requests even when small, and avoid oversized requests that strand capacity. Newer Kubernetes allows requests and limits as a shared budget at pod level instead of per container. In-place pod resize (recently stabilized) changes requests and limits without restarting pods, which pairs well with the vertical pod autoscaler; per-resource resizePolicy can restart on memory changes but not CPU ones. Java developers get a caveat: -Xmx is fixed at JVM startup, so memory resize helps them less.

### [12:29](https://youtu.be/AxhLQZqZdIg?t=749) Graceful shutdown
Pods die for many reasons (deletion, rollout, scale-down, node drain, priority preemption, eviction, OOM), and graceful shutdown prevents data loss and refused connections. The sequence: the pod goes Terminating, endpoints drop it, the preStop hook runs (set a 10-second sleep so in-flight requests drain), SIGTERM reaches PID 1, then SIGKILL after terminationGracePeriodSeconds (default 30s). Coverage is uneven: it generally works for rollouts and drains and sometimes for node-pressure eviction, but exceeding the memory limit means the kernel kills the container with no warning. Developer checklist: exec-form CMD/ENTRYPOINT so the app is PID 1 (verify with `ps` via kubectl exec or /proc/1/cmdline), a preStop sleep, a large grace period, and SIGTERM handling (JVM shutdown hook, Spring Boot and Quarkus settings, explicit handlers in Python and Node).

### [18:43](https://youtu.be/AxhLQZqZdIg?t=1123) Probes
Startup (finished booting), readiness (send traffic) and liveness (restart if stuck) probes, usually HTTP with 200-399 counting as success. Examples: Flask routes for /live and /ready, Spring Boot Actuator health endpoints, Quarkus equivalents. Best practices: never share one endpoint for liveness and readiness, emit no logs from probes, avoid hitting databases on every check, and raise timeouts for Java under load, a recurring cause of the mystery restarts the speaker sees in audits. HTTPS probe certificates are not verified.

### [22:25](https://youtu.be/AxhLQZqZdIg?t=1345) Image volumes
An OCI image can be mounted read-only inside a pod, which replaces the init-container trick of copying data (WAR/JAR, ML weights, GeoIP rules, security tools) at startup and reuses registry signing and scanning. The slide notes beta in 1.33 and stable in 1.36. The demo builds a Go blog content image, loads it into the kind cache, deploys with the image referenced in the volumes section, curls one article, then publishes a second article as image v0.2.0 and rolls it out with a patch, after which curl returns both.

### [25:34](https://youtu.be/AxhLQZqZdIg?t=1534) Debugging with kubectl debug
Few in the audience have used kubectl debug. For pods it attaches an ephemeral container (busybox or a debug image) so distroless images stay shell-free; for nodes it drops you on the host filesystem under /host with shared namespaces, optionally privileged. Caveats: ephemeral containers persist until the pod restarts, and node-debug pods must be deleted afterwards. The live scenario: a Python web pod looks Running but curl gets connection refused, exec finds no bash, so kubectl debug with --target plus the /proc/1/root trick reveals the server listening on 8080 instead of 80, and port-forwarding 8080 confirms the fix.

### [33:00](https://youtu.be/AxhLQZqZdIg?t=1980) mirrord and SBOMs
mirrord connects a local process or IDE to a live cluster, replacing one container so breakpoints and local code run against real traffic, env vars and sibling microservices; Telepresence-like but less intrusive, and not literally for production. SBOMs (software bills of materials) list every package inside an image so new CVEs can be matched against shipped artifacts: generate at build time with the bom tool, then rescan with Trivy, so an image built three months ago surfaces today's vulnerabilities.

### [36:06](https://youtu.be/AxhLQZqZdIg?t=2166) RuntimeClass and CEL admission policies
RuntimeClass picks how pod containers execute: the default runC shares the host kernel via cgroups and namespaces, while gVisor filters kernel calls and Kata Containers use lightweight VMs. One runtimeClassName field opts in, at some performance cost and with occasional breakage, which suits untrusted code, AI agents and multi-tenancy. CEL (Common Expression Language) expresses API-server validation that once needed extra webhooks. The GKE demo creates a policy requiring at least two replicas with a custom error message, binds it to the testvap namespace, and shows a one-replica nginx deployment rejected; further examples ban docker.io images and :latest tags, with Deny, Audit and Warn actions.

### [40:48](https://youtu.be/AxhLQZqZdIg?t=2448) securityContext and OpenTelemetry
securityContext hardens pod and container specs: refuse root, pin user and group, drop Linux capabilities, enforce a read-only root filesystem with state on real storage. OpenTelemetry, the CNCF standard merging the Prometheus, Jaeger and Zipkin lineages, collects traces, metrics and logs through vendor-neutral SDKs and a Collector speaking OTLP (gRPC 4317, HTTP 4318) to backends such as Jaeger, Tempo, Prometheus or Victoria Metrics. Developers should start with zero-code auto-instrumentation (Java agent, Node preload), then hand-instrument key methods with SDK spans and propagate W3C trace context so a slow span links to the logs emitted at that moment.

## Tools, libraries and specs
- kind (pinned version in Flox env) + cloud-provider-kind, Flox + Nix, miniKube, K3s
- Kaniko (Chainguard-maintained), Jib (Maven/Gradle), Buildpacks, Buildah
- Kubernetes 1.33–1.36 features: pod-level resources, in-place pod resize, image volumes, ValidatingAdmissionPolicy, CEL
- kubectl debug (ephemeral containers, --target, node debugging), mirrord, Telepresence
- bom (SBOM generation), Trivy (CVE scanning), gVisor, Kata Containers, runC
- OpenTelemetry (SDKs, Collector, OTLP 4317/4318, W3C traceparent), Jaeger, Tempo, Prometheus, Victoria Metrics, Grafana
- Spring Boot Actuator, Quarkus, Flask

## Who should watch
Developers shipping to Kubernetes who configure their own manifests and want the essential checklist in one sitting. Teams standardizing shutdown, probes and resource defaults gain directly. Cluster administrators and anyone after depth on one feature (CEL policy design, OTel pipeline operations) should look for dedicated sessions instead.

## Verdict
**5/10**: a wide-ranging Kubernetes-for-developers survey with a well-explained shutdown and debugging core, held back by replayed demos, an unmeasured overhead claim and no published artifact.

**Reach segment**: developers shipping their services to Kubernetes, a sizable share of this Java audience, can apply its manifest, shutdown, probe and debugging checklist in their own work.

**Novelty 1/2**

- **+** [21:54](https://youtu.be/AxhLQZqZdIg?t=1314) Audit experience names a pitfall seen at client companies: Java probe timeouts under load causing apparently random restarts.
- **−** Pod-level resource budgets, in-place pod resize and image volumes are covered by the official Kubernetes documentation and release notes.

**Demonstrated 1/2**

- **+** [31:24](https://youtu.be/AxhLQZqZdIg?t=1884) The kubectl debug scenario runs from connection refused through `--target` and `/proc/1/root` to the wrong-port root cause and the confirming port-forward and curl.
- **+** [40:48](https://youtu.be/AxhLQZqZdIg?t=2448) The admission-policy run shows the policy, the binding and the one-replica nginx deployment rejected with the custom message.
- **−** [29:30](https://youtu.be/AxhLQZqZdIg?t=1770) The demos replay an earlier run on slides rather than a live terminal or a recording of the run: this frame shows the `kubectl debug` command with no output while the speaker narrates the results.

**Measured 0/2**

- **−** [45:01](https://youtu.be/AxhLQZqZdIg?t=2701) The OpenTelemetry agent is said to use "a lot more resources than my core application", the reason given for switching to manual SDK spans, with no number, baseline or method.

**Depth 2/2**

- **+** [14:02](https://youtu.be/AxhLQZqZdIg?t=842) The termination sequence is explained in order with the reason for each safeguard: endpoint removal, the preStop sleep, SIGTERM to PID 1, the grace period, and the OOM kill that skips all of them.
- **+** [30:22](https://youtu.be/AxhLQZqZdIg?t=1822) The debugging segment explains why a plain `kubectl debug` shows no processes (no process-namespace sharing) and why `--target` and `/proc/1/root` expose the main container's files.
- **+** [37:39](https://youtu.be/AxhLQZqZdIg?t=2259) The gVisor and Kata Containers options come with their costs stated: possible breakage and execution overhead, which suits untrusted code and multi-tenancy.

**Reusable 1/2**

- **+** [40:20](https://youtu.be/AxhLQZqZdIg?t=2420) Policy, binding and probe YAML and commands appear on screen as copyable fragments.
- **+** [35:33](https://youtu.be/AxhLQZqZdIg?t=2133) The bom-generate and Trivy rescan commands are named for the SBOM workflow but left for the viewer to reconstruct.
- **·** [47:06](https://youtu.be/AxhLQZqZdIg?t=2826) No repository, sample project or checklist covering the talk's content is pointed to; the talk ends on the OpenTelemetry slides.
