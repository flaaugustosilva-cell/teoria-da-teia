"""H1, segunda etapa, entrega E - analise com os criterios do pre-registro (dados/h1b/PREREGISTRO.md, commit 8b30242).
Le h1b_E_n{n}.npz (pasta atual). Uso: python h1b_E_analise.py   ->  h1b_E_resultados.json e o relatorio na tela.
Definicao fixada antes de ver qualquer resultado de E (nao estava explicita no registro): no teste de estrutura
fina, "dentro de 3 erros" usa o erro combinado sqrt(ep_medida^2 + ep_parametros^2 + termos_k^2)."""
import json, math, numpy as np
from scipy import stats
from e1_comum import beta_de

NS = (10, 20, 40, 80, 160); NC = (40, 80, 160)
TH_PEQ = (0.01, 0.02, 0.03, 0.045, 0.06, 0.08, 0.10, 0.13, 0.16, 0.20, 0.25, 0.32)
TH_FINA = (0.5, 0.75, 1.0); NF = (10, 20, 40)
JAN = {'x=6': 2*beta_de(6.0), 'x=7': 2*beta_de(7.0), 'x=8': 2*beta_de(8.0)}
G = 50; rng = np.random.default_rng(0)   # rng so para o bootstrap de E2
dados = {n: np.load(f'h1b_E_n{n}.npz') for n in NS}

def Q_ep(B, th):
    """Estimador sem vies de |phi|^2 e erro por jackknife em G blocos contiguos."""
    z = np.exp(1j*th*B.astype(np.float64)); N = len(z)
    blocos = np.array_split(np.arange(N), G); s = np.array([z[b].sum() for b in blocos]); nb = np.array([len(b) for b in blocos])
    S = s.sum(); Q = (abs(S)**2/N - 1)/(N - 1)
    Sk = S - s; Nk = N - nb; Qk = (np.abs(Sk)**2/Nk - 1)/(Nk - 1)
    ep = math.sqrt((G - 1)/G*np.sum((Qk - Qk.mean())**2)); return float(Q), float(ep)

out = {'E1': {}, 'E2': {}, 'E3': {}}
# ---------------- E1: modo global
print('=== E1: regressao de B em R, R^2, h, minimais, maximais ===')
vres = []; vB = []
for n in NS:
    d = dados[n]; B = d['B'].astype(float)
    X = np.column_stack([d['R'], d['R'].astype(float)**2, d['h'], d['mmin'], d['mmax']]).astype(float)
    X = (X - X.mean(0))/np.where(X.std(0) > 0, X.std(0), 1); X = np.column_stack([np.ones(len(B)), X])
    coef, *_ = np.linalg.lstsq(X, B, rcond=None); res = B - X @ coef
    R2 = 1 - res.var()/B.var(); vres.append(res.var()); vB.append(B.var())
    out['E1'][n] = dict(R2=R2, var_B=B.var(), var_residuo=res.var(), validas=len(B), sorteios=int(d['sorteios']), descartadas=int(d['descartadas']))
    print(f' n={n:3d}: validas {len(B):7d} (descartadas {int(d["descartadas"])}), Var(B) = {B.var():10.1f}, R2 = {R2:.4f}, Var(residuo) = {res.var():9.1f}')
lg = np.log(NS); a_res = np.polyfit(lg, np.log(vres), 1)[0]; a_B = np.polyfit(lg, np.log(vB), 1)[0]
modo = all(out['E1'][n]['R2'] >= 0.90 for n in NC); local = a_res <= 1.2
out['E1'].update(expoente_var_residuo=a_res, expoente_var_B=a_B, modo_global_identificado=modo, residuo_local=local)
print(f' expoente de Var(B) em n: {a_B:.3f}; de Var(residuo): {a_res:.3f}')
print(f' -> modo global identificado (R2 >= 0,90 em 40, 80, 160): {modo}; residuo local (expoente <= 1,2): {local}')

# ---------------- E2: distribuicao
print('\n=== E2: distribuicao de X = (B - media)/desvio ===')
Xs = {}
for n in NS:
    B = dados[n]['B'].astype(float); X = (B - B.mean())/B.std(); Xs[n] = X
    sk = stats.skew(X); ku = stats.kurtosis(X)
    bs = []
    for _ in range(200):
        Y = X[rng.integers(0, len(X), len(X))]; bs.append((stats.skew(Y), stats.kurtosis(Y)))
    bs = np.array(bs); ic = np.percentile(bs, [2.5, 97.5], axis=0)
    t3 = float(np.mean(np.abs(X) > 3)); t4 = float(np.mean(np.abs(X) > 4))
    out['E2'][n] = dict(assimetria=sk, assim_ic=list(ic[:, 0]), curtose_exc=ku, curt_ic=list(ic[:, 1]), cauda3=t3, cauda4=t4)
    print(f' n={n:3d}: assimetria {sk:+.3f} [{ic[0,0]:+.3f}, {ic[1,0]:+.3f}]  curtose exc. {ku:+.3f} [{ic[0,1]:+.3f}, {ic[1,1]:+.3f}]'
          f'  P(|X|>3) = {t3:.5f} (gauss. 0,00270)  P(|X|>4) = {t4:.6f} (gauss. 0,000063)')
ks = stats.ks_2samp(Xs[80], Xs[160]); out['E2']['KS_80_160'] = dict(D=ks.statistic, p=ks.pvalue)
gauss = abs(out['E2'][160]['assimetria']) < 0.1 and abs(out['E2'][160]['curtose_exc']) < 0.2
out['E2']['compativel_gaussiana'] = gauss
print(f' KS entre n = 80 e 160: D = {ks.statistic:.4f}, p = {ks.pvalue:.3g}; compativel com gaussiana (n = 160): {gauss}')

# ---------------- E3: decaimento
print('\n=== E3: Q (estimador sem vies de |phi|^2) em angulos pequenos; * = valido (Q > 4 ep) ===')
tab = {}
for n in NS:
    for th in TH_PEQ + TH_FINA + tuple(JAN.values()):
        tab[(n, th)] = Q_ep(dados[n]['B'], th)
for n in NS:
    print(f' n={n:3d}: ' + '  '.join(f"{th}:{tab[(n,th)][0]:.3g}{'*' if tab[(n,th)][0] > 4*tab[(n,th)][1] else ''}" for th in TH_PEQ))
pts = {n: sorted([(n*th, *tab[(n, th)]) for th in TH_PEQ if tab[(n, th)][0] > 4*tab[(n, th)][1]]) for n in NC}
abaixo = {n: [th for th in TH_PEQ if not tab[(n, th)][0] > 4*tab[(n, th)][1]] for n in NS}
# colapso
comp = []
for a in NC:
    for b in NC:
        if a == b or len(pts[a]) < 2: continue
        wa = np.array([p[0] for p in pts[a]]); la = np.log([p[1] for p in pts[a]]); sa = np.array([p[2]/p[1] for p in pts[a]])
        for w, q, e in pts[b]:
            if wa[0] <= w <= wa[-1]:
                yi = np.interp(w, wa, la); si = np.interp(w, wa, sa)
                comp.append(abs(math.log(q) - yi)/math.hypot(e/q, si))
frac = float(np.mean(np.array(comp) <= 3)) if comp else float('nan')
colapso = bool(comp) and frac >= 0.8
print(f'\n Colapso (n = 40, 80, 160): {len(comp)} comparacoes, {frac:.0%} dentro de 3 erros -> aceito: {colapso}')
print(f'   desvios (em erros combinados): ' + ' '.join(f'{z:.1f}' for z in comp))
# modelos
W = np.array([p[0] for n in NC for p in pts[n]]); Y = 0.5*np.log([p[1] for n in NC for p in pts[n]])
S = np.array([p[2]/(2*p[1]) for n in NC for p in pts[n]])
base = {'gaussiano': lambda w: w**2, 'exponencial': lambda w: w, 'potencia': lambda w: np.log(w)}
fits = {}
for nome, f in base.items():
    X = np.column_stack([np.ones_like(W), -f(W)]); Wt = 1/S**2; A = X.T @ (Wt[:, None]*X)
    c = np.linalg.solve(A, X.T @ (Wt*Y)); cov = np.linalg.inv(A); chi2 = float(np.sum(Wt*(Y - X @ c)**2))
    fits[nome] = dict(a=c[0], taxa=c[1], cov=cov.tolist(), chi2=chi2, gl=len(W) - 2, AIC=chi2 + 4)
ordem = sorted(fits, key=lambda k: fits[k]['AIC']); melhor = ordem[0]; dAIC = fits[ordem[1]]['AIC'] - fits[melhor]['AIC']
decisivo = dAIC >= 10
print(f'\n Ajuste de ln|phi| = 0,5 ln Q contra omega ({len(W)} pontos validos de n = 40, 80, 160; omega de {W.min():.2f} a {W.max():.2f}):')
for k in ordem: print(f'   {k:11s}: a = {fits[k]["a"]:+.4f}, taxa = {fits[k]["taxa"]:.4f}, chi2/gl = {fits[k]["chi2"]/max(fits[k]["gl"],1):.2f}, AIC = {fits[k]["AIC"]:.1f}')
print(f'   melhor: {melhor}; diferenca de AIC para o segundo: {dAIC:.1f} -> decisivo: {decisivo}')
# estrutura fina
fb = base[melhor]; ca, ct = fits[melhor]['a'], fits[melhor]['taxa']; cov = np.array(fits[melhor]['cov'])
def g(w): return math.exp(ca - ct*fb(np.array(float(w))))
fina = []
for n in NF:
    for th in TH_FINA:
        q, e = tab[(n, th)]; w0 = n*th; g0 = g(w0); qp = g0**2
        J = np.array([1.0, -float(fb(np.array(w0)))]); dy = math.sqrt(J @ cov @ J); dq = 2*qp*dy
        al = (g0 + g(n*abs(th - 2*math.pi)) + g(n*(th + 2*math.pi)))**2 - qp
        err = math.sqrt(e*e + dq*dq + al*al); val = q > 4*e
        fina.append(dict(n=n, theta=th, Q=q, ep=e, valido=val, Q_prev=qp, erro_comb=err, desvio=abs(q - qp)/err))
vf = [f for f in fina if f['valido']]; frac_f = float(np.mean([f['desvio'] <= 3 for f in vf])) if vf else float('nan')
fina_ok = bool(vf) and frac_f >= 0.8
print(f'\n Estrutura fina (modelo {melhor}):')
for f in fina: print(f"   n={f['n']:2d} theta={f['theta']:.2f}: Q = {f['Q']:.3e} +- {f['ep']:.1e}{' (valido)' if f['valido'] else ' (abaixo da resolucao)'}  previsto {f['Q_prev']:.3e}  desvio {f['desvio']:.1f}")
print(f'   {len(vf)} pontos validos, {frac_f:.0%} dentro de 3 erros -> desprezivel: {fina_ok}')
print('\n Angulos da janela (so reportados):')
for nome, th in JAN.items():
    print(f'   {nome} (theta = {th:.3f}): ' + '  '.join(f"n={n}: {tab[(n,th)][0]:+.2e} +- {tab[(n,th)][1]:.1e}" for n in NS))

# ---------------- veredito
if modo and colapso and decisivo and melhor == 'gaussiano' and fina_ok: v = 'E-a: cancelamento rapido sustentado no substituto'
elif colapso and decisivo and melhor in ('exponencial', 'potencia'): v = 'E-b: decaimento lento sustentado no substituto'
else: v = 'E-c: inconclusivo'
print(f'\n=== VEREDITO DE E: {v} ===')
out['E3'] = dict(tabela={f'{n}|{th}': tab[(n, th)] for (n, th) in tab}, abaixo_da_resolucao={str(n): abaixo[n] for n in NS},
                 colapso=dict(comparacoes=comp, fracao=frac, aceito=colapso), modelos=fits, melhor=melhor, dAIC=dAIC, decisivo=decisivo,
                 estrutura_fina=dict(pontos=fina, fracao=frac_f, desprezivel=fina_ok), veredito=v)
json.dump(out, open('h1b_E_resultados.json', 'w'), indent=1, default=float)
