---
title: The Dark Secrets of Computer Science
talkId: "10031"
conference: devoxx-be-2026
speakers: [Fabien Marsaud]
track: Mind the Geek
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=2Yh7LKt8YNw
durationMin: 49
slides: null
verdict: 5
reach: broad
frames: 10
reviewedAt: 2026-10-15
---

# The Dark Secrets of Computer Science

Fabien Marsaud · Conference · Mind the Geek

## Key takeaways

- Money arithmetic in floating point bills 9.9999999 instead of 10: count in minor units or use BigDecimal.
- Every partner validates email with a different regex, so orders stall between disagreeing systems.
- Signed 32-bit time overflows on 19 January 2038 to 13 December 1901, not back to 1970.
- Case-insensitive Windows passes a misspelled filename that breaks on Linux in production.
- Bulk Excel imports undo validated pipelines: zeros vanish, dates swap, formats are ignored.

## Notes

### [02:07](https://youtu.be/2Yh7LKt8YNw?t=127) Debates and HTTP codes

Polls split the room on Lombok, Maven versus Gradle, ISO 8601 versus timestamps. Covered: official 418 (RFC 2324), Twitter's 420, Microsoft's 450, 451 for censored resources, plus joke RFCs 3514 and 9759.

### [05:47](https://youtu.be/2Yh7LKt8YNw?t=347) Encodings

KOI-8 garbled Russian files, and Unicode did not end it: a frame shows mangled French from AI-generated code, a tax-office email and a car stereo. Personal story: garbage in a file transfer came from a mainframe operator encoding metadata inside the file, unknown to everyone else.

### [08:53](https://youtu.be/2Yh7LKt8YNw?t=533) Floating point

For a Belgian operator, VAT-plus-discount math billed 9.9999999 instead of 10. NaN goes unchecked in most programs; the JDK detects it with `v != v`, shown from source on a frame.

### [11:00](https://youtu.be/2Yh7LKt8YNw?t=660) Dates

Leap seconds bridge atomic and solar time. Sweden sat a day ahead of Julian until 30 February 1712. Samoa skipped 30 December 2011 (UTC-11 to UTC+13), forcing JDK and airline patches.

### [13:41](https://youtu.be/2Yh7LKt8YNw?t=821) Regex and Y2K38

Every project validates email with its own regex despite RFC 5322, stalling orders between partners. Y2K was defused by patching, but 32-bit seconds overflow on 19 January 2038 to 13 December 1901, with 220 billion COBOL lines still active as of 2017.

### [18:26](https://youtu.be/2Yh7LKt8YNw?t=1106) Randomness and OTPs

Secure randomness must satisfy FIPS 140 and RFC 1750; PHP's generator once showed patterns. Cloudflare uses lava lamps, random.org atmospheric noise. Personal story: Belgian bank OTP tokens in the 2000s issued values increasing linearly over time.

### [21:03](https://youtu.be/2Yh7LKt8YNw?t=1263) Hashes, UUIDs, CORS

MD5 and SHA-1 fell to collisions; 2.71 quintillion random UUIDv4s give a 50% collision chance, so ID debates rage over a non-issue. CORS never works first try.

### [24:10](https://youtu.be/2Yh7LKt8YNw?t=1450) Line endings and filesystems

Endings descend from typewriters (Windows does CR+LF); FTP and AS/400 transfers rewrite them, Unicode added LS/PS. NTFS is actually case-sensitive but Windows keeps FAT behavior, so misspelled names fail only on Linux.

### [27:19](https://youtu.be/2Yh7LKt8YNw?t=1639) Windows, color, printers

Windows 11's TPM requirement pushes machine scrapping, and Rufus bypasses it. RGB and CMYK cover different spaces, so screen violets shift in print. Printers: outdated protocols, a scam business model, endless family tech support.

### [29:55](https://youtu.be/2Yh7LKt8YNw?t=1795) CSS and JavaScript

A clip soundtracks CSS centering, where a "simple change" costs two sprints. CSS gained OKLCH, fixing LCH's blue distortions. JavaScript's secret is "the whole thing": a frame shows the coercion table.

### [31:29](https://youtu.be/2Yh7LKt8YNw?t=1889) TypeScript Doom and C

TypeScript's type system is unsound; someone rendered Doom inside it as a VM: 3.5 trillion lines of types, 177 TB, 12 days per frame.

### [35:09](https://youtu.be/2Yh7LKt8YNw?t=2109) Null, Java, Raku

Null is address zero with decades of fallout; TypeScript has both null and undefined. Java developers write `true.equals(condition)`; Raku's tutorial hello-world is written in emoji.

### [37:16](https://youtu.be/2Yh7LKt8YNw?t=2236) People and process history

A tribute to Margaret Hamilton's assembly-coded Apollo guidance system. Post-2020, master became main and lists became blocklists. Pre-Git VCS was centralized; SOA's 2006-2012 era collapsed under hubris.

### [39:54](https://youtu.be/2Yh7LKt8YNw?t=2394) Excel and open source

Excel cripples pipelines: formats ignored, zeros vanish, dates swap. A clip shows Yun Van Demost's Excel stunts; marketing still emails `final-final-v2`. Then a tribute to curl and ffmpeg, and the closing slide asks for bone marrow donors.

### [43:41](https://youtu.be/2Yh7LKt8YNw?t=2621) Emulation and the 90/90 rule

MAME preserved arcade hardware, but encrypted ROMs needed CapsOff: acid decapping, microscope photos, volunteers transcribing bits. The Usual Suspects repeated it on the Roland JP-8000 with an LLM reading gates. The talk closes on Jira warfare and the 90/90 rule.

## Tools, libraries and specs

- Lombok, Maven, Gradle; ISO 8601; Java Time; RFC 2324, 3514, 9759, 5322, 1750; FIPS 140
- IEEE 754; JDK NaN semantics; BigDecimal; KOI-8, UTF-8, Windows-1252; Unicode LS/PS
- MD5, SHA-1, SHA-256; UUID v4; CORS; Spring Boot; NTFS/FAT; WSL; Rufus; TPM
- RGB/CMYK; CSS OKLCH; TypeScript type system; C undefined behavior; IOCCC; vi; Raku
- cURL; FFmpeg; MAME; CapsOff; Roland JP-8000; Git; Jira; Excel; COBOL

## Who should watch

Developers who enjoy shared industry pain, including students meeting these quirks for the first time. Specialists wanting depth, or anyone needing a citable reference, can skip it.

## Verdict

**5/10**: A humorous survey of software quirks with first-hand incidents and small practices to reuse, while its quantitative examples and technical explanations remain brief.

**Reach broad**: most of the conference's Java/JVM business-application developers encounter these encoding, arithmetic, date and data-import problems in their work within a year.

**Novelty 1/2**

- **+** [08:21](https://youtu.be/2Yh7LKt8YNw?t=501) The mainframe-metadata story is a first-hand production anecdote beyond the standard explanation of encoding problems.
- **+** [20:32](https://youtu.be/2Yh7LKt8YNw?t=1232) The speaker's token-engineering experience adds a personal case of unexpectedly increasing OTP values to the survey of randomness failures.
- **−** Individual curiosities such as Samoa's skipped date are already documented on Wikipedia's Samoa time-zone history page, limiting the novelty of the surrounding survey.

**Demonstrated 1/2**

- **·** [29:55](https://youtu.be/2Yh7LKt8YNw?t=1795) The CSS clip serves the humor survey rather than an end-to-end runnable claim, so a central demo is not fairly required.

**Measured 1/2**

- **+** [22:36](https://youtu.be/2Yh7LKt8YNw?t=1356) The quoted UUID collision figures put the risk in scale with 2.71 quintillion identifiers for a 50% collision chance and a billion per second for 86 years.
- **+** [33:06](https://youtu.be/2Yh7LKt8YNw?t=1986) The sourced Doom-in-TypeScript example supplies totals of 3.5 trillion lines and 177 TB with 12 days to compile its first frame.
- **−** [08:53](https://youtu.be/2Yh7LKt8YNw?t=533) The invoice figure of 9.9999999 instead of 10 remains an anecdote without its calculation reproduced, while the cited project totals provide no comparative measurement setup.

**Depth 1/2**

- **+** [16:50](https://youtu.be/2Yh7LKt8YNw?t=1010) The 2038 example explains how signed 32-bit seconds overflow from a future date into December 1901.
- **+** [24:10](https://youtu.be/2Yh7LKt8YNw?t=1450) Line endings are explained through typewriter mechanics, CR plus LF, file-transfer rewriting and Unicode separators.
- **·** [45:50](https://youtu.be/2Yh7LKt8YNw?t=2750) The closing Jira discussion continues the survey of familiar problems rather than developing a core mechanism or weighing design alternatives.

**Reusable 1/2**

- **+** [09:55](https://youtu.be/2Yh7LKt8YNw?t=595) BigDecimal or counting money in minor units gives a small practice to reconstruct from the floating-point example.
- **+** [11:00](https://youtu.be/2Yh7LKt8YNw?t=660) The displayed JDK NaN check supplies a code fragment showing why a value can compare unequal to itself.
- **−** [48:20](https://youtu.be/2Yh7LKt8YNw?t=2900) The closing QR code concerns bone marrow donor registration, and no repository, sample, configuration or checklist reproducing the survey's main content is offered.
