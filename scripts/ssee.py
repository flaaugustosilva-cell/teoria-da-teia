"""Entropia de emaranhamento de Sorkin (SSEE) de um campo escalar sem massa numa teia sorteada.
Diamante grande O (pontas em t = +-1/2) e diamante menor U (pontas em +-a/2), mesmo centro.
iDelta = i(G - G^T); vacuo de Sorkin-Johnston W = parte positiva de iDelta.
Corte duplo (Sorkin-Yazdi; Belenchia e outros): autovalores |lambda| < kappa sao zerados em O e em U,
kappa = c * V^(2/d - 1) * N^(1 - 1/d)   (em 2D, c = 1/(4 pi) da kappa = raiz(N)/(4 pi)).
S = soma mu*ln|mu| com W x = mu iDelta x restrito a U.
Funcao de Green retardada: 2D G = C/2; 3D G = 1/(2 pi tau) (tau = tempo proprio pelas coordenadas)."""
import numpy as np
from math import pi

def sorteia(N, d, rng):
    pts = []
    while len(pts) < N:
        x = rng.uniform(-0.5, 0.5, size=(4*N, d))
        r = np.sqrt((x[:, 1:]**2).sum(1))
        x = x[np.abs(x[:, 0]) + r < 0.5]
        pts.extend(x.tolist())
    return np.array(pts[:N])

def green(p, d):
    dt = p[None, :, 0] - p[:, None, 0]
    dr2 = ((p[None, :, 1:] - p[:, None, 1:])**2).sum(2)
    causal = (dt > 0) & (dt*dt > dr2)
    if d == 2: return 0.5*causal
    tau = np.sqrt(np.where(causal, dt*dt - dr2, 1.0))
    return np.where(causal, 1/(2*pi*tau), 0.0)

def vol(d, h):  # volume de diamante de altura h
    return h*h/2 if d == 2 else pi*h**3/12

def entropia(N, d, a, cs, rng):
    """devolve {c: S} para varios c do corte, e N_U"""
    p = sorteia(N, d, rng)
    A = green(p, d); A = A - A.T
    lam, V = np.linalg.eigh(1j*A)
    dentro = np.abs(p[:, 0]) + np.sqrt((p[:, 1:]**2).sum(1)) < a/2
    NU = int(dentro.sum()); out = {}
    for c in cs:
        kO = c*vol(d, 1)**(2/d-1)*N**(1-1/d) if c > 0 else 1e-9*lam.max()
        kU = c*vol(d, a)**(2/d-1)*NU**(1-1/d) if c > 0 else 1e-9*lam.max()
        pos = lam > kO; fica = np.abs(lam) > kO
        W = (V[:, pos]*lam[pos]) @ V[:, pos].conj().T
        Dk = (V[:, fica]*lam[fica]) @ V[:, fica].conj().T          # iDelta ja truncado em O
        Wu = W[np.ix_(dentro, dentro)]; Du = Dk[np.ix_(dentro, dentro)]
        l2, V2 = np.linalg.eigh(Du); k = np.abs(l2) > kU
        M = V2[:, k].conj().T @ Wu @ V2[:, k]
        mu = np.linalg.eigvals(M / l2[k][:, None])
        mu = mu.real; mu = mu[np.abs(mu) > 1e-12]
        out[c] = float(np.sum(mu*np.log(np.abs(mu))))
    return out, NU
