"""EXPLORATORIO (fora de registro), 20/11/2026: origem do desequilibrio de paridade no centro da janela.
Nivel ROTULADO: cada classe C vale L = n!/|Aut(C)| copias rotuladas, todas com o mesmo sinal s = (-1)^B.
Assim n! Z(pi) = T = sum_C L s e todas as somas sao inteiras e exatas.
Populacao OFICIAL: n = 5 a 10, altura >= 3 (todas cabem em 3+1). Le h1b_N_n{n}.npz (todas as ordens, para a formula
exponencial). Uso: python h1b_paridade_explora.py PASTA [n_max]"""
import sys, math, numpy as np
from collections import defaultdict
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_modelo_rede import contagens

def estrutura(pred, n):
    pred = pred.astype(np.int64); M = len(pred)
    pop = np.array([bin(x).count('1') for x in range(1 << n)], np.int64)
    suc = np.zeros((M, n), np.int64)
    for k in range(n):
        for i in range(n): suc[:, i] |= ((pred[:, k] >> i) & 1) << k
    adj = pred | suc
    R = adj | (np.int64(1) << np.arange(n))[None, :]
    for _ in range(int(math.ceil(math.log2(n))) + 1):          # fecho de alcance no grafo de comparabilidade
        Rn = R.copy()
        for j in range(n): Rn |= np.where(((R >> j) & 1).astype(bool), R[:, [j]], 0)
        R = Rn
    low = R & (-R)                                               # menor bit da componente
    comp = sum(((low[:, i] >> i) & 1) for i in range(n))
    full = (np.int64(1) << n) - 1; inc = (~adj) & full & ~(np.int64(1) << np.arange(n))[None, :]
    R2 = inc | (np.int64(1) << np.arange(n))[None, :]
    for _ in range(int(math.ceil(math.log2(n))) + 1):          # componentes do grafo de INcomparabilidade
        Rn = R2.copy()
        for j in range(n): Rn |= np.where(((R2 >> j) & 1).astype(bool), R2[:, [j]], 0)
        R2 = Rn
    serie = R2[:, 0] != full
    tipo = np.where(comp > 1, 0, np.where(serie, 1, 2))          # 0 paralelo, 1 serie (soma ordinal), 2 primo
    mini = (pred == 0).sum(1); maxi = (suc == 0).sum(1); iso = (adj == 0).sum(1)
    gi = np.zeros(M, bool); gc = np.zeros(M, bool)               # gemeos incomparaveis / comparaveis (cobertura)
    for i in range(n):
        for j in range(i + 1, n):
            gi |= (pred[:, i] == pred[:, j]) & (suc[:, i] == suc[:, j])
            bi, bj = np.int64(1) << i, np.int64(1) << j
            c1 = ((pred[:, j] >> i) & 1).astype(bool) & (pred[:, j] == pred[:, i] | bi) & (suc[:, i] == suc[:, j] | bj)
            c2 = ((pred[:, i] >> j) & 1).astype(bool) & (pred[:, i] == pred[:, j] | bj) & (suc[:, j] == suc[:, i] | bi)
            gc |= c1 | c2
    return dict(tipo=tipo, comp=comp, mini=mini, maxi=maxi, iso=iso, gi=gi, gc=gc, pred=pred, suc=suc, pop=pop)

def toggle_gemeos(E, L, s, n):
    """Para cada par {x,y} de gemeos incomparaveis (mesmo D = baixo, mesmo U = cima): tornar x < y.
    Mudanca em N0+N1 = 1 - #{d em D: exatamente 1 elemento entre d e x} - #{u em U: exatamente 1 entre x e u}.
    Nivel rotulado: cada (P, par nao ordenado) corresponde a DUAS ordens rotuladas (x<y ou y<x)."""
    pred, suc, pop = E['pred'], E['suc'], E['pop']; out = defaultdict(lambda: [0, 0])   # chave -> [peso, soma com sinal]
    for i in range(n):
        for j in range(i + 1, n):
            g = (pred[:, i] == pred[:, j]) & (suc[:, i] == suc[:, j])
            if not g.any(): continue
            a = np.zeros(len(pred), np.int64)
            for z in range(n):
                a += ((pred[:, i] >> z) & 1) * (pop[suc[:, z] & pred[:, i]] == 1)
                a += ((suc[:, i] >> z) & 1) * (pop[pred[:, z] & suc[:, i]] == 1)
            Dv = pred[:, i] == 0
            for vira in (0, 1):
                for minimo in (0, 1):
                    m = g & ((a % 2 == 0) == bool(vira)) & (Dv == bool(minimo))
                    out[(vira, minimo)][0] += int(L[m].sum()); out[(vira, minimo)][1] += int((L[m] * s[m]).sum())
    tot = sum(v[0] for v in out.values())
    print('  TOGGLE DE GEMEOS (pares incomparaveis -> x<y), contado por (ordem rotulada, par):')
    for (vira, minimo), (w, t) in sorted(out.items()):
        print(f'     {"troca" if vira else "mantem"} a paridade, par {"minimal" if minimo else "nao minimal"}: '
              f'{w/tot:.3f} dos pares; soma com sinal das ordens de partida {t:+d}')

def tabela(rot, chave, L, s, Ttot, Wtot):
    print(f'  por {rot}:  [valor: peso rotulado / soma com sinal T / vies T/peso / fracao de T]')
    for v in sorted(set(chave.tolist())):
        m = chave == v; Lv = int(L[m].sum()); Tv = int((L[m] * s[m]).sum())
        print(f'     {v}: {Lv:.4e} / {Tv:+d} / {Tv/Lv:+.2e} / {Tv/Ttot:+.3f}')

def main(pasta, nmax=10):
    ser = {}
    for n in range(1, nmax + 1):
        d = np.load(f'{pasta}/h1b_N_n{n}.npz'); f = math.factorial(n)
        L = f // d['aut'].astype(np.int64); s = np.where(d['B'] % 2 == 0, 1, -1).astype(np.int64)
        E = estrutura(d['pred'], n); con = E['comp'] == 1; boa = d['h'] >= 3
        ser[n] = dict(todas=int((L * s).sum()), conexas=int((L * s)[con].sum()), boas=int((L * s)[boa].sum()),
                      ruins=int((L * s)[~boa].sum()), boas_con=int((L * s)[boa & con].sum()), Wboa=int(L[boa].sum()))
        if n < 5: continue
        Lb, sb = L[boa], s[boa]; T = int((Lb * sb).sum()); W = int(Lb.sum())
        print(f'\n[OFICIAL] n={n}: peso rotulado das boas {W:.6e}; T = n! Z(pi) = {T:+d}; T/W = {T/W:+.3e}')
        for rot, k in (('tipo (0 paralelo, 1 serie, 2 primo)', E['tipo'][boa]), ('altura', d['h'][boa]), ('componentes', E['comp'][boa]), ('minimais', E['mini'][boa]),
                       ('isolados', E['iso'][boa]), ('|Aut|=1?', (d['aut'][boa] == 1).astype(int)),
                       ('tem gemeos incomparaveis', E['gi'][boa].astype(int)), ('tem gemeos comparaveis', E['gc'][boa].astype(int))):
            tabela(rot, k, Lb, sb, T, W)
        Eb = {k: (v[boa] if isinstance(v, np.ndarray) and v.ndim >= 1 and len(v) == len(L) else v) for k, v in E.items()}
        toggle_gemeos(Eb, Lb, sb, n)
        Ta = int((L * s).sum())
        print('  TODAS AS ORDENS por tipo: ' + '; '.join(f'{nm} {int((L*s)[E["tipo"]==t].sum()):+d}' for t, nm in ((0,'paralelo'),(1,'serie'),(2,'primo'))))
    print('\nSERIES (soma rotulada de (-1)^B, todas as somas exatas):')
    print(' n | todas as ordens | conexas | ruins (altura<=2) | boas | boas conexas')
    for n in ser:
        r = ser[n]; print(f' {n:2d} | {r["todas"]:+d} | {r["conexas"]:+d} | {r["ruins"]:+d} | {r["boas"]:+d} | {r["boas_con"]:+d}')
    # formula exponencial: A(x) = exp(C(x)) para os sinais (N0, N1 aditivos sobre componentes; B tem o termo n, tambem aditivo)
    a = [1] + [ser[n]['todas'] for n in range(1, nmax + 1)]; c = [0] + [ser[n]['conexas'] for n in range(1, nmax + 1)]
    ok = True
    for n in range(1, nmax + 1):                                   # a_n = sum_k C(n-1,k-1) c_k a_{n-k}
        prev = sum(math.comb(n - 1, k - 1) * c[k] * a[n - k] for k in range(1, n + 1))
        ok &= prev == a[n]
    print('formula exponencial (todas = exp(conexas)) confere exatamente:', ok)

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10)
