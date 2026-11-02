# Check the "worst-case representative b" argument on finite prime sets by exact counting over a full period.
# Event D: p^2 | a^2+1 for p in Dp; event P_b: q^2 | ab+1 for q in Pq (q not dividing b).
import itertools, numpy as np
from sympy.ntheory import sqrt_mod
from sympy.ntheory.modular import crt

def run(Dp, Pq):
    mods = [q*q for q in Pq]
    L = 1
    for m in mods: L *= m
    a = np.arange(L, dtype=np.int64)
    Dmask = np.zeros(L, bool)
    for p in Dp:
        Dmask |= ((a % (p*p)) * (a % (p*p)) + 1) % (p*p) == 0
    # local configurations: for q in Dp: 'div','coin','gen'; for others: 'div','gen'
    opts = [("div", "coin", "gen") if q in Dp else ("div", "gen") for q in Pq]
    worst_formula = None
    results = []
    for conf in itertools.product(*opts):
        residues = []
        for q, o in zip(Pq, conf):
            m = q*q
            if o == "div": residues.append(q)              # b = q mod q^2 -> q | b
            elif o == "coin": residues.append(sqrt_mod(-1, m))  # b^2 = -1 mod q^2
            else:
                # generic: unit, -b^{-1} not a root of x^2+1 mod q^2
                for r in range(2, m):
                    if r % q and (r*r+1) % m != 0 and (pow(r, -1, m)**2 + 1) % m != 0:
                        residues.append(r); break
        b = int(crt(mods, residues)[0])
        P = np.zeros(L, bool)
        for q in Pq:
            if b % q: P |= (a * (b % (q*q)) + 1) % (q*q) == 0
        dens = np.count_nonzero(Dmask & P) / L
        # formula 1 - prod Y - prod X + prod Z
        Y = X = Z = 1.0
        for q, o in zip(Pq, conf):
            m = q*q
            y = 1 - (2/m if q in Dp else 0)
            x = 1 if o == "div" else 1 - 1/m
            if o == "div": z = y
            elif o == "coin": z = y
            else: z = y - 1/m
            Y *= y; X *= x; Z *= z
        f = 1 - Y - X + Z
        results.append((dens, f, conf, b))
    allcoin = tuple("coin" if q in Dp else "gen" for q in Pq)
    worst = [r for r in results if r[2] == allcoin][0]
    mx = max(results, key=lambda r: r[0])
    ok = all(abs(d-f) < 1e-12 for d, f, _, _ in results)
    print("primes D=%s P=%s period %d: formula exact for all %d configs: %s; max density %.6g at %s; worst-case formula %.6g; max<=worst: %s"
          % (Dp, Pq, L, len(results), ok, mx[0], mx[2], worst[1], mx[0] <= worst[1] + 1e-12))

run([13], [7, 13])
run([13, 17], [7, 13, 17])
run([13, 17], [11, 13, 17])
run([13], [7, 11, 13])
