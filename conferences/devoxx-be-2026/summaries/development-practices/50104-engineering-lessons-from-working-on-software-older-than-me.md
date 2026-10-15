---
title: Engineering Lessons from Working on Software Older Than Me
talkId: "50104"
conference: devoxx-be-2026
speakers: [Guust Ysebie]
track: Development Practices
sessionType: Lunch Talk
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=VaT7DgmVSms
durationMin: 34
slides: null
verdict: 7
frames: 8
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Engineering Lessons from Working on Software Older Than Me

Guust Ysebie · Lunch Talk · Development Practices

## TL;DR

A senior Apryse engineer distills five lessons from maintaining PDF tooling, a format older than he is: solve the right problem, treat adoption as the hard part, open the rules, make noise, and take initiative. The payoff is a first-hand account of pushing Brotli compression into the PDF specification to shrink everyday files by about 20%.

## Key takeaways

- Ask the data supplier for structured data before writing a parser against a rendering format.
- A technically better format still loses without frictionless distribution, funded marketing, and user trust.
- Open the specification and pursue ISO status so policy can reference the format and no single vendor stays a point of failure.
- A feature for a mature ecosystem needs producer and reader implementations plus public pressure, or producer-viewer chicken-and-egg kills it.
- New compression must earn its place through maturity, licensing, reference implementations, and interop; raw ratio alone does not win.
- A prototype, an article, press noise, and pull requests to two major viewers can move a global specification.

## Notes

### [02:42](https://youtu.be/VaT7DgmVSms?t=162) A startup parsing job and how PDF actually works

Three months into his first job at a startup, Ysebie had to extract data from inbound PDFs into a database. Text came out in the wrong order, and "hello world" appears nowhere in the file: PDF has no tables, lists, or images, only positioned content. The 1993 motivation was fixed layout: the same document rendered differently on every system, so Adobe made it identical everywhere. A PDF page is a white sheet plus concatenated stack-based drawing programs (select a font, move to a pre-calculated position, draw glyphs). Lesson 1: solve the right problem. Instead of parsing a rendering format, he should have phoned the supplier and asked for JSON.

### [08:01](https://youtu.be/VaT7DgmVSms?t=481) Why PDF outlived every challenger

Every couple of months Hacker News or Lobsters hails a PDF killer, and even Microsoft's XPS, shipped with Vista, failed. Challengers fix real annoyances (small screens, reflow, extraction, editing) but forget what PDF already solved: fixed layout, print fidelity, digital signatures, and true content redaction. Lesson 2: the hard problem is adoption. A format needs distribution, investment in marketing, and trust in stable behavior. Good engineering solves a problem; then adoption begins.

### [12:39](https://youtu.be/VaT7DgmVSms?t=759) Free Reader, open spec, ISO standard

Adobe charged for PDF creation but shipped Acrobat Reader free, removing end-user friction, then gave away the IP and opened the standard so Office, SDK libraries, and export tools could produce PDFs. Lesson 3, per the slide: "Open rules grow the ecosystem." The timeline runs 1993 PDF launch, 2005 PDF/A-1 archival (ISO 19005-1), 2008 PDF 1.7 (ISO 32000-1), 2017 PDF 2.0 (ISO 32000-2) with Adobe proprietary pieces such as XFA removed. ISO status lets laws reference the format, for example to require accessible PDFs.

### [18:52](https://youtu.be/VaT7DgmVSms?t=1132) Changing a format everyone uses

Spec additions hit vendor-side adoption: producers will not emit a feature no viewer renders, and viewers will not render a feature no file uses. Lesson 4: generate noise. The process runs propose (with the PDF Association and industry evidence), draft the spec with heavy prototyping, implement both producer and reader sides, then roll out safely. Publication in the spec is only a milestone; an unused feature delivers no value.

### [21:28](https://youtu.be/VaT7DgmVSms?t=1288) Case study: Brotli compression for smaller PDFs

A slide shows content-stream syntax where one rectangle and the word HELLO take a dozen instructions with repeated coordinates and per-glyph positions, all squeezed by 1980s Flate. The PDF Association picked Brotli over a rival modern codec: PDFs are written once and decompressed constantly, and the rival's 5-10% edge in some cases did not beat Brotli's fast decompression on top of roughly 20% over Deflate. Ysebie implemented it in Java in iText, published "Want to make your PDFs 20% smaller for free?", posted it to Hacker News, and rode the noise through Heise into broad press. He sent pdf.js a pull request (Mozilla reimplemented it themselves a day later), nudged Chromium's PDF viewer into support weeks later, and watched smaller viewers follow. Brotli became part of the official spec a few months before the talk.

### [33:01](https://youtu.be/VaT7DgmVSms?t=1981) Initiative moves ecosystems

Lesson 5: a little initiative takes you far. The pipeline is propose, implement, deploy; Brotli sits in implementation, and deployment within a couple of years should shrink everyday PDFs by about 20%.

## Tools, libraries and specs

- iText SDK (Apryse): open-source PDF SDK where the speaker implemented Brotli
- PDF 2.0 (ISO 32000-2), PDF/A-1 (ISO 19005-1): the standardized spec and its archival subset
- Brotli, Flate/Deflate: the new and the incumbent content-stream compression
- pdf.js (Mozilla), Chromium PDF viewer: the two major viewers lobbied into Brotli support
- XPS: Microsoft's failed PDF competitor, shipped with Windows Vista

## Who should watch

Maintainers of long-lived libraries and formats, and anyone trying to land a change in a standardized ecosystem, get a playbook with receipts. Viewers wanting PDF API coding should read the iText docs instead, and compression specialists will find the codec analysis brief.

## Verdict

**7/10**: First-hand account of pushing Brotli into the PDF spec, with the 20% claim set against a named Deflate baseline but no measurement method and no artifact to reuse.

**Novelty 2/2**

- **+** [27:17](https://youtu.be/VaT7DgmVSms?t=1637) The Brotli campaign play-by-play (PDF Association article, Hacker News, Heise pickup, a pull request to pdf.js, lobbying Chromium) is first-hand standards work no search result gives.
- **+** [24:42](https://youtu.be/VaT7DgmVSms?t=1482) The codec rationale comes from inside the selection process: maturity, licensing, C reference implementations, and cross-vendor interop.
- **+** [32:00](https://youtu.be/VaT7DgmVSms?t=1920) The campaign's outcome is stated: the Brotli specification is released, and software that cannot decompress Brotli streams no longer supports PDF 2.0.

**Demonstrated 1/2**

- **·** [22:04](https://youtu.be/VaT7DgmVSms?t=1324) A lessons-and-standards narrative with nothing to execute on stage; evidence appears as slide content such as the content-stream walkthrough.

**Measured 1/2**

- **+** [26:16](https://youtu.be/VaT7DgmVSms?t=1576) The codec comparison names its baseline: a rival codec 5-10% better than Brotli in some cases, set against roughly 20% over Deflate.
- **−** [27:30](https://youtu.be/VaT7DgmVSms?t=1650) The headline figure (15-25% smaller files with zero quality loss) arrives as a conclusion, with no corpus, file sample, or measurement setup.
- **−** [28:19](https://youtu.be/VaT7DgmVSms?t=1699) The campaign's reach is self-reported ("this article did quite well", "like 10 comments") with no baseline.

**Depth 2/2**

- **+** [05:21](https://youtu.be/VaT7DgmVSms?t=321) The PDF mental model (white page plus stacked drawing programs with pre-calculated positions) explains why extraction and reflow fail.
- **+** [06:24](https://youtu.be/VaT7DgmVSms?t=384) Every visible element must also be written into the file, which is why PDFs get large and why compression is worth a spec change.
- **+** [24:11](https://youtu.be/VaT7DgmVSms?t=1451) The codec choice weighs maturity, licensing, reference implementations, interop, and the write-once/decompress-often pattern.

**Reusable 1/2**

- **+** [20:27](https://youtu.be/VaT7DgmVSms?t=1227) The propose, draft, implement-both-sides, roll-out sequence is a practice a reader can follow, though it is described and not packaged.
- **·** [01:38](https://youtu.be/VaT7DgmVSms?t=98) The one pointer is the speaker's employer's open-source iText SDK repository, which the talk does not tie to the Brotli work.
- **−** [26:46](https://youtu.be/VaT7DgmVSms?t=1606) The Java Brotli implementation, the article and the pull requests are described without a link, sample project, configuration or checklist.
