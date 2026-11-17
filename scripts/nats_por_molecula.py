"""Quantos nats de entropia um campo escalar deixa por molecula de horizonte, em 2+1 dimensoes.
Diamante U com volume 1/4 do diamante O (a = 2^(-5/3), como em Belenchia e outros).
Moleculas na borda de U (circulo de raio a/2): a3 * rho^(1/3) * comprimento, a3 = 0,218853
(Barton e outros; conferido por nos em 16/11). Varre a constante c do corte.
Uso: python nats_por_molecula.py"""
import numpy as np
from math import pi
from ssee import entropia
a = 2**(-5/3); a3 = 0.218853; V = pi/12
cs = (0.0, 0.02, 0.04, 0.08, 0.16)
print('Lei de area pede S proporcional a N^(1/3).')
print('    N   N_U  moleculas | nats por molecula para c = ' + '  '.join(f'{c:5.2f}' for c in cs[1:]) + ' | S sem corte')
tab = []
for N, reps in ((1000, 3), (2000, 3), (4000, 2)):
    acc = {c: [] for c in cs}
    for s in range(reps):
        o, NU = entropia(N, 3, a, cs, np.random.default_rng(7*N+s))
        for c in cs: acc[c].append(o[c])
    mol = a3*(N/V)**(1/3)*pi*a
    S = {c: np.mean(acc[c]) for c in cs}; tab.append((N, S))
    print(f'{N:5d} {NU:5d}   {mol:6.1f}   |                          ' + '  '.join(f'{S[c]/mol:5.2f}' for c in cs[1:]) + f' | {S[0.0]:7.1f}', flush=True)
Ns = np.array([t[0] for t in tab])
for c in cs:
    Sv = np.array([t[1][c] for t in tab])
    if np.all(Sv > 0): print(f'c = {c:4.2f}: S cresce como N^{np.polyfit(np.log(Ns), np.log(Sv), 1)[0]:.2f}')
