# Direct 0-1 program on all 900 types, solved with HiGHS (scipy.optimize.milp), no structural reduction.
import json, sys, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

cst = json.load(open("consts_ref.json"))
K = cst["K2p"][1]; J = cst["Jp"][1]
M = 900
def glued(s, t): x = s*t+1; return x % 4 == 0 or x % 9 == 0 or x % 25 == 0
C = [s for s in range(M) if s % 25 in (7, 18)]
nC = len(C)
# variables: x_0..x_899, then g_0..g_71 (good flag for C[i])
nv = M + nC
c = np.zeros(nv)
for s in range(M):
    c[s] = -(K if s % 25 in (7, 18) else J)
for i, s in enumerate(C):
    c[M+i] = -(1-K)
rows = []
for i, s in enumerate(C):
    rows.append(([M+i, s], [1, -1], -np.inf, 0))          # g_s <= x_s
    for t in range(M):
        if not glued(s, t):
            rows.append(([M+i, t], [1, 1], -np.inf, 1))   # g_s + x_t <= 1
def solve(case):
    R = list(rows)
    if case == "nonC":
        R.append(([s for s in range(M) if s % 25 not in (7, 18)], None, 1, np.inf))
    else:
        R.append(([s for s in range(M) if s % 25 == 7], None, 1, np.inf))
        R.append(([s for s in range(M) if s % 25 == 18], None, 1, np.inf))
    A = lil_matrix((len(R), nv)); lb = []; ub = []
    for r, (cols, vals, l, u) in enumerate(R):
        for k, col in enumerate(cols):
            A[r, col] = 1 if vals is None else vals[k]
        lb.append(l); ub.append(u)
    t0 = time.time()
    res = milp(c, constraints=LinearConstraint(A.tocsr(), lb, ub), integrality=np.ones(nv),
               bounds=Bounds(0, 1), options=dict(time_limit=3000, mip_rel_gap=1e-9))
    x = np.round(res.x).astype(int)
    S = [s for s in range(M) if x[s]]
    print(case, "status", res.status, res.message, "obj*900 =", -res.fun, "time %.1fs" % (time.time()-t0),
          "|S| =", len(S), "residues mod 100:", sorted({s % 100 for s in S})[:20])
    return -res.fun, S
for case in ("nonC", "both"):
    solve(case)
print("print 18 =", 18.0)
