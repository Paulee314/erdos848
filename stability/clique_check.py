# Exact largest admissible set not inside one class mod 25, for small N (referee code, independent of rival.py).
import sys, time
import numpy as np
import networkx as nx
from networkx.algorithms import bipartite

def nonsqfree_table(L):
    t = np.zeros(L+1, bool)
    p = 2
    s = np.ones(int(L**0.5)+2, bool); s[:2] = False
    for i in range(2, len(s)):
        if s[i]:
            s[i*i::i] = False
            t[i*i::i*i] = True
    return t

def max_clique(adj, cand):
    """adj: dict v->bitset int; cand: bitset. returns (size, bitset) of a maximum clique inside cand."""
    best = [0, 0]
    def color_order(P):
        # greedy colouring; returns list of (v, colour) in increasing colour
        order = []
        col = 0
        U = P
        while U:
            col += 1
            Q = U
            while Q:
                v = (Q & -Q).bit_length() - 1
                Q &= ~adj[v]; Q &= ~(1 << v)
                U &= ~(1 << v)
                order.append((v, col))
        return order
    def expand(R, rsize, P):
        order = color_order(P)
        for v, col in reversed(order):
            if rsize + col <= best[0]:
                return
            NR = R | (1 << v)
            NP = P & adj[v]
            if NP:
                expand(NR, rsize+1, NP)
            elif rsize + 1 > best[0]:
                best[0] = rsize + 1; best[1] = NR
            P &= ~(1 << v)
    expand(0, 0, cand)
    return best[0], best[1]

def run(N):
    t0 = time.time()
    nsf = nonsqfree_table(N*N+1)
    V = [n for n in range(1, N+1) if nsf[n*n+1]]
    pos = {v: i for i, v in enumerate(V)}
    adj = {}
    for i, a in enumerate(V):
        m = 0
        for j, b in enumerate(V):
            if i != j and nsf[a*b+1]: m |= 1 << j
        adj[i] = m
    bit = lambda S: sum(1 << pos[v] for v in S)
    c7 = [v for v in V if v % 25 == 7]; c18 = [v for v in V if v % 25 == 18]
    nonC = [v for v in V if v % 25 not in (7, 18)]
    assert len(c7) == len([n for n in range(1, N+1) if n % 25 == 7])
    # (i) cliques containing a non-C vertex
    best_i, arg_i = 0, None
    for v in nonC:
        i = pos[v]
        if 1 + bin(adj[i]).count("1") <= best_i: continue
        s, B = max_clique(adj, adj[i])
        if s + 1 > best_i:
            best_i = s + 1; arg_i = sorted(V[k] for k in range(len(V)) if (B | (1 << i)) >> k & 1)
    # (ii) cliques inside C meeting both classes: max biclique in cross graph via Konig, forcing a pair (u,w)
    best_ii, arg_ii = 0, None
    H = nx.Graph()
    H.add_nodes_from(c7, bipartite=0); H.add_nodes_from(c18, bipartite=1)
    H.add_edges_from((u, w) for u in c7 for w in c18 if not nsf[u*w+1])   # cross NON-edges
    for u in c7:
        for w in c18:
            if not nsf[u*w+1]: continue
            rem = set(c7) | set(c18)
            rem -= set(H[u]); rem -= set(H[w])
            Hs = H.subgraph(rem)
            top = [x for x in rem if x % 25 == 7]
            mt = bipartite.hopcroft_karp_matching(Hs, top_nodes=top)
            mis = len(rem) - len(mt)//2
            if mis > best_ii:
                cover = bipartite.to_vertex_cover(Hs, mt, top_nodes=top)
                best_ii = mis; arg_ii = sorted(rem - cover)
    pure = len(c7)
    print("N=%d |V|=%d pure7=%d | best non-pure via nonC vertex=%d | best inside C with both classes=%d | N/50=%.1f | time %.1fs"
          % (N, len(V), pure, best_i, best_ii, N/50, time.time()-t0))
    for name, arg in (("nonC", arg_i), ("C-both", arg_ii)):
        if arg: print("   %s argmax residues mod 100: %s ; mod 25: %s" % (name, sorted({x % 100 for x in arg}), sorted({x % 25 for x in arg})))
    sys.stdout.flush()
    return pure, best_i, best_ii

if __name__ == "__main__":
    for N in map(int, sys.argv[1:]):
        run(N)
