"""Pre-registro 19/11/2026 00:10: SVD do bloco cruzado do vacuo SJ (2+1, sem corte), U contra O\\U, e controle aleatorio.
Uso: python svd_teia.py"""
import numpy as np
from ssee import sorteia, green
from anticadeia_dimensoes import causal, moleculas

def s_svd(W, idx_a, idx_b):
    s = np.linalg.svd(W[np.ix_(idx_a, idx_b)], compute_uv=False); s = s[s > 1e-12*s.max()]
    l = s**2/np.sum(s**2); return float(-np.sum(l*np.log(l)))

def rodada(N, a, rng):
    p = sorteia(N, 3, rng); C, dt, dr2 = causal(p)
    A = green(p, 3); A = A - A.T; lam, V = np.linalg.eigh(1j*A); pos = lam > 1e-12*lam.max()
    W = (V[:, pos]*lam[pos]) @ V[:, pos].conj().T
    dentro = np.abs(p[:, 0]) + np.sqrt((p[:, 1:]**2).sum(1)) < a/2; U = np.where(dentro)[0]; F = np.where(~dentro)[0]
    ctl = rng.permutation(N)[:len(U)]; resto = np.setdiff1d(np.arange(N), ctl)
    return s_svd(W, U, F), s_svd(W, ctl, resto), moleculas(p, C, a), len(U)

if __name__ == '__main__':
    out = []
    for N, reps in ((1000, 3), (2000, 3), (4000, 2)):
        r = [rodada(N, 0.6, np.random.default_rng(31*N + s + 9)) for s in range(reps)]
        S = np.mean([x[0] for x in r]); Sc = np.mean([x[1] for x in r]); M = np.mean([x[2] for x in r])
        out.append((N, S, M)); print(f'N = {N}: S_svd = {S:.3f}  controle = {Sc:.3f}  moleculas = {M:.1f}  S/molecula = {S/M:.3f}  (controle difere {100*(Sc-S)/S:+.0f}%)  N_U = {np.mean([x[3] for x in r]):.0f}', flush=True)
    s_m = [S/M for _, S, M in out]; print(f'S/molecula: {s_m[0]:.3f} -> {s_m[-1]:.3f} (variacao {100*(s_m[-1]-s_m[0])/s_m[0]:+.0f}%)')
