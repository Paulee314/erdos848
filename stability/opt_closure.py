# Exhaustive solution of the type optimisation via Galois-closed sets (referee code).
# Reduction: a type s in C is (class c in {7,18}, sig=(s mod 4, s mod 9)); non-C types matter only by sig
# (23 non-C types per sig). Cross-class / C-vs-nonC gluing is a relation R on sigs (via 4 or 9).
import json, itertools, random, sys
from fractions import Fraction

cst = json.load(open("consts_ref.json"))
# use upper ends of the enclosures (conservative for an upper bound), and also lower ends to test sensitivity
K = cst["K2p"][1]; J = cst["Jp"][1]
if len(sys.argv) > 2:
    K = float(sys.argv[1]); J = float(sys.argv[2])
M = 900
sigs = [(a, b) for a in range(4) for b in range(9)]
idx = {s: i for i, s in enumerate(sigs)}
def sig(s): return (s % 4, s % 9)
def glued(s, t): x = s*t+1; return x % 4 == 0 or x % 9 == 0 or x % 25 == 0

# R from definition of gluing between a 7-class type and an 18-class type (must be type-independent)
Rm = [0]*36
for i, (a, b) in enumerate(sigs):
    for j, (a2, b2) in enumerate(sigs):
        if (a*a2+1) % 4 == 0 or (b*b2+1) % 9 == 0:
            Rm[i] |= 1 << j
# sanity: R agrees with actual gluing for 7-class vs 18-class and 7-class vs non-C types
for s in range(M):
    for t in range(M):
        if s % 25 == 7 and t % 25 != 7:
            assert glued(s, t) == bool(Rm[idx[sig(s)]] >> idx[sig(t)] & 1)
        if s % 25 == 18 and t % 25 != 18:
            assert glued(s, t) == bool(Rm[idx[sig(s)]] >> idx[sig(t)] & 1)
FULL = (1 << 36) - 1
def Rof(mask):
    r = FULL
    m = mask; i = 0
    while m:
        if m & 1: r &= Rm[i]
        m >>= 1; i += 1
    return r
pc = lambda m: bin(m).count("1")

# closed sets = intersections of the Rm[i] (plus FULL)
closed = {FULL}
frontier = [FULL]
while frontier:
    nf = []
    for X in frontier:
        for i in range(36):
            Y = X & Rm[i]
            if Y not in closed:
                closed.add(Y); nf.append(Y)
    frontier = nf
closed = sorted(closed, key=pc, reverse=True)
print("number of closed sets:", len(closed))
for X in closed: assert Rof(Rof(X)) == X

c = 23*J
res = []
for P in closed:
    RP = Rof(P)
    for Qs in closed:
        if Qs & ~RP: continue  # need Q subset R(P)
        RQ = Rof(Qs)
        Y = RP & RQ
        valid = (Y != 0) or (RP != 0 and RQ != 0)
        if not valid: continue
        F = (1-K)*(pc(P)+pc(Qs)) + K*(pc(RP)+pc(RQ)) + c*pc(Y)
        res.append((F, P, Qs))
res.sort(key=lambda r: -r[0])
def show(m): return sorted(sigs[i] for i in range(36) if m >> i & 1)
print("top values (900*F):")
seen = set()
for F, P, Qs in res[:12]:
    print(round(F, 6), "|G7|=%d |G18|=%d |R(G7)|=%d |R(G18)|=%d |Y|=%d" % (pc(P), pc(Qs), pc(Rof(P)), pc(Rof(Qs)), pc(Rof(P) & Rof(Qs))))
best = res[0][0]
maxers = [(P, Qs) for F, P, Qs in res if F > best - 1e-9]
print("max 900F =", best, " #maximizing closed pairs:", len(maxers))
for P, Qs in maxers:
    print("  G7 sigs:", show(P)); print("  G18 sigs:", show(Qs)); print("  R(G7):", show(Rof(P)), " R(G18):", show(Rof(Qs)))
second = max(F for F, P, Qs in res if F < best - 1e-9)
print("second best 900F =", second, "-> density", second/900)
# also report best config that uses at least one non-C type, and best with Y empty but not exact maximizer
bestY = max(F for F, P, Qs in res if Rof(P) & Rof(Qs))
print("best with non-C types present (900F):", bestY, "density", bestY/900)

# Direct definition of F(S) on 900 types, for cross-validation
Cset = {s for s in range(M) if s % 25 in (7, 18)}
def F_direct(S):
    tot = 0.0
    for s in S:
        if s in Cset:
            tot += 1.0 if all(glued(s, t) for t in S) else K
        else:
            tot += J
    return tot
def valid_S(S):
    return S and not all(s % 25 == 7 for s in S) and not all(s % 25 == 18 for s in S)
# realize maximizers as type sets and compute directly
for P, Qs in maxers:
    S = [s for s in range(M) if (s % 25 == 7 and P >> idx[sig(s)] & 1) or (s % 25 == 18 and Qs >> idx[sig(s)] & 1)]
    print("maximizer realized: residues mod 100 =", sorted({s % 100 for s in S}), " F_direct*900 =", F_direct(S), "valid", valid_S(S))
# random S: check F_direct <= best
random.seed(1)
worst = 0
for trial in range(3000):
    k = random.choice([2, 5, 10, 20, 40, 100, 300])
    pool = random.choice([list(Cset), list(range(M))])
    S = random.sample(pool, min(k, len(pool)))
    if not valid_S(S): continue
    worst = max(worst, F_direct(S))
print("random S: max F_direct*900 =", worst, "<= best:", worst <= best + 1e-9)
