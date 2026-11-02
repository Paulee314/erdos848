import clique_check as cc, numpy as np, sys
N=int(sys.argv[1])
nsf=cc.nonsqfree_table(N*N+1)
V=[n for n in range(1,N+1) if nsf[n*n+1]]
pos={v:i for i,v in enumerate(V)}
adj={i:sum(1<<j for j,b in enumerate(V) if j!=i and nsf[a*b+1]) for i,a in enumerate(V)}
best=(0,None)
for v in V:
    if v%25 in (7,18): continue
    s,B=cc.max_clique(adj,adj[pos[v]])
    if s+1>best[0]: best=(s+1,sorted([V[k] for k in range(len(V)) if B>>k&1]+[v]))
cl=best[1]
print(best[0], best[0]/N)
nonC=[x for x in cl if x%25 not in (7,18)]
print("nonC elements:",nonC, [ (x%4,x%9,x%25) for x in nonC])
print("C elements by (class, mod4):", {(c,m):sum(1 for x in cl if x%25==c and x%4==m) for c in (7,18) for m in range(4)})
print("C elements by (class, mod4, mod9):", sorted({(x%25,x%4,x%9) for x in cl if x%25 in (7,18)}))
