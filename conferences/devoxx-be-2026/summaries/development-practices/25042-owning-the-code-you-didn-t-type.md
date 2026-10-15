---
title: Owning the Code You Didn't Type
talkId: "25042"
conference: devoxx-be-2026
speakers: [Renato Guerra Cavalcanti]
track: Development Practices
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=SQUrHzMie3o
durationMin: 50
slides: https://renato.cavalcanti.io/presentations/owning-the-code/
verdict: 7
frames: 11
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Owning the Code You Didn't Type

Renato Guerra Cavalcanti · Conference · Development Practices

Slides: https://renato.cavalcanti.io/presentations/owning-the-code/

## TL;DR

Coding agents now produce code faster than anyone can read it, so the bottleneck moved from writing to understanding while accountability stayed exactly where it was. Cavalcanti argues developers must deliberately stay in the loop or lose both skill and ownership, then presents the daily practices he uses to do that: a readability bar for agent output, file-based collaboration instead of chat, guided walk-throughs, phased delivery with review gates, and engineering depth.

## Key takeaways

- Delegate mechanical tasks freely, but keep the tasks where thinking happens: doubting, experimenting and changing direction while coding is what wires the system into your brain.
- Without guidance a model drifts to the statistical center, so on average you get average code; your knowledge sets the anchors that pull it toward the design you want.
- Treat readability as an acceptance criterion for agent output and send back what fails it, because today's merged code becomes the context tomorrow's agent imitates.
- Replace scrolling chat threads with files: specs, plans, summaries and walk-throughs in a git-ignored directory, plus questions left as tagged comments where the code lives.
- Split agent work into small phases with a review gate after each: review, touch the code, commit, and only then continue.
- Keep one commit per phase with a written description so a later session, yours or another agent's, can review each step with its context intact.

## Notes

### [00:35](https://youtu.be/SQUrHzMie3o?t=35) Writing code as cognition and identity

Cavalcanti opens with a definition: writing code is a cognitive process of translating the problem, constraints and requirements into a programming language, and that translation is enjoyable engineering practice. It also forges identity: the languages and styles developers choose reveal who they are, and the activity itself shapes how they think. He illustrates this with his own story of understanding school mathematics better as an adult because programming had rewired how he reasons.

### [06:48](https://youtu.be/SQUrHzMie3o?t=408) Depth versus fluency, and a misdiagnosed for-comprehension

Fluency (syntax, idioms, standard library under your fingers) is now borrowable from the model; depth (the runtime, memory, concurrency, design judgment) stays the developer's responsibility. The danger of missing depth gets a worked example from that same week: Claude claimed his Scala for-comprehension silently recovered a failed `Future`, repeating the claim after a context reset. The desugared `flatMap` chain and its Java `CompletionStage` equivalent show the second stage never runs when the first fails, so there was no bug. He caught it by paying attention; a blind "fix it" would have churned correct code for no reason.

### [10:57](https://youtu.be/SQUrHzMie3o?t=657) Learning while coding, and "looks green to me"

A clear idea of what to build is a luxury; most coding time goes to doubting, probing and changing direction, and that friction builds the mental model. Opening an unfamiliar codebase feels hard precisely because that model is missing. Purely mechanical work costs nothing to delegate, but delegating the thinking tasks turns your application into someone else's. The review failure mode: "LGTM" degrades from "looks good to me" into "looks green to me", where merging means recognizing a color on GitHub instead of judging the code.

### [16:12](https://youtu.be/SQUrHzMie3o?t=972) Average by default, and the automation paradox

Models train on everything from well-crafted open source to internet slop, so an unguided prompt drifts to the center of the distribution. He pairs this with a quote from Charafeddine Mouzouni's How to Think With AI ("your knowledge is what pulls the model away from the center") and with Lisanne Bainbridge's 1983 "Ironies of Automation": automating most of the work leaves operators deskilled yet responsible for whatever cannot be automated, plus exhausting monitoring. The developer version is losing exactly the activity that kept judgment sharp.

### [25:04](https://youtu.be/SQUrHzMie3o?t=1504) Made for humans: writing rules and a reminder hook

Agent output must be understandable, in chat replies, comments, docs and code design alike. Two exhibits: an Akka constructor that accepted an `Optional`, null-checked it, and spread that pattern across constructors until every class had a meaningless no-arg path; and garbled agent prose ("there are two configs in play...") shown next to plain rewrites. His counter is a "How to write" ruleset (clarity over style, one idea per sentence, active voice, one term per concept) plus a hook that re-injects a reminder on every prompt, because rules loaded once at session start lose attention as context grows:

```json
// from published slides p.28
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Write replies per the \"How to write\" rules in ~/.claude/CLAUDE.md."
  }
}
```

### [33:32](https://youtu.be/SQUrHzMie3o?t=2012) Files over chat: .nogit, /check-inbox, /walk-through

Chat scrolls away and cannot be annotated, so sessions produce files in `.nogit/`, excluded via a global gitignore: specs, plans, summaries and walk-throughs. While reading generated code he leaves messages as tagged source comments (`TODO-AI` for changes, `QUESTION-AI` for explanations), answered later through a `/check-inbox` command with one approval per message. For reviews and unfamiliar code, `/walk-through` generates a logical reading order instead of an alphabetical diff, runs in parallel, and can be replayed step by step with `/walk-replay`:

```text
// from published slides p.32
/walk-through 238n6q6us                 # from this commit to HEAD
/walk-through 4582                      # a pull request
/walk-through explain the http client retry mechanism
/walk-through -i ...                    # interactive, step by step
/walk-replay pr-4582                    # one step at a time
```

### [38:13](https://youtu.be/SQUrHzMie3o?t=2293) Phased delivery and /autonomously

Implementation runs one phase at a time, then stops: review, touch the code, commit. Some phases he takes himself as pair programming, especially API shapes he wants to feel out by hand. When a task is clearly on rails he calls `/autonomously`, which finishes all phases but still commits per phase with a written description. A screenshot of his Rust tooling project shows three such commits; the descriptions let a fresh agent session review each phase with context. For him this is the moment he feels like a software engineer again: not typing, but guiding throughout.

### [42:28](https://youtu.be/SQUrHzMie3o?t=2548) Slow down to build knowledge

AI already pays off enormously: postponed migrations, flaky build diagnosis (a blessing for Akka's concurrency-heavy tests), experiments. But production of unverified code is being automated faster than verification, so he argues for deliberately slowing down to stay in the process. The closing message is "don't outsource your brain": accountability for merged code is not being removed, and the on-call engineer cannot answer a midnight page with "the AI wrote it". His setup lives at `octonato/octo-stack` on GitHub (a personal playground, offered for inspiration rather than adoption), alongside recommendations for the `/pr-review-toolkit` and `/superpowers` plugin sets.

## Tools, libraries and specs

- Claude (Anthropic), with Opus 5.5 named as the model behind the week's misdiagnosis story
- `/pr-review-toolkit`: Claude plugin set spawning specialist review sub-agents (security, test coverage, style)
- `/superpowers`: Claude plugin set for brainstorming, spec-driven development and code review
- `octonato/octo-stack`: the speaker's public personal setup with his commands and rules
- Charafeddine Mouzouni, How to Think With AI (quoted on knowledge pulling the model off-center)
- Lisanne Bainbridge, "Ironies of Automation" (1983), via its Wikipedia summary

## Who should watch

Developers who merge agent-written code daily and feel their grip on the codebase loosening will get the most, since every practice targets that exact situation. Beginners get an accessible framing of what the job is becoming. Skip it if you want measured comparisons of agents or benchmarks: there are no numbers here, and the tooling details assume a Claude-based workflow.

## Verdict

**7/10**: a personal agent-workflow system backed by two incidents from his own work and a published plugin repository, held back by practices that are described but never run on screen.

**Novelty 1/2**

- **+** [08:21](https://youtu.be/SQUrHzMie3o?t=501) The Scala for-comprehension misdiagnosis, repeated by Claude after a context reset in the same week, is the speaker's own field evidence for why depth matters.
- **+** [26:36](https://youtu.be/SQUrHzMie3o?t=1596) The constructor that accepted an `Optional`, null-checked it and spread that pattern across every constructor is a production incident behind the "today's code is tomorrow's context" rule.
- **·** [19:48](https://youtu.be/SQUrHzMie3o?t=1188) The automation-paradox passage is read from Wikipedia's article on the Bainbridge paradox, and the practices overlap with widely shared agent-workflow advice, so the added value is the integration with his own examples.

**Demonstrated 1/2**

- **+** [41:22](https://youtu.be/SQUrHzMie3o?t=2482) A screenshot of his Rust project after an `/autonomously` run shows three phase commits, each with a written description for later review.
- **−** [36:39](https://youtu.be/SQUrHzMie3o?t=2199) The `/walk-through` and `/check-inbox` commands are described but never run on screen, so their output is taken on trust.

**Measured 1/2**

- **·** The talk makes no quantitative claims about speed, cost, adoption or effect, so there is nothing a measurement would need to back.

**Depth 2/2**

- **+** [06:48](https://youtu.be/SQUrHzMie3o?t=408) The fluency-versus-depth model gives a beginner a mental frame: syntax is borrowable from the model, while runtime and design judgment stay with the developer.
- **+** [16:43](https://youtu.be/SQUrHzMie3o?t=1003) The drift-to-the-center explanation ties the model's probabilistic training distribution to why unguided output regresses to average code.
- **+** [31:57](https://youtu.be/SQUrHzMie3o?t=1917) The always-on reminder hook is chosen because rules loaded at session start lose attention as context grows, and weighed against a stateful hook that fires about a third of the time to save tokens.

**Reusable 2/2**

- **+** [48:18](https://youtu.be/SQUrHzMie3o?t=2898) The `octonato/octo-stack` repository publishes the walk-through, walk-replay, check-inbox and autonomously commands and the reviewer agents the talk's practices run on.
- **·** [48:48](https://youtu.be/SQUrHzMie3o?t=2928) The speaker calls the repository a playground he changes at will and tells listeners to build their own, and the setup targets Claude, so adapting it to other assistants is left to the reader.
