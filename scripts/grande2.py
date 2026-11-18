"""Versao para teias muito grandes (18/11/2026): regra da maior anticadeia em 2+1.
Diferencas para grande.py: (1) largura por fluxo sobre as ligacoes (largura_fluxo.py), identica ao
emparelhamento e de 10 a 80 vezes mais rapida; (2) nao guarda a matriz de relacoes; (3) ajuste
cuidadoso do metodo aleatorizado (folga 900, 4 iteracoes; erro de 0,1% validado em 8000 nos).
Como cada regiao U e um diamante (convexo), as ligacoes de U sao as ligacoes da teia dentro de U.
Uso: python grande2.py N rodadas semente"""
import sys, time, numpy as np
from ssee import sorteia
from grande import modos_positivos
from largura_fluxo import ligacoes, largura_por_fluxo
AS = (0.2, 0.315, 0.45)

def monta_A(p, bloco=2000):
    N = len(p); A = np.zeros((N, N), np.float32)
    for i0 in range(0, N, bloco):
        q = p[i0:i0+bloco]; dt = p[None, :, 0] - q[:, None, 0]; dr2 = ((p[None, :, 1:] - q[:, None, 1:])**2).sum(2)
        c = (dt > 0) & (dt*dt > dr2)
        A[i0:i0+bloco] = np.where(c, 1/(2*np.pi*np.sqrt(np.where(c, dt*dt - dr2, 1.0))), 0.0)
    A -= A.T; return A

def roda(N, rng, folga=900, pot=4):
    t0 = time.time(); p = sorteia(N, 3, rng)
    r, c = ligacoes(p); MO = largura_por_fluxo(N, r, c)
    rr = np.sqrt((p[:, 1:]**2).sum(1)); MU = {}; us = {}
    for a in AS:
        dentro = np.abs(p[:, 0]) + rr < a/2; iu = np.where(dentro)[0]; us[a] = iu
        novo = -np.ones(N, int); novo[iu] = np.arange(len(iu)); k = dentro[r] & dentro[c]
        MU[a] = largura_por_fluxo(len(iu), novo[r[k]], novo[c[k]])
    del r, c; tl = time.time() - t0
    A = monta_A(p); lam, V = modos_positivos(A, MO, rng, folga=folga, pot=pot); del A
    out = []
    for a, iu in us.items():
        Vu = V[iu]; W = (Vu*lam) @ Vu.conj().T; Dk = W - W.conj(); NU = len(iu)
        l2, V2 = np.linalg.eigh(Dk); o = np.argsort(l2); m = min(MU[a], NU//2)
        k2 = np.concatenate([o[:m], o[-m:]]); k2 = k2[np.abs(l2[k2]) > 1e-9*np.abs(l2).max()]
        mu = np.linalg.eigvals((V2[:, k2].conj().T @ W @ V2[:, k2]) / l2[k2][:, None]).real
        mu = mu[np.abs(mu) > 1e-12]; out.append(float(np.sum(mu*np.log(np.abs(mu)))))
    return out, MO, tl, time.time() - t0

if __name__ == '__main__':
    N, reps, sem = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    for s in range(reps):
        S, MO, tl, dt = roda(N, np.random.default_rng(9000 + 31*N + s + 10**6*sem))
        print(f'N = {N} rodada {s}: S(a = 0,2 / 0,315 / 0,45) = ' + ' / '.join(f'{x:.2f}' for x in S)
              + f'  largura O = {MO}  (largura {tl:.0f} s, total {dt:.0f} s)', flush=True)
