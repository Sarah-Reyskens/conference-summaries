---
name: rank-talks
description: Rank a conference's summarized talks against each other by their worth to its audience and assign tiers (must-watch, recommended, if-relevant, low-priority) with parallel sub-agents.
disable-model-invocation: true
---

Input: a conference slug (default: the only directory under `conferences/`), optionally `restart` to discard an existing ranking, and optionally `ranker=<name>`: the sub-agent, model or role alias that orders the groups, passed unchanged to your harness's sub-agent mechanism (default: the harness's default sub-agent). Run every command from the repo root.

Why this exists: a verdict rates a talk's quality for its subject, and absolute scores drift upward run after run. Agents order a handful of talks more reliably than they place one talk on a fixed scale, so `scripts/rank.py` runs Swiss-style rounds: each round splits the talks into groups of about 6 with similar current ratings, a sub-agent orders each group by worth to the conference's audience, and a Bradley-Terry fit over every pairwise outcome rates each talk. Tiers are quotas over that order (`TIERS` in `scripts/catalog.py`), so "must-watch" always means the top few.

You are the orchestrator: sub-agents order the groups and record their own results in `conferences/<slug>/ranking.json`, so a stopped run resumes where it left off.

## 1. Start or resume

`uv run scripts/rank.py status <slug>`:

- No ranking yet, `restart` given, or `stale` non-empty (talks summarized, rescored or reviewed since the ranking started): `uv run scripts/rank.py start <slug>`. It refuses while any summarized talk has no reach: report that the verdicts need a rescore first (`summarize-backlog` with `rescore`) and stop.
- Otherwise resume.

## 2. Rounds

Repeat until `uv run scripts/rank.py next <slug>` prints `"done": true`. Each `next` lists the current round's `pending` group numbers, opening the next round once the current one is complete.

Split the pending groups into batches of at most 5, start one sub-agent per batch with the ranker, at most 6 at a time, and wait for all of them before the next `next`. Each sub-agent's prompt:

```
Read .agents/skills/rank-talks/RANKER.md and follow it for conference <slug>, round <round>, groups <g1> <g2> …. Work from the repo root. End with its one-line replies.
```

A group still pending after two dispatches: stop and report the round, the group and the sub-agent's last reply.

## 3. Fit

`uv run scripts/rank.py fit <slug>` writes each talk's `rating` and `tier` into the catalog and regenerates `summaries/INDEX.md`, which opens with the must-watch and recommended talks across tracks.

## Reply

The tier counts, then the must-watch and recommended talks as a table (tier, title, verdict, reach, track) from `uv run scripts/catalog.py find <slug> --tier must-watch --tier recommended --sort rating --limit 100`, then one line naming any talk with a verdict of 9–10 that landed in if-relevant or below, with its reach.
