---
title: Run Frontier Open Models on consumer hardware
talkId: "31454"
conference: devoxx-be-2026
speakers: [Prince Canuma]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=DseVLPC4Qjs
durationMin: 50
slides: null
verdict: 8
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Run Frontier Open Models on consumer hardware
Prince Canuma · Conference · Agentic Engineering & Tooling

## TL;DR
Running a model on a Mac is easy; serving it fast, alongside an OS and other apps, takes an engine built for unified memory. The speaker demonstrates his open-source MLX-VLM engine and the Nativ Mac app running voice, chat, and coding agents entirely on device, with benchmark charts to back the speed claims. Viewers leave with a sizing mental model (bandwidth over model size) and a concrete stack to try locally.

## Key takeaways
- Estimate on-device speed as memory bandwidth divided by model size, since decode is memory-bound; buy the device against that number before anything else.
- Serve several users or agents from one Mac with continuous batching (admit requests mid-generation) instead of static batching, which serializes them.
- Compress the KV cache (his TurboQuant) to reach long contexts locally; he cites up to a million tokens on device.
- Pair a small draft model with the main model for verification (speculative decoding) for speedups around 3x.
- Validate a ported model against its PyTorch reference on long prompts, not just short ones, because engine-level errors accumulate with context length.
- Cap reasoning output (a token budget, or reasoning off) when a small local model spirals into repetition loops.

## Notes

### [00:35](https://youtu.be/DseVLPC4Qjs?t=35) The three knobs of local AI
Local inference trades accuracy, latency, and memory against each other: quantization cuts latency and memory by making the model dumber, though modern techniques keep quality close to full precision. Speculative decoding adds a fourth lever, with a small model drafting tokens for the large model to verify, worth about 3x. Badly done quantization hides accuracy problems behind good-looking evals, which motivates doing the porting carefully.

### [03:41](https://youtu.be/DseVLPC4Qjs?t=221) Unified memory and memory-bound decode
Since the M1 (2020), Apple Silicon shares one memory plane between CPU and GPU, so nothing moves between separate pools and one optimization benefits Mac, iPhone, and iPad. On-device models fight the OS, Chrome, and Cursor for fixed memory that cannot be upgraded after purchase. For sizing, he gives a simple relation: expected tokens per second ≈ memory bandwidth / model size (quantized or not), which tells you what hardware a target speed needs.

### [06:49](https://youtu.be/DseVLPC4Qjs?t=409) Continuous batching for many users and agents
Static batching finishes one request before starting the next; continuous batching admits new requests mid-generation, so one Mac Studio can serve many users, or voice plus text plus vision at once, or several sub-agents in parallel. His scheduler decides what to admit to memory, when, and how to prefill without stalling live requests, and throttles load (swap) before quality collapses.

### [08:21](https://youtu.be/DseVLPC4Qjs?t=501) The MLX-VLM engine
MLX-VLM started with vision-language models and is now omni (any input in, any output out: video, image, text, documents, code, generated media). The stack: continuous batching, TurboQuant KV-cache compression, speculative decoding, and support grown from 100 to 5,000 models on Apple devices. It installs as a Python package with a one-script inference example and a local server mode; a Swift SDK for native apps was announced for that week.

### [12:28](https://youtu.be/DseVLPC4Qjs?t=748) Nativ live demo
Nativ is the Mac app on top of the engine, downloaded as a DMG from his GitHub (account Blaizzy). With Wi-Fi off, he dictates voice input anywhere in the OS, chats with CohereLabs North Mini Code (~19 GB) at a stated ~90 tokens/s, and shows a dashboard of ~20M tokens generated on device in 50 days. He then has the local model build a chat website over a localhost endpoint, iterates on its layout in conversation, and shows earlier one-shot builds: a 3D animation and games with Qwen 27B. Scheduled tasks, GitHub PR review via MCP, and project workspaces with their own terminal round out the tour; installing the Pi and Codex CLI harnesses failed on the venue network.

### [24:10](https://youtu.be/DseVLPC4Qjs?t=1450) Repo Meter and agent-built side projects
Vibe-coded contributions had grown his engine's tests to 86,000 lines across 106 files inside a 300,000-line codebase, so he built Repo Meter (deployed, then run locally) to map where the lines lived. Guided by it, he cut tests to 22,000 lines, one test-model file from 20,000 lines to 1,000 with the same coverage, and 100 files to 16. He also demos in-browser editing (retagging a section, recoloring a button, converting page HTML to Markdown) executed by the local agent.

### [30:30](https://youtu.be/DseVLPC4Qjs?t=1830) Extensions, artifacts, and local image generation
The audio features are a prebuilt extension; anyone can add capabilities with a few JSON files declaring permissions (microphone, system audio for meeting capture). Artifacts collect locally generated images and documents, including a car image generated on the device; current image models named are Qwen Image. Releases ship weekly (Monday stable, Friday beta).

### [34:40](https://youtu.be/DseVLPC4Qjs?t=2080) Unlearning cloud habits
On device, maximize what fits rather than batch size (he runs at most four parallel agents before losing track), optimize for concurrency across mixed models instead of batch-of-one FLOPS, and tune per chip generation (M1 through M5) rather than per rack. Activity Monitor shows Nativ taking little CPU while Chrome and other apps run; GPU memory reads ~25 GB for the model plus context on a ~40 GB total footprint. Large prompts are cached to disk, making reloads up to 100x faster.

### [39:22](https://youtu.be/DseVLPC4Qjs?t=2362) Q&A: business model, PC, M1, doom loops
The engine stays open source (closing it would kill adoption, currently a cited 7.5M); Nativ crossed 40,000 downloads with 14,000 in a day, served at zero marginal cost, and monetization will target developers deploying to users. PC support exists via CUDA (he runs an RTX 6000 rack) and suits unified-memory NVIDIA hardware such as DGX Spark, but Mac comes first. M1 Macs with 32–64 GB run most models at similar speed; iPhones from the 15 Pro can run ~7 GB models with the right entitlements. Repetition "doom loops" come from training, not from running locally; Nativ counters them with a reasoning token budget or reasoning off, and he ships benchmarked official quantizations.

### [46:49](https://youtu.be/DseVLPC4Qjs?t=2809) EmbeddingGemma 2 benchmarks
With Google DeepMind he day-zero benchmarked the multimodal EmbeddingGemma 2 (text, image, audio, video search) on an M5 Max with 128 GB. Charts show peak memory and batched throughput across batch sizes 1–32 and BF16/8/6/4-bit: at batch 32, roughly 1,000 texts/s, 24 images/s, 70–80 audio clips/s, and ~5 video frames/s (real time). The 1 GB model peaks near 10 GB under mixed inputs, so it fits even a 16 GB M1 MacBook.

## Tools, libraries and specs
- MLX-VLM (MLX omni) engine: open-source Python package, local server mode, Swift SDK announced
- Nativ: Mac app (DMG from GitHub, account Blaizzy), weekly releases, dashboard, projects, extensions, artifacts
- TurboQuant (KV-cache compression), speculative decoding, continuous batching scheduler
- CohereLabs North Mini Code 1.0 (w4a16, ~19 GB), Qwen 27B, Liquid AI LFM2, MiniCPM4, EmbeddingGemma 2
- Pi agent harness, Codex CLI, GitHub MCP, MLX Audio
- Apple M1–M5, iPhone 15 Pro and newer; NVIDIA RTX 6000 / CUDA, DGX Spark

## Who should watch
Mac owners who want coding agents, voice tools, or private assistants running fully on their hardware, and engineers curious how Apple Silicon inference serving is put together. Skip it if you work on Windows or Linux without unified-memory NVIDIA hardware, or if you want engine internals and API detail rather than an app-led tour.

## Verdict
**8/10**: The engine's author runs fast local inference live with Wi-Fi off, backs the engine with open repositories and one day-zero benchmark, but most headline speed figures come with no baseline and the internals stay sketched.

**Novelty 2/2**

- **+** [34:40](https://youtu.be/DseVLPC4Qjs?t=2080) The engine's author explains his on-device design choices: maximize what fits rather than batch size, tune per chip generation, and validate ports against the PyTorch reference on long prompts because matmul-level errors accumulate with context.
- **+** [24:10](https://youtu.be/DseVLPC4Qjs?t=1450) Agent-written contributions grew his engine's tests to 86,000 lines inside a 300,000-line codebase before he noticed, which is first-hand production experience.
- **+** [47:20](https://youtu.be/DseVLPC4Qjs?t=2840) The EmbeddingGemma 2 day-zero benchmark with Google DeepMind is an original measurement no search result offers.

**Demonstrated 2/2**

- **+** [14:06](https://youtu.be/DseVLPC4Qjs?t=846) Voice dictation and chat with CohereLabs North Mini Code run live with Wi-Fi off and the transcript visible.
- **+** [19:59](https://youtu.be/DseVLPC4Qjs?t=1199) The local model builds a chat website over a localhost endpoint, fixes its layout on request, and then holds a working conversation with it.
- **−** [32:03](https://youtu.be/DseVLPC4Qjs?t=1923) The live image-generation demo is not run ("This demo might fail… Maybe not") and the X voice-generation video is skipped for time, so both are described through a stored artifact.

**Measured 1/2**

- **+** [48:22](https://youtu.be/DseVLPC4Qjs?t=2902) The EmbeddingGemma 2 throughput and peak-memory charts compare batch sizes 1–32 and four precisions on a stated M5 Max 128 GB with per-modality inputs.
- **+** [10:27](https://youtu.be/DseVLPC4Qjs?t=627) A slide line gives TurboQuant "3.24× faster decode at 150K tokens" with model (Gemma 4 E4B), benchmark (LongBench-v2) and chip (M3 Ultra 512 GB), though the speaker does not discuss it.
- **−** [38:50](https://youtu.be/DseVLPC4Qjs?t=2330) Prompt caching is "eight times 100 times faster depending on the model" with no method, and the 3x speculative-decoding and ~90 tokens/s chat figures likewise come with no baseline or repeat.

**Depth 1/2**

- **+** [05:13](https://youtu.be/DseVLPC4Qjs?t=313) The decode-ceiling slide (tok/s ≤ bandwidth ÷ bytes read per token, with fewer-bytes and more-tokens-per-read levers) is a working model for matching models to hardware.
- **+** [34:40](https://youtu.be/DseVLPC4Qjs?t=2080) Cloud and on-device priorities are weighed with reasons: fit over batch size, concurrency over batch-of-one, tuning per chip generation.
- **−** [07:49](https://youtu.be/DseVLPC4Qjs?t=469) The scheduler is described by the questions it answers (what to admit, how to prefill without stalling, when to throttle), with no mechanism, and the engine is never set against llama.cpp, Ollama or LM Studio.

**Reusable 2/2**

- **+** [11:58](https://youtu.be/DseVLPC4Qjs?t=718) A slide shows the open-source mlx-vlm and mlx-audio GitHub repositories, which hold the engine the talk is about, and the Python package, one-script example and server mode are described at [09:25](https://youtu.be/DseVLPC4Qjs?t=565).
- **+** [13:01](https://youtu.be/DseVLPC4Qjs?t=781) The Nativ Mac app download is pointed to ("search native blazy" on GitHub) and powers every demo that follows.
