"""EXPLORATORIO (21/11/2026): parte serie pelos elementos extremos, todas as ordens, theta = pi.
Sinal s = (-1)^(n + N0 + N1). Ordens com menor elemento: unica forma {*} (+) P, P qualquer em n-1 elementos.
  (D) s({*}+P) = -s(P) (-1)^(m(P)+D(P))       (o -1 vem de n -> n+1)
  (D) s(P+{*}) = -s(P) (-1)^(M(P)+U(P))
  (D) s({*}+P+{*}) = s(P) (-1)^(m+D+M+U) (-1)^[|P| <= 1]   (o par (bottom, top) tem |P| elementos entre si)
Uso: python h1b_serie_extremos.py PASTA"""
import sys, math, numpy as np
from collections import defaultdict
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_paridade_explora import estrutura
from h1b_soma_ordinal import perfis, idx

def bits(s): return s & 1, (s >> 1) & 1, (s >> 2) & 1, (s >> 3) & 1

def pecas(pred, suc, n):
    """Pecas ordinais (componentes do grafo de incomparabilidade) de baixo para cima: tamanhos."""
    full = (1 << n) - 1; out = []
    for p, q in zip(pred, suc):
        adj = [full & ~(int(p[i]) | int(q[i]) | (1 << i)) for i in range(n)]
        vis = 0; comps = []
        for i in range(n):
            if (vis >> i) & 1: continue
            c = 1 << i; fr = c
            while fr:
                nv = 0
                for j in range(n):
                    if (fr >> j) & 1: nv |= adj[j]
                fr = nv & ~c; c |= nv
            vis |= c; comps.append(c)
        # ordena de baixo para cima: componente com menos predecessores primeiro
        chave = [bin(int(p[(c & -c).bit_length() - 1])).count('1') for c in comps]
        out.append(tuple(bin(comps[k]).count('1') for k in np.argsort(chave)))
    return out

def main(pasta, nmax=10):
    A = {}; dados = {}
    for n in range(1, nmax + 1):
        d = np.load(f'{pasta}/h1b_N_n{n}.npz'); L = math.factorial(n) // d['aut'].astype(np.int64)
        s = np.where(d['B'] % 2 == 0, 1, -1).astype(np.int64); E = estrutura(d['pred'], n); u, dd = perfis(d['pred'], n)
        st = idx(E['mini'], dd[:, 1], E['maxi'], u[:, 1]); Ls = L * s
        A[n] = np.array([int(Ls[st == k].sum()) for k in range(16)], object)
        pc = np.array([bin(x).count('1') for x in range(1 << n)])
        bot = (pc[E['suc']] == n - 1).any(1); top = (pc[E['pred']] == n - 1).any(1)
        dados[n] = dict(L=L, s=s, Ls=Ls, tipo=E['tipo'], bot=bot, top=top, pred=E['pred'], suc=E['suc'])
    A[0] = np.array([1] + [0] * 15, object)
    tw = lambda v, f: sum(v[k] * (-1) ** f(*bits(k)) for k in range(16))
    print('Somas "torcidas" (todas as ordens): tau_bot(n) = sum A_n[s] (-1)^(m+D), tau_top(n) = sum A_n[s] (-1)^(M+U); dualidade exige igualdade')
    for n in range(1, nmax + 1):
        print(f'  n={n}: tau_bot {tw(A[n], lambda m, D, M, U: m + D):+d}  tau_top {tw(A[n], lambda m, D, M, U: M + U):+d}')
    pred_bot = lambda n: -n * tw(A[n - 1], lambda m, D, M, U: m + D)
    pred_top = lambda n: -n * tw(A[n - 1], lambda m, D, M, U: M + U)
    pred_bt = lambda n: n * (n - 1) * tw(A[n - 2], lambda m, D, M, U: m + D + M + U) * (-1 if n - 2 <= 1 else 1)
    print('\n1-2) Identidades (D) contra os dados (V), n = 2 a 10; S_bot, S_top, S_bot&top = somas com sinal das ordens com menor, maior, ambos')
    print(' n | S_bot dado / previsto | S_top dado / previsto | S_ambos dado / previsto | Ser_n | S_ext = S_bot + S_top - S_ambos | residuo R_n = Ser - S_ext')
    res = {}; ok = True
    for n in range(2, nmax + 1):
        D = dados[n]; Sb = int(D['Ls'][D['bot']].sum()); St = int(D['Ls'][D['top']].sum()); Sbt = int(D['Ls'][D['bot'] & D['top']].sum())
        Ser = int(D['Ls'][D['tipo'] == 1].sum()); ext = Sb + St - Sbt; res[n] = Ser - ext
        ok &= (Sb, St, Sbt) == (pred_bot(n), pred_top(n), pred_bt(n))
        ok &= bool(np.all(D['tipo'][D['bot'] | D['top']] == 1)) if n >= 2 else True
        print(f' {n:2d} | {Sb:+d} / {pred_bot(n):+d} | {St:+d} / {pred_top(n):+d} | {Sbt:+d} / {pred_bt(n):+d} | {Ser:+d} | {ext:+d} | {res[n]:+d}')
    print(f'   identidades conferem em todo n e toda ordem com extremo e do tipo serie: {ok}')
    Ser11 = 1787428412
    e11 = pred_bot(11) + pred_top(11) - pred_bt(11)
    print(f'\n   n = 11 pela identidade (todas as ordens): S_bot = S_top = {pred_bot(11):+d}; S_ambos = {pred_bt(11):+d}; S_ext = {e11:+d}; '
          f'Ser_11 = {Ser11:+d} (R1 = R2); residuo R_11 = {Ser11 - e11:+d}')
    print('\n4) Estrutura do residuo (ordens tipo serie SEM menor e SEM maior elemento), n = 6 a 10:')
    for n in range(6, nmax + 1):
        D = dados[n]; m = (D['tipo'] == 1) & ~D['bot'] & ~D['top']
        P = pecas(D['pred'][m], D['suc'][m], n); Ls = D['Ls'][m]; L = D['L'][m]
        pk = defaultdict(lambda: [0, 0])
        for t, v, w in zip(P, Ls, L):
            pk[len(t)][0] += int(v); pk[len(t)][1] += int(w)
        print(f'  n={n}: residuo {int(Ls.sum()):+d} sobre {int(L.sum()):.3e} ordens; por numero de pecas ordinais: '
              + '; '.join(f'{k}: {v[0]:+d} ({v[0]/v[1]:+.1e})' for k, v in sorted(pk.items())))

if __name__ == '__main__':
    main(sys.argv[1])
