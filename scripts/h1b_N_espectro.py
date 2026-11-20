"""EXPLORATORIO (fora de registro), 20/11/2026: estrutura espectral de Z_boa(theta) = sum_b W_b e^{i theta b}, n = 5 a 10.
(1) espectro W_b: suporte, media, desvio, assimetria, curtose;
(2) interferencia: com theta = pi + phi, Z = sum_b (-1)^b W_b e^{i phi b}; balanco de paridade W_par - W_impar e
    "aspereza" do espectro (quanto (-1)^b W_b sobrevive a suavizacao);
(3) quase-zeros: minimos locais de |Z_boa| na janela (grade de 400.001 pontos), posicoes e profundidade relativa.
Le h1b_N_n{n}.npz. Uso: python h1b_N_espectro.py"""
import numpy as np, math
from e1_comum import C_ACAO, F
TH = np.linspace(2*np.pi/3, 4*np.pi/3, 400001)
def x_de(t): return F*np.sqrt(t/2/C_ACAO)
for n in range(5, 11):
    d = np.load(f'h1b_N_n{n}.npz'); boa = d['h'] >= 3
    v, inv = np.unique(d['B'][boa], return_inverse=True); W = np.bincount(inv, weights=1.0/d['aut'][boa].astype(float))
    Wt = W.sum(); p = W/Wt; mu = (p*v).sum(); sd = math.sqrt((p*(v - mu)**2).sum())
    sk = (p*(v - mu)**3).sum()/sd**3; ku = (p*(v - mu)**4).sum()/sd**4 - 3
    par = W[v % 2 == 0].sum(); imp = W[v % 2 == 1].sum()
    # aspereza: espectro alternado comparado ao mesmo espectro suavizado (media de vizinhos b-1, b, b+1 numa grade completa)
    b0, b1 = v.min(), v.max(); Wf = np.zeros(b1 - b0 + 1); Wf[v - b0] = W
    alt = ((-1.0)**np.arange(b0, b1 + 1))*Wf
    suave = np.convolve(Wf, [0.25, 0.5, 0.25], mode='same')
    print(f'\nn={n}: W_boa = {Wt:.1f}; B de {b0} a {b1} ({len(v)} valores ocupados de {b1-b0+1}); media {mu:.2f}, desvio {sd:.2f}, assimetria {sk:+.2f}, curtose exc. {ku:+.2f}')
    print(f'  paridade: W_par = {par:.2f}, W_impar = {imp:.2f}; Z_boa(pi) = W_par - W_impar = {par-imp:+.3f} ({(par-imp)/Wt:+.2e} de W)')
    print(f'  aspereza: |sum (-1)^b W_b| / sum W_b = {abs(alt.sum())/Wt:.2e}; parte nao suave: sum|W - suave| / W = {np.abs(Wf - suave).sum()/Wt:.3f}')
    z = np.abs(np.exp(1j*np.outer(TH, v)) @ W)
    loc = np.where((z[1:-1] < z[:-2]) & (z[1:-1] < z[2:]))[0] + 1
    loc = loc[np.argsort(z[loc])][:6]
    print(f'  |Z_boa| na janela: mediana {np.median(z):.2f}, minimo {z.min():.4f}; {len(np.where((z[1:-1] < z[:-2]) & (z[1:-1] < z[2:]))[0])} minimos locais')
    print('  6 minimos locais mais fundos (x: |Z| , |Z|/W): ' + '; '.join(f'{x_de(TH[k]):.3f}: {z[k]:.3g}, {z[k]/Wt:.1e}' for k in loc))
