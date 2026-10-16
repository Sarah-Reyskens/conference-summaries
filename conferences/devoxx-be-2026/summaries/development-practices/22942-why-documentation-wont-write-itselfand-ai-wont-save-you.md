---
title: Why Documentation Won’t Write Itself—and AI Won’t Save You
talkId: "22942"
conference: devoxx-be-2026
speakers: [Christian Heitzmann]
track: Development Practices
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=A8TBUalnfdc
durationMin: 51
slides: https://link.simplexacode.ch/mix2
verdict: 6
reach: broad
frames: 10
summarizedAt: 2026-10-14
reviewedAt: 2026-10-15

# Why Documentation Won’t Write Itself—and AI Won’t Save You
Christian Heitzmann · Conference · Development Practices
Slides: https://link.simplexacode.ch/mix2

## TL;DR
Missing documentation stays missing unless teams decide what to write, for whom, and in which format; no Agile slogan, wiki, or AI assistant removes that decision. The talk builds the case on three foundations (audience and detail level, lightweight markup, docs as code), demonstrates AsciiDoc live in IntelliJ, and argues that human-written context matters more, not less, once AI enters the picture.

## Key takeaways
- Decide the audience and the level of detail before writing a word: architecture overviews, API references, and function internals each belong in a different place and format.
- Keep documentation in plain text next to the code (docs as code) so the same IDE, version control, reviews, and pipeline cover it; distance between code and docs is what lets docs rot.
- Drop Markdown for documentation in favor of AsciiDoc: the basics look nearly identical, while tables, cross-references, footnotes, includes, and diagrams work out of the box.
- Do not chase one documentation hub for everything; Javadoc-style output, guides, and management pages have different UI expectations and different distances from the code.
- Documentation must be handed to people, not searched for; querying an AI over the codebase is still searching, and it cannot surface decisions, rejected options, or history nobody wrote down.
- Make the specification (written before coding) the single source of truth rather than the source code, which contains bugs and no context; then use LLMs for spelling, grammar, and clarity, not for reverse engineering.

## Notes

### [00:31](https://youtu.be/A8TBUalnfdc?t=31) A new hire's first month
A developer joins a company that promised excellent documentation, then spends day one setting up a machine from outdated wiki pages, month one discovering there are no API comments or architecture records, and every month after that reverse engineering code. Asking management about docs earns either "we don't do that here" or a profanity, and the topic never comes up again.

### [03:06](https://youtu.be/A8TBUalnfdc?t=186) Three excuses for missing docs
"We work Agile" misreads every Agile author, none of whom argued against written documentation; Agile is about communication, and writing supports it. "No time or money" ignores the time new hires burn reconstructing undocumented systems (the speaker offers to do the math another time). "Code is documentation" fails twice: self-documenting code rarely survives contact with other readers, and even perfect code describes bricks, never the house built from them, which is the architecture.

### [06:43](https://youtu.be/A8TBUalnfdc?t=403) Four questions for the room
Most attendees have manually configured a system, written a long setup script, or built a disk image, yet almost nobody could recreate that system on a bare machine, and fewer still documented each step, let alone the reasons behind each step. The speaker admits he skips the "why" in his own internal notes too. Slides and examples for the talk are downloadable from the link on screen, repeated at the end.

### [09:49](https://youtu.be/A8TBUalnfdc?t=589) Foundation 1: audiences and altitudes
Documentation is a spectrum, not one thing, so each piece needs two parameters: who it addresses (external developers, internal developers, architects, product owners, managers) and its level of detail ("altitude"). Architecture overviews belong in external documents with diagrams, classes and APIs in Javadoc-style references, function internals in source comments; mixing these up puts architecture in comments or trivia in diagrams. The C4 model by Simon Brown is recommended as a starting point for layering.

### [13:26](https://youtu.be/A8TBUalnfdc?t=806) Foundation 2: lightweight markup languages
A markup language structures text in machine- and human-readable form; the lightweight variants keep the syntax from disturbing the writing flow, unlike LaTeX or raw HTML. The speaker's qualitative flexibility-versus-complexity chart places LaTeX at the powerful-but-costly extreme and Markdown at the simple-but-limited one, with AsciiDoc and reStructuredText as the compromise in the middle.

### [16:33](https://youtu.be/A8TBUalnfdc?t=993) Foundation 3: docs as code
Docs rot because code and documentation live in separate worlds (the codebase here, Confluence over there), so every code change silently skips the doc update. Treating docs like code means writing them in plain text in the same IDE, committing them to the same version control with the same review process, and rendering HTML or PDF from the same pipeline. Binary formats such as Word files in Git break this model.

### [19:34](https://youtu.be/A8TBUalnfdc?t=1174) 23 markup languages, one verdict
After evaluating the 23 lightweight markup languages listed on Wikipedia against published criteria, the speaker's top four are AsciiDoc, reStructuredText, MediaWiki, and Textile. Markdown gets its own slide for one reason: it has no standard (CommonMark and GitHub Flavored Markdown are still flavors), and anything beyond basics needs plugins or embedded HTML, which defeats the purpose. The verdict, shared with Eric Holscher's cited essay: do not use Markdown; AsciiDoc replaces it with nearly identical basic syntax (asterisks instead of dashes) and far more built in.

### [24:14](https://youtu.be/A8TBUalnfdc?t=1454) AsciiDoc live in IntelliJ
Using the AsciiDoc plugin for IntelliJ, the demo renders headings, paragraphs, images with alt text, hyperlinks, footnotes, lists, tables with column widths, and LaTeX-notation math formulas side by side with the source. Source inclusion pulls a whole Java file in with syntax highlighting from four lines, narrows to lines 20-26, then switches to tag-delimited snippets (T9/K) that survive line-number shifts and stay findable by full-text search across code and docs. Diagrams follow the same text model: blockdiag connections and PlantUML class diagrams re-render within a second of editing, with no drawing tool involved.

### [29:53](https://youtu.be/A8TBUalnfdc?t=1793) Wikis and the Confluence bill
Wiki stands for "where information kills itself": pages enter a document graveyard far from the code. Confluence specifically gets no praise: unusable search despite years of complaints, WYSIWYG-only editing stored in an internal binary format that makes export a one-way street, forced cloud migration with steep license steps (100 employees versus 101 jumps a whole tier), space-level access rights, and a support ticket that received a bot reply in under a minute and then nothing for three months.

### [34:28](https://youtu.be/A8TBUalnfdc?t=2068) Against the single documentation hub
Nobody would export generated Javadoc HTML into Confluence just to have one system, which proves different altitudes need different interfaces and different proximities to code. The speaker also stopped evaluating Confluence exporters entirely and recommends starting on a green field: a fresh system carries a shared agreement to keep it clean, while the old wiki stays a mess nobody feels responsible for. Of the generators surveyed, Antora is the AsciiDoc default (covered in the speaker's long-form article plus a showcase of documented open-source projects); Docusaurus, GitBook, and Hugo are Markdown-based, which rules them out on his terms, and Sphinx pairs with reStructuredText.

### [39:38](https://youtu.be/A8TBUalnfdc?t=2378) Documentation must be provided, not searched
The principle: a newcomer should be handed a package whose mastery means readiness, instead of spending days assembling puzzle pieces from code, Jira, tests, colleagues, stale wiki pages, and chat logs. Asking an AI over the loaded codebase repeats the searching pattern and dodges the guarantee. Documentation should cover the invisible parts: decisions and history, background and context, rejected designs with reasons, how-tos, open tasks and technical debt, emphases and warnings. Since RAG systems and agents answer from retrieved context, feeding them high-quality human documentation makes them perform better, which makes good documentation more important because of AI rather than obsolete through it.

### [45:47](https://youtu.be/A8TBUalnfdc?t=2747) Source of truth, AI for language, close
Of the three artifacts, the specification (before coding) should be the single source of truth: source code (during) contains bugs that would then become truth and carries no context, while documentation (after) qualifies only with context. LLMs still earn a place doing what they do best: accurate spelling, correct grammar, and clear expression, since sloppy language in the first paragraph destroys trust in the rest. The close quotes a LinkedIn comment almost verbatim (combine planning and documentation into one source of truth, also for AI, or admit the Wild West), then condenses the talk into markup language plus documentation system (AsciiDoc with Antora, or reStructuredText with Sphinx), organization (few responsible people, a style guide such as GitLab's), and AI (human docs as context, AI for language, never for reverse engineering). There was no time for questions; the session ends with the download link and a request for ratings.

## Tools, libraries and specs
- AsciiDoc with Asciidoctor, plus the AsciiDoc plugin for IntelliJ (by Alexander Schwartz) used in the demo
- Antora (AsciiDoc documentation generator) and its open-source showcase
- reStructuredText with Sphinx; Markdown (CommonMark, GitHub Flavored Markdown) argued against
- PlantUML and blockdiag diagram syntax inside AsciiDoc; reveal.js for AsciiDoc presentations; LaTeX and AsciiMath for formulas
- C4 model (c4model.com) for documentation layering; Javadoc as the API-doc layer
- Confluence, Docusaurus, GitBook, Hugo, MediaWiki, Textile as surveyed alternatives
- RAG systems, AI agents, and large language models (LLMs) for documentation context and language polish
- GitLab Documentation Style Guide as a template for documentation guidelines

## Who should watch
Developers and team leads who own internal documentation and wonder which format and toolchain to standardize on, especially teams currently centered on Confluence or Markdown wikis. Viewers wanting an Antora tutorial, a Sphinx comparison, or measured evidence for the ROI claims should look elsewhere; the talk points to articles instead of showing them.

## Verdict
**6/10**: Opinionated advocacy with a live AsciiDoc preview and a clear mental model of what documentation is for, held back by a docs-as-code pipeline that is described and never run, a 10x claim with no baseline, and an evaluation whose criteria stay in an article.

**Reach broad**: Most of the Devoxx Belgium audience writes or reviews team documentation, so the audience/altitude split, the docs-as-code setup, and the human-context-for-AI point are directly usable within the next year.

**Novelty 1/2**

- **+** [19:34](https://youtu.be/A8TBUalnfdc?t=1174) The speaker brings his own evaluation of the 23 lightweight markup languages in the Wikipedia table, ending in a ranked top four led by AsciiDoc.
- **+** [33:27](https://youtu.be/A8TBUalnfdc?t=2007) The Confluence case rests on firsthand consulting episodes, including a security ticket answered only by a bot for three months.
- **−** [20:36](https://youtu.be/A8TBUalnfdc?t=1236) The criteria behind the 23-language ranking are described in the speaker's article rather than shown on stage.

**Demonstrated 1/2**

- **+** [24:14](https://youtu.be/A8TBUalnfdc?t=1454) AsciiDoc source renders live in IntelliJ with tables, math formulas, and syntax-highlighted Java includes visible beside the markup.
- **+** [28:52](https://youtu.be/A8TBUalnfdc?t=1732) Edited PlantUML and blockdiag text re-renders into updated diagrams on screen within seconds.
- **−** [18:34](https://youtu.be/A8TBUalnfdc?t=1114) Committing docs to version control and generating HTML or PDF from the pipeline are described; no commit, review or pipeline run is shown.

**Measured 1/2**

- **−** [23:11](https://youtu.be/A8TBUalnfdc?t=1391) "With AsciiDoc you can do 10 times more" gives a multiplier with no baseline or method.
- **·** [04:07](https://youtu.be/A8TBUalnfdc?t=247) The return-on-documentation calculation is deferred for lack of time and sent to the speaker's articles, so it earns no `−`.

**Depth 2/2**

- **+** [21:38](https://youtu.be/A8TBUalnfdc?t=1298) Markdown is rejected for stated reasons (no standard, flavors differ, tables, cross-references and notes need plugins or raw HTML), with AsciiDoc as the replacement for the same basic syntax.
- **+** [34:58](https://youtu.be/A8TBUalnfdc?t=2098) The case against a single documentation hub weighs interface expectations, distance from code, and the effect of starting a clean system.
- **+** [42:42](https://youtu.be/A8TBUalnfdc?t=2562) Documentation is defined as the invisible part (decisions, history, rejected designs, how-tos, debt, warnings), with the argument that source code cannot supply it.

**Reusable 1/2**

- **+** [50:52](https://youtu.be/A8TBUalnfdc?t=3052) The linked zip supplies the AsciiDoc example from the live demo to start from.
- **−** [49:51](https://youtu.be/A8TBUalnfdc?t=2991) The organizational half (responsible owners, a style guide) is pointed at the GitLab guide and left to reconstruct, with nothing to copy in the zip.
