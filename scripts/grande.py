"""Versao para teias grandes (17/11/2026). Mesma regra da maior anticadeia, em 2+1.
Em vez de diagonalizar a matriz inteira (N x N complexa), calcula so os modos guardados:
1) A = G - G^T guardada em float32 (real, antissimetrica); 2) subespaco aleatorio Q com L colunas,
   2 iteracoes de potencia; 3) B = Q^T A Q (pequena), autovalores de iB; 4) volta com Q.
Os modos negativos sao os conjugados dos positivos (A real), entao so os positivos sao guardados.
Largura (maior anticadeia) por Dilworth com a relacao em formato esparso, montada em blocos.
Uso: python grande.py N a [rodadas] [semente]"""
import sys, time, numpy as np
from scipy.sparse import csr_matrix, vstack
from scipy.sparse.csgraph import maximum_bipartite_matching
from ssee import sorteia

def monta(p, bloco=2000):
    N = len(p); A = np.zeros((N, N), np.float32); linhas = []
    for i0 in range(0, N, bloco):
        q = p[i0:i0+bloco]
        dt = p[None, :, 0] - q[:, None, 0]; dr2 = ((p[None, :, 1:] - q[:, None, 1:])**2).sum(2)
        c = (dt > 0) & (dt*dt > dr2)
        A[i0:i0+bloco] = np.where(c, 1/(2*np.pi*np.sqrt(np.where(c, dt*dt - dr2, 1.0))), 0.0)
        linhas.append(csr_matrix(c))
    A -= A.T
    return A, vstack(linhas).tocsr()

def largura_de(C):
    m = maximum_bipartite_matching(C, perm_type='column'); return C.shape[0] - int(np.sum(m >= 0))

def modos_positivos(A, M, rng, folga=150, pot=2):
    N = A.shape[0]; L = min(N, 2*M + folga)
    Y = A @ rng.standard_normal((N, L)).astype(np.float32)
    for _ in range(pot):
        Q, _ = np.linalg.qr(Y.astype(np.float64)); Y = A @ (A @ Q.astype(np.float32))
    Q, _ = np.linalg.qr(Y.astype(np.float64)); Q32 = Q.astype(np.float32)
    B = (Q32.T @ (A @ Q32)).astype(np.float64); B = (B - B.T)/2
    lam, w = np.linalg.eigh(1j*B)
    o = np.argsort(lam)[::-1][:M]
    return lam[o], Q @ w[:, o]                       # M maiores positivos e seus vetores (N x M complexo)

def entropia(N, a, rng):
    t0 = time.time(); p = sorteia(N, 3, rng); A, C = monta(p)
    dentro = np.abs(p[:, 0]) + np.sqrt((p[:, 1:]**2).sum(1)) < a/2; iu = np.where(dentro)[0]; NU = len(iu)
    MO = largura_de(C); MU = largura_de(C[iu][:, iu]); del C
    lam, V = modos_positivos(A, MO, rng); del A
    Vu = V[iu]                                       # restrito a U
    W = (Vu*lam) @ Vu.conj().T
    Dk = W - W.conj()                                # soma dos positivos (W) menos os negativos (conjugados)
    l2, V2 = np.linalg.eigh(Dk); o = np.argsort(l2); MU = min(MU, NU//2)
    k2 = np.concatenate([o[:MU], o[-MU:]]); k2 = k2[np.abs(l2[k2]) > 1e-9*np.abs(l2).max()]
    mu = np.linalg.eigvals((V2[:, k2].conj().T @ W @ V2[:, k2]) / l2[k2][:, None]).real
    mu = mu[np.abs(mu) > 1e-12]
    return float(np.sum(mu*np.log(np.abs(mu)))), MO, MU, NU, time.time() - t0

if __name__ == '__main__':
    N, a = int(sys.argv[1]), float(sys.argv[2])
    reps = int(sys.argv[3]) if len(sys.argv) > 3 else 1; sem = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    mol = 0.218853*((N/(np.pi/12))**(1/3))*np.pi*a
    for s in range(reps):
        S, MO, MU, NU, dt = entropia(N, a, np.random.default_rng(10**6*sem + 31*N + s))
        print(f'N = {N} a = {a}: S = {S:.2f}  largura O/U = {MO}/{MU}  U tem {NU} nos  moleculas (formula) = {mol:.2f}  ({dt:.0f} s)', flush=True)
