---
title: Building LLM Inference Engines in Java with TornadoVM and the NVIDIA Ecosystem
talkId: "19730"
conference: devoxx-be-2026
speakers: [Thanos Stratikopoulos, Michalis Papadimitriou, Orion Papadakis]
track: Java Language & Platform
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=HO5CpETzywk
durationMin: 45
slides: null
verdict: 8
reach: niche
frames: 10
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Building LLM Inference Engines in Java with TornadoVM and the NVIDIA Ecosystem
Thanos Stratikopoulos, Michalis Papadimitriou, Orion Papadakis · Conference · Java Language & Platform

## TL;DR
The TornadoVM team presents jitllm, a pure-Java LLM inference engine that JIT-compiles model architectures to CUDA and mixes generated kernels with NVIDIA library calls, reaching 90-97% of llama.cpp decode throughput and beating it on prefill. Live benchmarks and two Quarkus/LangChain4j application demos show the engine running real models on a laptop RTX 5090 GPU.

## Key takeaways
- A Java inference engine can match llama.cpp: jitllm reaches up to 97% of llama.cpp decode throughput and up to 1.2x on prefill, measured with a Java port of the llama.cpp bench harness.
- Prefill and decode need different strategies: prefill is compute-bound, so jitllm routes GEMMs through cuBLAS/cuDNN; decode is memory-bandwidth-bound, so it runs fully JIT-compiled TornadoVM kernels.
- TornadoVM task graphs map onto CUDA graphs, so a whole transformer layer (alternating JIT kernels and library calls) dispatches as one unit with zero per-op dispatch overhead.
- Enabling batch prefill gave a 15x prefill speedup and native libraries added another 2x, for roughly 30x over naive token-by-token prefill.
- Local GPU inference drops into existing Java apps three ways: embed the `LocalModels.load(path)` API, swap the model provider in Quarkus LangChain4j or Spring AI config, or run `jitllm serve` as an OpenAI-compatible HTTP server.
- Quantized GGUF models up to 70B parameters (Llama 3, Qwen 3, Gemma, GLM, Mistral) run on a desktop or laptop GPU; FP32, Q8 and Q4 quantizations are supported.

## Notes

### [02:11](https://youtu.be/HO5CpETzywk?t=131) Opening demo: inference generating GPU code
The talk opens with a recorded demo on a desktop RTX 5090: a Qwen3 4B model in FP16 generates TornadoVM-compatible Java code for a Mandelbrot computation, the harness compiles it through javac, TornadoVM JIT-compiles it to CUDA, and it runs on the same GPU that ran the inference. The point: one Java engine runs the model and produces GPU code for the same device.

### [03:44](https://youtu.be/HO5CpETzywk?t=224) Headline numbers against llama.cpp
Last year's implementation was 10-30x slower than llama.cpp; the current engine reaches 90-97% of llama.cpp decode throughput and outperforms it on prefill in some cases. Supported models on screen include Gemma, GLM 4.5/4.7, Qwen3 8B and 27B. All comparisons use llama.cpp's own bench harness, ported to Java.

### [06:23](https://youtu.be/HO5CpETzywk?t=383) Why local inference on the JVM
Cloud access via LangChain4j, Quarkus LangChain, Spring AI is already smooth; the gap is local inference. HTTP to Python frameworks or JNI/FFM to llama.cpp work but leave pure Java. CPU-only Java options such as llama3.java and JLama exist, but nothing gave GPU acceleration from Java, which is the space TornadoVM targets.

### [09:01](https://youtu.be/HO5CpETzywk?t=541) TornadoVM: four ways to program the GPU
TornadoVM is a Java framework (JDK 21-27, CUDA/OpenCL/Metal) with four programming levels: `@Parallel` loop annotations with CPU fallback, the Kernel Context API close to CUDA intrinsics, the Tile Context abstraction between them, and Library Tasks calling NVIDIA libraries directly. All four chain into one compute pipeline. Distribution is via Maven jars and SDKMAN (`sdk install tornadovm`), with tooling (TornadoVM Pulse, VS Code plugin, Tornado Inside) bridging JFR profiling and Nsight debugging.

### [15:48](https://youtu.be/HO5CpETzywk?t=948) jitllm architecture: six layers
The engine was rebuilt from last year's GPULlama3.java into layered abstractions: a public API (`load` a GGUF file, create session, generate, close), an engine layer that queues and schedules requests (experimental continuous batching), a models layer for families/quantizations (FP32, Q8, Q4)/execution modes/devices/CUDA graphs/on-device sampling, a program layer chaining device-independent abstract ops, a lowering step mapping each op to a TornadoVM task graph and JIT-compiling it, and a backend layer executing on GPU or CPU. A paged KV cache splits the cache into reusable blocks shared across sessions to cut memory footprint.

### [23:41](https://youtu.be/HO5CpETzywk?t=1421) Live benchmark: jitllm bench vs llama.cpp
`jitllm bench` replicates llama.cpp's bench with identical parameters: 4K-token prefill, 128 generated tokens, 5 repetitions, native libraries on for prefill. On Qwen3 0.6B the result on screen: prefill 43,774 vs 36,291 tok/s (1.20x llama.cpp), decode 438.4 vs 471.0 tok/s (93% of llama.cpp). The same 90%+ decode pattern holds for Llama 3 70B and Qwen3 27B.

### [27:56](https://youtu.be/HO5CpETzywk?t=1676) Mixing JIT kernels with NVIDIA libraries
One transformer layer is a single TornadoVM task graph alternating purple JIT kernels (RMSNorm, RoPE+KV, SwiGLU) with green library calls (cuBLAS QKV/output/gate-up/down projections, JIT-or-cuDNN attention). Weights, activations and KV cache stay in shared device buffers; the whole graph is captured as a CUDA graph with zero dispatch overhead. A `--with-native-libraries` flag swaps the default Java MMA tensor-core kernel for cuBLAS GEMM; paged Q/K/V is packed to contiguous layout for cuDNN SDPA, then scattered back.

### [33:44](https://youtu.be/HO5CpETzywk?t=2024) Prefill vs decode, quantified
Batch prefill alone gave a 15x prefill improvement over naive token-by-token; native libraries added 2x more, about 30x combined. Prefill is compute-bound so mature libraries win; decode is bandwidth-bound so libraries stop helping and all-JIT wins.

### [34:48](https://youtu.be/HO5CpETzywk?t=2088) Three ways into your app
Embed the Java API, use the Quarkus/Spring framework integration by pointing the model provider at jitllm (standard `@RegisterAiService` code), or run `jitllm serve --model.gguf --gpu` for an OpenAI-compatible server on `localhost:8089/v1`.

### [36:58](https://youtu.be/HO5CpETzywk?t=2218) Demo 1: Quarkus weather agent with tool calling
A Quarkus LangChain4j sample runs on jitllm (Qwen3-8B Q8) with three tools: extract-city, coordinate search, and a remote forecast API. Asked for Manchester, then Antwerp, it returns plausible temperatures (22/13), with the second query answering immediately since the model stays loaded.

### [39:36](https://youtu.be/HO5CpETzywk?t=2376) Demo 2: GitHub PR reviewer on a 27B model
A Quarkus app fetches a real open jitllm pull request, loads Qwen3-28 27B, and streams a review summary with nvtop showing RTX 5090 laptop GPU utilization. A second round reviews a Quarkus LangChain4j Quarkus-4 port PR without reloading the model; its lengthy output was left running. The team plans to add the reviewer to their CI pipeline.

### [43:25](https://youtu.be/HO5CpETzywk?t=2605) Closing: try it
Everything is public: github.com/beehive-lab/jitllm, github.com/beehive-lab/TornadoVM, Maven Central `io.github.beehive-lab:jitllm`, the LangChain4j jitllm provider docs, CUDA demos, and SDKMAN installs.

## Tools, libraries and specs
- jitllm (github.com/beehive-lab/jitllm, Maven `io.github.beehive-lab:jitllm`) — the Java inference engine presented
- TornadoVM 2.x (tornadovm.org, SDKMAN, JDK 21-27) — Java-to-CUDA/OpenCL/Metal JIT framework
- llama.cpp bench — baseline harness, ported to Java for the comparison
- NVIDIA cuBLAS, cuDNN, cuFFT, cuTENSOR, CUDA graphs — called from Java via TornadoVM Library Tasks, no JNI
- Quarkus 3.40 + Quarkus LangChain4j, LangChain4j, Spring AI — integration targets
- GGUF models: Qwen3 (0.6B, 4B, 8B, 27B), Llama 3 70B, Gemma, GLM 4.5/4.7, Mistral; FP32/Q8/Q4
- RTX 5090 (desktop and laptop GPU) — demo and benchmark hardware

## Who should watch
Java developers curious about local LLM inference or GPU programming from the JVM, and anyone evaluating alternatives to shipping Python/llama.cpp sidecars. Skip if you only consume models through cloud APIs, or if you want TornadoVM compiler internals: that material was explicitly left to earlier deep dives.

## Verdict
**8/10**: A Java GPU inference engine benchmarked live against llama.cpp with a stated method (prefill 1.20x, decode 93%) and explained at the level of design reasons, with two Quarkus apps running on screen; Novelty is limited by the project's own docs covering the feature tour and Reusable by the project's own repo being the main artifact.

**Reach niche**: GPU and inference-engine developers in the audience; the Quarkus and LangChain4j provider swap needs an NVIDIA GPU and serves teams self-hosting local models, which most of the conference audience does not.

**Novelty 1/2**

- **+** [30:37](https://youtu.be/HO5CpETzywk?t=1837) The speakers report which transformer-layer operations they found fastest as JIT kernels and which as cuBLAS calls, a result of their own tuning, though the way they found it is not shown.
- **·** [03:13](https://youtu.be/HO5CpETzywk?t=193) They claim the engine can autotune the code it generates on the same GPU that runs inference, a feature claim with no experience behind it in the talk.
- **−** The tornadovm.org/jitllm page, the LangChain4j provider docs and the CUDA demos repo already state the toolkit, its TornadoVM compilation, the hybrid JIT-plus-library design and the supported model families.

**Demonstrated 2/2**

- **+** [24:15](https://youtu.be/HO5CpETzywk?t=1455) The live `jitllm bench` run is on screen with its llama.cpp comparison printed.
- **+** [39:03](https://youtu.be/HO5CpETzywk?t=2343) The weather agent completes its three-tool chain and returns 22/13 for the host city, which the presenter checks ("Okay seems correct").
- **+** [40:38](https://youtu.be/HO5CpETzywk?t=2438) The PR reviewer loads a 27B model, reads a real open pull request and returns its summary, with nvtop showing the memory line while the model loads.

**Measured 2/2**

- **+** [24:47](https://youtu.be/HO5CpETzywk?t=1487) The bench method is stated: llama.cpp's bench ported to Java with identical parameters, 4K prefill tokens, 128 decode tokens, 5 repetitions.
- **+** [26:56](https://youtu.be/HO5CpETzywk?t=1616) Last year's engine was "10 to 30 times slower" than llama.cpp and the current one is at near parity, a before/after on the same comparison.
- **+** [33:44](https://youtu.be/HO5CpETzywk?t=2024) Batch prefill gives a 15x prefill gain over token-by-token and native libraries add another 2x, each step attributed, though no run is shown (the caption's "30%" for the combined figure reads as 30x).

**Depth 2/2**

- **+** [33:14](https://youtu.be/HO5CpETzywk?t=1994) Prefill takes the library path because it is compute-bound while decode stays all-JIT because it is bandwidth-bound, with the reasoning for each.
- **+** [21:34](https://youtu.be/HO5CpETzywk?t=1294) Abstract ops lower to TornadoVM task graphs and JIT-compile to device code, and the six engine layers are walked with each layer's responsibility.
- **+** [23:07](https://youtu.be/HO5CpETzywk?t=1387) The paged KV cache is split into blocks shared across sessions, so concurrent requests avoid one full cache copy each.

**Reusable 1/2**

- **+** [43:56](https://youtu.be/HO5CpETzywk?t=2636) The closing slide links the jitllm and TornadoVM repos, Maven coordinates, the LangChain4j provider docs and a CUDA demos repo with runnable Java and CUDA versions of 23 demos, including the JIT→cuBLAS→JIT graph.
- **−** [34:48](https://youtu.be/HO5CpETzywk?t=2088) The three integration paths (`LocalModels.load(path)`, a registered LangChain4j service, `jitllm serve -m model.gguf --gpu`) come as slide fragments, not a sample project.
- **−** [42:19](https://youtu.be/HO5CpETzywk?t=2539) The PR-reviewer app is offered on request ("we can share the demo with you") rather than linked, and the linked repos do not contain the bench setup or the two Quarkus apps.
