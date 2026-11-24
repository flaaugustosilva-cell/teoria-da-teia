"""EXPLORATORIO (24/11/2026): de onde vem o excesso de coerencia da faixa ~3D? acao, geometria ou acoplamento.
Base exata (observacao do Flavio): Z_g(theta) = sum_b W_g(b) e^{i theta b}; a coerencia so depende do histograma W_g(b).
Populacao: todas as ordens, n = 8..11. Pesos L = n!/|Aut| (proporcionais a 1/|Aut|). Janela: 241 pontos em [2pi/3, pi].
Partes:
 (0) validacao: coerencia real pelo histograma = valores ja publicados; piso analitico do controle vs controles guardados.
 (1) degraus: independencia (histograma da populacao) -> tilt (media, variancia) -> tilt (+ paridade) -> real.
 (2) fatias por R (numero de pares comparaveis): coerencia e piso de cada valor de R; alinhamento de fase entre fatias.
 (3) geometria a B fixo: diferenca padronizada (classe vs resto), dentro de cada estrato de B, de h e N0..N3.
 (4) Controle B: 20 permutacoes dos rotulos da classe dentro dos estratos de B (semente 20261128);
     estatisticas: correlacao ponderada (B, R) e (B, h) dentro da classe; coerencia da pseudo-classe.
Uso: python h1b_mecanismo_coerencia.py PASTA_N9N10 PASTA_D11 [n ...]"""
import sys, math, json, numpy as np
from scipy.optimize import minimize
from scipy.special import logsumexp
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_dimensao import faixa, NOMES
from h1b_decoerencia import TH_JANELA as TH
from h1b_modelo_rede import contagens

GUARDADO = {8: ([5.1110e-02, 1.2731e-02, 8.6791e-02], [2.9184e-02, 6.6777e-03, 3.0812e-02]),
            9: ([1.8071e-02, 4.3490e-03, 2.9112e-02], [1.0921e-02, 2.6730e-03, 8.1497e-03]),
            10: ([8.4346e-03, 1.4544e-03, 1.4088e-02], [4.4280e-03, 7.0143e-04, 2.3311e-03]),
            11: ([2.6066e-03, 4.1178e-04, 5.6589e-03], [1.3428e-03, 1.6138e-04, 7.0251e-04])}

def carrega(n, p910, p11):
    if n == 11:
        D = [np.load(f'{p11}/h1b_D11_n11_parte{x}.npz') for x in range(20)]
        B = np.concatenate([d['B'] for d in D]).astype(np.int64); A = np.concatenate([d['aut'] for d in D])
        R = np.concatenate([d['R'] for d in D]).astype(np.int64); h = np.concatenate([d['h'] for d in D]).astype(np.int8)
        N = np.concatenate([d['N'] for d in D]); del D
    else:
        d = np.load(f'{p910}/h1b_N_n{n}.npz'); P = d['pred'].astype(np.int64)
        pc = np.array([bin(x).count('1') for x in range(1 << n)]); R = pc[P].sum(1)
        N = contagens(P, n).astype(np.int8); B = d['B'].astype(np.int64); A = d['aut']; h = d['h'].astype(np.int8)
    return B, math.factorial(n) // A.astype(np.int64), R, h, N

def rice_mediana(m, s2, rng):
    g = (rng.normal(size=4000) + 1j * rng.normal(size=4000)) * math.sqrt(s2 / 2)
    return np.array([np.median(np.abs(mi + g)) for mi in m])

def tilt(hpop, bv, alvo, usar_paridade):
    ok = hpop > 0; z = (bv - (hpop * bv).sum() / hpop.sum()) / math.sqrt((hpop * bv ** 2).sum() / hpop.sum() - ((hpop * bv).sum() / hpop.sum()) ** 2)
    F = [z, z ** 2] + ([(bv % 2).astype(float)] if usar_paridade else [])
    F = np.array(F)[:, ok]; lh = np.log(hpop[ok]); t = alvo(z[ok], bv[ok])[:F.shape[0]]
    f = lambda lam: (logsumexp(lh + lam @ F) - lam @ t)
    def g(lam):
        e = lh + lam @ F; p = np.exp(e - logsumexp(e)); return F @ p - t
    r = minimize(f, np.zeros(F.shape[0]), jac=g, method='BFGS', options=dict(gtol=1e-12, maxiter=2000))
    out = np.zeros_like(hpop); e = lh + r.x @ F; out[ok] = np.exp(e - logsumexp(e))
    return out, float(np.abs(g(r.x)).max())

def wcorr(x, y, w):
    w = w / w.sum(); mx, my = (w * x).sum(), (w * y).sum()
    return float((w * (x - mx) * (y - my)).sum() / math.sqrt((w * (x - mx) ** 2).sum() * (w * (y - my) ** 2).sum()))

def analisa_n(n, p910, p11, res):
    B, L, R, h, N = carrega(n, p910, p11); C2 = math.comb(n, 2); Lf = L.astype(float)
    b0 = int(B.min()); nb = int(B.max()) - b0 + 1; bv = np.arange(nb) + b0; E = np.exp(1j * np.outer(TH, bv))
    idx = R * nb + (B - b0)
    H = np.bincount(idx, weights=Lf, minlength=(C2 + 1) * nb).reshape(C2 + 1, nb)
    S2R = np.bincount(R, weights=Lf ** 2, minlength=C2 + 1)
    fR = faixa(np.arange(C2 + 1) / C2); hpop = H.sum(0); Zpop = E @ hpop; W = hpop.sum(); S2 = S2R.sum()
    coh = lambda hb: float(np.median(np.abs(E @ hb))) / hb.sum()
    rng = np.random.default_rng(0); R_ = {}
    print(f'\n===== n = {n} (todas as ordens; {len(B)} classes; B de {b0} a {b0 + nb - 1}) =====')
    print(f'coerencia da populacao inteira (independencia): {coh(hpop):.3e}')
    print(' faixa | q | real (guardado) | piso analitico (controles guardados) | razao | indep. | tilt(m,v) | tilt(m,v,par) | B: media/desvio classe vs pop. | alinhamento das fatias')
    mp, sp = (hpop * bv).sum() / W, math.sqrt((hpop * bv ** 2).sum() / W - ((hpop * bv).sum() / W) ** 2)
    for k in (0, 1, 2):
        hk = H[fR == k].sum(0); Wk = hk.sum(); q = Wk / W; real = coh(hk)
        piso = float(np.median(rice_mediana(q * np.abs(Zpop), q * (1 - q) * S2, rng))) / (q * W)
        mk = (hk * bv).sum() / Wk; sk = math.sqrt((hk * bv ** 2).sum() / Wk - mk ** 2); park = (hk * (bv % 2)).sum() / Wk
        alvo = lambda z, b: np.array([(hk[hpop > 0] * z).sum() / Wk, (hk[hpop > 0] * z ** 2).sum() / Wk, park])
        t2, e2 = tilt(hpop, bv, alvo, False); t3, e3 = tilt(hpop, bv, alvo, True)
        ct2, ct3 = coh(t2 * Wk), coh(t3 * Wk)
        Zs = np.stack([E @ H[r] for r in np.nonzero(fR == k)[0] if H[r].sum() > 0])
        alin = float(np.median(np.abs(Zs.sum(0)) / np.abs(Zs).sum(0)))
        gr, gc = GUARDADO[n]
        print(f' {NOMES[k]:8s}| {q:.4f} | {real:.4e} ({gr[k]:.4e}) | {piso:.3e} ({gc[k]:.3e}) | {real/piso:.2f} | {coh(hpop):.2e} | '
              f'{ct2:.3e} | {ct3:.3e} | {mk:+.1f}/{sk:.1f} vs {mp:+.1f}/{sp:.1f} | {alin:.3f}   (erro dos tilts {max(e2, e3):.0e})')
        R_[k] = dict(q=q, real=real, guardado=gr[k], piso=piso, piso_guardado=gc[k], indep=coh(hpop), tilt2=ct2, tilt3=ct3,
                     media=mk, desvio=sk, paridade_impar=park, alinhamento=alin)
    print(' Fatias por R (pares comparaveis): R | faixa | q | coerencia | piso | razao')
    fat = []
    for r in range(C2 + 1):
        if H[r].sum() == 0: continue
        q = H[r].sum() / W; c = coh(H[r])
        piso = float(np.median(rice_mediana(q * np.abs(Zpop), q * (1 - q) * S2, rng))) / (q * W)
        fat.append((r, int(fR[r]), q, c, piso))
    for r, f, q, c, piso in fat:
        if q > 1e-4: print(f'   {r:3d} | {NOMES[f]:8s} | {q:.4f} | {c:.3e} | {piso:.3e} | {c/piso:.2f}')
    # (3) geometria a B fixo
    print(' Geometria a B fixo (classe 2,5-3,5 vs resto; diferenca padronizada media por estrato, ponderada pelo peso da classe):')
    cl = fR[R] == 2; ger = {}
    for nome, x in (('altura', h.astype(float)),) + tuple((f'N{k}', N[:, k].astype(float)) for k in range(4)):
        s1 = np.bincount(B - b0, weights=Lf * x, minlength=nb); s2 = np.bincount(B - b0, weights=Lf * x * x, minlength=nb)
        c0 = np.bincount(B - b0, weights=Lf * cl, minlength=nb); c1 = np.bincount(B - b0, weights=Lf * x * cl, minlength=nb)
        tot = hpop; mu = s1 / np.maximum(tot, 1); sd = np.sqrt(np.maximum(s2 / np.maximum(tot, 1) - mu ** 2, 0))
        rest = tot - c0; ok = (c0 > 0) & (rest > 0) & (sd > 0)
        dif = (c1[ok] / c0[ok] - (s1[ok] - c1[ok]) / rest[ok]) / sd[ok]
        ger[nome] = float((c0[ok] * dif).sum() / c0[ok].sum())
    print('   ' + '; '.join(f'{k}: {v:+.2f} desvios' for k, v in ger.items()))
    res[n] = dict(faixas=R_, fatias=fat, geometria=ger)
    # (4) Controle B
    if n >= 10:
        print(' Controle B: 20 permutacoes dos rotulos da classe 2,5-3,5 dentro dos estratos de B (semente 20261128)')
        w = Lf; obsR, obsh = wcorr(B[cl].astype(float), R[cl].astype(float), w[cl]), wcorr(B[cl].astype(float), h[cl].astype(float), w[cl])
        hk = np.bincount(B[cl] - b0, weights=w[cl], minlength=nb); obs_c = coh(hk)
        ordem = np.argsort(B, kind='stable'); Bs = B[ordem]; ini = np.searchsorted(Bs, Bs, 'left')
        kg = np.bincount(B[cl] - b0, minlength=nb); marca = (np.arange(len(B)) - ini) < kg[Bs - b0]; del ordem, ini, Bs
        rng2 = np.random.default_rng(20261128); nul = []
        for _ in range(20):
            perm = np.lexsort((rng2.random(len(B)), B)); ps = np.zeros(len(B), bool); ps[perm[marca]] = True; del perm
            hs = np.bincount(B[ps] - b0, weights=w[ps], minlength=nb)
            nul.append((wcorr(B[ps].astype(float), R[ps].astype(float), w[ps]), wcorr(B[ps].astype(float), h[ps].astype(float), w[ps]), coh(hs)))
        nul = np.array(nul)
        print(f'   corr(B, R): real {obsR:+.4f}; permutadas {nul[:, 0].mean():+.4f} +- {nul[:, 0].std():.4f} [{nul[:, 0].min():+.4f}, {nul[:, 0].max():+.4f}]')
        print(f'   corr(B, h): real {obsh:+.4f}; permutadas {nul[:, 1].mean():+.4f} +- {nul[:, 1].std():.4f} [{nul[:, 1].min():+.4f}, {nul[:, 1].max():+.4f}]')
        print(f'   coerencia: real {obs_c:.4e}; permutadas {nul[:, 2].mean():.4e} [{nul[:, 2].min():.4e}, {nul[:, 2].max():.4e}] (mesma contagem por estrato; peso difere um pouco)')
        res[n]['controleB'] = dict(corrBR=obsR, corrBh=obsh, coer=obs_c, nulo=nul.tolist())
    sys.stdout.flush()

if __name__ == '__main__':
    p910, p11 = sys.argv[1], sys.argv[2]; ns = [int(x) for x in sys.argv[3:]] or [8, 9, 10, 11]; res = {}
    for n in ns: analisa_n(n, p910, p11, res)
    json.dump(res, open(f'mecanismo_coerencia_{"_".join(map(str, ns))}.json', 'w'), indent=1, default=float)
