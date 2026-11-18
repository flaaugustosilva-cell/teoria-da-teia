"""Pre-registro 18/11/2026 18:10: controle. Mesma construcao das moleculas, mas p e q do mesmo lado (dentro).
Uso: python controle_molecula.py"""
import numpy as np
from ssee import sorteia
from anticadeia_dimensoes import causal

def entropia_par(D, W, i, j):
    k = [i, j]; mu = np.linalg.eigvals(np.linalg.solve(D[np.ix_(k, k)], W[np.ix_(k, k)])).real
    mu = mu[np.abs(mu) > 1e-12]; return np.sum(mu*np.log(np.abs(mu)))

def rodada(N, a, rng):
    p = sorteia(N, 4, rng); C, dt, dr2 = causal(p)
    Cf = C.astype(np.float64); G = (C & ((Cf @ Cf) == 0)).astype(np.float64)
    A = G - G.T; lam, V = np.linalg.eigh(1j*A); pos = lam > 1e-12*lam.max()
    W = (V[:, pos]*lam[pos]) @ V[:, pos].conj().T; D = 1j*A
    r = np.sqrt((p[:, 1:]**2).sum(1)); t = p[:, 0]; abaixo = t < 0; vis = (a/2 - t) >= r
    Cb = C & abaixo[None, :]; um = Cb.sum(1) == 1
    cand = np.where(um & abaixo & vis)[0]; q = Cb[cand].argmax(1)
    mol = [entropia_par(D, W, i, j) for i, j in zip(cand[~vis[q]], q[~vis[q]])]
    ctl = [entropia_par(D, W, i, j) for i, j in zip(cand[vis[q]], q[vis[q]])]
    return np.mean(mol), np.mean(ctl), len(mol), len(ctl)

if __name__ == '__main__':
    for N in (1000, 2000, 4000):
        r = [rodada(N, 0.6, np.random.default_rng(31*N + s + 4)) for s in range(3)]
        m = np.mean([x[0] for x in r]); c = np.mean([x[1] for x in r])
        print(f'N = {N}: moleculas = {m:.3f} ({np.mean([x[2] for x in r]):.0f} pares)  controle = {c:.3f} ({np.mean([x[3] for x in r]):.0f} pares)  diferenca = {100*(m-c)/c:+.1f}%', flush=True)
