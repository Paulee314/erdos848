# Type (residue-class) stability analysis for Erdos 848.
# A type is a residue mod M. Pairs of types are "auto" if st+1 is divisible by 4, 9 or 25 (the prime squares dividing M).
# Upper bound on the density of A in type s:
#   s in C (s = 7,18 mod 25; a^2+1 automatically divisible by 25): 1 if every type present is auto with s, else K2'
#   s not in C: J' (needs p^2 | a^2+1 with p>=13 AND, with another element b, q^2 | ab+1 for q not dividing M; worst-case b)
import json, sys, pulp
c=json.load(open('consts.json'))
M=int(sys.argv[1])
mods=[m for m in (4,9,25) if M%m==0]
K2=c['K2_9'] if M%9==0 else c['K2']; J=c['J_9'] if M%9==0 else c['J']
T=range(M)
inC=lambda s: s%25 in (7,18)
cls=lambda s: 7 if s%25==7 else (18 if s%25==18 else None)
def auto(s,t): return any((s*t+1)%m==0 for m in mods)
C=[s for s in T if inC(s)]; NC=[s for s in T if not inC(s)]
# group non-C types by their residues mod the auto moduli other than 25 (25 never glues C with non-C)
key=lambda t: tuple(t%m for m in mods if m!=25)
groups={}
for t in NC: groups.setdefault(key(t),[]).append(t)
prob=pulp.LpProblem('f',pulp.LpMaximize)
x={s:pulp.LpVariable(f'x{s}',cat='Binary') for s in C}
z={s:pulp.LpVariable(f'z{s}',cat='Binary') for s in C}
y={g:pulp.LpVariable('y'+'_'.join(map(str,g)),cat='Binary') for g in groups}
prob+= pulp.lpSum(z[s]+K2*(x[s]-z[s]) for s in C) + pulp.lpSum(J*len(groups[g])*y[g] for g in groups)
for s in C:
    prob+= z[s]<=x[s]
    for t in C:
        if t!=s and not auto(s,t): prob+= z[s]+x[t]<=1
    for g,ts in groups.items():
        if not auto(s,ts[0]): prob+= z[s]+y[g]<=1
# exclude A inside a single 25-class: need something outside the 7-class AND something outside the 18-class
prob+= pulp.lpSum(x[s] for s in C if cls(s)!=7)+pulp.lpSum(y.values())>=1
prob+= pulp.lpSum(x[s] for s in C if cls(s)!=18)+pulp.lpSum(y.values())>=1
prob.solve(pulp.PULP_CBC_CMD(msg=0))
val=pulp.value(prob.objective)/M
S1=[s for s in C if z[s].value()>0.5]; Sk=[s for s in C if x[s].value()>0.5 and z[s].value()<0.5]
print(f"M={M}: worst mixed configuration has density <= {val:.4f}; margin to 1/25 = {0.04-val:.4f}")
print("  full-density types:",S1,"\n  reduced C types:",Sk,"\n  non-C groups used:",sum(1 for g in groups if y[g].value()>0.5),"of",len(groups))
