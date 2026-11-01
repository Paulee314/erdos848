# Certificate format for Erdős #848 seating-chart certificates

Definitions. A positive integer n is a *candidate* if n²+1 is not squarefree. An *anchor* is a_m = 25m+7.
For Nmax = 25K+31, plateau k (0 ≤ k ≤ K) covers N ∈ [25k+7, 25k+31]; there #{n ≤ N : n ≡ 7 (mod 25)} = k+1.

Files (directory per run):
- global.txt — first line `# Nmax <Nmax> K <K>`; then one line `n idx` per candidate n ≤ Nmax, in increasing n.
  idx = index m of n's class anchor a_m. For n ≡ 7 (mod 25), idx = (n−7)/25. For n ≡ 18 (mod 25), idx may be −1
  (no global class). For other n, idx = −1 means "not placed" (makes every plateau containing n invalid).
- deltas.txt — one line per plateau k = 0..K, in order: `k j:m j:m ...` (or `k FAIL`). Each `j:m` re-homes the
  18-mod-25 number x_j = 25j+18 (j ≤ k) to anchor index m for this plateau only, overriding its global idx.

The certificate for plateau k, with N = 25k+31, is valid iff
1. every candidate n ≤ N appears in global.txt (and no non-candidate appears);
2. every candidate n ≤ N has an effective index (override if listed for this plateau, else global idx) in [0, k];
3. every anchor a_m ≤ N has effective index m;
4. for every m ≤ k, any two distinct members u, v (n ≤ N with effective index m) satisfy: uv+1 is squarefree.
If valid, every A ⊆ [1, N'] with ab+1 non-squarefree for all a, b ∈ A has |A| ≤ k+1 for every N' in [25k+7, 25k+31].
(Members ≤ 25k+31 are checked; restricting to N' < 25k+31 keeps validity since all anchors a_0..a_k ≤ 25k+7.)
For N' ≤ 6 there are no candidates (check this too).
