"""Investigacao auxiliar em n = 11 (dados/h1b/PREREGISTRO_N11_AUX.md, commit 4a45931): processa UMA parte da saida do
genposetg, lida da entrada padrao, e grava so o agregado exato em inteiros:
para cada (B, altura >= 3, conexa): soma de n!/|Aut| e numero de classes.
Uso: genposetg n t m x y | python h1b_N11_parte.py n x  ->  h1b_N11_n{n}_parte{x}.npz"""
import sys, math, numpy as np
from collections import defaultdict
from h1b_N_classes import le_d6, fecho, aut
from h1b_B_exato import invariantes

def conexa(C):
    n = len(C); G = C | C.T; vis = {0}; pilha = [0]
    while pilha:
        i = pilha.pop()
        for j in np.nonzero(G[i])[0]:
            if j not in vis: vis.add(int(j)); pilha.append(int(j))
    return len(vis) == n

if __name__ == '__main__':
    n, x = int(sys.argv[1]), int(sys.argv[2]); fat = math.factorial(n)
    agg = defaultdict(lambda: [0, 0]); total_cl = 0; lote = []
    def processa(lote):
        P = np.array([p for p, _, _ in lote], np.int64)
        Cs = ((P[:, None, :] >> np.arange(n)[None, :, None]) & 1).astype(bool)
        B, h = invariantes(P, Cs, n)
        for (p, a, c), b, hh in zip(lote, B, h):
            r = agg[(int(b), int(hh >= 3), int(c))]; r[0] += fat // a; r[1] += 1
    for linha in sys.stdin:
        linha = linha.strip()
        if not linha: continue
        C = fecho(le_d6(linha))
        if not np.all(np.triu(C, 1) == C):
            C = C.T; assert np.all(np.triu(C, 1) == C), 'saida nao e ordem parcial em ordem topologica'
        assert not np.any(C & C.T) and not C.diagonal().any(), 'saida nao e ordem parcial'
        p = (C.astype(np.int64) << np.arange(n)[:, None]).sum(0)
        lote.append((p, aut(C), conexa(C))); total_cl += 1
        if len(lote) == 100_000: processa(lote); lote = []
    if lote: processa(lote)
    ch = np.array(sorted(agg), np.int64); val = [agg[tuple(k)] for k in ch]
    np.savez(f'h1b_N11_n{n}_parte{x}.npz', chaves=ch, peso=np.array([str(v[0]) for v in val]), classes=np.array([v[1] for v in val], np.int64), total_classes=total_cl)
    print(f'n={n} parte {x}: {total_cl} classes; soma n!/|Aut| = {sum(v[0] for v in val)}', flush=True)
