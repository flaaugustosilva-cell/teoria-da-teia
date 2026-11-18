"""Pre-registro 18/11/2026 18:35: corte em U = fluxo maximo de cadeias disjuntas (por ligacoes) de U para O\\U.
Em O: largura(O). Uso: python gargalo_causal.py"""
import numpy as np
from math import pi
from scipy.sparse import csr_matrix, coo_matrix
from scipy.sparse.csgraph import maximum_flow
from corte_cadeia import mantem
from ds2_anticadeia import sorteia as sorteia_ds, causal as causal_ds, largura
from ssee import sorteia as sorteia_mk

def gargalo(C, dentro):
    N = len(C); Cf = C.astype(np.float32); r, c = np.nonzero(C & ((Cf @ Cf) == 0))
    s, t = 0, 1; vin = 2 + np.arange(N); vout = 2 + N + np.arange(N)
    U = np.where(dentro)[0]; F = np.where(~dentro)[0]
    orig = np.concatenate([vin, vout[r], np.full(len(U), s), vout[F]])
    dest = np.concatenate([vout, vin[c], vin[U], np.full(len(F), t)])
    cap = np.ones(len(orig), np.int32)
    G = csr_matrix(coo_matrix((cap, (orig, dest)), shape=(2*N + 2, 2*N + 2)))
    return maximum_flow(G, s, t, method='dinic').flow_value

def S_de(C, dentro):
    A = (C.astype(float) - C.T.astype(float))/2.0; lam, V = np.linalg.eigh(1j*A)
    HO = largura(C); HU = gargalo(C, dentro)
    k = mantem(lam, HO); pos = k[lam[k] > 0]
    W = (V[:, pos]*lam[pos]) @ V[:, pos].conj().T; Dk = (V[:, k]*lam[k]) @ V[:, k].conj().T
    Wu = W[np.ix_(dentro, dentro)]; Du = Dk[np.ix_(dentro, dentro)]
    l2, V2 = np.linalg.eigh(Du); k2 = mantem(l2, HU); k2 = k2[np.abs(l2[k2]) > 1e-9*np.abs(l2).max()]
    mu = np.linalg.eigvals((V2[:, k2].conj().T @ Wu @ V2[:, k2]) / l2[k2][:, None]).real
    mu = mu[np.abs(mu) > 1e-12]
    return float(np.sum(mu*np.log(np.abs(mu)))), HO, HU

def ds(N, rng, h=1.2):
    T, th = sorteia_ds(N, h, rng); return S_de(causal_ds(T, th), np.abs(T) < np.minimum(th, pi - th))

def mk(N, rng, a=0.5):
    p = sorteia_mk(N, 2, rng); t, x = p[:, 0], p[:, 1]; dt = t[None, :] - t[:, None]
    return S_de((dt > 0) & (dt*dt > (x[None, :] - x[:, None])**2), np.abs(t) + np.abs(x) < a/2)

if __name__ == '__main__':
    for nome, f in (('Minkowski 1+1', mk), ('de Sitter 1+1', ds)):
        Ns = (500, 1000, 2000, 3000); S = []
        for N in Ns:
            r = [f(N, np.random.default_rng(31*N + s)) for s in range(3)]; S.append(np.mean([x[0] for x in r]))
            print(f'{nome} N = {N}: S = {S[-1]:.3f}  largura O = {np.mean([x[1] for x in r]):.0f}  gargalo U = {np.mean([x[2] for x in r]):.0f}', flush=True)
        print(f'{nome}: inclinacao = {np.polyfit(np.log(Ns), S, 1)[0]:.3f} (criterio 0,12 a 0,22)', flush=True)
