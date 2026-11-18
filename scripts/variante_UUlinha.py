"""Pre-registro 18/11/2026 14:40: em O guardam-se largura(U)+largura(U') modos de cada sinal; em U, largura(U).
U' = dominio de dependencia do complemento de U na fatia. Uma tentativa so.
Uso: python variante_UUlinha.py"""
import numpy as np
from math import pi
from corte_cadeia import mantem
from ds2_anticadeia import sorteia as sorteia_ds, causal as causal_ds, largura
from ssee import sorteia as sorteia_mk

def S_de(C, A, dentro, fora):
    lam, V = np.linalg.eigh(1j*A)
    HU = largura(C[np.ix_(dentro, dentro)]); HUl = largura(C[np.ix_(fora, fora)]); HO = HU + HUl
    k = mantem(lam, HO); pos = k[lam[k] > 0]
    W = (V[:, pos]*lam[pos]) @ V[:, pos].conj().T; Dk = (V[:, k]*lam[k]) @ V[:, k].conj().T
    Wu = W[np.ix_(dentro, dentro)]; Du = Dk[np.ix_(dentro, dentro)]
    l2, V2 = np.linalg.eigh(Du); k2 = mantem(l2, HU); k2 = k2[np.abs(l2[k2]) > 1e-9*np.abs(l2).max()]
    mu = np.linalg.eigvals((V2[:, k2].conj().T @ Wu @ V2[:, k2]) / l2[k2][:, None]).real
    mu = mu[np.abs(mu) > 1e-12]
    return float(np.sum(mu*np.log(np.abs(mu)))), HO, HU

def ds(N, rng, h=1.2):
    T, th = sorteia_ds(N, h, rng); C = causal_ds(T, th)
    dentro = np.abs(T) < np.minimum(th, pi - th); fora = np.abs(T) < np.minimum(th - pi, 2*pi - th)
    return S_de(C, (C.astype(float) - C.T.astype(float))/2.0, dentro, fora)

def mk(N, rng, a=0.5):
    p = sorteia_mk(N, 2, rng); t, x = p[:, 0], p[:, 1]
    dt = t[None, :] - t[:, None]; C = (dt > 0) & (dt*dt > (x[None, :] - x[:, None])**2)
    dentro = np.abs(t) + np.abs(x) < a/2; fora = (np.abs(t) < np.abs(x) - a/2)
    return S_de(C, (C.astype(float) - C.T.astype(float))/2.0, dentro, fora)

if __name__ == '__main__':
    for nome, f in (('de Sitter 1+1', ds), ('Minkowski 1+1', mk)):
        Ns = (500, 1000, 2000, 3000); S = []
        for N in Ns:
            r = [f(N, np.random.default_rng(31*N + s)) for s in range(3)]
            S.append(np.mean([x[0] for x in r]))
            print(f'{nome} N = {N}: S = {S[-1]:.3f} +- {np.std([x[0] for x in r])/3**.5:.3f}  cortes O/U = {np.mean([x[1] for x in r]):.0f}/{np.mean([x[2] for x in r]):.0f}', flush=True)
        print(f'{nome}: inclinacao contra ln N = {np.polyfit(np.log(Ns), S, 1)[0]:.3f} (previsto ~0,167)', flush=True)
