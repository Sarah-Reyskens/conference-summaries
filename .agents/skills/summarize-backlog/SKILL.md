---
name: summarize-backlog
description: Summarize the next batch of unsummarized catalog talks with parallel sub-agents.
disable-model-invocation: true
---

Input: a conference slug (default: the only directory under `conferences/`), an optional batch size (default 10), and optionally `checker=<name> judge=<name>` to have every verdict reviewed. Run every command from the repo root.

You are the orchestrator: sub-agents do the summarizing and record their own results in the catalog. That makes a stopped run safe to restart: unfinished talks are still `matched` and come back in the next queue.

## 1. Queue

`uv run scripts/catalog.py next <slug> --limit <batch>` lists `matched` talks, then `failed` talks with fewer than 3 attempts. Empty queue → report `uv run scripts/catalog.py status <slug>` and stop.

## 2. Dispatch in waves of 3

Split the queue into waves of at most 3 talks. For each wave, start one sub-agent per talk, all in parallel, and wait for the wave to finish before starting the next. Each sub-agent's prompt:

```
Read .agents/skills/summarize-talk/SKILL.md and follow it for talk <id> ("<title>") in conference <slug><, with checker=<name> judge=<name> when given>. Work from the repo root. End with the skill's one-line reply.
```

A review makes each sub-agent start two of its own, so the harness must let sub-agents start sub-agents.

## 3. Reconcile

For every dispatched talk, `uv run scripts/catalog.py show <slug> <id>`. A talk still `matched`, or `failed` with an unchanged attempt count, means its sub-agent ended without recording: `uv run scripts/catalog.py set <slug> <id> --status failed --error "sub-agent ended without recording a result"`. Done when every dispatched talk has a status other than `matched`.

## 4. Report

A table of the batch (id, title, status, verdict, reviewed old → new when reviews ran, summary path), then the overall status counts from `uv run scripts/catalog.py status <slug>`.
