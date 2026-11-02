# Heuristic (simulated annealing) search directly on the 900-type objective F(S), no reduction (referee code).
import json, random, math, sys
cst = json.load(open("consts_ref.json"))
K = cst["K2p"][1]; J = cst["Jp"][1]
M = 900
def glued(s, t): x = s*t+1; return x % 4 == 0 or x % 9 == 0 or x % 25 == 0
C = [s for s in range(M) if s % 25 in (7, 18)]
ng = {s: sum(1 << t for t in range(M) if not glued(s, t)) for s in C}
C7 = sum(1 << s for s in C if s % 25 == 7); C18 = sum(1 << s for s in C if s % 25 == 18)
Cmask = C7 | C18
def F(S):
    v = J * bin(S & ~Cmask).count("1")
    m = S & Cmask
    while m:
        s = (m & -m).bit_length() - 1; m &= m - 1
        v += 1.0 if not (S & ng[s]) else K
    return v
def valid(S):
    return S and (S & ~C7) and (S & ~C18)
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
best = (0, 0)
for restart in range(60):
    r = random.random()
    if r < 0.3: S = sum(1 << t for t in range(M) if random.random() < 0.5)
    elif r < 0.6: S = sum(1 << t for t in C if random.random() < 0.5) | (1 << random.randrange(M))
    else: S = (1 << random.choice(C)) | (1 << random.choice(C)) | (1 << random.randrange(M))
    if not valid(S): continue
    cur = F(S); T = 2.0
    for it in range(30000):
        T = max(0.01, T * 0.9997)
        t = random.choice(C) if random.random() < 0.7 else random.randrange(M)
        S2 = S ^ (1 << t)
        if not valid(S2): continue
        f2 = F(S2)
        if f2 >= cur or random.random() < math.exp((f2 - cur) / T):
            S, cur = S2, f2
            if cur > best[0] + 1e-12:
                best = (cur, S)
print("best 900F found:", best[0], " residues mod 100:", sorted({t % 100 for t in range(M) if best[1] >> t & 1}),
      " |S| =", bin(best[1]).count("1"))
