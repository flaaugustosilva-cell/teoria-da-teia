"""H1, segunda etapa, entrega B - EXTRA (nao registrado), exato e rigoroso, n <= 8, em toda a janela theta in [2pi/3, 4pi/3]:
(a) minimo rigoroso de |Z_boa| e maximo rigoroso de R = |Z_ruim|/|Z_boa|, por subdivisao adaptativa:
    num intervalo de centro c e meia largura r, |Z(theta)| esta entre |Z(c)| - D r e |Z(c)| + D r, com D = sum w |B|.
(b) conferencia em precisao alta (mpmath, 60 digitos, pesos racionais exatos 1/e(P)) do valor de |Z_boa| no ponto de minimo.
Uso: python h1b_B_rigor.py 5 6 7 8  ->  h1b_B_rigor.json"""
import sys, json, math, numpy as np, mpmath as mp
from e1_comum import C_ACAO, F
A, Bf = 2*np.pi/3, 4*np.pi/3
def x_de(t): return F*math.sqrt(t/2/C_ACAO)
out = {}
for n in map(int, sys.argv[1:]):
    d = np.load(f'h1b_B_n{n}.npz'); B = d['B'].astype(float); e = d['e']; w = 1/e.astype(float); boa = d['h'] >= 3
    def agrega(mask):
        v, inv = np.unique(B[mask], return_inverse=True); return v, np.bincount(inv, weights=w[mask])
    vb, Wb = agrega(boa); vr, Wr = agrega(~boa); Db = float(np.sum(Wb*np.abs(vb))); Dr = float(np.sum(Wr*np.abs(vr)))
    Zb = lambda t: np.abs(np.exp(1j*np.outer(t, vb)) @ Wb); Zr = lambda t: np.abs(np.exp(1j*np.outer(t, vr)) @ Wr)
    # subdivisao adaptativa
    N0 = 20000; r = (Bf - A)/N0/2; c = A + r + 2*r*np.arange(N0)
    minb_inf = math.inf; R_sup = 0.0; nivel = 0; total = 0
    while len(c):
        total += len(c); zb = Zb(c); zr = Zr(c)
        lb = zb - Db*r; ub_r = zr + Dr*r
        Rb = np.where(lb > 0, ub_r/np.where(lb > 0, lb, 1), np.inf)
        ok = (lb > 0.5*zb) & (Rb < 1.0) | ((lb > 0) & (Rb < 0.5))   # fechado: cota apertada o bastante
        if nivel >= 12: ok[:] = True                                  # limite de profundidade
        minb_inf = min(minb_inf, float(np.min(np.where(ok, lb, np.inf)))) if ok.any() else minb_inf
        R_sup = max(R_sup, float(np.max(np.where(ok, Rb, 0)))) if ok.any() else R_sup
        rest = c[~ok]; r /= 10; c = (rest[:, None] + r*(2*np.arange(10) - 9)[None, :]).ravel(); nivel += 1
    # minimo pontual (valor exato num ponto) e conferencia em precisao alta
    t = np.linspace(A, Bf, 400001); zb = Zb(t); k = int(np.argmin(zb)); tmin = float(t[k])
    mp.mp.dps = 60
    val, cnt = np.unique(e[boa], return_counts=True)       # pesos exatos por (B, e)
    pares = {}
    for Bv, ev in zip(d['B'][boa], e[boa]): pares[(int(Bv), int(ev))] = pares.get((int(Bv), int(ev)), 0) + 1
    zmp = mp.fsum(mp.mpf(c_)/ev*mp.expj(mp.mpf(tmin)*Bv) for (Bv, ev), c_ in pares.items())
    out[n] = dict(min_Zboa_pontual=float(zb[k]), theta_min=tmin, x_min=x_de(tmin), min_Zboa_mpmath=float(abs(zmp)),
                  min_Zboa_rigoroso=minb_inf, R_max_rigoroso=R_sup, intervalos_avaliados=total, niveis=nivel,
                  H1_toda_janela=bool(minb_inf >= 1), H1_falha_provada=bool(abs(zmp) < 1), Hstar_toda_janela=bool(R_sup < 1))
    print(f'n={n}: |Z_boa| minimo pontual {zb[k]:.6f} em x = {x_de(tmin):.4f} (mpmath, 60 digitos: {float(abs(zmp)):.6f}); '
          f'cota inferior rigorosa na janela {minb_inf:.4f}; R maximo rigoroso {R_sup:.4f}; {total} intervalos, {nivel} niveis', flush=True)
    print(f'     H1 (|Z_boa| >= 1 em toda a janela): {"demonstrada" if minb_inf >= 1 else ("FALHA (ponto exato abaixo de 1)" if abs(zmp) < 1 else "nao decidida")};'
          f'  H1* (R < 1 em toda a janela): {"demonstrada" if R_sup < 1 else "nao demonstrada"}')
json.dump(out, open('h1b_B_rigor.json', 'w'), indent=1)
