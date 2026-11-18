"""Maior anticadeia (largura) por fluxo minimo, usando so as LIGACOES (relacoes sem ninguem no meio).
Teorema de Dilworth: largura = menor numero de cadeias que cobrem todos os nos (cadeias podem pular nos
e repetir nos). Formulacao: fluxo com piso 1 em cada no; parte-se de N cadeias de um no so e funde-se
o maximo possivel por um fluxo maximo de t para s no grafo residual:
  t -> saida(u) [cap 1];  saida(u) -> entrada(v) por ligacao u -> v [cap N];
  entrada(v) -> saida(v) [cap N] (permite passar por v e reusa-lo);  entrada(v) -> s [cap 1].
largura = N - fluxo maximo. Mesmo resultado do emparelhamento, com muito menos arestas.
Uso: python largura_fluxo.py   (compara com o metodo antigo e mede o tempo)"""
import time, numpy as np
from scipy.sparse import csr_matrix, coo_matrix
from scipy.sparse.csgraph import maximum_flow

def ligacoes(p, bloco=4000):
    """matriz esparsa das ligacoes; C em float32 por blocos, ligacao = relacao sem elemento entre."""
    N = len(p); o = np.argsort(p[:, 0]); q = p[o]
    C = np.zeros((N, N), np.float32)
    for i0 in range(0, N, bloco):
        a = q[i0:i0+bloco]; dt = q[None, :, 0] - a[:, None, 0]
        dr2 = ((q[None, :, 1:] - a[:, None, 1:])**2).sum(2); C[i0:i0+bloco] = (dt > 0) & (dt*dt > dr2)
    linhas, colunas = [], []
    for i0 in range(0, N, bloco):
        meio = C[i0:i0+bloco] @ C                      # quantos elementos entre i e j
        r, c = np.nonzero((C[i0:i0+bloco] > 0) & (meio == 0)); linhas.append(r + i0); colunas.append(c)
    r = np.concatenate(linhas); c = np.concatenate(colunas)
    return o[r], o[c]

def largura_por_fluxo(N, r, c):
    t, s = 0, 1; sai = 2 + np.arange(N); ent = 2 + N + np.arange(N)
    orig = np.concatenate([np.full(N, t), sai[r], ent, ent])
    dest = np.concatenate([sai, ent[c], sai, np.full(N, s)])
    cap = np.concatenate([np.ones(N), np.full(len(r), N), np.full(N, N), np.ones(N)]).astype(np.int32)
    G = csr_matrix(coo_matrix((cap, (orig, dest)), shape=(2*N + 2, 2*N + 2)))
    return N - maximum_flow(G, t, s, method='dinic').flow_value

if __name__ == '__main__':
    from ssee import sorteia
    from grande import monta, largura_de
    for N in (1000, 2000, 4000, 8000):
        p = sorteia(N, 3, np.random.default_rng(N))
        t0 = time.time(); r, c = ligacoes(p); t1 = time.time(); w2 = largura_por_fluxo(N, r, c); t2 = time.time()
        A, C = monta(p); t3 = time.time(); w1 = largura_de(C); t4 = time.time()
        print(f'N = {N}: emparelhamento = {w1} ({t4-t3:.1f} s) | fluxo = {w2} (ligacoes {t1-t0:.1f} s + fluxo {t2-t1:.1f} s); '
              f'{len(r)} ligacoes contra {C.nnz} relacoes', flush=True)
