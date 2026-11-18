# Soma exata de exp(iS) sobre teias de 3 camadas (a,b,c) com a acao de ligacoes
# S = mu*(n - ligacoes). Camada 2: cada no tem >=1 antecessor na 1; camada 3: >=1 na 2.
# Relacoes 1->3 nao implicadas sao livres (cada uma e uma ligacao).
import itertools, numpy as np, sys
def Z3(a,b,c,mu):
    w=np.exp(-1j*mu); subs=[s for s in range(1,2**a)]
    pc=[bin(s).count('1') for s in range(2**a)]
    tot=0
    for D in itertools.product(subs,repeat=b):
        f=0
        for P in range(1,2**b):
            u=0;k=0
            for y in range(b):
                if P>>y&1: u|=D[y];k+=1
            f+=w**k*(1+w)**(a-pc[u])
        tot+=w**sum(pc[d] for d in D)*f**c
    return np.exp(1j*mu*(a+b+c))*tot
def Z2(a,b,mu):
    w=np.exp(-1j*mu); return np.exp(1j*mu*(a+b))*((1+w)**a-1)**b
a,b,c=map(int,sys.argv[1:4]); n=a+b+c
z30=Z3(a,b,c,0).real; z20=Z2(n//2,n-n//2,0).real
for beta in np.arange(0.2,3.1,0.15):
    mu=2*beta
    r3=np.log(abs(Z3(a,b,c,mu))/z30)/n; r2=np.log(abs(Z2(n//2,n-n//2,mu))/z20)/n
    print(f"{beta:.2f}  3cam {r3:7.3f}   2cam {r2:7.3f}")
