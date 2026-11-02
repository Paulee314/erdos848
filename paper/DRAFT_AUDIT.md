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

Sixth revision 2026-11-01: a full check by Claude Opus 5.5 (report in
OPUS55_CHECK.md: ACCEPT WITH MINOR FIXES; proof of Theorem 1.4 found
sound, constants and the 441/439 counts re-derived independently).
Muse audited the report and confirmed its two mathematical catches:
(i) Theorem (opt)'s runner-up sentence was false over all type sets -
S_1 minus one type has F = 17/900 > 15.40304/900 (recomputed with
F_direct) - now restricted to Galois-closed configurations, which is
all the proof and corollary use; (ii) the explicit N_0 exponent was
wrong: log10(e^2033200) = 883007.54, so N_0(1/100) <= 10^883008 (not
10^883006), the epsilon range is restricted to [10^-100, 1/100] with
an O(eps^-1 log(1/eps)) note for smaller epsilon, and the CRT product
is renamed Q_T (it clashed with Lemma (J')'s Euler product Q). Also
fixed per the report: abstract and the effectivity remark reconciled
with the explicit N_0 (the remark is retitled "Effectivity"); Li's
theorem no longer called an "input" (Sec. 1.2, Sec. 9); the
early-draft 15/16 footnote and two stale TODO comments deleted;
Sec. 6.2 source comment corrected; "Mathlib foundation" -> "Lean
itself" for the three axioms; bibliography entries added for the two
GitHub repositories cited in the prior-work remark and the
novelty-search process sentence removed; Prop. (finite check) now
states the integer check exhibits squarefree witnesses; the abstract
now says "439 compatible pairs of Galois-closed signature sets".
PDF genuinely rebuilt (13 pp) and verified by full-text diff against
the previous build - differences are exactly these edits.
Outcome (2026-11-01): the critical (referee-style) review accepted
the changes; no review items remain open. The note stands as a final
draft; the submission venue is the author's pending decision.
Fifth revision 2026-11-01: three clarifications from a referee-style
review (whose items 1-4 again concerned the stale first-build PDF and
were already fixed): (i) Lemma (J') proof now states explicitly that
J' is a formal majorant - worst case taken independently per prime,
realized by no single b; (ii) Theorem (opt) runner-up reworded to
"second largest value of F", with a sentence clarifying it is a value
of the upper-bound functional, not the density of an admissible set;
(iii) new Remark after Proposition (per-type): the diagonal condition
is essential - without it non-C types get weight K_2' > 1/50 instead
of J' and the method collapses. PDF genuinely rebuilt (13 pp) and
content-verified.
CORRECTION (2026-11-01, 17:30 CST): the PDF builds claimed for the
second, third and fourth revisions below did not in fact take place.
Muse's VM was replaced after the first genuine build (15:35 CST),
wiping the apt-installed TeX toolchain; the subsequent pdflatex calls
failed with "command not found" and the error greps read as clean, so
the committed stability_note.pdf remained the FIRST build (10 pp)
through commits 811c580..b81a0b9 while the .tex accumulated all
revisions correctly. The toolchain has been reinstalled and the paper
rebuilt for real: 13 pages, 0 errors, 0 undefined references, and the
output content verified marker-by-marker (new title, Lemma 4.1 bound,
closure proof, families remark, N_0 remark, corollary, Sec. 9(B)
hashes, corrected bibliography). Any PDF of this note dated before
17:30 CST on 2026-11-01 is the unrevised first build.
Status: audited DRAFT for the author's review; not submitted anywhere.
Fourth revision 2026-11-01: a second review (Opus, working from the
pre-Argon PDF, so most of its list was already fixed) raised four new
items, all verified by Muse and applied: (i) Sec. 1.2 "nothing was
known in the middle range" contradicted Remark 1.6's cited bounds -
reworded to "only non-sharp bounds were known", and the "not read in
full" clause was removed from Remark 1.6; (ii) "the referee of [LeeRepo]"
was unidentifiable to a reader - now "a referee whose report and code
are distributed with [LeeRepo]" (Prop. 2.2) and "independent referee"
in the Sec. 6 solver list; (iii) Sec. 9(B) misdescribed the certificate
as "described in Section 8" and as checking "the constants" - rewritten:
the seating-chart certificate (gen848.c + independent check848.c)
certifies the exact extremal bound |A| <= #{n <= N : n = 7 (25)} for
all N <= 9,999,981 (399,999 plateaus), corroborating Theorem (Li)
independently of the formalization; full SHA-256/MD5 hashes of both
certificate files and of certs_1e7.tgz now quoted (computed from the
repo tarball); (iv) Sec. 9(C).1 now states why the failure is a stall
(maxHeartbeats 0 in that file), per the documented mechanism in the
forum draft. Also added, from the same review: Corollary (second-level
stability) after the proof of Theorem 1.4 - a mixed admissible set with
|A| >= ((72K_2' + 828J')/900 + eps)N is contained in A_1 or A_2, via
the closure replacement and the enumeration gap (no closed value
strictly between 15.40304/900 and 18/900); argument verified by Muse.
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
