---
title: "Quixotic: Pure Java Inference at Native Speed"
talkId: "14452"
conference: devoxx-be-2026
speakers: [Alfonso² Peterssen]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=S7x4DxwRnk4
durationMin: 48
slides: null
verdict: 9
frames: 11
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Quixotic: Pure Java Inference at Native Speed

Alfonso² Peterssen · Conference · Agentic Engineering & Tooling

## TL;DR

Peterssen presents jinfer, an open-source engine that runs LLMs and multimodal models inside the JVM with no Python, ONNX or mandatory native code, so data never leaves the process. Live benchmarks and slides show it matching llama.cpp on decode and beating it 2-4x on prefill on x86, with a pure Vector API mode that rivals C++ on GraalVM. The talk mixes working demos, a clear explanation of why prefill beats decode, and one-line LangChain4j and Spring AI integrations.

## Key takeaways

- Prefill and decode run the same computations in different orders; prefill is faster purely as a caching effect, because each weight matrix loads once instead of once per token.
- On CPU inference, decode saturates memory bandwidth with just a few threads, so prefill kernels are where an engine wins or loses.
- A full inference engine (17 model families, tokenizers, GGUF and safetensors loaders) fits in a ~3 MB jar with no mandatory dependencies.
- Q8_0 is the quantization to default to; lower quants run faster but can silently cost model capability.
- Only matrix multiplication needs native code for peak speed; everything else in jinfer runs on the Vector API, and a pure-Java fallback covers locked-down environments.
- System prompts can be pre-computed once and persisted to disk as a reusable cache, so applications pay prefill only for the user input.

## Notes

### [00:35](https://youtu.be/S7x4DxwRnk4?t=35) Mission: AI in a jar

Peterssen, a former GraalVM team member who previously presented llama2.java at this conference, frames the problem: JVM services reach AI through side processes, native libraries or paid network APIs, and data must leave the JVM. The Quixotic stack (jinfer engine plus jam kernels) loads GGUF and safetensors weights, ships its own tokenizers, and runs everything in-process. "AI in a jar" is literal: every component ships as jars.

### [04:43](https://youtu.be/S7x4DxwRnk4?t=283) The jinfer CLI in a 3.3 MB jar

A JBang-launched CLI chats with models, transcribes audio, synthesizes speech and serves an OpenAI-compatible endpoint. The whole CLI jar is 3.3 MB with no dependencies. A four-line JBang script pulls a model from Hugging Face, caches it locally and runs inference. A chat with Liquid AI's 350M model at Q8 runs on the laptop CPU at interactive speed. An audio-transcription demo stalls on venue Wi-Fi and is skipped.

### [09:57](https://youtu.be/S7x4DxwRnk4?t=597) Model and feature coverage

The jar implements 17 model families: Gemma 4, Qwen, LFM (Liquid AI), Mistral, Granite (IBM), MeluM (JetBrains), gpt-oss, Nemotron (NVIDIA) and others, across text, image, audio, video, speech recognition and speech synthesis, plus all common quantizations. The engine itself maps tokens to logits and adds tool calling, constrained generation, KV caching and MTP. It needs Java 25+, runs best on x86 servers, works under Native Image, and is weaker on Apple Silicon for now.

### [13:36](https://youtu.be/S7x4DxwRnk4?t=816) Local models are no longer toys

NVIDIA's Nemotron Cascade, a mixture-of-experts model paying only 3B active parameters per token, earned gold-medal scores in the math, IOI and ICPC olympiads. The point: small local models now handle non-trivial work, which is what makes CPU inference worth optimizing.

### [14:37](https://youtu.be/S7x4DxwRnk4?t=877) Why prefill beats decode

An LLM is a fixed sequence of simple ops mapping tokens to next-token probabilities. Prefill (prompt processing) and decode (token generation) perform the same computations; only the order differs, because decode must wait for each previous token. Decode streams every weight from memory once per token, while prefill multiplies each matrix by all input tokens at once. The same arithmetic explains the industry's ~5x cheaper input pricing.

### [18:49](https://youtu.be/S7x4DxwRnk4?t=1129) Live benchmark: one thread versus all threads

Using jinfer-bench (same conventions as llama-bench) on a Liquid model, all 8 laptop threads give 2761 tok/s prefill versus 142 tok/s decode (19x). With a single thread, prefill still wins 560 to 75 tok/s (7.4x), proving the gap is a caching effect rather than parallelism. On the speaker's workstation the ratio reaches 50x.

### [23:33](https://youtu.be/S7x4DxwRnk4?t=1413) jinfer versus llama.cpp

On an AMD Ryzen 9 9950X3D (16 threads, Q8_0, pp512/tg128), jinfer's prefill beats llama.cpp on every model shown: Qwen 3.5 9B 3.90x, LFM 2.5 1.2B 3.65x, Granite 4.2 8B 3.18x, Gemma 4 12B 3.16x, gpt-oss 20B 3.11x, Gemma 4 E2B 2.61x, Nemotron 30B-A3B 2.17x. Decode is tied (~1.0x), as expected for a memory-bound phase. Aggregated over 121 model-by-quant runs, the geometric mean is 1.89x prefill and 1.01x decode, driven by jam's hand-tuned AVX-512 VNNI matmul kernels. All data is published on qxotic.ai.

### [26:41](https://youtu.be/S7x4DxwRnk4?t=1601) The single native method

Every op except matrix multiplication matches native speed on the Vector API. Peak matmul needs instructions the Vector API cannot express, so jinfer has exactly one native method; environments that forbid native libraries swap jam-native for jam-vector and run pure Java. Attention, tokenizers and the remaining kernels stay on the Vector API at full speed.

### [28:51](https://youtu.be/S7x4DxwRnk4?t=1731) Pure Java against C++ at Q8_0

With Vector API only and 3x3-tiled matmul kernels at Q8_0 (pp512 tok/s), jinfer on GraalVM CE 25.4 beats llama.cpp on Qwen3.5-4B (278 vs 195) and trails by 7% and 13% on LFM2.5-2.6B (459 vs 494) and Gemma 4 E2B (535 vs 615); OpenJDK 27 trails on all three. A newer 4x4-tiled kernel became viable two weeks earlier when GraalVM open-sourced its compiler, and with it GraalVM beats llama.cpp on all three models (329 vs 195, 561 vs 494, 621 vs 615: +69%, +14%, +1%) while OpenJDK 27 drops to 150, 311 and 334.

### [31:31](https://youtu.be/S7x4DxwRnk4?t=1891) Speech and single-binary demos

Kokoro text-to-speech synthesizes the Peter Piper passage at 3.07x real time. A 16 MB Native Image binary embeds a tiny TTS model and memory-maps the weights from its own executable, needing no model files. NVIDIA Parakeet transcribes 15 minutes of the "stay hungry, stay foolish" speech in 8 seconds, and a real-time terminal transcription runs live on stage.

### [35:44](https://youtu.be/S7x4DxwRnk4?t=2144) LangChain4j and Spring AI integrations

Both integrations need three dependencies (BOM `com.qxotic:jinfer-bom:0.3.1`, Java 25): the provider, the model artifact, and jam-native or jam-vector at runtime. They implement chat, embeddings, reranking, text-to-speech and audio transcription, so switching an existing app to local inference means swapping the model class: no API key, no network, models cached from Hugging Face.

### [37:51](https://youtu.be/S7x4DxwRnk4?t=2271) Persistent prompt cache

Unlike llama.cpp's RAM-only cache, jinfer stores its token tree on disk with fine-grained resume points. Applications pre-warm the engine with system prompts, save the cache to a file, and reload it on startup; requests match the longest cached prefix and skip straight to generating. Peterssen calls this a prompt compiler.

### [39:55](https://youtu.be/S7x4DxwRnk4?t=2395) OpenAI server demo fails

The OpenAI-compatible server starts, but the speaker's Java coding agent cannot connect to it after several retries, so this route is abandoned live. The stated recommendation stands: embed the engine in the JVM rather than serving it over HTTP.

### [43:14](https://youtu.be/S7x4DxwRnk4?t=2594) Wrap-up and roadmap

Recap: current open model families supported, competitive-to-faster than llama.cpp, one Maven dependency, data stays in the JVM, integrations unofficial for now. Next target is shared-memory accelerators (Apple Silicon GPU, AMD Strix Halo) to lift prefill and decode without moving weights; discrete CUDA GPUs are explicitly out of scope.

### [45:26](https://youtu.be/S7x4DxwRnk4?t=2726) Backup: judge models and their bias

Backup slides describe turning any chat model into a judge model with tree-shaped attention that answers several questions in one prefill without cross-talk. A caveat follows: judge models inherit language-model bias, shown favoring 4 on a fair-die question, so their verdicts need calibration.

## Tools, libraries and specs

- jinfer 0.3.1 (engine, CLI, server; BOM `com.qxotic:jinfer-bom:0.3.1`), jam-native / jam-vector kernels
- qxotic.ai website and benchmarks; github.com/qxoticai/qxotic (open source)
- LangChain4j and Spring AI integrations (`jinfer-langchain4j`, `jinfer-models-all`)
- llama.cpp and llama-bench (baseline), jinfer-bench (same conventions)
- Models: Gemma 4, Qwen3/Qwen 3.5, LFM 2.5, Granite 4.2, gpt-oss 20B, Nemotron 30B-A3B / Cascade, Kokoro TTS, Parakeet STT, MeluM, JBang, Hugging Face model hub
- Java 25+, Vector API, GraalVM CE 25.4 / Native Image, OpenJDK 27, AVX-512 VNNI

## Who should watch

Java developers evaluating local or sovereign AI (regulated industries, offline products) and performance engineers curious how far the Vector API and GraalVM go against hand-tuned C++. Viewers wanting GPU serving, CUDA optimization or LangChain4j/Spring AI tutorials should look elsewhere.

## Verdict

**9/10**: The author's own 121-run benchmark against llama.cpp, a reasoned one-native-method design and a public repository to reproduce it; held back by the pure-Java claim and several features reaching the audience only as slides or failed demos.

**Novelty 2/2**

- **+** [25:10](https://youtu.be/S7x4DxwRnk4?t=1510) The author's head-to-head against llama.cpp covers 121 model-by-quant runs, with per-model speedups on the [24:10](https://youtu.be/S7x4DxwRnk4?t=1450) slide.
- **+** [26:41](https://youtu.be/S7x4DxwRnk4?t=1601) The single-native-method design and the Vector API fallback come with the rationale of the person who built both.
- **+** [29:54](https://youtu.be/S7x4DxwRnk4?t=1794) A 4x4-tiled kernel became viable on GraalVM two weeks before the talk, when Graal open-sourced its compiler, and the speaker shows the effect on each model.

**Demonstrated 1/2**

- **+** [18:49](https://youtu.be/S7x4DxwRnk4?t=1129) jinfer-bench runs live with visible output on all threads and on one thread, giving 2761 versus 142 tok/s and 560 versus 75 tok/s.
- **−** [28:51](https://youtu.be/S7x4DxwRnk4?t=1731) The pure-Java (Vector API only) result appears as a chart, and no demo names the kernel backend it ran on.
- **−** [39:55](https://youtu.be/S7x4DxwRnk4?t=2395) The OpenAI-compatible server starts but the coding agent never connects, and the demo is abandoned.

**Measured 2/2**

- **+** [24:10](https://youtu.be/S7x4DxwRnk4?t=1450) Prefill speedups of 2.17x to 3.90x over llama.cpp name the models, Q8_0 weights, pp512/tg128, CPU and thread count; decode ties at about 1.0x.
- **+** [30:30](https://youtu.be/S7x4DxwRnk4?t=1830) The pure-Java chart shows 3x3 and 4x4 kernels on OpenJDK 27 and GraalVM CE 25.4 against llama.cpp per model: 329 versus 195, 561 versus 494 and 621 versus 615 tok/s with 4x4 on GraalVM.
- **−** [22:27](https://youtu.be/S7x4DxwRnk4?t=1347) The 50x prefill ratio on the speaker's workstation and the 100x on a GPU are stated with no run or number shown.

**Depth 2/2**

- **+** [21:56](https://youtu.be/S7x4DxwRnk4?t=1316) The single-thread experiment and the weight-streaming explanation show that prefill beats decode as a caching effect on identical computations.
- **+** [26:41](https://youtu.be/S7x4DxwRnk4?t=1601) The native-versus-Vector-API split is justified op by op: only matrix multiplication needs instructions the Vector API cannot express.
- **+** [29:23](https://youtu.be/S7x4DxwRnk4?t=1763) Tile size, register pressure and compiler spilling explain why the 4x4 kernel regresses on OpenJDK and wins on GraalVM.

**Reusable 2/2**

- **+** [44:50](https://youtu.be/S7x4DxwRnk4?t=2690) The closing slide points to github.com/qxoticai/qxotic and qxotic.ai, which hold the engine, examples and benchmarks.
- **+** [36:20](https://youtu.be/S7x4DxwRnk4?t=2180) The LangChain4j setup slide names the Maven coordinates and BOM version 0.3.1 needed to try the integration.
