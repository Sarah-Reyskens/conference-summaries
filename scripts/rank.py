#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Rank a conference's summarized talks against each other and assign tiers.

Absolute verdicts drift upward and say nothing about who can use a talk. This ranks every
summarized talk by its worth to the conference's audience (`audience` in conference.yaml)
through Swiss-style rounds: each round splits the talks into small groups of similar current
rating, an agent orders each group best first, and a Bradley-Terry fit over every pairwise
outcome gives each talk a rating. `fit` writes the ratings and quota-based tiers into the
catalog (catalog.TIERS) through catalog.py's locked writer.

State lives in conferences/<slug>/ranking.json, under a file lock, so groups can be judged
in parallel and a stopped run resumes where it left off.

Usage (from the repo root):
  uv run scripts/rank.py start  <slug> [--group-size N] [--rounds N]   # new ranking; discards the old one
  uv run scripts/rank.py next   <slug>                  # pending groups of the current round, opening the next round when due
  uv run scripts/rank.py group  <slug> <round> <group>  # the group's talks as briefs, in random order
  uv run scripts/rank.py record <slug> <round> <group> <id> [<id> ...]   # the group's ids, best first
  uv run scripts/rank.py status <slug>
  uv run scripts/rank.py fit    <slug>                  # ratings and tiers into the catalog
"""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import json
import math
import os
import random
import re
import sys

from catalog import ROOT, TIERS, conf_dir, load_conf, locked_catalog, minutes, now, read_catalog, section

MIN_GROUP = 3


@contextlib.contextmanager
def locked_state(slug: str, *, fresh: dict | None = None):
    """Yield ranking.json under an exclusive lock and write it back on exit; `fresh` replaces it."""
    path = conf_dir(slug) / "ranking.json"
    with open(path.with_suffix(".json.lock"), "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if fresh is not None:
            state = fresh
        elif path.exists():
            state = json.loads(path.read_text())
        else:
            sys.exit(f"no ranking yet: run `uv run scripts/rank.py start {slug}`")
        yield state
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
        os.replace(tmp, path)


def read_state(slug: str) -> dict:
    path = conf_dir(slug) / "ranking.json"
    if not path.exists():
        sys.exit(f"no ranking yet: run `uv run scripts/rank.py start {slug}`")
    return json.loads(path.read_text())


# ---------------------------------------------------------------- rating

def outcomes(state: dict):
    """Every recorded pairwise outcome as (winner, loser): in a group ordered best first, each talk beats every later one."""
    for rnd in state["history"]:
        for order in rnd["results"]:
            for i, winner in enumerate(order or []):
                for loser in order[i + 1:]:
                    yield winner, loser


def fit(state: dict) -> dict[str, float]:
    """Bradley-Terry strengths by minorization-maximization (Hunter 2004), as log-strength ratings.

    Each talk also plays one virtual win and one virtual loss against a fixed opponent of
    strength 1: this keeps unbeaten and winless talks finite and anchors the scale at 0.
    """
    ids = state["talks"]
    wins = {i: 1.0 for i in ids}
    games: dict[str, dict[str, int]] = {i: {} for i in ids}
    for w, l in outcomes(state):
        wins[w] += 1
        games[w][l] = games[w].get(l, 0) + 1
        games[l][w] = games[l].get(w, 0) + 1
    p = {i: 1.0 for i in ids}
    for _ in range(1000):
        new = {i: wins[i] / (sum(n / (p[i] + p[j]) for j, n in games[i].items()) + 2 / (p[i] + 1)) for i in ids}
        delta = max(abs(math.log(new[i] / p[i])) for i in ids)
        p = new
        if delta < 1e-9:
            break
    return {i: math.log(p[i]) for i in ids}


def tiers(ratings: dict[str, float]) -> dict[str, str]:
    """Assign catalog.TIERS by quota over the talks sorted best first."""
    ordered = sorted(ratings, key=lambda i: -ratings[i])
    out, start, cum = {}, 0, 0.0
    for name, share in TIERS:
        cum += share
        end = len(ordered) if name == TIERS[-1][0] else round(len(ordered) * cum)
        for i in ordered[start:end]:
            out[i] = name
        start = end
    return out


# ---------------------------------------------------------------- rounds

def make_round(state: dict) -> list[list[str]]:
    """Round 1 groups at random; later rounds group neighbours in rating order, the group
    boundaries shifting by half a group every other round so neighbours meet new talks."""
    size, n = state["groupSize"], len(state["history"])
    ids = list(state["talks"])
    random.shuffle(ids)
    if n:
        ratings = fit(state)
        ids.sort(key=lambda i: -ratings[i])  # stable: ties keep their random order
    offset = (size // 2) if n % 2 else 0
    groups = ([ids[:offset]] if offset else []) + [ids[k:k + size] for k in range(offset, len(ids), size)]
    if len(groups) > 1 and len(groups[-1]) < MIN_GROUP:
        groups[-2] += groups.pop()
    if len(groups) > 1 and len(groups[0]) < MIN_GROUP:
        groups[1] = groups.pop(0) + groups[1]
    return groups


def pending(rnd: dict) -> list[int]:
    return [g for g, order in enumerate(rnd["results"]) if order is None]


# ---------------------------------------------------------------- briefs

def brief(talk: dict) -> str:
    """What the ranker sees: the talk's frame, TL;DR, who it is for, and the verdict's head lines."""
    md = (ROOT / talk["summaryPath"]).read_text()
    m = re.search(r"^## Verdict\s*\n(.*?)(?=^## |\Z)", md, re.M | re.S)
    lines = [line for line in (m.group(1).splitlines() if m else []) if line.strip()]
    head = lines[:1] + [line for line in lines if line.startswith("**Reach ")][:1]
    return "\n".join([
        f"### {talk['id']}: {talk['title']}",
        f"{', '.join(talk['speakers'])} · {talk['sessionType']} · {talk['track']} · "
        f"{minutes(talk) or '?'} min · {(talk.get('audienceLevel') or '').title()}",
        "",
        f"TL;DR: {section(md, 'TL;DR')}",
        "",
        f"Who should watch: {section(md, 'Who should watch')}",
        "",
        *head,
        "",
    ])


# ---------------------------------------------------------------- commands

def cmd_start(args) -> None:
    talks = [t for t in read_catalog(args.slug)["talks"] if t["status"] == "summarized" and t.get("summaryPath")]
    stale = [t["id"] for t in talks if not t.get("reach")]
    if stale:
        sys.exit(f"{len(stale)} summarized talks have no reach (verdicts from an older rubric): "
                 f"rescore them first (`uv run scripts/catalog.py next {args.slug} --rescore`)")
    if len(talks) < 2 * MIN_GROUP:
        sys.exit(f"only {len(talks)} summarized talks: too few to rank")
    rounds = args.rounds or math.ceil(math.log2(len(talks))) + 2
    fresh = {"conference": args.slug, "startedAt": now(), "groupSize": args.group_size, "rounds": rounds,
             "talks": [t["id"] for t in talks], "history": []}
    with locked_state(args.slug, fresh=fresh) as state:
        groups = make_round(state)
        state["history"].append({"groups": groups, "results": [None] * len(groups)})
    print(json.dumps({"talks": len(talks), "rounds": rounds, "groupSize": args.group_size, "round": 1,
                      "pending": list(range(len(groups)))}))


def cmd_next(args) -> None:
    with locked_state(args.slug) as state:
        rnd = state["history"][-1]
        if not pending(rnd) and len(state["history"]) < state["rounds"]:
            groups = make_round(state)
            state["history"].append({"groups": groups, "results": [None] * len(groups)})
            rnd = state["history"][-1]
        left = pending(rnd)
        out = {"round": len(state["history"]), "rounds": state["rounds"], "pending": left}
        if not left:
            out = {"done": True, "rounds": state["rounds"]}
    print(json.dumps(out))


def get_group(state: dict, rnd: int, group: int) -> list[str]:
    if not 1 <= rnd <= len(state["history"]) or not 0 <= group < len(state["history"][rnd - 1]["groups"]):
        sys.exit(f"no group {group} in round {rnd}")
    return state["history"][rnd - 1]["groups"][group]


def cmd_group(args) -> None:
    ids = list(get_group(read_state(args.slug), args.round, args.group))
    random.shuffle(ids)  # no position the ranker could learn to favour
    by_id = {t["id"]: t for t in read_catalog(args.slug)["talks"]}
    conf = load_conf(args.slug)
    print(f"# Round {args.round}, group {args.group}: {len(ids)} talks\n\n"
          f"Audience of {conf['name']}: {' '.join(str(conf.get('audience') or 'not described').split())}\n")
    print("\n".join(brief(by_id[i]) for i in ids))


def cmd_record(args) -> None:
    with locked_state(args.slug) as state:
        ids = get_group(state, args.round, args.group)
        if sorted(args.ids) != sorted(ids):
            sys.exit(f"round {args.round} group {args.group} holds {' '.join(sorted(ids))}; pass each exactly once, best first")
        state["history"][args.round - 1]["results"][args.group] = args.ids
    print(json.dumps({"round": args.round, "group": args.group, "order": args.ids}))


def cmd_status(args) -> None:
    state = read_state(args.slug)
    rnd = state["history"][-1]
    ranked = set(state["talks"])
    summarized = [t for t in read_catalog(args.slug)["talks"] if t["status"] == "summarized" and t.get("summaryPath")]
    # talks summarized or rescored since the ranking started, and ranked talks no longer summarized
    stale = sorted({t["id"] for t in summarized if t["id"] not in ranked or (t.get("updatedAt") or "") > state["startedAt"]}
                   | (ranked - {t["id"] for t in summarized}))
    print(json.dumps({"talks": len(state["talks"]), "rounds": state["rounds"], "round": len(state["history"]),
                      "groups": len(rnd["groups"]), "pending": pending(rnd),
                      "comparisons": sum(1 for _ in outcomes(state)), "startedAt": state["startedAt"], "stale": stale}))


def cmd_fit(args) -> None:
    state = read_state(args.slug)
    complete = len(state["history"]) == state["rounds"] and not pending(state["history"][-1])
    ratings = fit(state)
    tier = tiers(ratings)
    with locked_catalog(args.slug) as cat:
        for t in cat["talks"]:
            ranked = t["id"] in ratings and t["status"] == "summarized"
            t["rating"] = round(ratings[t["id"]], 3) if ranked else None
            t["tier"] = tier[t["id"]] if ranked else None
        titles = {t["id"]: t["title"] for t in cat["talks"]}
    counts = {name: sum(1 for v in tier.values() if v == name) for name, _ in TIERS}
    top = sorted(ratings, key=lambda i: -ratings[i])[: counts[TIERS[0][0]] + counts[TIERS[1][0]]]
    print(json.dumps({"complete": complete, "tiers": counts,
                      "top": [{"id": i, "tier": tier[i], "rating": round(ratings[i], 3), "title": titles[i]} for i in top]},
                     indent=2, ensure_ascii=False))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start"); s.add_argument("slug")
    s.add_argument("--group-size", type=int, default=6, choices=range(MIN_GROUP, 11), metavar=f"{MIN_GROUP}-10")
    s.add_argument("--rounds", type=int, help="default: ceil(log2 talks) + 2")
    s.set_defaults(fn=cmd_start)
    n = sub.add_parser("next"); n.add_argument("slug"); n.set_defaults(fn=cmd_next)
    g = sub.add_parser("group"); g.add_argument("slug"); g.add_argument("round", type=int); g.add_argument("group", type=int)
    g.set_defaults(fn=cmd_group)
    r = sub.add_parser("record"); r.add_argument("slug"); r.add_argument("round", type=int); r.add_argument("group", type=int)
    r.add_argument("ids", nargs="+", help="the group's talk ids, best first"); r.set_defaults(fn=cmd_record)
    st = sub.add_parser("status"); st.add_argument("slug"); st.set_defaults(fn=cmd_status)
    f = sub.add_parser("fit"); f.add_argument("slug"); f.set_defaults(fn=cmd_fit)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
