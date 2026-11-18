"""Pre-registro 18/11/2026 14:57: a massa baixa s1 (nats por molecula) em 2+1?
G = exp(-m tau)/(2 pi tau). Regra original da anticadeia. N = 2000, a = 0.6, 3 rodadas, m = 0, 2, 8, 32.
Uso: python massa_s1.py"""
import numpy as np
from ssee import sorteia
from corte_cadeia import mantem
from corte_anticadeia import largura
from anticadeia_dimensoes import causal, moleculas

def entropia(N, a, m, rng):
    p = sorteia(N, 3, rng); C, dt, dr2 = causal(p)
    tau = np.sqrt(np.where(C, dt*dt - dr2, 1.0)); G = np.where(C, np.exp(-m*tau)/(2*np.pi*tau), 0.0)
    A = G - G.T; lam, V = np.linalg.eigh(1j*A)
    dentro = np.abs(p[:, 0]) + np.sqrt((p[:, 1:]**2).sum(1)) < a/2; NU = int(dentro.sum())
    MO, MU = min(largura(p), N//2), min(largura(p[dentro]), NU//2)
    k = mantem(lam, MO); pos = k[lam[k] > 0]
    W = (V[:, pos]*lam[pos]) @ V[:, pos].conj().T; Dk = (V[:, k]*lam[k]) @ V[:, k].conj().T
    Wu = W[np.ix_(dentro, dentro)]; Du = Dk[np.ix_(dentro, dentro)]
    l2, V2 = np.linalg.eigh(Du); k2 = mantem(l2, MU); k2 = k2[np.abs(l2[k2]) > 1e-9*np.abs(l2).max()]
    mu = np.linalg.eigvals((V2[:, k2].conj().T @ Wu @ V2[:, k2]) / l2[k2][:, None]).real; mu = mu[np.abs(mu) > 1e-12]
    return float(np.sum(mu*np.log(np.abs(mu)))), moleculas(p, C, a)

if __name__ == '__main__':
    N, a = 2000, 0.6
    for m in (0, 2, 8, 32):
        r = [entropia(N, a, m, np.random.default_rng(31*N + s)) for s in range(3)]   # mesmas teias para todo m
        S = np.array([x[0] for x in r]); M = np.array([x[1] for x in r]); s1 = S/M
        print(f'm = {m:2d}: S = {S.mean():.2f}  moleculas = {M.mean():.1f}  s1 = {s1.mean():.2f} +- {s1.std()/3**.5:.2f}', flush=True)
