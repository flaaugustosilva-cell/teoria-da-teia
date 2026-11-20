"""Modelo gaussiano de rede para a estrutura fina de Z(theta) -- ver dados/h1b/PREREGISTRO_MODELO_REDE.md.
Populacao OFICIAL apenas: n = 5 a 10, altura >= 3 (todas cabem em 3+1 para n <= 10), peso 1/|Aut|.
Le h1b_N_n{n}.npz (pred, B, h, aut). Nenhum parametro e ajustado: mu e Sigma sao os momentos ponderados.

Uso:
  python h1b_modelo_rede.py valida                 -> teste da implementacao em dados sinteticos (nao usa teias)
  python h1b_modelo_rede.py p3   PASTA SAIDA       -> P3 (controles artificiais), roda primeiro
  python h1b_modelo_rede.py p1p2 PASTA SAIDA       -> P1 e P2 (motivadas pelos dados), roda depois
"""
import sys, json, math, itertools, numpy as np

C_ORIG = (-1, 9, -16, 8)
FAM_A = [p for p in itertools.permutations(C_ORIG) if p != C_ORIG]                       # 23 permutacoes
FAM_C = [tuple(C_ORIG[k] + (d if k == j else 0) for k in range(4)) for j in range(4) for d in (1, -1)]  # 8 vizinhos
FAM_B = [(8, 8, -1, -12), (-3, 11, -14, 3), (8, 5, -1, -3), (-12, 14, 1, -3), (-6, -15, 6, -1),
         (15, -4, -10, -3), (8, 12, 8, -10), (9, 8, -11, -11), (-6, 12, 15, 10), (14, 7, -3, -16),
         (11, 10, -8, 15), (-11, 5, -13, 13), (-3, 5, -14, 8), (2, 12, -10, 9), (-9, -10, -16, 13),
         (-16, 9, -13, -14), (-7, 1, 10, 5), (-9, 16, -1, -7), (-1, -10, 1, -5), (12, 11, 11, 0)]
TH = np.linspace(0, np.pi, 3601)        # mesma grade da exploracao
PISO = 1e-12                             # piso de |phi| (relativo a W)
LTRUNC, LCHECK = 50.0, 70.0              # truncamento: termos com q/2 <= L
MAXCAIXA = 5_000_000                     # deslocamentos de rede candidatos acima disso: "nao computavel"
TH_OBS = {5: 0.740, 6: 0.740, 7: 0.740, 8: 0.741, 9: 0.742, 10: 0.742}   # publicados (EXPLORATORIO_ESTRUTURA_FINA)

def familia_b_regra():
    """Reproduz FAM_B pela regra registrada (semente 20261120)."""
    proib = set(FAM_A) | {C_ORIG} | set(FAM_C)
    proib |= {tuple(-x for x in v) for v in proib}
    rng = np.random.default_rng(20261120); out = []
    while len(out) < 20:
        v = tuple(int(x) for x in rng.integers(-16, 17, size=4))
        if v == (0, 0, 0, 0) or v in proib or v in out or tuple(-x for x in v) in out: continue
        out.append(v)
    return out

# ---------------- dados ----------------
def contagens(pred, n):
    """N_k = numero de pares x < y com exatamente k elementos estritamente entre eles (k = 0..3)."""
    pred = pred.astype(np.int64); M = len(pred)
    pop = np.array([bin(x).count('1') for x in range(1 << n)], np.int64)
    suc = np.zeros((M, n), np.int64)
    for k in range(n):
        for i in range(n): suc[:, i] |= ((pred[:, k] >> i) & 1) << k
    N = np.zeros((M, 4), np.int64)
    for j in range(n):
        for i in range(n):
            if i == j: continue
            rel = (pred[:, j] >> i) & 1
            ent = pop[pred[:, j] & suc[:, i]]
            for k in range(4): N[:, k] += rel * (ent == k)
    return N

def carrega(pasta, n):
    d = np.load(f'{pasta}/h1b_N_n{n}.npz'); boa = d['h'] >= 3
    N = contagens(d['pred'][boa], n)
    Bre = n + N @ np.array(C_ORIG)
    if not np.array_equal(Bre, d['B'][boa]): raise SystemExit(f'n={n}: B recalculado difere do armazenado -- ABORTA')
    aut = d['aut'][boa].astype(np.int64); f = math.factorial(n)
    if np.any(f % aut): raise SystemExit('|Aut| nao divide n!')
    return N, f // aut                                       # L = numero de rotulagens (inteiro)

def momentos(N, L):
    w = L.astype(float); w /= w.sum(); mu = w @ N
    X = N - mu; S = (X * w[:, None]).T @ X
    return mu, S

# ---------------- somas ----------------
def exato(N, L, cv, n):
    """phi_obs(theta) = sum_classes L e^{i theta B'} / sum L, com B' = n + cv.N, agregado por B'."""
    b = n + N @ np.array(cv, np.int64); b0 = b.min()
    Lb = np.bincount(b - b0, weights=L.astype(float))          # inteiros < 2^53: soma exata
    bb = np.arange(b0, b0 + len(Lb)); nz = Lb > 0; bb, Lb = bb[nz], Lb[nz]
    out = np.empty(len(TH), complex)
    for a in range(0, len(TH), 400):
        out[a:a+400] = np.exp(1j * np.outer(TH[a:a+400], bb)) @ Lb
    return out / Lb.sum(), len(bb)

def _caixa(S, L):
    """Deslocamentos K (m = round(t/2pi) + K) que podem ter q/2 <= L para algum delta em [-1/2, 1/2]^4."""
    Si = np.linalg.inv(S); r = np.sqrt(2 * L * np.diag(Si)) / (2 * np.pi)
    R = np.ceil(r).astype(int) + 1
    bruto = int(np.prod(2 * R + 1))
    if bruto > 50 * MAXCAIXA: return None, bruto
    K = np.array(list(itertools.product(*[range(-x, x + 1) for x in R])), float)
    lam = np.linalg.eigvalsh(S)[0]
    folga = np.maximum(0.0, np.linalg.norm(K, axis=1) - 1.0)          # |delta - K| >= |K| - 1
    K = K[(2 * np.pi) ** 2 * lam * folga ** 2 <= 2 * L]
    return K, len(K)

def soma_rede(mu, S, t0, L):
    """sum_m exp(i u.mu - u^T S u / 2), u = t0 - 2 pi m, somando todos os m com u^T S u / 2 <= L."""
    K, tam = _caixa(S, L)
    if K is None or tam > MAXCAIXA: return None
    SK = K @ S; KSK = np.einsum('pi,pi->p', K, SK)
    out = np.empty(len(t0), complex)
    for a in range(0, len(t0), 20):
        T = t0[a:a+20]; dl = T / (2 * np.pi) - np.rint(T / (2 * np.pi))        # delta em [-1/2, 1/2]^4
        q = (2 * np.pi) ** 2 * (np.einsum('ti,ij,tj->t', dl, S, dl)[:, None] - 2 * dl @ SK.T + KSK[None, :])
        for k in range(len(T)):
            ok = q[k] <= 2 * L
            u = 2 * np.pi * (dl[k][None, :] - K[ok])
            out[a + k] = np.sum(np.exp(1j * (u @ mu) - 0.5 * q[k][ok]))
    return out

def modelo(mu, S, cv, n, L=LTRUNC):
    num = soma_rede(mu, S, np.outer(TH, np.array(cv, float)), L)
    if num is None: return None, None
    D = soma_rede(mu, S, np.zeros((1, 4)), L)[0]
    return np.exp(1j * TH * n) * num / D, D

def Khat(sd):
    s = sd / 4; k = np.arange(-60, 61); ker = np.exp(-0.5 * (k / s) ** 2); ker /= ker.sum()
    return np.cos(np.outer(TH, k)) @ ker

# ---------------- metricas ----------------
def picos(a, msk):
    i = np.arange(1, len(a) - 1)
    ok = msk[i] & msk[i - 1] & msk[i + 1] & (a[i] > a[i - 1]) & (a[i] > a[i + 1]) & (a[i] >= PISO)
    return i[ok]

def metricas_p3(po, pm, sdp):
    ao, am = np.abs(po), np.abs(pm); th0 = 8 / sdp; R = TH >= th0
    A = R & (np.maximum(ao, am) >= PISO)
    po_k, pm_k = picos(ao, R), picos(am, R)
    if not A.any() or len(po_k) == 0 or len(pm_k) == 0:
        return dict(testavel=False, th0=th0)
    e = np.abs(np.log10(np.maximum(am[A], PISO)) - np.log10(np.maximum(ao[A], PISO)))
    io = po_k[np.argmax(ao[po_k])]; im = pm_k[np.argmax(am[pm_k])]
    dlt = abs(TH[im] - TH[io]); quase = ao[im] / ao[io]
    rpk = abs(math.log10(max(am[im], PISO) / max(ao[io], PISO))); emed = float(np.median(e))
    pos = 'ok' if (dlt <= 0.01 or quase >= 0.8) else ('falha' if (dlt > 0.05 and quase < 0.5) else 'intermediario')
    mag = 'ok' if (emed <= 0.3 and rpk <= 0.3) else ('falha' if (emed > 1 or rpk > 1) else 'intermediario')
    return dict(testavel=True, th0=th0, th_pico_obs=float(TH[io]), th_pico_mod=float(TH[im]), delta=dlt,
                obs_no_pico_mod_rel=float(quase), pico_obs=float(ao[io]), pico_mod=float(am[im]),
                log_razao_pico=rpk, e_mediana=emed, e_p90=float(np.percentile(e, 90)), posicao=pos, magnitude=mag)

def agrega(lista):
    tot = len(lista)
    out = {}
    for chave in ('posicao', 'magnitude'):
        ok = sum(1 for r in lista if r.get(chave) == 'ok'); fa = sum(1 for r in lista if r.get(chave) == 'falha')
        out[chave] = dict(ok=ok, falha=fa, nao_testavel=sum(1 for r in lista if not r['testavel']), total=tot,
                          frac_ok=ok / tot, frac_falha=fa / tot,
                          veredito='sucesso' if ok / tot >= 0.8 else ('falha' if fa / tot >= 0.5 else 'inconclusivo'))
    return out

def combina(v9, v10):
    if v9 == v10 == 'sucesso': return 'SUCESSO'
    if v9 == v10 == 'falha': return 'FALHA'
    return 'INCONCLUSIVO'

# ---------------- execucao ----------------
def prepara(pasta, n):
    N, L = carrega(pasta, n); mu, S = momentos(N, L); ev = np.linalg.eigvalsh(S)
    info = dict(n=n, classes=int(len(N)), W=float(L.sum() / math.factorial(n)), mu=mu.tolist(), Sigma=S.tolist(),
                autovalores=ev.tolist())
    degen = bool(ev[0] < 1e-6 * ev[-1])
    tam = _caixa(S, LCHECK)[1] if not degen else None
    info['degenerada'] = degen; info['caixa'] = tam; info['computavel'] = (not degen) and tam <= MAXCAIXA
    return N, L, mu, S, info

def roda_vetor(N, L, mu, S, cv, n, diag=False):
    Sx = np.diag(np.diag(S)) if diag else S
    po, nb = exato(N, L, cv, n); pm, D = modelo(mu, Sx, cv, n)
    pm2, _ = modelo(mu, Sx, cv, n, LCHECK)
    msk = np.abs(pm) >= PISO
    trunc = float(np.max(np.abs(pm2[msk] - pm[msk]) / np.abs(pm[msk]))) if msk.any() else 0.0
    sdp = math.sqrt(np.array(cv) @ Sx @ np.array(cv))
    return po, pm, D, trunc, sdp, nb

def p3(pasta, saida):
    res = {}
    for n in range(5, 11):
        N, L, mu, S, info = prepara(pasta, n); res[n] = dict(info=info)
        print(f'\n[OFICIAL] n={n}: classes {info["classes"]}, W = {info["W"]:.6g}, autovalores de Sigma = '
              + ', '.join(f'{x:.4g}' for x in info['autovalores']) + f'; caixa {info["caixa"]}')
        if not info['computavel']: print('  NAO COMPUTAVEL (regra de degenerescencia/caixa) -> n inconclusivo'); continue
        for rot, diag in (('completo', False), ('diagonal', True)):
            linhas = []
            for fam, vetores in (('A', FAM_A), ('B', FAM_B), ('C', FAM_C), ('orig', [C_ORIG])):
                for cv in vetores:
                    po, pm, D, trunc, sdp, nb = roda_vetor(N, L, mu, S, cv, n, diag)
                    m = metricas_p3(po, pm, sdp) if trunc <= 1e-3 else dict(testavel=False, motivo='truncamento')
                    m.update(fam=fam, c=list(cv), D=float(D.real), D_im=float(D.imag),
                                                           trunc=trunc, sd=sdp, valores_b=nb)
                    linhas.append(m)
            controles = [r for r in linhas if r['fam'] != 'orig']
            res[n][rot] = dict(vetores=linhas, agregado=agrega(controles),
                               por_familia={f: agrega([r for r in controles if r['fam'] == f]) for f in 'ABC'})
            ag = res[n][rot]['agregado']
            print(f'  modelo {rot}: posicao ok {ag["posicao"]["ok"]}/51, falha {ag["posicao"]["falha"]}, '
                  f'nao testavel {ag["posicao"]["nao_testavel"]} -> {ag["posicao"]["veredito"]}; '
                  f'magnitude ok {ag["magnitude"]["ok"]}/51, falha {ag["magnitude"]["falha"]} -> {ag["magnitude"]["veredito"]}')
            for f in 'ABC':
                pf = res[n][rot]['por_familia'][f]
                print(f'     familia {f}: posicao ok {pf["posicao"]["ok"]}/{pf["posicao"]["total"]}, magnitude ok {pf["magnitude"]["ok"]}/{pf["magnitude"]["total"]}')
            print(f'     max erro de truncamento {max(r["trunc"] for r in linhas):.1e}; D-1 = {linhas[0]["D"]-1:.2e}')
    fim = {}
    for rot in ('completo', 'diagonal'):
        for chave in ('posicao', 'magnitude'):
            try: fim[f'{rot}_{chave}'] = combina(res[9][rot]['agregado'][chave]['veredito'], res[10][rot]['agregado'][chave]['veredito'])
            except KeyError: fim[f'{rot}_{chave}'] = 'INCONCLUSIVO'
    print('\nVEREDITO P3 (n = 9 e 10, modelo completo): P3a posicao', fim['completo_posicao'], '| P3b magnitude', fim['completo_magnitude'])
    print('Descritivo (modelo diagonal): posicao', fim['diagonal_posicao'], '| magnitude', fim['diagonal_magnitude'])
    json.dump(dict(resultados=res, veredito=fim), open(f'{saida}/modelo_rede_p3.json', 'w'), indent=1)

def p1p2(pasta, saida):
    res = {}; jan = TH >= 2 * np.pi / 3
    for n in range(5, 11):
        N, L, mu, S, info = prepara(pasta, n)
        if not info['computavel']: res[n] = dict(computavel=False); continue
        po, pm, D, trunc, sdp, nb = roda_vetor(N, L, mu, S, C_ORIG, n)
        Kh = np.abs(1 - Khat(sdp)); alvo = TH > 0.5
        thm = float(TH[np.argmax(np.abs(pm) * Kh * alvo)])
        m0 = np.array([0, 1, -2, 1]); cc = np.array(C_ORIG)
        th1 = float(2 * np.pi * (cc @ S @ m0) / (cc @ S @ cc))
        ao, am = np.abs(po[jan]), np.abs(pm[jan])
        e = np.abs(np.log10(np.maximum(am, PISO)) - np.log10(np.maximum(ao, PISO)))
        W = info['W']
        r = dict(th_obs=TH_OBS[n], th_mod=thm, delta1=abs(thm - TH_OBS[n]), th_formula_um_termo=th1,
                 p1=('ok' if abs(thm - TH_OBS[n]) <= 0.005 else ('falha' if abs(thm - TH_OBS[n]) > 0.02 else 'intermediario')),
                 e_mediana=float(np.median(e)), e_max=float(np.max(e)),
                 p2=('ok' if (np.median(e) <= 0.3 and np.max(e) <= 1) else ('falha' if np.median(e) > 1 else 'intermediario')),
                 min_obs_Z=float(W * ao.min()), min_mod_Z=float(W * am.min()), cota_ruim=3 ** n / math.factorial(n),
                 Zpi_obs=float(W * po[-1].real), Zpi_mod=float(W * pm[-1].real), trunc=trunc, D=float(D.real))
        res[n] = r
        print(f'[OFICIAL] n={n}: P1 theta*_obs {r["th_obs"]:.3f}, modelo {thm:.4f} (formula de um termo {th1:.4f}), '
              f'|dif| {r["delta1"]:.4f} -> {r["p1"]} | P2 janela: erro log10 mediano {r["e_mediana"]:.3f}, max {r["e_max"]:.3f} -> {r["p2"]} | '
              f'min|Z| obs {r["min_obs_Z"]:.4g} mod {r["min_mod_Z"]:.4g} (cota ruim {r["cota_ruim"]:.3g}) | Z(pi) obs {r["Zpi_obs"]:+.4g} mod {r["Zpi_mod"]:+.4g}')
    v = {}
    for p, (s, f) in (('p1', ('ok', 'falha')), ('p2', ('ok', 'falha'))):
        a, b = res[9].get(p), res[10].get(p)
        v[p] = 'SUCESSO' if a == b == s else ('FALHA' if a == b == f else 'INCONCLUSIVO')
    print('\nVEREDITO (descritivo, previsoes motivadas pelos dados): P1', v['p1'], '| P2', v['p2'])
    json.dump(dict(resultados=res, veredito=v), open(f'{saida}/modelo_rede_p1p2.json', 'w'), indent=1)

def valida():
    """Teste de implementacao em distribuicao sintetica exatamente gaussiana na rede (nao usa teias)."""
    assert familia_b_regra() == FAM_B, 'familia B nao reproduz a regra'
    rng = np.random.default_rng(1); Q = np.linalg.qr(rng.normal(size=(4, 4)))[0]; pior = 0.0
    for eig in ([0.6, 1.5, 3.0, 5.0], [0.15, 0.4, 2.0, 6.0]):          # o segundo tem efeitos de rede fortes (D != 1)
        Sp = Q @ np.diag(eig) @ Q.T; mup = np.array([12.3, 9.1, 6.7, 4.2])
        g = [np.arange(int(mup[i] - 14 * math.sqrt(Sp[i, i])), int(mup[i] + 14 * math.sqrt(Sp[i, i])) + 1) for i in range(4)]
        N = np.array(list(itertools.product(*g)), np.int64); X = N - mup
        w = np.exp(-0.5 * np.einsum('pi,ij,pj->p', X, np.linalg.inv(Sp), X))
        for cv in [C_ORIG, FAM_A[3], FAM_B[0], FAM_C[2]]:
            b = 7 + N @ np.array(cv); b0 = b.min(); wb = np.bincount(b - b0, weights=w); bb = np.arange(b0, b0 + len(wb))
            ex = np.exp(1j * np.outer(TH, bb)) @ wb / wb.sum()
            md, D = modelo(mup, Sp, cv, 7)
            pior = max(pior, float(np.max(np.abs(ex - md))))
        mu2, S2 = momentos(N, w * 1e6)
        print(f'autovalores {eig}: D - 1 = {D.real-1:.2e}; momentos empiricos vs parametros: |dmu| {np.max(np.abs(mu2-mup)):.1e}, |dS| {np.max(np.abs(S2-Sp)):.1e}')
    print(f'validacao sintetica: max |exato - modelo| = {pior:.2e} (exigido < 1e-10)')
    # contagens: cadeia 0<1<2<3<4 -> N0=4, N1=3, N2=2, N3=1; antichain -> zeros
    cad = np.array([[(1 << j) - 1 for j in range(5)]]); anti = np.zeros((1, 5), np.int64)
    assert contagens(cad, 5).tolist() == [[4, 3, 2, 1]] and contagens(anti, 5).tolist() == [[0, 0, 0, 0]]
    print('contagens: cadeia e anticadeia corretas')
    return pior < 1e-10

if __name__ == '__main__':
    modo = sys.argv[1]
    if modo == 'valida': sys.exit(0 if valida() else 1)
    elif modo == 'p3': p3(sys.argv[2], sys.argv[3])
    elif modo == 'p1p2': p1p2(sys.argv[2], sys.argv[3])
