"""Rota R2 do PREREGISTRO_C3.md: confirmacao independente de Prim_11 por geracao direta.
Le UMA parte da saida do genposetg (mesma divisao em 20 partes da investigacao auxiliar) e grava somas exatas
de n!/|Aut| * (-1)^B por tipo (0 paralelo, 1 serie, 2 raiz prima), e a soma total com sinal da parte,
que deve coincidir com a da parte auxiliar publicada (validacao).
Uso: genposetg 11 t q m x 20 | python h1b_C3_R2_parte.py 11 x  ->  h1b_C3_R2_n11_parte{x}.npz"""
import sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_N_classes import le_d6, fecho, aut
from h1b_modelo_rede import contagens
from h1b_paridade_explora import estrutura

if __name__ == '__main__':
    n, x = int(sys.argv[1]), int(sys.argv[2]); fat = math.factorial(n)
    soma = {0: 0, 1: 0, 2: 0}; peso = {0: 0, 1: 0, 2: 0}; total = 0; lote = []; auts = []
    def processa(lote, auts):
        P = np.array(lote, np.int64); A = np.array(auts, np.int64); L = fat // A
        N = contagens(P, n); s = np.where((n + N[:, 0] + N[:, 1]) % 2 == 0, 1, -1)
        t = estrutura(P, n)['tipo']
        for k in (0, 1, 2):
            m = t == k; soma[k] += int((L[m] * s[m]).sum()); peso[k] += int(L[m].sum())
    for linha in sys.stdin:
        linha = linha.strip()
        if not linha: continue
        C = fecho(le_d6(linha))
        if not np.all(np.triu(C, 1) == C):
            C = C.T; assert np.all(np.triu(C, 1) == C), 'saida nao e ordem parcial em ordem topologica'
        assert not np.any(C & C.T) and not C.diagonal().any(), 'saida nao e ordem parcial'
        lote.append((C.astype(np.int64) << np.arange(n)[:, None]).sum(0)); auts.append(aut(C)); total += 1
        if len(lote) == 100_000: processa(lote, auts); lote = []; auts = []
    if lote: processa(lote, auts)
    np.savez(f'h1b_C3_R2_n{n}_parte{x}.npz', soma=np.array([str(soma[k]) for k in (0, 1, 2)]),
             peso=np.array([str(peso[k]) for k in (0, 1, 2)]), total_classes=total)
    print(f'n={n} parte {x}: {total} classes; soma com sinal por tipo {soma}', flush=True)
