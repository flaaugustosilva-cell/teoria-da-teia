"""Regra da maior anticadeia em 2+1 e 3+1, com moleculas CONTADAS na propria teia (17/11/2026).
Moleculas (Barton e outros): horizonte = fronteira do passado do topo de U (cujo corte em t = 0 e a borda de U).
p no passado do topo, q fora dele, p -> q, ambos com t < 0, e q e o unico no do futuro de p com t < 0.
Contar direto inclui a curvatura da borda, que a formula de horizonte plano nao inclui.
Funcao de Green: 3D 1/(2 pi tau); 4D proporcional a matriz de ligacoes (Johnston). A escala nao importa:
a regra conta modos e a entropia de Sorkin nao depende da normalizacao.
Uso: python anticadeia_dimensoes.py d a      (d = 3 ou 4; a = tamanho de U, ex. 0.6)"""
import sys, numpy as np
from ssee import sorteia
from corte_cadeia import mantem
from corte_anticadeia import largura

def causal(p):
    dt = p[None, :, 0] - p[:, None, 0]; dr2 = ((p[None, :, 1:] - p[:, None, 1:])**2).sum(2)
    return (dt > 0) & (dt*dt > dr2), dt, dr2

def moleculas(p, C, a):
    r = np.sqrt((p[:, 1:]**2).sum(1)); t = p[:, 0]
    abaixo = t < 0; vis = (a/2 - t) >= r
    Cb = C & abaixo[None, :]                      # futuro restrito a t < 0
    um = Cb.sum(1) == 1
    cand = np.where(um & abaixo & vis)[0]
    q = Cb[cand].argmax(1)
    return int(np.sum(~vis[q]))

def entropia(N, d, a, rng):
    p = sorteia(N, d, rng); C, dt, dr2 = causal(p)
    if d == 3: G = np.where(C, 1/(2*np.pi*np.sqrt(np.where(C, dt*dt - dr2, 1.0))), 0.0)
    else:
        Cf = C.astype(np.float64); G = (C & ((Cf @ Cf) == 0)).astype(np.float64)
    A = G - G.T; lam, V = np.linalg.eigh(1j*A)
    dentro = np.abs(p[:, 0]) + np.sqrt((p[:, 1:]**2).sum(1)) < a/2
    NU = int(dentro.sum()); MO, MU = min(largura(p), N//2), min(largura(p[dentro]), NU//2)
    k = mantem(lam, MO); pos = k[lam[k] > 0]
    W = (V[:, pos]*lam[pos]) @ V[:, pos].conj().T; Dk = (V[:, k]*lam[k]) @ V[:, k].conj().T
    Wu = W[np.ix_(dentro, dentro)]; Du = Dk[np.ix_(dentro, dentro)]
    l2, V2 = np.linalg.eigh(Du); k2 = mantem(l2, MU); k2 = k2[np.abs(l2[k2]) > 1e-9*np.abs(l2).max()]
    mu = np.linalg.eigvals((V2[:, k2].conj().T @ Wu @ V2[:, k2]) / l2[k2][:, None]).real
    mu = mu[np.abs(mu) > 1e-12]
    return float(np.sum(mu*np.log(np.abs(mu)))), moleculas(p, C, a), MU, NU

if __name__ == '__main__':
    d, a = int(sys.argv[1]), float(sys.argv[2]); Ns = (1000, 2000, 4000); S = []; M = []
    print(f'd = {d}, a = {a}. Lei de area pede S ~ N^{(d-2)/d:.2f}')
    for N, reps in ((1000, 3), (2000, 2), (4000, 1)):
        r = [entropia(N, d, a, np.random.default_rng(31*N+s+d)) for s in range(reps)]
        S.append(np.mean([x[0] for x in r])); M.append(np.mean([x[1] for x in r]))
        print(f' N = {N}: S = {S[-1]:.2f}  moleculas contadas = {M[-1]:.1f}  modos U = {np.mean([x[2] for x in r]):.0f} de '
              f'{np.mean([x[3] for x in r])/2:.0f}  nats por molecula = {S[-1]/M[-1]:.2f}', flush=True)
    print(f' S cresce como N^{np.polyfit(np.log(Ns), np.log(S), 1)[0]:.2f}; moleculas como N^{np.polyfit(np.log(Ns), np.log(M), 1)[0]:.2f}')
