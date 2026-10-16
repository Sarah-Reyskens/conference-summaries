---
title: Conquest, time travel and explosions using Git
talkId: "24218"
conference: devoxx-be-2026
speakers: [Alexander Chatzizacharias]
track: Mind the Geek
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=wbzpP0T9w6I
durationMin: 47
slides: null
verdict: 7
reach: broad
frames: 9
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Conquest, time travel and explosions using Git

Alexander Chatzizacharias · Conference · Mind the Geek

## TL;DR

Chatzizacharias built a real-time strategy game whose entire world state lives in a real Git repository, so staging, branching, merging and rebasing are literal gameplay. The talk plays the game live to build intuition for Git's object model (snapshots, the Merkle DAG, the `.git` layout, three-way merge), then closes by showing how plumbing commands can permanently destroy history. Beginners leave with a mental model of Git; veterans get a custom merge driver and a history-wipe recipe.

## Key takeaways

- Git stores snapshots, not diffs: every commit holds a complete tree, and only garbage collection later packs old versions as deltas to save space.
- A branch is a small file under `.git/refs` pointing at a commit hash; history is computed by walking each commit's ancestors through the DAG.
- Staged-but-uncommitted objects sit in the object store linked to no commit, so the next garbage collection treats them as garbage and deletes them; the game shows staged buildings at half capacity for exactly this reason.
- A rebase is a series of cherry-picks replayed onto the target branch, which is why a rebased branch merges back as a fast-forward with linear history.
- Custom merge drivers can replace line-based merging: the game's driver merges per grid cell so two buildings on the same map row do not false-conflict.
- "Nothing is ever lost in Git" holds only while objects stay referenced: `write-tree` plus deleting branches and tags plus expiring the reflog plus `gc` destroys history, and the result can be mirrored to a server to catch collaborators too.

## Notes

### [02:38](https://youtu.be/wbzpP0T9w6I?t=158) Why Git, and an agent's scary command

Nearly the whole room uses Git, and the speaker's premise is that nobody debates the choice of version control system anymore; Git is the default. The other motive: an AI coding agent once asked permission to run a command the speaker could not read at a glance, which made Git feel like the last line of defense against agents. The command, shown on screen:

```sh
# from slide at 04:47
git merge-base --octopus $(git branch --format='%(objectname)') 2>/dev/null || git rev-list --max-parents=0 --all
```

It tries an octopus merge-base across branches matching a format and, failing that, prints every root commit. Git's defining word is "distributed": every client holds the full history, so any healthy clone can restore the whole repository.

### [07:23](https://youtu.be/wbzpP0T9w6I?t=443) A ten-day history of Git

Git was created in 2005 by Linus Torvalds after the Linux kernel team lost its free BitKeeper license (a kernel developer reverse-engineered BitKeeper, violating its terms). Torvalds's requirements: a merge or patch in under 3 seconds, fully distributed like BitKeeper, and checksummed against corruption; stuck for ideas, he looked at CVS and did the opposite. The timeline runs from 3 April 2005 (start) to the first commit on 7 April, first merge on 18 April, first kernel release shipped via Git on 16 June, handover to Junio Hamano on 26 July, and Git 1.0 on 21 December. Hamano is still the core maintainer.

### [11:02](https://youtu.be/wbzpP0T9w6I?t=662) Using Git for everything, until it becomes a game

The speaker tried versioning notes (fine, over-engineered) and per-branch calendars (also over-engineered) before landing on game save files: committing an Elden Ring save lets you revert death, and the same trick carried an honour-mode run in Baldur's Gate 3. Losing an Age of Empires 2 match to someone named "git gud" suggested the next step: a real-time strategy game with Git as its core. The map is a text grid where each cell is a character, buildings are marked by a top-left anchor plus footprint, and metadata lives alongside; every map change is therefore a commit. The stack is a Unity (C#) client talking REST to a Quarkus sidecar server, which pushes events over websockets, drives Git through the CLI and JGit behind a file watcher, and ships custom merge drivers compiled with GraalVM Native Image.

### [18:58](https://youtu.be/wbzpP0T9w6I?t=1138) Staging, branching and merging, played live

Fighting the AI "silicon empire" as developers, the speaker proves the game is Git by driving it from a terminal: `git checkout -b mining`, placing a silicon cache (blue, working tree only), `git add` (gold, staged at half capacity), and `git commit` (full strength). Back on `main`, everything built on the branch is gone, as expected. Building defenses on `main` while the mining branch grows leaves the two diverged, and merging produces a real merge conflict, resolved in-game by keeping the GPU cluster; the result is a genuine merge commit joining both lines.

### [25:18](https://youtu.be/wbzpP0T9w6I?t=1518) Three-way merges and a custom merge driver

Git merges by three-way merge: it takes our changes and their changes and compares each against their first common ancestor, line by line. Line granularity breaks the game, since two buildings on the same map row would always conflict, so the speaker wrote a custom merge driver that applies the same three-way logic per character and reports conflict via its exit code: ours-only wins, theirs-only wins, identical changes merge silently, and real conflicts get conflict markers.

### [27:26](https://youtu.be/wbzpP0T9w6I?t=1646) The Merkle DAG and the `.git` folder tour

Every Git object is hashed into a Merkle directed acyclic graph: blobs for file contents, trees for folders, all under a root tree under a commit. Git is content-addressable, so identical content at different paths is stored once, and `git status` stays fast on huge repositories because it compares top-level hashes first and only drills into folders whose hash changed. Tagging the in-game wonder (the Tabularium) with `git tag` unlocks it as the `.git` folder: `HEAD` records the current branch tip, the index holds staged blobs, `logs` records every HEAD movement (the backing store of `git reflog`), `refs` maps branch and tag names to hashes, and `objects` stores the commits, trees, blobs and tags. Anything not hanging under a commit is orphaned and discarded by the next collection; `git gc` packs survivors by storing the newest file plus reverse deltas.

### [37:57](https://youtu.be/wbzpP0T9w6I?t=2277) Rebase as cherry-picks and the fast-forward

After an attack force is built on branch `attack_1`, the audience votes to rebase rather than merge. A rebase is just cherry-picks replayed one by one onto the target, which the game shows commit by commit with units exploding and reappearing on `main`. Since the rebased tip now contains everything, merging back is a fast-forward: Git slides the `main` reference forward to the branch tip with no new commit, producing the linear history on the Multiverse graph. An audience question about the still-separate mining branch is answered in passing: it still exists because it was never deleted.

### [41:06](https://youtu.be/wbzpP0T9w6I?t=2466) Winning, then destroying history

The first assault fails, so cheat codes spawn nine CTOs and the enemy headquarters falls. But in Git the loser could just revert, so the speaker demonstrates the opposite: how to truly destroy a repository. The recipe, run as visible commands while the Multiverse graph collapses: `git add -A`, `git write-tree` and `git commit-tree` to write the current tree as an unreferenced commit, `git checkout` onto it, `git branch -D` and `git tag -d` to unreference everything else, then expire the reflog and run `gc` so every unreferenced object reads as garbage. Mirrored to a server plus one tricked `checkout` by colleagues, the whole team loses history.

### [44:43](https://youtu.be/wbzpP0T9w6I?t=2683) Closing: coding is your superpower

The send-off is "git gud": coding is your superpower regardless of who writes it, so build playful things instead of another LLM wrapper. Voice actors are credited (all human, including Stephan Janssen as Astra Codexior VI and Sara Larsson as the CTO), and the closing slide links the server repository and a feedback QR.

## Tools, libraries and specs

- Unity (C#) client for the game and its slides
- Quarkus sidecar server (REST in, websocket events out, file watcher on the repo)
- JGit for driving Git from the server
- GraalVM Native Image for the compiled custom merge drivers
- git CLI: checkout, add, commit, merge, tag, cherry-pick, rebase, write-tree, commit-tree, branch -D, gc, reflog
- github.com/glycin/git-and-conquer-server, the published game server

## Who should watch

Beginners who stage, branch and merge by ritual gain the most: the game turns the object model into something visible. Veterans who never opened `.git` or wrote a merge driver get a compact internals tour with two reusable tricks. Git contributors and anyone fluent in plumbing can skip everything except the game implementation itself.

## Verdict

**7/10**: A beginner Git talk whose object-model explanations and live Git operations earn Depth and Demonstrated, held at 7 by Novelty and Reusable 1: the Git material is known, and the one linked repository is the game's own server without the client.

**Reach broad**: Nearly the whole conference audience versions code with Git daily, so the object-model intuition and merge and rebase practice apply to most viewers' own work.

**Novelty 1/2**

- **+** [15:16](https://youtu.be/wbzpP0T9w6I?t=916) The speaker's own RTS game stores its map as a text grid in a real Git repository, so staging, branching and merging become game mechanics.
- **+** [26:22](https://youtu.be/wbzpP0T9w6I?t=1582) A custom merge driver written by the speaker checks conflicts per character, because line-based merging false-conflicts on the game grid.
- **−** The Git internals it teaches (objects, DAG, three-way merge, rebase) are covered by the Pro Git book and the Git docs, and game-based Git teaching exists in [Oh My Git!](https://ohmygit.org) and [Learn Git Branching](https://learngitbranching.js.org).

**Demonstrated 2/2**

- **+** [19:32](https://youtu.be/wbzpP0T9w6I?t=1172) A live terminal session checks out the mining branch, stages and commits a building, and the game world updates from the repository on screen.
- **+** [38:58](https://youtu.be/wbzpP0T9w6I?t=2338) The rebase of attack_1 onto main replays commit by commit live, then merges back as a fast-forward with visible linear history.
- **+** [43:42](https://youtu.be/wbzpP0T9w6I?t=2622) The local history-destruction recipe runs as visible plumbing commands while the Multiverse graph collapses on screen.

**Measured 1/2**

- **·** [08:26](https://youtu.be/wbzpP0T9w6I?t=506) The talk makes no quantitative claim of its own; its numbers are historical requirements and game state, so measurement does not apply.

**Depth 2/2**

- **+** [27:57](https://youtu.be/wbzpP0T9w6I?t=1677) The object-model explanation connects hashed blobs, trees and commits to content-addressing and reuse of identical file contents.
- **+** [33:12](https://youtu.be/wbzpP0T9w6I?t=1992) Branches are explained as named references to commit hashes, with history recovered by following commit ancestry through the DAG.
- **+** [38:27](https://youtu.be/wbzpP0T9w6I?t=2307) Rebase is explained as replayed cherry-picks and fast-forward as reference movement, giving the reason behind linear history.

**Reusable 1/2**

- **+** [46:24](https://youtu.be/wbzpP0T9w6I?t=2784) The closing slide links [git-and-conquer-server](https://github.com/glycin/git-and-conquer-server), the game's server with its world repository handling, merge drivers and HTTP examples.
- **−** [16:19](https://youtu.be/wbzpP0T9w6I?t=979) The linked repository is the presented project's own server and lacks the Unity client that renders the demo, so the on-screen game cannot be reproduced from it.
