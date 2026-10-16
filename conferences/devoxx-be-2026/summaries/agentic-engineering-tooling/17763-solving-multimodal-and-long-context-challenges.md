---
title: Solving Multimodal and Long-Context Challenges
talkId: "17763"
conference: devoxx-be-2026
speakers: [Laurent Picard]
track: Agentic Engineering & Tooling
sessionType: Deep Dive
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=VTxhxCy_2lE
durationMin: 179
slides: null
verdict: 9
reach: segment
frames: 17
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# Solving Multimodal and Long-Context Challenges
Laurent Picard · Deep Dive · Agentic Engineering & Tooling

## TL;DR
Picard live-codes four production-style problems in Colab notebooks with Gemini: video transcription with speaker attribution, knowledge graph extraction from long documents, consistent image-series generation with Nano Banana, and visual-object detection plus restoration in scanned books. The thesis is that one well-crafted prompt with zero thinking tokens can replace a traditional multi-model ML pipeline when you prototype for model intuition, decouple the problem into sequential sub-tasks, and demand structured output.

## Key takeaways
- Prototype against a small model with no thinking tokens before scaling up: it builds intuition about what the model does naturally and where it breaks.
- When a single "do everything" prompt fails, decouple the task (transcripts table, then speakers table linked by voice ID) while keeping one request.
- Reuse the LLM's own domain terminology in prompts (strict verbatim, timestamp, entity, predicate): Picard asks the model for the vocabulary first, then writes the prompt with it.
- Emit TSV instead of JSON for tabular extractions: measured 30-40% fewer tokens than compact JSON and 60-70% fewer than formatted JSON, which makes generation faster and cheaper since output tokens are the bottleneck.
- For knowledge graphs, implied entities (Henry Jones Sr. inferred from "Jr.") and bidirectional relationships (child-of plus parent-of, friend both ways) must be requested explicitly or the model stays minimal.
- Image consistency comes from a generated reference/character sheet plus chaining each new scene off the previous image, with prompts that say what changed rather than re-describing everything.
- Save prompts and source-image IDs into PNG metadata so a folder of images implicitly carries its own provenance graph without a database.

## Notes

### [02:20](https://youtu.be/VTxhxCy_2lE?t=140) Agenda and ground rules
Four live problems: multimodal video transcription, knowledge graph extraction from documents, a consistent image bank, and visual-object detection/restoration/editing. Everything runs live in Jupyter/Colab notebooks from GitHub (QR code shared). Goals are reproducibility and production-shaped solutions: fixed seed, no thinking tokens, single prompts pushed as far as possible. Only two models used throughout: Gemini Flash-Lite (small) and Flash (medium).

### [09:00](https://youtu.be/VTxhxCy_2lE?t=540) Why multimodal LLMs replace the classic pipeline
A traditional video-transcription pipeline needs speech-to-text, OCR, person detection, entity extraction, and speaker diarization, wired together and calibrated over weeks. A natively multimodal model takes text, images, audio, video, and documents mixed in one request, with 100+ language support that gives cross-language input and one-line output translation. Frame shows the old block diagram collapsing into "one prompt plus configuration".

### [17:15](https://youtu.be/VTxhxCy_2lE?t=1035) Prototyping, part 1: a 1-minute teaser
Unit test is a 1-minute Google DeepMind podcast teaser with two hosts plus montage clips. "Transcribe with start timestamps" processes in about 4 seconds and consumes roughly 5,000 tokens: speech-to-text solved in one line. "List identifiable speakers" returns Demis Hassabis and Professor Hannah Fry in the order names appear on screen (OCR plus entity extraction in one line), answered in about a second from implicit cache, with cached tokens at a 90% discount. Asking for everything at once on this easy video looks perfect, which sets up the failure to come.

### [24:08](https://youtu.be/VTxhxCy_2lE?t=1448) An 8-minute video breaks the naive prompt
A heavily edited 8-minute AlphaFold documentary (narration over B-roll, voice-only passages, footage shot two years apart with different haircuts and clothes, sentences spliced across speakers) defeats the small model and larger ones alike: it mostly echoes whichever name is displayed on screen instead of attributing speech. Options are surrender or build intuition about how the model works.

### [27:47](https://youtu.be/VTxhxCy_2lE?t=1667) Token primer: how Gemini sees video
Tokens are the unit of everything: images run about 1,000 tokens by default, audio 25 tokens/second, video one frame sampled per second at 66 tokens per frame (adjustable frame rate and media resolution up to 264 tokens, or 1,000+ with manual frame extraction). All modalities share one semantic space, which is why native multimodality understands across them. LLMs are sequential statistical machines without self-reflection: order matters, so craft prompts that put the highest-probability material first and keep the statistics on your side.

### [36:38](https://youtu.be/VTxhxCy_2lE?t=2198) Prompt methodology and terminology mining
Method: iterate, be precise (single-meaning words reduce variability without thinking tokens), be concise (repetition introduces randomness and hurts maintainability). Since the speaker is not a transcription expert, he asks the model for the domain terminology and gets transcript, timestamp (not timecode, which means something stricter in video), strict verbatim vs clean verbatim, diarization; reusing these terms is the fastest route to a precise prompt.

### [41:51](https://youtu.be/VTxhxCy_2lE?t=2511) The fix: decouple into two tables, one prompt
Model the problem as two database tables: transcripts (start, text, voice ID) and speakers (voice ID, name). Task 1 asks for a strict-verbatim transcription with a distinct consistent voice ID per voice; task 2 maps each voice ID to a name using audio and visual cues, with "?" as the explicit negative. Generalizing further, "voices" becomes "audio sources" with type (voice, animal, audience), name, company, role, plus non-speech audio (laughter, barking, applause). Pydantic classes generate the JSON schema for guaranteed structured output, removing format description from the prompt.

### [51:47](https://youtu.be/VTxhxCy_2lE?t=3107) Transcription results across videos
The final prompt handles the teaser (detects overlapping laughter), a Jane Goodall nature clip with difficult vocabulary ("serene self-assurance"), a noisy French field report from Brut with four speakers and barking dogs, and the hard 8-minute AlphaFold video with 14 voices, including a correct inference that an unseen 2020 voice is Boris Johnson from context. Long-form works too: 54 minutes analyzed in about 3 minutes with 15 voices (host, keynote, five panelists, audience members, true negatives for people who never introduce themselves), an hour-plus keynote, and a 99-minute video with 40+ speakers in about 7 minutes, far beyond the roughly 10-speaker ceiling of dedicated diarization models. Picard claims the output beat a professional transcription company on the keynote with one phonetic-variant mistake.

### [65:32](https://youtu.be/VTxhxCy_2lE?t=3932) Q&A: YouTube metadata, silent video
Gemini receives only the YouTube video and audio streams, no subtitles or descriptions (verified by re-running from a bucket-stored MP4 with identical results). Silent video gets shot-by-shot summarization instead of transcription. A later question confirms video understanding (panel structure, interview order) has worked for years.

### [69:46](https://youtu.be/VTxhxCy_2lE?t=4186) Problem 2 setup: knowledge graphs from documents
Same approach applied to documents: extract structured knowledge with one prompt and one request, using NetworkX for graph handling. Unit test is an invented Indiana Jones paragraph mixing real and fake names (William Smith, Short Round, a dog named Bo) so hallucinations from training knowledge are detectable.

### [74:34](https://youtu.be/VTxhxCy_2lE?t=4474) Prototyping entity and relationship extraction
"List all people and animals using only the input data" returns every character plus volunteered relations; asking how they relate yields correct natural-language relations ("named after his own father"). Terminology mining gives entities/nodes, relationships/edges, properties, labels, schemas. Formalized as two tables (entities with IDs, relationships as source ID, predicate, target ID), the prompt extracts Henry Jones Sr. as an implied entity from "Jr." via the explicit instruction to include entities "implied and whose names can be determined from the context".

### [86:09](https://youtu.be/VTxhxCy_2lE?t=5169) TSV beats JSON for output tokens
Measuring a sample extraction: TSV uses 335 characters where compact JSON needs twice that and formatted JSON over three times; in tokens, TSV saves 30-40% vs compact JSON and about 70% vs formatted JSON. Output generation is the slow, expensive step, so shorter output means faster, cheaper, more iterable solutions. Templates generate the TSV format from the Entity/Relationship/KnowledgeGraph classes, and parsed rows rehydrate into objects (expandable to any graph database later).

### [92:59](https://youtu.be/VTxhxCy_2lE?t=5579) Books: Therese Raquin to Les Miserables
A book-oriented schema (persons, animals, organizations; pseudonyms as separate entities; relationships with examples like alias-of, son-of, murderer-of, in-love-with) plus instructions to keep every stage of evolving relationships and to emit inverse pairs (husband-of/wife-of, employer-of/employee-of) and both directions of symmetric ones. Results: Therese Raquin (100k+ tokens) in 5 seconds, 11 entities, 28 relationships, with the love triangle and murders visible; Les Miserables (800k tokens, 80% of the 1M context window) in 46 seconds, 64 entities; The Count of Monte Cristo in four volumes under a minute each, resolving Edmond Dantes's aliases (Lord Wilmore, Abbe Busoni, Sinbad the Sailor, the Count himself).

### [109:05](https://youtu.be/VTxhxCy_2lE?t=6545) Dense test: a 100-page pharma agreement
A real (slightly redacted) pharmaceutical co-development agreement, roughly 50k tokens, shows prompt specificity matters: a fully open "comprehensive extraction" prompt returns a minimal summary (two parties, effective date), adding entity types plus a request for legal obligations surfaces liabilities and a $10M payment clause, and a closed schema prompt extracts the document structure (definitions, sections, exhibits) in 6 seconds with 4k output tokens.

### [116:28](https://youtu.be/VTxhxCy_2lE?t=6988) Q&A: judging, guarantees, triples, corrupt I/O
LLM-as-a-judge (same or another model reviewing output) is the recommended production check since reviewing is easier than generating. JSON-schema responses carry a 100% conformance guarantee on Gemini; in practice TSV/YAML/XML emitted against a precise example never corrupted in his experience, though separator collisions (a tab inside data) must be handled. Triplet output works the same way. Corrupt input is mostly auto-corrected statistically unless genuinely ambiguous.

### [125:55](https://youtu.be/VTxhxCy_2lE?t=7555) Problem 3: a consistent image bank from one archive image
Two years ago Picard generated a felt robot he loved for a token-counting article but could never reuse consistently. With Nano Banana (Gemini image models; he uses the small fast Nano Banana 2 Light), the workflow is: think like an art director, not a Photoshop user. A reference/character sheet prompt (front view, back view, white background, studio lighting, plus a chocolate-brown suede backpack with brass buckle described down to the ring shape) generates in about 5 seconds and becomes the new starting point. Default 1K resolution, multiple aspect ratios, up to 2K/4K at higher latency.

### [135:48](https://youtu.be/VTxhxCy_2lE?t=8148) Chaining scenes into a story
Each scene prompt cites its sources (reference sheet, previous scene) and describes only the scene or the delta: mountain diorama with the robot in 3/4 rear view derived from the back view; descent into a valley with an invented felt map placed in its hands; a forest of thin trees in specified light/medium/dark greens with golden-hour lighting; crossing to a clearing; climbing a dome-shaped mountain with invented miniature felt ice picks; summit victory pose with picks planted in the snow. Unwanted continuity (the map) must be removed explicitly or the model keeps it.

### [147:28](https://youtu.be/VTxhxCy_2lE?t=8848) Imperative and indirect prompts
Drastic changes work better as imperative orders ("remove the ice picks, move the center mountain left, add a higher blue mountain right, suspend a felt-plank bridge between them, put the robot mid-bridge pointing at the blue mountain"), generated in about 8 seconds with bridge designs varying per run. The finale uses indirection ("the hammock has replaced the bridge; the robot sleeps in a tartan hammock, eyes closed"), and the model reuses the bridge attachments for the hammock and invents consistent sleeping eyes. Tip: store each image's prompt and source IDs in PNG metadata so the folder itself is a queryable provenance graph.

### [157:32](https://youtu.be/VTxhxCy_2lE?t=9452) Problem 4: detecting visual objects in scans
YOLO-style detectors fail on book pages (trained on chairs, cars, people); a multimodal LLM has spatial plus semantic understanding. One prompt with structured JSON output detects every illustration with bounding box, label, caption/legend, and "?" negatives: a woodcut incunable page with stains and ink bleed, a museum catalog with captions excluded from boxes, an art book where the box correctly stops around an overlapping bookmark, tilted pasted-in 19th-century photos, and a curved, perspectively distorted phone photo of a page. Same code retargeted to a blurry PCB photo extracts every component with on-chip text (including reversed print and line breaks) and classifies passives, diodes, inductors, ICs, transistors, at raised media resolution for exhaustiveness. Pixel-level segmentation masks are available from some models.

### [170:39](https://youtu.be/VTxhxCy_2lE?t=10239) Restore, colorize, reimagine
Restoration prompts ("isolate and straighten on pure white, clean physical artifacts, preserve original detail, center and scale with margins") remove discoloration, the bookmark (inventing what was beneath), tilt, and page curl in 5-10 seconds per image. Then one line each: colorize as a modern book illustration, watercolor vs traditional painting for Alice in Wonderland, engravings to flat digital graphics or to "modern camera photograph", and full cinema mode with movie stills and a generated cast. Closes by pointing at the notebooks QR code.

## Tools, libraries and specs
- Gemini Flash-Lite and Gemini Flash (small/medium models, 1M-token input context, implicit caching with ~90% discount, JSON-schema structured output)
- Nano Banana / Nano Banana 2 Light (Gemini image generation and editing models; 1K default, up to 2K/4K)
- Colab notebooks on GitHub (GoogleCloudPlatform/generative-ai: multimodal_video_transcription, knowledge graph generation) plus matching Google Codelabs
- Python: google-genai SDK, pandas, Pydantic (schema generation), tenacity (retries), NetworkX (graphs)
- TSV as LLM output format (measured token savings over JSON)
- YOLO (contrasted as failing on document illustration detection)
- Companions mentioned: Gemma (open-weights family), Gus Martins (Gemma PM) as a watch recommendation
- Sources: Library of Congress scans (incunabula, museum catalogs), Unsplash images, Brut video, AlphaFold documentary

## Who should watch
Practitioners who want copyable prompt-and-code patterns for video understanding, document extraction, or image pipelines on Gemini, and anyone curious how far zero-thinking-token single prompts stretch. Viewers committed to another model family or wanting Java-specific integration (Picard apologizes for being Python-only at a Java conference) will get patterns but no portable code.

## Verdict
**9/10**: Four problems pushed through live with an original prompt-craft method and reproducible notebooks, with only one like-for-like measurement and the other timings self-reported.

**Reach segment**: Developers adding LLM video, document-extraction or image features to their applications can copy the prompt-and-notebook patterns within the next year.

**Novelty 2/2**

- **+** [14:39](https://youtu.be/VTxhxCy_2lE?t=879) Inverting the usual scale-up habit, the speaker prototypes every problem against the smallest model with zero thinking tokens to build intuition about what the model does naturally.
- **+** [42:56](https://youtu.be/VTxhxCy_2lE?t=2576) The two-table decoupling (transcripts with voice IDs plus speakers mapped from those IDs in one prompt) is the speaker's own fix after the naive all-in-one prompt failed on the 8-minute video.

**Demonstrated 2/2**

- **+** [51:47](https://youtu.be/VTxhxCy_2lE?t=3107) The final transcription prompt runs live across the teaser, a nature clip, a French field report and the 8-minute AlphaFold video with 14 voices.
- **+** [104:51](https://youtu.be/VTxhxCy_2lE?t=6291) Les Misérables (800,000 tokens) analyzes live in 46 seconds with 64 entities extracted.
- **−** [173:15](https://youtu.be/VTxhxCy_2lE?t=10395) One restored illustration comes out still slightly tilted, with no retry mechanism on stage.

**Measured 1/2**

- **+** [89:20](https://youtu.be/VTxhxCy_2lE?t=5360) Live tokenization compares the same extraction across formats: TSV saves over 35% of tokens against compact JSON and about 70% against formatted JSON.
- **−** [110:40](https://youtu.be/VTxhxCy_2lE?t=6640) The 13, 11 and 6 second timings are single self-reported runs of three prompts that return different outputs, so they are no like-for-like comparison.
- **−** [65:01](https://youtu.be/VTxhxCy_2lE?t=3901) Beating a professional transcription firm is asserted without error-rate numbers.

**Depth 2/2**

- **+** [36:08](https://youtu.be/VTxhxCy_2lE?t=2168) Sequential token generation grounds the prompt-order rule: lead with the highest-probability material to keep the statistics on your side.
- **+** [89:52](https://youtu.be/VTxhxCy_2lE?t=5392) Output generation is the slow and costly step, which is the stated reason for choosing TSV over JSON.
- **+** [33:33](https://youtu.be/VTxhxCy_2lE?t=2013) Frame sampling trades tokens against detail: media resolution rises from 66 to 264 tokens per frame, or frames are sampled manually past 1,000 tokens.

**Reusable 2/2**

- **+** [04:14](https://youtu.be/VTxhxCy_2lE?t=254) All material is public through the shared URL and QR code, matching what runs on stage.
- **+** [05:16](https://youtu.be/VTxhxCy_2lE?t=316) The notebooks live on GitHub and open in Colab, so the staged runs can be repeated at home.
