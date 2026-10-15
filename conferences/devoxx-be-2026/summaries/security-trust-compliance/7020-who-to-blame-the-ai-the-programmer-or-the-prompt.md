---
title: "Who to blame? The AI, The Programmer, or The Prompt?"
talkId: "7020"
conference: devoxx-be-2026
speakers: [Makan Sepehrifar]
track: Security, Trust & Compliance
sessionType: Lunch Talk
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=VmPMUGImB-M
durationMin: 40
slides: null
verdict: 5
frames: 8
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Who to blame? The AI, The Programmer, or The Prompt?
Makan Sepehrifar · Lunch Talk · Security, Trust & Compliance

## TL;DR
The audience acts as jury in a courtroom game over four real CVEs in AI coding tools, voting after each case whether the model provider, the tool developer, or the end user is at fault, with the speaker arguing both sides before a final vote. Every case ends at the tool developer, yet the closing argument is that agentic AI security needs shared responsibility: providers must threat-model, and developers must treat agents as credentialed instruction-followers, not chat boxes.

## Key takeaways
- Treat every file an agent reads as untrusted input: prompt-injection payloads hide in PR comments, issues, dependencies, and agent config files alike.
- Never expose a tool built for localhost to the network without adding authentication: the Ollama container bound to 0.0.0.0 turned a local toy into a remote shell.
- Concatenating agent-supplied parameters into shell strings is CWE-78 no matter which layer does it; validate intent and execute at the OS level instead.
- Audit what your agent can change about itself: several 2025–2026 CVEs let prompts rewrite agent settings files and flip auto-approve on.
- Review agent configuration (Cursor rules, Copilot instructions, CLAUDE.md equivalents) the way you review dependencies, since the agent follows attacker's instructions in those files as faithfully as yours.
- Consume AI output the way you consume anything else: check the source, verify the quality, and share the vulnerabilities you find with the community.

## Notes

### [00:34](https://youtu.be/VmPMUGImB-M?t=34) How the courtroom vote works
Sepehrifar, a staff engineer at Productboard, runs the session as judge, defendant, and prosecutor at once. For each vulnerability case he presents the attack vector and impact, the audience votes for one of three suspects on their phones, he argues the defense and the prosecution, and the audience votes a final time. The deck holds around 150 slides in branching paths so the votes steer the session; blaming itself is framed as a game, not a culture to adopt.

### [04:11](https://youtu.be/VmPMUGImB-M?t=251) The three usual suspects
The suspects are the AI developer (the team that trained and released the model, responsible for model behavior and safety boundaries), the tool developer (the team behind the coding agent, plugin, or framework, responsible for architecture and secure design), and the end user (the developer running the tool, responsible for guardrails, configuration, credentials, and operational security).

### [06:26](https://youtu.be/VmPMUGImB-M?t=386) Case 1: Cameo, exfiltrating Copilot data as ASCII art
An attacker opens a PR carrying malicious instructions in invisible HTML comments. GitHub Copilot Chat blocks loading content outside the GitHub domain through its content security policy, but the camo.github.com image proxy is inside that domain. The attacker pre-builds one image per letter of the alphabet, prompts Copilot to render confidential information as ASCII art using camo image URLs, and reads the secrets back from the proxy access log as a sequence of letter requests. GitHub fixed it in 2025 by disabling image rendering entirely. The audience votes for the tool developer and holds that vote: the defense cites the content security policy and threat modeling already in place, while the prosecution notes GitHub knew Copilot reads PRs as context yet never threat-modeled the PR plus prompt-injection plus camo combination.

### [12:07](https://youtu.be/VmPMUGImB-M?t=727) Case 2: Probllama, Ollama remote code execution
Ollama shipped with no built-in authentication and a container image bound to 0.0.0.0 as root. Its `/api/pull` endpoint fetches a model manifest from a URL and writes files to an attacker-chosen path, so a crafted manifest drops a backdoored library plus an `ld.so.preload` entry and yields remote code execution with CVSS 9.8. The fix blocked path traversal outside the model directory and added manifest digest validation. The vote splits neck and neck between tool developer and end user before settling on the tool developer; several voters switch after the defense argues Ollama was an open-source local-development tool never designed for internet exposure, countered by the prosecution pointing at the 0.0.0.0 Docker default and the missing digest check.

### [17:28](https://youtu.be/VmPMUGImB-M?t=1048) Case 3: AWS MCP server shell injection
A developer connects a coding agent such as Claude to the AWS MCP server to manage infrastructure through natural language. A prompt-injection payload smuggled into a repo, PR, or issue makes the agent call the MCP server with attacker parameters, which the server concatenates directly into shell strings, giving remote command execution and reverse shells with no visible trace. AWS fixed it with a function validating user intent before execution and by moving from shell invocation to OS-level calls. The vote for the tool developer is conclusive and nobody changes it: string concatenation of untrusted input is CWE-78 straight out of the OWASP Top 10, and a trust boundary at the agent does not remove the need for defense in depth at the server.

### [23:13](https://youtu.be/VmPMUGImB-M?t=1393) Case 4: wormable command execution via VS Code settings
The GitHub Copilot plugin for VS Code could modify its own environment configuration, including the project's settings file. With the agent running in YOLO mode, a prompt-injection payload flips the auto-approve flag from false to true and plants arbitrary commands that execute on every VS Code startup, giving persistent remote code execution (CVE-2025-53773, CVSS 7.8 on the slide). The fix tightened plugin permissions on IDE settings, sanitized intent input and output, and added an audit trail for settings changes. The audience blames the tool side again: the defense notes YOLO mode was user-enabled and the patch shipped within a week, while the prosecution argues VS Code handed every plugin the keys to its own security with no audit trail.

### [27:53](https://youtu.be/VmPMUGImB-M?t=1673) The invisible collaborator
The same self-modification pattern recurs across agents: a slide lists six CVEs in Claude Code, Cursor, Roo Code, and Gemini CLI where prompt injection silently overrides agent settings to reach code execution. Sepehrifar names the broader pattern the invisible collaborator: an attacker with write access to any shared context (a PR, a dependency, a template, a translation file) plants instructions in agent configuration such as Cursor rules, Copilot instructions, or Claude config files, and the assistant follows them. AI-generated code already inflates PR sizes by about 60%, so poisoned output hides in diffs nobody fully reviews.

### [31:33](https://youtu.be/VmPMUGImB-M?t=1893) The mental-model gap
Users build a mental model of a new technology and keep it while the technology evolves: email in 1993–1997 looked like electronic post, and twenty years later phishing still exploits the assumption that the sender on the envelope is trustworthy. The iceberg slide applies this to agents: the user sees a productivity feature under control in a chat window on a safe local machine, while the attacker sees an autonomous agent holding credentials, loyal to instructions rather than to the developer, sharing one weakly-linked context. Untrusted repositories get accepted with a click nobody reconsiders.

### [34:13](https://youtu.be/VmPMUGImB-M?t=2053) The attack chain, end to end
Every case follows one chain: prompt injection finds a link into shared context, context manipulation plus path traversal or settings modification follows, then remote code execution, data theft, guardrail overrides, and finally tool impersonation, where a rogue MCP server answers in place of the real one. Three examples underline that some attacks are near-inevitable: Copilot's own MCP mixing private and public repositories under one token so a public issue can expose private code, fifteen malicious AI plugins in the JetBrains marketplace in February 2026 harvesting data, and an Anthropic report from October 2025 showing about 250 documents can poison a model trained on billions.

### [36:17](https://youtu.be/VmPMUGImB-M?t=2177) Shared responsibility, not blame
The closing argument replaces the blame game with a shared-responsibility model: model providers deliver the model safely, tool providers threat-model their products, and developers consume tools safely. A single small vulnerability turns the whole internet into the attack surface, and the human stays the weakest link. The parting analogy is beer: the point is not abstinence but knowing what you drink, choosing the place and the quality, not spilling it, and telling others what you found. In Q&A, asked whether everybody responsible means nobody responsible, Sepehrifar answers that the responsibility is communal (share what you know) and personal (own what you consume).

## Tools, libraries and specs
- GitHub Copilot Chat and Copilot VS Code plugin (incl. YOLO mode with auto-approve)
- camo.github.com (GitHub image proxy)
- Ollama (`/api/pull`, `/api/push`, Docker image)
- AWS MCP server
- Claude Code, Cursor (v1.3.9, ≤1.7), Roo Code (<3.22.6), Gemini CLI
- OWASP Top 10 / CWE-78 (OS command injection)
- CVSS scores as cited per case (9.8, 7.8, plus the settings-exposure slide)

## Who should watch
Developers who run AI coding agents with broad permissions and want concrete exploit stories to calibrate their caution, especially beginners in AI security. Practitioners already tracking prompt-injection CVEs can skip the case walkthroughs and take only the shared-responsibility framing.

## Verdict
**5/10**: four public AI-tool CVEs, with clear mechanisms in Cameo, Probllama and the VS Code case, held together by an attack-chain recap, but the evidence is second hand, no exploit runs and nothing is published.

**Novelty 1/2**

- **+** [27:53](https://youtu.be/VmPMUGImB-M?t=1673) The speaker names one self-modification pattern across Claude Code, Gemini CLI, Cursor and Roo Code and calls it the invisible collaborator, an attacker writing instructions into shared context such as agent configuration files.
- **+** [34:13](https://youtu.be/VmPMUGImB-M?t=2053) The recap compresses the four vendor cases into one progression: prompt injection, context manipulation, path traversal or settings change, remote code execution, data theft, guardrail override, tool impersonation.
- **+** [30:32](https://youtu.be/VmPMUGImB-M?t=1832) Beyond the four cases it adds the Copilot MCP shared-token issue, fifteen malicious JetBrains marketplace plugins in February 2026 and the Anthropic poisoning report, so the talk gathers incidents from several sources.

**Demonstrated 1/2**

- **·** [01:37](https://youtu.be/VmPMUGImB-M?t=97) No exploit runs on screen; the talk is an audience-vote argument over four patched CVEs, so there is nothing for it to run.

**Measured 1/2**

- **+** [06:57](https://youtu.be/VmPMUGImB-M?t=417) The speaker says the CVSS scores shown are the official ones, not the vendor's, which gives the severity claims a stated basis.
- **+** [31:02](https://youtu.be/VmPMUGImB-M?t=1862) The poisoning figure of about 250 documents is credited by name to Anthropic's October 2025 report.
- **−** [29:28](https://youtu.be/VmPMUGImB-M?t=1768) The 60% growth in PR size is hedged ("if I am correct about the statistics") and carries no source or method.

**Depth 1/2**

- **+** [09:01](https://youtu.be/VmPMUGImB-M?t=541) The Cameo segment explains why the bypass works: the camo proxy sits inside the GitHub domain the content security policy allows, so the attacker reads the secrets back from the access log.
- **+** [33:08](https://youtu.be/VmPMUGImB-M?t=1988) The iceberg contrasts what the user sees (a productivity feature in a chat window) with what the attacker sees (an autonomous agent holding credentials and following instructions), a mental model sized for beginners.
- **−** [37:20](https://youtu.be/VmPMUGImB-M?t=2240) The shared-responsibility model the title argues for is one line per party and is not applied back to the four cases to show where blame would land.

**Reusable 1/2**

- **+** [34:13](https://youtu.be/VmPMUGImB-M?t=2053) The attack-chain stages give a viewer a sequence to check their own agent setup against.
- **+** [28:56](https://youtu.be/VmPMUGImB-M?t=1736) The question of when you last checked your agent configuration files points to a habit, though it is left for the viewer to reconstruct.
- **−** [38:25](https://youtu.be/VmPMUGImB-M?t=2305) No repository, checklist or configuration is offered; the closing mentions only the voting QR code.
