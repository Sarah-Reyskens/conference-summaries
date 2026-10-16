---
title: "One tool to rule them all: bash, a tiny LLM, and the birth of a coding agent"
talkId: "22911"
conference: devoxx-be-2026
speakers: [Philippe Charrière]
track: Agentic Engineering & Tooling
sessionType: Tools-in-Action
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=wWfj4AJahlQ
durationMin: 30
slides: null
verdict: 7
reach: segment
frames: 7
summarizedAt: 2026-10-14
reviewedAt: 2026-10-16
---

# One tool to rule them all: bash, a tiny LLM, and the birth of a coding agent

Philippe Charrière · Tools-in-Action · Agentic Engineering & Tooling

## TL;DR

A coding agent is a loop around a model with tools, and one shell tool is enough: small local models already know Unix commands, so a single `bash` tool replaces a catalog of per-command tools and saves context window. Charrière builds this live in Go, from function calling through a `bash`-only toolbox to Bob, a conversational agent that writes, builds and refactors code inside a Docker sandbox.

## Key takeaways

- Expose one `bash` tool instead of one tool per shell command: local models already know `curl`, `grep` and friends, and unknown CLIs can be learned via `--help` or `man` at runtime.
- Every tool added to the catalog costs context window and model focus, a real problem for small local models.
- Each `bash` call starts a fresh shell, so the tool description must tell the model to chain with `&&`; also warn it that long output is truncated and that it must read files before writing them.
- Run a shell-wielding agent inside a sandbox (here Docker SBX, a microVM with a Docker engine and secret redaction), because the agent can execute anything on the host.
- Small models hallucinate and fall into silent endless loops, so a real agent needs guardrails: loop detection, error recovery, and eventually context compression and RAG.

## Notes

### [01:09](https://youtu.be/wWfj4AJahlQ?t=69) Setup: a tiny local model and Docker Model Runner

Charrière, a Docker solution architect, runs everything on JetBrains Mellum 2 (12B parameters, about 2.5B active per token) through Docker Model Runner, an open-source wrapper around llama.cpp or vLLM exposing an OpenAI-compatible API as a Docker Desktop plugin. Docker Desktop shows each request and response, which helps debug generative apps. All demos are Go with the Genkit SDK; a Kotlin port is planned for the repo.

### [04:21](https://youtu.be/wWfj4AJahlQ?t=261) How function calling works

Models cannot execute anything; they emit a tool name plus parameters as JSON, and the application runs the tool and feeds results back into the message history. The model matches user intent against a tool catalog with descriptions (a `getWeather` example) and extracts parameters. A diagram walks through the loop: messages plus tool list into `genkit.Generate`, tool call detected, tool executed, results appended, final answer composed.

### [06:57](https://youtu.be/wWfj4AJahlQ?t=417) Demo 1: a computer store with four tools

One small program drives every demo: model id, sampling parameters, a system prompt, a question list, an OpenAI-compatible client, a toolbox, one `genkit.Generate` call. The first toolbox holds `Add`, `Multiply`, `ListProducts` and `FindPrice` as plain commented Go functions. Live run: 21+21, keyboard price lookup, a multi-item order split into several tool calls with a computed total, and a missing-catalog-item report.

### [09:41](https://youtu.be/wWfj4AJahlQ?t=581) Demo 2: real shell commands as tools

Identical code, new toolbox: each tool shells out to a real command (`curl`, `grep`, `go mod init`). The agent fetches example.com, creates `playground/hello` with a `go.mod`, and confirms "module" exists in it. Cost observed: each new command means more code and more context-window description.

### [11:47](https://youtu.be/wWfj4AJahlQ?t=707) The one-tool idea: just bash

Every tool deleted except one `bash` tool with a coaching description: run a Unix command and return output plus exit status, chain with `&&` because each call starts a new shell, nothing is interactive, long output is truncated, read before writing. Same questions plus `go version` all succeed: fetch, mkdir, `go mod init`, grep check, version check.

### [14:57](https://youtu.be/wWfj4AJahlQ?t=897) Bob: the agent loop

The last example tidied into a `Run` loop in `internal/agent/agent.go`: read input, append to history, call generate, update history, print tool calls. Settings move to YAML (model, endpoint, sampling parameters, extra system-prompt instructions). Bob runs inside Docker SBX, a microVM sandbox with its own Docker engine and a proxy hiding API-key values from the agent.

### [19:18](https://youtu.be/wWfj4AJahlQ?t=1158) Live coding: write, build, run, refactor

Bob gets an 8-step task (Dog, Cat and Human structs with a Greet method; save, build, run) and completes it end to end, printing the greeting output. Follow-ups show memory-only answers, then `gopls help`, `workspace_symbol` and `references` to locate definitions with line numbers, and `gopls rename -w` turning `Greet` into `Welcome`, verified by re-running. For larger codebases he points at ripgrep and ast-grep.

### [23:38](https://youtu.be/wWfj4AJahlQ?t=1418) Going further, and mini

Graduation checklist: more CLIs, edit/diff tools, a skills tool, hallucination and endless-loop detection, RAG, context compression, MCP. A hardened side project called mini (loop-detection guardrails, nicer UI, many local models) is already his daily driver with bigger models. All source is on Codeberg at `codeberg.org/talks/2026-10-Devoxx-Belgium-One-tool-to-rule-them-all`, shown as a QR code on the closing slide.

### [28:20](https://youtu.be/wWfj4AJahlQ?t=1700) Q&A

How smart must a model be for function calling: small Qwen-class models handle it well now, so start with a ~4B-parameter model with tool support, and mix a small function-calling model with a larger one for completions.

## Tools, libraries and specs

- JetBrains Mellum 2 (12B params, ~2.5B active per token), served locally
- Docker Model Runner (OpenAI-compatible, llama.cpp / vLLM backends, Docker Desktop plugin)
- Genkit Go SDK (`genkit.Generate`, `genkit.DefineTool`)
- Docker SBX / cloud sandbox (microVM sandbox with secret redaction)
- gopls (help, workspace_symbol, references, rename -w), ripgrep, ast-grep
- mini (speaker's follow-up local-model agent); MCP and RAG named as next steps

## Who should watch

Beginners who want to see what a coding agent loop actually is instead of treating it as magic, and anyone curious how far a small local model goes. People who already build agents can skip it, apart from the `bash`-as-universal-tool framing.

## Verdict

**7/10**: a bash-only coding agent completes its task on screen, with a beginner-level explanation of the loop and a published demo repository, but the context-saving and tool-selection claims are unmeasured.

**Reach segment**: developers building LLM features or agent tooling can apply the implementation; the main content is agent construction rather than everyday use of coding assistants.

**Novelty 1/2**

- **+** [09:41](https://youtu.be/wWfj4AJahlQ?t=581) The speaker's own progression from a store assistant to shell commands and a conversational coding agent gives familiar tool-calling material a worked-example sequence beyond a single getting-started.

**Demonstrated 2/2**

- **+** [13:53](https://youtu.be/wWfj4AJahlQ?t=833) The single bash tool fetches a page, creates a Go module, checks its contents and reports the installed Go version.
- **+** [19:50](https://youtu.be/wWfj4AJahlQ?t=1190) Bob completes the coding task by creating, building and running the requested Go program, with output visible.
- **+** [22:32](https://youtu.be/wWfj4AJahlQ?t=1352) The follow-up uses `gopls rename -w` to rename `Greet` to `Welcome`, checks the change and runs the program again.

**Measured 0/2**

- **−** [12:20](https://youtu.be/wWfj4AJahlQ?t=740) The claim that one tool saves context space has no token counts or measured comparison with the multi-tool version.
- **−** [28:51](https://youtu.be/wWfj4AJahlQ?t=1731) Mellum's claimed near-perfect tool selection is not backed by a success rate or a stated test.

**Depth 2/2**

- **+** [04:52](https://youtu.be/wWfj4AJahlQ?t=292) The explanation separates model-generated tool names and arguments from application-side execution, establishing why an agent needs an execution loop.
- **+** [13:21](https://youtu.be/wWfj4AJahlQ?t=801) The bash implementation explains prompt constraints through shell behavior: fresh processes require `&&` chaining, interactive input cannot work, and a model must inspect files before editing.
- **+** [16:00](https://youtu.be/wWfj4AJahlQ?t=960) The code walkthrough connects user input, message history, generation and returned history, making the conversational loop explicit within the beginner slot.

**Reusable 2/2**

- **+** [27:19](https://youtu.be/wWfj4AJahlQ?t=1639) The closing points to the Codeberg repository for all presentation source, including the staged examples and Bob configuration used in the talk.
