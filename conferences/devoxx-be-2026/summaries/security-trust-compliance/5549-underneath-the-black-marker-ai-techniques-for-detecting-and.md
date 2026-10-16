---
title: "Underneath the Black Marker: AI Techniques for Detecting and Reversing Redactions"
talkId: "5549"
conference: devoxx-be-2026
speakers: [David vonThenen]
track: Security, Trust & Compliance
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=wJ7R4qkVs8Y
durationMin: 50
slides: https://github.com/davidvonthenen/2026-devoxx-belgium/blob/main/Underneath_the_Black_Marker_AI_Techniques_for_Detecting_and_Reversing_Redactions.pdf
verdict: 7
reach: segment
frames: 11
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
---

# Underneath the Black Marker: AI Techniques for Detecting and Reversing Redactions

David vonThenen · Conference · Security, Trust & Compliance

Slides: https://github.com/davidvonthenen/2026-devoxx-belgium/blob/main/Underneath_the_Black_Marker_AI_Techniques_for_Detecting_and_Reversing_Redactions.pdf

## TL;DR

Redactions that only paint over content leave the underlying data recoverable, and this talk proves it with live demos: text under PDF black boxes is copied out, rolled back from revision history, and decoded from object streams, while pixelated and blurred text is recovered with open-source tools and a custom-trained OCR model. The closing argument is that real redaction removes data rather than obscuring its display.

## Key takeaways

- Black boxes drawn over PDF text without flattening preserve the text layer, so select-all plus copy exposes everything underneath; verify redactions by extracting text programmatically before publishing.
- PDFs that were saved repeatedly but never flattened keep incremental revisions, and rolling a file back to an older revision can restore pre-redaction content.
- PDF object streams can carry the original text in encodings such as ASCII85, so stripping the visible layer is not enough; the objects themselves must go.
- Email archives published alongside redacted documents can leak attachments as base64 blobs that OCR plus decoding reconstructs into the original images.
- Pixelation and Gaussian blur change the signal instead of removing it: grid-intensity matching (Depixelization), generate-and-test font rendering (unpixel), and GAN restoration (DeepMosaics) each recovered obscured text on screen.
- A redaction or obfuscation API can be turned against itself: pay for legitimate calls, generate blurred images from known text, and train a specialized OCR model that reads that service's output directly.
- Narrowing the attack to one obfuscation pipeline makes the model practical, since a single consistent pipeline keeps the variation the model must learn small.

## Notes

### [02:40](https://youtu.be/wJ7R4qkVs8Y?t=160) Why this talk: the DOJ releases

The motivating case is the US Department of Justice document releases of December 2025 and January 2026, published in tens of gigabytes and millions of pages, then repeatedly pulled and republished after redaction failures. Files disappeared from the DOJ site on December 20-21, 2025, a second batch followed on January 30, 2026, and about 9,500 documents were recalled again around February 6, 2026. The speaker frames the session as a set of thought exercises on how such documents fail, with all demos reproducible from his repository.

### [06:20](https://youtu.be/wJ7R4qkVs8Y?t=380) Copy-and-paste redaction failure

The first demo opens a released PDF with black-box redactions and copies the "redacted" text straight out of it, then pastes it into a file to display what sat under the boxes. A scripted version runs across a folder of PDFs and writes a `*-unredacted.txt` report (91 improper redactions found in the demo file), showing the same failure is exploitable in bulk. A frame of the side-by-side comparison shows the redacted page next to the recovered text.

### [14:48](https://youtu.be/wJ7R4qkVs8Y?t=888) PDF revisions and object streams

Two deeper PDF attacks follow. First, a PDF that was saved repeatedly without a final publish keeps every incremental revision, and a script rolls it back to the oldest version to recover earlier content. Second, a PDF posted online as a puzzle hides a passphrase in an object stream; copying the stream into an ASCII85 decoder fails on two invalid characters, deleting them reveals the passphrase "incremental updates". The lesson drawn is to read the manual for redaction tooling and understand flattening behavior.

### [21:34](https://youtu.be/wJ7R4qkVs8Y?t=1294) Email MIME attachments

Since most of the released material traveled by email, the talk turns to MIME metadata. A redacted email's published archive includes its attachment as a base64-encoded blob; OCR over the blob, followed by decoding and file-type identification from the header, reconstructs the original image with names intact. The speaker shows an adapted version rather than the real names.

### [24:12](https://youtu.be/wJ7R4qkVs8Y?t=1452) A sketch: data locality plus NER

An unbuilt idea closes the text section: communication clusters in time the way related disk blocks cluster physically, so named-entity recognition over unredacted messages sent near a redacted one could yield candidate names whose lengths fit a given black box. The speaker offers it as an exercise for the audience.

### [27:21](https://youtu.be/wJ7R4qkVs8Y?t=1641) Reversing image obfuscation

Three open-source projects are presented and then demoed. Depixelization matches pixel-block intensities against known OS default fonts scanning left to right; unpixel renders every candidate letter combination across supplied fonts and sizes and picks the pixelation pattern that matches; DeepMosaics uses generative adversarial networks to restore mosaiced images and video frame by frame.

### [32:01](https://youtu.be/wJ7R4qkVs8Y?t=1921) Three recovery demos

Depixelization recovers "Hello from the other side" from a pixelated image, rough but readable. Unpixel, sweeping 9 fonts against a mosaic-redacted image, ranks Liberation Sans first with confidence 1.00 (its match score is inverted: the winner sits at total=0.0000) and returns the word "admin", the correct answer. DeepMosaics cleans up a pixelated video of a moving dialog box; the box's movement across frames supplied varying pixelation samples that aided reconstruction, and the final restored frame is shown.

### [38:19](https://youtu.be/wJ7R4qkVs8Y?t=2299) A custom model that skips restoration

The speaker's own project drops image restoration entirely and predicts text directly from Gaussian-blurred images. The recipe: use the obfuscation service legitimately to turn known strings into blurred images, producing a (blurred image, original string) dataset, then train a PyTorch model on it. The architecture is SVTRv2, a connectionist temporal classifier scene-text recognizer that scans left to right and collapses repeated character predictions, the same family of model used in OCR. Training took about 14 hours on an H100; a safetensors checkpoint for CPU inference is published. The deck notes the attack generalizes: any customer list or output sample from the same service is readable by the trained model.

### [44:01](https://youtu.be/wJ7R4qkVs8Y?t=2641) Final demo and conclusions

Running `predict.py` on a blurred test image returns "a test david", matching the original exactly. The conclusions: specialize in one pipeline instead of attacking obfuscation in general, recognition is easier than pixel reconstruction, and security fails at its weakest link. The repo includes a bonus challenge PDF with a black box for the audience to attack at home.

## Tools, libraries and specs

- Depixelization_poc (Codeberg spipm) — pixel-block intensity matching against reference fonts
- unpixel (github.com/oioio-space/unpixel) — generate-and-test redaction reversal across fonts and sizes
- DeepMosaics (github.com/HypoX64/DeepMosaics) — GAN-based mosaic removal for images and video
- SVTRv2 — CTC-based scene text recognition model used for the speaker's deblurring model
- PyTorch — training framework for the custom model
- safetensors — published CPU inference checkpoint format
- ASCII85 stream decoding — used to recover the passphrase from the PDF object stream
- github.com/davidvonthenen/2026-devoxx-belgium — slides, all nine demos with commands, dataset and checkpoint links, bonus challenge

## Who should watch

Developers and security engineers who publish redacted documents or handle PII gain the most, since every failure mode maps to a concrete verification step. ML practitioners interested in OCR or adversarial uses of model distillation get a compact applied example. Viewers wanting formal redaction standards or compliance checklists should look elsewhere, and the ML architecture itself is summarized rather than taught.

## Verdict

**7/10**: working PDF and image-recovery demos with reproducible materials, limited by self-reported measurement and brief explanations of the recovery techniques.

**Reach segment**: security engineers and developers handling redacted documents or publishing sensitive images can apply the failure modes and verification techniques.

**Novelty 1/2**

- **+** [23:41](https://youtu.be/wJ7R4qkVs8Y?t=1421) The speaker adds his own unbuilt proposal for correlating nearby communications and black-box lengths to the collection of published redaction attacks.

**Demonstrated 2/2**

- **+** [06:52](https://youtu.be/wJ7R4qkVs8Y?t=412) Copying and pasting a black-boxed PDF exposes its concealed text on screen.
- **+** [33:04](https://youtu.be/wJ7R4qkVs8Y?t=1984) Depixelization produces a readable recovery of the pixelated input phrase.
- **+** [45:34](https://youtu.be/wJ7R4qkVs8Y?t=2734) The final demo runs the custom recognizer on a blurred image and checks the predicted text against the clear original.

**Measured 1/2**

- **+** [44:32](https://youtu.be/wJ7R4qkVs8Y?t=2672) Training is reported as about 14 hours on an H100, giving a resource estimate without a baseline or measurement method.
- **−** [46:04](https://youtu.be/wJ7R4qkVs8Y?t=2764) The custom-model results conclude without test-set accuracy or an evaluation across blur strengths to establish how reliably the recovery works.
- **−** [47:06](https://youtu.be/wJ7R4qkVs8Y?t=2826) The claim that a trained model could read other customers’ output from the same service is not backed by a cross-customer evaluation.

**Depth 1/2**

- **+** [29:24](https://youtu.be/wJ7R4qkVs8Y?t=1764) Unpixel’s generate-and-test mechanism is explained through font candidates and the lightness of pixelated boxes.
- **+** [42:59](https://youtu.be/wJ7R4qkVs8Y?t=2579) The CTC explanation follows character predictions, blank markers and duplicate collapse to show how OCR emits text.

**Reusable 2/2**

- **+** [48:09](https://youtu.be/wJ7R4qkVs8Y?t=2889) The linked talk repository supplies the demo code and commands, plus links to the generated dataset and CPU inference checkpoint for the custom-model example.
