---
title: "Java on Kubernetes Without Container Images: The WebAssembly Way"
talkId: "25048"
conference: devoxx-be-2026
speakers: [Bruno Borges]
track: Cloud Native, Data & Infrastructure
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=fszyRIZXjQM
durationMin: 53
slides: null
verdict: 9
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15

# Java on Kubernetes Without Container Images: The WebAssembly Way
Bruno Borges · Conference · Cloud Native, Data & Infrastructure

## TL;DR
Borges presents Brewlet, his open-source project that runs Java applications on Kubernetes straight from OCI artifacts (JAR plus metadata) with the JDK installed on the node, so platform teams own the runtime and developers ship only their code. The approach copies the SpinKube/KWasm model for WebAssembly: a `RuntimeClass`, a containerd shim, and a node provisioner assemble the JDK, dependencies, and application at deploy time. A live demo deploys a Spring Boot app and upgrades it from JDK 25 to 27 without rebuilding the artifact.

## Key takeaways
- Java bytecode is already portable, so a container image around it can be redundant: the registry can hold just the JAR, classpath, and JVM launch configuration while the node provides the JDK.
- `runtimeClassName: brewlet` on a Deployment (or a `JavaApplication` CRD) routes scheduling through a custom containerd shim that bundles the OCI artifact with a platform-approved JDK and launches it under runC like any other container.
- Splitting the stack into three independently managed layers (thin application JAR, managed dependency bundle, node-managed JDK) lets a JDK patch mean restarting pods and a dependency CVE mean repointing an OCI reference, with no application rebuild.
- Platform teams define approved JDKs per node pool in a node profile (distribution, major version, source image digest, java-home path); mixing Brewlet and regular workloads in one cluster works because selection is per-workload.
- An experimental platform of this scope (operator, provisioner, shim, CLI, Maven plugin) was built by one Java developer in about 12 weeks using spec-driven agentic coding, with real clusters catching the 30% of bugs kind and Docker Desktop missed.

## Notes

### [02:08](https://youtu.be/fszyRIZXjQM?t=128) Ownership has shifted too far to developers
Developers write only the business layer but own every layer beneath it: dependencies, JDK, base OS image. A CVE in any of them forces every team to pause, rebuild, and redeploy. Golden images and smart pipelines soften the pain, but the rebuild-everything cycle remains. Brewlet moves the runtime and optionally the dependencies back to platform-team ownership.

### [06:18](https://youtu.be/fszyRIZXjQM?t=378) The SpinKube model, mapped onto Java
SpinKube (originally KWasm) puts a WebAssembly runtime on the node; developers push only a Wasm module to OCI and select it with a RuntimeClass. The same mapping works for Java: portable bytecode (JAR) instead of a portable Wasm module, a JAR plus classpath/module path plus launch configuration instead of a Wasm app as the developer artifact. Project started about three months before the talk.

### [08:24](https://youtu.be/fszyRIZXjQM?t=504) Brewlet in one picture
A CLI and a Maven plugin build the application and push it to OCI. A Helm-installed operator and provisioner enable chosen node pools, and `runtimeClassName: brewlet` triggers the node-installed JDK to launch the artifact. Unlike Cloud Foundry and buildpacks, whose end product is still a container image, the OCI registry here holds only the JAR, metadata, and optionally dependencies; the runtime is assembled on the node at deploy time.

### [09:57](https://youtu.be/fszyRIZXjQM?t=597) What happens behind runtimeClassName
`kubectl apply` goes to the scheduler, which reads the RuntimeClass and picks a node; kubelet prepares the sandbox through containerd, and the shim assembles the bundle from OCI plus the JDK, then launches it with runC. The result is a cgroup namespace with a JVM process as PID 1. The shim is a TTRPC task service; bundling generates `config.json` and a rootfs whose userland is the JDK container image mounted read-only, so applications cannot modify the shared runtime. runC was chosen for stability over newer runtimes, and all resource limits and configuration behave as with traditional containers.

### [15:12](https://youtu.be/fszyRIZXjQM?t=912) Platform side: node profiles and approved JDKs
After installing the operator, provisioner, daemonset, and admission webhook, the platform team writes a node profile per node pool: distribution name, JDK major version, source image digest, and the java-home path inside that image. A JDK entry can also be a customized image carrying modules, libraries, configuration, or CA roots.

### [17:21](https://youtu.be/fszyRIZXjQM?t=1041) Developer side: annotations or a CRD
A plain Deployment needs only `runtimeClassName: brewlet` plus `brewlet.sh/jdk` (and optionally `brewlet.sh/jvm-args`) annotations. Alternatively a `JavaApplication` CRD (apiVersion `apps.brewlet.sh/v1alpha1`) declares the OCI artifact digest, replicas, JVM version and distribution, resources, ports, service creation, and autoscaling in one object, and the operator expands it into Deployment plus Service (plus HPA).

### [19:27](https://youtu.be/fszyRIZXjQM?t=1167) Managed dependency bundles: three layers
A platform team can publish an approved BOM as an immutable OCI artifact; the Maven project references the BOM's dependency management and the deployment references its OCI artifact, which the runtime bundles at provisioning. App change means a new JAR; dependency CVE means repointing to a new bundle; JDK CVE means updating the node and restarting pods.

### [22:38](https://youtu.be/fszyRIZXjQM?t=1358) Live demo on AKS
After a screen-mirroring hiccup filled with audience Q&A, the demo runs against a real AKS cluster: operator and provisioner already installed, node pool advertising Temurin 25, Temurin 27, and a distroless 25 build. The Maven plugin configuration sets registry, image name, layered mode with separate snapshot layers, port 8080, and default readiness/liveness probes. `brewlet push` initially fails because Docker Desktop is not running; after starting it, login and push succeed. `brewlet inspect` shows the OCI manifest: config layer, application tarball layer, a large classpath layer, a snapshot-deps layer, and a JVM launch-configuration layer (classpath, fat-JAR, and JPMS module modes supported). `kubectl apply` of the generated `JavaApplication` manifest brings up the ShowMyJVM Spring Boot app, tunneled into a browser. Then, with the same artifact digest, the node profile switches the workload from JDK 25 to 27 and the app's JVM page confirms Eclipse Adoptium 27 (SerialGC to G1, the new default). Rollback and a shell-into-distroless failure are mentioned but skipped for time; a Quarkus variant of the demo exists in the same project.

### [26:23](https://youtu.be/fszyRIZXjQM?t=1583) Mid-talk Q&A
Static files outside the JAR would need pipeline changes to land in the application layer (use case not yet explored). Brewlet is opt-in per workload, so clusters mix Brewlet and regular deployments freely. Prometheus telemetry from workloads should work but is untested.

### [46:54](https://youtu.be/fszyRIZXjQM?t=2814) Built with agents: the numbers and the method
About 12 weeks, 600 commits (over half AI-assisted), 48,000 lines of Go, a 2,200-line specification, and a comprehensive test harness; a burst-VM operator bug was fixed the night before. The method: humans own the specification and trust boundaries, review selectively, have agents review too, and always test on real clusters. Recipe for a custom platform: containerd shim, node provisioner, RuntimeClass, CRD.

### [49:34](https://youtu.be/fszyRIZXjQM?t=2974) Takeaways and links
Ship what you wrote and let the platform team own the runtime; `runtimeClassName` is the door (CRI to containerd to Runtime v2 TTRPC shim to OCI bundle to runC); custom platforms are cheap to build now. Brewlet is experimental, pre-1.0: try it with kind, Docker Desktop, or staging clusters. Site at brewlet.sh, code under the Microsoft organization on GitHub.

### [50:37](https://youtu.be/fszyRIZXjQM?t=3037) Closing Q&A
Fontconfig for image-rendering apps must come from the chosen JDK image, which the platform team can customize. No Gradle plugin yet, but the CLI is easy to wrap in a Gradle task. Live repatching of dependency layers is architecturally plumbed but untested.

## Tools, libraries and specs
- Brewlet (CLI, Maven plugin, Kubernetes operator, node provisioner, admission webhook, `JavaApplication` CRD) — experimental, pre-1.0, at brewlet.sh and GitHub `microsoft/brewlet`
- SpinKube / KWasm (WebAssembly on Kubernetes via RuntimeClass)
- containerd with a Runtime v2 TTRPC shim, runC, OCI artifacts and registries
- Spring Boot and Quarkus demo apps (ShowMyJVM project on the speaker's GitHub)
- Eclipse Temurin / Adoptium JDK 25 and 27, Microsoft OpenJDK image, distroless JDK images
- Azure Kubernetes Service (AKS), Azure Container Registry, Helm, kind, Docker Desktop

## Who should watch
Platform engineers and Kubernetes-minded Java developers weighing who should own the JDK and dependency layers, and anyone curious how far RuntimeClass plus a custom shim can stretch Kubernetes. Teams happy with buildpacks or golden images, and viewers wanting production hardening or performance data, can skip it: this is an experimental project's debut, not a migration guide.

## Verdict
**9/10**: Brewlet is the speaker's own design, shown live from push through a JDK 25 to 27 switch on an unchanged artifact digest, with a public repo; the main limit is that its only numbers are self-reported totals.

**Novelty 2/2**

- **+** [07:20](https://youtu.be/fszyRIZXjQM?t=440) The SpinKube model is mapped onto Java (JAR plus classpath and launch configuration as the developer artifact) in the speaker's own project, first shown publicly at this talk.
- **+** [19:27](https://youtu.be/fszyRIZXjQM?t=1167) The three-layer ownership model with managed dependency bundles as immutable OCI artifacts is the speaker's own design.

**Demonstrated 2/2**

- **+** [41:33](https://youtu.be/fszyRIZXjQM?t=2493) The Spring Boot app deploys from the OCI artifact and serves its JVM details page in the browser, live.
- **+** [44:48](https://youtu.be/fszyRIZXjQM?t=2688) The workload switches from JDK 25 to 27 with the artifact digest unchanged, confirmed on the app's JVM page.
- **−** [30:02](https://youtu.be/fszyRIZXjQM?t=1802) The Helm install walkthrough is a replay ("a simulation, not a live execution because it's already installed"), and the rollback and distroless-shell steps are cut for time at [45:50](https://youtu.be/fszyRIZXjQM?t=2750).

**Measured 1/2**

- **+** [47:26](https://youtu.be/fszyRIZXjQM?t=2846) The build effort is quantified as 12 weeks, 600 commits, 48,000 lines of Go, and a 2,200-line specification.
- **−** [14:40](https://youtu.be/fszyRIZXjQM?t=880) The claims of building a custom platform "in a matter of weeks instead of years" and "way cheaper now" ([49:34](https://youtu.be/fszyRIZXjQM?t=2974)) rest on those self-reported totals, with no baseline.
- **−** [48:30](https://youtu.be/fszyRIZXjQM?t=2910) "kind and Docker Desktop covered 70% of the issues, the other 30% only in real clusters" is a ratio with no stated method.

**Depth 2/2**

- **+** [10:59](https://youtu.be/fszyRIZXjQM?t=659) The request path from scheduler through kubelet, containerd, the TTRPC shim, and runC down to a PID 1 JVM is explained stage by stage.
- **+** [13:37](https://youtu.be/fszyRIZXjQM?t=817) The bundle layout and its reasons are given: app JAR under /app, the JDK mounted read-only so apps cannot modify it and nodes can share it, and runC chosen for stability over newer runtimes.
- **−** [52:10](https://youtu.be/fszyRIZXjQM?t=3130) Live repatching of dependency layers is admitted untested, so that part of the design has no proven behavior yet.

**Reusable 2/2**

- **+** [50:04](https://youtu.be/fszyRIZXjQM?t=3004) The talk points to brewlet.sh and github.com/microsoft/brewlet, which hold the CLI, shim, operator, provisioner, and Maven plugin.
- **+** [46:23](https://youtu.be/fszyRIZXjQM?t=2783) The demoed ShowMyJVM project with Spring Boot and Quarkus variants is published on the speaker's GitHub for trying the flow.
- **·** [48:30](https://youtu.be/fszyRIZXjQM?t=2910) The project is experimental and pre-1.0, recommended only for kind, Docker Desktop, or staging clusters.
