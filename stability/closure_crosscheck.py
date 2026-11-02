# For every valid closed pair (G7,G18), build the realizing type set S_G on all 900 types and evaluate F directly.
import runpy, sys
sys.argv = ["opt_closure.py"]
g = runpy.run_path("opt_closure.py")
res, Rof, idx, sig, F_direct, valid_S, M = g["res"], g["Rof"], g["idx"], g["sig"], g["F_direct"], g["valid_S"], g["M"]
mx = 0; bad = 0
for F, P, Qs in res:
    X7, X18 = Rof(Qs), Rof(P); Y = X7 & X18
    S = [s for s in range(M) if (s % 25 == 7 and X7 >> idx[sig(s)] & 1) or (s % 25 == 18 and X18 >> idx[sig(s)] & 1)
         or (s % 25 not in (7, 18) and Y >> idx[sig(s)] & 1)]
    assert valid_S(S)
    fd = F_direct(S)
    if fd < F - 1e-9: bad += 1
    mx = max(mx, fd)
print("closed pairs checked:", len(res), " F_direct >= F* violations:", bad, " max F_direct over realizations:", mx)
