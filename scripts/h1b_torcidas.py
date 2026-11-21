"""ANALITICO/EXPLORATORIO (21/11/2026): somas torcidas, todas as ordens, theta = pi.
 tau_n   = sum_P s(P) (-1)^(m+D)          (torcao inferior; a superior e igual por dualidade)
 omega_n = sum_P s(P) (-1)^(m+D+M+U)      (torcao dupla; entra em S_ambos)
 (0) = restrita as ordens sem pontos isolados.
Identidades: tau = sum_j C(n,j) tau0_(n-j)   [ponto isolado: s -> -s, m -> m+1, D igual: peso torcido invariante]
             omega = sum_j C(n,j) (-1)^j omega0_(n-j)   [m -> m+1 e M -> M+1: peso duplamente torcido troca de sinal]
Uso: python h1b_torcidas.py PASTA"""
import sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_paridade_explora import estrutura
from h1b_soma_ordinal import perfis

def main(pasta, nmax=10):
    t, t0, w, w0, a, Prim = {0: 1}, {0: 1}, {0: 1}, {0: 1}, {0: 1}, {}
    tt = {}                                         # tau por tipo
    for n in range(1, nmax + 1):
        d = np.load(f'{pasta}/h1b_N_n{n}.npz'); L = math.factorial(n) // d['aut'].astype(np.int64)
        s = np.where(d['B'] % 2 == 0, 1, -1).astype(np.int64); E = estrutura(d['pred'], n); u, dd = perfis(d['pred'], n)
        m, D, M, U = E['mini'], dd[:, 1], E['maxi'], u[:, 1]; iso = E['iso'] > 0; tp = E['tipo']
        vt = L * s * (-1) ** ((m + D) % 2); vw = L * s * (-1) ** ((m + D + M + U) % 2)
        t[n], t0[n] = int(vt.sum()), int(vt[~iso].sum()); w[n], w0[n] = int(vw.sum()), int(vw[~iso].sum())
        a[n] = int((L * s).sum()); Prim[n] = int((L * s)[tp == 2].sum())
        tt[n] = {k: int(vt[tp == j].sum()) for k, j in (('par', 0), ('ser', 1), ('prim', 2))}
        tt[n]['par0'] = int(vt[(tp == 0) & ~iso].sum())
    ok1 = all(t[n] == sum(math.comb(n, j) * t0[n - j] for j in range(n + 1)) for n in t)
    ok2 = all(t0[n] == sum((-1) ** j * math.comb(n, j) * t[n - j] for j in range(n + 1)) for n in t)
    ok3 = all(w[n] == sum((-1) ** j * math.comb(n, j) * w0[n - j] for j in range(n + 1)) for n in w)
    ok4 = all(w0[n] == sum(math.comb(n, j) * w[n - j] for j in range(n + 1)) for n in w)
    print(f'(V) tau = sum C(n,j) tau0: {ok1}; inversa: {ok2}; omega = sum C(n,j)(-1)^j omega0: {ok3}; inversa: {ok4}  (n = 0..{nmax})')
    # formula exponencial: peso torcido e multiplicativo na uniao disjunta -> tau = exp(tau_conexas)
    tc = {n: tt[n]['ser'] + tt[n]['prim'] for n in range(1, nmax + 1)}
    ok5 = all(t[n] == sum(math.comb(n - 1, k - 1) * tc[k] * t[n - k] for k in range(1, n + 1)) for n in range(1, nmax + 1))
    print(f'(V) tau = exp(tau das conexas) (formula exponencial): {ok5}')
    print('\n n | tau_n | tau0_n | sinal*(-1)^(n+1) tau, tau0 | tau por tipo: paralelo (sem isolados) / serie / raiz prima | omega_n | omega0_n')
    for n in range(1, nmax + 1):
        sg = lambda x: '+' if x * (-1) ** (n + 1) > 0 else ('0' if x == 0 else '-')
        print(f' {n:2d} | {t[n]:+d} | {t0[n]:+d} | {sg(t[n])} {sg(t0[n])} | {tt[n]["par0"]:+d} / {tt[n]["ser"]:+d} / {tt[n]["prim"]:+d} | {w[n]:+d} | {w0[n]:+d}')
    print('\nPeso de cada parcela de tau0_n (|parcela|/|tau0_n|): termo j=0 e soma dos termos j>=1 de tau = sum C(n,j) tau0_(n-j)')
    for n in range(4, nmax + 1):
        rest = t[n] - t0[n]
        print(f'  n={n}: tau = {t[n]:+d} = tau0 {t0[n]:+d} + (isolados) {rest:+d}; |isolados|/|tau| = {abs(rest)/abs(t[n]):.3f}')
    print('\nMagnitude frente a Prim_n e a parte de um ponto E_ext(n) = -2n tau_(n-1) - n(n-1)(+-)omega_(n-2):')
    for n in range(5, nmax + 1):
        S2 = -2 * n * t[n - 1]; Sbt = n * (n - 1) * w[n - 2] * (-1 if n - 2 <= 1 else 1)
        print(f'  n={n}: |2n tau_(n-1)|/|Prim_n| = {abs(S2)/abs(Prim[n]):.3f}; |n(n-1) omega_(n-2)|/|Prim_n| = {abs(Sbt)/abs(Prim[n]):.3f}; '
              f'E_ext = {S2 - Sbt:+d}; |tau_(n-1)|/|Prim_(n-1)| = {abs(t[n-1])/abs(Prim[n-1]) if Prim.get(n-1) else float("nan"):.3f}')

if __name__ == '__main__':
    main(sys.argv[1])
