"""PREREGISTRO_D11.md: geracao independente de n = 11 (todas as ordens) para o teste de coerencia dimensional.
Le UMA parte da saida do genposetg (mesma divisao em 20 partes) e grava, por classe e na ordem de saida:
B (acao de 4 dimensoes), aut, N0..N3, R (pares comparaveis), h (altura).
Uso: genposetg N t q m x 20 | python h1b_D11_parte.py N x PASTA_SAIDA"""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_N_classes import le_d6, fecho, aut
from h1b_modelo_rede import contagens

if __name__ == '__main__':
    n, x, saida = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    pop = np.array([bin(v).count('1') for v in range(1 << n)], np.int64)
    Bs, As, Ns, Rs, Hs = [], [], [], [], []; lote = []; auts = []
    def processa(lote, auts):
        P = np.array(lote, np.int64); N = contagens(P, n)
        Bs.append((n + N @ np.array([-1, 9, -16, 8])).astype(np.int16)); As.append(np.array(auts, np.int64))
        Ns.append(N.astype(np.int8)); Rs.append(pop[P].sum(1).astype(np.int8))
        h = np.ones((len(P), n), np.int64)                       # ordem topologica: predecessores tem indice menor
        for j in range(n):
            for i in range(j):
                h[:, j] = np.where(((P[:, j] >> i) & 1).astype(bool), np.maximum(h[:, j], h[:, i] + 1), h[:, j])
        Hs.append(h.max(1).astype(np.int8))
    for linha in sys.stdin:
        linha = linha.strip()
        if not linha: continue
        C = fecho(le_d6(linha))
        if not np.all(np.triu(C, 1) == C):
            C = C.T; assert np.all(np.triu(C, 1) == C), 'saida nao e ordem parcial em ordem topologica'
        assert not np.any(C & C.T) and not C.diagonal().any(), 'saida nao e ordem parcial'
        lote.append((C.astype(np.int64) << np.arange(n)[:, None]).sum(0)); auts.append(aut(C))
        if len(lote) == 100_000: processa(lote, auts); lote = []; auts = []
    if lote: processa(lote, auts)
    np.savez_compressed(f'{saida}/h1b_D11_n{n}_parte{x}.npz', B=np.concatenate(Bs), aut=np.concatenate(As),
                        N=np.concatenate(Ns), R=np.concatenate(Rs), h=np.concatenate(Hs))
    print(f'n={n} parte {x}: {sum(len(b) for b in Bs)} classes', flush=True)
