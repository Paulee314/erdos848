# MEMORANDUM

**Date:** November 1, 2026
**To:** File — Erdős Problem #848 project (`/Users/paullee/AI-workspace/Claude-Projects/Erdos/e848/`)
**From:** Muse (independent second-opinion audit)
**Subject:** Audit of Gemini's `UPDATE_2026-11-01.md` — what is verified, what is wrong, and what must be fixed before the forum post is used

---

## 1. Purpose

At Paul Lee's request, I independently checked the summary posted by Gemini as
`UPDATE_2026-11-01.md` (created Nov 1, 2026, 18:33 UTC) in the Erdős #848
project folder. That document claims (i) a sharp 1/50 structural stability
theorem, (ii) seating-chart certificates to $N = 10^7$, and (iii) a complete
independent verification of A. C. Li's all-$N$ Lean proof, and it contains a
draft forum post for erdosproblems.com/848 combining all three.

Attribution, stated up front: **the all-$N$ proof of Problem #848 is A. C.
Li's** (`crabsatellite/erdos-848-squarefree-product`, SSRN 7230480). The work
audited here is (a) the 1/50 stability theorem and its extremal constructions,
(b) the certificates to $N \le 9{,}999{,}981$, and (c) the independent source
rebuild, bugfix, and external kernel replay of Li's proof. None of the
findings below changes that attribution.

## 2. Summary verdict

The UPDATE is **substantially correct, but must not be posted as-is**. The
load-bearing numbers, the certificates, and the Li replay all check out
(Section 3). However, the document contains one definite mathematical error, two
material overstatements of method/novelty, and one missing caveat
(Section 4). The forum post draft in Part 3 of the UPDATE is in better shape
than Part 1 — it already uses the correct forms for the two main items — and
is postable once the corrections in Section 6 are applied.

The 1/50 theorem itself stands as **CLAIM v2 plus an independent referee
check**, not as a formalized or peer-reviewed proof. That status, not
"CONFIRMED" without qualification, is the accurate label.

## 3. Verified by independent recomputation or rerun by Muse

1. **Extremal constructions.** $\{7, 93\} \pmod{100}$ and $\{43, 57\} \pmod{100}$
   are admissible: pairs within one residue give $ab+1 \equiv 50 \pmod{100}$
   (divisible by 25); cross pairs give $7\cdot93+1 = 652$ and
   $43\cdot57+1 = 2452$, both $\equiv 52 \pmod{100}$ (divisible by 4). An
   exhaustive check of all mod-100 cross-class pairs (7/18 mod 25 classes)
   confirms these are the only two pairs glued by 4 or 25.
2. **Density constants** (recomputed from the prime-product definitions, with
   tail bounds):
   $K_1 \approx 0.0273465$, in $[0.02734649, 0.02734654]$;
   $K_2' = 1 - 9.375/\pi^2 \approx 0.0501139$;
   $J' \approx 0.0142450$, in $[0.01424497, 0.01424500]$;
   $Q \approx 0.963123$.
   Runner-up configuration: $(72K_2' + 828J')/900 \approx 0.0171145 < 1/50$,
   with $72K_2' + 828J' = 15.40306 < 18$.
3. **Mod-900 optimization.** Reran the referee's Galois-closed enumeration
   (`review/agent/opt_closure.py`) on Muse's VM: 64 closed sets, maximum
   $18/900 = 1/50$, exactly two maximizers — realized as $\{7, 93\}$ and
   $\{43, 57\}$ mod 100 — second best $15.40306/900$, attained by all
   900 types. (This is verification of the enumeration *given* the
   Galois-closed reduction; see item 2 of Section 4.)
4. **Certificates to $N \le 9{,}999{,}981$.** Downloaded `cert/certs_1e7.tgz`
   from the Mac; MD5s of `out1e7/global.txt` and `out1e7/deltas.txt`
   (`e5b8573a` / `e3330948`) match `cert/RESULTS.md`. Recompiled the
   independently written checker (`cert/checker/check848.c`, Miller–Rabin +
   Pollard–Brent) and reran it on Muse's VM: **PASS** — 399,999 plateaus,
   1,051,580 candidates, 857,402 re-homing moves, 0 failures. The checker's
   48 s on the VM vs 27.8 s reported on the Mac is machine speed only.
5. **Li replay — build fix.** The patch is exactly the two binder declarations
   claimed (`diag/review_packet/patch.diff`): $\{v\ w : \mathbb{N}\}$ added at
   line 27 (`append_le_append`) and $\{w : \mathbb{N}\}$ at line 262
   (`globalMixedCpopNatRec_eq_sum`) of `TailGlobalMixedWordCountSound.lean`.
   Per `diag/review_packet/report.json`, the patched module compiles in
   6.4 s and all 30 declarations elaborate to types identical to the
   auto-bound original.
6. **Li replay — manifest and escape hatches.** Per
   `diag/integrity/report.json`: 30,735 of 30,736 manifest entries match
   `PUBLICATION_MANIFEST.json` by SHA-256, the sole differing file being the
   patched file in item 5; the `sorry` / `native_decide` / `admit` hits in the
   scan occur only in comments and ordinary English, with zero occurrences of
   `skipKernelTC`, `implemented_by`, `extern`, or `unsafe`.
7. **Li replay — full build and statement check.** `li_replay_work/full.log`
   ends Oct 30, 2026 (03:06:36 UTC) with "Build completed successfully
   (39,069 jobs)" and `full_exit=0`. `final/final_check.log` shows
   `Erdos848.PaperGeneratedCertificateProvider.all_N` proves a transcription
   of Problem #848 written purely with Mathlib `Squarefree` (diagonal
   $a = b$ included, extremal set $n \equiv 7 \pmod{25}$), depending only on
   axioms `[propext, Classical.choice, Quot.sound]`.
8. **Li replay — standalone kernel check.**
   `leanchecker/lc_groups/finished` records completion on Nov 1, 2026 at
   17:32:06 UTC: 30,636 modules in the import closure, 0 failures,
   0 problems. This matches the UPDATE.
9. **Novelty against Li's paper, specifically.** I grepped Li's
   1,182-line TeX manuscript myself: it contains no $\{7, 93\}$ or
   $\{43, 57\}$ construction, no $1/50$ or $0.02$ stability threshold, and no
   cross-class maximum-density determination. On that comparison, the
   UPDATE's novelty claim is correct.

## 4. Errors and overstatements found

1. **A definite mathematical error (Part 1, §A.2).** The UPDATE writes
   $$K_2' = 1 - \tfrac{15}{16}\cdot\tfrac{8}{9}\cdot\tfrac{24}{25}\cdot\tfrac{6}{\pi^2} \approx 0.050113903.$$
   That expression evaluates to $0.5137$, not $0.0501$; the factor
   $15/16$ is spurious. The correct forms are
   $K_2' = 1 - 9.375/\pi^2$ and
   $K_2' = 1 - (6/\pi^2)\big/\big(\tfrac34\cdot\tfrac89\cdot\tfrac{24}{25}\big)$.
   The quoted numerical value is right; the expansion is wrong. The forum
   draft in Part 3 uses the correct form and is unaffected.
2. **Method overstatement (Part 1, §A.3).** "Across all $2^{900}$ subsets
   $S \subseteq \mathbb{Z}/900\mathbb{Z}$ … the maximum … is $18/900$"
   describes a brute-force search that did not and could not take place.
   The maximum was obtained by (i) the author's CBC 0–1 program
   (`typebound.py`), (ii) exhaustive enumeration over the 64 Galois-closed
   signature sets, relying on the referee's argument that the objective is
   maximized on such a set, and (iii) a HiGHS MILP with cuts. The forum
   draft's wording ("verified via MILP and exhaustive enumeration over
   the 64 Galois-closed signature sets mod 36") is the accurate one.
3. **Novelty overstatement (Part 2).** "Yes — unequivocally" and "do not
   appear in … any community repository" overstate the October 27, 2026
   novelty search on file (`review/novelty_2026-10-27.md`), which itself
   lists sources not read in full (arXiv 2511.16072 §IV.1, the raw forum
   text, Sothanaphan's notes, the Zenodo archive). In particular,
   AstroCat93's `erdos-848-verification` had already noted that 7 and 93
   mod 100 are compatible "through 4" and had a subcase of limiting
   density 0.02 — without showing attainment or the sharp bound. The
   contribution is the attainment, the sharp bound, and the classification;
   it is not the first observation of 7·93 compatibility. The forum draft
   should say so.
4. **Missing caveat (Part 2, item 3).** The Fable sieve work
   (`fable/NOTES.md`) is a *conditional reduction* — Designs A/B′ reduce
   certificate existence for all large $N$ to uniform per-element sieve
   inequalities — with no explicit $N_1$ proved (heuristic estimate
   $10^9$–$10^{11}$ with elementary tools) and, in its own words, a route
   that "cannot close the problem by itself." The UPDATE presents it
   alongside proved results without that qualification.
5. **Minor / cosmetic.** (a) Part 1, §B: as worded, the partition is into
   cliques of the *compatibility* graph, so the invariant directly verified
   is the clique-cover statement and its consequence $|A| \le c(N)$ for
   every $N \le 9{,}999{,}981$; the $\chi(G_N) = \omega(G_N)$ formulation
   is correct only with $G_N$ taken as the non-squarefree-product graph.
   (b) Part 1, §A.1 omits the diagonal checks for $A_2$ ($43^2+1 = 1850$ and
   $57^2+1 = 3250$, both divisible by 25); they hold. (c) "compiled all
   30,638 modules" in the forum draft refers to the project's `.lean`
   files; the build log's own total is 39,069 jobs including dependencies.

## 5. Checked against sources but not independently re-derived

- The worst-case-$b$ argument behind the $J'$ bound (monotonicity of the
  local CRT factors; coincidence at $\ell^2 \mid b^2+1$ as worst case). The
  referee reports exact CRT-period product-formula checks and empirical
  densities to $10^7$; I verified the resulting formula and constants, not
  the argument from scratch.
- Sawhney's underlying lemmas (not re-derived; his case bounds
  0.0377 / 0.0358 / 0.0336 / 0.0294, hence $\eta \approx 0.0023$, were taken
  from CLAIM v2 as referee-corrected).
- The exact maximum-clique computations for $557 \le N \le 10{,}000$
  underlying the forum draft's sharpness paragraph (referee-reported in
  `review/referee_2026-10-27.md`).
- The build-stall figure "28,122 of 30,638 modules" and the superlative
  "first" independent rebuild of Li's repository. No contradicting
  evidence was found; neither is established by the artifacts alone.

## 6. Required corrections before the forum post is used

**Blocking**

1. Delete or correct the $15/16$ expansion of $K_2'$ in Part 1 (item 4.1).
2. Replace the "$2^{900}$ subsets" sentence with the MILP + Galois-closed
   enumeration description (item 4.2).
3. Add one sentence to the forum draft distinguishing AstroCat93's prior
   observation of 7·93 compatibility through 4 (item 4.3), and drop
   "unequivocally" from the novelty assessment.

**Non-blocking**

4. Qualify the Fable sieve contribution as a conditional reduction with
   no explicit $N_1$ (item 4.4), and fix the graph wording in Part 1, §B
   (item 4.5).
5. Label the 1/50 theorem throughout as "CLAIM v2, referee-checked" rather
   than formally proved.

## 7. Recommendation

With the Section 6 corrections, the document is a fair record: the
certificates and the Li kernel verification may be reported as *verified*
(the certificates were independently rerun in this audit), and the 1/50
stability theorem may be posted as a referee-checked claim with the
AstroCat93 distinction noted. No correction is needed to the headline
results themselves — every load-bearing number I recomputed agreed with
the UPDATE.

---

*Audit artifacts produced by Muse during this check: this memo, copied into
the e848 folder at Paul Lee's request on Nov 1, 2026; no other files were
added to the Mac. The certificate checker was rerun on Muse's VM against
the Mac's `certs_1e7.tgz` (MD5s in item 3.4); the optimization enumeration
was rerun from `review/agent/opt_closure.py` with the referee's
`consts_ref.json`.*
