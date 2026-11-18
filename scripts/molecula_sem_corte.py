"""Pre-registro 18/11/2026 17:50: entropia de Sorkin do par {p,q} de cada molecula de horizonte,
com o vacuo SJ da teia inteira SEM corte. Uso: python molecula_sem_corte.py d   (d = 3 ou 4)"""
import sys, numpy as np
from ssee import sorteia
from anticadeia_dimensoes import causal

def pares(p, C, a):
    r = np.sqrt((p[:, 1:]**2).sum(1)); t = p[:, 0]
    abaixo = t < 0; vis = (a/2 - t) >= r
    Cb = C & abaixo[None, :]; um = Cb.sum(1) == 1
    cand = np.where(um & abaixo & vis)[0]; q = Cb[cand].argmax(1)
    ok = ~vis[q]; return cand[ok], q[ok]

def rodada(N, d, a, rng):
    p = sorteia(N, d, rng); C, dt, dr2 = causal(p)
    if d == 3: G = np.where(C, 1/(2*np.pi*np.sqrt(np.where(C, dt*dt - dr2, 1.0))), 0.0)
    else: Cf = C.astype(np.float64); G = (C & ((Cf @ Cf) == 0)).astype(np.float64)
    A = G - G.T; lam, V = np.linalg.eigh(1j*A); pos = lam > 1e-12*lam.max()
    W = (V[:, pos]*lam[pos]) @ V[:, pos].conj().T; D = 1j*A
    s = []
    for i, j in zip(*pares(p, C, a)):
        k = [i, j]; mu = np.linalg.eigvals(np.linalg.solve(D[np.ix_(k, k)], W[np.ix_(k, k)])).real
        mu = mu[np.abs(mu) > 1e-12]; s.append(np.sum(mu*np.log(np.abs(mu))))
    return np.mean(s), len(s)

if __name__ == '__main__':
    d = int(sys.argv[1]); a = 0.6
    for N in (1000, 2000, 4000):
        r = [rodada(N, d, a, np.random.default_rng(31*N + s + d)) for s in range(3)]
        v = np.array([x[0] for x in r])
        print(f'd = {d}, N = {N}: s por molecula = {v.mean():.3f} +- {v.std()/3**.5:.3f}  (moleculas por teia: {np.mean([x[1] for x in r]):.0f})', flush=True)
