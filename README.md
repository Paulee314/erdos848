# Erdős Problem #848 — stability claim, certificates, and independent verification of Li's proof

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23874488.svg)](https://doi.org/10.5281/zenodo.23874488)

**Cite:** Paul J. Lee, *A sharp stability threshold for Erdős Problem 848: admissible sets not contained in a single extremal class have density at most 1/50*, Zenodo, 2026. https://doi.org/10.5281/zenodo.23874488

**Attribution first.** The all-$N$ proof of Erdős Problem #848 is due to
**A. C. Li** ([crabsatellite/erdos-848-squarefree-product](https://github.com/crabsatellite/erdos-848-squarefree-product),
SSRN 7230480). This repository does **not** contain a new proof of #848.
It contains, by Paul Lee (Paulee314):

1. **A sharp stability claim (referee-checked, not formally proved).**
   Every admissible $A \subseteq \{1,\dots,N\}$ (i.e. $ab+1$ non-squarefree
   for all $a,b \in A$, including $a=b$) that is not contained in a single
   class $\{n \equiv 7 \pmod{25}\}$ or $\{n \equiv 18 \pmod{25}\}$ satisfies
   $|A| \le (1/50 + \varepsilon)N$ for $N \ge N_0(\varepsilon)$. The constant
   $1/50$ is sharp, attained exactly by
   $\{n \equiv 7 \text{ or } 93 \pmod{100}\}$ and
   $\{n \equiv 43 \text{ or } 57 \pmod{100}\}$.
   See `CLAIM.md` (v2) and `stability/`.
   Prior observation: AstroCat93's `erdos-848-verification` had already
   noted that 7 and 93 mod 100 are compatible "through 4" with a 0.02
   sub-case, without showing attainment or the sharp bound
   (see `stability/novelty_2026-10-27.md`).

2. **Explicit seating-chart certificates to $N \le 9{,}999{,}981$.**
   A C generator and an independently written checker (Miller–Rabin +
   Pollard–Brent) exhibiting, for all 399,999 plateaus, a partition of the
   candidate set $\{n \le N : n^2+1 \text{ not squarefree}\}$ into
   $c(N) = |\{n \le N : n \equiv 7 \pmod{25}\}|$ pairwise-compatible
   classes — hence $|A| \le c(N)$ for every $N \le 9{,}999{,}981$.
   See `cert/RESULTS.md` and `cert/FORMAT.md`.

3. **An independent source rebuild and kernel replay of Li's proof.**
   From Li's repository at commit `011a0d9` (toolchain
   `leanprover/lean4:v4.30.0-rc2`):
   - a plain `lake build` stalls on `TailGlobalMixedWordCountSound.lean`
     because `lakefile.toml` sets `autoImplicit = false` while two
     declarations omit binders; the 2-line fix is in `li-replay/patch.diff`
     and was reported upstream as
     [Issue #1](https://github.com/crabsatellite/erdos-848-squarefree-product/issues/1)
     (filed 2026-10-29, before the full replay below completed);
   - with that fix, `lake build Erdos848.PaperGeneratedCertificateProvider`
     completed: 39,069 jobs, exit 0 (`li-replay/full_build.log.gz`). All
     30,636 `Erdos848` modules behind the final theorem were compiled from
     source; Mathlib and its dependencies were taken from the official
     Mathlib build cache (`lake exe cache get`, 8,418 files), not rebuilt and
     not taken from any cache of Li's. (The two remaining project files,
     `PublicationAxiomAudit` and `PublicationTheoremMap`, are not imported by
     the final theorem and were not built.)
   - `Erdos848.PaperGeneratedCertificateProvider.all_N` was checked against
     a transcription of #848 written purely with Mathlib `Squarefree`
     (`li-replay/check_all_N.lean`), depending only on
     `[propext, Classical.choice, Quot.sound]`
     (`li-replay/final_check.log`);
   - `leanchecker` (the toolchain's re-checker, formerly lean4checker: it
     re-runs every declaration of a compiled module through the Lean kernel,
     so it catches anything that bypassed the kernel during elaboration; it
     uses the same kernel, so it is not an independent kernel) replayed all
     30,636 `Erdos848` modules and finished 2026-11-01T17:32:06Z with
     0 failures and 0 problems. Mathlib was not replayed. It was run as one
     call per namespace group (624 groups, at most two at a time); every
     group log ends with `exit=0`, contains no "found a problem" line, and
     lists every module of its group as replayed
     (`li-replay/leanchecker/`: `groups.tsv`, `group_logs.tgz`, the runner
     `lc_groups_v3b.py` and `lc_one.sh`, `all_modules.txt.gz`);
   - manifest audit: 30,735 of 30,736 files match Li's
     `PUBLICATION_MANIFEST.json` by SHA-256; only the patched file differs
     (`li-replay/integrity_report.json`).

## Independent audit

`AUDIT_MEMO_2026-11-01.md` is a second-opinion audit (by Muse) of the
verification record in `UPDATE_2026-11-01.md`: it lists what was
recomputed or rerun independently (including a rerun of the certificate
checker: PASS, and a rerun of the mod-900 optimization: max $18/900$,
exactly two maximizers), what was found wrong in earlier drafts, and what
was checked against sources but not re-derived (e.g. the worst-case-$b$
argument behind the $J'$ density bound, and Sawhney's lemmas).

## Reproduce the certificates

```sh
cd cert
tar xzf certs_1e7.tgz
gcc -O2 -march=native -o gen848 gen848.c -lm
gcc -O2 -fopenmp -o check848 checker/check848.c -lm
./check848 verify out1e7    # expect: RESULT out1e7 PASS, 399,999 plateaus
```

MD5s (`out1e7`): global `e5b8573a`, deltas `e3330948` — see
`cert/RESULTS.md`.

## Layout

- `CLAIM.md` — the 1/50 stability claim, v2 (referee-checked).
- `UPDATE_2026-11-01.md` — the full verification record (revised per the
  audit memo).
- `AUDIT_MEMO_2026-11-01.md` — independent audit of that record.
- `stability/` — density constants and type-optimization code, referee
  report, novelty search.
- `cert/` — certificate generator, independent checker, results, and the
  $10^7$ certificate archive.
- `li-replay/` — the 2-line patch, manifest/integrity reports, statement
  check, build log, and (`li-replay/leanchecker/`) the kernel-replay runner,
  per-group results and logs for Li's proof.
- `forum/forum-post.md` — draft post for erdosproblems.com/848 (not yet
  posted; one wording change from the UPDATE draft: "referee-checked
  claim", not "proof", in the introduction).

Some documents cite paths from the working folder on the author's machine
(`final/`, `leanchecker/`, `diag/`, `review/`, `fable/`); in this repository
the corresponding files are in `li-replay/` and `stability/`. The referee's
other files, the Argon review and the Fable notes are not included.

## Credits and AI use

Paul Lee directed this work and made the decisions. Much of the computation,
code and writing was done with AI models, which are named where they
contributed:

- **Claude** (Anthropic): the source rebuild of Li's repository, the
  diagnosis of the build stall and the 2-line fix, the manifest and
  escape-hatch scan, the statement and axiom check (`check_all_N.lean`), and
  the `leanchecker` replay and its runner.
- **Muse**: the independent audit (`AUDIT_MEMO_2026-11-01.md`).
- Other reviewers (a separate referee agent, Argon, Fable, Gemini) are named
  in the documents where their work appears.

Corrections are welcome as GitHub issues.
