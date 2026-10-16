---
name: find-talks
description: Find conference talks by topic, day, length, level, track, tier, verdict, reach, or popularity across catalog and summaries. Use when asked which talks cover a subject, for talk recommendations, for talks on a given conference day, or for talks fitting a time slot or audience level.
---

Input: what the user is looking for, plus an optional conference slug (default: every directory under `conferences/`, each searched separately). Run every command from the repo root.

## 1. Translate the request

Map the request onto `uv run scripts/catalog.py find <slug>` filters (`--help` lists them):

- **Topic** → several `--text` terms: the user's words plus synonyms, abbreviations and related tools (`--text "virtual threads" --text loom --text "structured concurrency"`). Any term matching counts; the search covers title, abstract, CFP keywords, speakers and summary text, on word boundaries.
- **Length** → `--max-minutes` / `--min-minutes` (video length when matched, else the slot length).
- **Level** → `--level BEGINNER|INTERMEDIATE|ADVANCED`; **track** / **session type** → `--track` / `--type` substrings.
- **Worth watching, no topic given** ("must-see", "the best talks", "what should I watch") → `--tier must-watch` (add `--tier recommended` for a longer list) or `--sort rating`. The tier ranks every summarized talk by its worth to the conference's audience, weighing quality and how many can use it; it is the answer to "should I watch this".
- **Best within a topic** ("the best Kafka talk", "good talks on Valhalla") → the topic terms with `--sort verdict` or `--min-verdict 7`. The verdict (0–10) rates quality for the talk's subject; once the user has picked the subject, reach no longer matters. A typical good talk scores 5–6.
- **Breadth** ("something everyone on my team can use", "nothing too specialised") → `--reach broad` (repeat `--reach segment` to widen). Reach is `niche`, `segment` or `broad`: how much of the conference's audience can use the main content.
- **Criterion** ("novel", "with live demos", "with real numbers or benchmarks", "deep", "something I can reuse") → `--min-novelty` / `--min-demonstrated` / `--min-measured` / `--min-depth` / `--min-reusable`, each 0–2: 2 means the summary found something specific there, 1 is the norm, 0 a shortfall. "Skip talks without demos" → `--min-demonstrated 1`; "the most novel" → `--sort novelty`. Filters combine with AND; for an OR ("novel or deep") run one search per criterion and merge the results. Pacing and speaking style are not scored: say so when asked.
- **Day** ("talks I saw Monday", "what ran on Tuesday afternoon") → `--day mon` (repeatable; weekday or `YYYY-MM-DD`, conference-local time) with `--sort time`; narrow to a part of the day from each result's `when`.
- **"popular"** → `--sort favourites` or `--min-favourites N`. `favourites` counts attendees who bookmarked the talk in the schedule: interest before the talk, never a quality rating; say so whenever you cite it.
- Searches the whole catalog by default; `--status summarized` only when the user wants talks they can read now.

## 2. Search and judge

Run the search. Each result carries a `brief` (the summary's TL;DR, or the abstract when unsummarized) and the `matched` terms. A text match is a lead, not a verdict: keep a talk only when its brief shows the topic is central to it, not a passing mention. Zero or very few results → widen the terms or relax one filter once, and say which.

Done when every candidate in the result list has been kept or dropped on its brief.

## 3. Reply

A list ranked by relevance (tier, then verdict, breaks ties), or in time order for day questions:

`[<title>](<summaryPath>)`, `<speakers>` · `<when>` · `<minutes> min` · `<level>` · `<tier>` · `verdict <n>/10` · `<reach>` · `[slides](<url>)` when present. Under it, one line on why it fits. When a criterion drove the search, name its score (`novelty 2`). Talks not yet ranked or rescored show no tier or reach; leave those out of the line.

Unsummarized talks link the `video` instead and are marked *not summarized yet*; offer to summarize the ones the user wants.
