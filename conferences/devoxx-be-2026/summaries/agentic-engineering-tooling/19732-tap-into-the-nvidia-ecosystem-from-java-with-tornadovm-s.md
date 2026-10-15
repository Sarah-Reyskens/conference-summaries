---
title: "Tap into the NVIDIA Ecosystem from Java with TornadoVM's Hybrid API"
talkId: "19732"
conference: devoxx-be-2026
speakers: [Thanos Stratikopoulos, Michalis Papadimitriou, Mary Xekalaki]
track: Agentic Engineering & Tooling
sessionType: Tools-in-Action
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=6SPnBmQrYEk
durationMin: 27
slides: null
verdict: 10
frames: 8
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Tap into the NVIDIA Ecosystem from Java with TornadoVM's Hybrid API

Michalis Papadimitriou, Mary Xekalaki · Tools-in-Action · Agentic Engineering & Tooling

## TL;DR

TornadoVM's Hybrid API lets Java developers mix JIT-compiled GPU kernels with direct calls to NVIDIA libraries (cuBLAS, cuFFT, cuDNN, cuDF) inside one TaskGraph, shipped as a plain Maven jar with no JNI. The talk walks through the four programming APIs and backs them with live demos: a signal filter, a GEMM ladder against cuBLAS, a Java LLM inference engine, and a GPU-accelerated Flink query reaching 17.4x over vanilla Flink.

## Key takeaways

- A `LibraryTask` calls NVIDIA library functions from Java through a one-to-one mapping of the NVIDIA C API, sharing TornadoVM-managed FFM device buffers with JIT kernels so data stays on the GPU between stages.
- Chaining library tasks with custom JIT tasks in a single TaskGraph covers the realistic case: use the vendor library where it exists, write your own kernel for the glue (filtering, normalization) around it.
- The new TileContext API expresses tiled GPU compute in compact Java and reached about 90% of cuBLAS throughput on FP16 GEMM (125 vs 146.5 TFLOP/s), slightly beating a hand-optimized KernelContext kernel on the same problem.
- GPU acceleration can be bolted onto existing frameworks transparently: the Flink integration accelerates a standard SQL query behind a config flag, no query rewrite.
- Development loop stays local and portable: write once on a laptop (OpenCL/Metal), deploy to CUDA servers; profile with JFR plus Nsight Systems, and bridge them with TornadoVM's Pulse/Insight tools.

## Notes

### [01:07](https://youtu.be/6SPnBmQrYEk?t=67) Why Java needs the NVIDIA ecosystem

Java runs the enterprise side (microservices, Flink, Spark, Cassandra, LangChain4j, Spring AI) while NVIDIA owns accelerated compute (linear algebra, vector search, data frames, FFT). Reaching that compute from Java has meant a Python sidecar, JNI/FFM bindings, or rewriting hot paths in C++. The Hybrid API ships as a Maven jar that imports like any other Java library.

### [03:41](https://youtu.be/6SPnBmQrYEk?t=221) TornadoVM in one minute

TornadoVM is a decade-old GPU programming framework for JDK 21+ distributions (OpenJDK, GraalVM, Temurin, Zulu). It JIT-compiles parallel Java to CUDA, OpenCL, or Metal at runtime, aiming at write-once-run-anywhere with tuning at deploy time. SDKs install via SDKMAN; integrations exist for Quarkus, LangChain4j, Flink, and Spring AI.

### [06:17](https://youtu.be/6SPnBmQrYEk?t=377) Four ways to program an NVIDIA GPU

Parallel API: a `@Parallel` loop annotation as a parallelization hint for the compiler. KernelContext: full GPU-programmer control from Java (thread/block ids, atomics, local memory, tensor-core fragments) for hand-tuned kernels. TileContext: the newest level, aligned with NVIDIA's CUDA Tiles model, where the developer thinks in data layouts and the compiler handles threads and prefetching. LibraryTask: direct calls into CUDA libraries. The point is composing all four in one application.

### [09:25](https://youtu.be/6SPnBmQrYEk?t=565) Anatomy of a library task

A task carries a name (used by the runtime to optimize data movement across chained tasks), a provider such as cuFFT, the specific function (e.g. forward R2C), FFM-based input/output buffers, and the function's arguments. Signatures mirror the NVIDIA documentation one-to-one, so porting a C call is mechanical. A TaskGraph example chains transfer-to-device, a forward FFT library task, a custom low-pass JIT kernel, an inverse FFT library task, and a normalize JIT kernel. Runtime features exposed for IO tuning include async staged transfers, grid scheduling, multi-stream execution, and CUDA graphs.

### [12:34](https://youtu.be/6SPnBmQrYEk?t=754) Demo: low-pass signal filter

The filter application ran live: a distorted input signal plus its spectrum on top, the smoothed output accumulating below as the spectrum passed through the chain of library and JIT tasks. The actual Java source was shown alongside: library tasks with the custom filter and normalization attached between them.

### [14:39](https://youtu.be/6SPnBmQrYEk?t=879) Tile ladder: three APIs, one GEMM, profiled

The same matrix computation was expressed three ways: manual KernelContext with fragments and unrolling, compact TileContext, and a direct cuBLAS call. The `tile-ladder` Java class ran all variants under Nsight Systems: cuBLAS fastest, with TileContext and the hand-optimized kernel close behind. A backup slide gives numbers for FP16 GEMM with FP32 accumulate at n = 2048 on an RTX 4090 (TornadoVM 7.0.0): cuBLAS 146.5 TFLOP/s, Tile 128x128x64 with hint 125.0, hand-optimized KernelContext 119.5. Tile shape alone moved throughput 5.6x; knowing extents at JIT time beat native CUDA Tile with runtime n by 4.5x.

### [17:44](https://youtu.be/6SPnBmQrYEk?t=1064) jitLLM: an inference engine in Java on the GPU

The team built a full LLM inference engine (jitLLM) in Java on the TornadoVM backend, running Llama 4 and Qwen3 models up to 27B parameters with a mix of JIT kernels and cuBLAS/cuDNN calls. The live demo prompted a 4B model to generate a TornadoVM kernel, compiled it with javac, JIT-compiled it to CUDA, and ran it on the same RTX 4090 via tool calling, with GPU output matching CPU on 99.87% of 786,432 Mandelbrot pixels. Prefill beats llama.cpp by about 12% in some cases; larger models reach 90 to 95% of llama.cpp throughput, up from roughly 30x slower a year ago.

### [20:51](https://youtu.be/6SPnBmQrYEk?t=1251) Accelerating Apache Flink with cuDF

 A developer writes a standard Flink SQL/Table API query and sets a config flag. At the task manager, a provider library analyzes the query IR: operations it recognizes become library tasks (cuDF for Parquet reads and regex matching), the rest become JIT tasks, all in one TaskGraph. The demo screened log lines against eight regexes: the Flink dashboard showed the unmodified application running, and the task executor log showed the generated TornadoVM bytecode (Parquet read, contains, generated code). On 64M log lines, one GPU at parallelism 1 ran 17.43x faster than vanilla Flink at parallelism 1 end to end (8.1 s vs 142 s; 5.26x against vanilla at 4 slots). Setup: RTX 4070 laptop, CUDA 12.5, JDK 21, Flink 2.3.0, median of 3 runs.

### [25:02](https://youtu.be/6SPnBmQrYEk?t=1502) Takeaways and resources

Recap: code generation reaches about 98% kernel-time parity with equivalent hand-written CUDA, Cassandra/JVector graph builds run 90x faster on a local GPU. Everything is on GitHub: TornadoVM, jitLLM, the talk's demos (mikepapadim/tornadovm-devoxx2026-cuda-demos), the Flink accelerator, plus the SDKMAN SDK.

## Tools, libraries and specs

- TornadoVM 7.0.0 (Hybrid API: Parallel, KernelContext, TileContext, LibraryTask; Maven Central; SDKMAN; JDK 21+)
- NVIDIA libraries: cuBLAS (GemmEx), cuFFT (R2C), cuDNN, cuDF, CUDA Graphs, Nsight Systems (nsys)
- jitLLM (github.com/beehive-lab/jitllm): Java LLM inference on TornadoVM; Llama 4, Qwen3 up to 27B
- Apache Flink 2.3.0 with flink-accelerator-tornadovm (cuDF Parquet read + regex)
- Profiling: JFR, Nsight Systems, TornadoVM Pulse and Insight
- Frameworks named: LangChain4j, Spring AI, Quarkus, Apache Cassandra with JVector, Elasticsearch

## Who should watch

Java developers curious about GPU acceleration without leaving the JVM, and anyone running Flink, vector search, or local LLM inference who wants measured numbers for the GPU path. Skip it if you want TornadoVM compiler internals (deferred to the team's deep-dive talks) or a general CUDA tutorial.

## Verdict

**10/10**: Four working GPU demos, the authors' comparative benchmarks, a task-composition mental model and published example repositories meet the five criteria, with uneven support for the closing performance claims and extra setup for Flink.

**Novelty 2/2**

- **+** [17:13](https://youtu.be/6SPnBmQrYEk?t=1033) The speakers compare their TileContext and hand-tuned KernelContext GEMM implementations against cuBLAS on the same RTX 4090.
- **+** [23:58](https://youtu.be/6SPnBmQrYEk?t=1438) The authors' Flink measurements compare GPU execution with vanilla Flink at three parallelism levels on two dataset sizes.

**Demonstrated 2/2**

- **+** [12:34](https://youtu.be/6SPnBmQrYEk?t=754) The low-pass filter runs its library/JIT chain beside the Java source and reaches PASSED, and [16:12](https://youtu.be/6SPnBmQrYEk?t=972) the GEMM ladder shows the variants executing under Nsight Systems.
- **+** [19:18](https://youtu.be/6SPnBmQrYEk?t=1158) jitLLM generates a Java GPU kernel, compiles and executes it on the same GPU, with the output reporting PASSED and a 99.87% GPU/CPU pixel match.
- **+** [22:56](https://youtu.be/6SPnBmQrYEk?t=1376) The Flink query runs to completion in the dashboard and its task-executor log shows the generated library and JIT tasks.

**Measured 2/2**

- **+** [17:13](https://youtu.be/6SPnBmQrYEk?t=1033) The GEMM chart states workload, GPU, tool and version for cuBLAS/TileContext/KernelContext throughput of 146.5/125.0/119.5 TFLOP/s, while [13:20](https://youtu.be/6SPnBmQrYEk?t=800) the filter compares plain execution at 63.3 µs with CUDA graphs at 38.9 µs using medians of 300 executions each.
- **+** [23:58](https://youtu.be/6SPnBmQrYEk?t=1438) The Flink chart gives hardware, versions and end-to-end comparisons for 16M and 64M log lines, including 8.1 s versus 142 s at parallelism 1, although it compares a device median of three runs with a vanilla mean of two.
- **−** [19:49](https://youtu.be/6SPnBmQrYEk?t=1189) The llama.cpp throughput claims, [25:02](https://youtu.be/6SPnBmQrYEk?t=1502) 90x graph-build speedup and [25:36](https://youtu.be/6SPnBmQrYEk?t=1536) 98% CUDA kernel-time parity lack the workload and measurement setup needed to assess them.

**Depth 2/2**

- **+** [09:25](https://youtu.be/6SPnBmQrYEk?t=565) Named tasks let the runtime reason about data movement across a chain, and the FFT/filter/normalization example explains when to combine vendor libraries with custom Java kernels.
- **+** [12:01](https://youtu.be/6SPnBmQrYEk?t=721) The runtime-feature discussion separates compute from IO overhead and identifies staged transfers, grid scheduling, CUDA graphs and multiple streams as tuning controls.
- **+** [21:24](https://youtu.be/6SPnBmQrYEk?t=1284) The Flink provider analyzes the query IR and selects library tasks for supported operations or JIT tasks for the remaining work inside one TaskGraph.

**Reusable 2/2**

- **+** [26:06](https://youtu.be/6SPnBmQrYEk?t=1566) The closing resources point to the talk's demos repository and jitLLM, alongside the TornadoVM and Flink accelerator repositories, covering the main examples with published code.
- **+** [08:53](https://youtu.be/6SPnBmQrYEk?t=533) The Hybrid API abstraction ships as a Maven jar, and the SDKMAN distribution supplies an installation route for the core TornadoVM examples.
- **−** [20:51](https://youtu.be/6SPnBmQrYEk?t=1251) Reproducing the Flink path requires the unreleased gpu-offload branch and a locally built TornadoVM development version, rather than only the configuration flag described here.
