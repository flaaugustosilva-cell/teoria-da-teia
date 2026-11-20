"""phi_n exato em n = 9 e 10 (dados/h1b/PREREGISTRO_N9N10.md, commit 5c5f9a8) - classes nao rotuladas.
Le a saida do genposetg (diagramas de Hasse em digraph6, ordem topologica), faz o fecho transitivo, confere que e
ordem parcial, calcula B (Benincasa-Dowker 4D, eps = 1), altura e |Aut| (codigo proprio: gemeos + busca).
Uso: python h1b_N_classes.py ARQUIVO_D6 n  ->  h1b_N_n{n}.npz (pred em mascaras, B, h, aut) ; grava por partes."""
import sys, os, math, numpy as np
from h1b_B_exato import invariantes

def le_d6(linha):
    s = linha.strip(); assert s[0] == '&'; n = ord(s[1]) - 63; bits = []
    for ch in s[2:]:
        v = ord(ch) - 63; bits += [(v >> (5 - k)) & 1 for k in range(6)]
    A = np.array(bits[:n*n], bool).reshape(n, n); return A

def fecho(A):
    C = A.copy(); n = len(C)
    for k in range(n): C |= C[:, k][:, None] & C[k, :][None, :]
    return C

def aut(C):
    """|Aut| de uma ordem parcial: k! por classe de gemeos (mesmo passado e mesmo futuro) vezes os automorfismos
    do quociente que preservam o tamanho das classes, contados por busca com refinamento."""
    n = len(C); assin = {}
    for i in range(n): assin.setdefault((C[:, i].tobytes(), C[i, :].tobytes()), []).append(i)
    grupos = list(assin.values()); fator = 1
    for g in grupos: fator *= math.factorial(len(g))
    rep = [g[0] for g in grupos]; m = len(rep); tam = [len(g) for g in grupos]
    Q = C[np.ix_(rep, rep)]
    inv = [(tam[i], int(Q[:, i].sum()), int(Q[i, :].sum())) for i in range(m)]
    for _ in range(3):
        inv = [(inv[i], tuple(sorted(inv[j] for j in range(m) if Q[j, i])), tuple(sorted(inv[j] for j in range(m) if Q[i, j]))) for i in range(m)]
        mp_ = {v: r for r, v in enumerate(sorted(set(inv)))}; inv = [mp_[v] for v in inv]
    ordem = sorted(range(m), key=lambda i: sum(1 for j in range(m) if inv[j] == inv[i]))
    img = [-1]*m; usado = [False]*m; cont = 0
    def busca(k):
        nonlocal cont
        if k == m: cont += 1; return
        i = ordem[k]
        for j in range(m):
            if usado[j] or inv[j] != inv[i]: continue
            ok = True
            for kk in range(k):
                a = ordem[kk]; b = img[a]
                if Q[a, i] != Q[b, j] or Q[i, a] != Q[j, b]: ok = False; break
            if ok:
                img[i] = j; usado[j] = True; busca(k + 1); usado[j] = False; img[i] = -1
    busca(0)
    return fator*cont

if __name__ == '__main__':
    arq, n = sys.argv[1], int(sys.argv[2]); saida = f'h1b_N_n{n}.npz'; PARTE = 100_000
    linhas = open(arq).read().split()
    P = np.zeros((len(linhas), n), np.int64); AUT = np.zeros(len(linhas), np.int64)
    for p, l in enumerate(linhas):
        C = fecho(le_d6(l))
        if not (np.all(np.triu(C, 1) == C)):      # ordem topologica: so arcos de indice menor para maior
            C = C.T
            assert np.all(np.triu(C, 1) == C), f'saida {p} nao e ordem parcial em ordem topologica'
        assert not np.any(C & C.T) and not C.diagonal().any(), f'saida {p} nao e ordem parcial'
        P[p] = (C.astype(np.int64) << np.arange(n)[:, None]).sum(0)   # mascara de antecessores
        AUT[p] = aut(C)
        if (p + 1) % PARTE == 0: print(f'  n={n}: {p+1}/{len(linhas)}', flush=True)
    Cs = ((P[:, None, :] >> np.arange(n)[None, :, None]) & 1).astype(bool)
    B, h = [], []
    for a in range(0, len(P), 200_000):
        b_, h_ = invariantes(P[a:a+200_000], Cs[a:a+200_000], n); B.append(b_); h.append(h_)
    B = np.concatenate(B); h = np.concatenate(h)
    np.savez_compressed(saida, pred=P, B=B, h=h, aut=AUT)
    print(f'n={n}: {len(P)} classes; altura >= 3: {int((h >= 3).sum())}; soma n!/|Aut| = {sum(math.factorial(n)//int(a) for a in AUT)}', flush=True)
