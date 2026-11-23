"""ANALITICO/EXPLORATORIO (23/11/2026): kappa ao trocar um ponto q_i de Q (estritamente prima) por um modulo de 2 elementos.
kappa(P) = s(P)(-1)^(D+U). Com os demais modulos sendo pontos, kappa(Q[..M_i..]) = kappa(Q) * rho_i(M_i), em que
  rho_i(M) = -w_c(M) (-1)^(alpha+gamma+eps),  w_c(M) = s(M)(-1)^(alpha m + beta D + gamma X + delta U),
e c_i = (alpha, beta, gamma, delta), eps dependem so da posicao de q_i em Q (deducao em ANALITICO_10.md):
  alpha = cob_abaixo + n2_abaixo + [exatamente 1 abaixo]     beta  = cob_abaixo + [q_i minimo]
  gamma = cob_acima + n2_acima + [exatamente 1 acima]        delta = cob_acima + [q_i maximo]
  eps   = (pares j < i < l com i unico no meio) + #{j: i e o unico abaixo de j} + #{j: i e o unico acima de j}
 cob_* = coberturas; n2_* = pontos j com exatamente um ponto entre j e i.
Anticadeia de 2 (1 rotulagem): rho = -(-1)^(alpha+gamma+eps). Cadeia de 2 (2 rotulagens): rho = (-1)^(beta+delta+eps) cada.
Uso: python h1b_modulo2.py PASTA"""
import sys, math, numpy as np
from collections import defaultdict
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_paridade_explora import estrutura
from h1b_soma_ordinal import perfis
from h1b_raiz_prima_modulos import blocos

def local(pq, k):
    rel = [[(pq[j] >> i) & 1 for j in range(k)] for i in range(k)]          # rel[i][j]: q_i < q_j
    ent = [[sum(rel[i][l] and rel[l][j] for l in range(k)) for j in range(k)] for i in range(k)]
    out = []
    for i in range(k):
        ab = [j for j in range(k) if rel[j][i]]; ac = [j for j in range(k) if rel[i][j]]
        cob_ab = sum(ent[j][i] == 0 for j in ab); cob_ac = sum(ent[i][j] == 0 for j in ac)
        n2_ab = sum(ent[j][i] == 1 for j in ab); n2_ac = sum(ent[i][j] == 1 for j in ac)
        a = cob_ab + n2_ab + (len(ab) == 1); b = cob_ab + (len(ab) == 0)
        g = cob_ac + n2_ac + (len(ac) == 1); dl = cob_ac + (len(ac) == 0)
        meio = sum(1 for j in ab for l in ac if ent[j][l] == 1)
        e = meio + sum(1 for j in range(k) if [x for x in range(k) if rel[x][j]] == [i]) \
                 + sum(1 for j in range(k) if [x for x in range(k) if rel[j][x]] == [i])
        out.append(dict(a=a % 2, b=b % 2, g=g % 2, d=dl % 2, e=e % 2, cob_ab=cob_ab, cob_ac=cob_ac, n2_ab=n2_ab, n2_ac=n2_ac,
                        mini=len(ab) == 0, maxi=len(ac) == 0, um_ab=len(ab) == 1, um_ac=len(ac) == 1))
    return out

def main(pasta, nmax=10):
    cl = {n: np.load(f'{pasta}/h1b_N_n{n}.npz') for n in range(4, nmax + 1)}
    print(' n | k | dado: anticadeia / cadeia | formula: anticadeia / cadeia | confere | kappa estritamente prima (k)')
    tabela = {}
    for n in range(5, nmax + 1):
        k = n - 1
        # quociente: ordens estritamente primas de tamanho k
        dq = cl[k]; E = estrutura(dq['pred'], k); m = E['tipo'] == 2
        Pq = dq['pred'][m].astype(np.int64); autq = dq['aut'][m].astype(np.int64)
        rq = blocos(Pq, k); estr = (rq == np.arange(k)[None, :]).all(1)
        Pq, autq = Pq[estr], autq[estr]; sq = np.where(dq['B'][m][estr] % 2 == 0, 1, -1)
        u, dd = perfis(Pq, k); kq = sq * (-1) ** ((dd[:, 1] + u[:, 1]) % 2)
        fa = fc = 0; tipo = defaultdict(lambda: [0, 0])
        for pq, aut, kv in zip(Pq, autq, kq):
            for L in local([int(x) for x in pq], k):
                ra = -(-1) ** (L['a'] + L['g'] + L['e']); rc = 2 * (-1) ** (L['b'] + L['d'] + L['e'])
                fa += kv * ra * math.factorial(n) // (2 * aut); fc += kv * rc * math.factorial(n) // (2 * aut)
                chave = (L['b'] + L['d'] + L['e']) % 2, (L['a'] + L['g'] + L['e']) % 2
                tipo[chave][0] += kv * math.factorial(n) // (2 * aut)
                tipo[chave][1] += 1
        # dado: classes de raiz prima em n com exatamente um modulo de 2 elementos e o resto pontos
        d = cl[n]; E = estrutura(d['pred'], n); m = E['tipo'] == 2
        P = d['pred'][m].astype(np.int64); L_ = math.factorial(n) // d['aut'][m].astype(np.int64); s = np.where(d['B'][m] % 2 == 0, 1, -1)
        u, dd = perfis(P, n); wk = L_ * s * (-1) ** ((dd[:, 1] + u[:, 1]) % 2)
        rot = blocos(P, n); tam = np.stack([(rot == j).sum(1) for j in range(n)], 1)
        sel = ((tam == 2).sum(1) == 1) & ((tam >= 3).sum(1) == 0)
        # qual o tipo do modulo: o par (x, y) do bloco de tamanho 2 e comparavel?
        bl = np.argmax(tam == 2, 1)
        cadeia = np.zeros(len(P), bool)
        for r in np.nonzero(sel)[0]:
            xs = np.nonzero(rot[r] == bl[r])[0]; x, y = xs[0], xs[1]
            cadeia[r] = bool(((P[r, y] >> x) & 1) or ((P[r, x] >> y) & 1))
        da, dc = int(wk[sel & ~cadeia].sum()), int(wk[sel & cadeia].sum())
        kstr = int(sum(kv * math.factorial(k) // aut for kv, aut in zip(kq, autq)))
        print(f' {n:2d} | {k} | {da:+d} / {dc:+d} | {fa:+d} / {fc:+d} | {(da, dc) == (fa, fc)} | {kstr:+d}', flush=True)
        tabela[n] = (tipo, kstr, fa, fc)
    print('\nPor tipo local da posicao, (paridade de beta+delta+eps, paridade de alpha+gamma+eps):')
    print('  (0,*): a cadeia NAO troca o sinal de kappa(Q); (1,*): troca.  (*,0): a anticadeia troca; (*,1): nao troca.')
    for n in range(5, nmax + 1):
        tipo, kstr, fa, fc = tabela[n]
        print(f'  n={n}: ' + '; '.join(f'{c}: soma kappa(Q) ponderada {v[0]:+d} ({v[1]} posicoes)' for c, v in sorted(tipo.items()))
              + f' | total (anticadeia+cadeia) {fa+fc:+d}; sinal vs (-1)^n: {"+" if (fa+fc)*(-1)**n > 0 else "-"}')

if __name__ == '__main__':
    main(sys.argv[1])
