"""Analise pre-registrada do teste de H1 (19/11/2026, ~13:45).
Le os histogramas h1_hist_d*_s*.npz (pasta atual) e ../dados/e1/e1_resultados.csv.
Uso (de dentro de scripts, depois de h1_robustez.py): python h1_ajuste.py
Saida: h1_resultados.csv, h1_ajustes.csv e o resumo na tela."""
import csv, math, os, numpy as np
from e1_comum import beta_de

NS = (6, 8, 10, 12, 14, 16, 20, 24, 28, 32); XS = (6.0, 7.0, 8.0, 0.832, 9.0); DENTRO = (6.0, 7.0, 8.0)
CASOS = [(4, 20261120), (4, 7777), (3, 20261120), (2, 20261120)]
C2E2 = math.log(2*math.e**2)
E1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dados', 'e1', 'e1_resultados.csv')
Lr = {(float(d['x']), int(d['n'])): float(d['L']) for d in csv.DictReader(open(E1))}
def T_H1(n): return -math.lgamma(n + 1) + C2E2
def T_H1s(n, x): return Lr[(x, n)] - math.lgamma(n + 1) + C2E2

MODELOS = {'a: -g n': lambda n: n, 'b: -g n ln n': lambda n: n*np.log(n), 'c: -k n^2': lambda n: n**2}
def ajusta(ns, y, s, f):
    X = np.column_stack([np.ones(len(ns)), -f(np.asarray(ns, float))]); W = 1/np.asarray(s)**2
    A = X.T @ (W[:, None]*X); coef = np.linalg.solve(A, X.T @ (W*y)); cov = np.linalg.inv(A)
    chi2 = float(np.sum(W*(y - X @ coef)**2)); return coef, np.sqrt(np.diag(cov)), chi2

linhas = []; ajustes = []
for d, sem in CASOS:
    H = np.load(f'h1_hist_d{d}_s{sem}.npz')
    for x in XS:
        th = 2*beta_de(x); pts = []
        for n in NS:
            B = H[f'n{n}_B']; c = H[f'n{n}_cont']; N = c.sum(); z = np.exp(1j*th*B)
            m = np.sum(c*z)/N; g = abs(m); se = math.sqrt(max(1 - g*g, 0)/N)
            row = dict(d=d, semente=sem, x=x, n=n, N=int(N), Gamma=g, ep=se, valido=g > 4*se)
            if f'n{n}_peso' in H.files and f'n{n}_peso2' in H.files:
                w = H[f'n{n}_peso']; w2 = H[f'n{n}_peso2']; R = np.sum(w*z)/w.sum()
                row.update(Gamma_w=abs(R), ep_w=math.sqrt(np.sum(w2*np.abs(z - R)**2))/w.sum())
            linhas.append(row)
            if row['valido']: pts.append((n, math.log(g), se/g))
        if len(pts) < 4:
            ajustes.append(dict(d=d, semente=sem, x=x, modelo='-', pontos=len(pts), veredito='inconclusivo')); continue
        ns, y, s = map(np.array, zip(*pts)); vered = []
        for nome, f in MODELOS.items():
            coef, ep, chi2 = ajusta(ns, y, s, f)
            ex = {n: coef[0] - coef[1]*f(np.array(float(n))) for n in (40, 80, 120, 160)}
            a_h1 = ex[160] > T_H1(160); a_h1s = (ex[160] > T_H1s(160, x)) if x in DENTRO else None
            kc = (coef[0] - T_H1(160))/160**2 if nome.startswith('c') else None
            ajustes.append(dict(d=d, semente=sem, x=x, modelo=nome, pontos=len(pts), a=coef[0], taxa=coef[1], ep_taxa=ep[1],
                                chi2_por_gl=chi2/max(len(pts) - 2, 1), ext40=ex[40], ext80=ex[80], ext120=ex[120], ext160=ex[160],
                                limiar_H1_160=T_H1(160), limiar_H1s_160=T_H1s(160, x) if x in DENTRO else '',
                                acima_H1=a_h1, acima_H1s=a_h1s, kappa_critico_H1=kc if kc is not None else ''))
            vered.append((a_h1, a_h1s))
        if x in DENTRO:
            v = 'H1 sustentada (proxy)' if all(a for a, _ in vered) else ('H1 em risco' if all(b for _, b in vered) else 'E1 em risco')
        else: v = 'controle'
        for a in ajustes[-3:]: a['veredito'] = v

with open('h1_resultados.csv', 'w', newline='') as f:
    campos = sorted({k for r in linhas for k in r}, key=lambda k: list(linhas[0]).index(k) if k in linhas[0] else 99)
    w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(linhas)
with open('h1_ajustes.csv', 'w', newline='') as f:
    campos = list(max(ajustes, key=len)); w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(ajustes)

print('Gamma (valido = > 4 erros padrao); [*] = valido')
for d, sem in CASOS:
    for x in XS:
        rs = [r for r in linhas if r['d'] == d and r['semente'] == sem and r['x'] == x]
        print(f' d={d} s={sem:8d} x={x:5.3f}: ' + ' '.join(f"{r['n']}:{r['Gamma']:.4f}{'*' if r['valido'] else ''}" for r in rs))
print('\nAjustes e veredito:')
for a in ajustes:
    if a['modelo'] == '-': print(f" d={a['d']} s={a['semente']} x={a['x']}: {a['pontos']} pontos validos -> {a['veredito']}"); continue
    print(f" d={a['d']} s={a['semente']} x={a['x']} {a['modelo']:13s} pts={a['pontos']} taxa={a['taxa']:.4f}+-{a['ep_taxa']:.4f} chi2/gl={a['chi2_por_gl']:.2f}"
          f" ext160={a['ext160']:9.2f} (H1 {a['limiar_H1_160']:.1f}) -> {a['veredito']}"
          + (f"  kappa_crit={a['kappa_critico_H1']:.4f}" if a['kappa_critico_H1'] != '' else ''))
print('\nConcordancia entre sementes (3+1), pontos validos nas duas:')
for x in XS:
    a = {r['n']: r for r in linhas if r['d'] == 4 and r['semente'] == 20261120 and r['x'] == x and r['valido']}
    b = {r['n']: r for r in linhas if r['d'] == 4 and r['semente'] == 7777 and r['x'] == x and r['valido']}
    zs = [abs(math.log(a[n]['Gamma']) - math.log(b[n]['Gamma']))/math.hypot(a[n]['ep']/a[n]['Gamma'], b[n]['ep']/b[n]['Gamma']) for n in a if n in b]
    print(f' x={x}: {len(zs)} pontos, maior desvio = {max(zs) if zs else float("nan"):.2f} erros combinados')
print('\nPeso 1/|Aut| (3+1, semente 20261120): |Gamma_w - Gamma| em erros combinados')
for x in XS:
    rs = [r for r in linhas if r['d'] == 4 and r['semente'] == 20261120 and r['x'] == x and 'Gamma_w' in r]
    print(f' x={x}: ' + ' '.join(f"{r['n']}:{abs(r['Gamma_w']-r['Gamma'])/math.hypot(r['ep'], r['ep_w']):.1f}" for r in rs))
