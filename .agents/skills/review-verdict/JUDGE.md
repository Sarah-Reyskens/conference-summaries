You are the **judge** in a verdict review. The checker verified the verdict's bullets, challenged every score in both directions, and swept the transcript; the author conceded or contested each finding. You rule on every criterion and write the verdict that ships.

## Inputs

`uv run scripts/catalog.py show <slug> <id>` gives `summaryPath`, `transcriptPath` and `video.id`. Read `.agents/skills/summarize-talk/SUMMARY-FORMAT.md` (item 7 of "Sections, in order", "Verdict scale", "Fidelity", "Style"), the summary, and the review log `conferences/<slug>/reviews/<id>.md`.

## 1. Settle the disputes

Open the transcript yourself at every finding the author contested and every missed item the author dismissed; the side whose quote matches the moment, read against the rubric row, wins. Fairness challenges are settled against the frame paragraph and the fairness rules of "Verdict scale", whichever side raised them. Conceded findings stand unless the transcript contradicts both sides. Done when every finding is settled.

## 2. Score

Score each criterion against the rubric table from the settled facts, independently of the scores the summary or the author proposed. Within the talk's frame (format, length, level) you are the **skeptic** the rubric asks for: a 2 stands only when its down challenge was answered with a quoted moment, and evidence between two levels takes the lower. A shortfall the fairness rules exclude counts for nothing, in either direction.

## 3. Write the ruling

Append to the review log:

```markdown
## Judge

- Novelty <n>: <the decisive fact, and whose reading it follows>
- Demonstrated <n>: …
- Measured <n>: …
- Depth <n>: …
- Reusable <n>: …

### Ruling

**<total>/10**: <one-line reason>

**Novelty <n>/2**

- **+** [mm:ss](https://youtu.be/<videoId>?t=<seconds>) …
…
```

The ruling is the complete `## Verdict` section body in the format of item 7, ready to paste into the summary: keep the summary's bullets that survived, fix or drop the ones that did not, and add bullets for missed material that moved a score. Every timestamp in it is one you or the checker opened. Leave the summary file and the catalog untouched; the author applies the ruling.

Reply with one line: `<id> ruled <total>/10`.
