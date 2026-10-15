---
title: "Snake in 10 Lines: Learning More by Coding Less"
talkId: "19748"
conference: devoxx-be-2026
speakers: [Guus de Wit]
track: Mind the Geek
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=LD2tKMpToYg
durationMin: 49
slides: null
verdict: 8
frames: 8
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Snake in 10 Lines: Learning More by Coding Less
Guus de Wit · Conference · Mind the Geek

## TL;DR
Guus de Wit live-codes Snake from a 114-line Kotlin prototype down to 10 lines of JDK-only code, at most 130 characters each, keeping the game playable at every stage. Each round of compression forces a better design: terminal output gives way to a 3-line Swing window, per-segment movement becomes add-head-remove-tail, and the 2D board collapses into a 1D array rendered with line wrap. The talk leaves three lessons: learn by doing, constraints breed creativity, and brevity builds understanding.

## Key takeaways
- Spec a feature in six words before building it: "snake moves, guided, eats, grows, dies" maps directly onto game state, user input, game logic, and termination.
- Plain terminal I/O cannot do real-time key input without libraries, so the JDK-only build uses a Swing window with a KeyAdapter, compressed to three lines.
- Move the snake by prepending a new head and removing the tail instead of updating every segment; thinking about corners first leads to that design.
- Store the board as a 1D array and display it as 2D with JTextArea line wrap, turning positions and directions into single-number arithmetic.
- Compress Kotlin by inlining single-use variables and methods, using static imports, `apply` blocks, and `generateSequence` instead of while loops, plus dropping unneeded Swing configuration.
- With no lines left for a score display, report the score through the process exit code (`snake.size - 3`).
- Stage direction changes in a pending-direction variable and reject the reverse of the current direction, so the snake cannot instantly crash into itself.

## Notes
### [00:32](https://youtu.be/LD2tKMpToYg?t=32) Six-word stories and the rules
Six-word stories ("I wanted it, I got it, damn it") motivate the exercise: say more with less. The challenge rules: a playable, recognizable Snake on a computer, 10 functional lines inside `main` (imports not counted), max 130 characters per line, JDK only with no external libraries, demonstrated in Kotlin. Desirable properties, in order: readable, few bugs, extra features such as a score if room remains.

### [04:05](https://youtu.be/LD2tKMpToYg?t=245) Snake in six words
The whole spec becomes "snake moves, guided, eats, grows, dies". Each word maps onto an implementation need: state (where the snake is), evolution (movement per frame), user input (guidance), game logic (eating and growing), and termination. Guessing games from six-word descriptions (Pong, Tetris, the Chrome dino game) show the technique generalizes to scoping features.

### [06:09](https://youtu.be/LD2tKMpToYg?t=369) First version: terminal Snake moving right
Starting from Conway's Game of Life experience, the first version prints frames as strings to the terminal: a 2D grid class, a Snake class holding a list of X/Y cells, a game loop that moves, renders, and sleeps. It is recognizable but moves in one direction only and has no input.

### [08:11](https://youtu.be/LD2tKMpToYg?t=491) Real-time input via a 3-line Swing window
Arrow keys in a terminal only move the cursor, and line-based input would make Snake turn-based, so a 40-plus-line Swing prototype with a JFrame, JTextArea, and KeyAdapter replaces terminal output. Reading the docs removes everything optional (window title, defaults), IntelliJ's join-lines shortcut (Ctrl+Shift+J) plus an anonymous KeyAdapter object compress it to three lines, and the board renders as text-area content. Takeaway one: you learn by doing; the speaker had never built such games before.

### [14:23](https://youtu.be/LD2tKMpToYg?t=863) Movement, eating, growing, dying
Moving each body part individually costs too much code, and tracking only corners saves memory but needs extra rendering code. The final design: prepend a new head cell in the current direction, drop the tail. Eating re-attaches the removed tail and relocates food to a random empty cell; death ends the `while` loop when the snake overlaps itself, detected by comparing unique cells against the full body. The playable result is 114 lines.

### [22:37](https://youtu.be/LD2tKMpToYg?t=1357) The board goes 1D
X/Y pairs cost too many characters, so positions become single numbers in a 1D array while JTextArea line wrap keeps the display 2D. Left/right is plus or minus 1, up/down plus or minus the screen width. The snake, directions, and food all simplify to about 100 lines. Known quirk: reaching a line edge wraps to the next line. Takeaway two: constraints lead to creativity, and the first design is rarely the one that fits.

### [26:44](https://youtu.be/LD2tKMpToYg?t=1604) Compressing 100 lines into 10
Ten numbered comments mark the target lines. The key handler, movement, eating (via `generateSequence` plus `first` instead of a retry loop), rendering, and state each collapse to one line through inlining, short names, whitespace removal, a static import of `nextInt`, and building the JFrame with `apply` so no window variable is needed. Lines 10-19 of `main` hold the whole game: state, window, input, direction check, move, eat, render, sleep, and exit.

### [36:03](https://youtu.be/LD2tKMpToYg?t=2163) Bugs, and features that fit in the gaps
Three issues surface: static food start at position 15, no reversal guard, and the wrap-around edge. Fixes within budget: shorten the snake by one cell and spawn food under its nose so the first frame randomizes it unseen; stage input in a pending-direction variable checked against the reverse; report the score as the `exitProcess` code. Speeding the game up reveals a "kill screen": with no empty cells left, food placement loops forever and the game freezes.

### [42:44](https://youtu.be/LD2tKMpToYg?t=2564) One skeleton, more games
Half the lines are Snake-specific and half are generic game scaffolding (window, loop, sleep, exit), so the same 10-line shape yields more games live on stage: a reversed variant with moving food, a gravity variant that plays like Tetris, and others. The published versions are reworked for readability under a character budget rather than a line budget. Takeaway three: conciseness leads to understanding, for the author refactoring and for reviewers reading less.

### [47:27](https://youtu.be/LD2tKMpToYg?t=2847) Q and A: the Java version
Asked whether it works in Java, the speaker shows "Jake": the same game in 10 lines of Java, where declaring several same-type variables with one `int` is terser than Kotlin.

## Tools, libraries and specs
- Kotlin with JDK-only APIs (no external libraries)
- Swing: JFrame, JTextArea (with line wrap), KeyAdapter for real-time key input
- IntelliJ IDEA join-lines shortcut (Ctrl+Shift+J)
- Kotlin `generateSequence` (Java `Stream.generate` mentioned as equivalent)

## Who should watch
Kotlin and Java developers who enjoy constraint coding, and beginners who want a guided live-coding session where every design decision is explained. Skip it if you want production game architecture, engine internals, or advanced JVM material; the point is the learning exercise, not the game.

## Verdict
**8/10**: A live-built 10-line Snake whose design choices are the speaker's own and shown working, limited by self-counted line totals and no linked code.

**Novelty 2/2**

- **+** [23:39](https://youtu.be/LD2tKMpToYg?t=1419) The 1D board model with single-number coordinates rendered 2D via line wrap is the speaker's own design answer to the line budget.
- **+** [37:04](https://youtu.be/LD2tKMpToYg?t=2224) Reporting the score through the process exit code is an original trick invented for the constraint.
- **·** [01:33](https://youtu.be/LD2tKMpToYg?t=93) Short-code Snake implementations are a known code-golf genre; the value here is the documented journey and its transferable techniques.

**Demonstrated 2/2**

- **+** [37:04](https://youtu.be/LD2tKMpToYg?t=2224) The finished 10-line program is first played live, with the exit-code score showing one, two, then three.
- **+** [40:10](https://youtu.be/LD2tKMpToYg?t=2410) The reversal-guard fix is verified live: pressing the opposite arrow no longer crashes the snake.
- **+** [44:47](https://youtu.be/LD2tKMpToYg?t=2687) Derivative games built on the same 10-line skeleton run live, including the gravity variant.

**Measured 1/2**

- **+** [22:05](https://youtu.be/LD2tKMpToYg?t=1325) Line counts trace the compression on screen: 114 lines, about 100 after the 1D switch, exactly 10 at the end.
- **+** [28:16](https://youtu.be/LD2tKMpToYg?t=1696) The input logic lands at exactly the 130-character limit, shown against the editor ruler.
- **·** [02:03](https://youtu.be/LD2tKMpToYg?t=123) The counting method is self-defined ("I only count functional lines of code"), so the totals have no external baseline.

**Depth 2/2**

- **+** [14:54](https://youtu.be/LD2tKMpToYg?t=894) The movement design walks from per-segment updates through corners-only storage to add-head-remove-tail, with the reason each earlier step falls short.
- **+** [23:39](https://youtu.be/LD2tKMpToYg?t=1419) The 2D-to-1D switch is justified as single-number arithmetic for positions and directions, with the wrap-around edge disclosed as the cost.
- **+** [42:13](https://youtu.be/LD2tKMpToYg?t=2533) The "conciseness leads to understanding" claim is grounded in the refactoring just performed rather than asserted.

**Reusable 1/2**

- **+** [35:01](https://youtu.be/LD2tKMpToYg?t=2101) The complete 10-line game is visible on screen and short enough to retype from the video.
- **+** [40:40](https://youtu.be/LD2tKMpToYg?t=2440) Two fixes for the wrap-around bug are described (go back to the previous line, or end the game at the boundary) and left for the audience to build.
- **·** [45:17](https://youtu.be/LD2tKMpToYg?t=2717) The speaker mentions a page with reworked implementations but gives no address on screen or in speech, so no published artifact is linked.
