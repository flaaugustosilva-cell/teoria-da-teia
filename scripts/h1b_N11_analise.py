"""Investigacao auxiliar em n = 11 (PREREGISTRO_N11_AUX.md): junta as 20 partes, faz as validacoes e responde A1, A2, A3.
Uso (na pasta das partes): python h1b_N11_analise.py  ->  h1b_N11_resultados.json e o relatorio.
Estatuto: 'nao ruins' = todas as ordens de altura >= 3; NAO e a definicao oficial de teia boa."""
import json, math, numpy as np, mpmath as mp
from collections import defaultdict
from e1_comum import C_ACAO, F, lnZ_ruim
n = 11; fat = math.factorial(n); A, Bf = 2*np.pi/3, 4*np.pi/3
def x_de(t): return F*math.sqrt(t/2/C_ACAO)
W = defaultdict(int); classes = 0; tot = 0; con = 0
for x in range(20):
    d = np.load(f'h1b_N11_n{n}_parte{x}.npz'); classes += int(d['total_classes'])
    for (b, h3, c), w in zip(d['chaves'], d['peso']):
        w = int(w); W[(int(b), int(h3))] += w; tot += w; con += w if c else 0
val = {'classes': (classes, 46749427), 'rotuladas': (tot, 1396281677105899), 'conexas': (con, 1320327172853172)}
Tr = sum(((-1)**((b - n) % 2))*w for (b, h3), w in W.items() if not h3)
Tnr = sum(((-1)**((b - n) % 2))*w for (b, h3), w in W.items() if h3)
print('VALIDACOES:')
for k, (a, e) in val.items(): print(f'  {k}: {a} (esperado {e}) -> {a == e}')
print(f'  T_11(ruim) = {Tr} (esperado +1, Teorema 1\') -> {Tr == 1}')
vr = np.array(sorted(b for (b, h3) in W if not h3), float); Wr = np.array([W[(int(b), 0)] for b in vr], float)/fat
vb = np.array(sorted(b for (b, h3) in W if h3), float); Wb = np.array([W[(int(b), 1)] for b in vb], float)/fat
conf = max(abs(math.log(abs(np.exp(1j*2*b*vr) @ Wr)) - (lnZ_ruim(n, F*math.sqrt(b/C_ACAO)) - math.lgamma(n + 1))) for b in (1.2, 1.5, 1.9))
print(f'  lado ruim x formula do E1: maior diferenca em ln|Z| = {conf:.1e} -> {conf < 1e-6}')
ok = all(a == e for a, e in val.values()) and Tr == 1 and conf < 1e-6
print(f'  TODAS AS VALIDACOES: {ok}')
assert ok, 'validacao falhou: A1-A3 nao serao respondidas'
# A1
c1 = 3**n/fat
print(f'\nA1 (centro): T_11(nao ruim) = {Tnr}; |T| > 3^11 = {3**n}? -> {abs(Tnr) > 3**n}')
# A2 e A3 (mesmo metodo de h1b_N_analise.py, com W_nc = 0)
Db = float(np.sum(Wb*np.abs(vb))); Dr = float(np.sum(Wr*np.abs(vr)))
def _Z(t, v, w):   # avaliacao em blocos de 20.000 angulos (mesmo resultado, menos memoria)
    t = np.asarray(t); return np.concatenate([np.abs(np.exp(1j*np.outer(t[i:i+20000], v)) @ w) for i in range(0, len(t), 20000)]) if len(t) else np.zeros(0)
Zb = lambda t: _Z(t, vb, Wb); Zr = lambda t: _Z(t, vr, Wr)
N0 = 20000; r = (Bf - A)/N0/2; c = A + r + 2*r*np.arange(N0); minb = math.inf; Rsup = 0.0; nivel = 0; c1_ponto = False; a3_ponto = False; forcado = False
while len(c):
    zb = Zb(c); zr = Zr(c); lb = zb - Db*r; ub = zr + Dr*r
    Rb = np.where(lb > 0, ub/np.where(lb > 0, lb, 1), np.inf)
    Rp = zr/np.maximum(zb, 1e-300)                     # razao exata no ponto central
    a3_ponto = a3_ponto or bool((Rp >= 1.0).any())     # um ponto exato com R >= 1 ja refuta A3
    ok_ = ((Rb < 1.0) | (Rp >= 1.0)) & ((lb > c1) | (zb <= c1))
    if (ok_ & (zb <= c1)).any(): c1_ponto = True
    if nivel >= 12 or len(c) > 2_000_000: ok_[:] = True; forcado = True   # teto de profundidade e de memoria
    if ok_.any():
        minb = min(minb, float(lb[ok_].min())); fin = Rb[ok_ & (Rp < 1.0)]
        if len(fin): Rsup = max(Rsup, float(fin.max()))
    rest = c[~ok_]; r /= 10; c = (rest[:, None] + r*(2*np.arange(10) - 9)[None, :]).ravel(); nivel += 1
t = np.linspace(A, Bf, 400001); z = Zb(t); k = int(np.argmin(z)); tmin = float(t[k])
mp.mp.dps = 60
zmp = abs(mp.fsum(mp.mpf(W[(int(b), 1)])/fat*mp.expj(mp.mpf(tmin)*int(b)) for b in vb))
A2 = 'falha' if zmp <= c1 else ('vale' if (minb > c1 and not c1_ponto) else 'nao decidida')
tr = np.linspace(A, Bf, 400001); Rg = Zr(tr)/Zb(tr); kr = int(np.argmax(Rg))
A3 = 'falha' if (a3_ponto or Rg[kr] >= 1) else ('vale' if (Rsup < 1 and not forcado) else 'nao decidida')
print(f'   R_aux maximo pontual na grade = {Rg[kr]:.3e} em x = {x_de(float(tr[kr])):.4f}; refinamento forcado: {forcado}')
print(f'A2 (analogo de C1): min |Z_nao-ruim| pontual {z[k]:.6f} (60 digitos {float(zmp):.6f}) em x = {x_de(tmin):.4f}; cota rigorosa >= {minb:.4f}; limiar {c1:.6f} -> {A2}')
print(f'A3 (analogo de H1*): R_aux maximo rigoroso = {Rsup:.4f} -> {A3}')
# descricao de W_b (sem valor de teste)
p = Wb/Wb.sum(); mu = (p*vb).sum(); sd = math.sqrt((p*(vb - mu)**2).sum())
sk = (p*(vb - mu)**3).sum()/sd**3; ku = (p*(vb - mu)**4).sum()/sd**4 - 3
b0, b1 = int(vb.min()), int(vb.max()); Wf = np.zeros(b1 - b0 + 1); Wf[(vb - b0).astype(int)] = Wb
suave = np.convolve(Wf, [0.25, 0.5, 0.25], mode='same')
print(f'\nDescritivo: W_nao-ruim = {Wb.sum():.1f}; B de {b0} a {b1} ({len(vb)} valores ocupados de {b1-b0+1}); desvio {sd:.2f}, assimetria {sk:+.2f}, curtose exc. {ku:+.2f}; '
      f'parte nao suave {np.abs(Wf - suave).sum()/Wb.sum():.3f}; mediana de |Z|/W na janela {np.median(z)/Wb.sum():.2e}')
json.dump(dict(validacoes={k: list(v) for k, v in val.items()}, T_ruim=Tr, T_nao_ruim=str(Tnr), conferencia_formula=conf,
               A1=bool(abs(Tnr) > 3**n), A2=A2, A3=A3, min_pontual=float(z[k]), min_60_digitos=float(zmp), x_min=x_de(tmin),
               cota_rigorosa=minb, limiar_C1=c1, R_max_rigoroso=Rsup, W_nao_ruim=float(Wb.sum()), W_ruim=float(Wr.sum())),
          open('h1b_N11_resultados.json', 'w'), indent=1)
