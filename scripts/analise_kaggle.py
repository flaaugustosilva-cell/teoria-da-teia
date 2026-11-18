"""Analise das rodadas grandes no Kaggle (18/11/2026): regra da maior anticadeia, 2+1, metodo rapido com erro de 0,1%."""
import numpy as np
from math import pi
D = {4000: [(31.71,38.34,37.20),(12.32,26.91,35.57),(36.22,41.08,42.04),(19.32,41.87,53.41),(25.64,36.27,41.81),(20.47,43.64,53.65),(24.61,26.84,37.58),(19.44,29.99,36.16)],
     8000: [(25.52,52.45,58.60),(40.70,54.20,64.70),(39.71,48.03,59.30),(34.12,50.18,61.35),(40.58,63.33,69.00),(38.00,51.85,71.19)],
     16000:[(37.57,66.83,85.08),(45.79,71.66,93.03),(52.67,63.41,82.48),(41.90,74.76,95.30)],
     24000:[(62.90,87.05,104.47),(47.04,87.46,103.47)]}
AS = (0.2, 0.315, 0.45); Ns = np.array(sorted(D))
mol = lambda N, a: 0.218853*((N/(pi/12))**(1/3))*pi*a
print('   N   rod.  ' + '   '.join(f'S(a={a})       ' for a in AS))
M = {a: [] for a in AS}; E = {a: [] for a in AS}
for N in Ns:
    x = np.array(D[N]); m = x.mean(0); e = x.std(0, ddof=1)/np.sqrt(len(x))
    for i, a in enumerate(AS): M[a].append(m[i]); E[a].append(e[i])
    print(f'{N:6d}  {len(x)}   ' + '   '.join(f'{m[i]:6.1f} +- {e[i]:4.1f}' for i in range(3)))
for a in AS:
    S = np.array(M[a]); w = 1/np.array(E[a])
    k = np.polyfit(np.log(Ns), np.log(S), 1, w=w*S)[0]
    mo = np.array([mol(N, a) for N in Ns]); c, b = np.polyfit(mo, S, 1, w=w)
    print(f'a = {a}: S ~ N^{k:.2f} (lei de area 0,33);  S/moleculas = ' + ', '.join(f'{s/m:.2f}' for s, m in zip(S, mo))
          + f';  reta S = {c:.2f}*moleculas {b:+.1f}')
print('\nComparacao de formas (qui-quadrado; menor = ajusta melhor):')
from scipy.optimize import curve_fit
for a in AS:
    S = np.array(M[a]); e = np.array(E[a]); e[e < 1] = 1.0   # piso de erro para N = 24000 (2 rodadas)
    f1 = lambda N, c, b: c*N**(1/3) + b                        # lei de area + constante
    f2 = lambda N, c, n0: c*N**(1/3)*np.log(N/n0)               # area x log
    f3 = lambda N, c, k: c*N**k                                 # potencia livre
    out = []
    for f, p0 in ((f1, (1, 0)), (f2, (0.5, 100)), (f3, (1, 0.4))):
        p, _ = curve_fit(f, Ns, S, p0=p0, sigma=e, maxfev=20000); out.append(np.sum(((f(Ns, *p) - S)/e)**2))
    print(f'a = {a}: area+constante {out[0]:.2f} | area x log {out[1]:.2f} | potencia livre {out[2]:.2f}')
