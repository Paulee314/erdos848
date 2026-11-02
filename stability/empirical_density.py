# Empirical densities of P_b and D & P_b for a <= X and several representatives b (referee code).
import sys, math, json, time
import numpy as np
from sympy.ntheory.modular import crt

X = int(sys.argv[1]) if len(sys.argv) > 1 else 10**7
cst = json.load(open("consts_ref.json"))
K2p = cst["K2p"][1]; Jp = cst["Jp"][1]

def primes_upto(n):
    s = np.ones(n+1, dtype=bool); s[:2] = False
    for i in range(2, int(n**0.5)+1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

def sqrtm1_p2(p):
    for c in range(2, p):
        t = pow(c, (p-1)//4, p)
        if (t*t + 1) % p == 0: break
    m = p*p
    t = (t - (t*t+1) * pow(2*t, -1, m)) % m
    assert (t*t+1) % m == 0
    return t

t0 = time.time()
PR = primes_upto(max(X, 1))
# D(a): p^2 | a^2+1 for p = 1 mod 4, p >= 13, p <= X
Dm = np.zeros(X+1, bool)
roots = {}
for p in PR[(PR % 4 == 1) & (PR >= 13)].tolist():
    m = p*p; t = sqrtm1_p2(p); roots[p] = t
    for r in (t, m - t):
        if m <= X: Dm[r::m] = True
        elif r <= X: Dm[r] = True
Dm[0] = False
print("D sieve done %.1fs, dens(D) over a<=X = %.6f (K1 = %.6f)" % (time.time()-t0, Dm[1:].mean(), cst["K1"][1]))
a = np.arange(X+1)
inC = (a % 25 == 7) | (a % 25 == 18)
nonC = ~inC; nonC[0] = False; inC[0] = False

def coincide_b(ps, extra_coprime=()):
    mods = [p*p for p in ps]; res = [sqrtm1_p2(p) for p in ps]
    b = int(crt(mods, res)[0])
    return b

PRbig = None
def P_mask(b):
    Q = int(math.isqrt(X*b + 1)) + 1
    global PRbig
    if PRbig is None or PRbig[-1] < Q: PRbig = primes_upto(Q)
    P = np.zeros(X+1, bool)
    for q in PRbig[(PRbig >= 7) & (PRbig <= Q)].tolist():
        if b % q == 0: continue
        m = q*q
        r = (-pow(b, -1, m)) % m
        if m <= X: P[r::m] = True
        elif 1 <= r <= X: P[r] = True
    P[0] = False
    return P

def predicted(b, Pmax=10**7):
    # exact density formulas for this b (products truncated at Pmax; tail negligible at 1e-7 level)
    ps = PR[PR >= 7].tolist() if PR[-1] >= Pmax else primes_upto(Pmax)[3:].tolist()
    lX = lA = lZ = 0.0
    for l in ps:
        m = l*l
        div = (b % l == 0)
        if l % 4 == 1:
            lA += math.log1p(-2/m)
            if div: lZ += math.log1p(-2/m)
            else:
                coin = (b*b + 1) % m == 0
                lZ += math.log1p(-(2 if coin else 3)/m)
            if not div: lX += math.log1p(-1/m)
        else:
            if not div:
                lX += math.log1p(-1/m); lZ += math.log1p(-1/m)
    A, Xb, Z = math.exp(lA), math.exp(lX), math.exp(lZ)
    return 1 - Xb, 1 - A - Xb + Z

bs = {
  "b=1": 1,
  "b=9699690 (2*3*5*7*11*13*17*19)": 9699690,
  "b=30030 (2*3*5*7*11*13)": 30030,
  "b: 13^2*17^2 | b^2+1": coincide_b([13, 17]),
  "b: 13^2*17^2*29^2 | b^2+1": coincide_b([13, 17, 29]),
  "b: 13^2 | b^2+1": coincide_b([13]),
  "b=9999991 (prime)": 9999991,
}
out = {}
for name, b in bs.items():
    t1 = time.time()
    P = P_mask(b)
    pP, pDP = predicted(b)
    dP_C = P[inC].mean(); dDP_nonC = (Dm & P)[nonC].mean()
    # per-type maxima (types mod 900) for D&P over non-C types and P over C types
    types = a % 900
    cntDP = np.bincount(types[nonC], weights=(Dm & P)[nonC], minlength=900)
    totnC = np.bincount(types[nonC], minlength=900)
    cntP = np.bincount(types[inC], weights=P[inC], minlength=900)
    totC = np.bincount(types[inC], minlength=900)
    mxDP = max(cntDP[s]/totnC[s] for s in range(900) if totnC[s]); mxP = max(cntP[s]/totC[s] for s in range(900) if totC[s])
    zDP = max((cntDP[s] - totnC[s]*pDP)/math.sqrt(totnC[s]*pDP*(1-pDP)) for s in range(900) if totnC[s])
    zP = max((cntP[s] - totC[s]*pP)/math.sqrt(totC[s]*pP*(1-pP)) for s in range(900) if totC[s])
    zaggDP = ((Dm & P)[nonC].sum() - nonC.sum()*pDP)/math.sqrt(nonC.sum()*pDP*(1-pDP))
    zaggP = (P[inC].sum() - inC.sum()*pP)/math.sqrt(inC.sum()*pP*(1-pP))
    spot = {s: round(cntDP[s]/totnC[s], 5) for s in (1, 2, 13, 100, 451) if totnC[s]}
    print("%-36s b=%-10d | P on C-types: %.5f (pred %.5f, K2'=%.5f, max over types %.5f) | D&P on nonC: %.5f (pred %.5f, J'=%.5f, max over types %.5f) [%.0fs]"
          % (name, b, dP_C, pP, K2p, mxP, dDP_nonC, pDP, Jp, mxDP, time.time()-t1))
    print("      z-scores vs exact prediction: aggregate P %.2f, D&P %.2f; max per-type z: P %.2f (72 types), D&P %.2f (828 types); D&P in types 1,2,13,100,451: %s" % (zaggP, zaggDP, zP, zDP, spot))
    sys.stdout.flush()
    out[name] = dict(b=b, P_C=dP_C, P_pred=pP, DP_nonC=dDP_nonC, DP_pred=pDP, maxtype_P=mxP, maxtype_DP=mxDP, zaggP=zaggP, zaggDP=zaggDP, zmaxP=zP, zmaxDP=zDP)
json.dump(out, open("empirical_density_%d.json" % X, "w"), indent=1)
