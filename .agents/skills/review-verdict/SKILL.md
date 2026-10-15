---
name: review-verdict
description: Review a summarized talk's verdict in a three-way discussion (author, checker, judge) and apply the judge's ruling. Use when asked to review a verdict with a named checker and judge; summarize-talk runs it when given both.
---

Input: a conference slug (default: the only directory under `conferences/`), one or more talk ids, and two sub-agents named by the user:

- `checker=<name>`: a fast, cheap agent or model for fact checks and broad scanning.
- `judge=<name>`: the strongest agent or model available, for the ruling.

Both are required. Pass each name unchanged to your harness's sub-agent mechanism (an agent name, model, or role alias, whatever the harness accepts). Either missing → ask the user for it and stop; the user picks the models, so never substitute one.

You are the **author**. Sent here from `summarize-talk`, you wrote the summary and keep everything you read for it; run on its own, read the summary first and open the transcript wherever a finding points. Run every command from the repo root. Each talk runs steps 1–5 on its own; talks may run in parallel.

## 1. Resolve

`uv run scripts/catalog.py show <slug> <id>` gives `summaryPath`, `transcriptPath` and `video.id`. Proceed only when `status` is `summarized`; otherwise report the status and skip the talk. The review log is `conferences/<slug>/reviews/<id>.md` (create the directory if needed); start it with a line `# Review of <id>, <YYYY-MM-DD>`, overwriting an earlier log.

## 2. Checker

Start one sub-agent with the checker, prompt:

```
Read .agents/skills/review-verdict/CHECKER.md and follow it for talk <id> in conference <slug>. Work from the repo root.
```

Done when the log has a `## Checker` section; a checker that ends without one is a failed review: report it and skip the talk.

## 3. Author

Answer every checker finding in a `## Author` section of the log, in the checker's numbering: **concede** or **contest**, with one sentence of reasons. Contest only after opening the transcript at the finding's timestamp; quote what you read. A challenge stands unless you can quote a moment that answers it against the rubric row; defend the verdict where the transcript carries it, never the score for its own sake. Missed material: say which criterion it moves and in which direction, or why it doesn't. End with your proposed scores, `Novelty <n> · Demonstrated <n> · Measured <n> · Depth <n> · Reusable <n>`.

## 4. Judge

Start one sub-agent with the judge, prompt:

```
Read .agents/skills/review-verdict/JUDGE.md and follow it for talk <id> in conference <slug>. Work from the repo root.
```

Done when the log has a `## Judge` section ending in a `### Ruling` subsection.

## 5. Apply

Replace the summary's `## Verdict` section with the ruling's Verdict text, unchanged, and set the front matter's `verdict:` to its total and `reviewedAt:` to today. Record the scores:

```
uv run scripts/catalog.py set <slug> <id> --status summarized --scores <novelty> <demonstrated> <measured> <depth> <reusable>
```

## Reply

One line per talk: `<id> reviewed <old total> -> <new total> <criteria that changed, e.g. "Measured 2->1"> (<n> findings, <n> conceded)`, or `<id> review skipped: <reason>`.
