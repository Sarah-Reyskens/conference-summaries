---
title: High-Performance Java-Native AI with CUDA and the Vector API
talkId: "22947"
conference: devoxx-be-2026
speakers: [Zoran Sevarac]
track: Java Language & Platform
sessionType: Conference
audienceLevel: ADVANCED
video: https://www.youtube.com/watch?v=8NURE3I4AJQ
durationMin: 49
slides: null
verdict: 7
frames: 9
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# High-Performance Java-Native AI with CUDA and the Vector API

Zoran Sevarac · Conference · Java Language & Platform

## TL;DR

Modern Java can run neural networks on CPUs and NVIDIA GPUs with no JNI and no Python, using the Foreign Function & Memory API for CUDA access and the Vector API for SIMD. The speaker shows how his Deep Netts platform layers these accelerators, reports a benchmark where GPU timings beat single-threaded CPU by about 9x on large datasets, and closes with a fraud detection model wired into Spring Boot.

## Key takeaways

- Prefer the FFM API's jextract, arenas, and OS library loading over JNI when calling native GPU libraries: generated bindings, resource-scoped off-heap memory, and no hand-rolled loader logic.
- Never write raw CUDA kernels for routine ML math; call cuBLAS/cuDNN-style libraries, since kernel code is hard to debug (opaque pointers, six-plus-parameter calls, "bad parameter" failures).
- Plan CUDA distribution up front: either assume compatible drivers and libraries on the target machine or bundle gigabytes of version-sensitive native libraries, since both choices break in different ways.
- For small datasets, Vector API acceleration on CPU roughly matches GPU speed, so a GPU only pays off once data movement stops dominating runtime.
- Wrap generated FFM bindings in a domain-level API (tensors, accelerator services) instead of exposing C-style pointer calls to application code.

## Notes

### [00:34](https://youtu.be/8NURE3I4AJQ?t=34) Intro: a Java-native AI platform

Sevarac introduces Deep Netts, a Java-native ML platform meant to give Java developers hardware-accelerated machine learning without deep-learning expertise or leaving the JVM ecosystem.

### [02:06](https://youtu.be/8NURE3I4AJQ?t=126) Why Java fell behind in AI

Modern AI is mostly matrix math over vectors, but Java lacked GPU support, talked to native libraries only through painful JNI, and could not express SIMD vectorized CPU operations explicitly; auto-vectorization usually failed to trigger for unclear reasons.

### [04:10](https://youtu.be/8NURE3I4AJQ?t=250) Project Panama answers: FFM and the Vector API

Two Panama APIs address those gaps: the Foreign Function & Memory API (final since Java 21, stable and fast in Java 25 by his benchmarks) for safe native calls, and the Vector API for explicit SIMD over array chunks.

### [04:42](https://youtu.be/8NURE3I4AJQ?t=282) FFM's three load-bearing features

The jextract tool generates Java bindings from C headers and binaries, ending handwritten JNI C/Java pairs and manual rewrites on version bumps. Arenas treat native memory as a try-with-resources resource, so off-heap segments free automatically at scope exit. Library loading delegates to the OS loader instead of manual `System.loadLibrary` chains, which matters once dependencies multiply.

### [08:53](https://youtu.be/8NURE3I4AJQ?t=533) The Vector API idea

Instead of looping element by element, code loads a chunk of an array into a vector register and applies one instruction to all lanes (SIMD). The API exposes the register capacity through species and `loopBound`, so the same code adapts to the CPU it runs on.

### [10:27](https://youtu.be/8NURE3I4AJQ?t=627) CUDA programming model crash course

CUDA is NVIDIA-only. Each GPU thread runs a kernel function over part of a huge array; threads group into three-dimensional blocks, blocks into a three-dimensional grid. Large structured arrays (tensors) carry explicit layout metadata, blocks synchronize and share memory, and the host cannot inspect device variables directly.

### [13:14](https://youtu.be/8NURE3I4AJQ?t=794) The data path that dominates GPU cost

Data must travel from the Java heap to native memory, then to GPU device memory; results come back the same way. Transfer, not arithmetic, is usually the bottleneck, which is why many published GPU benchmarks mostly measure transfer optimization and graph-level caching.

### [14:48](https://youtu.be/8NURE3I4AJQ?t=888) The pain of shipping CUDA with Java

A working CUDA stack needs about ten native libraries (CUDA runtime, cuBLAS, cuDNN, others) totaling around 1.5 GB, plus platform extras such as zlib on Windows and a C compiler for custom kernels. Driver, card, CUDA, and cuDNN versions must line up; install locations and library names differ between Windows and Linux distributions.

### [19:33](https://youtu.be/8NURE3I4AJQ?t=1173) Integrating CUDA through FFM

The recipe: run jextract over CUDA headers to get static-method bindings with pointers as memory segments, link libraries by name or full path via system lookup, and manage device-side buffers with arenas. Deep Netts adds automatic probing of default install locations and names, since that lookup is a main failure point. Proprietary CUDA structs surface as generic pointers, which the speaker flags as an open modeling annoyance.

### [24:16](https://youtu.be/8NURE3I4AJQ?t=1456) SIMD walkthrough: adding two float vectors

On-screen code loads chunks of arrays A and B with `FloatVector.fromArray`, adds them with one `add` call compiled to register operations (no objects allocated), stores the result into C, and finishes leftover elements that do not fill a register with a scalar loop. Reported speedups reach 10x depending on workload, but only for problems expressible as vector math.

### [29:31](https://youtu.be/8NURE3I4AJQ?t=1771) Accelerator architecture in Deep Netts

An Accelerator Service Provider specifies tensor and neural-network operations; FFM-backed CUDA and Vector API implementations sit behind it, with Project Babylon, TornadoVM, and Intel oneAPI named as future providers. Above the raw generated bindings, five layers stack up: native CUDA libraries, jextract bindings, a higher-level Java API hiding C pointer style, the CUDA accelerator service, and Deep Netts Core.

### [34:14](https://youtu.be/8NURE3I4AJQ?t=2054) Fraud detection use case

Rule-based fraud detection decays as fraudsters adapt, so the demo trains a feedforward network on about a million generated transactions (under 10% fraudulent). Features include distance from home, distance from the previous transaction, ratio to median purchase, repeated retailer, amount, transaction counts, and online-order flag.

### [37:53](https://youtu.be/8NURE3I4AJQ?t=2273) Enabling the accelerators

Vector API use needs `--add-modules jdk.incubator.vector` plus a Deep Netts `setUseVectorAPI(true)` switch; native access needs `--enable-native-access=ALL-UNNAMED` (a warning today, mandatory later); CUDA needs `setUseCUDA`. The speaker expects the Vector API to leave incubation within about a year.

### [40:02](https://youtu.be/8NURE3I4AJQ?t=2402) Benchmarks: single-threaded CPU vs Vector API vs GPU

On a small feedforward network (hidden layers 32, 16, 8; Intel i9 CPU, RTX 4070 GPU), benchmark timings (the slide's "Performance Metrics (ms)" never says what is timed) scale with dataset size: at 1M rows, Vector API (554 ms, 2.2x) slightly beats GPU (595 ms, 2.1x) over the 1,238 ms CPU baseline; at 10M/20M/50M rows the Vector API holds near 2x while the GPU reaches 9.2x/9.5x/9.4x. Conclusion: small data runs fine on CPU with Vector API help; large data justifies the GPU.

### [43:17](https://youtu.be/8NURE3I4AJQ?t=2597) Train, test, and Spring Boot integration

A builder defines the network, a trainer sets stop error, epochs, and learning rate, then `train` and `test` run against the datasets and report classification metrics:

```java
// from slide at 43:30
FeedForwardNetwork neuralNet = FeedForwardNetwork.builder()
    .addInputLayer(numInputs)
    .addFullyConnectedLayer(32, ActivationType.RELU)
    .addFullyConnectedLayer(16, ActivationType.RELU)
    .addOutputLayer(numOutputs, ActivationType.SIGMOID)
    .lossFunction(LossType.CROSS_ENTROPY)
    .build();
neuralNet.train(trainingSet);
EvaluationMetrics evaluation = neuralNet.test(testSet);
```

A Spring Boot service loads the serialized model in `@PostConstruct`, feeds request features into `predict`, and returns a fraud probability against a configurable threshold (0.5–0.8, trading false alarms against misses).

### [45:54](https://youtu.be/8NURE3I4AJQ?t=2754) Open source, course, and JCP working group

Deep Netts went open source two days before the talk, with examples, templates, an ML-for-Java-developers course, and bookable workshops at deepnetts.com. The speaker also recruits real-world use cases for the JCP executive committee's Java and AI working group.

### [48:03](https://youtu.be/8NURE3I4AJQ?t=2883) Q&A: FFM overhead vs raw CUDA and PyTorch

Asked about the cost of the Java layer over CUDA, he admits raw-CUDA JNI-vs-FFM overhead was never measured, but Deep Netts training times came out nearly identical to PyTorch on the same models.

## Tools, libraries and specs

- Deep Netts (open source Java-native ML platform, deepnetts.com)
- Foreign Function & Memory API (final since Java 21; jextract, arenas, `--enable-native-access`)
- Vector API (incubator, `jdk.incubator.vector`, SIMD)
- NVIDIA CUDA: CUDA runtime, cuBLAS, cuDNN (~10 libraries, ~1.5 GB)
- Spring Boot (fraud detection service integration)
- Project Babylon, TornadoVM, Intel oneAPI (named as future accelerator providers)

## Who should watch

Java developers who want GPU or SIMD acceleration without JNI or a Python sidecar, and anyone evaluating Java-native ML stacks for tabular problems like fraud scoring. Skip it if you already maintain FFM-based GPU bindings (the integration lessons will repeat what you know) or if your interest is LLM application development rather than numerical acceleration.

## Verdict

**7/10**: Integration experience from building CUDA support in Java and a three-backend benchmark carry the talk; it loses points for no run of the fraud flow, a benchmark that never says what is timed, and an open-source release that leaves out the accelerators.

**Novelty 2/2**

- **+** [15:51](https://youtu.be/8NURE3I4AJQ?t=951) The ten-library, 1.5 GB CUDA stack with version, driver and platform traps (zlib on Windows, per-distro install paths) comes from the team that built the integration.
- **+** [32:37](https://youtu.be/8NURE3I4AJQ?t=1957) The five-layer FFM-to-Core architecture and Accelerator Service Provider come from the platform's author, with reasons: swap in other accelerators and hide the C pointer API.
- **+** [40:34](https://youtu.be/8NURE3I4AJQ?t=2434) The CPU, Vector API and GPU table across four dataset sizes is a head-to-head the speaker ran himself.

**Demonstrated 1/2**

- **+** [40:34](https://youtu.be/8NURE3I4AJQ?t=2434) The benchmark table puts millisecond timings and speedups for all three backends on screen at 1M through 50M rows.
- **−** [44:19](https://youtu.be/8NURE3I4AJQ?t=2659) The fraud model training and Spring Boot inference appear only as code slides; no live or recorded run with visible output confirms the flow.

**Measured 1/2**

- **+** [40:34](https://youtu.be/8NURE3I4AJQ?t=2434) Each row has a single-threaded CPU baseline against Vector API and GPU times, with the i9 / RTX 4070 hardware and the 32/16/8 network shape on the slide.
- **−** [40:02](https://youtu.be/8NURE3I4AJQ?t=2402) The slide is titled "Performance Metrics (ms)" and neither it nor the speech says what is timed (training, epoch or inference), and the speaker adds that the values are "not absolute".
- **−** [48:36](https://youtu.be/8NURE3I4AJQ?t=2916) Parity with PyTorch ("no difference") and "full native performance" are claimed without numbers, and raw-CUDA overhead was never measured.

**Depth 2/2**

- **+** [04:42](https://youtu.be/8NURE3I4AJQ?t=282) Each FFM feature is motivated against its JNI predecessor: jextract ends handwritten binding pairs, arenas end manual off-heap frees, OS loading ends hand-rolled library chains.
- **+** [42:10](https://youtu.be/8NURE3I4AJQ?t=2530) The heap-to-native-to-device copy path (traced at 13:14) is given as the reason data movement, not arithmetic, decides whether a GPU wins on small data.
- **+** [17:56](https://youtu.be/8NURE3I4AJQ?t=1076) The choice between assuming installed CUDA libraries (with matching jextract bindings) and bundling about 3 GB of them is weighed with the failure mode of each.

**Reusable 1/2**

- **+** [45:54](https://youtu.be/8NURE3I4AJQ?t=2754) Deep Netts was open-sourced two days before the talk, with examples and templates to start from.
- **−** [45:54](https://youtu.be/8NURE3I4AJQ?t=2754) The open-source Community Edition is the pure-Java engine; per deepnetts.com/pricing the Vector API and CUDA accelerators ship in the account-gated Free edition, so the artifact misses the talk's main content.
- **·** [37:53](https://youtu.be/8NURE3I4AJQ?t=2273) The enablement flags (`--add-modules jdk.incubator.vector`, `--enable-native-access`, `setUseVectorAPI`, `setUseCUDA`) are fragments to assemble yourself.
