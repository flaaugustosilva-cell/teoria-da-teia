"""H1, segunda etapa, entrega C - analise descritiva (DECISOES_H1STAR.md): sem ajuste de modelo e sem veredito.
Le h1b_C_n{n}.npz. Uso: python h1b_C_analise.py  ->  h1b_C_resultados.csv e a tabela na tela.
Q = estimador sem vies de |phi_sorteio|^2; erro por jackknife em 50 blocos; IC 95% = Q +- 1,96 ep; resolvido se Q > 4 ep."""
import csv, math, numpy as np
from e1_comum import C_ACAO, F
NS = (6, 8, 10, 12, 14, 16, 20, 24); TH = np.linspace(2*np.pi/3, 4*np.pi/3, 21)
def x_de(t): return F*math.sqrt(t/2/C_ACAO)
linhas = []
for n in NS:
    d = np.load(f'h1b_C_n{n}.npz'); H = d['hist'].astype(float); v = np.arange(H.shape[1]) - int(d['offset'])
    nb = H.sum(1); N = nb.sum(); G = len(nb)
    for t in TH:
        sb = H @ np.exp(1j*t*v); S = sb.sum()
        Q = (abs(S)**2/N - 1)/(N - 1); Sk = S - sb; Nk = N - nb; Qk = (np.abs(Sk)**2/Nk - 1)/(Nk - 1)
        ep = math.sqrt((G - 1)/G*np.sum((Qk - Qk.mean())**2))
        linhas.append(dict(n=n, theta=t, x=x_de(t), validas=int(N), Q=Q, ep=ep, ic_inf=Q - 1.96*ep, ic_sup=Q + 1.96*ep, resolvido=Q > 4*ep))
with open('h1b_C_resultados.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)
print('Q (|phi_sorteio|^2 sem vies) na janela; * = resolvido (Q > 4 ep); entre colchetes, o erro')
print('  theta   x     ' + ''.join(f'{"n="+str(n):>22s}' for n in NS))
for i, t in enumerate(TH):
    print(f'  {t:.3f} {x_de(t):5.2f}  ' + ''.join(
        f"{r['Q']:>11.2e}[{r['ep']:.0e}]{'*' if r['resolvido'] else ' '}" for r in linhas if abs(r['theta'] - t) < 1e-12))
print('\nResolvidos por n: ' + ', '.join(f"n={n}: {sum(r['resolvido'] for r in linhas if r['n'] == n)}/21" for n in NS))
print('Validas por n: ' + ', '.join(f"n={n}: {next(r['validas'] for r in linhas if r['n'] == n)}" for n in NS))
