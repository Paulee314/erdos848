# Erdős Problem 848: a sharp stability threshold (claim, v2 after review)

v2 (Oct 27 2026, evening): revised after an independent referee check (no mathematical errors found;
presentation fixes applied below), an Argon review, and a novelty search. See review/.

## Problem
Erdős #848 (Erdős–Sárközy). Call A ⊆ {1,…,N} *admissible* if ab+1 is not squarefree for all a, b ∈ A,
**including a = b** (as in Sawhney's proof; the argument below uses the diagonal condition and gives nothing
without it). Is max |A| attained by {n ≤ N : n ≡ 7 (mod 25)}?
Sawhney (2025, with GPT-5 assistance) proved: there is η > 0 such that for N large, every admissible A with
|A| ≥ (1/25 − η)N lies inside {n ≡ 7 (mod 25)} or inside {n ≡ 18 (mod 25)}. His case bounds are
0.0377N, 0.0358N, 0.0336N, 0.0294N (+o(N)), so η ≈ 0.0023 is implicit. He leaves open "a strong structural
classification of sets A with size δN".

## Claim
For every ε > 0 there is N₀(ε) such that every admissible A ⊆ [N], N ≥ N₀, that is NOT contained in a single
class {7 mod 25} or {18 mod 25} satisfies |A| ≤ (1/50 + ε)N.
Equivalently: admissible sets with more than (1/50 + ε)N elements lie in one of the two classes.
The constant 1/50 is sharp. Exactly two residue-class constructions attain it:
A = {n ≤ N : n ≡ 7 or 93 (mod 100)} and A = {n ≤ N : n ≡ 43 or 57 (mod 100)}.

## Sharpness examples
- n ≡ 7 (mod 100): for a ≡ b ≡ 7 (mod 100), ab+1 ≡ 50 (mod 100), divisible by 25.
- n ≡ 93 (mod 100): 93·93+1 = 8650 = 2·5²·173.
- Cross pairs: 7·93+1 = 652 = 2²·163, and in general ab+1 ≡ 52 (mod 100), divisible by 4.
- 7 ≡ 7 and 93 ≡ 18 (mod 25), so the set meets both classes.
- {43, 57 (mod 100)} is the mirror image: 43 ≡ 18 and 57 ≡ 7 (mod 25), glued by 4.
- Among the residues mod 100 lying in the two classes, these are the only cross-class pairs that give admissible sets.

## Argument
Fix M = 900 = 4·9·25. The *type* of n is n mod M.

Local facts (verified by direct computation):
- (F1) n²+1 is never divisible by 4 or 9; it is divisible by 25 iff n ≡ 7 or 18 (mod 25); primes p ≡ 3 (mod 4)
  never divide n²+1; for p ≡ 1 (mod 4), x² ≡ −1 has exactly two roots mod p². Hence for n mod 25 ∉ {7,18},
  n²+1 is not squarefree ⇔ p² | n²+1 for some prime p ≡ 1 (mod 4), p ≥ 13 (event D).
- (F2) Whether 4, 9 or 25 divides ab+1 depends only on the types of a and b. A pair of types (s, t) is *glued* if
  4 | st+1 or 9 | st+1 or 25 | st+1. If (s, t) is not glued, then for a of type s and b of type t,
  ab+1 is not squarefree ⇔ q² | ab+1 for some prime q ≥ 7, and necessarily q ∤ b (event P_b).
- (F3) Let C = types with s ≡ 7 or 18 (mod 25) (72 types). Each type in C is glued to itself and to every type
  in the same class mod 25. A type outside C is never glued to itself. A type in C and a type outside C can only
  be glued through 4 or 9.

Density bounds. All of these hold uniformly in the representative b ≤ N, in the following ε–T form.
- Truncate at T. For primes ≤ T the count is an exact CRT count, with error O_T(1).
- Only primes q ≤ N matter, since q² ≤ ab+1 ≤ N²+1. Primes T < q ≤ N add at most Σ (N/q² + 1) ≤ N/T + π(N)
  for P_b, and at most twice that for D.
- Choose T = T(ε), then N₀. The constants below are limits of the truncated products, and only upper bounds are
  used.

The two density bounds:
- For s ∈ C and any b: #{a ≤ N : a ≡ s (M), P_b(a)} ≤ (K₂′ + ε) N/M, where
  K₂′ = 1 − ∏_{q ≥ 7}(1 − q⁻²) = 1 − 9.375/π² ≈ 0.0501139.
- For s ∉ C and any b: #{a ≤ N : a ≡ s (M), D(a) ∧ P_b(a)} ≤ (J′ + ε) N/M, where
  J′ = K₁ − Q·(∏_{p∈𝒟}(1 − p⁻²) − ∏_{p∈𝒟}(1 − 2p⁻²)) ≈ 0.0142450.
  Here 𝒟 = {p ≡ 1 (mod 4), p ≥ 13}, K₁ = 1 − ∏_{p∈𝒟}(1 − 2p⁻²) ≈ 0.0273465 and
  Q = ∏_{p ≡ 3 (mod 4), p ≥ 7}(1 − p⁻²) ≈ 0.963123.

Derivation of J′.
- Write dens(D ∧ P_b) = 1 − ∏Y − ∏X + ∏Z. X, Y and Z are the local densities at each prime of ¬P, ¬D and
  ¬D ∧ ¬P respectively, and Z ≤ X at every prime.
- At a prime ℓ, D_ℓ = {±r} with r² ≡ −1 (mod ℓ²), and P_ℓ = {−b⁻¹ mod ℓ²} when ℓ ∤ b.
- If ℓ | b, then P_ℓ is empty. The change in the density is (Z′ − X′)/ℓ² ≤ 0 when P_ℓ lies outside D_ℓ, and
  −X′/ℓ² ≤ 0 when it lies inside. So b coprime to ℓ is the worse case.
- If P_ℓ ⊂ D_ℓ (equivalently ℓ² | b²+1), then Z_ℓ rises from 1 − 3/ℓ² to 1 − 2/ℓ², which raises the density.
  So coincidence is the worse case.
- Taking the worst case at every prime simultaneously therefore gives an upper bound valid for all b.
- The referee checked the product formula exactly over full CRT periods on several small prime sets, and checked
  densities empirically for a ≤ 10⁷ with b having 0–3 coincidences. The largest observed density was 0.01120,
  below J′.

Per-type bound. Let S be the set of types present in A. For s ∈ S define f(s, S) as follows:
- f(s, S) = 1 if s ∈ C and s is glued to every t ∈ S.
- f(s, S) = K₂′ if s ∈ C and some t ∈ S is not glued to s. Use any b ∈ A of type t; a C type is glued to itself,
  so t ≠ s.
- f(s, S) = J′ if s ∉ C and type s has at least 2 elements, since a second element of type s is a non-glued
  partner. If type s has a single element, it contributes 1, which goes into the O(M) term.

Then |A| ≤ (1/M) Σ_{s∈S} f(s, S) · N + εN + O(M).

Optimization. Maximize F(S) = (1/M) Σ_{s∈S} f(s, S) over all S ⊆ ℤ/M not contained in the 7-class and not
contained in the 18-class.
- Non-C types interact with C types only through (t mod 4, t mod 9), and all have weight J′.
- The maximum is 18/900 = 1/50. It is attained exactly by S = {types ≡ 7 or 93 (mod 100)} and
  S = {types ≡ 43 or 57 (mod 100)}.
- The second-best configuration is all 900 types, with value (72K₂′ + 828J′)/900 ≈ 0.017115. It is also the best
  configuration that contains any type outside C.
- So the whole result reduces to the single inequality 72K₂′ + 828J′ < 18. This holds with room to spare: it would
  still hold for any J′ < 0.01738 at the actual K₂′. Using K₁ in place of J′ is not enough (it gives 0.0292).
- The optimum was computed three ways:
  - a CBC 0-1 program (author, typebound.py);
  - an exhaustive enumeration over the 64 Galois-closed sets, which the referee showed the objective is maximized
    on;
  - a HiGHS MILP with cuts listing all optima (referee).

Hence every admissible A that is not inside one class satisfies |A| ≤ (1/50 + ε)N for N ≥ N₀(ε).

## Numerical evidence (consistent with, but weak for, an asymptotic statement)
Exact maximum-clique computations by the referee:
- For every N ≤ 10000, the overall maximum equals |{n ≤ N : n ≡ 7 (mod 25)}|.
- For every N from 557 to 10000, the largest admissible set not inside one class is exactly the 7/93 (or 43/57)
  mod 100 set. For some N ≤ 556 it is one element larger.
- The best set containing an element outside C has about 0.0155N elements for N = 4000–10000, below the asymptotic
  0.0171.

## Not claimed
No explicit N₀. The large-prime error terms are exactly as in Sawhney's argument. The result enlarges the margin
from ≈ 0.0023N to 1/50 = 0.02N, and identifies the sharp threshold and its extremal constructions.

## Prior work (novelty search, Oct 27 2026)
Neither the 1/50 threshold nor the {7, 93} or {43, 57} (mod 100) constructions were found stated.

The closest prior work:
- AstroCat93/erdos-848-verification (Oct 2026). It remarks that 7 and 93 mod 100 can be compatible "through 4",
  and one of its sub-cases has limiting density 0.02. It does not show that this density is attained, and its
  overall bound is about 0.0282.
- bzanghi/erdos-848: overall bound about 0.0276.
- erdos-banger Lean formalization: η = 1/2000.

One repository (hjyuh/erdos, marked as an incorrect proof on the community wiki) claims the two classes can never be
combined; the examples above refute that. Section IV.1 of arXiv 2511.16072 could not be read in full.

## Files
- dens.py, typebound.py, rival.py, small.py (author).
- review/agent/ (referee's independent code and report).
- review/2026-10-27_argon.md.
- review/novelty_2026-10-27.md.
