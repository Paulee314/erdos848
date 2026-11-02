# Independent check of F1-F3 and the sharpness example (referee code).
M = 900

def sqdiv(x):
    """which of 4, 9, 25 divide x"""
    return [d for d in (4, 9, 25) if x % d == 0]

# F1
assert all((n*n+1) % 4 for n in range(4))
assert all((n*n+1) % 9 for n in range(9))
r25 = [n for n in range(25) if (n*n+1) % 25 == 0]
print("n^2+1 = 0 mod 25 for n mod 25 in", r25)
# p = 3 mod 4 never divides n^2+1 (check small primes)
from sympy import primerange
for p in primerange(3, 2000):
    if p % 4 == 3:
        assert all((n*n+1) % p for n in range(p))
# p = 1 mod 4: exactly two roots mod p^2
for p in primerange(5, 400):
    if p % 4 == 1:
        assert sum(1 for n in range(p*p) if (n*n+1) % (p*p) == 0) == 2
print("F1 ok")

C = [s for s in range(M) if s % 25 in (7, 18)]
assert len(C) == 72
glued = lambda s, t: bool(sqdiv(s*t+1))
# F2: glue depends only on types: check (s + 900k)(t+900l)+1 mod 4,9,25
import random
for _ in range(20000):
    a = random.randrange(1, 10**9); b = random.randrange(1, 10**9)
    assert sqdiv(a*b+1) == sqdiv((a % M)*(b % M)+1)
print("F2 ok (type-determinedness of 4,9,25)")
# F3
Cset = set(C)
for s in C:
    assert glued(s, s)
    for t in C:
        if s % 25 == t % 25:
            assert glued(s, t)
for s in range(M):
    if s not in Cset:
        assert not glued(s, s)
for s in C:
    for t in range(M):
        if t % 25 != s % 25:
            assert (s*t+1) % 25 != 0
print("F3 ok")
# counts: how many types in 7-class glued to a given outside type, max
best = 0
for t in range(M):
    if t % 25 == 7: continue
    k = sum(1 for s in C if s % 25 == 7 and glued(s, t))
    best = max(best, k)
print("max # of 7-class types glued to one type outside 7-class:", best)

# Sharpness example
A_types = [s for s in range(M) if s % 100 in (7, 93)]
print("types in example:", len(A_types), "density", len(A_types)/M)
assert all(glued(s, t) for s in A_types for t in A_types)
print("all pairs (incl. a=b) glued, mod-25 classes present:", sorted({s % 25 for s in A_types}))
# brute check on actual integers
N = 20000
A = [n for n in range(1, N+1) if n % 100 in (7, 93)]
from sympy import factorint
def nonsqfree_by_small(x):
    return x % 4 == 0 or x % 25 == 0
assert all(nonsqfree_by_small(a*b+1) for a in A for b in A)
print("example admissible on [1,%d], |A| = %d, N/50 = %g" % (N, len(A), N/50))
# other maximizers of the same shape: pairs (u mod 100 in 7-class, v mod 100 in 18-class) with all glued
sols = []
for u in range(100):
    for v in range(100):
        if u % 25 == 7 and v % 25 == 18 and u < 100 and v < 100:
            T = [s for s in range(M) if s % 100 in (u, v)]
            if all(glued(s, t) for s in T for t in T):
                sols.append((u, v))
print("pairs of residue classes mod 100 (7-class, 18-class) giving glued set:", sols)
