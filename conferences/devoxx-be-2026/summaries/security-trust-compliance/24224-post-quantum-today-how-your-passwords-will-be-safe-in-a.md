---
title: "Post-Quantum Today: How Your Passwords Will Be Safe in a Quantum Future"
talkId: "24224"
conference: devoxx-be-2026
speakers: [Julian Burr]
track: Security, Trust & Compliance
sessionType: Conference
audienceLevel: ADVANCED
video: https://www.youtube.com/watch?v=yUMnuh5U5k4
durationMin: 36
slides: null
verdict: 5
reach: segment
frames: 8
reviewedAt: 2026-10-15
---

# Post-Quantum Today: How Your Passwords Will Be Safe in a Quantum Future
Julian Burr · Conference · Security, Trust & Compliance

## TL;DR
Burr argues quantum computers threaten RSA and elliptic-curve cryptography through Shor's algorithm, and that "harvest now, decrypt later" attacks make migration urgent even though cryptographically relevant hardware is still years away. The talk builds a mental model of superposition, walks through Shor's period-finding and lattice-based cryptography with worked examples, then surveys where provider migrations stand. You leave understanding the threat and the fix, with pointers to the NIST standards and cloud roadmaps.

## Key takeaways
- Treat quantum processors as accelerators attached to classical computers, not replacements: only specific algorithms such as period-finding gain the speedup.
- RSA is safe because factoring is slow, not impossible; Shor's algorithm converts bad factor guesses into good ones with 37.5% success per attempt by finding the period of g^x mod n.
- The quantum part of Shor's algorithm is exactly one step (period-finding via the quantum Fourier transform); every other step is classical mathematics.
- "Harvest now, decrypt later" is the reason to migrate before the hardware exists: adversaries can store ciphertext today and decrypt it once quantum computers catch up.
- Of NIST's post-quantum families, lattice-based schemes lead adoption (Kyber, standardized as ML-KEM); no known classical or quantum algorithm solves the underlying lattice problems efficiently.
- If you run your own cryptography, switch to a standardized post-quantum algorithm (ML-KEM ships in Java 24 standard APIs); otherwise choose a provider with a dated migration plan, since Google, AWS and Azure all target roughly 2029-2030.

## Notes
### [00:33](https://youtu.be/yUMnuh5U5k4?t=33) Quantum computing as an enhancement
Burr opens with a disclaimer that the talk simplifies heavily and skips quantum physics, aiming instead for a working idea of how quantum computing threatens encryption. His first point: quantum computers do not replace classical ones. Vendors call the hardware quantum processing units because a QPU sits on top of a classical computer and accelerates computations it otherwise could not do. Classical bits hold one of 2^n states at a time; qubits in superposition can occupy all 2^n states simultaneously.

### [05:14](https://youtu.be/yUMnuh5U5k4?t=314) Superposition and the double-slit experiment
Superposition alone does not give free parallelism, which Burr illustrates with the double-slit experiment: light through two slits forms an interference pattern, even photon by photon, until measuring which slit was used collapses it to two spikes. Qubits behave the same way: feeding a superposition of candidate answers into a circuit yields a superposition of inputs and results, but measuring it collapses to one random answer, no better than brute force. The power comes from quantum algorithms, which arrange for wrong answers to interfere destructively and right answers constructively so the collapse most likely yields the correct result.

### [08:24](https://youtu.be/yUMnuh5U5k4?t=504) Shor's algorithm breaking RSA
RSA rests on factoring being impractical: Burr's rule of thumb is that each extra 10 digits multiplies factoring time by 10, from 10 minutes for 50 digits to trillions of years for RSA-2048. Shor's algorithm breaks this with number theory: for a bad guess g sharing no factor with n, g^p is a multiple of n plus 1 for some p, which rearranges into (g^(p/2)+1)(g^(p/2)-1), two better guesses. Finding p is the hard part classically, but g^x mod n repeats with period p, and a quantum Fourier transform extracts that frequency from a superposition of guesses efficiently. Each attempt succeeds 37.5% of the time (3 in 8), reaching 99% within 10 tries. Discrete-logarithm and elliptic-curve cryptography fall to similar algorithms.

### [18:23](https://youtu.be/yUMnuh5U5k4?t=1103) Why RSA still stands: qubits and error correction
Running Shor's on RSA-2048 needs many qubits: estimates fell from 20 million noisy qubits (2019) to about 1 million and then 100,000 (2025) as algorithms and error correction improved, while the largest QPUs have around 1,000 physical qubits. Burr stresses these numbers are hardware-specific and fast-moving. Quantum error correction cannot reuse classical methods, so it remains an active research field whose progress keeps lowering the threshold. The takeaway: hardware is orders of magnitude away, but approaching faster than intuition suggests.

### [21:00](https://youtu.be/yUMnuh5U5k4?t=1260) Harvest now, decrypt later and the NIST competition
The urgency comes from harvest-now-decrypt-later attacks: adversaries store encrypted state secrets, medical or browsing data today and decrypt once the hardware arrives. NIST has run a multi-year competition with Google, IBM and Amazon to standardize quantum-resistant algorithms, producing four families: lattice-based, hash-based, code-based and multivariate-based, including Kyber and Dilithium. The strategy in each case is to find mathematical problems without the periodic structure that quantum algorithms exploit.

### [23:36](https://youtu.be/yUMnuh5U5k4?t=1416) Lattice-based crypto and learning with errors
A lattice is the grid of points reachable by combining basis vectors; finding the lattice point closest to a target is hard, especially in hundreds of dimensions with a "bad basis" of long, near-parallel vectors. That good-basis versus bad-basis asymmetry suggested public and private keys, and a late-1990s scheme (GGH) tried exactly that but leaked the private key, which is why NIST candidates undergo years of attack testing. Modern schemes use learning with errors instead: the public key is a set of linear equations the private vector (Burr's example: 10, 82, 50, 5) satisfies, with results taken modulo a large number and perturbed by small random errors (minus 4 to plus 4), defeating linear algebra. To send a bit, the sender sums some equations and adds half the modulus for a 1; the receiver compares against the true value and checks whether the gap is nearer zero or half the modulus. The frame at 28:00 shows the private vector beside its six public equations.

### [32:27](https://youtu.be/yUMnuh5U5k4?t=1947) Migration roadmaps and what to do now
Google's published plan migrates harvest-now-decrypt-later exposure first (ALTS and key management done first, APIs next) and targets full quantum safety by 2029; the circular roadmap frame lists dated items from 2025 ALTS migration through 2026 APIs, 2027 load balancing, 2028 client libraries and KMS algorithms. AWS and Azure follow essentially the same timeline toward 2029-2030. Kyber won the NIST competition in 2022 and was standardized as ML-KEM in 2024, with support in most languages' core libraries. The closing resources slide links the Google, AWS and Azure roadmaps plus the explainer videos behind the lattice material.

## Tools, libraries and specs
- ML-KEM (standardized Kyber, NIST 2024): lattice-based key encapsulation; available in Java 24 standard APIs
- ML-DSA and SLH-DSA: NIST post-quantum signature schemes appearing in cloud KMS offerings
- NIST post-quantum cryptography competition: source of the standardized algorithms
- Google Cloud migration roadmap ("PQC in Plaintext"): ALTS migration, API endpoints, client libraries, Cloud KMS, Confidential Computing
- AWS post-quantum cryptography page and KMS timeline; Azure "Accelerating the quantum-safe timeline"

## Who should watch
Developers and architects who want a conceptual grounding in why post-quantum migration matters now and how the replacement math works. Skip it if you already understand Shor's algorithm and learning with errors, or if you need implementation code rather than the ideas behind it.

## Verdict
**5/10**: a conceptual tour from qubits to migration timelines that joins credited sources, limited by unsourced numbers and migration advice left to reconstruct.

**Reach segment**: architects and teams who choose providers or run their own cryptography can act on the migration guidance within the year; most attendees take background rather than an applicable change.

**Novelty 1/2**

- **+** [32:27](https://youtu.be/yUMnuh5U5k4?t=1947) The talk joins three strands no single search result covers together: Shor's internals, lattice-based internals, and Google's dated migration roadmap.
- **·** [35:36](https://youtu.be/yUMnuh5U5k4?t=2136) The core material traces to credited sources (Google's roadmap post, NIST standards, the explainer videos behind the Shor, lattice and learning-with-errors slides, the last of which supplies the worked example), so watching organizes rather than replaces them.

**Demonstrated 1/2**

- **·** [01:35](https://youtu.be/yUMnuh5U5k4?t=95) The talk sets itself up as a conceptual journey with no runnable artifact at stake and carries its claims through worked equations and diagrams on slides.

**Measured 1/2**

- **+** [09:58](https://youtu.be/yUMnuh5U5k4?t=598) The RSA factoring rule of thumb (each extra 10 digits multiplies the time by 10) comes with 10 minutes at 50 digits, 2 hours at 60 and 20 hours at 70, extended to trillions of years at RSA-2048.
- **+** [18:55](https://youtu.be/yUMnuh5U5k4?t=1135) The qubit estimates are dated and compared against current hardware: 20 million (2019) down to 100,000 (2025) versus roughly 1,000 physical qubits today.
- **−** [09:28](https://youtu.be/yUMnuh5U5k4?t=568) The factoring times name no machine or method ("with a normal computer") and the qubit estimates are quoted without method, which the speaker flags as hardware-specific numbers to take with a grain of salt.

**Depth 1/2**

- **+** [12:02](https://youtu.be/yUMnuh5U5k4?t=722) The Shor's algorithm derivation shows each mathematical step from the bad guess through period-finding to the improved factors, and places the quantum computation in that one step.
- **+** [28:14](https://youtu.be/yUMnuh5U5k4?t=1694) The learning-with-errors section explains why each mechanism exists (the modulus, the error bounds, the half-modulus margin for distinguishing bits), after the earlier geometric scheme GGH was broken because the public key leaked information about the private key.
- **·** [29:16](https://youtu.be/yUMnuh5U5k4?t=1756) The learning-with-errors example is the speaker's simplified version ("the implementation of Kyber and other algorithms does a lot more steps"), and the other post-quantum families are set aside as not needed, so how ML-KEM itself works and how the schemes trade off stays outside the talk.

**Reusable 1/2**

- **+** [34:34](https://youtu.be/yUMnuh5U5k4?t=2074) The talk points to standardized algorithms in standard libraries, naming ML-KEM in Java 24 APIs as the switch to make.
- **−** [34:03](https://youtu.be/yUMnuh5U5k4?t=2043) The migration advice ships with no sample project, configuration, or checklist, so viewers reconstruct the change themselves from the linked roadmaps.
