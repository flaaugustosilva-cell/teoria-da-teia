"""EXPLORATORIO (24/11/2026): a dimensao e propriedade das teias individuais (Modelo A) ou so coletiva (Modelo B)?
Formalismo de medida quantica (Sorkin): para uma particao das teias em classes A_g, Z_g(theta) = sum_{P in A_g} w e^{i theta B4},
matriz de decoerencia D_gh = Z_g conj(Z_h) (soma de todas = |Z|^2). 'Antes' = peso classico p_g = W_g/W;
'depois' = medida quantica normalizada mu_g = |Z_g|^2 / sum_h |Z_h|^2; indice de decoerencia I = sum_{g!=h}|D_gh| / sum_g D_gg.
I << 1: as classes nao interferem (dimensao 'classica'); I >~ 1: interferem (dimensao nao e atributo definido).
Particoes: (1) faixas de Myrheim-Meyer; (2) grupo de perfil de intervalos mais proximo (diamantes d=2,3,4 e camadas).
Uso: python h1b_decoerencia.py PASTA"""
import sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_modelo_rede import contagens
from h1b_dimensao import faixa, NOMES
from h1b_dimensao_piloto import diamante, camadas, perfil

def grupos_perfil(P, N, h, n, rng, M=4000):
    refs = {}
    for nome, g in (('d=2', lambda: diamante(n, 2, rng)), ('d=3', lambda: diamante(n, 3, rng)),
                    ('d=4', lambda: diamante(n, 4, rng)), ('camadas', lambda: camadas(n, rng, True))):
        V = []
        for _ in range(M):
            Nn, R4, hh = perfil(g()); V.append(np.r_[Nn, R4, hh] / np.r_[[math.comb(n, 2)] * 5, n])
        refs[nome] = np.array(V)
    sd = np.vstack(list(refs.values())).std(0) + 1e-9; cen = [v.mean(0) / sd for v in refs.values()]
    pc = np.array([bin(x).count('1') for x in range(1 << n)]); R4 = pc[P].sum(1) - N.sum(1)
    V = np.c_[N, R4, h] / np.r_[[math.comb(n, 2)] * 5, n] / sd
    return np.stack([((V - c) ** 2).sum(1) for c in cen], 1).argmin(1), list(refs)

def analisa(B, w, g, nomes, th):
    v, inv = np.unique(B, return_inverse=True); E = np.exp(1j * np.outer(th, v)); G = len(nomes)
    Z = np.stack([E @ np.bincount(inv, weights=w * (g == k), minlength=len(v)) for k in range(G)], 1)   # (theta, G)
    p = np.array([w[g == k].sum() for k in range(G)]) / w.sum()
    diag = np.abs(Z) ** 2; mu = diag / diag.sum(1, keepdims=True)
    tot = np.abs(Z.sum(1)) ** 2
    fora = (np.abs(Z[:, :, None] * np.conj(Z[:, None, :])).sum((1, 2)) - diag.sum(1))
    I = fora / diag.sum(1)
    return p, mu, I, tot / diag.sum(1)

def main(pasta):
    th = np.linspace(2 * np.pi / 3, np.pi, 241); rng = np.random.default_rng(20261124)
    for n in range(8, 11):
        d = np.load(f'{pasta}/h1b_N_n{n}.npz'); P = d['pred'].astype(np.int64); N = contagens(P, n)
        pc = np.array([bin(x).count('1') for x in range(1 << n)]); r = pc[P].sum(1) / math.comb(n, 2)
        gp, nomes_p = grupos_perfil(P, N, d['h'], n, rng)
        for pop, m in (('todas as ordens', np.ones(len(r), bool)), ('oficial (altura >= 3)', d['h'] >= 3)):
            w = 1.0 / d['aut'][m]; B = d['B'][m]
            for rot, g, nomes in (('Myrheim-Meyer', faixa(r[m]), NOMES), ('perfil de intervalos', gp[m], nomes_p)):
                p, mu, I, coer = analisa(B, w, g, nomes, th)
                print(f'[n={n}, {pop}, particao {rot}] indice de decoerencia I na janela: mediana {np.median(I):.1f} '
                      f'(min {I.min():.2f}, max {I.max():.0f}); |Z|^2 / soma dos |Z_g|^2: mediana {np.median(coer):.1e}')
                print('   classe: peso classico p  ->  medida quantica mu (mediana na janela [min, max])')
                for k, nm in enumerate(nomes):
                    print(f'     {nm:9s}: {p[k]:.4f} -> {np.median(mu[:, k]):.4f} [{mu[:, k].min():.4f}, {mu[:, k].max():.4f}]')
            # media complexa da fracao de ordenacao: pode sair do intervalo fisico [0, 1]
            v, inv = np.unique(B, return_inverse=True); E = np.exp(1j * np.outer(th, v))
            rm = (E @ np.bincount(inv, weights=w * r[m])) / (E @ np.bincount(inv, weights=w))
            fora = np.mean((rm.real < 0) | (rm.real > 1))
            print(f'   media complexa <r>_theta na janela: Re de {rm.real.min():+.2f} a {rm.real.max():+.2f}; '
                  f'fracao da janela com Re<r> fora de [0, 1]: {fora:.2f}', flush=True)

if __name__ == '__main__' and len(sys.argv) == 2:
    main(sys.argv[1])

# ---------------- controle por subconjuntos aleatorios (antes so num comando avulso; agora congelado aqui) ----------------
TH_JANELA = np.linspace(2 * np.pi / 3, np.pi, 241)

def coerencia(B, w, mask):
    """mediana na janela de |Z_mask(theta)| / W_mask, com Z_mask = sum_{mask} w e^{i theta B}."""
    v, inv = np.unique(B, return_inverse=True); E = np.exp(1j * np.outer(TH_JANELA, v))
    return float(np.median(np.abs(E @ np.bincount(inv, weights=w * mask, minlength=len(v))))) / float(w[mask].sum())

def razoes_controle(B, w, g, rng, sorteios=20, faixas=(0, 1, 2)):
    """Para cada faixa k: real = coerencia da faixa; controle: 'sorteios' subconjuntos com cada classe incluida
    independentemente com probabilidade q = W_k/W (rng.random(numero de classes) < q), na ordem faixa a faixa.
    Retorna {k: (real, lista dos controles, razao = real / mediana(controles))}."""
    out = {}
    for k in faixas:
        mk = g == k; real = coerencia(B, w, mk); q = w[mk].sum() / w.sum(); cs = []
        for _ in range(sorteios):
            sub = rng.random(len(w)) < q; cs.append(coerencia(B, w, sub))
        out[k] = (real, cs, real / float(np.median(cs)))
    return out

def reproduz_n8_10(pasta):
    """Reproduz o controle de 24/11/2026 (n = 8, 9, 10; todas as ordens; semente 20261124, um so gerador na ordem n, faixa)."""
    rng = np.random.default_rng(20261124)
    for n in (8, 9, 10):
        d = np.load(f'{pasta}/h1b_N_n{n}.npz'); P = d['pred'].astype(np.int64)
        pc = np.array([bin(x).count('1') for x in range(1 << n)]); r = pc[P].sum(1) / math.comb(n, 2)
        res = razoes_controle(d['B'], 1.0 / d['aut'], faixa(r), rng)
        print(f'  n={n}: ' + ' | '.join(f'{NOMES[k]}: real {v[0]:.4e}, controle mediano {np.median(v[1]):.4e} '
                                         f'[{min(v[1]):.2e}, {max(v[1]):.2e}], razao {v[2]:.3f}' for k, v in res.items()), flush=True)

if __name__ == '__main__' and len(sys.argv) > 2 and sys.argv[2] == 'controle':
    reproduz_n8_10(sys.argv[1])
