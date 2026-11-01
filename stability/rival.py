# For Erdos 848: compare the 7 mod 25 set with the best set NOT inside a single class (7 or 18 mod 25).
import sys, time, networkx as nx, json
def sqfree(m):
    d=2
    while d*d<=m:
        if m%(d*d)==0: return False
        if m%d==0: m//=d
        d+=1 if d==2 else 2
    return True
Nmax=int(sys.argv[1]); step=int(sys.argv[2])
V=[a for a in range(1,Nmax+1) if not sqfree(a*a+1)]
adj={a:set() for a in V}
for i,a in enumerate(V):
    for b in V[:i]:
        if not sqfree(a*b+1): adj[a].add(b); adj[b].add(a)
def omega(S):
    if not S: return 0,[]
    H=nx.Graph(); H.add_nodes_from(S)
    S=list(S)
    for i,a in enumerate(S):
        for b in S[:i]:
            if b in adj[a]: H.add_edge(a,b)
    c,w=nx.max_weight_clique(H,weight=None); return w,c
out=[]
for N in range(step,Nmax+1,step):
    t=time.time()
    VN=[a for a in V if a<=N]; C7=[a for a in VN if a%25==7]; C18=[a for a in VN if a%25==18]
    best=(0,None)
    for v in VN:
        if v%25 in (7,18): continue
        w,c=omega({u for u in adj[v] if u<=N}); 
        if w+1>best[0]: best=(w+1,sorted(c+[v]))
    for a in C7:
        for b in C18:
            if b in adj[a]:
                w,c=omega({u for u in adj[a]&adj[b] if u<=N})
                if w+2>best[0]: best=(w+2,sorted(c+[a,b]))
    a7=len(C7)
    out.append({"N":N,"a7":a7,"rival":best[0],"example":best[1]})
    print(N,a7,best[0],best[1],f"{time.time()-t:.1f}s",flush=True)
json.dump(out,open(f"rival_{Nmax}.json","w"))
