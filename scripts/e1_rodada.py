"""E1 - rodada principal com os parametros pre-registrados (19/11/2026 02:24). Nao mudar.
Saidas: e1_amostras.npz (B de cada teia boa sorteada) e e1_resultados.csv."""
import json, math, numpy as np
from e1_comum import sorteia_diamante, causal, contagens, B_de, tem_gemeos, beta_de, lnZ_ruim

NS = (40, 80, 120, 160); M = 20000; SEMENTE = 20261119
XS = (0.832, 5.0, 6.0, 7.0, 8.0, 9.0); DENTRO = (6.0, 7.0, 8.0)

amostras = {}; info = {}
for n in NS:
    rng = np.random.default_rng([SEMENTE, n]); Bs = []; ruins = 0; gem = 0
    for _ in range(M):
        C = causal(sorteia_diamante(n, rng)); N, h3 = contagens(C)
        if not h3: ruins += 1; continue                      # altura <= 2: pertence as ruins
        gem += tem_gemeos(C); Bs.append(B_de(n, N))
    Bs = np.array(Bs, dtype=np.int64); amostras[f'n{n}'] = Bs
    info[n] = dict(boas=len(Bs), altura2=ruins, gemeos=int(gem), B_media=float(Bs.mean()), B_desvio=float(Bs.std()))
    print(n, info[n], flush=True)
np.savez_compressed('e1_amostras.npz', **amostras)

def gamma(B, beta):
    z = np.exp(2j*beta*B); m = z.mean()
    se = math.sqrt((z.real.var() + z.imag.var())/len(z)); return abs(m), se

linhas = []
for x in XS:
    b = beta_de(x)
    for n in NS:
        lz400 = lnZ_ruim(n, x, 400); lz800 = lnZ_ruim(n, x, 800)
        lnf = math.lgamma(n + 1); L = lz400 - lnf
        Lrig = lz400 - 4*n*math.log(2*math.e*(n - 1))
        B = amostras[f'n{n}']; g, se = gamma(B, b); g2, se2 = gamma(B[:len(B)//2], b)
        linhas.append(dict(x=x, n=n, beta=b, lnZ_ruim=lz400, dif_precisao=abs(lz800 - lz400), ln_fat=lnf, L=L, L_rig=Lrig,
                           Gamma=g, Gamma_ep=se, Gamma_meia=g2, Gamma_meia_ep=se2))
        print(f'x={x:5.3f} n={n:3d} lnZ={lz400:10.4f} L={L:11.4f} Lrig={Lrig:11.2f} Gamma={g:.4f}+-{se:.4f} (M/2: {g2:.4f}) dprec={abs(lz800-lz400):.1e}', flush=True)
import csv
with open('e1_resultados.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)
json.dump({str(k): v for k, v in info.items()}, open('e1_teias_boas.json', 'w'), indent=1)
