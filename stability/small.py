import sys, time, networkx as nx
from sympy import factorint
Nmax=int(sys.argv[1])
def sqfree(m):
    d=2
    while d*d<=m:
        if m%(d*d)==0: return False
        if m%d==0: m//=d
        d+=1 if d==2 else 2
    return True
V=[a for a in range(1,Nmax+1) if not sqfree(a*a+1)]
G=nx.Graph(); 
t=time.time(); bad=[]
for i,a in enumerate(V):
    G.add_node(a)
    for b in V[:i]:
        if not sqfree(a*b+1): G.add_edge(a,b)
    # check N=a (only changes when a vertex is added)
    w=len(nx.max_weight_clique(G,weight=None)[0])
    a7=sum(1 for n in range(1,a+1) if n%25==7)
    if w>a7: bad.append((a,w,a7))
print(f"N<={Nmax}: {len(V)} candidate vertices, {G.number_of_edges()} edges, violations={bad[:10]} ({time.time()-t:.1f}s)")
