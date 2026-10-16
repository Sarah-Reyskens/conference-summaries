# Conference talk summaries

Summaries of software-engineering conference talks, written from their YouTube videos. Everything specific to one conference lives in its conference file; skills and scripts stay conference-agnostic.

## Layout

```
conferences/<slug>/
  conference.yaml      conference file
  catalog.json         catalog (written only through scripts/catalog.py's locked writer; rank.py uses it)
  ranking.json         talk-against-talk ranking state (written only by scripts/rank.py)
  summaries/
    INDEX.md           generated on every catalog write: must-watch and recommended talks, then summarized talks by track, best ranked first, with day/time/room and schedule bookmarks
    <track-slug>/      one summary per talk: <talkId>-<title-slug>.md
  transcripts/         cached caption transcripts (gitignored)
  frames/              cached video stills (gitignored)
  slides/              downloaded slide-deck PDFs (gitignored)
  reviews/             review-verdict discussion logs, one per talk (gitignored)
scripts/
  catalog.py           build / status / next / show / path / find / index / set (file-locked writes)
  rank.py              start / next / group / record / status / fit: Swiss-round ranking of summarized talks into tiers
  transcript.py        fetch YouTube auto-captions → [mm:ss] paragraphs
  frames.py            grab video stills at timestamps (needs ffmpeg)
.agents/skills/
  catalog-talks/       user-invoked: build or refresh a catalog
  summarize-talk/      model-invoked: summarize one talk, with an opt-in verdict review; SUMMARY-FORMAT.md defines the output
  summarize-backlog/   user-invoked: summarize the next batch with parallel sub-agents, or rescore verdicts after a rubric change
  review-verdict/      model-invoked, only with a checker and a judge named (summarize-talk runs it as step 8): author/checker/judge discussion of one summary's verdict; CHECKER.md and JUDGE.md brief the sub-agents
  rank-talks/          user-invoked: rank summarized talks against each other into tiers with parallel sub-agents; RANKER.md briefs them
  find-talks/          model-invoked: search talks by topic, day, length, level, track, tier, verdict, reach, bookmarks
```

Scripts run with `uv run scripts/<name>.py`; `--help` lists commands.

## Glossary

- **Talk**: one session from a conference's CFP, identified by its CFP `id`.
- **Conference file**: `conference.yaml`; the talk source, video playlists, matching thresholds, excluded session types, manual video overrides, and the `audience` description for one conference.
- **Catalog**: `catalog.json`; every talk with its matched video and progress `status`: `excluded`, `no-video`, `needs-review`, `matched`, `summarized`, `no-transcript`, `failed`.
- **Summary**: the Markdown file for one talk, in the format of `.agents/skills/summarize-talk/SUMMARY-FORMAT.md`.
- **Verdict**: a summary's 0–10 score of the talk's quality for its subject, the sum of five 0–2 criteria (novelty, demonstrated, measured, depth, reusable) defined in `SUMMARY-FORMAT.md`.
- **Reach**: `niche`, `segment` or `broad`; how much of the conference's `audience` can use a talk's main content, rated with the verdict but never added to it.
- **Tier**: `must-watch`, `recommended`, `if-relevant` or `low-priority`; a talk's quota-based place in the ranking of all summarized talks by worth to the audience (`rank-talks`). The answer to "should I watch this"; the verdict alone is not.
