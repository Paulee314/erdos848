# Independent computation of K1, K2', J', Q with rigorous enclosures (referee code).
import numpy as np, math, json, sys
from mpmath import mp, mpf, pi
mp.dps = 30

P = int(sys.argv[1]) if len(sys.argv) > 1 else 50_000_000

def primes_upto(n):
    s = np.ones(n+1, dtype=bool); s[:2] = False
    for i in range(2, int(n**0.5)+1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

pr = primes_upto(P).astype(np.float64)
D = pr[(pr % 4 == 1) & (pr >= 13)]
Q3 = pr[(pr % 4 == 3) & (pr >= 7)]

def logprod(ps, c):
    # sum of log(1 - c/p^2), accurate summation
    return math.fsum(np.log1p(-c/ps**2).tolist())

lA = logprod(D, 2.0); lB = logprod(D, 1.0); lQ = logprod(Q3, 1.0); lA3 = logprod(D, 3.0)
A, B, Q, A3 = (math.exp(x) for x in (lA, lB, lQ, lA3))
# tail: prod_{p>P}(1-c/p^2) in [1 - c/P, 1]; plus fp slack 1e-12 relative
slack = 1e-12
def enc(v, c):
    return (v*(1-c/P)*(1-slack), v*(1+slack))
Ae, Be, Qe, A3e = enc(A, 2), enc(B, 1), enc(Q, 1), enc(A3, 3)

def Jp(A, B, Q):  # J' = 1 - A - Q B + A Q  (decreasing in A, B, Q)
    return 1 - A - Q*B + A*Q
J_lo = Jp(Ae[1], Be[1], Qe[1]); J_hi = Jp(Ae[0], Be[0], Qe[0])
K1_lo, K1_hi = 1 - Ae[1], 1 - Ae[0]
K2_lo, K2_hi = 1 - Qe[1]*Be[1], 1 - Qe[0]*Be[0]
K2_closed = 1 - (6/pi**2) / (mpf(3)/4 * mpf(8)/9 * mpf(24)/25)
# "generic b" (b coprime to all, no coincidence anywhere): 1 - A - QB + Q*A3
Jgen = 1 - A - Q*B + Q*A3
out = dict(P=P, A=A, B=B, Q=Q, K1=(K1_lo, K1_hi), K2p=(K2_lo, K2_hi), K2p_closed=float(K2_closed),
           Jp=(J_lo, J_hi), J_generic_b=Jgen)
for k, v in out.items(): print(k, v)
print("72K2' + 828J' =", 72*K2_hi + 828*J_hi, "(vs 18)")
json.dump(out, open("consts_ref.json", "w"), indent=1)
