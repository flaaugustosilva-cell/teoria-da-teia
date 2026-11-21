"""EXPLORATORIO/ANALITICO (21/11/2026): caracteres das somas refinadas e a alternancia da parte serie torcida.
Caractere c = (c_m, c_D, c_M, c_U) em Z2^4; X^[c] = sum_sigma X[sigma] (-1)^(c . sigma). tau = c (1,1,0,0); omega = (1,1,1,1).
Uso: python h1b_caracteres.py PASTA"""
import sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_soma_ordinal import somas_refinadas, idx

def bits(s): return s & 1, (s >> 1) & 1, (s >> 2) & 1, (s >> 3) & 1
NOME = lambda c: '(' + ','.join(str(x) for x in bits(c)) + ')'

def chi(X, c): return sum(X[s] * (-1) ** bin(s & c).count('1') for s in range(16))

def padrao(vals):
    """vals: dict n -> valor, n = 4..10. Classifica o sinal."""
    sg = {n: (v > 0) - (v < 0) for n, v in vals.items()}
    if all(sg[n] == 1 for n in sg): return 'sempre +'
    if all(sg[n] == -1 for n in sg): return 'sempre -'
    if all(sg[n] == (-1) ** n for n in sg): return '(-1)^n'
    if all(sg[n] == (-1) ** (n + 1) for n in sg): return '(-1)^(n+1)'
    return 'irregular' + (' (tem zero)' if 0 in sg.values() else '')

def serie_char_por_k(I, A, n, c):
    out = {}
    for k in range(1, n):
        q = n - k; tot = 0
        for s1 in range(16):
            if I[k][s1] == 0: continue
            m1, D1, M1, U1 = bits(s1)
            for s2 in range(16):
                if A[q][s2] == 0: continue
                m2, D2, M2, U2 = bits(s2)
                delta = (M1 * m2 + U1 * m2 + M1 * D2) & 1
                novo = idx(m1, D1 + (m2 if k == 1 else 0), M2, U2 + (M1 if q == 1 else 0))
                tot += I[k][s1] * A[q][s2] * (-1) ** (delta + bin(novo & c).count('1'))
        out[k] = math.comb(n, k) * tot
    return out

def main(pasta, nmax=10):
    R = somas_refinadas(pasta, nmax)
    A = {0: np.array([1] + [0] * 15, object), **{n: R[0][n] + R[1][n] + R[2][n] for n in range(1, nmax + 1)}}
    I = {n: R[0][n] + R[2][n] for n in range(1, nmax + 1)}
    print('1) Padrao de sinal de cada caractere, n = 4..10 (todas as ordens; e por tipo):')
    print('   caractere (m,D,M,U) | todas | paralelo | serie | raiz prima')
    for c in range(16):
        linha = [padrao({n: chi(A[n], c) for n in range(4, nmax + 1)})]
        for t in (0, 1, 2): linha.append(padrao({n: chi(R[t][n], c) for n in range(4, nmax + 1)}))
        print(f'   {NOME(c)} | ' + ' | '.join(linha))
    print('\n   Valores de alguns caracteres de TODAS as ordens, n = 1..10:')
    for c in (0, 0b0011, 0b0010, 0b0001, 0b1111, 0b1100, 0b0101, 0b1010):
        print(f'   {NOME(c)}: ' + ', '.join(f'{chi(A[n], c):+d}' for n in range(1, nmax + 1)))
    tau = 0b0011
    print('\n2) Parte serie torcida (caractere (1,1,0,0)) por tamanho k da peca de baixo (k=1: ponto embaixo; k=n-1 com Q ponto: ponto em cima):')
    for n in range(4, nmax + 1):
        pk = serie_char_por_k(I, A, n, tau); tot = sum(pk.values()); assert tot == chi(R[1][n], tau)
        borda = pk[1] + pk[n - 1]; meio = tot - borda
        print(f'   n={n}: total {tot:+d}; k=1 {pk[1]:+d}; k=n-1 {pk[n-1]:+d}; meio (2<=k<=n-2) {meio:+d}; '
              f'(borda)/total {borda/tot:+.2f}')
    print('\n3) Formulas dos termos de borda (D) conferidas:')
    for n in range(4, nmax + 1):
        pk = serie_char_por_k(I, A, n, tau)
        f1 = n * chi(A[n - 1], 0b0010)                       # {*} + Q: peso torcido = s(Q)(-1)^D(Q)  (n-1 >= 2)
        f2 = -n * chi(I[n - 1], 0b1111)                      # P1 + {*}, P1 indecomponivel: peso = -s(P1)(-1)^(m+D+M+U)
        print(f'   n={n}: k=1: {pk[1]:+d} = n * A_(n-1)^[(0,1,0,0)] = {f1:+d} ({pk[1] == f1}); '
              f'k=n-1: {pk[n-1]:+d} = -n * I_(n-1)^[(1,1,1,1)] = {f2:+d} ({pk[n-1] == f2})')

if __name__ == '__main__':
    main(sys.argv[1])

def propagacao(pasta, nmax=10):
    """Caractere D (0,1,0,0): peso w_D = s(P)(-1)^D(P). (D) w_D({*}+P) = -w_D(P); ponto isolado: w_D troca de sinal.
    Decompoe D_n = (ordens com menor elemento) + (com ponto isolado) + (com maior elemento e sem menor) + resto."""
    from h1b_paridade_explora import estrutura
    from h1b_soma_ordinal import perfis
    Dn = {0: 1}; partes = {}
    for n in range(1, nmax + 1):
        d = np.load(f'{pasta}/h1b_N_n{n}.npz'); L = math.factorial(n) // d['aut'].astype(np.int64)
        s = np.where(d['B'] % 2 == 0, 1, -1).astype(np.int64); E = estrutura(d['pred'], n); u, dd = perfis(d['pred'], n)
        w = L * s * (-1) ** (dd[:, 1] % 2); pc = np.array([bin(x).count('1') for x in range(1 << n)])
        bot = (pc[E['suc']] == n - 1).any(1); top = (pc[E['pred']] == n - 1).any(1); iso = E['iso'] > 0
        Dn[n] = int(w.sum())
        partes[n] = (int(w[bot].sum()), int(w[iso].sum()), int(w[top & ~bot].sum()), int(w[~bot & ~iso & ~(top & ~bot)].sum()))
    print('\n4) Caractere D de todas as ordens: propagacao da alternancia')
    print('   (D) {*}+P: w_D = -w_D(P)  =>  parte "menor elemento" = -n D_(n-1)  (n >= 2)')
    print('   n | D_n | menor elemento (= -n D_(n-1)?) | ponto isolado | maior e sem menor | resto | (menor+isolado)/D_n | D_n/D_(n-1)')
    for n in range(2, nmax + 1):
        b, i, t, r = partes[n]
        print(f'   {n:2d} | {Dn[n]:+d} | {b:+d} ({b == -n * Dn[n-1]}) | {i:+d} | {t:+d} | {r:+d} | {(b+i)/Dn[n]:+.2f} | {Dn[n]/Dn[n-1]:+.1f}')

if __name__ == '__main__' and len(sys.argv) > 2 and sys.argv[2] == 'prop':
    propagacao(sys.argv[1])
