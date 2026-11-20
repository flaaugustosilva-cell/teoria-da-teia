"""phi_n exato em n = 9 e 10 (PREREGISTRO_N9N10.md) - analise: categorias de classes, H1* na janela, conjectura C1.
Le h1b_N_n{n}.npz e h1b_N_cert_n{n}_t*.npz. Uso: python h1b_N_analise.py 9 10  ->  h1b_N_resultados.json
Pesos 1/|Aut| por classe. |Z_boa| >= |Z_cert| - W_nc quando ha classes sem certificado (W_nc = peso delas)."""
import sys, glob, json, math, numpy as np, mpmath as mp
from e1_comum import C_ACAO, F, lnZ_ruim
A, Bf = 2*np.pi/3, 4*np.pi/3
def x_de(t): return F*math.sqrt(t/2/C_ACAO)
out = {}
for n in map(int, sys.argv[1:]):
    d = np.load(f'h1b_N_n{n}.npz'); B = d['B'].astype(float); h = d['h']; w = 1.0/d['aut'].astype(float)
    est = np.zeros(len(B), np.int8)
    for f in sorted(glob.glob(f'h1b_N_cert_n{n}_t*.npz')):
        s = np.load(f); est[s['indices']] = s['estado']
    boa = h >= 3; cert = boa & (est > 0); nc = boa & (est < 0); nt = boa & (est == 0)
    cat = dict(total=int(len(B)), altura3=int(boa.sum()), cert_passada1=int((boa & (est == 1)).sum()), cert_passada2=int((boa & (est == 2)).sum()),
               sem_certificado=int(nc.sum()), nao_tentadas=int(nt.sum()), demonstradas_nao_embutiveis=0)
    Wnc = float(w[nc | nt].sum())
    def agrega(m):
        v, inv = np.unique(B[m], return_inverse=True); return v, np.bincount(inv, weights=w[m])
    vb, Wb = agrega(cert); vr, Wr = agrega(~boa)
    Db = float(np.sum(Wb*np.abs(vb))); Dr = float(np.sum(Wr*np.abs(vr)))
    Zb = lambda t: np.abs(np.exp(1j*np.outer(t, vb)) @ Wb); Zr = lambda t: np.abs(np.exp(1j*np.outer(t, vr)) @ Wr)
    # conferencia do lado ruim com a formula exata (Teorema 1)
    conf = max(abs(math.log(Zr(np.array([2*b]))[0]) - (lnZ_ruim(n, F*math.sqrt(b/C_ACAO)) - math.lgamma(n + 1))) for b in (1.2, 1.5, 1.9))
    # subdivisao adaptativa (mesmo metodo de h1b_B_rigor.py), com |Z_boa| >= |Z_cert| - W_nc
    c1 = 3**n/math.factorial(n)
    N0 = 20000; r = (Bf - A)/N0/2; c = A + r + 2*r*np.arange(N0); minb = math.inf; Rsup = 0.0; nivel = 0; c1_ponto = False
    while len(c):
        zb = Zb(c) - Wnc; zr = Zr(c); lb = zb - Db*r; ub = zr + Dr*r
        Rb = np.where(lb > 0, ub/np.where(lb > 0, lb, 1), np.inf)
        # fecha o intervalo quando H1* esta garantida nele (Rb < 1) e C1 esta decidida nele:
        # cota inferior acima do limiar, ou um ponto exato abaixo do limiar (refuta C1)
        ok = (Rb < 1.0) & ((lb > c1) | (zb + Wnc <= c1))
        if (ok & (zb + Wnc <= c1)).any(): c1_ponto = True
        if nivel >= 12: ok[:] = True
        if ok.any(): minb = min(minb, float(lb[ok].min())); Rsup = max(Rsup, float(Rb[ok].max()))
        rest = c[~ok]; r /= 10; c = (rest[:, None] + r*(2*np.arange(10) - 9)[None, :]).ravel(); nivel += 1
    t = np.linspace(A, Bf, 400001); zb = Zb(t); k = int(np.argmin(zb)); tmin = float(t[k])
    mp.mp.dps = 60
    v_, inv_ = np.unique(np.column_stack([d['B'][cert], d['aut'][cert]]), axis=0, return_counts=True)
    zmp = abs(mp.fsum(mp.mpf(int(c_))/int(a_)*mp.expj(mp.mpf(tmin)*int(b_)) for (b_, a_), c_ in zip(v_, inv_)))
    out[n] = dict(categorias=cat, W_boa_cert=float(Wb.sum()), W_nc=Wnc, W_ruim=float(Wr.sum()), conferencia_ruim_formula=conf,
                  min_Zboa_pontual=float(zb[k]), min_Zboa_mpmath=float(zmp), x_min=x_de(tmin), min_Zboa_rigoroso=minb, R_max_rigoroso=Rsup,
                  H1_toda_janela=('demonstrada' if minb >= 1 else ('falha' if (Wnc == 0 and zmp < 1) else 'nao decidida')),
                  H1estrela_toda_janela=('demonstrada' if Rsup < 1 else 'nao decidida'), C1_limiar=c1,
                  C1=('refutada' if (Wnc == 0 and zmp <= c1) else ('confirmada' if (minb > c1 and not c1_ponto) else 'nao decidida')))
    o = out[n]; print(f'n={n}: categorias {cat}')
    print(f'   W_boa (certificadas) = {o["W_boa_cert"]:.4f}, W_nc = {Wnc}, W_ruim = {o["W_ruim"]:.4f}; lado ruim x formula: {conf:.1e}')
    print(f'   min |Z_boa| na janela: pontual {o["min_Zboa_pontual"]:.6f} (60 digitos: {o["min_Zboa_mpmath"]:.6f}) em x = {o["x_min"]:.4f}; rigoroso >= {minb:.4f}')
    print(f'   R maximo rigoroso = {Rsup:.4f} -> H1*: {o["H1estrela_toda_janela"]}; H1 (>= 1): {o["H1_toda_janela"]}; C1 (> {c1:.4f}): {o["C1"]}', flush=True)
json.dump(out, open('h1b_N_resultados.json', 'w'), indent=1)
