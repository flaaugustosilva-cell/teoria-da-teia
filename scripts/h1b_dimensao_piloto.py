"""EXPLORATORIO (21/11/2026): duas frentes da dimensao emergente.
 (a) PILOTO de Monte Carlo: para ordens de n = 20, 40, 80 elementos, compara a coerencia de fase |E[e^{i theta B4}]|
     na janela de familias de ordens: pontos sorteados em diamantes de d = 2, 3, 4 (variedades) e ordens em camadas
     (tipo Kleitman-Rothschild: 3 camadas n/4, n/2, n/4; e 2 camadas). Ignora a entropia (quantas ordens ha de cada tipo).
 (c) Perfil de intervalos: para as classes exatas de n = 8, 9, 10, classifica cada classe pelo centroide mais proximo
     (perfil (N0..N3, R_4+)/C(n,2) e altura/n) entre: diamantes d = 2, 3, 4 e camadas; e mede a participacao
     de cada grupo em Z(theta) ao longo da janela (Re(Z_g conj Z)/|Z|^2, soma 1).
Uso: python h1b_dimensao_piloto.py a  |  python h1b_dimensao_piloto.py c PASTA"""
import sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_modelo_rede import contagens

C4 = np.array([-1, 9, -16, 8])

def diamante(n, d, rng):
    pts = np.empty((0, d))
    while len(pts) < n:
        p = rng.uniform(-1, 1, (4 * n * 2 ** d, d))
        ok = np.abs(p[:, 0]) + np.sqrt((p[:, 1:] ** 2).sum(1)) <= 1
        pts = np.vstack([pts, p[ok]])
    p = pts[:n]; p = p[np.argsort(p[:, 0])]
    dt = p[None, :, 0] - p[:, None, 0]; dr2 = ((p[None, :, 1:] - p[:, None, 1:]) ** 2).sum(2)
    return (dt > 0) & (dt * dt > dr2)

def camadas(n, rng, tres=True):
    if tres:
        a = n // 4; b = n - 2 * a; L = [a, b, a]
    else:
        L = [n // 2, n - n // 2]
    lay = np.repeat(np.arange(len(L)), L); C = np.zeros((n, n), bool)
    for i in range(n):
        for j in range(n):
            if lay[j] == lay[i] + 1: C[i, j] = rng.random() < 0.5
            elif lay[j] >= lay[i] + 2: C[i, j] = True
    return C

def perfil(C):
    n = len(C); Cf = C.astype(np.int32); K = Cf @ Cf; ent = np.where(C, K, -1)
    N = np.array([(ent == k).sum() for k in range(4)]); R4 = (ent >= 4).sum()
    h = np.ones(n, int)
    for j in range(n):
        pr = np.nonzero(C[:j, j])[0]
        if len(pr): h[j] = 1 + h[pr].max()
    return N, R4, h.max()

def piloto(M=1000):
    rng = np.random.default_rng(20261121); th = np.linspace(2 * np.pi / 3, np.pi, 61)
    fams = [('diamante d=2', lambda n: diamante(n, 2, rng)), ('diamante d=3', lambda n: diamante(n, 3, rng)),
            ('diamante d=4', lambda n: diamante(n, 4, rng)), ('camadas 3 (KR)', lambda n: camadas(n, rng, True)),
            ('camadas 2 (ruim)', lambda n: camadas(n, rng, False))]
    print(f'(a) PILOTO: coerencia de fase |E[e^(i theta B4)]| na janela theta em [2pi/3, pi], {M} amostras por familia '
          f'(piso estatistico ~ {1/math.sqrt(M):.3f}); r = fracao de ordenacao media; B4 = acao de 4 dimensoes')
    for n in (20, 40, 80):
        for nome, g in fams:
            B = np.empty(M); r = np.empty(M); hh = np.empty(M)
            for k in range(M):
                C = g(n); N, R4, h = perfil(C); B[k] = n + C4 @ N; r[k] = C.sum() / math.comb(n, 2); hh[k] = h
            coh = np.abs(np.exp(1j * np.outer(th, B)).mean(1))
            print(f'   n={n:3d} {nome:17s}: r {r.mean():.3f}, altura {hh.mean():5.1f}, B4 media {B.mean():9.1f} desvio {B.std():8.1f}; '
                  f'coerencia na janela: min {coh.min():.3f}, media {coh.mean():.3f}, no centro {coh[-1]:.3f}', flush=True)

def perfil_classes(pasta, nmin=8, nmax=10, M=4000):
    rng = np.random.default_rng(20261122); th = np.linspace(2 * np.pi / 3, np.pi, 241)
    print('(c) PERFIL DE INTERVALOS: participacao de cada grupo em Z(theta) na janela (soma 1); grupos pelo centroide mais proximo')
    for n in range(nmin, nmax + 1):
        refs = {}
        for nome, g in (('d=2', lambda: diamante(n, 2, rng)), ('d=3', lambda: diamante(n, 3, rng)),
                        ('d=4', lambda: diamante(n, 4, rng)), ('camadas', lambda: camadas(n, rng, True))):
            V = []
            for _ in range(M):
                N, R4, h = perfil(g()); V.append(np.r_[N, R4, h] / np.r_[[math.comb(n, 2)] * 5, n])
            refs[nome] = np.array(V)
        todos = np.vstack(list(refs.values())); sd = todos.std(0) + 1e-9
        cen = {k: v.mean(0) / sd for k, v in refs.items()}; nomes = list(cen)
        d = np.load(f'{pasta}/h1b_N_n{n}.npz'); P = d['pred'].astype(np.int64); N = contagens(P, n)
        pc = np.array([bin(x).count('1') for x in range(1 << n)]); R = pc[P].sum(1); R4 = R - N.sum(1)
        V = np.c_[N, R4, d['h']] / np.r_[[math.comb(n, 2)] * 5, n] / sd
        dist = np.stack([((V - cen[k]) ** 2).sum(1) for k in nomes], 1); grp = dist.argmin(1)
        B = d['B']; w = 1.0 / d['aut']
        for pop, m in (('todas as ordens', np.ones(len(w), bool)), ('oficial (altura >= 3)', d['h'] >= 3)):
            v, inv = np.unique(B[m], return_inverse=True); E = np.exp(1j * np.outer(th, v))
            Z = E @ np.bincount(inv, weights=w[m]); linha = []
            for k, nm in enumerate(nomes):
                Zk = E @ np.bincount(inv, weights=w[m] * (grp[m] == k), minlength=len(v))
                part = (Zk * np.conj(Z)).real / np.abs(Z) ** 2
                linha.append(f'{nm}: peso sem fase {w[m][grp[m] == k].sum()/w[m].sum():.3f}, participacao media {part.mean():+.2f} '
                             f'[{part.min():+.2f}, {part.max():+.2f}]')
            print(f'   n={n} {pop}: ' + ' | '.join(linha), flush=True)

if __name__ == '__main__':
    if sys.argv[1] == 'a': piloto()
    else: perfil_classes(sys.argv[2])
