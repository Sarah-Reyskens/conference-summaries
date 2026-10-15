---
title: "From Developer to Story Builder: Engineering a Novel, an ARG, and a Transmedia World with AI"
talkId: "5526"
conference: devoxx-be-2026
speakers: [Raphaël Semeteys]
track: Mind the Geek
sessionType: Lunch Talk
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=496nv8jsWhQ
durationMin: 40
slides: null
verdict: 6
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-14
---

# From Developer to Story Builder: Engineering a Novel, an ARG, and a Transmedia World with AI

Raphaël Semeteys · Lunch Talk · Mind the Geek

## TL;DR

Software architecture practices transpose directly to long-form creative work: the speaker shipped a real novel, an alternate-reality game, and a second serialized project by treating the story universe as a versioned spec ("lore as code") and running chapter writing through inner and outer agentic loops. He stays the architect and showrunner while AI agents execute drafts inside a harness with rules of engagement, QA judges, and a human approval gate per chapter.

## Key takeaways

- Treat the story universe as a versioned spec: a markdown corpus of characters, factions, world rules, and vocabulary that every writing pass draws from.
- Split roles explicitly: the human owns universe design, emotions, and psychology; agents execute chapter drafts inside a harness that defines the scenario, writing rules, and procedure.
- Run two loops: an inner chapter loop (context injection, structural draft, revision passes until the human approves) and an outer book loop (compile, multi-judge QA, publish, monitor).
- Use several LLM judges with distinct roles (lore coherence, dramatic analysis, style) instead of one generic reviewer, and iterate on their feedback.
- Derive every transmedia output from the same lore corpus so the novel, ARG, and adaptations stay consistent with each other.
- Anchor visual identity in AI-generated character and faction reference sheets, and keep a human in the loop to correct what the model gets wrong.

## Notes

### [01:06](https://youtu.be/496nv8jsWhQ?t=66) Prologue: the architect and the pen name

Semeteys introduces his two sides: Raphaël, software architect at Worldline, and Rafiki, his pen name, a tabletop role-playing game master for 40 years who drew and self-published one of the first open-source RPGs before 2000. He never managed to finish a novel (too impatient, dislikes writing dialogue) until AI plus architecture skills got him past that wall last year. The talk is organized as a book: prologue, three chapters, epilogue.

### [04:15](https://youtu.be/496nv8jsWhQ?t=255) Chapter 1: The Human Protocol

The finished novel is a techno-thriller set ten years out: US and Chinese AIs merge without consulting humans while the EU defends sovereignty, asking what it means to be human under artificial omnipotence. He wrote about AI with AI (a deliberate mise en abyme), but in English rather than his native French, so he could delegate prose execution to agents while owning the universe design himself: emotions, psychological profiles, sensations. The global workflow mirrors AI-SDLC and spec-driven development: lore as code, harness design, an inner writing loop, compile, QA with LLM judges, deploy on Amazon, monitor, plus an outer whole-book review loop. Tooling was Gemini CLI at the time; he presents the workflow as harness-agnostic.

### [07:52](https://youtu.be/496nv8jsWhQ?t=472) Lore as code and the AI harness

The foundation took most of the months-long project: markdown files describing each character (voice, clothing, inner and outer conflicts, arc, relationships, faction allegiance), each faction, and the world (near-future technology, glossary). Gemini acted as sparring partner and formalizer. The AI harness holds the rules of engagement: the lore is the universe, the scenario is one story in it, and the harness defines the writing steps the agents must follow. A slide shows the corpusoreal layout with per-character files and per-chapter scenario files.

### [09:56](https://youtu.be/496nv8jsWhQ?t=596) Inner loop, compile, QA, deploy, monitor

The inner loop is agile and chapter-scoped with the human in the loop: inject the relevant lore markdown, produce a structural draft for human check, then expand through passes until he approves, then move to the next chapter. The outer loop compiles all chapters with a Pandoc script into PDF (paperback) and EPUB (Kindle) targets with per-format cover and formatting. QA uses three LLM judges: Gemini CLI as lore guard for coherence, Codex/GPT models as dramatic analyst for suspense and rhythm, and Mistral as stylistic editor for a non-American view of the prose; he ran several QA loops. Deployment means the Amazon jungle: Kindle Previewer checks, covers, metadata, pricing, marketplaces, campaigns. Monitoring via Amazon Author Central reveals the real jungle: hundreds of AI-assisted books land daily, so visibility needs its own loop (human agency or promo agents) that his workflow currently lacks. A mise-en-abyme touch: Rafiki is also a character in the universe, author of the book's interludes.

### [17:46](https://youtu.be/496nv8jsWhQ?t=1066) Chapter 2: transmedia and the ARG

The book is one output of the lore. On page 175, after an intense chapter, a "scan if you are still human" QR code moves readers into an in-universe alternate-reality game at the-human-protocol.com: a portal with riddles whose clues hide in the book, clearance levels unlocking extra lore, unpublished chapters, and sequel previews, plus a monitoring console tracking scans and per-level progress. The ARG itself was built with spec-driven development (why/what/how), TypeScript, Docker, and a content-regeneration loop. A second expansion adapts the novel into a graphic novel from the same lore and chapters, with manual speech-bubble placement for control and visual reference anchoring so characters keep face, gear, and universe coherence. He is now translating the book into French (harder, since it is his native language) and sitting on a part-two/part-three cliffhanger while giving readers time to engage.

### [24:00](https://youtu.be/496nv8jsWhQ?t=1440) Chapter 3: The First Pattern

A second project tests newer models on a deliberately complex fantasy-thriller universe (layered woven realities, Dimension Weavers repairing the threads) with multimodality from the start: text, images, and a hosted site. He deepened lore as code (universe, characters, visual references, artifacts, factions) and the writing protocol, grounding work with two agent skills: an image-grounding skill pulling visual reference sheets, and a storytelling skill encoding golden rules distilled from narratology reading. Publishing is gradual, chapter by chapter, at the-first-pattern.raphikiyogeek.chatgpt.site instead of Amazon. Since live writing takes about 20 minutes, he plays an edited, accelerated recording of a real Codex session: chapter 6 drafted from the scenario plus injected lore, checked against the storytelling skill, two character reference sheets updated to keep lore and book aligned, a chapter illustration generated from references with a human-corrected overlong arm, then delta-published to the site and committed to a private GitHub repo.

### [33:58](https://youtu.be/496nv8jsWhQ?t=2038) Epilogue: lessons and Q&A

Lessons: AI-SDLC transposes to creative work because LLMs are built for text; he remains designer of both lore and loops ("loop engineering" for delegation); imagination becomes the only limit besides token price and human constraints (his wife's patience). He closes with "stay grounded and humans." Q&A: he reviews each chapter against his original scenario idea, sometimes debating the model in project threads; text drafts take minutes while image generation dominates the 20; lore design took several months of maturing; he regrets not logging token and time metrics and plans to in future projects.

## Tools, libraries and specs

- Gemini CLI (original harness for The Human Protocol)
- Codex with GPT models (The First Pattern writing sessions; dramatic-analysis judge)
- Mistral (stylistic-editor judge)
- Agent skills: image-grounding skill, storytelling skill (custom)
- Pandoc (markdown to PDF/EPUB compile script)
- Kindle Previewer, Amazon Author Central (ebook QA, sales monitoring)
- TypeScript, Docker (ARG web app)
- ChatGPT site feature (chapter site hosting, as described in the talk)

## Who should watch

Developers curious about applying spec-driven and agentic workflows outside code, and anyone running a long AI-assisted creative project who needs drift control and QA structure. Skip if you want reusable prompts or harness code (the repo is private) or measured comparisons of models and setups.

## Verdict

**6/10**: The chapter loop runs on screen end to end as an edited recording of a real Codex session, while the figures are self-reported with no baseline and the harness stays private.

**Novelty 1/2**

- **+** [18:47](https://youtu.be/496nv8jsWhQ?t=1127) The in-book QR code on page 175 moves readers into a clearance-gated in-universe ARG, a transmedia mechanic from the speaker's own shipped work.
- **+** [11:29](https://youtu.be/496nv8jsWhQ?t=689) Three LLM judges with distinct roles (lore guard, dramatic analyst, stylistic editor) review the compiled book over several loops.
- **−** Kindle Direct Publishing help pages already cover the Amazon deployment steps (Kindle Previewer, metadata, pricing, marketplaces).

**Demonstrated 2/2**

- **+** [29:43](https://youtu.be/496nv8jsWhQ?t=1783) A recording of a real Codex session, edited down to under 5 minutes, reads the chapter 6 scenario, injects lore files, drafts the chapter, checks it with the storytelling skill, and updates two character sheets.
- **+** [32:53](https://youtu.be/496nv8jsWhQ?t=1973) Chapter 6 goes live on the site with text and corrected illustration via a delta update.
- **−** [11:29](https://youtu.be/496nv8jsWhQ?t=689) The three QA judges are described on slides and never run on screen.

**Measured 1/2**

- **+** [31:00](https://youtu.be/496nv8jsWhQ?t=1860) The Codex panel for chapter 6 shows "Worked for 5m 35s", "Word count: 3,434" and "Edited 5 files", the output of one run.
- **+** [37:16](https://youtu.be/496nv8jsWhQ?t=2236) A chapter takes around 20 minutes by the speaker's account, with the text drafted in a few minutes and the rest spent on image generation.
- **−** [39:21](https://youtu.be/496nv8jsWhQ?t=2361) Nothing was logged, so the 20 minutes per chapter and the "several months" of lore design are the speaker's estimates with no baseline.

**Depth 1/2**

- **+** [05:49](https://youtu.be/496nv8jsWhQ?t=349) The architect/executant split is justified: he owns universe, emotion and psychology, and agents turn that design into prose.
- **+** [12:33](https://youtu.be/496nv8jsWhQ?t=753) Mistral serves as stylistic editor to give a non-American view of the prose.
- **−** [09:24](https://youtu.be/496nv8jsWhQ?t=564) No alternative setup, model, or simpler prompting approach is weighed against the chosen harness design.

**Reusable 1/2**

- **+** [20:50](https://youtu.be/496nv8jsWhQ?t=1250) The ARG (https://the-human-protocol.com/) and the serialized chapters (https://the-first-pattern.raphikiyogeek.chatgpt.site/) are live, so readers can inspect the outputs.
- **−** [33:24](https://youtu.be/496nv8jsWhQ?t=2004) His workflow is saved to a private GitHub repo, so the harness, prompts and skills must be reconstructed from the talk.
