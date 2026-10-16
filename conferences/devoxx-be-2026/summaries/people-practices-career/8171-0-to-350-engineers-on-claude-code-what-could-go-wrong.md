---
title: "0 to 350 Engineers on Claude Code: What Could Go Wrong?"
talkId: "8171"
conference: devoxx-be-2026
speakers: [Nicolas Martignole]
track: People, Practices & Career
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=HzbNrEDZkYU
durationMin: 45
verdict: 8
reach: broad
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-15

# 0 to 350 Engineers on Claude Code: What Could Go Wrong?

Nicolas Martignole · Conference · People, Practices & Career

## TL;DR

Back Market's principal engineer Nicolas Martignole recounts taking Claude Code from 2 volunteer licenses to 350 users in a year, then hitting four collisions: unreviewable pull requests, cross-team refactors nobody owns, an $86k monthly API bill, and the people problem of scaling adoption. The fixes were structural rather than technical: PR-size discipline, contribution guidelines agents can read, a switch to OpenRouter plus OpenCode with a fixed $200 monthly cap per engineer, and an elected-resident community instead of AI champions.

## Key takeaways

- Generation is not velocity: when writing code costs nothing but human review time stays fixed, seniors drown in monster PRs and rubber-stamp them.
- Keep agent sessions short and split generation from test-writing; a week-long session resends its whole context on every Enter, and tests written by the same session that wrote the code are green by construction.
- Friction used to protect repositories (a frontend dev would never touch your Scala service); agents erase it, so CODEOWNERS, CONTRIBUTING.md files, and platform guardrails must state the boundaries for agents, not just humans.
- Never manage AI spend with an average: at Back Market the median was $40 while the mean was $141, dragged up by 3 developers burning $22.7k.
- Put a hard per-user budget ceiling in place from day one, because spend has no relationship to value generated.
- Adoption scales through an elected peer community with real decision power, not through appointed champions or external training.

## Notes

### [01:05](https://youtu.be/HzbNrEDZkYU?t=65) Organic rollout: 2 licenses to 350 users

Martignole, a principal engineer at Back Market (900 employees, ~300 in tech, operating in 18 countries), started in June 2025 with two tools, Cursor and Claude Code, bought quietly with a colleague and offered to volunteers with no executive mandate. Adoption grew through word of mouth: 30 pioneers by September, over 100 users after Okta SSO made Claude Code available to every employee around end of November, on the way to 350. Non-developers joined too: product managers fixing backlog bugs, engineering managers building their own tools. Back Market had to use Anthropic pay-as-you-go API pricing because the company sits between the fixed-price plans and the enterprise tier.

### [07:57](https://youtu.be/HzbNrEDZkYU?t=477) Collision 1: the monster pull request

A senior opens a PR with hundreds of insertions and few deletions from a junior who spent four minutes implementing a new currency: tests green, linter clean, mergeable. Multiplied across a team, reviewers are overwhelmed and "looks good to me" replaces real review. Four prompting failure modes feed this: the vague wish ("fix the bug", then coffee), context bloat (one session kept open all week, each Enter re-sending the full context at dollars a prompt), the green-test echo chamber (same session writes code and tests), and the doom loop (scolding the agent instead of rewinding). The remedies are spec-first work, short sessions, PR-size limits back from the Google engineering-practices era, and prompting skills such as Matt Pocock's. The speaker's rule of thumb: AI-generated code gets a human reviewer, human-written code gets an AI reviewer.

### [15:42](https://youtu.be/HzbNrEDZkYU?t=942) Collision 2: agents ignore your org chart

A team blocked by another team's legacy Python pricing service refactored and upgraded it unilaterally via agent and sent the PR. Before agents, stack friction acted as a firewall; that protection is gone across some 300 repositories, while 3 a.m. accountability still sits with the owning team. Back Market cleaned up CODEOWNERS (blurry on frontend repos), pushed CONTRIBUTING.md files that tell agents what each repo accepts, and leaned on platform guardrails. The prediction: next year's talks will be about agent factories.

### [20:25](https://youtu.be/HzbNrEDZkYU?t=1225) Collision 3: the $86,947 bill

June 2026 peaked at $86,947 for under 300 users, and a hard workspace usage cap froze every Claude Code user at Back Market until July 1, with the speaker debugging it from a conference audience. The anatomy slide breaks it down over 1,892 active user-months: median $40, mean $141, top 3 spenders $22.7k total, and the top spenders rotate monthly so manual coaching of outliers does not scale. The fix was switching to OpenRouter (83 providers, 31 shortlisted for GDPR zero-data-retention compliance) plus OpenCode, which imports Claude Code skills, rules, and CLAUDE.md files with the same shortcuts. Each engineer gets a fixed $200 monthly cap; a Slack bot grants a $20 extension after a short usage questionnaire, and squads with genuine needs get project budgets (the speaker runs 41 of them, $100-500 each, each tied to a business case). Result: $171k saved in three months with more users than before, shown as a month-by-month provider-spend chart. Under 150 users, he recommends staying on fixed-price plans; a $200 Claude Max seat represents roughly $7,000 of equivalent API tokens.

### [30:18](https://youtu.be/HzbNrEDZkYU?t=1818) Collision 4: the people problem

Rollout ran through elected residents: each of 40+ feature teams elects one peer (any level, any role), meeting Fridays to decide on skills, MCP servers, PR size, and tooling bets. This group, not management, killed Cursor after a mid-August license change. Everyone gets the same credit allowance regardless of rank. Non-developers needed access fixes (GitHub for PMs, an internal deploy platform instead of Vercel), and only 35% of engineering managers had tried Claude Code by March, so the speaker ran a two-hour managers workshop using agents for everything except code. He rejects vanity metrics (PR counts, lines generated) in favor of time-to-deploy stories. The most striking number: OpenRouter's September classification of 229 tech users shows code generation at 23.6% of activity, behind debugging, workflow execution, DevOps config, and Q&A.

### [38:10](https://youtu.be/HzbNrEDZkYU?t=2290) What worked

Four lessons: reviewing matters more than generating; fragile contribution norms explode under agents; fixed budgets are mandatory; community beats champions. Skills stay per-repository (a Python microservice skill differs from a Go one), blurry ownership or deploy rules must be clarified before agents find them, and the next step is a remote-agent platform for inhuman tasks like library upgrades. Closing line: AI will not replace developers, but developers using AI will replace the rest.

## Tools, libraries and specs

- Claude Code (Anthropic CLI agent, pay-as-you-go API pricing)
- OpenRouter (83 providers, 31 GDPR zero-data-retention shortlisted)
- OpenCode (provider-agnostic agent, imports Claude Code skills and CLAUDE.md)
- Cursor (dropped mid-August 2026 over a license change)
- Matt Pocock's agent skills (prompting and workflow skills for Claude Code / OpenCode)
- Crush, Pi (named as OpenCode alternatives)
- Anthropic API, Mistral-hosted open-weight models

## Who should watch

Engineering leaders, platform engineers, and principal-level individual contributors rolling out coding agents past the pilot stage gain the most, especially the cost-governance mechanics and the resident-community model. Working developers pick up prompting failure modes and the PR-size argument. Skip it if you want a tool tutorial or code-level agent technique; this is an adoption retrospective with no live demo.

## Verdict

**8/10**: A production-scale adoption retrospective with the speaker's own spend data and governance mechanics, limited to practices you must reconstruct yourself and with nothing to run.

**Reach broad**: Developers, tech leads and platform engineers in the audience who use or roll out AI coding assistants can apply the PR-size, session, repository-boundary, budget and peer-community practices.

**Novelty 2/2**

- **+** [23:00](https://youtu.be/HzbNrEDZkYU?t=1380) Spending April to June coaching the top spenders one by one worked for each person but did not scale, because the heavy spenders change every month; that failure is what pushed the team to a fixed budget.
- **+** [32:54](https://youtu.be/HzbNrEDZkYU?t=1974) The elected-resident group, not the CTO or a manager, decided to drop Cursor after its mid-August license change, a decision made by the community that the rollout was built around.
- **+** [34:29](https://youtu.be/HzbNrEDZkYU?t=2069) Most engineering managers had not tried Claude Code by March, so the speaker ran a two-hour workshop in which agents did everything except write code, to win them over before adoption stalled.

**Demonstrated 1/2**

- **·** [20:25](https://youtu.be/HzbNrEDZkYU?t=1225) An adoption retrospective has nothing to run live, so the evidence takes the form of console screenshots and charts rather than a demo.

**Measured 2/2**

- **+** [28:46](https://youtu.be/HzbNrEDZkYU?t=1726) Before/after monthly spend with per-provider bars backs the savings claim: ~$87k peak months versus ~$23-28k after the switch, $171k saved in three months with more users than in early June.
- **+** [22:30](https://youtu.be/HzbNrEDZkYU?t=1350) The spend distribution states its method: per-developer monthly spend over 1,892 active user-months from November 2025 to June 2026, giving median $40, mean $141 and $22.7k for the top 3.
- **−** [37:07](https://youtu.be/HzbNrEDZkYU?t=2227) The 23.6% code-generation share of activity among 229 tech users rests on OpenRouter's own prompt classifier, whose accuracy the speaker never validates.

**Depth 2/2**

- **+** [11:34](https://youtu.be/HzbNrEDZkYU?t=694) A session kept open all week re-sends its whole context on every Enter, adding three to five dollars each time, which is the mechanism behind the short-session and split-generation-from-tests remedies.
- **+** [16:15](https://youtu.be/HzbNrEDZkYU?t=975) The friction-as-firewall model explains why agents break cross-team norms, paired with the accountability reasoning behind the CODEOWNERS and CONTRIBUTING.md fixes.
- **+** [26:41](https://youtu.be/HzbNrEDZkYU?t=1601) The pricing choice is argued from constraints: Anthropic's per-user budget controls need a commitment of at least $1 million, leaving Back Market too big for the fixed price and too small for enterprise, which motivated the router.

**Reusable 1/2**

- **+** [27:12](https://youtu.be/HzbNrEDZkYU?t=1632) The $200 cap plus $20 Slack-bot extension plus project-exception budgets is described clearly enough to copy, though only in words and a screenshot.
- **+** [14:20](https://youtu.be/HzbNrEDZkYU?t=860) The Spec-First slide lists takeaway fragments (Clean Session Rule: spec in read-only mode, `/clear`, then run the execution; Plan Mode First; Matt Pocock's skills).
- **−** [43:58](https://youtu.be/HzbNrEDZkYU?t=2638) No repository, checklist or configuration is linked; the speaker points to his French YouTube channel for more detail.
