---
title: Java and the Next Generation of Programming Models
talkId: "22916"
conference: devoxx-be-2026
speakers: [Ana-Maria Mihalceanu]
track: Java Language & Platform
sessionType: Conference
audienceLevel: ADVANCED
video: https://www.youtube.com/watch?v=kuUeHD_k5fs
durationMin: 40
slides: null
verdict: 8
frames: 9
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Java and the Next Generation of Programming Models
Ana-Maria Mihalceanu · Conference · Java Language & Platform

## TL;DR
Java's CPU-shaped programming model needs extending to reach AI runtimes that live outside the JVM. The talk shows two bridges: the Foreign Function and Memory API with jextract for calling native runtimes like ONNX, and Project Babylon's code reflection for writing a model directly in Java and lowering it to a foreign runtime.

## Key takeaways
- Reach a C-based inference runtime from Java by generating bindings with jextract from its C headers, resolving symbols as FFM downcall handles, and passing tensors as memory segments.
- Every ONNX operator can be mirrored as an `@Reflect`-annotated Java method, so a whole model graph becomes ordinary Java code that code reflection can inspect and transform.
- Code reflection targets a semantic tree (operations, bodies, blocks), not bytecode, because bytecode discards the structure a foreign runtime needs and is optimized only for the JVM.
- The Babylon ONNX prototype regenerates its operator bindings (obgen) and protobuf serialization (protogen) from the operator schema whenever the runtime version changes.
- FFM cuts the transfer overhead around inference (no unnecessary copies, explicit native lifetime), while HotSpot, intrinsics and the Vector API cover CPU-side execution efficiency.

## Notes

### [01:34](https://youtu.be/kuUeHD_k5fs?t=94) Framing: programming models, not features
A programming model is the set of abstractions through which a programmer, or their AI, expresses computation while hiding execution details. Java's model was shaped around the CPU, but AI inference is a capability embedded inside ordinary applications now, and it executes in a world outside the JVM.

### [04:38](https://youtu.be/kuUeHD_k5fs?t=278) How generative inference works
Each generated token repeats a pipeline: tokenization to IDs, embedding into dense vectors, transformer layers (attention plus feed-forward blocks) producing next-token logits, sampling (temperature and similar strategies), then decoding back to text or image. Almost all compute sits in the transformer step: a large repeated computational graph of tensor operations across layers, heads and tokens. Deep-learning weights ship in framework-specific formats (PyTorch, ONNX, GGUF), each with its own runtime, so Java faces an inference ecosystem outside the JVM.

### [08:14](https://youtu.be/kuUeHD_k5fs?t=494) Bridge one: FFM and jextract
Crossing the runtime boundary needs tensor and buffer movement without copying, plus control over memory layout. The pattern: run jextract over the runtime's C headers to generate Java bindings, load the native library, resolve symbols as downcall handles, pass memory segments, read return values, and explicitly destroy native objects, all from Java. ONNX is the worked example: LangChain4j uses it for in-process embeddings, and DJL plus Inference for J (transcript: "inference forj") build on it.

### [11:51](https://youtu.be/kuUeHD_k5fs?t=711) Demo one: local LLM inference through FFM
Live in the jextract samples: jextract (`compile.sh`, target package plus the GenAI `c_api.h` header) generates bindings for the ONNX GenAI runtime, with warnings for C constructs it cannot interpret that the demo does not need. A single Java class then runs token-by-token inference against a Phi-3 Mini 4K Instruct ONNX model from Hugging Face (max-length config set for the target), enabled with native access and the library path. Prompted to write a poem about Java, the model answers on the speaker's laptop.

### [18:06](https://youtu.be/kuUeHD_k5fs?t=1086) What the model binary contains
The ONNX file opened in Netron shows a large repeating graph. Metadata records the producing framework and format version, which matters for compatibility; nodes are operators transforming inputs to outputs, with protobuf-serialized tensors passed between them. The question for the second half: can that graph be expressed in Java and transformed into something the native library understands, even CUDA code?

### [20:46](https://youtu.be/kuUeHD_k5fs?t=1246) Bridge two: code reflection
Project Babylon's code reflection extends core reflection: Java code stays ordinary Java, but foreign runtimes can reflect on it and translate it into their own programming models. It is a JEP draft heading for incubation. Java becomes an intermediate representation: inspect and transform the code model, then hand it to a library that lowers it to ONNX, PyTorch or a GPU target.

### [23:21](https://youtu.be/kuUeHD_k5fs?t=1401) The ReLU example and code-model structure
ReLU, an activation function inside the shown graph, written in Java with `@Reflect` so its representation can be captured:

```java
// from slide at 23:30
@Reflect
public static float relu(float x) {
    return Math.max(0, x);
}
```

The code model is an immutable tree: the root of every model is an operation (variable declarations, arithmetic, method calls); a body is contained by an operation (here FuncOp); a block inside the body holds a sequence of operations with parameters and `%`-prefixed results consumed by later operations.

### [26:30](https://youtu.be/kuUeHD_k5fs?t=1590) The code reflection APIs
Access a method's FuncOp through core reflection, then traverse by streaming over elements, bodies, blocks and operations:

```java
// from slide at 26:40
codeModel.elements().forEach(
  (CodeElement<?, ?> e) -> {
    switch(e) {
      case VarOp varOp -> ...
    }
  }
);
```

Build new models with builders (every block needs a terminating operation that yields, exits or transfers control). Transform by traversing an input model and building a new one from it, optionally with rules, then passing it to a library for lowering. Bytecode is deliberately not the target: it is too low level, discards useful information and serves only the JVM.

### [29:05](https://youtu.be/kuUeHD_k5fs?t=1745) The Babylon ONNX prototype
Starting from the annotated ReLU, every ONNX operator becomes a Java method the transform recognizes. `obgen` regenerates the operator bindings from the operator schema on each runtime release; `protogen` generates the protobuf serialization classes used by the ONNX builder to emit a valid model binary. Together they form a Java ONNX-script library: low-overhead foreign access via FFM with the LLM represented in Java.

### [32:46](https://youtu.be/kuUeHD_k5fs?t=1966) Demo two: Llama expressed in Java
Live in the Project Babylon repository (`onnx` example): a Llama model in Java holds sampling constants, layer counts and weights initialized from the open-weights file in the constructor, with a 16-layer transformer loop. The `forward` method, annotated `@Reflect`, composes the generated ONNX operators (group-query attention, layer normalization, quantized matmuls) in under 200 lines and is what gets transformed into the foreign code model. Running it as a test with a "tell me a joke" prompt produces a generated joke. A summer side project reused the approach for an embedding model and tokenizer (a "modern BERT in front of an LLM" setup, demoed at the booth rather than on stage).

### [36:53](https://youtu.be/kuUeHD_k5fs?t=2213) Takeaways and outlook
FFM minimizes copy overhead and transfer inefficiency around native calls today; HotSpot JIT, intrinsics and the Vector API handle CPU execution efficiency. Code reflection extends this into new programming models while still coding in Java, with ONNX shown here and GPU offload (Juan Fumero's work) as the next step. More is promised toward JavaOne 2027. No audience questions followed; slides were to be uploaded to the event companion app.

## Tools, libraries and specs
- Foreign Function and Memory API (FFM, Java 25 LTS guide)
- jextract (early access, jdk.java.net/jextract, also via SDKMAN)
- Project Babylon code reflection (`@Reflect`, JEP draft, pre-incubation)
- ONNX Runtime and ONNX GenAI runtime (C API)
- Netron (model graph visualization)
- Phi-3 Mini 4K Instruct ONNX model (Hugging Face)
- LangChain4j, DJL, Inference for J (Java AI libraries using ONNX)
- Vector API, HotSpot JIT intrinsics

## Who should watch
Java developers embedding local inference or curious about Babylon gain the most, especially anyone weighing FFM against JNI-style glue. Viewers wanting GPU offload specifics or measured latency numbers should look to the follow-up work instead. Beginners to either Java internals or ML inference will find the pace steep.

## Verdict
**8/10**: Two live end-to-end demos, code-model internals and runnable examples earn it; the synthesis stays introductory and the latency claims carry no numbers.

**Novelty 1/2**

- **+** [10:18](https://youtu.be/kuUeHD_k5fs?t=618) The talk ties FFM, jextract and code reflection together around ONNX and credits LangChain4j, DJL and Inference for J as existing users of the runtime.
- **+** [29:05](https://youtu.be/kuUeHD_k5fs?t=1745) The obgen/protogen regeneration of operator bindings and protobuf classes on each ONNX runtime release is tooling the Babylon prototype adds.

**Demonstrated 2/2**

- **+** [16:33](https://youtu.be/kuUeHD_k5fs?t=993) jextract generates the ONNX GenAI bindings on the spot and the Java class then runs token-by-token inference on the laptop, answering the poem prompt.
- **+** [35:50](https://youtu.be/kuUeHD_k5fs?t=2150) The Babylon Llama test runs live and generates the joke from the model expressed in Java.

**Measured 1/2**

- **−** [37:24](https://youtu.be/kuUeHD_k5fs?t=2244) The closing claims reduced end-to-end latency and transfer inefficiency from FFM with no number, baseline or benchmark anywhere in the talk.
- **·** [34:17](https://youtu.be/kuUeHD_k5fs?t=2057) The only figure is the self-reported "less than 200 lines of code" for the Llama in Java, with no baseline.

**Depth 2/2**

- **+** [24:55](https://youtu.be/kuUeHD_k5fs?t=1495) The code-model anatomy (operations, bodies, blocks, parameters, `%` results) is explained at the level needed to debug a reflected LLM.
- **+** [28:04](https://youtu.be/kuUeHD_k5fs?t=1684) The choice of a semantic tree over bytecode is justified: bytecode is too low level, discards useful information and serves only the JVM.
- **−** [34:17](https://youtu.be/kuUeHD_k5fs?t=2057) The `forward` method is said to be transformed at compilation time into the ONNX model, but no step of that lowering is shown for the ReLU example or the Llama.

**Reusable 2/2**

- **+** [11:51](https://youtu.be/kuUeHD_k5fs?t=711) The first demo is the published jextract samples ONNX example, built with a `compile.sh` and runnable with the commands shown.
- **+** [31:44](https://youtu.be/kuUeHD_k5fs?t=1904) The second demo is the published Project Babylon `onnx` example, which the speaker says specifies everything needed to run it.
