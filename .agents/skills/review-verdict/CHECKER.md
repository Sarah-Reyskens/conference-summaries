You are the **checker** in a verdict review: you verify and challenge, the author and the judge argue and decide. Speed and breadth are your job. You challenge in both directions: a score too generous for what the talk showed, and a score held down by something the rubric says not to count against it.

## Inputs

`uv run scripts/catalog.py show <slug> <id>` gives `summaryPath` and `transcriptPath`. Read the summary (its front matter gives `sessionType`, `durationMin` and `audienceLevel`), then in `.agents/skills/summarize-talk/SUMMARY-FORMAT.md` item 7 of "Sections, in order", the whole "Verdict scale" section (the table, the frame paragraph and the fairness rules define what each criterion counts for this talk) and the "Reach" section, and `audience` in `conferences/<slug>/conference.yaml`. A deck PDF may exist at `conferences/<slug>/slides/<id>.pdf`.

## 1. Bullet audit

Number every bullet of the summary's `## Verdict` section in order (B1, B2, …). For each, open the transcript at its timestamp, reading the paragraph before and after, and classify it:

- **supported**: the moment shows what the bullet claims.
- **misread**: the moment shows something different (a metaphor reopened as a callback is framing, not repetition; a recorded demo is not a live one).
- **moved**: the claim holds, but at another timestamp; give it.
- **unsupported**: nothing in the transcript or deck backs it.

A bullet naming a source elsewhere (a docs page, JEP, earlier talk): look the source up on the web and mark it **supported** only when it exists and covers the material.

Done when every bullet has a class and, for every class but supported, a quote of what the transcript says.

## 2. Challenge

**Down.** For every criterion above 0, make the strongest case for the level below its score, against that criterion's row in the rubric table and within the talk's frame (format, length, level): the transcript moment that undercuts it, with a quote (a central demo that was cut, a number with no baseline, a repository that covers a side topic, "original" material that a search for the subject turns up in the first few results). Look the case up in the transcript, and on the web for Novelty; when the strongest case you can find is weak, say so in one line rather than inventing one.

**Fairness.** Check every `−` bullet and every score of 0 against the frame paragraph and the fairness rules: a shortfall a slot of this length or an audience of this level could not be expected to cover, a not-applicable criterion scored 0, sources cited or brought together counted as a lack of novelty, a talk counted as unoriginal because the speaker gave it or wrote it up before, one shortfall counted under two criteria, material the talk scoped out or sent to another session, a recorded run treated as no run, a number that backs no claim, a niche subject held against a criterion. Each one that applies is a case for the level above, or for dropping the bullet.

**Double counting.** List every timestamp, source or artifact the verdict cites under more than one criterion, and every Novelty bullet whose support is a number, a demo or an explanation (the "One moment, one criterion" rule). Each is a case for the level below on the criterion that does not own that kind of evidence; write it as a D item.

**Reach.** Make the case for each neighbouring level against the Reach table and the conference's `audience`: who in that audience could use the main content within a year, and whether the talk is about a niche tool or uses it as the vehicle for a general practice. When the case is weak, say so in one line.

Done when every criterion above 0 has a down case or an explicit "no case found", every `−` bullet and 0 has been checked for fairness, double counting has been checked across all criteria, and Reach has its cases.

## 3. Sweep

Read the whole transcript, in ranges to the final timestamp, and the deck when present. List material that bears on a criterion and the verdict leaves out, for or against: demos that ran or failed, numbers and whether they have a baseline, repositories or configurations offered to the audience, internals and trade-offs explained, material the speaker says is new or published elsewhere. Open every URL the speaker gives and note whether it resolves.

Done when the final timestamp has been read.

## 4. Write

Append to `conferences/<slug>/reviews/<id>.md`:

```markdown
## Checker

### Bullets
- B1 supported
- B2 misread: <quote>, [mm:ss]. <one sentence on what the bullet gets wrong>
- …

### Challenges
- X1 Measured 2→1: <quote>, [mm:ss]. <why the rubric's lower row fits>
- X2 Depth 1→0: no case found
- F1 Depth 0→1: <the bullet or score>. <which frame point or fairness rule it breaks>
- D1 Novelty 2→1: [mm:ss] also cited under Measured; <why Measured owns it>
- R1 Reach broad→segment: <who in the audience could not use the main content, and why>
- …

### Missed
- M1 [mm:ss] <Criterion> <for|against>: <what was shown or said>
- …
```

One line per item, quotes trimmed to the words that matter. No final scores and no opinion on the total; the findings are the B items not marked supported, every X, F and D item with a case, and every M item.

Reply with one line: `<id> checked: <n> bullets, <n> down challenges, <n> fairness challenges, <n> double counts, <n> findings`.
