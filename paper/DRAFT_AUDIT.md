# Audit of the API-drafted stability note (2026-11-01)

`stability_note.tex` was drafted by Claude (claude-opus-5) via the Anthropic
API from the source pack in this repository (CLAIM.md, stability/ code and
constants, referee and novelty reports, UPDATE_2026-11-01.md, and
AUDIT_MEMO_2026-11-01.md), then audited by Muse against those sources.

## Verified against sources
- Theorem statement matches Claim v2, incl. sharpness and exactly two
  extremal constructions; N_0 stated ineffective everywhere; no explicit
  N_0 claimed anywhere.
- Constants table matches consts_ref.json enclosures: K1 = 0.0273465
  [0.02734649, 0.02734654]; K2' = 1 − 9.375/π² ≈ 0.0501139
  [0.05011390, 0.05011395]; J' ≈ 0.0142450 [0.01424497, 0.01424500];
  Q = 0.9631226050.
- Binding inequality 72K2' + 828J' = 15.40306 < 18; runner-up 0.0171145;
  derived side-values recomputed: J' < 0.01738 threshold and
  (72K2' + 828K1)/900 ≈ 0.0292 both correct.
- Gluing arithmetic: 652 = 4·163, 2452, 1850, 3250 all correct.
- Maximization described as MILP + exhaustive enumeration over the 64
  Galois-closed sets (439 compatible pairs); no 2^900 brute-force claim.
- Attribution correct: Li's theorem as input; Sawhney η ≈ 0.0023 with his
  four case bounds; AstroCat93 credited with the 7·93 observation and the
  ≈0.0282 bound, attainment/bound explicitly new here.

## Errors found in the API draft and fixed before commit
1. The draft was truncated at the API token limit mid-sentence in the
   final section; the ending (verification section items B–D, references)
   was generated in a second call and joined.
2. Removed a fabricated claim that AstroCat93's verification scripts "were
   run against our certificate and agree on the common range" — not in any
   source.
3. Third solver corrected to "HiGHS MILP solve" (draft said "brute-force
   search over all admissible sets", which misdescribes the method).
4. Patch description corrected: the two declarations were missing implicit
   binders under autoImplicit = false; the patch adds {v w : ℕ} and
   {w : ℕ} with elaborated types identical (draft's "explicit-to-implicit
   adjustment" was garbled).
5. Fixed two broken cross-references in the generated ending
   (sec:cert → sec:small; sec:li → thm:li).
6. Li reference title taken from his GitHub profile's listing of the work;
   verify against the SSRN page before any submission.

## Known gaps (marked in the .tex as % TODO(author))
1. No effective N_0 (inherited from the sources; Sawhney's argument is
   used, not re-derived).
2. The worst-case-b step behind J' rests on the finite CRT-period checks
   reported by the referee, not a written monotonicity proof.
3. The closure reduction (maximization attained on Galois-closed sets) is
   stated by the referee and implemented in opt_closure.py; a written-out
   proof is not in the sources and should be supplied in a final version.
   (The computational conclusion is cross-checked by three solvers, only
   one of which uses the reduction.)
4. Sawhney's reference lacks full bibliographic data in the sources.

Status: audited DRAFT for the author's review; not submitted anywhere.
Third revision 2026-11-01: (i) explicit N_0 example added (new Remark
after Remark 1.5): tracking the Section 4 choices with crude bounds gives
N_0(eps) = exp(20332/eps) for eps <= 1/100, in particular
N_0(1/100) <= 10^883006; arithmetic verified numerically (Rosser
pi(x) < 1.25506 x/log x; CRT error <= prod q^2 <= e^{2T log T}, dominated).
This closes the effective-N_0 TODO. (ii) Sawhney bibliography completed
from the primary source, located and read 2026-11-01: Mehtaab Sawhney,
"On A subseteq [N] such that ab+1 is never squarefree for a,b in A",
unpublished note, October 2025, math.columbia.edu/~msawhney/Problem_848.pdf
(the note linked from erdosproblems.com/848; its Proposition 1.1, remark
and four case bounds 0.0377/0.0358/0.0336/0.0294 match the paper's quotes
exactly). The placeholder title "Stability for Erdos Problem 848" in the
draft was not a real title and has been replaced. Caution: the
arXiv number 2511.16072 seen in a GitHub issue is the GPT-5 science
paper (Sawhney is a co-author), NOT this note - do not cite it as such.
Second revision 2026-11-01: at the author's direction, the remaining
Argon items were put to Claude via the Anthropic API (responses saved as
ARGON_ITEMS_CLAUDE.md; Opus for A-D3, Sonnet for D4-D5 after Opus refused
the follow-up prompt) and all were applied: (A) independence framing -
abstract edits, Remark 1.5 rewritten (no ineffectivity inherited; Li
quoted only for the exact f(N)), subsection retitled Inputs -> Context,
Section 9 logical-status paragraph rewritten (Theorem 1.4 implies
Sawhney for every eta < 1/50); (B) remark listing the 7 explicit families
of the 64 Galois-closed sets; (C) title changed to "admissible sets not
contained in a single extremal class"; (D1) the 7*18+1=127 clause moved
out of the divisibility claim; (D2) hand proof of the cross-class check
added as a remark after Proposition 2.2; (D3) runner-up display
recomputed from unrounded J' (11.79484, 15.40304) with a rounding note;
(D4) Lemma 6.1 now states 441 compatible pairs, 439 after excluding the
two single-class pairs; (D5) "a two declarations" grammar fixed. Claude's
draft for (A) cited two labels that do not exist in the file (lem:tail,
sec:gluing); these were corrected to lem:trunc and sec:types on insertion.
Revision 2026-11-01 (post-review): an independent review (Argon) found,
and Muse verified, a genuine gap in Lemma 4.1 as drafted — the tail bound
needs coefficient 3 (a large prime can witness D in two classes or P_b in
one) and class-relative scaling N/(Mq^2); the lemma and its error-budget
paragraph are patched accordingly (conclusions unchanged). The same review
supplied a proof of the closure reduction (Lemma 6.1), verified by Muse
against the section's definitions and now included in the paper; that
TODO gap is closed. Remaining TODOs in the source: effective N_0 and
Sawhney's full bibliographic data.
Compiled 2026-11-01 with pdflatex after removing a stray markdown fence
at the head of the generated file and reconciling citation keys between
the two generation calls (Li2026 → Li; EP848 → ErdosProblem848; EP848Code
→ LeeRepo, the repository that distributes the referee materials):
clean build, 10 pages, no errors or undefined references.
`stability_note.pdf` is committed alongside the source.
