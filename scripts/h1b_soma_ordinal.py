"""Identidade da soma ordinal (dados/h1b/ANALITICO_3.md) e recursao exata das somas rotuladas com sinal.
Uso:
  python h1b_soma_ordinal.py verifica PASTA        -> (a) verificacao ponto a ponto, todos os pares |P|+|Q| <= 10;
                                                      (b) recursao agregada para n <= 10 (todas as ordens)
  python h1b_soma_ordinal.py c3 PASTA PASTA_N11     -> previsao da soma de raiz prima em n = 11 pela identidade
                                                      (so depois do pre-registro PREREGISTRO_C3.md)
Estado de uma ordem: sigma = (m, D, M, U) mod 2, com m = #minimos, D = #elementos com exatamente 1 elemento abaixo,
M = #maximos, U = #elementos com exatamente 1 elemento acima. Sinal s = (-1)^B = (-1)^(n + N0 + N1)."""
import sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_modelo_rede import contagens
from h1b_paridade_explora import estrutura

def perfis(pred, n):
    """u[:, a] = #elementos com exatamente a acima; d[:, b] = #elementos com exatamente b abaixo."""
    pred = pred.astype(np.int64); pop = np.array([bin(x).count('1') for x in range(1 << n)], np.int64)
    suc = np.zeros_like(pred)
    for k in range(n):
        for i in range(n): suc[:, i] |= ((pred[:, k] >> i) & 1) << k
    ac, ab = pop[suc], pop[pred]
    u = np.stack([(ac == a).sum(1) for a in range(max(n, 2))], 1); d = np.stack([(ab == b).sum(1) for b in range(max(n, 2))], 1)
    return u, d

def soma_ordinal(pP, a, pQ, b):
    """pred de P (+) Q: P nos elementos 0..a-1, Q nos elementos a..a+b-1, tudo de P abaixo de tudo de Q."""
    lo = (1 << a) - 1
    return np.concatenate([pP, (pQ << a) | lo], 1)

def verifica_pontual(pasta, nmax=10):
    cl = {k: np.load(f'{pasta}/h1b_N_n{k}.npz')['pred'].astype(np.int64) for k in range(1, nmax)}
    NN = {k: contagens(cl[k], k) for k in cl}; PF = {k: perfis(cl[k], k) for k in cl}
    total = 0
    for a in range(1, nmax):
        for b in range(1, nmax - a + 1):
            iP, iQ = np.meshgrid(np.arange(len(cl[a])), np.arange(len(cl[b])), indexing='ij'); iP, iQ = iP.ravel(), iQ.ravel()
            for s0 in range(0, len(iP), 200_000):
                jP, jQ = iP[s0:s0+200_000], iQ[s0:s0+200_000]
                N = contagens(soma_ordinal(cl[a][jP], a, cl[b][jQ], b), a + b)
                u, d = PF[a][0][jP], PF[b][1][jQ]
                X = np.stack([sum((u[:, x] * d[:, k - x] for x in range(k + 1) if x < a and k - x < b), np.zeros(len(jP), np.int64)) for k in range(4)], 1)
                prev = NN[a][jP] + NN[b][jQ] + X
                if not np.array_equal(prev, N): raise SystemExit(f'FALHA da identidade em |P|={a}, |Q|={b}')
                total += len(jP)
    print(f'(a) identidade N_k(P+Q) = N_k(P) + N_k(Q) + sum_(x+y=k) u_x(P) d_y(Q), k = 0..3: '
          f'confere em todos os {total} pares de classes com |P| + |Q| <= {nmax}')

# ---------------- recursao agregada ----------------
def idx(m, D, M, U): return (m & 1) | ((D & 1) << 1) | ((M & 1) << 2) | ((U & 1) << 3)

def somas_refinadas(pasta, nmax=10):
    """R[tipo][n] = vetor de 16 inteiros: soma rotulada de s por estado; tipo 0 paralelo, 1 serie, 2 raiz prima."""
    R = {t: {} for t in (0, 1, 2)}
    for n in range(1, nmax + 1):
        d = np.load(f'{pasta}/h1b_N_n{n}.npz'); L = math.factorial(n) // d['aut'].astype(np.int64)
        s = np.where(d['B'] % 2 == 0, 1, -1).astype(np.int64); E = estrutura(d['pred'], n)
        u, dd = perfis(d['pred'], n)
        st = idx(E['mini'], dd[:, 1], E['maxi'], u[:, 1])
        for t in (0, 1, 2):
            m = E['tipo'] == t; v = np.zeros(16, object)
            for k in range(16): v[k] = int((L * s)[m & (st == k)].sum())
            R[t][n] = v
    return R

def xor_conv(x, y):
    z = np.zeros(16, object)
    for i in range(16):
        if x[i] == 0: continue
        for j in range(16): z[i ^ j] += x[i] * y[j]
    return z

def serie_de(I, A, n):
    """Soma das ordens tipo serie em n: P (+) Q, P indecomponivel em serie (k elementos), Q qualquer (n-k)."""
    z = np.zeros(16, object)
    for k in range(1, n):
        c = math.comb(n, k); q = n - k
        for s1 in range(16):
            if I[k][s1] == 0: continue
            m1, D1, M1, U1 = s1 & 1, (s1 >> 1) & 1, (s1 >> 2) & 1, (s1 >> 3) & 1
            for s2 in range(16):
                if A[q][s2] == 0: continue
                m2, D2, M2, U2 = s2 & 1, (s2 >> 1) & 1, (s2 >> 2) & 1, (s2 >> 3) & 1
                delta = (M1 * m2 + U1 * m2 + M1 * D2) & 1
                novo = idx(m1, D1 + (m2 if k == 1 else 0), M2, U2 + (M1 if q == 1 else 0))
                z[novo] += c * I[k][s1] * A[q][s2] * (-1 if delta else 1)
    return z

def paralelo_de(Conn, A, n):
    """Exponencial: A_n = sum_k C(n-1,k-1) Conn_k * A_(n-k); a parte paralela exclui k = n."""
    z = np.zeros(16, object)
    for k in range(1, n):
        z += math.comb(n - 1, k - 1) * xor_conv(Conn[k], A[n - k])
    return z

def verifica_agregada(pasta, nmax=10):
    R = somas_refinadas(pasta, nmax)
    A = {0: np.array([1] + [0] * 15, object)}; Ad = {}
    for n in range(1, nmax + 1): Ad[n] = R[0][n] + R[1][n] + R[2][n]
    ok1 = ok2 = True
    for n in range(1, nmax + 1):                     # cada parte a partir dos DADOS de tamanhos menores
        Am = {0: A[0], **{k: Ad[k] for k in range(1, n)}}
        I = {k: R[0][k] + R[2][k] for k in range(1, n)}; Conn = {k: R[1][k] + R[2][k] for k in range(1, n)}
        ok1 &= all(serie_de(I, Am, n) == R[1][n]) and all(paralelo_de(Conn, Am, n) == R[0][n])
    P = {k: R[2][k] for k in range(1, nmax + 1)}; A2 = {0: A[0]}; S2 = {}; Pa2 = {}
    for n in range(1, nmax + 1):                     # recursao PURA: so as ordens de raiz prima entram como dado
        I = {k: Pa2[k] + P[k] for k in range(1, n)}; Conn = {k: S2[k] + P[k] for k in range(1, n)}
        S2[n] = serie_de(I, A2, n); Pa2[n] = paralelo_de(Conn, A2, n); A2[n] = S2[n] + Pa2[n] + P[n]
        ok2 &= all(A2[n] == Ad[n])
    print(f'(b1) partes paralela e serie de cada n <= {nmax} reproduzidas exatamente a partir dos tamanhos menores: {ok1}')
    print(f'(b2) recursao pura (so raiz prima como dado) reproduz exatamente as somas de todas as ordens, n <= {nmax}: {ok2}')
    print(' n | raiz prima (dado) | paralelo | serie | todas')
    for n in range(1, nmax + 1):
        print(f' {n:2d} | {int(P[n].sum()):+d} | {int(Pa2[n].sum()):+d} | {int(S2[n].sum()):+d} | {int(A2[n].sum()):+d}')
    return R, ok1 and ok2

def c3(pasta, pasta11):
    """PREREGISTRO_C3.md, rota R1: Prim_11 = T_todas(11) - Par_11 - Ser_11."""
    R = somas_refinadas(pasta, 10)
    A = {0: np.array([1] + [0] * 15, object), **{k: R[0][k] + R[1][k] + R[2][k] for k in range(1, 11)}}
    I = {k: R[0][k] + R[2][k] for k in range(1, 11)}; Con = {k: R[1][k] + R[2][k] for k in range(1, 11)}
    ser11, par11 = int(serie_de(I, A, 11).sum()), int(paralelo_de(Con, A, 11).sum())
    Ttodas = Truins = 0; classes = 0
    for x in range(20):
        d = np.load(f'{pasta11}/h1b_N11_n11_parte{x}.npz')
        for (b, h3, c), p in zip(d['chaves'], d['peso']):
            v = int(p) * (1 if b % 2 == 0 else -1); Ttodas += v
            if not h3: Truins += v
        classes += int(d['total_classes'])
    print(f'validacao: classes nas 20 partes = {classes} (A000112(11) = 46749427); soma das ruins = {Truins} (formula fechada: -1)')
    if classes != 46749427 or Truins != -1: raise SystemExit('VALIDACAO FALHOU -- sem veredito')
    prim = Ttodas - par11 - ser11
    print(f'T_todas(11) = {Ttodas:+d}; paralelo(11) = {par11:+d}; serie(11) = {ser11:+d}')
    print(f'Prim_11 = {prim:+d}  ->  C3 em n = 11: {"SUCESSO (negativa)" if prim < 0 else "FALHA (nao negativa)"}')
    print(f'descritivo: Prim_11 / T_todas(11) = {prim / Ttodas:.3f}')

if __name__ == '__main__':
    if sys.argv[1] == 'verifica':
        verifica_pontual(sys.argv[2]); verifica_agregada(sys.argv[2])
    elif sys.argv[1] == 'c3':
        c3(sys.argv[2], sys.argv[3])
