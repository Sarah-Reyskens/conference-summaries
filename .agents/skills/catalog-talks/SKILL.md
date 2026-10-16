---
name: catalog-talks
description: Build or refresh a conference's talk catalog and match each talk to its YouTube video.
disable-model-invocation: true
---

Input: a conference slug (a directory under `conferences/`). Run every command from the repo root.

## 1. Conference file

`conferences/<slug>/conference.yaml` drives everything: talk source, playlists, thresholds, excluded session types, overrides, and the `audience` description that verdicts' Reach and the ranking are judged against. Missing → stop and say which file is needed; another conference's file shows the fields. A new conference file without `audience`: ask the user who attends and write it before anything is summarized.

## 2. Build

`uv run scripts/catalog.py build <slug>` fetches talks and playlist videos, matches them, and writes `conferences/<slug>/catalog.json`. Re-running is safe: it re-matches only `excluded`, `no-video` and `needs-review` talks and keeps every other talk's video and progress. It prints status counts, then one line per `needs-review` and `no-video` talk.

## 3. Review

For each `needs-review` line, judge whether the candidate video is the same talk (retitled, same speakers) and give a one-line reason. Present them to the user as a table and ask which to confirm. For each confirmed talk, add `<talkId>: <videoId>` under `overrides:` in the conference file; for talks the user says have no video, add `<talkId>: null`. When overrides changed, run the build again.

## 4. Report

Reply with the final status counts, matched versus unmatched (`no-video` + `needs-review`), and the remaining unmatched talks by title and session type.
