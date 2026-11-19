"""E1 - diagnosticos pre-registrados: tamanho do automorfismo por gemeos e inclinacoes de L.
Cota inferior: |Aut| >= produto de k! sobre as classes de gemeos (mesmo passado e mesmo futuro)."""
import math, csv, numpy as np
from e1_comum import sorteia_diamante, causal
NS = (40, 80, 120, 160); SEMENTE = 20261119; MD = 2000
print('ln|Aut| (cota inferior por gemeos) e elementos isolados, primeiras 2000 teias de cada n (mesma semente):')
for n in NS:
    rng = np.random.default_rng([SEMENTE, n]); la = []; iso = []
    for _ in range(MD):
        C = causal(sorteia_diamante(n, rng)); assin = np.concatenate([C, C.T], 1)
        _, cont = np.unique(assin, axis=0, return_counts=True)
        la.append(sum(math.lgamma(k + 1) for k in cont)); iso.append(int(np.sum(~C.any(0) & ~C.any(1))))
    la = np.array(la); print(f' n={n:3d}: ln|Aut| media {la.mean():6.2f}  max {la.max():6.2f} | isolados media {np.mean(iso):5.2f}')
r = list(csv.DictReader(open('e1_resultados.csv')))
print('\nCrescimento de ln|Z_ruim| (por n e por n ln n) e inclinacao de L:')
for x in ('0.832', '5.0', '6.0', '7.0', '8.0', '9.0'):
    rows = [d for d in r if d['x'] == x]; n = np.array([float(d['n']) for d in rows])
    lz = np.array([float(d['lnZ_ruim']) for d in rows]); L = np.array([float(d['L']) for d in rows])
    dec = all(L[i] > L[i+1] for i in range(3))
    print(f' x={x:>5}: lnZ/n = ' + ' '.join(f'{v:6.3f}' for v in lz/n) + ' | lnZ/(n ln n) = ' + ' '.join(f'{v:6.3f}' for v in lz/(n*np.log(n)))
          + f' | inclinacao dL/dn = {np.polyfit(n, L, 1)[0]:7.3f} | L<0 em todos: {bool(np.all(L < 0))} | decrescente: {dec}')
