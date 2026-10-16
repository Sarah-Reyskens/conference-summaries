---
title: "Beyond encryption at rest: computing on encrypted data"
talkId: "16401"
conference: devoxx-be-2026
speakers: [Andrea Iacono]
track: Security, Trust & Compliance
sessionType: Conference
audienceLevel: BEGINNER
video: https://www.youtube.com/watch?v=ePQyy9sLmsY
durationMin: 51
slides: null
verdict: 7
reach: niche
frames: 14
summarizedAt: 2026-10-15
reviewedAt: 2026-10-15

# Beyond encryption at rest: computing on encrypted data

Andrea Iacono · Conference · Security, Trust & Compliance

## TL;DR

TLS and disk encryption leave one gap: applications decrypt data into memory before using it. Homomorphic encryption closes that gap by letting a server add and multiply values it cannot read, and this talk builds the idea from textbook RSA through noise budgets and bootstrapping to a live demo that scores cardiovascular risk on encrypted inputs.

## Key takeaways

- Treat in-memory cleartext as the weak link: network and disk encryption do nothing once the application decrypts data to work on it, and Heartbleed showed memory exposure can go unnoticed for years.
- Size BFV parameters to fit the circuit: declare the plaintext modulus and multiplicative depth up front so the library picks a modulus large enough to skip bootstrapping entirely (leveled SHE).
- Keep branching out of BFV circuits: approximating an `if` with polynomials costs more than bootstrapping, so compute the score on ciphertext and classify on the client.
- Match the scheme to the data type: BFV for exact integers, CKKS for approximate reals and ML workloads, TFHE for boolean gates and lookup tables.
- Test HE code with oracles through the real library: on noise overflow OpenFHE silently returns a wrong value instead of an error, so assert known answers at the boundaries with the production parameters.
- Budget four orders of magnitude, bootstrapping excluded: the demo ran about 20,000x slower than cleartext, and (de)serialization cost more than the homomorphic computation itself.

## Notes

### [01:03](https://youtu.be/ePQyy9sLmsY?t=63) Data lives in three places; only two are covered

Network traffic gets TLS and stored bytes get encryption at rest. Two caveats follow: under the US CLOUD Act an American provider can be compelled to hand over cleartext customer data even when stored in the EU, so keys should live with a different provider than the database. The running application then decrypts everything into memory, where Meltdown, Spectre, cold-boot attacks, Heartbleed and Cloudbleed all harvested it; the Heartbleed bug in OpenSSL went unnoticed for two years with no accounting of what was taken.

### [04:42](https://youtu.be/ePQyy9sLmsY?t=282) Homomorphic encryption, defined

An encryption scheme is homomorphic when `Enc(a) + Enc(b) = Enc(a+b)` and `Enc(a) * Enc(b) = Enc(a*b)`. The motivating example is a loan-rate service: the client encrypts its financial history, the server adds and multiplies ciphertexts without understanding them, and returns ciphertext the client decrypts into its rate. Addition plus multiplication suffices for arbitrary computation.

### [07:19](https://youtu.be/ePQyy9sLmsY?t=439) Textbook RSA is partially homomorphic

With hand-picked parameters, encrypting 65 and 12 and multiplying the ciphertexts yields exactly the encryption of 780, while adding them does not match. RSA therefore supports unlimited multiplications but no addition: a partially homomorphic scheme, limited to one operation type.

### [09:26](https://youtu.be/ePQyy9sLmsY?t=566) Learning with errors and the BFV scheme

The talk reduces learning-with-errors to scalars: given many pairs satisfying `b = a*s + e (mod q)`, find the secret `s`, where `e` is small random noise (real LWE uses polynomials with thousands of coefficients). BFV encryption layers the message on top as `c = a*s + e + (q/t)*m`. Here `q` bounds every value and `t` is the plaintext alphabet size: with `q=100, t=4` the range splits into four buckets, enough to encode a DNA sequence, and each bucket holds one message value.

### [14:40](https://youtu.be/ePQyy9sLmsY?t=880) Noise: additions are cheap, multiplications kill

A ciphertext lands somewhere inside its bucket; decryption subtracts `a*s` and reads whichever bucket remains. Each multiplication shifts that position, and after a few of them the value crosses into a neighboring bucket and decrypts wrong. Additions move it barely at all. Larger `t` means narrower buckets and fewer affordable operations. BFV with both operations but a bounded count is therefore called somewhat homomorphic encryption.

### [18:23](https://youtu.be/ePQyy9sLmsY?t=1103) Bootstrapping: Gentry's fix

Craig Gentry's answer is to decrypt the ciphertext homomorphically, using an encrypted secret key, which recenters the value in its bucket so computation can continue indefinitely. Division by the constant `q` becomes multiplication by its inverse; rounding and modulo need polynomial approximations built from additions and multiplications only. The catch is cost: bootstrapping one value over realistic polynomials takes tens of seconds. Unlimited additions and multiplications is the third level, fully homomorphic encryption.

### [22:06](https://youtu.be/ePQyy9sLmsY?t=1326) Demo app: cardiovascular risk score on encrypted inputs

The demo computes a weighted health score from age, total cholesterol, HDL, systolic blood pressure, hypertension medication and smoker status, with weights such as 3 for age and -2 for HDL, then labels the total low (under 500), medium, or high (over 1000). It uses OpenFHE, a C++ library with Python bindings and no Java binding. `build_context` selects BFV with plaintext modulus 2^16+1 and multiplicative depth 1, enabling PKE plus leveled SHE so the library sizes `q` to fit exactly one multiplication and bootstrapping is never needed.

### [27:18](https://youtu.be/ePQyy9sLmsY?t=1638) Client encrypts, server computes blind, client classifies

`encrypt_inputs` generates keys, serializes the crypto context (scheme plus `q` and `t`, no secrets) and each encrypted field to bytes via temporary files, and posts them to the server. The server deserializes in memory, multiplies each ciphertext by its weight and accumulates the score, then returns one encrypted number. Back on the client, decryption yields the score and the low/medium/high label is assigned locally, because branching under BFV is the most expensive operation of all and was deliberately kept out of the encrypted circuit.

### [34:47](https://youtu.be/ePQyy9sLmsY?t=2087) Live run: score 430, low risk

The live run worked end to end. The server log showed a 531,111-byte request whose JSON fields were ciphertext strings several thousand characters long (truncated to 50 characters on screen), proving the server never saw the inputs. Default inputs (age 30, cholesterol 200, and the rest) came back as encrypted 430, which the client decrypted and displayed as Low.

### [36:54](https://youtu.be/ePQyy9sLmsY?t=2214) Benchmark: about 20,000x slower than cleartext

On a log-scale chart, cleartext scoring took 0.43 microseconds against 7.71 milliseconds fully homomorphic. The server-side breakdown was deserialization 4.75 ms, homomorphic computation 2.15 ms, serialization 156.41 microseconds: moving bytes dwarfed the crypto. These numbers exclude bootstrapping, which would push the total into tens of seconds. The speaker guessed the same workload five years earlier would have run roughly ten times worse, as libraries and research keep closing the gap.

### [39:28](https://youtu.be/ePQyy9sLmsY?t=2368) Testing, branching, and the other schemes

When a value overflows its bucket, OpenFHE and similar libraries hand back a wrong number with no error, so testing means oracle cases with known answers, heavy on boundaries, run through the unmocked library with production parameters. Branching stays the hard part for BFV. Two other schemes cover different shapes: CKKS computes on vectors of approximate real numbers and suits machine learning, while TFHE offers boolean gates and lookup tables that would make classification nearly free but integer scoring expensive. Scheme choice is a trade-off driven by the workload's data types.

### [44:16](https://youtu.be/ePQyy9sLmsY?t=2656) Takeaway and Q&A

The closing message: FHE makes in-memory computation safe, it is expensive and limited, and it is worth it when data privacy matters. Questions covered ciphertext expansion (an audience member's figure, versus future breaks) answered with LWE's quantum resistance; real-world use in finance and health on small datasets; client trust, answered with open-source clients the user can inspect; and a pointer to Microsoft's managed HE offering on Azure.

## Tools, libraries and specs

- OpenFHE (C++ homomorphic encryption library, Python bindings, no Java binding)
- BFV scheme (exact integer arithmetic, leveled SHE mode)
- CKKS scheme (approximate real numbers, ML workloads)
- TFHE scheme (boolean gates, lookup tables)

## Who should watch

Developers and architects handling sensitive data in finance, health, or confidential AI who want a first mental model of homomorphic encryption plus a realistic cost picture. Cryptographers and anyone already shipping FHE can skip it: the math is deliberately scalar-simplified and the demo stays at one multiplication depth.

## Verdict

**7/10**: A live end-to-end encrypted computation with a beginner mental model of noise and bootstrapping, held back by standard core material, a benchmark with no stated method, and no published demo code.

**Reach niche**: Backend developers handling highly sensitive health or financial data could pilot the approach, but with no Java binding and a roughly 20,000x slowdown most of the Devoxx audience will not compute on encrypted data in their own work within the year.

**Novelty 1/2**

- **+** [22:06](https://youtu.be/ePQyy9sLmsY?t=1326) The cardiovascular risk-score app, with its six inputs, weights and low/medium/high thresholds, is the speaker's own worked example illustrating the standard RSA→LWE→BFV→bootstrapping arc.
- **·** [09:26](https://youtu.be/ePQyy9sLmsY?t=566) The speaker sends the learning-with-errors background to another session ("explained a lot better than I'm going to do it now"), so the theory arc is the established one.

**Demonstrated 2/2**

- **+** [34:47](https://youtu.be/ePQyy9sLmsY?t=2087) The client and server run live: default inputs are entered and the encrypted request is sent.
- **+** [35:52](https://youtu.be/ePQyy9sLmsY?t=2152) The server log shows a 531,111-byte request whose fields are ciphertext strings several thousand characters long (truncated to 50 on screen), and the client prints `Risk score: 430 (Low)` at [36:23](https://youtu.be/ePQyy9sLmsY?t=2183).

**Measured 1/2**

- **+** [36:54](https://youtu.be/ePQyy9sLmsY?t=2214) The log-scale chart compares 0.43 µs cleartext against 7.71 ms homomorphic (about 20,000x) and splits server time into deserialization 4.75 ms, computation 2.15 ms and serialization 156.41 µs.
- **+** [38:27](https://youtu.be/ePQyy9sLmsY?t=2307) The scope is stated: serialization is included and bootstrapping is excluded, since it would take tens of seconds.
- **−** [38:58](https://youtu.be/ePQyy9sLmsY?t=2338) The talk gives no machine, iteration count or variance, and the "10 times worse five years ago" remark has no source.

**Depth 2/2**

- **+** [14:40](https://youtu.be/ePQyy9sLmsY?t=880) The noise-and-bucket model explains why multiplications exhaust the budget, how Q/T sizing trades alphabet size against operation count, and where leveled SHE fits.
- **+** [41:05](https://youtu.be/ePQyy9sLmsY?t=2465) Branching cost and the BFV/CKKS/TFHE comparison weigh each scheme against the workload it suits.
- **·** [10:29](https://youtu.be/ePQyy9sLmsY?t=629) The LWE math is scalar-simplified with real polynomials only named, which fits a beginner slot.

**Reusable 1/2**

- **+** [27:18](https://youtu.be/ePQyy9sLmsY?t=1638) The `encrypt_inputs` client code and the server's weighted-sum loop are shown and walked through, enough to rebuild the encrypt-compute-decrypt loop.
- **+** [39:28](https://youtu.be/ePQyy9sLmsY?t=2368) Oracle testing through the unmocked library with production parameters, heavy on boundaries, is described as the way to catch OpenFHE's silent wrong values on noise overflow.
- **−** [29:54](https://youtu.be/ePQyy9sLmsY?t=1794) The connection code is skipped ("I don't show all the rest of the application because it's trivial"), and no repository, gist or download link for the demo is given.
