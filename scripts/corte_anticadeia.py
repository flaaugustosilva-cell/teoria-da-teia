"""Opcao 1 (17/11/2026): regra que vale em qualquer dimensao, sem parametro.
Guardar, em cada regiao, tantas vibracoes (de cada sinal) quantos nos tem a MAIOR ANTICADEIA da regiao
(o maior conjunto de nos sem relacao entre si: a "camada" mais larga, o equador).
Por que: num diamante 1+1 a maior anticadeia e a maior cadeia tem o mesmo tamanho medio (~2 raiz N),
entao a regra repete a da cadeia, que passou; em 2+1 a anticadeia cresce como N^(2/3), a escala das camadas.
Largura calculada pelo teorema de Dilworth: largura = N - emparelhamento maximo da relacao de ordem.
Uso: python corte_anticadeia.py 2      (1+1)   |   python corte_anticadeia.py 3 [a]   (2+1, a = tamanho de U)"""
import sys, numpy as np
from math import pi
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching
from ssee import sorteia, green
from corte_cadeia import altura, mantem

def largura(p):
    dt = p[None, :, 0] - p[:, None, 0]; dr2 = ((p[None, :, 1:] - p[:, None, 1:])**2).sum(2)
    C = csr_matrix((dt > 0) & (dt*dt > dr2))
    m = maximum_bipartite_matching(C, perm_type='column')
    return len(p) - int(np.sum(m >= 0))

def entropia(N, d, a, rng):
    p = sorteia(N, d, rng); A = green(p, d); A = A - A.T
    lam, V = np.linalg.eigh(1j*A)
    dentro = np.abs(p[:, 0]) + np.sqrt((p[:, 1:]**2).sum(1)) < a/2
    MO, MU = largura(p), largura(p[dentro]); NU = int(dentro.sum())
    MO, MU = min(MO, N//2), min(MU, NU//2)
    k = mantem(lam, MO); pos = k[lam[k] > 0]
    W = (V[:, pos]*lam[pos]) @ V[:, pos].conj().T; Dk = (V[:, k]*lam[k]) @ V[:, k].conj().T
    Wu = W[np.ix_(dentro, dentro)]; Du = Dk[np.ix_(dentro, dentro)]
    l2, V2 = np.linalg.eigh(Du); k2 = mantem(l2, MU); k2 = k2[np.abs(l2[k2]) > 1e-9*np.abs(l2).max()]
    mu = np.linalg.eigvals((V2[:, k2].conj().T @ Wu @ V2[:, k2]) / l2[k2][:, None]).real
    mu = mu[np.abs(mu) > 1e-12]
    return float(np.sum(mu*np.log(np.abs(mu)))), MO, MU, NU, altura(p, d)

if __name__ == '__main__':
    d = int(sys.argv[1])
    if d == 2:
        Ns = (500, 1000, 2000); S = []
        for N in Ns:
            r = [entropia(N, 2, 0.5, np.random.default_rng(100*N+s)) for s in range(3)]
            S.append(np.mean([x[0] for x in r]))
            print(f' N = {N}: S = {S[-1]:.3f}  largura O/U = {np.mean([x[1] for x in r]):.0f}/{np.mean([x[2] for x in r]):.0f}'
                  f'  (cadeia de O = {np.mean([x[4] for x in r]):.0f})', flush=True)
        print(f' inclinacao contra ln N: {np.polyfit(np.log(Ns), S, 1)[0]:.3f}  (regra da cadeia deu 0,251; teoria 0,167)')
    else:
        a = float(sys.argv[2]) if len(sys.argv) > 2 else 2**(-5/3); a3 = 0.218853; V = pi/12; Ns = (1000, 2000, 4000); S = []
        for N, reps in ((1000, 2), (2000, 2), (4000, 1)):
            r = [entropia(N, 3, a, np.random.default_rng(7*N+s)) for s in range(reps)]
            S.append(np.mean([x[0] for x in r])); mol = a3*(N/V)**(1/3)*pi*a
            print(f' N = {N}: S = {S[-1]:.2f}  largura O/U = {np.mean([x[1] for x in r]):.0f}/{np.mean([x[2] for x in r]):.0f}'
                  f' (U tem {np.mean([x[3] for x in r]):.0f} nos)  nats por molecula = {S[-1]/mol:.2f}', flush=True)
        print(f' S cresce como N^{np.polyfit(np.log(Ns), np.log(S), 1)[0]:.2f}  (lei de area: 0,33; volume: 1)')
