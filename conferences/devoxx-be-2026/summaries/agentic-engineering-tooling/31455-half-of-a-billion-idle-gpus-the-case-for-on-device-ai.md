---
title: "Half of a billion Idle GPUs: The Case for On-Device AI"
talkId: "31455"
conference: devoxx-be-2026
speakers: [Prince Canuma]
track: Agentic Engineering & Tooling
sessionType: Keynote
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=qFTuteOEtsE
durationMin: 20
slides: null
verdict: 7
frames: 8
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# Half of a billion Idle GPUs: The Case for On-Device AI

Prince Canuma · Keynote · Agentic Engineering & Tooling

## TL;DR

Apple Silicon devices are the largest distributed AI compute base in the world, and almost all of it sits idle. Canuma presents his NeuraLabs stack (MLX-VLM/MLX-Audio engine, the Native app, single-JSON extensions) plus TurboQuant optimization as the platform that moves most cloud queries on device. Run locally first for privacy, latency, cost, and sovereignty; reach for the cloud only for very long runs or trillion-parameter models.

## Key takeaways

- Treat hardware you own as the first cluster: unified memory lets CPU, GPU, and Neural Engine share everything loaded, and Apple passed a billion AI-capable devices.
- Locally solvable cloud queries rose from 23% to 70-90% in three years as chips improved and open models closed to 3-6 months behind closed ones.
- TurboQuant KV-cache quantization enables 1M-token contexts on a Mac Studio with faster decode and no accuracy loss, unlocking DeepSeek 4.1 and GLM 5.3 Flash on device.
- One Mac Studio serves 100-plus concurrent local streams; serving Native's 40,000 downloads cost the team zero.

## Notes

### [00:33](https://youtu.be/qFTuteOEtsE?t=33) Half a billion idle GPUs

Born in Mozambique, Canuma spent a decade building local AI, including five years in India after seeing the technology at Google I/O 2017. ChatGPT-style tools never reached billions of people, yet those same people own Macs and iPhones. Apple held half a billion AI-capable devices in 2023 with no platform for open frontier models; today it is over a billion. Unified memory plus the Neural Engine makes every one of them an inference machine.

### [03:45](https://youtu.be/qFTuteOEtsE?t=225) The NeuraLabs stack

The base is the MLX-VLM and MLX-Audio engine, used by millions of developers, translating open models to iPhone, iPad, Mac, and visionOS. MLX-VLM grew from vision-language into any-input/any-output multimodal, all local. Native, a macOS/iOS app, plugs local models into existing coding tools (Codex, OpenCode, Pi, Hermes). Extensions define a Native app UI and workflow in one JSON file; a videographer built a voice-cloning extension in days, and a marketplace is coming. The team grew Apple-runnable models from 100 to 5,000.

### [07:00](https://youtu.be/qFTuteOEtsE?t=420) Cloud versus local

Cloud coding means rate limits and $100-200 top-ups. Locally, memory is shared across apps and models, the bottleneck is memory bandwidth (improving yearly), and a Mac Studio serves 100-plus streams. Per-token pricing turns punishing once agents add image, audio, and video tokens.

### [10:39](https://youtu.be/qFTuteOEtsE?t=639) Intelligence per watt and TurboQuant
Intelligence per watt (better chips times open models nearing closed ones) puts locally answerable queries at 70-90%, up from 23%. Canuma's TurboQuant port speeds up decode and reaches 1M-token contexts on a Mac Studio; LongBench V2 runs on Gemma 4 E4B reached 256K, 512K, and 1M contexts on an M3 Ultra, with 3.24x faster decode at 150K tokens and the same answers as baseline on every sample. Speculative decoding, MTP, and D-Flash add 2-3x across modalities.

### [13:43](https://youtu.be/qFTuteOEtsE?t=823) Four forces, then demos

Enterprises keep sensitive documents local (privacy), GPT-6-class models are slow over the network (latency), subscriptions plus overages hit thousands monthly (cost), and Fable 5's post-release block stranded its users for a week (sovereignty). Demos: a Reachy Mini robot doing on-device voice cloning and speech tasks powered by his laptop, and Native with a local code model building a working snake game in minutes. A hands-on deep dive follows at 14:00 in Room 3.

## Tools, libraries and specs

- MLX-VLM / MLX-Audio: multimodal and speech inference engines on Apple MLX
- Native: NeuraLabs local-AI app; single-JSON extensions; 40,000 downloads
- TurboQuant: Google Research KV-cache quantization; speaker's local port in mlx-vlm
- LongBench V2: long-context benchmark behind the 1M-context runs
- Reachy Mini: Pollen Robotics robot driven by the laptop in the demo
- Models named: DeepSeek 4.1, 4.1 Flash, GLM 5.3 Flash, GPT-6, Fable 5

## Who should watch

Apple-device owners curious what local inference does today, and developers adding AI under privacy or cost constraints. Skip it for hands-on MLX code (that is the 14:00 deep dive) or non-Apple coverage.

## Verdict

**7/10**: The speaker's own TurboQuant port with 1M-token runs, a local code model building a game on screen, a reasoned local-versus-cloud model for a 20-minute slot, and public mlx-vlm, mlx-audio and nativ repositories; limited by benchmark numbers without a baseline setup, claims about frontier models and 1M contexts shown only on slides, and a thesis built mostly on credited and common sources.

**Novelty 1/2**

- **+** [11:42](https://youtu.be/qFTuteOEtsE?t=702) The TurboQuant port in mlx-vlm is the speaker's own implementation of Google's method, run on an M3 Ultra with LongBench V2.
- **+** [05:55](https://youtu.be/qFTuteOEtsE?t=355) The growth of Apple-runnable models from 100 to 5,000 over three years is the speaker's own experience, which he says is documented on his YouTube.
- **−** [12:50](https://youtu.be/qFTuteOEtsE?t=770) The speaker's own results fill one slide with one model (Gemma 4 E4B), a small part of a talk whose frame is the credited intelligence-per-watt study and the cloud-versus-local argument.

**Demonstrated 1/2**

- **+** [18:29](https://youtu.be/qFTuteOEtsE?t=1109) Native on screen shows a snake game that a local code model generated, with token counts, decode tok/s and peak memory visible.
- **+** [17:57](https://youtu.be/qFTuteOEtsE?t=1077) The Reachy Mini robot answers "Hey there. Great to see you." with a laptop-cloned voice, played as a short video after a reload.
- **−** [12:50](https://youtu.be/qFTuteOEtsE?t=770) The 1M-token contexts, the frontier-model runs and the 100-plus streams appear only on slides or in speech; no run of them is shown.

**Measured 1/2**

- **+** [12:50](https://youtu.be/qFTuteOEtsE?t=770) The slide names Gemma 4 E4B, LongBench-v2 and M3 Ultra, with 3.24x faster decode at 150K tokens, the same answer as baseline on every sample, and a KV cache 3.8x smaller at 3.5-bit and 4.9x at 2.5-bit.
- **−** [12:43](https://youtu.be/qFTuteOEtsE?t=763) The 256K, 512K and 1M contexts are spoken ("I think it was 256") with no numbers on the slide, and the baseline configuration and variance are not given.
- **−** [09:07](https://youtu.be/qFTuteOEtsE?t=547) "Up to 100 streams" names no model, device or load, and the 3 to 6 month open-model lag and the 40,000 downloads at zero cost [16:22] are self-reported with no source.

**Depth 2/2**

- **+** [02:43](https://youtu.be/qFTuteOEtsE?t=163) Unified memory is explained as the mechanism: whatever is loaded is shared by CPU and GPU, and the Neural Engine is efficient but not the fastest.
- **+** [08:04](https://youtu.be/qFTuteOEtsE?t=484) Cloud and local are weighed on memory, bottlenecks, concurrency, hardware and per-token cost, each with a reason.
- **+** [15:18](https://youtu.be/qFTuteOEtsE?t=918) After the four forces of privacy, latency, cost and sovereignty [13:43], the cloud boundary is drawn: the 5 to 10% of tasks such as a week-long run belong on the cloud, 30-minute to one-hour work runs locally.

**Reusable 2/2**

- **+** [04:00](https://youtu.be/qFTuteOEtsE?t=240) The stack slide shows mlx-vlm and mlx-audio, the engine the talk builds on, as GitHub repositories, and the benchmark slide labels the TurboQuant runs "in mlx-vlm".
- **+** [19:45](https://youtu.be/qFTuteOEtsE?t=1185) The closing slide lists github.com/Blaizzy, where mlx-vlm, mlx-audio and the Native repository (nativ) are public under the MIT license.
- **−** [18:35](https://youtu.be/qFTuteOEtsE?t=1115) The robot demo is published as a video on his X account; no repository for the robot application is on a slide.
