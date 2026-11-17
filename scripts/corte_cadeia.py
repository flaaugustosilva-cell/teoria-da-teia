"""Reflexao 11, refinada (17/11/2026): "contam tantas vibracoes quantos nos cabem na maior cadeia".
Em cada regiao (diamante O e diamante U) mantem-se os H modos de maior |lambda| de cada sinal,
H = altura (maior cadeia) da propria regiao, medida na teia. Nenhum parametro livre.
Teste 1+1: S deve crescer como logaritmo (inclinacao ~1/6 contra ln N).
Teste 2+1: lei de area pede S ~ N^(1/3); mede nats por molecula de horizonte.
Uso: python corte_cadeia.py"""
import numpy as np
from math import pi
from ssee import sorteia, green

def altura(p, d):
    o = np.argsort(p[:, 0]); q = p[o]
    dt = q[None, :, 0] - q[:, None, 0]; dr2 = ((q[None, :, 1:] - q[:, None, 1:])**2).sum(2)
    C = (dt > 0) & (dt*dt > dr2); h = np.ones(len(q), int)
    for j in range(len(q)):
        a = C[:j, j]
        if a.any(): h[j] = 1 + h[:j][a].max()
    return int(h.max())

def mantem(lam, H):
    """indices dos H maiores positivos e H mais negativos"""
    o = np.argsort(lam); return np.concatenate([o[:H], o[-H:]])

def entropia(N, d, a, rng):
    p = sorteia(N, d, rng); A = green(p, d); A = A - A.T
    lam, V = np.linalg.eigh(1j*A)
    dentro = np.abs(p[:, 0]) + np.sqrt((p[:, 1:]**2).sum(1)) < a/2
    HO, HU = altura(p, d), altura(p[dentro], d)
    k = mantem(lam, HO); pos = k[lam[k] > 0]
    W = (V[:, pos]*lam[pos]) @ V[:, pos].conj().T; Dk = (V[:, k]*lam[k]) @ V[:, k].conj().T
    Wu = W[np.ix_(dentro, dentro)]; Du = Dk[np.ix_(dentro, dentro)]
    l2, V2 = np.linalg.eigh(Du); k2 = mantem(l2, HU); k2 = k2[np.abs(l2[k2]) > 1e-9*np.abs(l2).max()]
    mu = np.linalg.eigvals((V2[:, k2].conj().T @ Wu @ V2[:, k2]) / l2[k2][:, None]).real
    mu = mu[np.abs(mu) > 1e-12]
    return float(np.sum(mu*np.log(np.abs(mu)))), HO, HU, int(dentro.sum())

if __name__ == '__main__':
    print('--- 1+1 (calibracao) ---')
    Ns = (500, 1000, 2000); S = []
    for N in Ns:
        r = [entropia(N, 2, 0.5, np.random.default_rng(100*N+s)) for s in range(3)]
        S.append(np.mean([x[0] for x in r]))
        print(f' N = {N}: S = {S[-1]:.3f}   altura de O = {np.mean([x[1] for x in r]):.0f} (2 raiz N = {2*N**.5:.0f})', flush=True)
    print(f' inclinacao contra ln N: {np.polyfit(np.log(Ns), S, 1)[0]:.3f}  (esperado 1/6 = 0,167; Sorkin-Yazdi aqui deu 0,28)')
    print('--- 2+1 ---')
    a = 2**(-5/3); a3 = 0.218853; V = pi/12; Ns = (1000, 2000, 4000); S = []
    for N, reps in ((1000, 3), (2000, 3), (4000, 2)):
        r = [entropia(N, 3, a, np.random.default_rng(7*N+s)) for s in range(reps)]
        S.append(np.mean([x[0] for x in r])); mol = a3*(N/V)**(1/3)*pi*a
        print(f' N = {N}: S = {S[-1]:.3f}  alturas O/U = {np.mean([x[1] for x in r]):.0f}/{np.mean([x[2] for x in r]):.0f}  '
              f'moleculas = {mol:.1f}  nats por molecula = {S[-1]/mol:.3f}', flush=True)
    if min(S) > 0: print(f' S cresce como N^{np.polyfit(np.log(Ns), np.log(S), 1)[0]:.2f}  (lei de area: 0,33)')
