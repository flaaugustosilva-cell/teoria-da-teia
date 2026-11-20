"""Consolidacao de E (E2) - analise com os criterios de dados/h1b/PREREGISTRO_E2.md (commit 5a3427b).
Le h1b_E2_n{n}.npz. Uso: python h1b_E2_analise.py  ->  h1b_E2_resultados.json, h1b_E2_tabela.csv e o relatorio.
Escopo: so o sorteio; nenhum resultado aqui e evidencia sobre H1*."""
import csv, json, math, numpy as np
NS = (10, 20, 40, 80, 160); NT1 = (20, 40, 80, 160); US = np.round(np.arange(1, 41)*0.1, 1); G = 50
dados = {n: np.load(f'h1b_E2_n{n}.npz') for n in NS}

def Q_err(B, th):
    z = np.exp(1j*th*B.astype(np.float64)); N = len(z)
    bl = np.array_split(np.arange(N), G); sb = np.array([z[b].sum() for b in bl]); nb = np.array([len(b) for b in bl])
    S = sb.sum(); Q = (abs(S)**2/N - 1)/(N - 1); Sk = S - sb; Nk = N - nb; Qk = (np.abs(Sk)**2/Nk - 1)/(Nk - 1)
    ej = math.sqrt((G - 1)/G*np.sum((Qk - Qk.mean())**2)); return float(Q), max(ej, math.sqrt(2)/N), ej

tab = {}; linhas = []
for n in NS:
    B = dados[n]['B']; sd = float(B.std())
    for u in US:
        Q, e, ej = Q_err(B, u/sd); tab[(n, u)] = (Q, e)
        linhas.append(dict(n=n, u=u, theta=u/sd, Q=Q, erro=e, erro_jackknife=ej, gauss=math.exp(-u*u), resolvido=Q > 4*e))
with open('h1b_E2_tabela.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0])); w.writeheader(); w.writerows(linhas)
res = lambda n, u: tab[(n, u)][0] > 4*tab[(n, u)][1]
out = {}
print('=== Q por u (* = resolvido); entre parenteses, e^(-u^2) ===')
for u in US[::2]:
    print(f' u={u:3.1f} ({math.exp(-u*u):.2e}): ' + '  '.join(f"n={n}: {tab[(n,u)][0]:+.2e}{'*' if res(n,u) else ' '}" for n in NS))
# T1
comp = []
for i, a in enumerate(NT1):
    for b in NT1[i+1:]:
        for u in US:
            if res(a, u) and res(b, u):
                (qa, ea), (qb, eb) = tab[(a, u)], tab[(b, u)]
                comp.append(dict(a=a, b=b, u=float(u), desvio=abs(math.log(qa) - math.log(qb))/math.hypot(ea/qa, eb/qb)))
f1 = float(np.mean([c['desvio'] <= 3 for c in comp])) if comp else float('nan')
v1 = 'inconclusivo' if len(comp) < 10 else ('confirmado' if f1 >= 0.8 else 'nao confirmado')
out['T1'] = dict(comparacoes=len(comp), fracao=f1, veredito=v1, detalhe=comp)
print(f'\nT1 colapso em u: {len(comp)} comparacoes, {f1:.0%} dentro de 3 erros -> {v1}')
for a, b in [(20, 40), (40, 80), (80, 160), (20, 160)]:
    cs = [c for c in comp if c['a'] == a and c['b'] == b]
    if cs: print(f'   n={a} x n={b}: {len(cs)} pontos, mediana do desvio {np.median([c["desvio"] for c in cs]):.1f}, maximo {max(c["desvio"] for c in cs):.1f} (u ate {max(c["u"] for c in cs):.1f})')
# T2
p2 = [(n, u) for n in NS for u in US if u <= 1.0 and res(n, u)]
d2 = [abs(tab[k][0] - math.exp(-k[1]**2))/tab[k][1] for k in p2]
f2 = float(np.mean([d <= 3 for d in d2])) if d2 else float('nan'); v2 = 'confirmado' if d2 and f2 >= 0.8 else ('inconclusivo' if not d2 else 'nao confirmado')
out['T2'] = dict(pontos=len(p2), fracao=f2, veredito=v2, desvios=d2)
print(f'\nT2 nucleo gaussiano (u <= 1): {len(p2)} pontos, {f2:.0%} dentro de 3 erros -> {v2}')
for n in NS:
    ds = [abs(tab[(n,u)][0] - math.exp(-u*u))/tab[(n,u)][1] for u in US if u <= 1.0 and res(n, u)]
    print(f'   n={n}: desvio maximo {max(ds):.1f} erros; Q/e^(-u^2) em u = 1: {tab[(n,1.0)][0]/math.exp(-1):.4f}')
# T3
p3 = [(n, u) for n in NS for u in US if u >= 2.0 and res(n, u)]
d3 = [(tab[k][0] - math.exp(-k[1]**2))/tab[k][1] for k in p3]
f3 = float(np.mean([d > 3 for d in d3])) if d3 else float('nan')
v3 = 'inconclusivo' if len(p3) < 5 else ('confirmado' if f3 >= 0.8 else 'nao confirmado')
out['T3'] = dict(pontos=len(p3), fracao=f3, veredito=v3)
print(f'\nT3 cauda nao gaussiana (u >= 2): {len(p3)} pontos resolvidos, {f3:.0%} acima de e^(-u^2) por mais de 3 erros -> {v3}')
for n in NS:
    us = [u for u in US if u >= 2.0 and res(n, u)]
    if us: print(f'   n={n}: resolvidos ate u = {max(us):.1f}; em u = {max(us):.1f}: Q = {tab[(n,max(us))][0]:.2e} contra e^(-u^2) = {math.exp(-max(us)**2):.2e}')
    else: print(f'   n={n}: nenhum ponto resolvido com u >= 2')
# T4
print('\nT4 origem da variancia de B (fracoes de Var(B)):')
c = np.array([-1, 9, -16, 8]); t4 = {}
for n in NS:
    S = np.cov(dados[n]['N'].T.astype(float)); VB = float(c @ S @ c)
    V12 = 81*S[1, 1] + 256*S[2, 2] - 288*S[1, 2]
    dec = {f'N{i}': c[i]**2*S[i, i]/VB for i in range(4)}
    t4[n] = dict(VarB=VB, V12_sobre_VarB=V12/VB, diagonais=dec, cov_N1N2=-288*S[1, 2]/VB)
    print(f'   n={n:3d}: Var(B) = {VB:9.1f}; V12/Var(B) = {V12/VB:.3f}; diagonais N0 {dec["N0"]:.2f}, N1 {dec["N1"]:.2f}, N2 {dec["N2"]:.2f}, N3 {dec["N3"]:.2f}; termo -288 Cov(N1,N2) = {-288*S[1,2]/VB:+.2f}')
v4 = 'confirmado' if all(t4[n]['V12_sobre_VarB'] >= 0.8 for n in (40, 80, 160)) else 'nao confirmado'
out['T4'] = dict(por_n=t4, veredito=v4); print(f'   -> {v4}')
print(f'\n=== VEREDITOS (so sobre o sorteio): T1 {v1}; T2 {v2}; T3 {v3}; T4 {v4} ===')
json.dump(out, open('h1b_E2_resultados.json', 'w'), indent=1, default=float)
