"""H1, segunda etapa, entrega B - calculos EXTRAS (nao registrados), exatos, para n <= 8:
(1) conferencia: a soma das teias ruins (altura <= 2) da enumeracao bate com a formula exata do E1 (lnZ)?
(2) H1 em TODA a janela theta = 2 beta em [2pi/3, 4pi/3]: minimo rigoroso de |Z_boa(theta)| = |sum w e^{i theta B}|,
    com w = 1/e(P), por grade + cota da derivada (|dZ/dtheta| <= sum w |B|).
(3) razao exata R(theta) = |Z_ruim| / |Z_boa| na janela (maximo rigoroso pela mesma tecnica).
Uso: python h1b_B_extra.py 5 6 7 8   ->  h1b_B_extra.json"""
import sys, json, math, numpy as np
from e1_comum import lnZ_ruim, beta_de, C_ACAO, F
NG = 200001; th = np.linspace(2*np.pi/3, 4*np.pi/3, NG); hstep = th[1] - th[0]
out = {}
for n in map(int, sys.argv[1:]):
    d = np.load(f'h1b_B_n{n}.npz'); B = d['B'].astype(float); h = d['h']; w = 1/d['e'].astype(float)
    boa = h >= 3; ruim = ~boa
    # (1) conferencia com a formula do E1 em tres valores de x
    conf = []
    for x in (5.0, 7.0, 9.0):
        t = 2*beta_de(x); zr = np.sum(w[ruim]*np.exp(1j*t*B[ruim]))   # soma direta, teia por teia
        conf.append(abs(math.log(abs(zr)) - (lnZ_ruim(n, x) - math.lgamma(n + 1))))
    # (2) e (3)
    def Z(mask):   # agrupado por valor de B (identico a somar teia por teia)
        v, inv = np.unique(B[mask], return_inverse=True); Wv = np.bincount(inv, weights=w[mask])
        return np.exp(1j*np.outer(th, v)) @ Wv
    zb = np.abs(Z(boa)); zr = np.abs(Z(ruim))
    Db = np.sum(w[boa]*np.abs(B[boa])); Dr = np.sum(w[ruim]*np.abs(B[ruim]))
    minb = zb.min() - Db*hstep/2; maxr = zr.max() + Dr*hstep/2
    Rgrade = zr/zb; k = int(np.argmax(Rgrade))
    Rmax = maxr/minb if minb > 0 else float('inf')
    W = w[boa].sum()
    xs_min = F*math.sqrt(th[int(np.argmin(zb))]/2/C_ACAO)
    out[n] = dict(W_n=W, conferencia_max_dif_ln=max(conf), min_Zboa_grade=float(zb.min()), min_Zboa_rigoroso=float(minb),
                  x_do_minimo=xs_min, max_Zruim_rigoroso=float(maxr), R_max_grade=float(Rgrade[k]), x_R_max=F*math.sqrt(th[k]/2/C_ACAO),
                  R_max_rigoroso=Rmax, H1_em_toda_janela=bool(minb >= 1))
    print(f'n={n}: conferencia ruins x formula do E1: maior diferenca em ln|Z| = {max(conf):.2e}')
    print(f'   W_n = {W:.4f}; min |Z_boa| na janela: grade {zb.min():.4f} (em x = {xs_min:.3f}), rigoroso >= {minb:.4f} -> H1 em toda a janela: {minb >= 1}')
    print(f'   max |Z_ruim| rigoroso <= {maxr:.4f}; R = |Z_ruim|/|Z_boa|: max na grade {Rgrade[k]:.4f} (x = {F*math.sqrt(th[k]/2/C_ACAO):.3f}), max rigoroso <= {Rmax:.4f}', flush=True)
json.dump(out, open('h1b_B_extra.json', 'w'), indent=1)
