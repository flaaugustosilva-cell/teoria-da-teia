"""Que valor de c_d a regra da maior anticadeia escolhe? (18/11/2026)
Corte de Belenchia e outros: kappa = c_d * V^(2/d-1) * N^(1-1/d). A regra guarda tantos modos quanto a largura;
o kappa implicito e o autovalor na posicao da largura, e c_d = kappa / (V^(2/d-1) N^(1-1/d)).
Normalizacao de Green igual a deles: 2D C/2; 3D 1/(2 pi tau) (= a forma intrinseca deles); 4D raiz(rho)/(2 pi raiz 6) * ligacoes.
Em 2D o esperado e c_2 = 1/(4 pi) = 0,0796. Uso: python c_implicito.py"""
import numpy as np
from math import pi, gamma
from ssee import sorteia
from joelho import espectro
from largura_fluxo import ligacoes, largura_por_fluxo
def vol(d):  # diamante de altura 1
    return 2*(pi**((d-1)/2)/gamma((d-1)/2 + 1))*(0.5**d)/d
for d in (2, 3, 4):
    V = vol(d); cs = []
    for N in (1000, 2000, 4000):
        for s in range(2):
            p = sorteia(N, d, np.random.default_rng(100*N + 10*d + s)); lam = espectro(p, d)
            if d == 4: lam = lam*np.sqrt(N/V)/(2*pi*np.sqrt(6))
            r, c = ligacoes(p); w = largura_por_fluxo(N, r, c)
            cs.append((N, lam[w - 1]/(V**(2/d - 1)*N**(1 - 1/d))))
    cs = np.array(cs)
    print(f'd = {d}: c_d implicito = ' + ', '.join(f'{np.mean(cs[cs[:,0]==N,1]):.4f} (N={int(N)})' for N in (1000, 2000, 4000))
          + ('   [esperado em 2D: 0,0796]' if d == 2 else ''), flush=True)
