---
title: "Decoding the Cosmos: Voyager's 1970s Algorithms Meet Today's Cutting-Edge Tech"
talkId: "22946"
conference: devoxx-be-2026
speakers: [Pieter van der Meer]
track: Mind the Geek
sessionType: Conference
audienceLevel: INTERMEDIATE
video: https://www.youtube.com/watch?v=CuvV3Aud3Q0
durationMin: 41
slides: null
verdict: 7
reach: niche
frames: 8
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15
# Decoding the Cosmos: Voyager's 1970s Algorithms Meet Today's Cutting-Edge Tech

Pieter van der Meer · Conference · Mind the Geek

## TL;DR

Voyager still phones home across 25 billion kilometers on 23 watts because its signal is wrapped in a 1970s convolutional code decoded by the Viterbi algorithm. The speaker rebuilds that decoder live, shows the same algorithm tagging named entities in sentences, then denoises signals with a TensorFlow autoencoder to connect vintage error correction to modern machine learning.

## Key takeaways

- Voyager's downlink survives because of forward error correction: each input bit becomes two coded bits, so the ground station can reconstruct the original even with corrupted bits.
- Viterbi decoding is a trellis search that keeps the most likely path by Hamming distance and discards the rest; the demo recovers 1- and 2-bit errors and breaks at 3.
- The same Viterbi search powers named-entity recognition: states become entity tags, transitions become tag probabilities, and the traceback yields the best tag sequence.
- A plain denoising autoencoder can strip noise from a sine wave and even from bits on a carrier, but training and testing on the same noise profile is cheating, not a result.
- Link budgets are won by antennas and coding, not raw power: Voyager's 23 W reaches a 70 m dish across interstellar space while a 0.2 W phone drops out two kilometers from a tower.

## Notes

### [00:33](https://youtu.be/CuvV3Aud3Q0?t=33) When Voyager 1 started talking gibberish

Late-2024 news drew the speaker in: Voyager 1 began sending gibberish after a memory chip died. NASA could still command it, requested a memory dump (a two-day round trip), reworked the code in a mix of Fortran and assembly to jump over the dead chip, uplinked the patch, and reestablished contact. Digging through NASA documentation for details surfaced hand-typed memos and the telemetry-encoding documents that became this talk.

### [03:41](https://youtu.be/CuvV3Aud3Q0?t=221) Voyager by the numbers and the Deep Space Network

Voyager 1 launched September 5, 1977 (Voyager 2 a few weeks earlier) and is now about 25.7 billion kilometers out, with a 24-hour one-way light time. It transmits at 23 W, holds about 51 kilobits of memory, and was designed for a ten-year mission to Pluto that never ended. NASA listens with 70 m Deep Space Network dishes in Madrid, Goldstone, and Canberra, uplinking at around 100 kW. A live DSN Now recording shows the contrast: the James Webb telescope at 28 Mbps while Voyager 2 trickles at 160 bits per second with received power near 10^-22 W. On a logarithmic scale, a strong phone signal sits near -60 dBm and Voyager near -160 dBm: roughly a billion times less power than a full-bars phone.

### [15:48](https://youtu.be/CuvV3Aud3Q0?t=948) Convolutional codes and the Viterbi algorithm

Peter Elias introduced convolutional codes in 1955, but nobody could decode them efficiently until Andrew Viterbi's 1967 algorithm (Viterbi later founded Qualcomm). The slide shows Voyager's actual code: the DSN legacy (7, 1/2) convolutional encoder, rate 1/2 with constraint length 7, one input bit producing two output symbols through XOR taps. A simplified K=3 version encodes the letter A step by step so the audience sees redundant bits accumulate.

### [19:57](https://youtu.be/CuvV3Aud3Q0?t=1197) Decoding live: the trellis walkthrough

The centerpiece is a self-built "convolutional coding explorer" web app. Starting from state 00 with received bits, each step extends every surviving path, scores branches by Hamming distance against the received pair, and discards losers when paths merge (a 5-loss path against a 3-loss path is dropped on screen). The traceback recovers the sent bits exactly; injected 1- and 2-bit errors still decode correctly, while 3 flipped bits produce gibberish, matching the code's guaranteed correction limit.

### [25:50](https://youtu.be/CuvV3Aud3Q0?t=1550) The same algorithm tags your sentences

Viterbi search reappears in NLP for text classification, sentiment analysis, and especially named-entity recognition. A second hand-coded demo runs Viterbi over "Alice works for Google in Paris" with a tiny vocabulary (a few persons, Paris/London/Berlin/Tokyo, three organizations). Per-word state probabilities and person-to-location transition chances feed the same trellis machinery, and the traceback yields Alice/PER works/O for/O Google/ORG in/O Paris/LOC.

### [31:46](https://youtu.be/CuvV3Aud3Q0?t=1906) Denoising signals with a TensorFlow autoencoder

A Jupyter notebook demo generates a sine wave, adds noise, trains a TensorFlow denoising autoencoder, and recovers a clean wave, shown as original, noisy, denoised, and merged plots. A harder variant with real bits modulated on a carrier also decodes to a usable signal. The speaker flags the cheat: the model trains on the same noise it is tested against. Researchers extend this idea seriously, training models that predict solar-flare interference during a receive window and adapt decoding.

### [34:23](https://youtu.be/CuvV3Aud3Q0?t=2063) AI at NASA, and why your phone loses signal

Other places AI meets space work: deep learning for gravitational-wave detection, AI-designed noise-resilient waveforms, autonomous spacecraft that cannot wait out a 20-minute Mars-Earth light delay, and an AI-designed antenna that took engineers two years to prove optimal. The closing comparison answers the opening question: a phone transmits 0.2 W to a tower at most 2 km away and still drops out, while Voyager's 23 W crosses 25 billion kilometers into a precisely aimed 70 m dish. Q&A adds that the Voyager fix meant hand-editing assembly jump addresses with the original toolchain so the faulty chip was never addressed.

## Tools, libraries and specs

- TensorFlow (denoising autoencoder demo, Python/Jupyter notebook)
- NASA Deep Space Network / DSN Now (live station data and link rates)
- Speaker's own local web demos (convolutional coding explorer, NER trellis; shown running, no published URL given)

## Who should watch

Developers and data scientists curious how error correction actually works, and anyone who likes a vintage-to-modern algorithm thread from 1970s space probes to NLP. Skip it if you already know convolutional codes and Viterbi decoding cold; the ML half stays at demo level and the decoding math is worked, not proved.

## Verdict

**7/10**: Three working demos connect convolutional decoding, NER and denoising, with the trellis explained down to path pruning, but the measurements remain illustrative and no reproduction artifact is shared.

**Reach niche**: Developers working with communications, signal processing or specialized NLP decoding can apply the main content; for most of the Java/JVM business-application audience it remains a curiosity subject.

**Novelty 1/2**

- **+** [05:47](https://youtu.be/CuvV3Aud3Q0?t=347) Research across NASA's hand-typed memos and telemetry documents brings Voyager's coding setup into a developer-oriented account.
- **+** [25:50](https://youtu.be/CuvV3Aud3Q0?t=1550) The talk connects Voyager coding, Viterbi decoding, NER tagging and ML denoising into one arc.
- **·** [15:48](https://youtu.be/CuvV3Aud3Q0?t=948) The credited history and established convolutional-coding material make the synthesis the added value.

**Demonstrated 2/2**

- **+** [23:36](https://youtu.be/CuvV3Aud3Q0?t=1416) The simplified decoder runs through to recovered data, with its output visible.
- **+** [30:02](https://youtu.be/CuvV3Aud3Q0?t=1802) The NER demo tags "Alice works for Google in Paris" end to end with the winning path traced through the trellis.
- **+** [32:49](https://youtu.be/CuvV3Aud3Q0?t=1969) The autoencoder notebook displays the noisy sine wave alongside the recovered signal.

**Measured 1/2**

- **+** [24:14](https://youtu.be/CuvV3Aud3Q0?t=1454) The error-injection runs recover one- and two-bit errors and fail with three in the shown example.
- **−** [14:44](https://youtu.be/CuvV3Aud3Q0?t=884) The phone-to-Voyager signal-strength comparison supplies quoted figures without an evaluation method.
- **−** [32:18](https://youtu.be/CuvV3Aud3Q0?t=1938) The speaker acknowledges optimizing the denoising model for the noise just added, leaving performance on other noise unmeasured.

**Depth 2/2**

- **+** [17:18](https://youtu.be/CuvV3Aud3Q0?t=1038) The encoder explanation follows an input bit into registers and logic that produce two output bits.
- **+** [22:02](https://youtu.be/CuvV3Aud3Q0?t=1322) The walkthrough explains accumulated Hamming distance as the metric used to compare candidate decoding paths.
- **+** [22:34](https://youtu.be/CuvV3Aud3Q0?t=1354) Comparing a distance-five path with a distance-three path explains why the decoder discards the less likely candidate.

**Reusable 1/2**

- **+** [31:46](https://youtu.be/CuvV3Aud3Q0?t=1906) The signal-generation and TensorFlow denoising recipe gives viewers a starting point to reconstruct.
- **·** [33:51](https://youtu.be/CuvV3Aud3Q0?t=2031) The notebook example ends without a published repository or reproduction URL.
