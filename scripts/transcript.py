#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Fetch a talk's YouTube auto-captions and cache them as `[mm:ss] text` paragraphs.

Usage (from the repo root):
  uv run scripts/transcript.py <slug> <talk-id>

Prints the transcript path (repo-relative) on stdout.
Exit codes: 0 ok (cached or fetched) | 3 video has no captions in the configured language | 4 fetch failed.
Throttling (HTTP 429) is retried once after 60 s before exiting 4.
"""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PARAGRAPH_SEC = 30
CUE = re.compile(r"^(\d+):(\d\d):(\d\d)\.(\d+) --> (\d+):(\d\d):(\d\d)\.(\d+)")
TAG = re.compile(r"<[^>]+>")


def clean_vtt(vtt: str) -> str:
    """Auto-caption VTT repeats each line in the next cue (rolling window); keep each line once."""
    lines: list[tuple[float, str]] = []
    start = None
    for raw in vtt.splitlines():
        m = CUE.match(raw)
        if m:
            h, mi, s, ms = map(int, m.groups()[:4])
            start = h * 3600 + mi * 60 + s + ms / 1000
            continue
        if start is None or not raw.strip():
            continue
        text = " ".join(html.unescape(TAG.sub("", raw)).split())
        if text and (not lines or lines[-1][1] != text):
            lines.append((start, text))
    paras: list[str] = []
    cur_start, cur = None, []
    for ts, text in lines:
        if cur_start is None:
            cur_start = ts
        elif ts - cur_start >= PARAGRAPH_SEC:
            paras.append(f"[{int(cur_start // 60):02d}:{int(cur_start % 60):02d}] {' '.join(cur)}")
            cur_start, cur = ts, []
        cur.append(text)
    if cur:
        paras.append(f"[{int(cur_start // 60):02d}:{int(cur_start % 60):02d}] {' '.join(cur)}")
    return "\n".join(paras) + "\n"


def download(video_id: str, lang: str, out: Path) -> tuple[Path | None, str]:
    # Fall back from the configured original track (e.g. en-orig) to the merged
    # track (en): some videos only carry the latter.
    langs = lang if "," in lang or lang == "en" else f"{lang},en"
    res = subprocess.run(
        ["yt-dlp", "--skip-download", "--write-auto-subs", "--sub-langs", langs, "--sub-format", "vtt",
         "-o", str(out / "%(id)s"), f"https://www.youtube.com/watch?v={video_id}"],
        capture_output=True, text=True)
    files = [f for f in out.glob(f"{video_id}*.vtt") if ".en-orig." in f.name or ".en." in f.name] or list(out.glob(f"{video_id}*.vtt"))
    return (files[0] if files else None), res.stdout + res.stderr


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    slug, talk_id = sys.argv[1:]
    cdir = ROOT / "conferences" / slug
    conf = yaml.safe_load((cdir / "conference.yaml").read_text())
    lang = conf["videos"].get("captionLang", "en-orig")
    talk = next((t for t in json.loads((cdir / "catalog.json").read_text())["talks"] if t["id"] == talk_id), None)
    if talk is None or not talk.get("video"):
        sys.exit(f"talk {talk_id} not in catalog or has no matched video")
    vid = talk["video"]["id"]
    dest = cdir / "transcripts" / f"{vid}.txt"
    if not dest.exists():
        with tempfile.TemporaryDirectory() as tmp:
            for attempt in (1, 2):
                vtt, log = download(vid, lang, Path(tmp))
                if vtt or "429" not in log or attempt == 2:
                    break
                print("HTTP 429 from YouTube; retrying in 60 s", file=sys.stderr)
                time.sleep(60)
            if vtt is None:
                if "429" in log or "ERROR" in log:
                    print(log[-1500:], file=sys.stderr)
                    sys.exit(4)
                print(f"no '{lang}' captions for {vid}", file=sys.stderr)
                sys.exit(3)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(clean_vtt(vtt.read_text()))
    text = dest.read_text()
    print(dest.relative_to(ROOT))
    print(f"{len(text.splitlines())} paragraphs, {len(text.split())} words", file=sys.stderr)


if __name__ == "__main__":
    main()
