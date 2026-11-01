# 0-1 program on the reduced model (72 C types + 36 non-C signature groups of 23 types), HiGHS.
# Also enumerates all optimal solutions by no-good cuts.
import json, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

cst = json.load(open("consts_ref.json"))
K = cst["K2p"][1]; J = cst["Jp"][1]
M = 900
def glued(s, t): x = s*t+1; return x % 4 == 0 or x % 9 == 0 or x % 25 == 0
C = [s for s in range(M) if s % 25 in (7, 18)]
sigs = [(a, b) for a in range(4) for b in range(9)]
# representative non-C type for each signature (verify all 23 behave the same towards C)
rep = {}
for sg in sigs:
    members = [t for t in range(M) if t % 25 not in (7, 18) and (t % 4, t % 9) == sg]
    assert len(members) == 23
    for s in C:
        assert len({glued(s, t) for t in members}) == 1
    rep[sg] = members[0]
nC = 72; nY = 36
# vars: x (72), y (36), g (72)
nv = nC + nY + nC
c = np.zeros(nv); c[:nC] = -K; c[nC:nC+nY] = -23*J; c[nC+nY:] = -(1-K)
rows = []
for i, s in enumerate(C):
    gi = nC + nY + i
    rows.append(({gi: 1, i: -1}, -np.inf, 0))
    for j, t in enumerate(C):
        if not glued(s, t): rows.append(({gi: 1, j: 1}, -np.inf, 1))
    for k, sg in enumerate(sigs):
        if not glued(s, rep[sg]): rows.append(({gi: 1, nC+k: 1}, -np.inf, 1))
def build(extra):
    R = rows + extra
    A = lil_matrix((len(R), nv))
    for r, (d, l, u) in enumerate(R):
        for col, v in d.items(): A[r, col] = v
    return LinearConstraint(A.tocsr(), [l for _, l, _ in R], [u for _, _, u in R])
cases = {
  "nonC present": [({nC+k: 1 for k in range(nY)}, 1, np.inf)],
  "C only, both classes": [({i: 1 for i, s in enumerate(C) if s % 25 == 7}, 1, np.inf),
                           ({i: 1 for i, s in enumerate(C) if s % 25 == 18}, 1, np.inf),
                           ({nC+k: 1 for k in range(nY)}, -np.inf, 0)],
}
for name, extra in cases.items():
    sols = []; cuts = []
    while True:
        t0 = time.time()
        res = milp(c, constraints=build(extra + cuts), integrality=np.ones(nv), bounds=Bounds(0, 1),
                   options=dict(mip_rel_gap=0, time_limit=600))
        if res.status != 0: print(name, "status", res.message); break
        val = -res.fun
        if sols and val < sols[0][0] - 1e-7:
            print("  next value after optima:", round(val, 6), "density", val/900); break
        x = np.round(res.x).astype(int)
        S = [C[i] for i in range(nC) if x[i]]
        Y = [sigs[k] for k in range(nY) if x[nC+k]]
        sols.append((val, S, Y))
        print(name, ": 900F =", round(val, 6), " C types mod 100:", sorted({s % 100 for s in S}), " #C:", len(S), " #sig groups:", len(Y), " (%.1fs)" % (time.time()-t0))
        # no-good cut on (x, y) part
        ones = [i for i in range(nC+nY) if x[i]]; zeros = [i for i in range(nC+nY) if not x[i]]
        d = {i: 1 for i in zeros}; d.update({i: -1 for i in ones})
        cuts.append((d, 1 - len(ones), np.inf))
        if len(sols) > 6: break
