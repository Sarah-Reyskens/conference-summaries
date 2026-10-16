---
title: "Reflect, Transform, Accelerate: Bringing GPU Computing to Java"
talkId: "21657"
conference: devoxx-be-2026
speakers: [Juan Fumero]
track: Java Language & Platform
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=0-1IGpVrFLQ
durationMin: 50
slides: null
verdict: 7
reach: niche
frames: 11
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Reflect, Transform, Accelerate: Bringing GPU Computing to Java

Juan Fumero · Conference · Java Language & Platform

## TL;DR

OpenJDK Project Babylon adds code reflection plus HAT (Heterogeneous Accelerator Toolkit), which reflects on Java methods, transforms them, and JIT-compiles them to GPU code at runtime. Fumero argues every GPU programming model trades off performance, portability, and productivity, then walks HAT's three APIs (SIMT, tensor, tile) from a naive kernel to within 84% of native cuBLAS, all from portable Java.

## Key takeaways

- HAT reflects on `@Reflect`-annotated Java methods at runtime and generates OpenCL or CUDA per GPU backend, so one Java source runs on Nvidia, Apple, AMD, and Intel GPUs.
- Judge a GPU programming model on three axes (performance, functional plus performance portability, productivity); pushing one axis to the peak usually costs the others.
- A naive HAT matrix multiply is 12 lines but ~7x off native; matching cuBLAS with the SIMT model takes 100+ lines of shared-memory and register-tiling tricks most Java developers should never write.
- The tensor and tile APIs recover the performance without the complexity: a few lines of `Tensor.load16`/`mma` or tile code reaches 78 µs versus 66 µs for cuBLAS FP16 on an RTX 5060.
- When GPU performance plateaus, profile with NVIDIA Nsight Compute: a memory-section hint about shared-store bank conflicts led to adding swizzling, which closed most of the gap to Python cuTILE past 2k matrices.

## Notes

### [02:40](https://youtu.be/0-1IGpVrFLQ?t=160) Live demo: LLM inference in pure Java on the GPU

Fumero opens with a vibe-coded LLaMA inference app written entirely in portable HAT Java, run live on a MacBook with `btop` showing CPU idle and GPU busy. It generates ~140 tokens/second (quantized QMAX11 build, 174-token prompt), launches around 84,000 GPU kernels for the prompt, and HAT flags print the generated OpenCL (matmul, flash attention, RMS norm) plus the GPU used (Apple M4 Max). The whole transformer runs on the GPU. Reported numbers: 140 tok/s on the M4 Max versus ~14 tok/s for a Java parallel version, and up to 160 tok/s on an RTX 5060. Training and fine-tuning also work; the demo is not yet published.

### [08:58](https://youtu.be/0-1IGpVrFLQ?t=538) Two ways to reach a GPU from Java

With a stock JDK the options are Panama FFI against prebuilt native libraries (best performance, vendor lock-in) or JIT compilation: detect offloadable code at runtime and generate GPU-suitable code, which is the HAT path. The pipeline is Java source, an engine that reflects and transforms it to CUDA/OpenCL source or binary, then the GPU driver's compiler producing the final binary, with data marshalled to the device (discrete GPUs need explicit transfer; unified-memory machines like the Mac do not).

### [12:07](https://youtu.be/0-1IGpVrFLQ?t=727) A triangle for judging parallel APIs

Fumero borrows a framework from a parallel-patterns book: rate each model on performance, portability (functional: same code runs everywhere; performance: it runs acceptably everywhere), and productivity (tooling, debuggers, profilers). CUDA C++ maximizes performance at the cost of portability and productivity; OpenCL stretches portability; plain Java maximizes portability and productivity. HAT's goal is to stretch all three edges at once.

### [17:23](https://youtu.be/0-1IGpVrFLQ?t=1043) Code reflection in brief

`javac` lowers source through a verbose AST to compact bytecode, losing control flow and some types. Code reflection adds a layer in between: annotating a method with `@Reflect` makes the compiler keep a code model with names, structure, and types preserved, which tools can then reflect on and transform (the example fuses a multiply-add into an FMA op). Earlier projects (TornadoVM, Aparapi, Sumatra) worked from bytecode; the code model makes the same tasks simpler as a JDK building block.

### [20:28](https://youtu.be/0-1IGpVrFLQ?t=1228) HAT stack and the SIMT thread model

HAT sits on the JVM above CPU and accelerators, with CUDA, OpenCL, and Java backends (the Java backend enables debugging and future Vector API use) and three APIs: SIMT, tensor, tile. The SIMT model maps one loop iteration to one GPU thread: a vector multiply becomes a per-thread method using `GIDX`/`GIDY`/`GIDZ` intrinsics for the thread index in each grid dimension, guarded by a bounds check, launched with as many threads as input elements.

### [26:10](https://youtu.be/0-1IGpVrFLQ?t=1570) Kernel, compute, and application layers

HAT code has three layers: the kernel method that runs on the GPU (restricted Java: no reflection, inheritance allowed, mainly for performance), the compute layer that builds a dispatch graph over one or many kernels with an `NDRange` declaring the 1D/2D/3D thread count (the LLaMA demo offloads ~10 kernels per layer over 16 layers per token), and the plain-Java application layer that creates an accelerator, attaches data, and calls compute.

### [29:19](https://youtu.be/0-1IGpVrFLQ?t=1759) Matrix-multiply performance study

Using matrix multiply (the dominant LLM cost) with kernel times from NVIDIA Nsight Compute on an RTX 5060: multithreaded Java takes ~300 ms, naive HAT ~2000 µs (150x faster), tuned HAT FP32 295 µs versus cuBLAS FP32 203 µs, and HAT FP16 ~220 µs versus cuBLAS FP16 66 µs. The catch is visible on screen: the naive kernel is 12 lines at ~1 TFLOP/s while the near-native one is 100+ lines of shared memory, register tiling, and private memory at 7.3 TFLOP/s. Full details are in a Babylon article on optimizing GPU matmul.

### [34:02](https://youtu.be/0-1IGpVrFLQ?t=2042) Tensor API: productivity back

Matrix-multiply speed needs tensor instructions (Nvidia WMMA/fragment, Intel XMX, AMD WMMA). HAT's tensor API expresses tiling directly: define a shape, zero an accumulator, loop over tiles loading A/B with `Tensor.load16`, accumulate with `Tensor.mma`, store. On backends without tensor support (OpenCL 1.2 on Mac) HAT expands tensors to private arrays plus loop unrolling, giving ~8-10x over parallel streams while keeping the same source. On the 5060 the tensor version runs in 274 µs with far fewer lines than the tuned SIMT code, trading a little performance for large gains in portability and productivity.

### [39:52](https://youtu.be/0-1IGpVrFLQ?t=2392) Tile API: matching Python cuTILE

Nvidia's cuTILE (under a year old, inspired by Triton and Gluon) generalizes tensors to more operations. The HAT tile API mirrors the tensor code but dispatches work per tile instead of per thread. On 1k matrices: HAT SIMT best 218 µs, Python cuTILE 77 µs, HAT-Tile 78 µs, cuBLAS FP16 66 µs, so Java lands within 84% of native and matches Python. A TFLOP/s sweep from 512 to 8k shows HAT-Tile tracking cuTILE until ~2k, then falling behind.

### [42:29](https://youtu.be/0-1IGpVrFLQ?t=2549) Debugging the post-2k gap with Nsight

Comparing Nsight Compute profiles, HAT-Tile shows lower compute utilization and higher memory saturation than Python cuTILE; the memory section flags suboptimal shared-store access with bank conflicts. The Python SDK sample avoids them with swizzling, so Fumero adds a swizzle index remap to the HAT compute and the new version nearly matches cuTILE (a small gap remains and is being investigated with Nvidia). The conclusion slide reports up to 35 TFLOP/s and 87% of cuBLAS. The lesson drawn: constraining the domain (a tile sub-domain inside the GPU domain) buys performance, portability, and productivity together.

### [48:58](https://youtu.be/0-1IGpVrFLQ?t=2938) Q&A: scaling to large multi-kernel programs

Asked about scaling to complex frameworks, Fumero says the first HAT LLaMA port ran at 0.6 tok/s and needed guided fusion work (combining kernels, avoiding data movement) via an AI assistant to reach the demoed speed. He sees AI assistants as the practical route for the AI space, with programmer knowledge of the system still necessary.

## Tools, libraries and specs

- OpenJDK Project Babylon (code reflection, `@Reflect`) and HAT (Heterogeneous Accelerator Toolkit): SIMT, tensor, and tile APIs; CUDA, OpenCL, and Java backends
- NVIDIA Nsight Compute and Nsight Systems (kernel profiling that found the bank conflicts)
- cuBLAS, Python cuTILE / cuTILE C++, Triton, Gluon (comparison points)
- Tensor instructions: Nvidia WMMA/fragment API, Intel XMX, AMD WMMA
- JDK 27, Panama FFI, Java Vector API, OpenCL 1.2, CUDA 13.3, `btop`
- HAT-LLaMA inference demo (unpublished; ask at the Oracle booth), Babylon matmul article (openjdk.org/projects/babylon/articles/hat-matmul/hat-matmul)

## Who should watch

Java developers curious about GPU acceleration without learning CUDA, and anyone tracking Project Babylon or Java for AI workloads. Skip it if you already follow HAT development closely or want Code Reflection API details (those belong to the companion session by Fumero's colleague).

## Verdict

**7/10**: Portable Java within 84% of cuBLAS FP16 on an RTX 5060 is measured with its setup and explained down to the Nsight-found bank conflicts; the core is the speaker's own published HAT material, only the LLaMA run is shown live, and the repository is the project's own.

**Reach niche**: only developers already doing GPU work from Java can put the kernel-level HAT content to use within a year.

**Novelty 1/2**

- **+** [48:58](https://youtu.be/0-1IGpVrFLQ?t=2938) The first HAT LLaMA port ran at 0.6 tok/s and needed guided kernel fusion through an AI assistant to reach the demoed speed, with programmer system knowledge still necessary.
- **+** [46:10](https://youtu.be/0-1IGpVrFLQ?t=2770) The three HAT APIs are placed side by side on the performance-portability-productivity triangle taken from a parallel-patterns book the speaker credits, so the shape identifies which model is in use.
- **−** The API walk-through and the matmul progression are covered by the Babylon article "Optimizing GPU Programs from Java using Babylon and HAT" and the HAT README, both written by the project's authors.

**Demonstrated 1/2**

- **+** [04:14](https://youtu.be/0-1IGpVrFLQ?t=254) The LLaMA demo generates text live at ~140 tok/s with the btop GPU monitor visible on screen.
- **+** [04:47](https://youtu.be/0-1IGpVrFLQ?t=287) HAT prints the emitted OpenCL kernels for the whole transformer and then the detected Apple M4 GPU, so the run's output is shown.
- **−** [36:40](https://youtu.be/0-1IGpVrFLQ?t=2200) The tensor and tile code appears only as slides and its results as charts, so the near-native performance claim the talk is built on is never run on stage.

**Measured 2/2**

- **+** [41:26](https://youtu.be/0-1IGpVrFLQ?t=2486) The 1k-matmul chart states setup (RTX 5060, driver 610.57.04, CUDA 13.3) with HAT-Tile 78 µs against cuBLAS FP16 66 µs and Python cuTILE 77 µs.
- **+** [30:54](https://youtu.be/0-1IGpVrFLQ?t=1854) Nsight Compute kernel times compare Java (~300 ms), naive HAT (~2000 µs), tuned HAT and cuBLAS with the method named, and the speaker states the tuned SIMT build is still 3x off cuBLAS FP16 [31:57](https://youtu.be/0-1IGpVrFLQ?t=1917).
- **−** [06:22](https://youtu.be/0-1IGpVrFLQ?t=382) The 140-vs-14 tok/s CPU baseline is admitted unoptimized, so that particular gap overstates the speedup.

**Depth 2/2**

- **+** [42:29](https://youtu.be/0-1IGpVrFLQ?t=2549) The post-2k regression is root-caused through Nsight profiles to shared-store bank conflicts and fixed with swizzling.
- **+** [37:42](https://youtu.be/0-1IGpVrFLQ?t=2262) On OpenCL 1.2 (Mac) HAT expands tensors to private arrays and loop tiling under the hood, so the same Java source runs without tensor hardware.
- **+** [45:38](https://youtu.be/0-1IGpVrFLQ?t=2738) The tile speedup is framed as a deliberate trade-off: a constrained sub-domain that buys all three triangle axes at once.

**Reusable 1/2**

- **+** [29:49](https://youtu.be/0-1IGpVrFLQ?t=1789) The matmul study points to a published Babylon article with the full numbers and process.
- **·** [48:14](https://youtu.be/0-1IGpVrFLQ?t=2894) The conclusion slide links github.com/openjdk/babylon, the presented project's own repository, as the getting-started point.
- **−** [05:51](https://youtu.be/0-1IGpVrFLQ?t=351) The opening LLaMA demo, with its web interface and benchmark engine, is unpublished and available only by asking at the Oracle booth.
