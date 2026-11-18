"""Teias grandes, varias regioes na mesma teia (os modos de O sao calculados uma vez so).
Uso: python grande_regioes.py N rodadas semente   -> regioes a = 0,2 / 0,315 / 0,45"""
import sys, time, numpy as np
from ssee import sorteia
from grande import monta, largura_de, modos_positivos
AS = (0.2, 0.315, 0.45)
def roda(N, rng):
    t0 = time.time(); p = sorteia(N, 3, rng); A, C = monta(p); MO = largura_de(C)
    r = np.sqrt((p[:, 1:]**2).sum(1)); out = []
    us = {a: np.where(np.abs(p[:, 0]) + r < a/2)[0] for a in AS}
    MU = {a: largura_de(C[iu][:, iu]) for a, iu in us.items()}; del C
    lam, V = modos_positivos(A, MO, rng); del A
    for a, iu in us.items():
        Vu = V[iu]; W = (Vu*lam) @ Vu.conj().T; Dk = W - W.conj(); NU = len(iu)
        l2, V2 = np.linalg.eigh(Dk); o = np.argsort(l2); m = min(MU[a], NU//2)
        k2 = np.concatenate([o[:m], o[-m:]]); k2 = k2[np.abs(l2[k2]) > 1e-9*np.abs(l2).max()]
        mu = np.linalg.eigvals((V2[:, k2].conj().T @ W @ V2[:, k2]) / l2[k2][:, None]).real
        mu = mu[np.abs(mu) > 1e-12]; out.append(float(np.sum(mu*np.log(np.abs(mu)))))
    return out, MO, time.time() - t0
N, reps, sem = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
for s in range(reps):
    S, MO, dt = roda(N, np.random.default_rng(10**6*sem + 7*N + s))
    print(f'N = {N}  S(a = 0,2 / 0,315 / 0,45) = ' + ' / '.join(f'{x:.2f}' for x in S) + f'  largura O = {MO}  ({dt:.0f} s)', flush=True)
