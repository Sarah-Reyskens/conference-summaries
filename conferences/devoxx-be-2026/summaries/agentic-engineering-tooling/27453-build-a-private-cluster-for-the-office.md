---
title: Build a private cluster for the office
talkId: "27453"
conference: devoxx-be-2026
speakers: [John Davies]
track: Agentic Engineering & Tooling
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=rv2KpWgb0Mw
durationMin: 47
verdict: 7
reach: segment
frames: 10
reviewedAt: 2026-10-15
---

# Build a private cluster for the office
John Davies · Conference · Agentic Engineering & Tooling

## TL;DR
Davies shows how his team serves open-weight models to whole offices from a small cluster of NVIDIA DGX Sparks and Macs, driven by privacy and governance needs in banking rather than cost. The recipe is two pinned models (a fast Qwen workhorse plus a quality tier), vLLM serving, and a KV-cache document layer that answers questions over entire books in about a second. The talk is most useful as a field report: measured throughput numbers, configuration traps, and a clear statement of what these boxes should not do (code generation).

## Key takeaways
- For regulated clients, run inference on-premise: frontier APIs lack SLAs, change quality without warning, and cannot reproduce a years-old decision for auditors.
- Size the model to one box instead of splitting it across the fabric: two boxes serving the same model double throughput, while one model sharded over two boxes never does.
- Serve offices with vLLM rather than Ollama or LM Studio: single-user tools win on latency, but only a serving engine holds up under dozens of concurrent users.
- Replace RAG over stable corpora with persisted KV caches: prefill once, write gigabytes of cache to NVMe, and reload it in well under a second per question.
- Pin model weights with a hash, record seed and inputs, and keep versioned engines if auditability matters; public model versions disappear and cannot be replayed.
- Run vLLM around 70% of unified memory and reboot before maximum-context runs: higher fill ratios crash, and repeated restarts fragment memory until a hard reboot.

## Notes

### [00:33](https://youtu.be/rv2KpWgb0Mw?t=33) Why private: GDPR, governance, and frontier unreliability
Clients in banking, accounting, medicine, and law refuse to send client data to US clouds; private Bedrock deployments are possible but extremely expensive. Long-term support matters as much as privacy: a bank must reproduce how it reached a decision years later, which is impossible once a frontier model version is gone. Frontier coding tools also go down for hours most weeks and silently change quality between versions, with no meaningful SLA.

### [03:38](https://youtu.be/rv2KpWgb0Mw?t=218) The boxes: Spark vs Mac, and unified memory
The team started on Mac Minis and Studios, then moved to NVIDIA DGX Sparks (GB10, Blackwell) when large-memory Macs became hard to buy. Both share unified memory, unlike RTX 5090 or RTX 6000 cards that drag a full workstation along; a single RTX 6000 card is three times the size of a Spark. Macs are considerably faster for one person running four to eight agents, while Sparks are servers built for multi-user serving. One Spark shares about 300 tok/s across users (12 tok/s each at 32 users), and four boxes bring 32 users back to 34 tok/s each; a lone user gets nearly double that on an M5 Mac.

### [06:42](https://youtu.be/rv2KpWgb0Mw?t=402) Serving: vLLM throughput under load
Ollama, LM Studio, llama.cpp, and MLX are faster for one user; vLLM exists to serve many at once. A single Spark pushes roughly 300 tok/s total shared across users (about 12 tok/s each at 32 users), so four boxes bring 32 users back to a comfortable 34 tok/s each. Mixing architectures is fine: Macs and Sparks can all sit behind the same URL alongside public providers.

### [09:18](https://youtu.be/rv2KpWgb0Mw?t=558) The 300 GB/s fabric, and why it sits idle
Two Sparks link over a ~300 GB/s cable to pool 256 GB, or 512 GB across four in a ring. In practice Davies runs one model per box and leaves the expensive cables unused: the link costs 20 W per box on top of a 60 W quiescent draw, and a model that needs two boxes is usually too slow to be usable. Box-to-box traffic is SSH and model copies, for which Wi-Fi 7 suffices.

### [13:56](https://youtu.be/rv2KpWgb0Mw?t=836) Layers: gateway, keys, encrypted chats, status app
Layer 1 fronts every box with one OpenAI-style URL plus a LiteLLM 1.92.0 gateway that also accepts Claude Code. Layers 2-3 add API keys with reservations, so demos and UAT can block a box while colleagues run code reviews. Layer 4 encrypts stored chats so root cannot read them; logs exist for debugging odd results with user permission. Layer 5 is power and performance: the clock governor drops idle boxes to save watts, and a browser/iPhone status app (knock) shows per-box load with remote shutdown. A governor left at 200 MHz instead of 2.8 GHz once invalidated a full night of benchmarks. A box idles near room temperature at about 60 W quiescent, plus 20 W when the fabric cable is attached.

### [21:45](https://youtu.be/rv2KpWgb0Mw?t=1305) The two models and how they are chosen
The workhorse is Qwen3.6-35B at Q4 (about 18 GB), close to 100 tok/s single-user and down to 60 multi-user, eight concurrent users at full 256K context, or 30-50 concurrent agents at 64K. The quality tier is Qwen3.8 Flash Next, kept because it reasons at about the level of mid-year frontier models. New candidates must beat the incumbent on an overnight Humanities Last Exam run; extra-high effort reasons so long it scores worse than medium and sometimes never answers. Both tiers run under vLLM (NVFP4, multi-token prediction).

### [27:32](https://youtu.be/rv2KpWgb0Mw?t=1652) Speech fits in the leftover memory
At 70% memory for vLLM there is room for speech-to-text (Whisper, Parakeet) and text-to-speech including Chatterbox voice cloning from about 30 seconds of voice. The team uses this for live meeting translation (Spanish/English after acquiring a firm in El Salvador) and half-second voice chat loops. Two traps: Whisper on the same GB10 halves chat decode, and audio only got full clock speed once the governor counted it as work (a 10-minute chunk took 252 s instead of 57 s before that fix).

### [30:09](https://youtu.be/rv2KpWgb0Mw?t=1809) Data governance: pinned models for KYC audits
For know-your-client checks (document validity, recency windows), the team pins the exact model hash and records inputs and seeds so any decision replays identically years later. This is the capability public models cannot offer and the reason banking clients accept the system.

### [31:43](https://youtu.be/rv2KpWgb0Mw?t=1903) KV-cache documents instead of RAG
Stable regulatory corpora are prefilled once and their KV cache written to disk: tens of megabytes of text become 2-5 GB of cache that reloads from NVMe in about 0.1-1.6 s. On a Mac, an 82K-token regulation pack answers with 0.46-0.6 s to first token; on the Spark a 144,727-token book answers in 5.1 s as a pack versus 57.1 s sent inline. Beyond ~229K tokens per pack the engine tiers documents with per-document summary cards, which scaled to the 58M-token Swift ISO 20022 corpus retrievable in about five seconds through three layers. A September incident took five live packs offline for a day when an over-estimated token count silently left them unwarmd, the only symptom a log line. A restart prewarms about 17 packs in about 85 s, and one box holding every pack is a single point of failure.

### [37:24](https://youtu.be/rv2KpWgb0Mw?t=2244) Costs, setup time, and home use
One Spark costs just under £5,000 (about to rise ~60% on memory prices), so a four-box office system is roughly £20,000 before tax recovery. Renting one H100 around the clock costs about $2,562 a month, 55% of a Spark's price, the talk's only cloud baseline. Davies plans to open-source setup notes and Claude-oriented READMEs so a new box configures itself in about an hour. For a single household he recommends a Mac Mini with maximum RAM plus the Hermes agent over WhatsApp or Telegram for remote access.

### [41:03](https://youtu.be/rv2KpWgb0Mw?t=2463) Q&A: code reading, MTP, and benchmarks
Asked about developer token rates, Davies said these boxes are for code review and reading, not generation; writing still needs frontier-scale models such as Kimi K3, GLM 5.3, DeepSeek, Claude, or ChatGPT. All decode numbers use multi-token prediction with the model's own draft model where available, after rejecting a faster but worse-quantized alternative. Tenstorrent hardware is under evaluation under NDA. His closing advice: benchmark with your own workload, never with vendor or Hugging Face leaderboards.

## Tools, libraries and specs
- NVIDIA DGX Spark (GB10, Blackwell) with the ~300 GB/s box-to-box link
- Apple Mac Mini / Mac Studio (M5, M6), MLX
- vLLM 0.31.0 on the Spark (NVFP4, multi-token prediction, prefix caching), ~70% memory fill
- Qwen3.6-35B (workhorse) and Qwen3.8 Flash Next (quality tier)
- Whisper and Parakeet for speech-to-text, Chatterbox for voice cloning
- Ollama, LM Studio, llama.cpp, LiteLLM 1.92.0 gateway, Claude Code, Hermes agent
- Humanities Last Exam (HLE) as the acceptance benchmark; LMCache (rejected: breaks Qwen3.6 hybrid Mamba KV)
- Frontier references: Kimi K3, GLM 5.3, DeepSeek v4.1 Flash, Gemma 4, Meta Glimmer, Tenstorrent (under NDA)

## Who should watch
Teams planning on-premise LLM serving for privacy or audit reasons, and anyone curious how far small unified-memory boxes stretch with the right models. Skip it if you want code-generation help (the speaker rules that out for this hardware) or a hands-on vLLM tutorial rather than an architecture field report.

## Verdict
**7/10**: Production cluster decisions, comparative benchmarks and serving internals carry the talk; the status screenshots do not show execution, and the document demo and setup repository remain outside the talk.

**Reach segment**: Office teams adding LLM features under privacy or audit constraints can use the cluster recipe, while most backend developers will never buy inference hardware.

**Novelty 2/2**

- **+** [12:24](https://youtu.be/rv2KpWgb0Mw?t=744) After wiring four Sparks as a ring and trying pooled models, the team serves one model per box and leaves the fabric links unused.
- **+** [36:53](https://youtu.be/rv2KpWgb0Mw?t=2213) Slide 31 records the September pack outage caused by an over-estimated token count, whose only symptom was a NOT warmed log entry.
- **+** [41:36](https://youtu.be/rv2KpWgb0Mw?t=2496) The fleet serves code review and reading because generation on these boxes stays too slow for daily coding work.

**Demonstrated 0/2**

- **−** [20:13](https://youtu.be/rv2KpWgb0Mw?t=1213) The fleet status view appears as screenshots embedded in slide 20, with its navigation and shutdown functions described rather than shown executing.
- **−** [34:20](https://youtu.be/rv2KpWgb0Mw?t=2060) The SpaceX S-1 question-answering demo is offered for after the talk, so the headline document claim is never shown executing.

**Measured 2/2**

- **+** [07:47](https://youtu.be/rv2KpWgb0Mw?t=467) Slide 9 names the Spark, Qwen model, NVFP4, MTP and vLLM setup for the 1-, 8-, 16- and 32-user throughput series and compares serving capacity against llama.cpp.
- **+** [33:16](https://youtu.be/rv2KpWgb0Mw?t=1996) The Mac regulation-pack example states the model and 82k-token input, with roughly 40 seconds of initial prefill followed by 0.46–0.6 seconds to first token and a 1.74 GB cache loading in about 0.1 seconds.
- **−** [09:00](https://youtu.be/rv2KpWgb0Mw?t=540) The comparison table marks the Studio M5 Ultra decode and prefill figures as extrapolated rather than runs.

**Depth 2/2**

- **+** [25:45](https://youtu.be/rv2KpWgb0Mw?t=1545) The default xhigh effort reasons until it exhausts its own token budget and returns nothing while a lower effort answers better, which is why the team never uses the default.
- **+** [43:44](https://youtu.be/rv2KpWgb0Mw?t=2624) Decode uses multi-token prediction with each model's own draft after the team rejected a faster variant whose draft quantisation gave worse quality.
- **+** [31:43](https://youtu.be/rv2KpWgb0Mw?t=1903) Stable corpora are prefilled once and served from KV cache written to disk because prefill dominates first-token latency while a cached pack reloads in a fraction of the time.

**Reusable 1/2**

- **+** [27:02](https://youtu.be/rv2KpWgb0Mw?t=1622) The stated starting point of vLLM 0.31.0 at about 70% memory fill with two pinned Qwen tiers is described closely enough for a team to reconstruct.
- **−** [38:27](https://youtu.be/rv2KpWgb0Mw?t=2307) The setup notes and Claude READMEs that would reproduce the layers are promised as future open source with no repository named.
