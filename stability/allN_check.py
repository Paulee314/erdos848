# For every N <= Nmax: (1) overall max admissible |A| vs |{n<=N: n=7 mod 25}|,
# (2) max admissible A not inside one class mod 25, vs N/50. Incremental in N (referee code).
import sys, time
import clique_check as cc

Nmax = int(sys.argv[1])
nsf = cc.nonsqfree_table(Nmax*Nmax+1)
V = []; adj = {}
omega = 0; nonpure = 0
viol1 = []; excess = []
t0 = time.time()
def is_pure(cl):
    return all(x % 25 == 7 for x in cl) or all(x % 25 == 18 for x in cl)
for N in range(1, Nmax+1):
    if nsf[N*N+1]:
        i = len(V); m = 0
        for j, b in enumerate(V):
            if nsf[N*b+1]:
                m |= 1 << j; adj[j] |= 1 << i
        V.append(N); adj[i] = m
        # (1) overall: clique containing N
        if 1 + bin(m).count("1") > omega:
            s, B = cc.max_clique(adj, m)
            omega = max(omega, s + 1)
        # (2) non-pure cliques containing N
        if N % 25 not in (7, 18):
            if 1 + bin(m).count("1") > nonpure:
                s, B = cc.max_clique(adj, m)
                nonpure = max(nonpure, s + 1)
        else:
            # N in class c; need another vertex u outside class c in the clique
            c = N % 25
            for j in range(i):
                if (m >> j & 1) and V[j] % 25 != c:
                    cand = m & adj[j]
                    if 2 + bin(cand).count("1") <= nonpure: continue
                    s, B = cc.max_clique(adj, cand) if cand else (0, 0)
                    nonpure = max(nonpure, s + 2)
    pure7 = 0 if N < 7 else (N - 7)//25 + 1
    if omega != pure7: viol1.append((N, omega, pure7))
    ref = max(sum(1 for r in (7, 93) if r <= N) + sum((N - r)//100 for r in (7, 93) if r <= N),
              sum(1 for r in (43, 57) if r <= N) + sum((N - r)//100 for r in (43, 57) if r <= N))
    if nonpure > ref: excess.append((N, nonpure, ref))
    if N % 500 == 0:
        print("N=%d omega=%d pure7=%d nonpure=%d N/50=%.1f  (%.0fs)" % (N, omega, pure7, nonpure, N/50, time.time()-t0)); sys.stdout.flush()
print("N with omega != pure7 count:", viol1[:20], "... total", len(viol1))
print("N with nonpure > |{7,93 or 43,57 mod 100} cap [N]|: total", len(excess), " largest such N:", excess[-5:] if excess else None)
mx = max(((np - r), n, np) for n, np, r in excess) if excess else None
print("max excess over that reference:", mx)
