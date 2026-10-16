---
name: summarize-backlog
description: Summarize the next batch of unsummarized catalog talks with parallel sub-agents, or rescore the verdicts of summarized talks after a rubric change.
disable-model-invocation: true
---

Input: a conference slug (default: the only directory under `conferences/`), an optional batch size (default 10), optionally `rescore` to redo the verdicts of summarized talks scored before Reach existed instead of summarizing new talks, and optionally `checker=<name> judge=<name>` to have every verdict reviewed. Run every command from the repo root.

You are the orchestrator: sub-agents do the summarizing and record their own results in the catalog. That makes a stopped run safe to restart: unfinished talks are still `matched` and come back in the next queue.

## 1. Queue

`uv run scripts/catalog.py next <slug> --limit <batch>` lists `matched` talks, then `failed` talks with fewer than 3 attempts. With `rescore`, `uv run scripts/catalog.py next <slug> --limit <batch> --rescore` lists summarized talks that have no reach yet. Empty queue → report `uv run scripts/catalog.py status <slug>` and stop; after a rescore, also say the ranking is due (`rank-talks`).

## 2. Dispatch

Only YouTube limits the pace: it answers bursts of caption requests with HTTP 429. So you fetch the transcripts yourself, at most 3 fetches at a time: `uv run scripts/transcript.py <slug> <id>` (instant when cached; exit 3 or 4 → record the talk as `summarize-talk` step 2 says and don't dispatch it). Once a talk's transcript is cached, it is past YouTube: start its sub-agent right away. With `rescore`, every transcript is already cached, so every talk can be dispatched immediately.

Keep at most 8 sub-agents running, and start the next talk as soon as one finishes; don't wait for a whole group. The cap leaves room for reviews: each talk then runs its own agent plus a checker or judge. Each sub-agent's prompt:

```
Read .agents/skills/summarize-talk/SKILL.md and follow it for talk <id> ("<title>") in conference <slug><, in rescore mode when rescoring><, with checker=<name> judge=<name> when given>. Work from the repo root. End with the skill's one-line reply.
```

A review makes each sub-agent start two of its own, so the harness must let sub-agents start sub-agents. Run the dispatch loop in the background when your harness allows it, so the user can steer while it runs.

## 3. Reconcile

For every dispatched talk, `uv run scripts/catalog.py show <slug> <id>`. A talk still `matched`, or `failed` with an unchanged attempt count, means its sub-agent ended without recording: `uv run scripts/catalog.py set <slug> <id> --status failed --error "sub-agent ended without recording a result"`. Done when every dispatched talk has a status other than `matched`. With `rescore`, a talk whose `reach` is still null was not rescored: leave its catalog entry untouched (it stays in the rescore queue) and list it in the report with the sub-agent's reason. With reviews, a summarized talk whose summary has no `reviewedAt:` was stopped during its review: run `review-verdict` for it with the same checker and judge.

## 4. Report

A table of the batch (id, title, status, verdict (old → new when rescoring), reach, reviewed old → new when reviews ran, summary path), then the overall status counts from `uv run scripts/catalog.py status <slug>`.
