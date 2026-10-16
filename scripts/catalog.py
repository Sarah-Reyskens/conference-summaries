#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Conference catalog: build/re-match from a conference file, query, and update talk status.

Every write to catalog.json goes through this script under an exclusive file lock,
so concurrent summarize-talk runs never clobber each other. Each write also regenerates
summaries/INDEX.md.

Usage (from the repo root):
  uv run scripts/catalog.py build  <slug>
  uv run scripts/catalog.py status <slug>
  uv run scripts/catalog.py show   <slug> <talk-id | title fragment>
  uv run scripts/catalog.py next   <slug> [--limit N] [--rescore]   # --rescore: summarized talks without a reach
  uv run scripts/catalog.py path   <slug> <talk-id>          # where the talk's summary belongs
  uv run scripts/catalog.py find   <slug> [--text T ...] [--track T] [--type T] [--level L]
                                   [--min-minutes N] [--max-minutes N] [--min-verdict N] [--min-favourites N]
                                   [--min-novelty N] [--min-demonstrated N] [--min-measured N] [--min-depth N] [--min-reusable N]
                                   [--reach R ...] [--tier T ...] [--day D ...]
                                   [--sort relevance|time|favourites|rating|verdict|<criterion>] [--status S]
  uv run scripts/catalog.py index  <slug>
  uv run scripts/catalog.py set    <slug> <talk-id> --status S [--summary P] [--transcript P] [--slides URL|none]
                                   [--scores NOV DEM MEA DEP REU --reach niche|segment|broad] [--error MSG]

Tiers and ratings are written by scripts/rank.py, through this script's locked writer.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import difflib
import fcntl
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

ROOT = Path(__file__).resolve().parent.parent
STATUSES = ("excluded", "no-video", "needs-review", "matched", "summarized", "no-transcript", "failed")
# Statuses a rebuild may re-match; everything else keeps its video and progress.
REMATCHABLE = {"excluded", "no-video", "needs-review"}
MAX_ATTEMPTS = 3
# Verdict criteria, in the order of SUMMARY-FORMAT.md; each 0-2, the verdict is their sum.
CRITERIA = ("novelty", "demonstrated", "measured", "depth", "reusable")
# Who in the conference's audience can use a talk's main content (SUMMARY-FORMAT.md, "Reach").
REACH = ("niche", "segment", "broad")
# Ranking tiers, best first, with the share of ranked talks each takes (scripts/rank.py assigns them).
TIERS = (("must-watch", 0.05), ("recommended", 0.15), ("if-relevant", 0.40), ("low-priority", 0.40))
TIER_NAMES = tuple(name for name, _ in TIERS)


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def conf_dir(slug: str) -> Path:
    d = ROOT / "conferences" / slug
    if not (d / "conference.yaml").is_file():
        sys.exit(f"no conference file: {d / 'conference.yaml'}")
    return d


def load_conf(slug: str) -> dict:
    return yaml.safe_load((conf_dir(slug) / "conference.yaml").read_text())


@contextlib.contextmanager
def locked_catalog(slug: str, *, create: bool = False):
    """Yield the catalog dict under an exclusive lock; write it back atomically on exit."""
    path = conf_dir(slug) / "catalog.json"
    with open(path.with_suffix(".json.lock"), "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if path.exists():
            cat = json.loads(path.read_text())
        elif create:
            cat = {"conference": slug, "generatedAt": None, "talks": []}
        else:
            sys.exit(f"no catalog yet: run `uv run scripts/catalog.py build {slug}`")
        yield cat
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(cat, indent=2, ensure_ascii=False) + "\n")
        os.replace(tmp, path)
        write_index(slug, cat)


def read_catalog(slug: str) -> dict:
    path = conf_dir(slug) / "catalog.json"
    if not path.exists():
        sys.exit(f"no catalog yet: run `uv run scripts/catalog.py build {slug}`")
    return json.loads(path.read_text())


# ---------------------------------------------------------------- talk sources

def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "talk-catalog"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def source_devoxx_cfp(cfg: dict) -> list[dict]:
    """cfp.dev public API, shared by Devoxx / VoxxedDays events."""
    base = cfg["baseUrl"].rstrip("/")
    talks = fetch_json(f"{base}/talks")
    slots: dict[int, dict] = {}
    for link in fetch_json(f"{base}/schedules").get("links", []):
        for entry in fetch_json(link["href"]):
            pid = (entry.get("proposal") or {}).get("id")
            if pid and pid not in slots:
                slots[pid] = {"start": entry.get("fromDate"), "timezone": entry.get("timezone"),
                              "room": (entry.get("room") or {}).get("name")}
    out = []
    for t in talks:
        st = t.get("sessionType") or {}
        slot = slots.get(t["id"], {})
        out.append({
            "id": str(t["id"]),
            "title": t["title"].strip(),
            "speakers": [s.get("fullName") or f"{s.get('firstName', '')} {s.get('lastName', '')}".strip()
                         for s in t.get("speakers") or []],
            "track": (t.get("track") or {}).get("name"),
            "sessionType": st.get("name"),
            "durationMin": st.get("duration"),
            "audienceLevel": t.get("audienceLevel"),
            "start": slot.get("start"),
            "timezone": slot.get("timezone"),
            "room": slot.get("room"),
            # Attendees who bookmarked the talk in the schedule: interest, not a rating.
            "favourites": t.get("totalFavourites"),
            "keywords": [k["name"] if isinstance(k, dict) else k for k in t.get("keywords") or []],
            "abstract": (t.get("summary") or t.get("description") or "").strip(),
        })
    return out


SOURCES = {"devoxx-cfp": source_devoxx_cfp}


def fetch_videos(cfg: dict) -> list[dict]:
    seen: dict[str, dict] = {}
    for url in cfg["playlists"]:
        res = subprocess.run(["yt-dlp", "--flat-playlist", "-J", url], capture_output=True, text=True)
        if res.returncode != 0:
            sys.exit(f"yt-dlp failed for {url}:\n{res.stderr[-2000:]}")
        for e in json.loads(res.stdout).get("entries") or []:
            # Untitled entries are private/deleted videos.
            if e.get("id") and e.get("title") and e["id"] not in seen:
                seen[e["id"]] = {"id": e["id"], "title": e["title"], "durationSec": e.get("duration")}
    return list(seen.values())


# ---------------------------------------------------------------- matching

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def score(talk: dict, video: dict, suffix: re.Pattern) -> float:
    t = norm(talk["title"])
    raw = video["title"]
    # Score both with and without the speaker suffix: a CFP title may itself contain " by ".
    variants = {norm(suffix.sub("", raw)), norm(raw)}
    best = 0.0
    for v in variants:
        if not v:
            continue
        r = difflib.SequenceMatcher(None, t, v).ratio()
        # YouTube cuts titles at 100 chars: a long-enough prefix is a near-certain match.
        if len(v) >= 20 and t.startswith(v):
            r = max(r, 0.95)
        best = max(best, r)
    vt = norm(raw)
    surnames = [norm(s).split()[-1] for s in talk["speakers"] if norm(s)]
    if any(f" {n}" in f" {vt}" for n in surnames if len(n) > 2):
        best = min(1.0, best + 0.05)
    return round(best, 3)


def video_ref(v: dict, sc: float | None) -> dict:
    return {"id": v["id"], "url": f"https://www.youtube.com/watch?v={v['id']}", "title": v["title"],
            "durationSec": v.get("durationSec"), "score": sc}


def cmd_build(args) -> None:
    conf = load_conf(args.slug)
    tcfg, vcfg, mcfg = conf["talks"], conf["videos"], conf.get("matching", {})
    accept, review = mcfg.get("accept", 0.85), mcfg.get("review", 0.60)
    excluded_types = set(conf.get("excludeSessionTypes") or [])
    overrides = {str(k): v for k, v in (conf.get("overrides") or {}).items()}
    suffix = re.compile(vcfg.get("titleSuffix", r"$^"), re.IGNORECASE)

    fresh = SOURCES[tcfg["source"]](tcfg)
    videos = fetch_videos(vcfg)
    by_vid = {v["id"]: v for v in videos}
    print(f"fetched {len(fresh)} talks, {len(videos)} videos", file=sys.stderr)

    with locked_catalog(args.slug, create=True) as cat:
        old = {t["id"]: t for t in cat["talks"]}
        talks = []
        for f in fresh:
            prev = old.get(f["id"], {})
            t = {**f}
            for k in ("status", "video", "candidate", "transcriptPath", "summaryPath", "slides", "verdict", "scores",
                      "reach", "rating", "tier", "attempts", "error", "updatedAt"):
                t[k] = prev.get(k)
            t["attempts"] = t["attempts"] or 0
            talks.append(t)

        taken: set[str] = set()
        pending: list[dict] = []
        for t in talks:
            if t["id"] in overrides:
                vid = overrides[t["id"]]
                if vid is None:
                    new = {"status": "no-video", "video": None}
                else:
                    v = by_vid.get(vid, {"id": vid, "title": None, "durationSec": None})
                    new = {"status": t["status"] if t["status"] not in REMATCHABLE and (t["video"] or {}).get("id") == vid else "matched",
                           "video": video_ref(v, None)}
                    taken.add(vid)
                if (t["status"], (t["video"] or {}).get("id")) != (new["status"], (new["video"] or {}).get("id")):
                    t.update(new, candidate=None, updatedAt=now())
            elif t["status"] and t["status"] not in REMATCHABLE:
                taken.add(t["video"]["id"])
            elif t["sessionType"] in excluded_types:
                if t["status"] != "excluded":
                    t.update(status="excluded", video=None, candidate=None, updatedAt=now())
            else:
                pending.append(t)

        pairs = []
        for t in pending:
            for v in videos:
                if v["id"] not in taken:
                    sc = score(t, v, suffix)
                    if sc >= review:
                        pairs.append((sc, t["id"], v["id"]))
        pairs.sort(reverse=True)
        best: dict[str, tuple[float, str]] = {}
        for sc, tid, vid in pairs:
            if tid in best or vid in taken:
                continue
            best[tid] = (sc, vid)
            taken.add(vid)
        for t in pending:
            sc, vid = best.get(t["id"], (0.0, None))
            if vid and sc >= accept:
                new = dict(status="matched", video=video_ref(by_vid[vid], sc), candidate=None)
            elif vid:
                new = dict(status="needs-review", video=None,
                           candidate={"id": vid, "title": by_vid[vid]["title"], "score": sc})
            else:
                new = dict(status="no-video", video=None, candidate=None)
            if any(t.get(k) != v for k, v in new.items()):
                t.update(new, updatedAt=now())

        talks.sort(key=lambda t: (t["start"] or "9999", t["title"]))
        cat.update(conference=args.slug, generatedAt=now(), talks=talks)

    print_status(cat, detail=True)


# ---------------------------------------------------------------- queries / updates

def print_status(cat: dict, detail: bool = False) -> None:
    counts = {s: 0 for s in STATUSES}
    for t in cat["talks"]:
        counts[t["status"]] += 1
    print(json.dumps({"total": len(cat["talks"]), **counts}))
    if detail:
        for t in cat["talks"]:
            if t["status"] == "needs-review":
                c = t["candidate"]
                print(f"needs-review {t['id']}: {t['title']!r} ~ {c['id']} {c['title']!r} ({c['score']})")
        for t in cat["talks"]:
            if t["status"] == "no-video":
                print(f"no-video     {t['id']}: {t['title']!r} [{t['sessionType']}]")


def cmd_status(args) -> None:
    print_status(read_catalog(args.slug), detail=args.detail)


def cmd_next(args) -> None:
    talks = read_catalog(args.slug)["talks"]
    if args.rescore:
        queue = [t for t in talks if t["status"] == "summarized" and not t.get("reach")]
    else:
        queue = [t for t in talks if t["status"] == "matched"]
        queue += [t for t in talks if t["status"] == "failed" and t["attempts"] < MAX_ATTEMPTS]
    print(json.dumps([{"id": t["id"], "title": t["title"], "status": t["status"], "attempts": t["attempts"]}
                      for t in queue[: args.limit]], indent=2, ensure_ascii=False))


def find(talks: list[dict], key: str) -> list[dict]:
    exact = [t for t in talks if t["id"] == key]
    return exact or [t for t in talks if norm(key) in norm(t["title"])]


def cmd_show(args) -> None:
    hits = find(read_catalog(args.slug)["talks"], args.talk)
    if len(hits) != 1:
        print(json.dumps([{"id": t["id"], "title": t["title"], "status": t["status"]} for t in hits], indent=2, ensure_ascii=False))
        sys.exit(f"{len(hits)} talks match {args.talk!r}; pass an exact id")
    print(json.dumps(hits[0], indent=2, ensure_ascii=False))


def cmd_set(args) -> None:
    if (args.scores is None) != (args.reach is None):
        sys.exit("--scores and --reach go together: a verdict is its five criteria plus its reach")
    with locked_catalog(args.slug) as cat:
        t = next((t for t in cat["talks"] if t["id"] == args.talk), None)
        if t is None:
            sys.exit(f"no talk with id {args.talk}")
        t["status"] = args.status
        if args.summary is not None:
            t["summaryPath"] = args.summary
        if args.transcript is not None:
            t["transcriptPath"] = args.transcript
        if args.slides is not None:
            t["slides"] = None if args.slides == "none" else args.slides
        if args.scores is not None:
            t["scores"] = dict(zip(CRITERIA, args.scores))
            t["verdict"] = sum(args.scores)
            t["reach"] = args.reach
        if args.status != "summarized":
            # a verdict, reach and ranking belong to a summary
            t["verdict"] = t["scores"] = t["reach"] = t["rating"] = t["tier"] = None
        if args.status == "failed":
            t["attempts"] = (t["attempts"] or 0) + 1
            t["error"] = args.error or "unspecified"
        else:
            t["error"] = args.error
        t["updatedAt"] = now()
    print(json.dumps({k: t.get(k) for k in ("id", "status", "attempts", "summaryPath", "slides", "verdict", "scores", "reach", "tier", "error")}, ensure_ascii=False))


# ---------------------------------------------------------------- summary paths, index, search

def slugify(s: str, limit: int = 60) -> str:
    words, out = norm(s).split(), ""
    for w in words:
        if len(out) + len(w) + 1 > limit:
            break
        out = f"{out}-{w}" if out else w
    return out or "untitled"


def summary_path(slug: str, talk: dict) -> Path:
    """Where a talk's summary lives: summaries/<track-slug>/<id>-<title-slug>.md."""
    return ROOT / "conferences" / slug / "summaries" / slugify(talk["track"] or "other") / f"{talk['id']}-{slugify(talk['title'])}.md"


def minutes(t: dict) -> int | None:
    sec = (t.get("video") or {}).get("durationSec")
    return round(sec / 60) if sec else t.get("durationMin")


def local_start(t: dict) -> dt.datetime | None:
    if not t.get("start"):
        return None
    start = dt.datetime.fromisoformat(t["start"].replace("Z", "+00:00"))
    return start.astimezone(ZoneInfo(t["timezone"])) if t.get("timezone") else start


def when(t: dict) -> str:
    """Local slot as 'Mon 10:30, Room 4' (empty when unscheduled)."""
    start = local_start(t)
    return ", ".join(x for x in (start and start.strftime("%a %H:%M"), t.get("room")) if x)


def on_day(t: dict, day: str) -> bool:
    """day: weekday name or abbreviation (mon, tuesday) or local date YYYY-MM-DD."""
    start = local_start(t)
    if start is None:
        return False
    day = day.lower()
    return start.date().isoformat() == day or start.strftime("%A").lower().startswith(day[:3])


def anchor(heading: str) -> str:
    return re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")


def rank_key(t: dict) -> tuple:
    """Best first: tier, then ranking rating, then verdict; unranked talks after every tier."""
    tier = TIER_NAMES.index(t["tier"]) if t.get("tier") in TIER_NAMES else len(TIER_NAMES)
    return tier, -(t.get("rating") or 0.0), -(t.get("verdict") or 0), t["title"]


def index_rows(slug: str, talks: list[dict]) -> list[str]:
    lines = ["| Tier | Verdict | Reach | Talk | Speakers | When | Type | Min | Level | Favs | Slides |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in talks:
        rel = Path(t["summaryPath"]).relative_to(f"conferences/{slug}/summaries").as_posix()
        title = t["title"].replace("|", "\\|")
        slides = f"[deck]({t['slides']})" if t.get("slides") else ""
        verdict = "" if t.get("verdict") is None else t["verdict"]
        lines.append(f"| {t.get('tier') or ''} | {verdict} | {t.get('reach') or ''} | [{title}]({rel}) | {', '.join(t['speakers'])} "
                     f"| {when(t)} | {t['sessionType']} | {minutes(t) or ''} | {(t.get('audienceLevel') or '').title()} "
                     f"| {t.get('favourites') or ''} | {slides} |")
    return lines + [""]


def write_index(slug: str, cat: dict) -> None:
    """Regenerate summaries/INDEX.md: top picks across tracks, then summarized talks by track, best ranked first."""
    sdir = conf_dir(slug) / "summaries"
    sdir.mkdir(exist_ok=True)
    eligible = [t for t in cat["talks"] if t["status"] != "excluded"]
    done = sorted((t for t in eligible if t["status"] == "summarized" and t.get("summaryPath")), key=rank_key)
    picks = [t for t in done if t.get("tier") in TIER_NAMES[:2]]
    tracks = sorted({t["track"] or "Other" for t in eligible})
    picks_heading = f"{TIER_NAMES[0].capitalize()} and {TIER_NAMES[1]}"
    toc = [f"[{picks_heading}](#{anchor(picks_heading)}) ({len(picks)})"] if picks else []
    toc += [f"[{tr}](#{anchor(tr)}) ({sum(1 for t in done if (t['track'] or 'Other') == tr)})" for tr in tracks]
    lines = [f"# {load_conf(slug)['name']}: talk summaries", "",
             f"{len(done)} of {len(eligible)} talks summarized. Generated by `scripts/catalog.py` on every catalog write; edits here are overwritten.", "",
             " · ".join(toc), ""]
    if picks:
        lines += [f"## {picks_heading}", "",
                  "Across all tracks, from the ranking of every summarized talk by its worth to this conference's audience.", ""]
        lines += index_rows(slug, picks)
    for tr in tracks:
        in_track = [t for t in eligible if (t["track"] or "Other") == tr]
        rows = [t for t in done if (t["track"] or "Other") == tr]
        lines += [f"## {tr}", "", f"{len(rows)} of {len(in_track)} talks summarized.", ""]
        if rows:
            lines += index_rows(slug, rows)
    lines += ["*Tier*: the talk's place in a ranking of all summarized talks by how much watching it is worth to this conference's "
              "audience (" + ", ".join(f"{name} {round(share * 100)}%" for name, share in TIERS) + " of ranked talks). "
              "*Verdict*: the talk's quality for its subject, 0–10. "
              "*Reach*: how much of the audience can use its main content (niche, segment, broad). "
              "*Favs*: attendees who bookmarked the talk in the conference schedule (interest before the talk, not a rating).", ""]
    (sdir / "INDEX.md").write_text("\n".join(lines))


def cmd_path(args) -> None:
    t = next((t for t in read_catalog(args.slug)["talks"] if t["id"] == args.talk), None)
    if t is None:
        sys.exit(f"no talk with id {args.talk}")
    print(summary_path(args.slug, t).relative_to(ROOT))


def cmd_index(args) -> None:
    write_index(args.slug, read_catalog(args.slug))
    print((conf_dir(args.slug) / "summaries" / "INDEX.md").relative_to(ROOT))


def section(md: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", md, re.M | re.S)
    return " ".join(m.group(1).split()) if m else ""


def cmd_find(args) -> None:
    lc = lambda s: (s or "").lower()
    hits = []
    for t in read_catalog(args.slug)["talks"]:
        if t["status"] == "excluded":
            continue
        summarized = t["status"] == "summarized" and t.get("summaryPath")
        if args.status == "summarized" and not summarized or args.status == "unsummarized" and summarized:
            continue
        mins = minutes(t)
        if (args.track and lc(args.track) not in lc(t["track"])
                or args.type and lc(args.type) not in lc(t["sessionType"])
                or args.level and lc(args.level) != lc(t.get("audienceLevel"))
                or args.min_minutes and (mins or 0) < args.min_minutes
                or args.max_minutes and (mins or 10**6) > args.max_minutes
                or args.min_verdict is not None and (t.get("verdict") or 0) < args.min_verdict
                or args.min_favourites and (t.get("favourites") or 0) < args.min_favourites
                or args.reach and t.get("reach") not in args.reach
                or args.tier and t.get("tier") not in args.tier
                or args.day and not any(on_day(t, d) for d in args.day)
                or any(getattr(args, f"min_{c}") is not None and (t.get("scores") or {}).get(c, 0) < getattr(args, f"min_{c}")
                       for c in CRITERIA)):
            continue
        md = (ROOT / t["summaryPath"]).read_text() if summarized and (ROOT / t["summaryPath"]).exists() else ""
        abstract = re.sub(r"<[^>]+>", " ", t["abstract"])
        haystack = lc(" ".join([t["title"], abstract, " ".join(t.get("keywords") or []), " ".join(t["speakers"]), md]))
        matched = [term for term in args.text if re.search(rf"\b{re.escape(term.lower())}\b", haystack)]
        if args.text and not matched:
            continue
        brief = section(md, "TL;DR") or " ".join(abstract.split())
        hits.append({"id": t["id"], "title": t["title"], "speakers": t["speakers"], "track": t["track"],
                     "sessionType": t["sessionType"], "minutes": mins, "level": t.get("audienceLevel"),
                     "when": when(t), "start": t.get("start"), "favourites": t.get("favourites"),
                     "verdict": t.get("verdict"), "scores": t.get("scores"), "reach": t.get("reach"),
                     "tier": t.get("tier"), "rating": t.get("rating"), "summarized": bool(summarized), "summaryPath": t.get("summaryPath"),
                     "slides": t.get("slides"), "video": (t.get("video") or {}).get("url"),
                     "keywords": t.get("keywords"), "matched": matched, "brief": brief[:500]})
    orders = {
        "relevance": lambda h: (-len(h["matched"]), *rank_key(h)[:3], -(h["favourites"] or 0), h["title"]),
        "time": lambda h: (h["start"] or "9999", h["title"]),
        "favourites": lambda h: (-(h["favourites"] or 0), h["title"]),
        "rating": lambda h: (*rank_key(h)[:3], -(h["favourites"] or 0), h["title"]),
        "verdict": lambda h: (-(h["verdict"] or 0), -(h["favourites"] or 0), h["title"]),
        **{c: (lambda c: lambda h: (-(h["scores"] or {}).get(c, -1), -(h["verdict"] or 0), h["title"]))(c) for c in CRITERIA},
    }
    hits.sort(key=orders[args.sort])
    print(json.dumps({"total": len(hits), "talks": hits[: args.limit]}, indent=2, ensure_ascii=False))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("slug"); b.set_defaults(fn=cmd_build)
    s = sub.add_parser("status"); s.add_argument("slug"); s.add_argument("--detail", action="store_true"); s.set_defaults(fn=cmd_status)
    n = sub.add_parser("next"); n.add_argument("slug"); n.add_argument("--limit", type=int, default=10)
    n.add_argument("--rescore", action="store_true", help="summarized talks whose verdict predates reach"); n.set_defaults(fn=cmd_next)
    sh = sub.add_parser("show"); sh.add_argument("slug"); sh.add_argument("talk"); sh.set_defaults(fn=cmd_show)
    pa = sub.add_parser("path"); pa.add_argument("slug"); pa.add_argument("talk"); pa.set_defaults(fn=cmd_path)
    ix = sub.add_parser("index"); ix.add_argument("slug"); ix.set_defaults(fn=cmd_index)
    f = sub.add_parser("find"); f.add_argument("slug")
    f.add_argument("--text", action="append", default=[], help="word/phrase; repeat for synonyms (any matches)")
    f.add_argument("--track"); f.add_argument("--type", help="session type substring")
    f.add_argument("--level", choices=["BEGINNER", "INTERMEDIATE", "ADVANCED"], type=str.upper)
    f.add_argument("--min-minutes", type=int); f.add_argument("--max-minutes", type=int)
    f.add_argument("--min-verdict", type=int, choices=range(0, 11), metavar="0-10")
    f.add_argument("--min-favourites", type=int, help="schedule bookmarks (interest, not a rating)")
    for c in CRITERIA:
        f.add_argument(f"--min-{c}", type=int, choices=range(0, 3), metavar="0-2", help=f"verdict criterion {c}")
    f.add_argument("--reach", action="append", choices=REACH, help="repeatable; any matches")
    f.add_argument("--tier", action="append", choices=TIER_NAMES, help="ranking tier; repeatable, any matches")
    f.add_argument("--day", action="append", default=[], help="weekday (mon, tuesday) or YYYY-MM-DD, local time; repeatable")
    f.add_argument("--sort", choices=["relevance", "time", "favourites", "rating", "verdict", *CRITERIA], default="relevance")
    f.add_argument("--status", choices=["any", "summarized", "unsummarized"], default="any")
    f.add_argument("--limit", type=int, default=30)
    f.set_defaults(fn=cmd_find)
    st = sub.add_parser("set"); st.add_argument("slug"); st.add_argument("talk")
    st.add_argument("--status", required=True, choices=STATUSES)
    st.add_argument("--summary"); st.add_argument("--transcript"); st.add_argument("--slides")
    st.add_argument("--scores", type=int, nargs=5, choices=range(0, 3), metavar=tuple(c[:3].upper() for c in CRITERIA),
                    help="verdict criteria 0-2 in order " + " ".join(CRITERIA) + "; the verdict is their sum")
    st.add_argument("--reach", choices=REACH, help="who in the conference audience can use the talk; required with --scores")
    st.add_argument("--error")
    st.set_defaults(fn=cmd_set)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
