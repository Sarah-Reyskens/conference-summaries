# Summary format

One Markdown file per talk, at the path `uv run scripts/catalog.py path <slug> <id>` prints (`summaries/<track-slug>/<talkId>-<title-slug>.md`). Written in English whatever the talk's language.

## Length

Body (everything below the front matter) ≈ 300 words per 15 minutes of video (`video.durationSec`), minimum 300, cap 2500. A 50-minute talk lands near 1000 words, a 3-hour Deep Dive at the cap. The section notes absorb the scaling; the other sections stay compact.

## Front matter

```yaml
---
title: <CFP title>
talkId: "<id>"
conference: <slug>
speakers: [<full names>]
track: <track>
sessionType: <session type>
audienceLevel: <BEGINNER|INTERMEDIATE|ADVANCED>
video: https://www.youtube.com/watch?v=<videoId>
durationMin: <video length, rounded>
slides: <deck URL, or null when none was accepted>
slidesNote: from <other event>   # only when the deck is from an earlier event
verdict: <0-10, the sum of the five criteria in the verdict scale>
reach: <niche|segment|broad, see Reach>
frames: <number of frames looked at, 0 if none>
summarizedAt: <YYYY-MM-DD>
reviewedAt: <YYYY-MM-DD>     # only after the review-verdict skill ruled on the verdict; a rescore removes it
---
```

## Sections, in order

1. `# <title>` followed by a line `<speakers> · <sessionType> · <track>`, and, when a deck was accepted, a line `Slides: <url>`.
2. `## TL;DR`: 2–3 sentences: the talk's thesis and what it leaves you with.
3. `## Key takeaways`: 3–7 bullets. Each is a claim or practice you could act on, specific enough to disagree with.
4. `## Notes`: the talk's arc as `###` subsections, one per major segment, each heading a timestamp link: `### [12:34](https://youtu.be/<videoId>?t=754) <segment topic>`. Keep the speaker's concrete material: numbers, benchmarks, demos and what they showed, examples, production incidents and what they taught, audience Q&A worth keeping.
5. `## Tools, libraries and specs`: bullets of everything named with enough weight to look up, with versions when stated (`LangChain4j 1.x`, `JEP 401`). Omit the section when nothing qualifies.
6. `## Who should watch`: who gains most, and who can skip it (already knows X, needs Y instead).
7. `## Verdict`: first line `**<score>/10**: <one-line reason>` naming what earns the score and its main limit. Second line, after a blank line: `**Reach <level>**: <one sentence naming who in the conference audience can use the main content>`. Then one block per criterion, in scale order: a line `**<Criterion> <n>/2**`, a blank line, and 1–3 bullets, followed by a blank line. Each bullet is one sentence: `**+**` (a strength) or `**−**` (a weakness), then the timestamp link of the moment it is about, then the claim. The mix follows the score: a 2 is mostly `+` with at most one `−`; a 1 balances strengths with evidenced limitations where both exist; a 0 is mostly `−`. Never invent a weakness to balance the bullets; use `**·**` for a neutral limit rather than treating ordinary scope or credited background as a fault. A criterion scored 1 as not applicable (see the rules under the scale) has a single `**·**` bullet saying why instead.

   ```markdown
   **Measured 2/2**

   - **+** [41:10](https://youtu.be/<videoId>?t=2470) The dashboard shows p99 latency drop from 900 ms to 120 ms after the connection-pool fix.
   - **−** [43:05](https://youtu.be/<videoId>?t=2585) The speedup comes from one service under synthetic load; no production numbers follow.
   ```

   A bullet about something missing links the moment where it was due (the claim it would have backed). A Novelty `−` saying the material is what a search already gives names the source (docs page, JEP, well-known article) instead of a timestamp.

## Verdict scale

The verdict is the sum of five criteria, each scored 0, 1 or 2 from the talk itself (transcript, frames, deck). Each one rests on something a reader can check: a moment in the video, or a named source. It rates the talk's quality for its subject; who can use that subject is Reach, rated separately (see below). A niche subject is no `−` on any criterion, and a broad one earns no point.

**Judge the talk it set out to be.** The front matter's `sessionType`, `durationMin` and `audienceLevel` set what a criterion can fairly ask for. A 20-minute keynote, a 40-minute lunch talk and a 3-hour deep dive are held to different bars on Depth and Demonstrated, and a BEGINNER talk to a beginner's depth. Write each bullet about what this talk did with its slot, never about what a longer or more advanced talk would have added.

Score as a **skeptic** within that frame. 1 is the default for a competent talk. A 2 must survive the strongest case against it: before writing one, put that case to the transcript and look for the moment that answers it. When the evidence sits between two levels, take the lower. Most criteria of a good talk land at 1; four or five 2s in one talk are rare.

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Novelty | what searching the subject and reading the first few results already tells you: the official docs, a vendor's getting-started, a well-known article | more than a quick search gives: several sources brought together, or the speaker's own examples illustrating known material | the core rests on what no search gives: production experience (what the speaker's team tried, what broke, what they changed and why) or a synthesis no single source offers (a decision framework tested on their own cases, approaches compared across several tools); prior publication of the speaker's own material does not disqualify it |
| Demonstrated | the talk claims something can be done and only describes it | some claims shown working on screen; or the central demo fails or is cut | the central claim shown working on screen end to end, live or as a recording of the actual run with its output visible (a recording trimmed or sped up for time counts) |
| Measured | the talk makes quantitative claims (speed, cost, adoption, effect) and backs none with a number | numbers without a baseline or method: anecdotes, self-reported totals (lines of code, tests passing, "500 PRs a week"), "about three times faster" | measurements with a baseline or comparison and a stated method: before/after, A against B, a benchmark whose setup is shown, production metrics over time |
| Depth | names things, for its level and slot | shows how to use it, or explains the internals of a side topic | explains why and how the core topic works at the depth its level and slot allow: internals, trade-offs weighed against alternatives, design decisions with their reasons. For a BEGINNER talk or a slot under 30 minutes, a clear mental model of why the thing works and when to choose it is depth |
| Reusable | nothing to take away beyond the ideas | fragments: code on slides, practices described but left for you to reconstruct, a repository unrelated to the talk's main content, the presented project's own repository or distribution | a published artifact the talk points to that reproduces its main content: a sample project or demo repository, a complete configuration, a checklist |

Rules that keep the criteria fair:

- **Not applicable is 1.** A criterion the talk had no reason to meet scores 1 with one neutral bullet saying why: Demonstrated for a subject with nothing to run (a language proposal that isn't in any JDK, a strategy or culture talk, an audience workshop, a short keynote with no demo slot), Measured for a talk that makes no quantitative claim. 0 is for a shortfall on something the talk claimed or needed.
- **Novelty asks: does watching beat searching?** The baseline is a search for the subject and its first few results. A talk that brings several sources together, credits them, or uses a published algorithm or benchmark scores at least 1; write no `−` for it. The speaker's own material stays theirs: the same talk given at another event, or built on their own blog post or book, is no `−`.
- **A project's own authors.** When the speakers present a project they build or sell, its docs, README, release notes and blog posts are part of the search baseline: a tour of its features and API is Novelty 1, and its design decisions with their reasons count under Depth. The project itself is the talk's subject, not a takeaway, so its repository, jar or distribution is Reusable 1; a demo repository or sample project that reproduces the talk's examples is 2.
- **One moment, one criterion.** Every moment, source or artifact the verdict cites backs exactly one criterion, strengths and shortfalls alike: no timestamp appears under two criteria. Each criterion owns one kind of evidence: numbers are Measured, something running on screen is Demonstrated, explanations of how and why something works are Depth, published artifacts are Reusable. Novelty owns what is left: experience and synthesis a search doesn't give. A benchmark the speaker ran is Measured however original it is; a Novelty bullet states in words what a viewer learns that no search gives, and a Novelty point whose only support is a number, a demo or an explanation does not count. A shortfall likewise counts once: a cut demo is Demonstrated, not also Depth or Reusable.
- **Scope is the speaker's call.** Material the talk declares out of scope or sends to another session (a companion deep dive, a later talk) earns no `−`; judge what it covers.
- **Numbers must back the talk's claims.** An audience poll or a configured parameter is not a measurement.
- The deck does not count toward Reusable, and its absence is no `−` either; the summary already links any deck. Pacing, voice and stage presence are not scored: captions and stills can't show them reliably.

What totals mean, so scores stay comparable across runs:

- **9–10**: exceptional for its subject: original, shown, measured, explained and reproducible. A handful per conference.
- **7–8**: strong for its subject.
- **5–6**: a typical good conference talk.
- **3–4**: thin, or the material is better elsewhere.
- **0–2**: skip.

Whether a talk is worth watching depends on its verdict and its Reach together. That is the job of the ranking tier (`rank-talks` skill) and never of the verdict alone: a 10 on a niche subject is excellent for the few who work on it.

## Reach

One of three levels, judged against `audience` in `conferences/<slug>/conference.yaml`: the share of that audience who could put the talk's main content to use in their own work within the next year. It rates the subject, not the talk: a weak talk on unit testing is broad, an excellent one on GPU kernels is niche.

| Reach | Who can use the main content |
|---|---|
| niche | people already working in a specialised area most of the audience never touches: GPU computing, compiler or JVM internals, one vendor's product, a curiosity subject with nothing to apply |
| segment | a sizable minority: users of one common framework or platform, one role, one kind of system (teams building LLM features, Kubernetes operators, Spring Boot users) |
| broad | most of the audience: everyday language and library features, testing, design and architecture, team practice, AI-assisted development in general |

- Judge what a viewer carries into their own work. When a niche tool is only the vehicle for a general practice the talk spends most of its time on, the practice sets the reach; a talk about the tool itself stays niche however general its framing.
- A feature most of the audience will meet once it ships (a JDK feature, a major framework release) is broad, even when the talk is about its internals; the internals then show in Depth, not in Reach.
- Between two levels, take the narrower.

## Fidelity

- Ground every statement in the transcript, a frame, or the accepted deck. The CFP abstract is context for what the talk set out to do, never a source of claims. Where the deck and the captions disagree on a name, number or URL, the deck wins.
- Auto-captions mishear names ("longchain forj" is LangChain4j); write the correct product, project and speaker names, using the deck, the abstract and context.
- Code goes in fenced blocks whose first line is a comment naming its origin: `// from published slides p.12` when taken from the deck, `// from slide at 23:10` when read off a frame, `// reconstructed from speech` when rebuilt from what was said. Include code only when one of these carries enough to make it accurate.

## Style

Write like a colleague's notes, not a review blurb: plain declarative sentences that state what the speaker said, showed or measured.

- Name the thing itself: "a production outage where the Debezium connector lost its offsets", not "a war story". Same for "deep dive", "under the hood", "the punchline", "the real X", "through-line".
- No intensifiers or praise adverbs: "genuinely", "honest(ly)", "refreshingly", "candid", "solid", "concrete", "actionable", "game-changer". A verdict earns its score through the specifics in its bullets.
- No "not just X, but Y" or "X, not Y" constructions as a rhetorical device; say what it is.
- At most one em dash per paragraph; use a colon, parentheses or a new sentence instead.
- No labels like "Takeaway:" inside Notes; the Key takeaways section holds those.
- Vary sentence openings; don't open consecutive bullets or paragraphs with the speaker's name.
