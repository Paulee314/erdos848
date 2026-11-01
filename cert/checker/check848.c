/*
 * check848.c -- independent verifier for Erdos #848 seating-chart certificates.
 * Written only from FORMAT.md (no generator code consulted).
 *
 * Squarefree test: full factorisation = trial division by small primes (exact
 * division via 64-bit modular inverses), then deterministic Miller-Rabin
 * (7-base set valid for all n < 2^64) and Pollard-Brent rho, both in Montgomery
 * arithmetic with unsigned __int128 products. n is squarefree iff no prime
 * occurs with exponent >= 2.
 *
 * Usage:  check848 selftest
 *         check848 verify <run-dir>
 * Build:  gcc -O2 -fopenmp -o check848 check848.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>
#include <time.h>
#ifdef _OPENMP
#include <omp.h>
#endif

typedef uint64_t u64;
typedef unsigned __int128 u128;

static double now(void) {
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + 1e-9 * ts.tv_nsec;
}

/* ------------------------------------------------------------------ */
/* Montgomery arithmetic modulo odd n < 2^64                           */
/* ------------------------------------------------------------------ */
typedef struct { u64 n, ninv, one, r2; } mont_t;

static inline u64 inv64(u64 n) {          /* n odd: n * x == 1 mod 2^64 */
    u64 x = n;                            /* correct to 3 bits */
    for (int i = 0; i < 5; i++) x *= 2 - n * x;
    return x;
}
static inline void mont_init(mont_t *M, u64 n) {
    M->n = n; M->ninv = inv64(n);
    M->one = (u64)((((u128)1) << 64) % n);          /* R mod n */
    M->r2 = (u64)(((u128)M->one * M->one) % n);     /* R^2 mod n */
}
static inline u64 redc(u128 T, const mont_t *M) {   /* T < n*2^64 -> T/R mod n */
    u64 lo = (u64)T, hi = (u64)(T >> 64);
    u64 m = lo * M->ninv;
    u64 mnhi = (u64)(((u128)m * M->n) >> 64);
    return hi >= mnhi ? hi - mnhi : hi - mnhi + M->n;
}
static inline u64 mmul(u64 a, u64 b, const mont_t *M) { return redc((u128)a * b, M); }
static inline u64 to_mont(u64 a, const mont_t *M) { return mmul(a % M->n, M->r2, M); }
static inline u64 madd(u64 a, u64 b, const mont_t *M) {
    u64 s = a + b;                          /* a,b < n < 2^63 here; still guard */
    if (s < a || s >= M->n) s -= M->n;
    return s;
}
static inline u64 msub(u64 a, u64 b, const mont_t *M) { return a >= b ? a - b : a - b + M->n; }

static inline u64 gcd64(u64 a, u64 b) {
    if (!a) return b;
    if (!b) return a;
    int sh = __builtin_ctzll(a | b);
    a >>= __builtin_ctzll(a);
    do {
        b >>= __builtin_ctzll(b);
        if (a > b) { u64 t = a; a = b; b = t; }
        b -= a;
    } while (b);
    return a << sh;
}

/* deterministic Miller-Rabin for odd n > 2 (bases: Jim Sinclair's 7-base set, all n < 2^64) */
static int is_prime_mr(u64 n) {
    static const u64 bases[7] = {2, 325, 9375, 28178, 450775, 9780504, 1795265022};
    if (n < 2) return 0;
    if (n % 2 == 0) return n == 2;
    if (n < 9) return 1;                      /* 3,5,7 */
    if (n % 3 == 0) return 0;
    mont_t M; mont_init(&M, n);
    u64 d = n - 1; int s = __builtin_ctzll(d); d >>= s;
    u64 one = M.one, mone = n - M.one;
    for (int i = 0; i < 7; i++) {
        u64 a = bases[i] % n;
        if (a == 0) continue;
        u64 x = to_mont(a, &M), r = one, e = d;
        while (e) { if (e & 1) r = mmul(r, x, &M); x = mmul(x, x, &M); e >>= 1; }
        if (r == one || r == mone) continue;
        int ok = 0;
        for (int t = 1; t < s; t++) { r = mmul(r, r, &M); if (r == mone) { ok = 1; break; } }
        if (!ok) return 0;
    }
    return 1;
}

/* Pollard-Brent rho: n odd composite. Returns a nontrivial factor. */
static u64 rho_brent(u64 n) {
    mont_t M; mont_init(&M, n);
    for (u64 c0 = 1;; c0++) {
        u64 c = to_mont(c0, &M), y = to_mont(2 + c0, &M), x = y, ys = y, q = M.one, g = 1;
        u64 r = 1; const u64 m = 128;
        do {
            x = y;
            for (u64 i = 0; i < r; i++) y = madd(mmul(y, y, &M), c, &M);
            u64 k = 0;
            do {
                ys = y;
                u64 lim = (m < r - k) ? m : r - k;
                for (u64 i = 0; i < lim; i++) {
                    y = madd(mmul(y, y, &M), c, &M);
                    q = mmul(q, x > y ? x - y : y - x, &M);
                }
                g = gcd64(q, n);
                k += m;
            } while (k < r && g == 1);
            r <<= 1;
        } while (g == 1);
        if (g == n) {                         /* backtrack */
            do { ys = madd(mmul(ys, ys, &M), c, &M); g = gcd64(x > ys ? x - ys : ys - x, n); } while (g == 1);
        }
        if (g != n && g != 1) return g;
        /* else: cycle closed mod n; try next c */
    }
}

/* ------------------------------------------------------------------ */
/* trial-division table                                                 */
/* ------------------------------------------------------------------ */
typedef struct { u64 p, pinv, lim; } tdp_t;
#define TD_MAX 4096
static tdp_t td[TD_MAX];
static int ntd = 0;
static u64 td_bound = 0;          /* all primes < td_bound are in td[] (plus 2 handled separately) */

static void td_setup(u64 bound) {
    ntd = 0; td_bound = bound;
    for (u64 p = 3; p < bound; p += 2) {
        int pr = 1;
        for (u64 d = 3; d * d <= p; d += 2) if (p % d == 0) { pr = 0; break; }
        if (!pr) continue;
        if (ntd >= TD_MAX) { fprintf(stderr, "td overflow\n"); exit(2); }
        td[ntd].p = p; td[ntd].pinv = inv64(p); td[ntd].lim = UINT64_MAX / p; ntd++;
    }
}

/* Recursively split odd cofactor r (no prime factor < td_bound, r > 1) into primes. */
static void split_big(u64 r, u64 *out, int *cnt) {
    if ((u128)td_bound * td_bound > r || is_prime_mr(r)) { out[(*cnt)++] = r; return; }
    u64 d = rho_brent(r);
    split_big(d, out, cnt);
    split_big(r / d, out, cnt);
}

/* Full factorisation of n >= 1: primes with multiplicity into out (unsorted). */
static int factor_full(u64 n, u64 *out) {
    int cnt = 0;
    if (n <= 1) return 0;
    while ((n & 1) == 0) { out[cnt++] = 2; n >>= 1; }
    for (int i = 0; i < ntd && n > 1; i++) {
        u64 p = td[i].p;
        if (p * p > n) break;                  /* n is 1 or prime */
        while (n * td[i].pinv <= td[i].lim) { out[cnt++] = p; n *= td[i].pinv; }
    }
    if (n > 1) {
        /* if loop ended early because p^2 > n, n is prime; split_big handles via MR anyway */
        split_big(n, out, &cnt);
    }
    return cnt;
}

static int cmpu64(const void *a, const void *b) {
    u64 x = *(const u64 *)a, y = *(const u64 *)b; return x < y ? -1 : x > y;
}

/* squarefree via factorisation; early exit if trial division already finds p^2 */
static int is_squarefree(u64 n) {
    u64 f[80]; int cnt = 0;
    if (n == 0) return 0;
    if ((n & 3) == 0) return 0;
    if ((n & 1) == 0) n >>= 1;
    for (int i = 0; i < ntd && n > 1; i++) {
        u64 p = td[i].p;
        if (p * p > n) { return 1; }           /* remaining n is 1 or a prime */
        if (n * td[i].pinv <= td[i].lim) {
            n *= td[i].pinv;
            if (n * td[i].pinv <= td[i].lim) return 0;   /* p^2 | n */
        }
    }
    if (n == 1) return 1;
    split_big(n, f, &cnt);
    if (cnt == 1) return 1;
    qsort(f, cnt, sizeof(u64), cmpu64);
    for (int i = 1; i < cnt; i++) if (f[i] == f[i - 1]) return 0;
    return 1;
}

/* ------------------------------------------------------------------ */
/* self tests                                                           */
/* ------------------------------------------------------------------ */
static u64 rng_state = 0x9E3779B97F4A7C15ULL;
static u64 rnd(void) {           /* splitmix64 */
    u64 z = (rng_state += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}

/* segmented sieve: primes in [lo, lo+len) using base primes up to sqrt(lo+len) */
static int seg_primes(u64 lo, u64 len, const unsigned char *isc, u64 smax, u64 *out, int maxout) {
    unsigned char *seg = malloc(len); memset(seg, 1, len);
    for (u64 p = 2; p * p < lo + len; p++) {
        if (p > smax) { fprintf(stderr, "seg sieve base too small\n"); exit(2); }
        if (isc[p]) continue;
        u64 s = ((lo + p - 1) / p) * p;
        if (s < p * p) s = p * p;
        for (u64 x = s; x < lo + len; x += p) seg[x - lo] = 0;
    }
    int c = 0;
    for (u64 i = 0; i < len && c < maxout; i++) if (seg[i] && lo + i > 1) out[c++] = lo + i;
    free(seg); return c;
}

static int selftest(void) {
    const u64 L = 10000000ULL;
    double t0 = now();
    int fails = 0;
    /* simple sieves: composite flags up to S, squarefree flags up to L */
    const u64 S = 20000000ULL;
    unsigned char *isc = calloc(S + 1, 1);
    isc[0] = isc[1] = 1;
    for (u64 p = 2; p * p <= S; p++) if (!isc[p]) for (u64 q = p * p; q <= S; q += p) isc[q] = 1;
    unsigned char *sf = malloc(L + 1); memset(sf, 1, L + 1); sf[0] = 0;
    for (u64 p = 2; p * p <= L; p++) if (!isc[p]) for (u64 q = p * p; q <= L; q += p * p) sf[q] = 0;

    u64 bounds[3] = {1024, 8, 3};   /* normal bound, tiny bound (rho/MR do the work), none */
    for (int b = 0; b < 3; b++) {
        td_setup(bounds[b]);
        long bad = 0, badf = 0;
        #pragma omp parallel for schedule(dynamic, 65536) reduction(+:bad,badf)
        for (u64 n = 1; n <= L; n++) {
            if (is_squarefree(n) != sf[n]) bad++;
            u64 f[80]; int c = factor_full(n, f);
            u64 prod = 1; int okp = 1;
            for (int i = 0; i < c; i++) { prod *= f[i]; if (f[i] > S || isc[f[i]]) okp = 0; }
            if (prod != n || !okp) badf++;
            else {   /* squarefree from factor list must agree too */
                qsort(f, c, sizeof(u64), cmpu64);
                int s2 = 1; for (int i = 1; i < c; i++) if (f[i] == f[i - 1]) s2 = 0;
                if (s2 != sf[n]) badf++;
            }
        }
        printf("selftest sieve n<=%llu, trial bound %llu: squarefree mismatches %ld, bad factorisations %ld\n",
               (unsigned long long)L, (unsigned long long)bounds[b], bad, badf);
        fails += (bad || badf);
    }
    td_setup(1024);

    /* MR vs sieve primality up to S (odd n) */
    {
        long bad = 0;
        #pragma omp parallel for schedule(dynamic, 65536) reduction(+:bad)
        for (u64 n = 2; n <= S; n++) if (is_prime_mr(n) != !isc[n]) bad++;
        printf("selftest MR vs sieve n<=%llu: mismatches %ld\n", (unsigned long long)S, bad);
        fails += bad != 0;
    }
    /* known strong pseudoprimes (composite) */
    {
        static const u64 sp[] = {2047ULL, 1373653ULL, 25326001ULL, 3215031751ULL, 2152302898747ULL,
            3474749660383ULL, 341550071728321ULL, 3825123056546413051ULL, 4759123141ULL, 1122004669633ULL,
            561ULL, 41041ULL, 825265ULL, 321197185ULL, 5394826801ULL, 232250619601ULL, 9746347772161ULL};
        int bad = 0;
        for (unsigned i = 0; i < sizeof(sp) / sizeof(sp[0]); i++) {
            u64 n = sp[i], f[80]; int c = factor_full(n, f);
            u64 prod = 1; int okp = 1;
            for (int t = 0; t < c; t++) {
                prod *= f[t];
                for (u64 d = 2; d * d <= f[t]; d++) if (f[t] % d == 0) { okp = 0; break; }   /* trial-division primality */
            }
            if (is_prime_mr(n) || prod != n || !okp || c < 2) bad++;
        }
        printf("selftest strong pseudoprimes: %d failures\n", bad);
        fails += bad != 0;
    }
    /* random products of known primes */
    {
        /* pools: sieve primes < 2^24, primes near 1e14 and near 2^31, 2^40 (segmented sieve) */
        int np = 0; u64 *pr = malloc(sizeof(u64) * 1100000);
        for (u64 p = 2; p < (1u << 24); p++) if (!isc[p]) pr[np++] = p;
        u64 big14[2000], big31[2000], big40[2000];
        int n14 = seg_primes(100000000000000ULL - 200000, 400000, isc, S, big14, 2000);
        int n31 = seg_primes((1ULL << 31) - 30000, 60000, isc, S, big31, 2000);
        int n40 = seg_primes((1ULL << 40) - 60000, 120000, isc, S, big40, 2000);
        long tests = 0, bad = 0, nsf = 0;
        const u64 LIM14 = 200000000000000ULL, LIM62 = 1ULL << 62;
        for (long it = 0; it < 3000000; it++) {
            u64 lim = (it % 50 == 0) ? LIM62 : LIM14;
            u64 known[64]; int kc = 0; u64 n = 1;
            int mode = rnd() % 8;
            if (mode == 0) {                       /* single huge prime, maybe squared/times small */
                u64 p = big14[rnd() % n14]; known[kc++] = p; n = p;
            } else if (mode == 1) {                /* product of two ~2^31 primes (hard rho), or square */
                u64 p = big31[rnd() % n31], q = (rnd() & 1) ? p : big31[rnd() % n31];
                known[kc++] = p; known[kc++] = q; n = p * q; lim = LIM62;
            } else if (mode == 2) {                /* ~2^40 prime times small stuff */
                u64 p = big40[rnd() % n40]; known[kc++] = p; n = p;
            }
            int want = 1 + rnd() % 7;
            for (int t = 0; t < want * 4 && kc < 60; t++) {
                u64 p;
                int r = rnd() % 10;
                if (r < 3 && kc > 0) p = known[rnd() % kc];            /* repeat */
                else if (r < 6) p = pr[rnd() % 200];                   /* small */
                else p = pr[rnd() % np];                               /* up to 2^24 */
                if ((u128)n * p > lim) continue;
                n *= p; known[kc++] = p;
                if (kc >= want && (rnd() & 3) == 0) break;
            }
            if (n == 1) continue;
            qsort(known, kc, sizeof(u64), cmpu64);
            int ksf = 1; for (int t = 1; t < kc; t++) if (known[t] == known[t - 1]) ksf = 0;
            u64 f[80]; int c = factor_full(n, f);
            qsort(f, c, sizeof(u64), cmpu64);
            int same = (c == kc);
            for (int t = 0; same && t < c; t++) if (f[t] != known[t]) same = 0;
            if (!same || is_squarefree(n) != ksf) {
                if (bad < 5) printf("  random-product mismatch n=%llu\n", (unsigned long long)n);
                bad++;
            }
            tests++; nsf += ksf;
        }
        printf("selftest random products of known primes: %ld tests (%ld squarefree), %ld failures\n", tests, nsf, bad);
        fails += bad != 0;
        free(pr);
    }
    printf("selftest %s (%.1fs)\n", fails ? "FAILED" : "passed", now() - t0);
    free(isc); free(sf);
    return fails ? 1 : 0;
}

/* ------------------------------------------------------------------ */
/* squarefree cache for products uv+1                                   */
/* ------------------------------------------------------------------ */
static u64 *htab = NULL; static u64 hcap = 0, hcnt = 0;
static long long n_eval = 0, n_lookup = 0;
#define SFBIT (1ULL << 63)
static inline u64 hmix(u64 x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; return x; }
static void hgrow(void) {
    u64 oc = hcap, *ot = htab;
    hcap = oc ? oc * 2 : (1ULL << 22);
    htab = calloc(hcap, sizeof(u64));
    for (u64 i = 0; i < oc; i++) if (ot[i]) {
        u64 key = ot[i] & ~SFBIT, h = hmix(key) & (hcap - 1);
        while (htab[h]) h = (h + 1) & (hcap - 1);
        htab[h] = ot[i];
    }
    free(ot);
}
static int sf_cached(u64 x) {
    n_lookup++;
    if (2 * (hcnt + 1) > hcap) hgrow();
    u64 h = hmix(x) & (hcap - 1);
    while (htab[h]) {
        if ((htab[h] & ~SFBIT) == x) return (htab[h] & SFBIT) != 0;
        h = (h + 1) & (hcap - 1);
    }
    int s = is_squarefree(x); n_eval++;
    htab[h] = x | (s ? SFBIT : 0); hcnt++;
    return s;
}

/* ------------------------------------------------------------------ */
/* verifier                                                             */
/* ------------------------------------------------------------------ */
#define NOTIN INT_MIN
static long long K_, Nmax_;
static long long first_k = LLONG_MAX; static char first_reason[512] = "";
static long long cfirst[6]; static char creason[6][512];   /* per condition 0=format,1..4 */

static void fail_at(int cond, long long k, const char *msg) {
    if (k < cfirst[cond]) { cfirst[cond] = k; snprintf(creason[cond], sizeof creason[cond], "%s", msg); }
    if (k < first_k) { first_k = k; snprintf(first_reason, sizeof first_reason, "cond %d: %s", cond, msg); }
}
static inline long long kmin_of(long long n) { return n <= 31 ? 0 : (n - 31 + 24) / 25; }

static int verify(const char *dir) {
    double t0 = now(), t;
    char path[4096], msg[512];
    for (int c = 0; c < 6; c++) { cfirst[c] = LLONG_MAX; creason[c][0] = 0; }
    td_setup(1024);

    /* ---- global.txt ---- */
    snprintf(path, sizeof path, "%s/global.txt", dir);
    FILE *fg = fopen(path, "r");
    if (!fg) { printf("RESULT %s FAIL cannot open global.txt\n", dir); return 1; }
    char *line = NULL; size_t lcap = 0; ssize_t len;
    if ((len = getline(&line, &lcap, fg)) <= 0 || sscanf(line, "# Nmax %lld K %lld", &Nmax_, &K_) != 2) {
        printf("RESULT %s FAIL bad header\n", dir); return 1;
    }
    if (K_ < 0 || Nmax_ != 25 * K_ + 31) { printf("RESULT %s FAIL Nmax != 25K+31\n", dir); return 1; }
    long long K = K_, Nmax = Nmax_;
    printf("run %s: Nmax=%lld K=%lld\n", dir, Nmax, K);

    int *gidx = malloc(sizeof(int) * (Nmax + 1));
    for (long long i = 0; i <= Nmax; i++) gidx[i] = NOTIN;
    long long prev = 0, nlines = 0;
    while ((len = getline(&line, &lcap, fg)) > 0) {
        long long n, idx; char extra;
        if (line[0] == '\n') continue;
        if (sscanf(line, "%lld %lld %c", &n, &idx, &extra) != 2) {
            snprintf(msg, sizeof msg, "global.txt malformed line after n=%lld", prev);
            fail_at(0, kmin_of(prev + 1), msg); continue;
        }
        nlines++;
        if (n < 1 || n > Nmax) { snprintf(msg, sizeof msg, "global.txt n=%lld outside [1,Nmax]", n); fail_at(0, n < 1 ? 0 : K, msg); continue; }
        if (n <= prev) { snprintf(msg, sizeof msg, "global.txt not strictly increasing at n=%lld", n); fail_at(0, kmin_of(n), msg); }
        if (gidx[n] != NOTIN) { snprintf(msg, sizeof msg, "global.txt duplicate n=%lld", n); fail_at(0, kmin_of(n), msg); continue; }
        if (idx < INT_MIN + 1) idx = INT_MIN + 1;
        if (idx > INT_MAX) idx = INT_MAX;
        gidx[n] = (int)idx; prev = n;
    }
    fclose(fg);

    /* ---- candidates (own computation) & condition 1 ---- */
    t = now();
    unsigned char *cand = calloc(Nmax + 1, 1);
    #pragma omp parallel for schedule(dynamic, 16384)
    for (long long n = 1; n <= Nmax; n++) cand[n] = !is_squarefree((u64)n * n + 1);
    long long ncand = 0, c1miss = 0, c1extra = 0;
    for (long long n = 1; n <= Nmax; n++) {
        ncand += cand[n];
        int listed = gidx[n] != NOTIN;
        if (cand[n] && !listed) { c1miss++; snprintf(msg, sizeof msg, "candidate n=%lld missing from global.txt", n); fail_at(1, kmin_of(n), msg); }
        if (!cand[n] && listed) { c1extra++; snprintf(msg, sizeof msg, "non-candidate n=%lld listed in global.txt", n); fail_at(1, kmin_of(n), msg); }
    }
    int small_ok = 1;
    for (int n = 1; n <= 6 && n <= Nmax; n++) if (cand[n]) small_ok = 0;
    printf("  candidates computed: %lld (global lines %lld; missing %lld, extra %lld) in %.1fs; none <= 6: %s\n",
           ncand, nlines, c1miss, c1extra, now() - t, small_ok ? "yes" : "NO");
    if (!small_ok) fail_at(1, 0, "candidate <= 6");

    /* ---- counting identity ---- */
    {
        long long cnt = 0; int ok = 1;
        for (long long N = 1; N <= Nmax; N++) {
            if (N % 25 == 7) cnt++;
            if (N >= 7) { long long k = (N - 7) / 25; if (cnt != k + 1 || k > K) ok = 0; }
            else if (cnt != 0) ok = 0;
        }
        /* explicit endpoints of each plateau */
        for (long long k = 0; k <= K; k++) {
            long long lo = 25 * k + 7, hi = 25 * k + 31;
            if (hi / 25 + (hi % 25 >= 7) != k + 1 || lo / 25 + (lo % 25 >= 7) != k + 1) ok = 0;
        }
        printf("  counting identity #{n<=N: n=7 mod 25}=k+1 on [25k+7,25k+31], all N<=Nmax: %s\n", ok ? "ok" : "FAILED");
        if (!ok) fail_at(0, 0, "counting identity");
    }

    /* ---- condition 3: anchors ---- */
    for (long long m = 0; m <= K; m++) {
        long long a = 25 * m + 7;
        if (gidx[a] != m) { snprintf(msg, sizeof msg, "anchor %lld has global idx %d != %lld", a, gidx[a], m); fail_at(3, m, msg); }
    }

    /* ---- condition 2 (static part) ---- */
    /* required-override intervals for 18-mod-25 numbers: [j, end] */
    long long nreq = 0;
    long long *req_j = malloc(sizeof(long long) * (K + 1)), *req_end = malloc(sizeof(long long) * (K + 1));
    for (long long n = 1; n <= Nmax; n++) {
        if (gidx[n] == NOTIN) continue;
        long long g = gidx[n], km = kmin_of(n);
        long long end = (g < 0 || g > K) ? K : g - 1;     /* plateaus where global idx is not in [0,k] */
        if (end < km) continue;
        if (n % 25 == 18) { req_j[nreq] = (n - 18) / 25; req_end[nreq] = end; nreq++; }
        else { snprintf(msg, sizeof msg, "n=%lld (not overridable) has global idx %lld outside [0,%lld]", n, g, km); fail_at(2, km, msg); }
    }
    /* req_j is increasing in j already (n increasing) and kmin(x_j)=j */

    /* ---- classes ---- */
    long long *coff = calloc(K + 2, sizeof(long long));
    for (long long n = 1; n <= Nmax; n++) if (gidx[n] >= 0 && gidx[n] <= K) coff[gidx[n] + 1]++;
    for (long long m = 0; m <= K; m++) coff[m + 1] += coff[m];
    int *cmem = malloc(sizeof(int) * (coff[K + 1] + 1));
    { long long *fill = malloc(sizeof(long long) * (K + 1)); memcpy(fill, coff, sizeof(long long) * (K + 1));
      for (long long n = 1; n <= Nmax; n++) if (gidx[n] >= 0 && gidx[n] <= K) cmem[fill[gidx[n]]++] = (int)n;
      free(fill); }

    /* ---- condition 4, part (a): all pairs within each global class, members up to Nmax ---- */
    t = now();
    long long gpairs = 0, nbad = 0, badcap = 1024;
    long long (*bad)[3] = malloc(sizeof(long long[3]) * badcap);
    long long maxcls = 0;
    for (long long m = 0; m <= K; m++) {
        long long a = coff[m], b = coff[m + 1];
        if (b - a > maxcls) maxcls = b - a;
        for (long long i = a; i < b; i++) for (long long i2 = i + 1; i2 < b; i2++) {
            gpairs++;
            u64 u = cmem[i], v = cmem[i2];
            if (!sf_cached(u * v + 1)) {
                if (nbad == badcap) { badcap *= 2; bad = realloc(bad, sizeof(long long[3]) * badcap); }
                bad[nbad][0] = m; bad[nbad][1] = u; bad[nbad][2] = v; nbad++;
            }
        }
    }
    printf("  global-class pairs checked: %lld (max class size %lld), non-squarefree pairs: %lld, %.1fs\n",
           gpairs, maxcls, nbad, now() - t);

    /* ---- per-plateau pass: deltas ---- */
    t = now();
    snprintf(path, sizeof path, "%s/deltas.txt", dir);
    FILE *fd = fopen(path, "r");
    if (!fd) { fail_at(0, 0, "cannot open deltas.txt"); }
    int *ovr_at = malloc(sizeof(int) * (K + 1)), *ovr_to = malloc(sizeof(int) * (K + 1));
    for (long long j = 0; j <= K; j++) ovr_at[j] = -1;
    long long *oj = malloc(sizeof(long long) * (K + 2)), *om = malloc(sizeof(long long) * (K + 2));
    long long *act_j = malloc(sizeof(long long) * (K + 1)), *act_end = malloc(sizeof(long long) * (K + 1));
    long long nact = 0, rq = 0;
    long long pp_pairs = 0, tot_ovr = 0, maxovr = 0, nfailpl = 0;
    long long k = 0;
    for (k = 0; k <= K; k++) {
        long long N = 25 * k + 31;
        int plfail = 0;
        #define PFAIL(c, ...) do { snprintf(msg, sizeof msg, __VA_ARGS__); fail_at(c, k, msg); plfail = 1; } while (0)
        long long no = 0;
        len = fd ? getline(&line, &lcap, fd) : -1;
        if (len <= 0) { PFAIL(0, "no deltas line for plateau %lld", k); }
        else {
            char *p = line, *e;
            long long kk = strtoll(p, &e, 10);
            if (e == p || kk != k) PFAIL(0, "deltas line %lld has plateau number '%.20s'", k, line);
            p = e;
            while (*p == ' ' || *p == '\t') p++;
            if (strncmp(p, "FAIL", 4) == 0) PFAIL(0, "plateau %lld marked FAIL", k);
            else {
                while (*p && *p != '\n') {
                    long long j = strtoll(p, &e, 10);
                    if (e == p || *e != ':') { PFAIL(0, "malformed token in deltas line %lld", k); break; }
                    p = e + 1;
                    long long m = strtoll(p, &e, 10);
                    if (e == p) { PFAIL(0, "malformed token in deltas line %lld", k); break; }
                    p = e;
                    while (*p == ' ' || *p == '\t') p++;
                    if (j < 0 || j > k) { PFAIL(0, "override j=%lld outside [0,%lld]", j, k); continue; }
                    if (ovr_at[j] == k) { PFAIL(0, "duplicate override of x_%lld=%lld (double counting)", j, 25 * j + 18); continue; }
                    if (m < 0 || m > k) { PFAIL(2, "override x_%lld=%lld -> idx %lld outside [0,%lld]", j, 25 * j + 18, m, k); }
                    ovr_at[j] = (int)k; ovr_to[j] = (int)m;
                    oj[no] = j; om[no] = m; no++;
                }
            }
        }
        tot_ovr += no; if (no > maxovr) maxovr = no;

        /* cond 2: 18-numbers whose global idx is invalid at k must be overridden */
        while (rq < nreq && req_j[rq] == k) { act_j[nact] = req_j[rq]; act_end[nact] = req_end[rq]; nact++; rq++; }
        { long long w = 0;
          for (long long i = 0; i < nact; i++) {
              if (act_end[i] < k) continue;
              act_j[w] = act_j[i]; act_end[w] = act_end[i]; w++;
              long long j = act_j[i];
              if (ovr_at[j] != k) PFAIL(2, "x_%lld=%lld has global idx %d not in [0,%lld] and no override", j, 25 * j + 18, gidx[25 * j + 18], k);
          }
          nact = w; }

        /* cond 4 (a'): a bad global pair is a violation at k if both present, neither re-homed, class index <= k */
        for (long long i = 0; i < nbad; i++) {
            long long m = bad[i][0], u = bad[i][1], v = bad[i][2];
            if (u > N || v > N || m > k) continue;
            if (u % 25 == 18 && ovr_at[(u - 18) / 25] == k) continue;
            if (v % 25 == 18 && ovr_at[(v - 18) / 25] == k) continue;
            PFAIL(4, "class %lld: %lld*%lld+1 not squarefree", m, u, v);
        }

        /* cond 4 (b): each re-homed x_j against every member of its new class at plateau k */
        for (long long i = 0; i < no; i++) {
            long long m = om[i]; u64 u = 25 * oj[i] + 18;
            if (m < 0 || m > k) continue;          /* already a cond-2 failure */
            for (long long t2 = coff[m]; t2 < coff[m + 1]; t2++) {
                u64 v = cmem[t2];
                if ((long long)v > N) break;
                if (v % 25 == 18 && ovr_at[(v - 18) / 25] == k) continue;   /* re-homed away (or u itself) */
                pp_pairs++;
                if (!sf_cached(u * v + 1)) PFAIL(4, "plateau class %lld: re-homed %llu with member %llu: product+1 not squarefree",
                                                m, (unsigned long long)u, (unsigned long long)v);
            }
            for (long long i2 = i + 1; i2 < no; i2++) if (om[i2] == m) {
                u64 v = 25 * oj[i2] + 18;
                pp_pairs++;
                if (!sf_cached(u * v + 1)) PFAIL(4, "plateau class %lld: re-homed %llu with re-homed %llu: product+1 not squarefree",
                                                m, (unsigned long long)u, (unsigned long long)v);
            }
        }
        nfailpl += plfail;
    }
    if (fd) {
        long long extra = 0;
        while ((len = getline(&line, &lcap, fd)) > 0) if (line[0] != '\n') extra++;
        if (extra) { snprintf(msg, sizeof msg, "deltas.txt has %lld extra lines beyond K", extra); fail_at(0, K, msg); }
        fclose(fd);
    }
    printf("  plateau pass: %lld plateaus, %lld overrides (max %lld/plateau), re-homed pair checks %lld, %.1fs\n",
           K + 1, tot_ovr, maxovr, pp_pairs, now() - t);
    printf("  squarefree cache: %lld lookups, %lld distinct uv+1 factored\n", n_lookup, n_eval);
    const char *cn[5] = {"format", "cond1 candidates", "cond2 index range", "cond3 anchors", "cond4 pairs"};
    for (int c = 0; c < 5; c++)
        if (cfirst[c] != LLONG_MAX) printf("  first failure [%s]: plateau %lld: %s\n", cn[c], cfirst[c], creason[c]);
    if (first_k == LLONG_MAX)
        printf("RESULT %s PASS  plateaus 0..%lld (N=31..%lld)  global pairs %lld  plateau pairs %lld  time %.1fs\n",
               dir, K, Nmax, gpairs, pp_pairs, now() - t0);
    else
        printf("RESULT %s FAIL  first failing plateau %lld (N=%lld): %s  [plateau-loop failing plateaus: %lld]  time %.1fs\n",
               dir, first_k, 25 * first_k + 31, first_reason, nfailpl, now() - t0);
    return first_k == LLONG_MAX ? 0 : 1;
}

int main(int argc, char **argv) {
    if (argc >= 2 && !strcmp(argv[1], "selftest")) return selftest();
    if (argc >= 3 && !strcmp(argv[1], "verify")) return verify(argv[2]);
    if (argc >= 3 && !strcmp(argv[1], "sqf")) {      /* utility: squarefree status of numbers */
        td_setup(1024);
        for (int i = 2; i < argc; i++) {
            u64 n = strtoull(argv[i], 0, 10), f[80]; int c = factor_full(n, f);
            qsort(f, c, sizeof(u64), cmpu64);
            printf("%llu sqf=%d :", (unsigned long long)n, is_squarefree(n));
            for (int t = 0; t < c; t++) printf(" %llu", (unsigned long long)f[t]);
            printf("\n");
        }
        return 0;
    }
    fprintf(stderr, "usage: %s selftest | verify <dir> | sqf <n...>\n", argv[0]);
    return 2;
}
