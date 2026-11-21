"""EXPLORATORIO/ANALITICO (20/11/2026): tamanho das partes paralela e serie frente a raiz prima, todas as ordens.
Usa as somas refinadas de n <= 10 (dados n9n10) e, para n = 11, os valores da rota R1 (RESULTADOS_C3.md).
Uso: python h1b_C3_analise.py PASTA"""
import sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_soma_ordinal import somas_refinadas, idx

def serie_por_k(I, A, n):
    """Ser_n separado pelo tamanho k da parte de baixo (total sobre estados)."""
    out = {}
    for k in range(1, n):
        c = math.comb(n, k); q = n - k; tot = 0
        for s1 in range(16):
            if I[k][s1] == 0: continue
            m1, D1, M1, U1 = s1 & 1, (s1 >> 1) & 1, (s1 >> 2) & 1, (s1 >> 3) & 1
            for s2 in range(16):
                if A[q][s2] == 0: continue
                m2, D2 = s2 & 1, (s2 >> 1) & 1
                tot += c * I[k][s1] * A[q][s2] * (-1 if (M1 * m2 + U1 * m2 + M1 * D2) & 1 else 1)
        out[k] = tot
    return out

def main(pasta):
    R = somas_refinadas(pasta, 10)
    A = {0: np.array([1] + [0] * 15, object), **{k: R[0][k] + R[1][k] + R[2][k] for k in range(1, 11)}}
    I = {k: R[0][k] + R[2][k] for k in range(1, 11)}
    a = {k: int(A[k].sum()) for k in A}; con = {k: int((R[1][k] + R[2][k]).sum()) for k in range(1, 11)}
    prim = {k: int(R[2][k].sum()) for k in range(1, 11)}; ser = {k: int(R[1][k].sum()) for k in range(1, 11)}
    prim[11] = -77098086120; ser[11] = 1787428412; con[11] = prim[11] + ser[11]; a[11] = -40491236963   # R1
    # pesos (numero de ordens rotuladas) por tipo, n <= 10
    W = {}
    for n in range(1, 11):
        d = np.load(f'{pasta}/h1b_N_n{n}.npz'); L = math.factorial(n) // d['aut'].astype(np.int64)
        from h1b_paridade_explora import estrutura
        t = estrutura(d['pred'], n)['tipo']; W[n] = [int(L[t == k].sum()) for k in (0, 1, 2)]
    print('1) Formula exponencial nos totais: a_n = sum_k C(n-1,k-1) con_k a_(n-k) (k = tamanho da componente do rotulo 1)')
    print('   Parte paralela por k (n = 8 a 11):')
    for n in range(8, 12):
        termos = {k: math.comb(n - 1, k - 1) * con[k] * a[n - k] for k in range(1, n)}
        par = sum(termos.values())
        top = sorted(termos.items(), key=lambda kv: -abs(kv[1]))[:3]
        print(f'   n={n}: Par = {par:+d}; maiores termos: ' + ', '.join(f'k={k}: {v:+d} ({v/par:+.2f})' for k, v in top))
    print('   Ponto isolado: os termos k=1 (o rotulo 1 isolado) e k=n-1 (uma conexa de n-1 + um ponto isolado) valem -a_(n-1) e -(n-1) con_(n-1).')
    print('2) Parte serie por tamanho k da parte de baixo (n = 8 a 10, e 11 pela recursao):')
    for n in range(8, 12):
        Ik = {k: I[k] for k in range(1, min(n, 11))}; Ak = {q: A[q] for q in range(0, min(n, 11))}
        sk = serie_por_k(Ik, Ak, n); tot = sum(sk.values())
        top = sorted(sk.items(), key=lambda kv: -abs(kv[1]))[:3]
        print(f'   n={n}: Ser = {tot:+d}; maiores: ' + ', '.join(f'k={k}: {v:+d} ({v/tot:+.2f})' for k, v in top))
    print('3) Razoes de crescimento e vies (todas as ordens):')
    print('   n | Prim_n | con_n/con_(n-1) | |Par|/|Prim| | |Ser|/|Prim| | vies Prim/peso_prim | fracao de peso (par, serie, prima)')
    for n in range(5, 12):
        par = a[n] - con[n]
        vies = f'{prim[n]/W[n][2]:+.2e}' if n in W else '   -   '
        fr = '(' + ', '.join(f'{w/sum(W[n]):.3f}' for w in W[n]) + ')' if n in W else ''
        print(f'   {n:2d} | {prim[n]:+d} | {con[n]/con[n-1]:+.1f} | {abs(par)/abs(prim[n]):.3f} | {abs(ser[n])/abs(prim[n]):.3f} | {vies} | {fr}')
    print('4) Cota grosseira: |Par_n| <= (numero de ordens rotuladas desconexas), |Ser_n| <= (numero do tipo serie):')
    for n in range(6, 11):
        print(f'   n={n}: |Prim_n| = {abs(prim[n]):.3e}; desconexas {W[n][0]:.3e}; serie {W[n][1]:.3e} -> cota basta? {abs(prim[n]) > W[n][0] + W[n][1] + 1}')

if __name__ == '__main__':
    main(sys.argv[1])
