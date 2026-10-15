---
name: summarize-talk
description: Summarize one conference talk from the catalog into a summary file from its video transcript. Use when asked to summarize a talk, or when given a talk id and conference slug to summarize.
---

Input: a conference slug and a talk (id or title fragment), and optionally `checker=<name> judge=<name>` to have the verdict reviewed (step 8). With no slug, use the only directory under `conferences/`; with several, ask. Run every command from the repo root. Commands below write `<slug>` and `<id>` for the resolved values.

Any step that ends the run early records the outcome in the catalog first; the catalog is how `summarize-backlog` knows what is done.

## 1. Resolve the talk

`uv run scripts/catalog.py show <slug> <talk>` prints the talk record. Several matches → pick the exact id when the request makes it unambiguous, otherwise ask. Proceed when `status` is `matched`, `failed`, or `summarized` (a re-summarize overwrites). Any other status: report it and stop.

## 2. Transcript

`uv run scripts/transcript.py <slug> <id>` prints the cached transcript path (`[mm:ss] text` paragraphs).

- Exit 3 (no captions): `uv run scripts/catalog.py set <slug> <id> --status no-transcript`, then stop.
- Exit 4 (fetch failed): `uv run scripts/catalog.py set <slug> <id> --status failed --error "<last stderr line>"`, then stop.

## 3. Read the whole transcript

Read it in ranges until you have read the final timestamp. Note segment boundaries, timestamps, and moments where the speaker points at the screen ("as you can see", code walkthroughs, diagrams, benchmark charts).

## 4. Slides

Find the speaker's published deck from two sources:

- **Closing**: the transcript's last three minutes for a spoken link ("slides are on…"), and a frame of the final slide via `uv run scripts/frames.py` (see step 5) for a URL or QR caption.
- **Web search**: `"<title>" <first speaker> slides`. Decks live on Speaker Deck, SlideShare, GitHub, Google Slides, personal sites.

Accept a deck only when all three hold: its title is this talk (or plainly the same talk renamed), its author is one of the speakers, and it names this conference (`name` in `conferences/<slug>/conference.yaml`) or was published on or after the talk's `start`. The same talk's deck from an earlier event is accepted with a `slidesNote: from <event>`. Anything less certain stays unlinked.

An accepted deck with a downloadable PDF (Speaker Deck's "Download PDF" link): `curl -sL -o conferences/<slug>/slides/<id>.pdf <pdf url>` (create the directory if needed), then read the whole PDF. Done when a deck is accepted and its PDF read where one exists, or both sources came up empty.

## 5. Frames

Look at the screen where it carries what the speech and the deck leave out: code, architecture diagrams, benchmark numbers, demo output. The frame budget scales with `video.durationSec`: one frame per 5 minutes, minimum 5, cap 30 (a 50-minute talk gets 10, a 3-hour Deep Dive 30). A talk with code, demos or diagrams uses at least a third of its budget, unless the deck already covers them; a talk that is all speech may use fewer. `uv run scripts/frames.py <slug> <id> <mm:ss> [<mm:ss> ...]` grabs them in one call and prints one image path per frame; read each image. Frames are best-effort: a failed frame costs only that frame, so continue with what you have. Done when the frames you read are counted for the front matter's `frames` field.

## 6. Write the summary

Read [`SUMMARY-FORMAT.md`](SUMMARY-FORMAT.md) and write the file it specifies, at the path printed by `uv run scripts/catalog.py path <slug> <id>`; a re-summarize overwrites that file. Done when every section is present (Tools may be omitted per the format), the body length is within the format's budget, and every claim traces to the transcript, a frame, or the deck.

## 7. Record

```
uv run scripts/catalog.py set <slug> <id> --status summarized --summary <summary path> --transcript <transcript path> --slides <deck url | none> --scores <novelty> <demonstrated> <measured> <depth> <reusable>
```

The catalog stores the five criteria and their sum as the verdict, so the scores here match the summary's `## Verdict` section.

An unexpected error in steps 2–7: `uv run scripts/catalog.py set <slug> <id> --status failed --error "<what broke>"`.

## 8. Review (opt-in)

Only when the input named both a checker and a judge: read [`../review-verdict/SKILL.md`](../review-verdict/SKILL.md) and run its steps 1–5 for this talk with those two, as its author, with everything you read for the summary still in hand. A review that fails leaves the recorded summary as it is, unreviewed; say so in the reply.

## Reply

End with exactly one line: `<id> summarized verdict=<score> <summary path>`, followed by `, reviewed <old> -> <new>` or `, review failed: <reason>` when step 8 ran; or `<id> <status>: <reason>` when the run stopped early.
