# Referee report: "A sharp stability threshold for Erdős Problem 848"

Numbering below follows the compiled document. All environments share the section counter, so the items are: Def 1.1, Thm 1.2 (Li), Thm 1.3 (Sawhney), Thm 1.4 (main), Rem 1.5–1.7, Prop 2.1–2.2, Rem 2.3, Lemma 3.1, Lemmas 4.1–4.3, Prop 5.1, Rem 5.2, Lemma 6.1, Rem 6.2, **Thm 6.3**, Rem 6.4, Cor 7.1, §8 (small N), §9 (verification).

## 1. Proof of Theorem 1.4, step by step

**§2 (constructions).** All arithmetic checks out:
- 93²+1 = 8650 = 2·5²·173.
- 7·93+1 = 652 = 2²·163.
- 43²+1 = 1850 = 2·5²·37.
- 57²+1 = 3250 = 2·5³·13.
- 43·57+1 = 2452 ≡ 52 (mod 100).

Remark 2.3's mod-4 table is correct, and the only cross pairs with uv ≡ 3 (mod 4) are (7,93) and (57,43).

One minor rigor point in Prop 2.2. A computation modulo 900 can only show that a pair has *no local obstruction*. To conclude that the residue-class set is *not admissible*, you need an actual squarefree value of ab+1. The integer check up to 20000 presumably supplies these witnesses; the proof should say so.

**§3 (Lemma 3.1).** (F1)–(F3) are correct, and the proofs are complete. In particular, 25 | st+1 with s ≡ 7 (mod 25) forces t ≡ −7⁻¹ ≡ 7 (mod 25), since 7·18 ≡ 1. The computational verification is redundant but harmless.

**§4 (sieve bounds).**
- *Lemma 4.1.* Correct. The tail bound uses Σ_{n>T} n⁻² < 1/T. The witness for D occupies two classes mod q² and the witness for P_b one class, giving at most three classes per q. The CRT error is uniform in b. Stylistically, the justification sits after the lemma rather than in a proof environment.
- *Lemma 4.2.* Correct. Every truncated majorant 1 − ∏_{q≤T}(1−q⁻²) is already ≤ K₂′.
- *Lemma 4.3.* The inclusion–exclusion formula and the local data are correct. In the worst case:
  - ∏Y = A_𝒟,
  - ∏X = Q·B_𝒟 = 1 − K₂′,
  - ∏Z = Q·A_𝒟,

  which gives J′.

  I checked both one-prime changes:
  - ℓ | b changes the density by (Z′ − X′)/ℓ² ≤ 0, because Z′ ≤ X′ holds for every sub-product.
  - A coincidence raises Z_ℓ from 1 − 3/ℓ² to 1 − 2/ℓ², which increases the density.

  Because these signs do not depend on the other factors, and only finitely many primes ≤ T are involved, the stated argument *is* the monotonicity induction. Moving one prime at a time suffices.

  The source comment `% TODO(author): ... global monotonicity induction ... not present` is therefore overly cautious. One sentence ("iterate over the finitely many primes ≤ T") closes it. Delete the TODO either way.

**§5 (Prop 5.1).** Correct.
- In the C/non-glued case, t ≠ s follows from self-gluing, so b ∉ A_s.
- In the non-C case, every a ∈ A_s∖{b} satisfies D(a) ∧ P_b(a).
- Singletons are absorbed in O(M).

**§6 (Lemma 6.1).** The closure argument is correct.
- W₇ ⊆ R(G₁₈ ∪ Y) gives Y ⊆ B.
- Antitonicity gives R(A) ⊆ R(G₇) ⊆ R(W₇) = B.
- The new weight-1 set A ∩ R(B) contains W₇.
- Y = A∩B does not shrink the weight-1 sets, because A∩B ⊆ B.

**The counts in Lemma 6.1 and Remark 6.2, checked by hand.** Using the families of Remark 6.2, I recomputed the number of compatible pairs (A, B) by counting the closed supersets of R(A):

| A | number of such A | closed B ⊇ R(A) | pairs |
|---|---|---|---|
| ∅ | 1 | 1 | 1 |
| full set | 1 | 64 | 64 |
| family 3 | 12 | 2 | 24 |
| family 4 | 12 | 16 | 192 |
| family 5 | 30 | 4 | 120 |
| family 6 | 6 | 4 | 24 |
| family 7 | 2 | 8 | 16 |

The total is **441**, and removing the two single-class pairs gives **439**. Both match the paper.

**Values of F on the closed pairs.** Evaluating the pairs gives:
- maximum 18 (the family-7 pair and its mirror);
- next 72K₂′ + 828J′ = 15.40 (the pair (full, full));
- then 13.75 (full, family 7), 13.58 (full, singleton), 13 (family 3 with its dual), and so on.

So the computational Theorem 6.3 is confirmed independently of the solvers, restricted to closed configurations.

**§7.** The proof of Theorem 1.4 is correct. Corollary 7.1 is also correct as proved, because it passes through the closed replacement.

**Overall:** I find no gap in the argument for Theorem 1.4.

## 2. Constants

| Constant | Check | Result |
|---|---|---|
| K₂′ | (6/π²)/0.64 = 9.375/π² ≈ 0.9498861, so K₂′ = 0.05011390… | Inside the stated enclosure, at its lower edge |
| Q·B_𝒟 | 0.9631226 × 0.9862567 = 0.9498861 = 1 − K₂′ | Consistent |
| K₁ | 1 − 0.9726535 = 0.0273465 | Matches. A partial-sum sanity check of A_𝒟 agrees to about 3 digits |
| J′ | 0.0273465 − 0.9631226 × 0.0136032 = 0.0142450 | Matches |
| 72K₂′ | 3.60820 | Correct |
| 828J′ | 11.79484 | Correct |
| Runner-up | 15.40304/900 = 0.0171145 | Correct |
| 18/900 | 1/50 | Correct |
| Rem 6.4 threshold | (18 − 3.6082)/828 = 0.017381 | Correct |
| Rem 6.4 with K₁ | (3.6082 + 22.643)/900 ≈ 0.0292 | Correct |

The enclosure widths in Table 1 are consistent with the stated tail bounds.

## 3. The three clarifications

- **(a) Lemma 4.3 proof.** Present and correct. Coincidences ℓ² | b²+1 hold for only finitely many ℓ, so no single b realizes the worst case, but the bound holds for every b.
- **(b) After Theorem 6.3.** Present and correct. It is consistent with §8's observed value of about 0.0155N.
- **(c) Remark 5.2.** Present and correct. Without the diagonal condition, F(ℤ/900) = K₂′ ≈ 0.0501. That value exceeds not only 1/50 but even 1/25, so "gives nothing" in §1.1 is accurate.

## 4. Other issues

**Mathematical misstatements**

1. **Thm 6.3, runner-up statement: false as written.**
   - The theorem says "the second largest value of F is attained at S = ℤ/900ℤ" over Σ.
   - But S₁ minus one type lies in Σ and has F = 17/900 > 15.40/900.
   - The claim holds only among Galois-closed configurations. That is how Corollary 7.1 uses it (and its parenthetical already says "the enumeration").
   - The theorem statement needs that qualifier.
   - The final clause ("largest among configurations containing a non-C type") is true over all of Σ.

2. **Rem 1.6, explicit N₀.**
   - (i) exp(2033200) ≈ 10^{883007.6}, so the claim "N₀(1/100) ≤ 10^{883006}" is false. The correct bound is ≤ 10^{883008}.
   - (ii) The condition Q ≤ e^{2T log T} ≤ εN/(6M) requires log N ≳ (48/ε)·log(24/ε). Because of the log(24/ε) factor, log N ≥ 20332/ε does *not* imply it for all ε ≤ 1/100; it fails for (absurdly) tiny ε. Restrict the range of ε or include the log factor.
   - (iii) The symbol Q clashes with the Euler product Q of Lemma 4.3.

**Internal inconsistencies**

3. **Explicit N₀ versus "no explicit N₀ claimed".** The abstract ("No explicit N₀ is claimed") and Rem 1.5 ("No explicit N₀ … anywhere in this note") contradict Rem 1.6, which gives an explicit N₀. Rem 1.5 is also titled "Ineffectivity" while stating the argument is effective.

4. **Role of Li's theorem.** §1.2 calls Thm 1.2 "an *input* to the present note", and §9(C) says "The input Theorem 1.2 relies on…" and "the input we take from [Li]". This contradicts Rem 1.5, the abstract, and the §9 summary, which say Li is not used in the proof. Rephrase as "quoted for context".

5. **Source comments.**
   - The comment before §6.2 refers to "Theorem 6.2"; it is actually Theorem 6.3.
   - The same comment says "only one of [the solvers] uses the reduction", but solvers 1 and 3 both use the reduced model.
   - The §9(A) TODO about "64 = 2⁶ … 6-element Galois orbit structure" is stale and meaningless, since Remark 6.2 already lists the closed sets. Delete it.

**Editorial items**

6. **Footnote in Lemma 4.2** about a "spurious factor 15/16 in an early draft": remove from a final version.

7. **Unsupported claims.**
   - *Missing references.* bzanghi/erdos-848 and The-Obstacle-Is-The-Way/erdos-banger (Rem 1.7) have no bibliography entries.
   - *Unsupported content in Rem 1.7.* The "novelty search carried out on 27 October 2026" is not citable content.
   - *Verifiers in Prop 2.2 and §6.* An "independent referee" whose code is distributed with the paper is unusual; identify the verifiers in the acknowledgments instead.

8. **Overstatement in the abstract and Thm 1.4.** "Attained exactly by" the two constructions is proved only within the type framework. Cor 7.1 actually gives the stronger statement, that any mixed set of density above the runner-up is contained in A₁ or A₂. Cite Cor 7.1 at that point.

9. **Minor.**
   - *Notation clashes:* f(N) vs f(s,S); A, B, A_𝒟 vs the admissible set A.
   - *Table 1:* column spec `{llll}` for 3 columns.
   - *§9(C):* propext, Classical.choice and Quot.sound are Lean core axioms, not "Mathlib foundation".
   - *Abstract:* "exhaustive enumeration over the 64 Galois-closed signature sets" is really over the 439 compatible pairs.
   - *Rem 2.3:* "obstruct uv+1 for all such u, v" should read "for all integers in these classes".

## 5. Verdict

**ACCEPT WITH MINOR FIXES.** The proof of Theorem 1.4 is sound and self-contained, and the constants and finite enumeration check out (I re-derived the 441/439 counts and the top values of F by hand). Required fixes:

1. Restrict the runner-up claim of Thm 6.3 to Galois-closed configurations (item 1).
2. Correct Rem 1.6 (item 2): change 10^{883006} to 10^{883008}, fix the ε-range or log factor, and rename Q.
3. Reconcile the abstract and Rem 1.5 with Rem 1.6 (item 3).
4. Remove the "input" wording for Li in §1.2 and §9(C) (item 4).
5. Delete the stale TODOs and the early-draft footnote, and fix the comment's theorem number (items 5–6).
6. Add the missing bibliography entries and trim the novelty-search sentence (item 7).
7. Minor editorial fixes (items 8–9) and the witness sentence in Prop 2.2 (§1).