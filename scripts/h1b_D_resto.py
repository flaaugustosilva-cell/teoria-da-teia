"""EXPLORATORIO (21/11/2026): o resto do carater D (ordens sem menor elemento e sem ponto isolado), por tipo.
w_D = s(P)(-1)^D(P). (D) w_D(P + {top}) = -s(P)(-1)^(D+M+U)  -> parte 'maior elemento' = -n * A_(n-1)^[(0,1,1,1)].
Uso: python h1b_D_resto.py PASTA"""
import sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_paridade_explora import estrutura
from h1b_soma_ordinal import perfis
pasta = sys.argv[1]; Dn = {}; Ach = {}
print(' n | D_n | menor | isolado | maior sem menor (= -n A^[(0,1,1,1)]_(n-1)?) | paralelo s/ isolado | serie s/ extremos | raiz prima | sinal (-1)^n de cada')
for n in range(1, 11):
    d = np.load(f'{pasta}/h1b_N_n{n}.npz'); L = math.factorial(n) // d['aut'].astype(np.int64)
    s = np.where(d['B'] % 2 == 0, 1, -1).astype(np.int64); E = estrutura(d['pred'], n); u, dd = perfis(d['pred'], n)
    w = L * s * (-1) ** (dd[:, 1] % 2); pc = np.array([bin(x).count('1') for x in range(1 << n)])
    bot = (pc[E['suc']] == n - 1).any(1); top = (pc[E['pred']] == n - 1).any(1); iso = E['iso'] > 0; t = E['tipo']
    Dn[n] = int(w.sum()); Ach[n] = int((L * s * (-1) ** ((dd[:, 1] + E['maxi'] + u[:, 1]) % 2)).sum())
    if n < 4: continue
    resto = ~bot & ~iso & ~top
    partes = [int(w[bot].sum()), int(w[iso].sum()), int(w[top & ~bot].sum()), int(w[resto & (t == 0)].sum()),
              int(w[resto & (t == 1)].sum()), int(w[resto & (t == 2)].sum())]
    prev = -n * Ach[n - 1]
    sg = ''.join('+' if x * (-1) ** n > 0 else ('0' if x == 0 else '-') for x in partes)
    print(f' {n:2d} | {Dn[n]:+d} | ' + ' | '.join(f'{x:+d}' for x in partes[:2]) + f' | {partes[2]:+d} ({partes[2] == prev}) | '
          + ' | '.join(f'{x:+d}' for x in partes[3:]) + f' | {sg}')
