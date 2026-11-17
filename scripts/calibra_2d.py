"""Calibracao em 1+1: com o corte de Sorkin-Yazdi (c = 1/4pi), S deve crescer como (1/3) ln(L/eps),
isto e, inclinacao ~ 1/6 contra ln N (eps ~ N^(-1/2)). Sem corte: lei de volume (cresce como N).
Uso: python calibra_2d.py"""
import numpy as np
from math import pi
from ssee import entropia
cs = (0.0, 1/(4*pi), 2/(4*pi))
res = {c: [] for c in cs}; Ns = (500, 1000, 2000)
print('   N   N_U   S sem corte   S(c=1/4pi)   S(c=2/4pi)   (media de 3)')
for N in Ns:
    acc = {c: [] for c in cs}
    for s in range(3):
        o, NU = entropia(N, 2, 0.5, cs, np.random.default_rng(100*N+s))
        for c in cs: acc[c].append(o[c])
    for c in cs: res[c].append(np.mean(acc[c]))
    print(f'{N:5d} {NU:5d}   {np.mean(acc[0.0]):9.2f}   {np.mean(acc[cs[1]]):9.3f}   {np.mean(acc[cs[2]]):9.3f}', flush=True)
for c in cs[1:]:
    b = np.polyfit(np.log(Ns), res[c], 1)[0]
    print(f'inclinacao contra ln N com c = {c*4*pi:.0f}/(4 pi): {b:.3f}   (esperado 1/6 = 0,167)')
b = np.polyfit(np.log(Ns), np.log(res[0.0]), 1)[0]
print(f'sem corte: S cresce como N^{b:.2f}   (lei de volume: 1)')
