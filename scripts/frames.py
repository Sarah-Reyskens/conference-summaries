#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Grab still frames from a talk's video at given timestamps (needs ffmpeg on PATH).

Usage (from the repo root):
  uv run scripts/frames.py <slug> <talk-id> <mm:ss|hh:mm:ss> [...]

Seeks the 720p stream directly (no video download), ~3 s per frame. Writes
conferences/<slug>/frames/<videoId>-<seconds>.jpg (gitignored cache) and prints
one repo-relative path per frame that succeeded; failures go to stderr.
Exit 0 if at least one frame succeeded, 4 otherwise.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def seconds(ts: str) -> int:
    total = 0
    for part in ts.split(":"):
        total = total * 60 + int(part)
    return total


def main() -> None:
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    slug, talk_id, *stamps = sys.argv[1:]
    cdir = ROOT / "conferences" / slug
    talk = next((t for t in json.loads((cdir / "catalog.json").read_text())["talks"] if t["id"] == talk_id), None)
    if talk is None or not talk.get("video"):
        sys.exit(f"talk {talk_id} not in catalog or has no matched video")
    vid = talk["video"]["id"]
    out = cdir / "frames"
    out.mkdir(exist_ok=True)
    pending = [(ts, out / f"{vid}-{seconds(ts)}.jpg") for ts in stamps]
    errors: dict[str, str] = {}
    # Stream URLs occasionally reject a request (403 under parallel load); one fresh URL fixes it.
    for _attempt in (1, 2):
        todo = [(ts, dest) for ts, dest in pending if not dest.exists()]
        if not todo:
            break
        stream = stream_url(vid)
        if stream is None:
            errors = {ts: "yt-dlp could not resolve a stream URL" for ts, _ in todo}
            continue
        for ts, dest in todo:
            r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(seconds(ts)), "-i", stream,
                                "-frames:v", "1", "-q:v", "3", str(dest)], capture_output=True, text=True)
            if dest.exists():
                errors.pop(ts, None)
            else:
                # ffmpeg echoes the signed stream URL; keep only its final line's message.
                errors[ts] = (r.stderr.strip().splitlines() or ["no frame (timestamp past the end?)"])[-1].split(": ")[-1][:200]
    ok = 0
    for ts, dest in pending:
        if dest.exists():
            print(dest.relative_to(ROOT))
            ok += 1
        else:
            print(f"{ts}: {errors.get(ts, 'failed')}", file=sys.stderr)
    sys.exit(0 if ok else 4)


def stream_url(vid: str) -> str | None:
    res = subprocess.run(["yt-dlp", "-g", "-f", "bv*[height<=720][ext=mp4]/bv*[height<=720]/b",
                          f"https://www.youtube.com/watch?v={vid}"], capture_output=True, text=True)
    lines = res.stdout.strip().splitlines()
    return lines[0] if res.returncode == 0 and lines else None


if __name__ == "__main__":
    main()
