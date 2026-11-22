"""ANALITICO/EXPLORATORIO (22/11/2026): os caracteres chi = (0,1,1,1) e kappa = (0,1,0,1), todas as ordens, theta = pi.
Ordem dos componentes: (c_m, c_D, c_M, c_U). s(P) = (-1)^(n + N0 + N1).
  chi:   w(P) = s (-1)^(D+M+U)      kappa: w(P) = s (-1)^(D+U)
Operacoes de um ponto (|P| >= 2), deducao em ANALITICO_8.md:
  chi:   isolado: invariante;  {bot}+P: -w(P);  P+{top}: +w_kappa(P)
  kappa: isolado: -w(P);       {bot}+P: -w(P);  P+{top}: -w(P)
Uso: python h1b_carater_0111.py PASTA"""
import sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_paridade_explora import estrutura
from h1b_soma_ordinal import perfis

def main(pasta, nmax=10):
    X = {}
    for n in range(1, nmax + 1):
        d = np.load(f'{pasta}/h1b_N_n{n}.npz'); L = math.factorial(n) // d['aut'].astype(np.int64)
        s = np.where(d['B'] % 2 == 0, 1, -1).astype(np.int64); E = estrutura(d['pred'], n); u, dd = perfis(d['pred'], n)
        D, M, U = dd[:, 1], E['maxi'], u[:, 1]
        pc = np.array([bin(x).count('1') for x in range(1 << n)])
        bot = (pc[E['suc']] == n - 1).any(1); top = (pc[E['pred']] == n - 1).any(1); iso = E['iso'] > 0; t = E['tipo']
        X[n] = {}
        for nome, e in (('chi', D + M + U), ('kappa', D + U)):
            w = L * s * (-1) ** (e % 2); r = ~bot & ~top & ~iso
            X[n][nome] = dict(tot=int(w.sum()), sem_iso=int(w[~iso].sum()), bot=int(w[bot].sum()), top=int(w[top].sum()),
                              ambos=int(w[bot & top].sum()), iso=int(w[iso].sum()),
                              r_par=int(w[r & (t == 0)].sum()), r_ser=int(w[r & (t == 1)].sum()), r_prim=int(w[r & (t == 2)].sum()))
    c = {n: X[n]['chi']['tot'] for n in X}; k = {n: X[n]['kappa']['tot'] for n in X}; c[0] = k[0] = 1
    c0 = {0: 1, **{n: X[n]['chi']['sem_iso'] for n in X}}; k0 = {0: 1, **{n: X[n]['kappa']['sem_iso'] for n in X}}
    # (V) identidades
    v = {}
    v['chi: isolado invariante, chi = sum C(n,j) chi0'] = all(c[n] == sum(math.comb(n, j) * c0[n - j] for j in range(n + 1)) for n in X)
    v['kappa: isolado troca, kappa = sum C(n,j)(-1)^j kappa0'] = all(k[n] == sum(math.comb(n, j) * (-1) ** j * k0[n - j] for j in range(n + 1)) for n in X)
    v['chi: menor elemento = -n chi_(n-1)  (n>=3)'] = all(X[n]['chi']['bot'] == -n * c[n - 1] for n in range(3, nmax + 1))
    v['chi: maior elemento = +n kappa_(n-1)  (n>=3)'] = all(X[n]['chi']['top'] == n * k[n - 1] for n in range(3, nmax + 1))
    v['kappa: menor elemento = -n kappa_(n-1)  (n>=3)'] = all(X[n]['kappa']['bot'] == -n * k[n - 1] for n in range(3, nmax + 1))
    v['kappa: maior elemento = -n kappa_(n-1)  (n>=3)'] = all(X[n]['kappa']['top'] == -n * k[n - 1] for n in range(3, nmax + 1))
    v['kappa: ambos = +n(n-1) kappa_(n-2)  (n>=4)'] = all(X[n]['kappa']['ambos'] == n * (n - 1) * k[n - 2] for n in range(4, nmax + 1))
    v['chi: ambos = -n(n-1) kappa_(n-2)  (n>=4)'] = all(X[n]['chi']['ambos'] == -n * (n - 1) * k[n - 2] for n in range(4, nmax + 1))
    for nome, ok in v.items(): print(f'(V) {nome}: {ok}')
    for nome in ('kappa', 'chi'):
        print(f'\nDecomposicao de {nome}_n (todas as ordens): um ponto = menor + maior - ambos + isolado; resto = sem extremos e sem isolados, por tipo')
        print(' n | total | menor | maior | -ambos | isolado | resto paralelo | resto serie | resto raiz prima | (um ponto)/total | sinais vs (-1)^n')
        for n in range(4, nmax + 1):
            x = X[n][nome]; um = x['bot'] + x['top'] - x['ambos'] + x['iso']
            assert x['tot'] == um + x['r_par'] + x['r_ser'] + x['r_prim']
            partes = [x['tot'], x['bot'], x['top'], -x['ambos'], x['iso'], x['r_par'], x['r_ser'], x['r_prim']]
            sg = ''.join('+' if p * (-1) ** n > 0 else ('0' if p == 0 else '-') for p in partes)
            print(f' {n:2d} | ' + ' | '.join(f'{p:+d}' for p in partes) + f' | {um/x["tot"]:+.2f} | {sg}')

if __name__ == '__main__':
    main(sys.argv[1])

def regra_geral(pasta, nmax=10):
    """(V) Para os 16 caracteres c = (cm, cD, cM, cU):
       isolado: fator -(-1)^(cm+cM)   (ordens com pontos isolados: c = e^{fator x} c0)
       {bot}+P: c -> (1+cD, 1, cM, cU) com sinal -(-1)^cm   => parte 'menor' = n * sinal * A_(n-1)^[c']
       P+{top}: c -> (cm, cD, 1+cU, 1) com sinal -(-1)^cM   => parte 'maior' = n * sinal * A_(n-1)^[c']"""
    A = {}; partes = {}
    for n in range(1, nmax + 1):
        d = np.load(f'{pasta}/h1b_N_n{n}.npz'); L = math.factorial(n) // d['aut'].astype(np.int64)
        s = np.where(d['B'] % 2 == 0, 1, -1).astype(np.int64); E = estrutura(d['pred'], n); u, dd = perfis(d['pred'], n)
        st = [E['mini'], dd[:, 1], E['maxi'], u[:, 1]]
        pc = np.array([bin(x).count('1') for x in range(1 << n)])
        bot = (pc[E['suc']] == n - 1).any(1); top = (pc[E['pred']] == n - 1).any(1); iso = E['iso'] > 0
        for c in range(16):
            cv = [(c >> i) & 1 for i in range(4)]; w = L * s * (-1) ** (sum(cv[i] * st[i] for i in range(4)) % 2)
            A[n, c] = int(w.sum()); partes[n, c] = (int(w[bot].sum()), int(w[top].sum()), int(w[~iso].sum()))
    A.update({(0, c): 1 for c in range(16)})
    okb = okt = oki = True
    for c in range(16):
        cm, cD, cM, cU = [(c >> i) & 1 for i in range(4)]
        cb = ((1 + cD) & 1) | (1 << 1) | (cM << 2) | (cU << 3); sb = -(-1) ** cm
        ct = cm | (cD << 1) | (((1 + cU) & 1) << 2) | (1 << 3); stp = -(-1) ** cM
        fi = -(-1) ** (cm + cM)
        for n in range(3, nmax + 1):
            okb &= partes[n, c][0] == n * sb * A[n - 1, cb]
            okt &= partes[n, c][1] == n * stp * A[n - 1, ct]
        for n in range(1, nmax + 1):
            c0 = {0: 1, **{k: partes[k, c][2] for k in range(1, nmax + 1)}}
            oki &= A[n, c] == sum(math.comb(n, j) * fi ** j * c0[n - j] for j in range(n + 1))
    print(f'\n(V) regra geral para os 16 caracteres, n <= {nmax}: ponto embaixo {okb}; ponto em cima {okt}; pontos isolados {oki}')
    fixo = [c for c in range(16) if (((1 + ((c >> 1) & 1)) & 1) | 2 | (c & 12)) == c and ((c & 3) | (((1 + ((c >> 3) & 1)) & 1) << 2) | 8) == c]
    print('    caracteres fixos pelas duas operacoes de extremo:', ['(' + ','.join(str((c >> i) & 1) for i in range(4)) + ')' for c in fixo])

if __name__ == '__main__' and len(sys.argv) > 2 and sys.argv[2] == 'geral':
    regra_geral(sys.argv[1])
