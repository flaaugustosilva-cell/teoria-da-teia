"""Regra da maior anticadeia em de Sitter 1+1 (fatia simetrica |T|<h, como Surya-X-Yazdi 2008.07697).
Coordenadas conformes: ds^2 = sec^2 T (-dT^2 + dtheta^2), theta periodico. Densidade ~ sec^2 T.
Regiao U = cunha tipo Rindler: dominio de dependencia de 0<theta<pi em T=0. G = C/2 (invariancia conforme em 2D).
Corte: em O e em U guardam-se tantos modos de cada sinal quanto a largura (maior anticadeia) da regiao.
Uso: python ds2_anticadeia.py"""
import numpy as np, sys
from math import pi
from scipy.sparse import csr_matrix, coo_matrix
from scipy.sparse.csgraph import maximum_flow
from corte_cadeia import mantem

def sorteia(N, h, rng):
    T = np.arctan(rng.uniform(-np.tan(h), np.tan(h), N)); th = rng.uniform(0, 2*pi, N)
    return T, th

def causal(T, th):
    dT = T[None, :] - T[:, None]; d = np.abs(th[None, :] - th[:, None]); d = np.minimum(d, 2*pi - d)
    return (dT > d)

def largura(C):
    N = len(C); Cf = C.astype(np.float32); meio = Cf @ Cf
    r, c = np.nonzero(C & (meio == 0))
    t, s = 0, 1; sai = 2 + np.arange(N); ent = 2 + N + np.arange(N)
    orig = np.concatenate([np.full(N, t), sai[r], ent, ent]); dest = np.concatenate([sai, ent[c], sai, np.full(N, s)])
    cap = np.concatenate([np.ones(N), np.full(len(r), N), np.full(N, N), np.ones(N)]).astype(np.int32)
    G = csr_matrix(coo_matrix((cap, (orig, dest)), shape=(2*N+2, 2*N+2)))
    return N - maximum_flow(G, t, s, method='dinic').flow_value

def entropia(N, h, rng, corte='largura'):
    T, th = sorteia(N, h, rng); C = causal(T, th)
    A = C/2.0; A = A - A.T
    lam, V = np.linalg.eigh(1j*A)
    dentro = np.abs(T) < np.minimum(th, pi - th)
    HO, HU = largura(C), largura(C[np.ix_(dentro, dentro)])
    if corte == 'nenhum': k = np.arange(N)
    else: k = mantem(lam, HO)
    pos = k[lam[k] > 0]
    W = (V[:, pos]*lam[pos]) @ V[:, pos].conj().T; Dk = (V[:, k]*lam[k]) @ V[:, k].conj().T
    Wu = W[np.ix_(dentro, dentro)]; Du = Dk[np.ix_(dentro, dentro)]
    l2, V2 = np.linalg.eigh(Du)
    k2 = np.arange(len(l2)) if corte == 'nenhum' else mantem(l2, HU)
    k2 = k2[np.abs(l2[k2]) > 1e-9*np.abs(l2).max()]
    mu = np.linalg.eigvals((V2[:, k2].conj().T @ Wu @ V2[:, k2]) / l2[k2][:, None]).real
    mu = mu[np.abs(mu) > 1e-12]
    return float(np.sum(mu*np.log(np.abs(mu)))), HO, HU, int(dentro.sum())

if __name__ == '__main__':
    h = float(sys.argv[1]) if len(sys.argv) > 1 else 1.2
    Ns = (500, 1000, 2000, 3000); S = []; S0 = []
    for N in Ns:
        r = [entropia(N, h, np.random.default_rng(31*N+s)) for s in range(3)]
        r0 = entropia(N, h, np.random.default_rng(31*N), 'nenhum')[0]
        S.append(np.mean([x[0] for x in r])); S0.append(r0)
        print(f'N = {N}: S (largura) = {S[-1]:.3f} +- {np.std([x[0] for x in r])/3**.5:.3f} | sem corte = {r0:.1f} | '
              f'larguras O/U = {np.mean([x[1] for x in r]):.0f}/{np.mean([x[2] for x in r]):.0f} | N_U = {np.mean([x[3] for x in r]):.0f}', flush=True)
    print(f'inclinacao contra ln N: com largura {np.polyfit(np.log(Ns), S, 1)[0]:.3f}; sem corte cresce como N^{np.polyfit(np.log(Ns), np.log(S0), 1)[0]:.2f}')
