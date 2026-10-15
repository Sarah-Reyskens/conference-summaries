# Conference talk summaries

Summaries of software-engineering conference talks, written from their YouTube videos. Everything specific to one conference lives in its conference file; skills and scripts stay conference-agnostic.

## Layout

```
conferences/<slug>/
  conference.yaml      conference file
  catalog.json         catalog (written only by scripts/catalog.py)
  summaries/
    INDEX.md           generated on every catalog write: summarized talks by track, best verdict first, with day/time/room and schedule bookmarks
    <track-slug>/      one summary per talk: <talkId>-<title-slug>.md
  transcripts/         cached caption transcripts (gitignored)
  frames/              cached video stills (gitignored)
  slides/              downloaded slide-deck PDFs (gitignored)
  reviews/             review-verdict discussion logs, one per talk (gitignored)
scripts/
  catalog.py           build / status / next / show / path / find / index / set (file-locked writes)
  transcript.py        fetch YouTube auto-captions → [mm:ss] paragraphs
  frames.py            grab video stills at timestamps (needs ffmpeg)
.agents/skills/
  catalog-talks/       user-invoked: build or refresh a catalog
  summarize-talk/      model-invoked: summarize one talk, with an opt-in verdict review; SUMMARY-FORMAT.md defines the output
  summarize-backlog/   user-invoked: summarize the next batch with parallel sub-agents
  review-verdict/      model-invoked, only with a checker and a judge named (summarize-talk runs it as step 8): author/checker/judge discussion of one summary's verdict; CHECKER.md and JUDGE.md brief the sub-agents
  find-talks/          model-invoked: search talks by topic, day, length, level, track, verdict, bookmarks
```

Scripts run with `uv run scripts/<name>.py`; `--help` lists commands.

## Glossary

- **Talk**: one session from a conference's CFP, identified by its CFP `id`.
- **Conference file**: `conference.yaml`; the talk source, video playlists, matching thresholds, excluded session types, and manual video overrides for one conference.
- **Catalog**: `catalog.json`; every talk with its matched video and progress `status`: `excluded`, `no-video`, `needs-review`, `matched`, `summarized`, `no-transcript`, `failed`.
- **Summary**: the Markdown file for one talk, in the format of `.agents/skills/summarize-talk/SUMMARY-FORMAT.md`.
- **Verdict**: a summary's 0–10 score, the sum of five 0–2 criteria (novelty, demonstrated, measured, depth, reusable) defined in `SUMMARY-FORMAT.md`.
