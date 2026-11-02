> **Superseded.** The stability result is now written up in `paper/stability_note.pdf` (v1.0.0, DOI [10.5281/zenodo.23874488](https://doi.org/10.5281/zenodo.23874488)). This file is kept as the earlier record; where the two differ, the paper is authoritative.

We have two updates on Problem 848 (with the diagonal condition $a = b$ included, as in Sawhney's note): (1) an independent source rebuild and `leanchecker` kernel verification of A. C. Li's all-$N$ Lean 4 proof (plus explicit colouring certificates to $N = 10^7$), and (2) a referee-checked claim of the sharp $1/50$ structural stability threshold and its two extremal constructions.

### 1. Independent kernel verification of A. C. Li's all-$N$ Lean proof (and certificates to $N = 10^7$)

A. C. Li's preprint and Lean 4 repository (`crabsatellite/erdos-848-squarefree-product`, SSRN 7230480) give a complete proof of Problem 848 for **all $N \ge 1$**, combining an exact prefix colouring for $N \le 5 \cdot 10^6$ with a Hall-defect sieve and transformed-root spacing argument for $N \ge 5 \cdot 10^6$ across 30,638 project `.lean` files (`leanprover/lean4:v4.30.0-rc2`, 2.35 GB of source).

We performed an independent build from source and a `leanchecker` kernel replay, without running any of Li's scripts or using any of Li's build caches (Li's modules were compiled from source; Mathlib came from the official Mathlib build cache):

1. **Build stall diagnosis & 2-line binder fix:** Running a plain `lake build` stalls indefinitely on module `Erdos848.TailGlobalMixedWordCountSound`. We traced this to a build-configuration mismatch: `lakefile.toml` sets `autoImplicit = false` (which `lake build` passes via `--setup`, whereas Li's build driver invokes `lake env lean` where `autoImplicit` defaults to `true`), and lines 27 (`append_le_append`) and 262 (`globalMixedCpopNatRec_eq_sum`) use undeclared `BitVec` width variables `v` and `w`. Because the file sets `set_option maxHeartbeats 0`, the follow-on elaboration failure in `pack8_mono` never terminates. Adding `{v w : ℕ}` at line 27 and `{w : ℕ}` at line 262 produces identical elaborated types (`set_option pp.all true`) to auto-binding across all 30 declarations in the file and lets the module compile in 6.4 seconds.
2. **Manifest & source audit:** All other 30,735 entries in Li's `PUBLICATION_MANIFEST.json` match by SHA-256 bit-for-bit. A scan across all 30,638 `.lean` files confirmed zero occurrences of `sorry`, `admit`, `native_decide`, `ofReduceBool`, `implemented_by`, `extern`, `unsafe`, or `debug.skipKernelTC` outside comments.
3. **Full source compilation & axiom check:** With the 2-line binder fix, `lake build` completed all 39,069 build jobs with exit code 0, compiling from source the 30,636 project modules behind the final theorem. Compiling our own check file against the built library confirmed that `Erdos848.PaperGeneratedCertificateProvider.all_N` unifies directly with a transcription written purely with Mathlib's `Squarefree`:
   ```lean
   theorem erdos848_our_statement :
       ∀ N : ℕ, ∀ A : Finset ℕ, A ⊆ Finset.Icc 1 N →
         (∀ a ∈ A, ∀ b ∈ A, ¬ Squarefree (a * b + 1)) →
         A.card ≤ ((Finset.Icc 1 N).filter fun n => n % 25 = 7).card :=
     Erdos848.PaperGeneratedCertificateProvider.all_N
   ```
   and `#print axioms` reports only `[propext, Classical.choice, Quot.sound]`.
4. **Standalone external kernel replay (`leanchecker`):** We replayed every declaration of all 30,636 project modules behind the final theorem through the Lean kernel with `leanchecker` (Mathlib itself was not replayed): 0 failures, 0 problems.

Separately, using a standalone C generator and an independent verifier (Miller–Rabin + Pollard–Brent rho), we generated and verified explicit plateau colouring certificates partitioning $\{n \le N : n^2+1 \text{ not squarefree}\}$ into $|\{n \le N : n \equiv 7 \pmod{25}\}|$ pairwise-compatible classes (where $xy+1$ is squarefree within each class, so $\chi(G_N) = \omega(G_N) = c(N)$ in the non-squarefree-product graph $G_N$) for all 399,999 plateaus up to $N = 9,999,981$.

---

### 2. Sharp structural stability threshold ($1/50$) and extremal mixed sets

Sawhney proved that for $N$ large, any admissible $A \subseteq \{1, \ldots, N\}$ with $|A| \ge (1/25 - \eta)N$ (with $\eta \approx 0.0023$ from his four case bounds) is contained in either $\{n \equiv 7 \pmod{25}\}$ or $\{n \equiv 18 \pmod{25}\}$, and asked about a structural classification of sets $A$ at lower density $\delta N$.

We show that the sharp stability threshold is **$1/50$**:

> **Claim (checked by independent referee code).** For every $\varepsilon > 0$ and $N \ge N_0(\varepsilon)$, every admissible $A \subseteq \{1, \ldots, N\}$ that is not contained in $\{n \equiv 7 \pmod{25}\}$ and not contained in $\{n \equiv 18 \pmod{25}\}$ satisfies $|A| \le (1/50 + \varepsilon)N$.
>
> The constant $1/50$ is sharp and is attained by exactly two residue-class constructions:
> $$A_1 = \{n \le N : n \equiv 7 \text{ or } 93 \pmod{100}\} \quad \text{and} \quad A_2 = \{n \le N : n \equiv 43 \text{ or } 57 \pmod{100}\}.$$

*(Note on prior work: `AstroCat93/erdos-848-verification` previously noted that $7$ and $93 \pmod{100}$ can be compatible through $4$ and had a sub-case of limiting density $0.02$, without showing that density $1/50$ is attained or establishing $1/50$ as the overall stability bound, which was $\approx 0.0282$ there.)*

*Sharpness:* In $A_1$, $7 \equiv 7 \pmod{25}$ and $93 \equiv 18 \pmod{25}$, so $25 \mid ab+1$ for pairs within the same class ($7^2+1 = 50$, $93^2+1 = 8650$), while for cross pairs $ab + 1 \equiv 7 \cdot 93 + 1 = 652 \equiv 52 \equiv 0 \pmod 4$. The set $A_2 = \{43, 57 \pmod{100}\}$ is the mirror image ($43 \equiv 18$ and $57 \equiv 7 \pmod{25}$, $43^2+1 = 1850$, $57^2+1 = 3250$, and $43 \cdot 57 + 1 = 2452 \equiv 0 \pmod 4$). For $557 \le N \le 10000$, exact maximum-clique computations confirm that the largest admissible set not contained in a single mod-25 class has size equal to that of $A_1$ or $A_2$.

*Proof sketch:* Partition integers by their residue ("type") modulo $M = 900 = 4 \cdot 9 \cdot 25$. A pair of types $(s, t)$ is "glued" if $4 \mid st+1$, $9 \mid st+1$, or $25 \mid st+1$. Let $C$ be the 72 types with $s \equiv 7$ or $18 \pmod{25}$.
- If $s \in C$ is glued to every $t \in S$ (where $S \subseteq \mathbb{Z}/900\mathbb{Z}$ is the set of types present in $A$), its upper density in $A$ is at most $1$.
- If $s \in C$ is not glued to some $t \in S$, choosing a witness $b \in A$ of type $t$ forces $q^2 \mid ab+1$ for some prime $q \ge 7$, giving upper density at most $K_2' = 1 - \prod_{q \ge 7}(1 - q^{-2}) = 1 - 9.375/\pi^2 \approx 0.0501139$.
- If $s \notin C$ (and type $s$ has at least two elements in $A$), each element $a$ of type $s$ satisfies both $p^2 \mid a^2+1$ for some prime $p \equiv 1 \pmod 4$, $p \ge 13$ (event $D$) and $q^2 \mid ab+1$ for some prime $q \ge 7$ with a second element $b$ of type $s$ (event $P_b$). By monotonicity of the local CRT factors, the worst-case $b$ occurs when $\gcd(b, q) = 1$ for all $q$ and $p^2 \mid b^2+1$ at every prime $p \equiv 1 \pmod 4$, $p \ge 13$, yielding uniform upper density
  $$J' = K_1 - Q\left(\prod_{p \equiv 1 (4), p \ge 13}(1 - p^{-2}) - \prod_{p \equiv 1 (4), p \ge 13}(1 - 2p^{-2})\right) \approx 0.0142450,$$
  where $K_1 = 1 - \prod_{p \equiv 1 (4), p \ge 13}(1 - 2p^{-2}) \approx 0.0273465$ and $Q = \prod_{p \equiv 3 (4), p \ge 7}(1 - p^{-2}) \approx 0.963123$.

Maximizing $\frac{1}{900}\sum_{s \in S} f(s, S)$ over all $S \subseteq \mathbb{Z}/900\mathbb{Z}$ not contained in a single mod-25 class—verified via 0–1 MILP and exhaustive enumeration over the 64 Galois-closed signature sets mod 36—gives a maximum of $18/900 = 1/50$, attained uniquely by $\{7, 93 \pmod{100}\}$ and $\{43, 57 \pmod{100}\}$. The second-best configuration is all 900 types, which gives
$$\frac{72 K_2' + 828 J'}{900} \approx 0.017115 < \frac{1}{50}.$$
