# Conference talk summaries

Written summaries of software-engineering conference talks, produced from the talk videos (captions, on-screen slides and, where the speaker published them, the slide deck). Currently covers **Devoxx Belgium 2026**.

Each summary tells you what the talk argued, what you'd take away, what was shown section by section (with links that jump to that moment in the video), which tools and specs came up, who should watch it, and an opinionated verdict with its audience reach. A separate ranking compares summarized talks and assigns watch-priority tiers.

## Finding talks

### Browse the index

Start at [`conferences/devoxx-be-2026/summaries/INDEX.md`](conferences/devoxx-be-2026/summaries/INDEX.md). It opens with must-watch and recommended talks across tracks, then lists every summarized talk by track. Within each list, talks sort by tier, ranking rating, then verdict; unranked talks follow the ranked ones.

| Column | Meaning |
|---|---|
| Tier | watch priority from the comparative ranking, see below |
| Verdict | 0–10, see the scale below |
| Reach | `niche`, `segment` or `broad`: how much of the conference audience can use the main content |
| Talk | links to the summary |
| When | day, local start time and room, handy for finding talks you attended or skipped |
| Type, Min, Level | session type, video length, audience level from the CFP |
| Favs | attendees who bookmarked the talk in the conference schedule. This measures interest *before* the talk, not quality. |
| Slides | the speaker's published deck, when one was found |

Summary files live in one folder per track: `summaries/<track>/<talkId>-<title>.md`.

### Tiers and reach

**Tier answers “should I watch this?”** It comes from comparing summarized talks by their worth to the audience described in [`conference.yaml`](conferences/devoxx-be-2026/conference.yaml), considering quality, reach and time investment.

| Tier | Share of ranked talks |
|---|---|
| `must-watch` | top 5% |
| `recommended` | next 15% |
| `if-relevant` | next 40% |
| `low-priority` | remaining 40% |

Quotas are rounded to whole talks. They apply to the ranked, summarized talks, not every session in the conference. The ranking is an agent judgment, not an attendee vote; it changes as talks are added or reassessed.

**Reach describes who can use the subject**, independent of quality: `niche` for a specialised area, `segment` for a sizable minority such as users of a common framework, `broad` for most of the conference audience. The horizon is applying the main content in their own work within the next year. Reach is never added to the verdict: a 10/10 niche talk can still rank below a lower-scoring talk useful to many more people.

For recommendations across subjects, use tier. Once you've chosen a subject, use verdict to compare its talks. Talks awaiting ranking or rescoring may have no tier or reach.

### Verdict scale

The verdict is the sum of five criteria, each scored 0–2 and each resting on something you can check: **novelty** (does watching give you more than searching the subject and reading the first few results?), **demonstrated** (claims shown working on screen), **measured** (numbers with a baseline or method), **depth** (internals and trade-offs) and **reusable** (a repository, configuration, checklist or code you can apply). A competent talk scores 1 on each, so the typical good talk lands at 5–6.

Each talk is judged against its own slot: a 20-minute beginner keynote isn't expected to go as deep or demo as much as a 3-hour deep dive, and a criterion that doesn't apply (no demo for a language proposal, no numbers for a talk that makes no quantitative claim) scores a neutral 1. Pacing, voice and stage presence are not scored: captions and video stills can't show them reliably.

| Score | Meaning |
|---|---|
| 9–10 | exceptional for its subject |
| 7–8 | strong for its subject |
| 5–6 | a typical good conference talk |
| 3–4 | thin, or the material is better elsewhere |
| 0–2 | skip |

Each summary's `## Verdict` section lists the five criteria with timestamp-linked evidence and a reach explanation. Each cited moment, source or artifact backs one criterion only, so the same evidence cannot inflate multiple scores. The verdict is the summarizing model's judgment of quality for the subject; it is not a conference-wide watch recommendation. The full rubric is in [`SUMMARY-FORMAT.md`](.agents/skills/summarize-talk/SUMMARY-FORMAT.md).

### Search from the command line

```sh
uv run scripts/catalog.py find devoxx-be-2026 --text "virtual threads" --text loom --max-minutes 60
uv run scripts/catalog.py find devoxx-be-2026 --tier must-watch --tier recommended --sort rating --limit 100
uv run scripts/catalog.py find devoxx-be-2026 --reach broad --sort rating
uv run scripts/catalog.py find devoxx-be-2026 --day mon --day tue --sort time
uv run scripts/catalog.py find devoxx-be-2026 --status summarized --min-verdict 7 --level beginner
uv run scripts/catalog.py find devoxx-be-2026 --min-depth 2 --min-demonstrated 1 --sort novelty
```

Each verdict criterion has its own filter, `--min-novelty`, `--min-demonstrated`, `--min-measured`, `--min-depth` and `--min-reusable` (0–2), and `--sort` accepts any criterion name.

The command returns JSON with each talk's TL;DR (or its abstract when not yet summarized), when it ran, length, verdict, criterion scores, reach, tier, rating and links. Tier and reach filters are repeatable (any listed value matches); different filters combine with AND. `--sort rating` uses tier, rating and verdict in that order. `--help` lists all filters. It needs only [`uv`](https://docs.astral.sh/uv/).

### Ask a coding agent

With a coding agent running in this repo, ask in plain language. The `find-talks` skill turns questions about topic, day, length, level, track, tier, verdict, reach or popularity into the search above, judges which results really fit, and also covers talks that aren't summarized yet:

- "Which talks under an hour cover Java concurrency or performance?"
- "Which talks should I watch first, across all tracks?"
- "Which recommended talks could most of my team use?"
- "Which talks did I possibly see on Monday morning?"
- "Most popular beginner talks on Tuesday?"

## Contributing

Adding summaries, reviewing verdicts, ranking talks and adding a conference are covered in [`CONTRIBUTING.md`](CONTRIBUTING.md). [`AGENTS.md`](AGENTS.md) has the repo layout and glossary.
