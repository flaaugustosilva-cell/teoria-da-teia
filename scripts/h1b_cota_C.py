"""EXPLORATORIO/ANALITICO (21/11/2026): cota de C_n = Par_n + Ser_n por somas com sinal, theta = pi.
Decomposicao exata (n >= 2), todas as ordens:
  C_n = E_n + Q_n
  E_n = E_iso + E_ext   (ordens com ponto isolado; ordens com menor ou maior elemento) -- "um ponto"
  Q_n = Q_par + Q_ser   (paralelas sem ponto isolado; serie sem menor e sem maior)   -- "compostos nao triviais"
Formulas a partir de tamanhos menores:
  E_iso = sum_{j>=1} C(n,j)(-1)^j b_(n-j);  E_ext = S_bot + S_top - S_ambos (EXPLORATORIO_SERIE_EXTREMOS)
  Q_par = sum_{k=2}^{n-2} C(n-1,k-1) con_k b_(n-k)
  Q_ser = sum_{k=2}^{n-2} C(n,k) sum_{s1,s2} I_k[s1] A'_(n-k)[s2] (-1)^Delta,  A' = ordens SEM maior elemento
Uso: python h1b_cota_C.py PASTA"""
import sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_paridade_explora import estrutura
from h1b_soma_ordinal import perfis, idx

def bits(s): return s & 1, (s >> 1) & 1, (s >> 2) & 1, (s >> 3) & 1

def ref(Ls, st, m):
    return np.array([int(Ls[m & (st == k)].sum()) for k in range(16)], object)

def carrega(pasta, nmax=10):
    X = {}
    for n in range(1, nmax + 1):
        d = np.load(f'{pasta}/h1b_N_n{n}.npz'); L = math.factorial(n) // d['aut'].astype(np.int64)
        s = np.where(d['B'] % 2 == 0, 1, -1).astype(np.int64); E = estrutura(d['pred'], n); u, dd = perfis(d['pred'], n)
        st = idx(E['mini'], dd[:, 1], E['maxi'], u[:, 1]); Ls = L * s; t = E['tipo']
        pc = np.array([bin(x).count('1') for x in range(1 << n)])
        bot = (pc[E['suc']] == n - 1).any(1); top = (pc[E['pred']] == n - 1).any(1); iso = E['iso'] > 0
        tudo = np.ones(len(L), bool); boa = d['h'] >= 3
        X[n] = dict(A=ref(Ls, st, tudo), Par=ref(Ls, st, t == 0), Ser=ref(Ls, st, t == 1), Prim=ref(Ls, st, t == 2),
                    b=ref(Ls, st, ~iso), top=ref(Ls, st, top), Eiso=ref(Ls, st, iso), Eext=ref(Ls, st, bot | top),
                    Qpar=ref(Ls, st, (t == 0) & ~iso), Qser=ref(Ls, st, (t == 1) & ~bot & ~top),
                    boa={k: int(Ls[boa & (t == j)].sum()) for k, j in (('Par', 0), ('Ser', 1), ('Prim', 2))})
    return X

def Qser_por_k(X, n, Iget, Aget):
    out = {}
    for k in range(2, n - 1):
        q = n - k; c = math.comb(n, k); I = Iget(k); Ap = Aget(q); tot = 0; tabs = 0
        for s1 in range(16):
            if I[s1] == 0: continue
            m1, D1, M1, U1 = bits(s1)
            for s2 in range(16):
                if Ap[s2] == 0: continue
                m2, D2, _, _ = bits(s2)
                v = c * I[s1] * Ap[s2] * (-1 if (M1 * m2 + U1 * m2 + M1 * D2) & 1 else 1)
                tot += v; tabs += abs(v)
        out[k] = (tot, tabs)
    return out

def main(pasta):
    X = carrega(pasta)
    T = lambda v: int(sum(v))
    a = {0: 1, **{n: T(X[n]['A']) for n in X}}; b = {0: 1, **{n: T(X[n]['b']) for n in X}}
    con = {n: T(X[n]['Ser']) + T(X[n]['Prim']) for n in X}
    tw = lambda v, f: sum(v[k] * (-1) ** f(*bits(k)) for k in range(16))
    A0 = np.array([1] + [0] * 15, object)
    Aget = lambda n: A0 if n == 0 else X[n]['A']
    def Sext(n):
        sb = -n * tw(Aget(n - 1), lambda m, D, M, U: m + D); st_ = -n * tw(Aget(n - 1), lambda m, D, M, U: M + U)
        sbt = n * (n - 1) * tw(Aget(n - 2), lambda m, D, M, U: m + D + M + U) * (-1 if n - 2 <= 1 else 1)
        return sb + st_ - sbt
    # ---- (V) a decomposicao e as formulas conferem com os dados, n = 4..10 ----
    ok = True
    for n in range(4, 11):
        Eiso_f = sum(math.comb(n, j) * (-1) ** j * b[n - j] for j in range(1, n + 1))
        Qpar_f = sum(math.comb(n - 1, k - 1) * con[k] * b[n - k] for k in range(2, n - 1))
        Qser_f = sum(v[0] for v in Qser_por_k(X, n, lambda k: X[k]['Par'] + X[k]['Prim'], lambda q: X[q]['A'] - X[q]['top']).values())
        C = T(X[n]['Par']) + T(X[n]['Ser'])
        ok &= (Eiso_f, Sext(n), Qpar_f, Qser_f) == (T(X[n]['Eiso']), T(X[n]['Eext']), T(X[n]['Qpar']), T(X[n]['Qser']))
        ok &= C == Eiso_f + Sext(n) + Qpar_f + Qser_f
    print(f'(V) C_n = E_iso + E_ext + Q_par + Q_ser, cada parte pela formula de tamanhos menores = contagem direta, n = 4..10: {ok}')
    # ---- n = 11 (todas as ordens): valores de R1 = R2 e formulas ----
    Prim = {n: T(X[n]['Prim']) for n in X}; Par = {n: T(X[n]['Par']) for n in X}; Ser = {n: T(X[n]['Ser']) for n in X}
    Prim[11], Par[11], Ser[11], a[11] = -77098086120, 34819420745, 1787428412, -40491236963
    b[11] = sum(math.comb(11, j) * a[11 - j] for j in range(12)); con[11] = Prim[11] + Ser[11]
    print('\nTODAS AS ORDENS. Razoes em relacao a |Prim_n| (C = Par + Ser; E = um ponto; Q = compostos; Qbar = |.| por k com estados exatos;')
    print('Qtil = |.| por k e por par de estados; L1 = soma dos |.| de todos os estados de tamanho n-1)')
    print(' n | Prim_n | |C|/|P| | (|Par|+|Ser|)/|P| | |Par|/|P| | |Ser|/|P| | |E|/|P| | |Q|/|P| | (|E|+Qbar)/|P| | (|E|+Qtil)/|P|')
    linhas = {}
    for n in range(5, 12):
        Eiso = sum(math.comb(n, j) * (-1) ** j * b[n - j] for j in range(1, n + 1)); Ee = Sext(n); E = Eiso + Ee
        qp = {k: math.comb(n - 1, k - 1) * con[k] * b[n - k] for k in range(2, n - 1)}
        qp_til = {k: math.comb(n - 1, k - 1) * sum(abs(x) for x in X[k]['Ser'] + X[k]['Prim']) * sum(abs(x) for x in X[n - k]['b']) for k in range(2, n - 1)}
        qs = Qser_por_k(X, n, lambda k: X[k]['Par'] + X[k]['Prim'], lambda q: X[q]['A'] - X[q]['top'])
        Q = sum(qp.values()) + sum(v[0] for v in qs.values())
        Qbar = sum(abs(v) for v in qp.values()) + sum(abs(v[0]) for v in qs.values())
        Qtil = sum(qp_til.values()) + sum(v[1] for v in qs.values())
        C = Par[n] + Ser[n]; P = abs(Prim[n])
        if C != E + Q: raise SystemExit(f'decomposicao falhou em n={n}')
        linhas[n] = (E, Q, Qbar, Qtil)
        print(f' {n:2d} | {Prim[n]:+d} | {abs(C)/P:.3f} | {(abs(Par[n])+abs(Ser[n]))/P:.3f} | {abs(Par[n])/P:.3f} | {abs(Ser[n])/P:.3f} | '
              f'{abs(E)/P:.3f} | {abs(Q)/P:.3f} | {(abs(E)+Qbar)/P:.3f} | {(abs(E)+Qtil)/P:.3f}')
    print('\nPartes de E e Q (todas as ordens):')
    for n in range(5, 12):
        Eiso = sum(math.comb(n, j) * (-1) ** j * b[n - j] for j in range(1, n + 1)); E, Q, _, _ = linhas[n]
        lead = -n * b[n - 1] - 2 * n * tw(Aget(n - 1), lambda m, D, M, U: m + D)
        print(f'  n={n}: E_iso {Eiso:+d}; E_ext {E - Eiso:+d}; termo de ordem n-1 [-n b_(n-1) - 2n tau(n-1)] = {lead:+d} ({lead/E:+.2f} de E); Q {Q:+d}')
    print('\nCrescimento: |Prim_n|/|Prim_(n-1)| e |Prim_n| / (n * L1_(n-1)), L1 = soma dos |A_(n-1)[s]|:')
    for n in range(6, 12):
        L1 = sum(abs(x) for x in X[n - 1]['A'])
        print(f'  n={n}: {abs(Prim[n])/abs(Prim[n-1]):.1f}; {abs(Prim[n])/(n*L1):.3f}')
    print('\nPOPULACAO OFICIAL (altura >= 3, n = 5..10; a recursao NAO vale dentro dela; so descritivo):')
    for n in range(5, 11):
        bo = X[n]['boa']; P = abs(bo['Prim'])
        r = f'{abs(bo["Par"] + bo["Ser"])/P:.3f}' if P else 'Prim = 0'
        print(f'  n={n}: Prim {bo["Prim"]:+d}; Par {bo["Par"]:+d}; Ser {bo["Ser"]:+d}; |Par+Ser|/|Prim| = {r}')

if __name__ == '__main__':
    main(sys.argv[1])
