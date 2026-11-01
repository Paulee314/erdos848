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

Status: audited DRAFT for the author's review. Not compiled to PDF yet at
audit time (no TeX toolchain on the auditing machine); not submitted
anywhere.
