"""ANALITICO/EXPLORATORIO (23/11/2026): a parte de raiz modular prima por modulos substituidos, todas as ordens, theta = pi.
P = Q[M_1..M_k], Q estritamente prima (sem modulos nao triviais, k >= 4), M_i ordens quaisquer (decomposicao unica, Gallai).
Formula (deducao em ANALITICO_9.md), com m_i, D_i, X_i (= maximos), U_i de M_i e e_i = [|M_i| = 1]:
  s(P) = prod s(M_i) * (-1)^( sum_{q_i cobre-se por q_j} (X_i m_j + U_i m_j + X_i D_j)
                              + sum_{q_i < q_l < q_j, unico entre, e_l = 1} X_i m_j )
  m(P) = sum_{q_i minimo} m_i;  D(P) = sum_{q_i minimo} D_i + sum_{q_i com 1 so abaixo q_l, e_l=1} m_i
  X(P) = sum_{q_i maximo} X_i;  U(P) = sum_{q_i maximo} U_i + sum_{q_i com 1 so acima q_l, e_l=1} X_i
Uso: python h1b_raiz_prima_modulos.py PASTA"""
import sys, math, numpy as np
from collections import defaultdict
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_modelo_rede import contagens
from h1b_paridade_explora import estrutura
from h1b_soma_ordinal import perfis

def blocos(pred, n):
    """Modulos maximos de cada ordem (vetorizado por bitmask). Retorna rotulo do bloco (menor elemento) por elemento."""
    pred = pred.astype(np.int64); M = len(pred); full = (1 << n) - 1
    suc = np.zeros_like(pred)
    for k in range(n):
        for i in range(n): suc[:, i] |= ((pred[:, k] >> i) & 1) << k
    inc = full & ~(pred | suc) & ~(np.int64(1) << np.arange(n))[None, :]
    rot = np.tile(np.arange(n), (M, 1))
    for x in range(n):
        for y in range(x + 1, n):
            S = np.full(M, (1 << x) | (1 << y), np.int64)
            while True:
                novo = S.copy()
                for z in range(n):
                    fora = ((S >> z) & 1) == 0
                    homog = ((S & ~pred[:, z]) == 0) | ((S & ~suc[:, z]) == 0) | ((S & ~inc[:, z]) == 0)
                    novo |= np.where(fora & ~homog, np.int64(1) << z, 0)
                if np.array_equal(novo, S): break
                S = novo
            mesmo = S != full
            rot[:, y] = np.where(mesmo & (rot[:, y] > x), np.minimum(rot[:, y], rot[:, x]), rot[:, y])
    return rot

def estado_sinal(pred, n):
    N = contagens(pred[None, :], n)[0]; E = estrutura(pred[None, :], n); u, d = perfis(pred[None, :], n)
    s = (-1) ** (n + N[0] + N[1])
    return s, (int(E['mini'][0]), int(d[0, 1]), int(E['maxi'][0]), int(u[0, 1]))

def substitui(Qp, k, mods):
    """Constroi P = Q[mods]; Qp: pred de Q (bitmask em k); mods: lista de (pred, tamanho)."""
    off = np.cumsum([0] + [t for _, t in mods]); n = int(off[-1]); P = np.zeros(n, np.int64)
    for i, (mp, t) in enumerate(mods):
        abaixo = 0
        for j in range(k):
            if (int(Qp[i]) >> j) & 1: abaixo |= ((1 << mods[j][1]) - 1) << int(off[j])
        for a in range(t): P[off[i] + a] = (int(mp[a]) << int(off[i])) | abaixo
    return P, n

def formula(Qp, k, mods):
    pq = [int(x) for x in Qp]; rel = [[(pq[j] >> i) & 1 for j in range(k)] for i in range(k)]   # rel[i][j]: q_i < q_j
    entre = [[[l for l in range(k) if rel[i][l] and rel[l][j]] for j in range(k)] for i in range(k)]
    st = []; sg = 1; ntot = 0
    for mp, t in mods:
        s, e = estado_sinal(np.array(mp, np.int64), t); st.append(e); sg *= s; ntot += t
    um = [t == 1 for _, t in mods]; X = 0
    for i in range(k):
        for j in range(k):
            if not rel[i][j]: continue
            mi, Di, Xi, Ui = st[i]; mj, Dj, Xj, Uj = st[j]
            if len(entre[i][j]) == 0: X += Xi * mj + Ui * mj + Xi * Dj
            elif len(entre[i][j]) == 1 and um[entre[i][j][0]]: X += Xi * mj
    minimo = [not any(rel[j][i] for j in range(k)) for i in range(k)]; maximo = [not any(rel[i][j] for j in range(k)) for i in range(k)]
    abaixo = [[j for j in range(k) if rel[j][i]] for i in range(k)]; acima = [[j for j in range(k) if rel[i][j]] for i in range(k)]
    m = sum(st[i][0] for i in range(k) if minimo[i]); Xp = sum(st[i][2] for i in range(k) if maximo[i])
    D = sum(st[i][1] for i in range(k) if minimo[i]) + sum(st[i][0] for i in range(k) if len(abaixo[i]) == 1 and um[abaixo[i][0]])
    U = sum(st[i][3] for i in range(k) if maximo[i]) + sum(st[i][2] for i in range(k) if len(acima[i]) == 1 and um[acima[i][0]])
    return sg * (-1) ** (X % 2), (m % 2, D % 2, Xp % 2, U % 2)

def main(pasta, nmax=10):
    cl = {n: np.load(f'{pasta}/h1b_N_n{n}.npz') for n in range(1, nmax + 1)}
    # ---- (V1) verificacao ponto a ponto da formula de substituicao ----
    rng = np.random.default_rng(20261123); primas = {}
    for k in (4, 5, 6):
        d = cl[k]; E = estrutura(d['pred'], k); m = E['tipo'] == 2
        rot = blocos(d['pred'][m], k); estr = (rot == np.arange(k)[None, :]).all(1)
        primas[k] = d['pred'][m][estr]
    print('ordens estritamente primas (classes): ' + ', '.join(f'k={k}: {len(primas[k])}' for k in primas))
    ok_s = ok_e = ok_b = True; testes = 0
    for _ in range(3000):
        k = int(rng.choice([4, 5, 6])); Qp = primas[k][rng.integers(len(primas[k]))]
        mods = []
        for i in range(k):
            t = int(rng.choice([1, 1, 2, 3, 4])) if sum(x for _, x in mods) < 10 - (k - i) else 1
            mods.append((cl[t]['pred'][rng.integers(len(cl[t]['pred']))].astype(np.int64), t))
        P, n = substitui(Qp, k, mods)
        if n > 10: continue
        s_dir, e_dir = estado_sinal(P, n); s_f, e_f = formula(Qp, k, mods)
        ok_s &= s_dir == s_f; ok_e &= tuple(x % 2 for x in e_dir) == e_f
        rot = blocos(P[None, :], n)[0]; off = np.cumsum([0] + [t for _, t in mods])
        esperado = np.concatenate([[off[i]] * t for i, (_, t) in enumerate(mods)])
        ok_b &= np.array_equal(rot, esperado); testes += 1
    print(f'(V1) {testes} substituicoes aleatorias Q[M1..Mk] (k = 4..6, n <= 10): sinal {ok_s}; estado {ok_e}; modulos recuperados {ok_b}')
    # ---- (O) decomposicao de kappa e do carater trivial na raiz prima ----
    print('\nRaiz prima por estrutura de modulos (somas rotuladas com sinal; kappa = s(-1)^(D+U); trivial = s):')
    print(' n | trivial: estritamente prima / com modulos | kappa: estritamente prima / com modulos | sinal de kappa vs (-1)^n (total, estrita, com mod.)')
    det = {}
    for n in range(4, nmax + 1):
        d = cl[n]; E = estrutura(d['pred'], n); m = E['tipo'] == 2
        P = d['pred'][m]; L = (math.factorial(n) // d['aut'][m].astype(np.int64)); s = np.where(d['B'][m] % 2 == 0, 1, -1)
        u, dd = perfis(P, n); wk = L * s * (-1) ** ((dd[:, 1] + u[:, 1]) % 2); wt = L * s
        rot = blocos(P, n); tam = np.stack([(rot == j).sum(1) for j in range(n)], 1)
        nbl = (tam > 0).sum(1); estr = nbl == n; maior = tam.max(1); nnt = (tam >= 2).sum(1)
        a, b = int(wt[estr].sum()), int(wt[~estr].sum()); c, e = int(wk[estr].sum()), int(wk[~estr].sum())
        sg = ''.join('+' if x * (-1) ** n > 0 else ('0' if x == 0 else '-') for x in (c + e, c, e))
        print(f' {n:2d} | {a:+d} / {b:+d} | {c:+d} / {e:+d} | {sg}', flush=True)
        g = defaultdict(lambda: [0, 0, 0])
        for chave, vk, vt in zip(zip(nnt.tolist(), maior.tolist()), wk.tolist(), wt.tolist()):
            g[chave][0] += vk; g[chave][1] += vt; g[chave][2] += 1
        det[n] = g
    print('\nkappa na raiz prima por (numero de modulos nao triviais, maior modulo), n = 8..10:')
    for n in range(8, nmax + 1):
        it = sorted(det[n].items(), key=lambda kv: -abs(kv[1][0]))[:6]
        print(f'  n={n}: ' + '; '.join(f'{k}: kappa {v[0]:+d} ({v[2]} classes)' for k, v in it))

if __name__ == '__main__':
    main(sys.argv[1])
