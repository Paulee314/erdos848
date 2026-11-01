# Rigorous density constants for Erdos 848 (products over primes up to P, tails bounded).
import numpy as np, itertools, json
P=20_000_000
s=np.ones(P+1,bool); s[:2]=False
for i in range(2,int(P**.5)+1):
    if s[i]: s[i*i::i]=False
pr=np.nonzero(s)[0].astype(np.float64)
tail=1.0/(P-1)            # sum_{n>P} 1/n^2 < 1/(P-1)
def prod(mask,c):         # prod over primes in mask of (1-c/p^2); returns (lo,hi) for the infinite product over the same congruence family
    v=np.exp(np.sum(np.log1p(-c/pr[mask]**2)))
    return v*(1-c*tail), v
diag=(pr%4==1)&(pr>=13); m3=(pr%4==3); odd_no5=(pr>=3)&(pr!=5); all_no5=(pr!=5)
Pd2=prod(diag,2); Pd1=prod(diag,1); Q=prod(m3,1); Q3=prod(m3&(pr>3),1)
K1=1-Pd2[0]                      # density of D': p^2 | a^2+1 for some p=1 mod 4, p>=13   (upper bound)
K2=1-prod(odd_no5,1)[0]          # density of P': q^2 | ab+1, q not in {2,5}, worst case b
K3=1-prod(all_no5,1)[0]          # q not 5 (q=2 allowed)
# J = dens(D' and P') with worst-case b (coprime to everything, b's own root class mod l^2 at every diag prime)
J=(1-Pd2[0]) - Q[1]*(Pd1[1]-Pd2[0]) if False else None
# rigorous upper bound: J = K1 - Q*(Pd1-Pd2); use upper K1, lower Q, lower (Pd1-Pd2)
J = (1-Pd2[0]) - Q[0]*(Pd1[0]-Pd2[1])
# versions excluding 3 as well (for M divisible by 9)
K2_9=1-prod(odd_no5&(pr>3),1)[0]
J_9=(1-Pd2[0]) - Q3[0]*(Pd1[0]-Pd2[1])
out=dict(K1=K1,K2=K2,K3=K3,J=J,K2_9=K2_9,J_9=J_9)
for k,v in out.items(): print(f"{k:6s} {v:.6f}")
json.dump(out,open('consts.json','w'))
print("\nSawhney's cases (bound on |A|/N, margin to 1/25):")
cases={"1a A* has even elt":23/25*K1+2/25*K2,
       "1b-i A* odd, A7,A18 odd":0.5*23/25*K1+1/50+K2/50,
       "1b-ii A* odd, even elt in A7/A18":0.5*23/25*K1+K3/25+K2/25,
       "2a A* empty, A7 & A18 nonempty":2/25*K3}
for k,v in cases.items(): print(f"  {k:36s} {v:.4f}  margin {0.04-v:.4f}")
