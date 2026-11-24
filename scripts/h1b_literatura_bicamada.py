"""ANALITICO (24/11/2026): comparacao da janela da Teia com as condicoes de supressao da literatura (ordens de 2 camadas).
Convencao (igual a P. Carlip e S. Carlip, arXiv:2209.00327, Eq. 3.1): I/hbar = 2 sqrt(2/3) (l/l_p)^2 B = theta B,
logo o 'beta' da literatura e beta = theta/2. Janela da Teia: theta em [2pi/3, 4pi/3]  <=>  |cos beta| <= 1/2.
Formula exata (D, ANALITICO_1): soma ROTULADA de e^{i theta B} sobre ordens de altura <= 2:
   a_n(theta) = e^{i theta n} sum_a C(n,a) (y^a - 1)^(n-a),  y = 1 + e^{-i theta}.
Sem pontos isolados (cada ponto isolado multiplica por e^{i theta}):  b_n = sum_j C(n,j) (-e^{i theta})^j a_(n-j).
Compara |a_n|, |b_n| com o termo de sela de Loomis-Carlip, exp[(n^2/4) ln(2|cos beta|)], e com a contagem 2^(n^2/4).
Uso: python h1b_literatura_bicamada.py PASTA_N9N10"""
import sys, math, mpmath as mp, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
mp.mp.dps = 400

def a_n(n, th):
    y = 1 + mp.exp(-1j * th)
    return mp.exp(1j * th * n) * mp.fsum(mp.binomial(n, a) * (y ** a - 1) ** (n - a) for a in range(n + 1))

def b_n(n, th, cache):
    return mp.fsum(mp.binomial(n, j) * (-mp.exp(1j * th)) ** j * cache[n - j] for j in range(n + 1))

def main(pasta):
    print('Condicoes: Loomis-Carlip |cos beta| < 1/2  <=>  beta em (pi/3, 2pi/3) mod pi  <=>  theta em (2pi/3, 4pi/3) = janela da Teia (aberta).')
    lim = math.atan(math.sqrt(27 / 4 * math.exp(-0.5) - 1))
    print(f'P. e S. Carlip (2022), Eq. 3.3: tan beta > {math.sqrt(27/4*math.exp(-0.5)-1):.4f}  <=>  beta em ({lim:.4f}, pi/2) mod pi '
          f'<=>  theta em ({2*lim:.4f}, {math.pi:.4f}); janela da Teia: ({2*math.pi/3:.4f}, {4*math.pi/3:.4f})')
    # (V) conferir a_n e b_n contra os dados exatos n <= 10 em theta = pi e em um ponto da janela
    from h1b_paridade_explora import estrutura
    ok = True
    for th in (mp.pi, 2 * mp.pi / 3 + mp.mpf('0.3')):
        cache = {m: a_n(m, th) for m in range(11)}; cache[0] = mp.mpf(1)
        for n in range(1, 11):
            d = np.load(f'{pasta}/h1b_N_n{n}.npz'); L = math.factorial(n) // d['aut'].astype(np.int64)
            m = d['h'] <= 2; iso = estrutura(d['pred'], n)['iso'] > 0
            fase = np.exp(1j * float(th) * d['B'])
            ok &= abs(complex(cache[n]) - (L[m] * fase[m]).sum()) < 1e-6 * max(1, abs(complex(cache[n])))
            ok &= abs(complex(b_n(n, th, cache)) - (L[m & ~iso] * fase[m & ~iso]).sum()) < 1e-6 * max(1, abs(complex(b_n(n, th, cache))))
    print(f'(V) formulas de a_n e b_n conferem com os dados exatos, n = 1..10, theta = pi e theta = 2pi/3 + 0,3: {ok}')
    print('\n theta | n | |a_n| (altura <= 2) | |b_n| (sem isolados) | sela de Loomis-Carlip e^{(n^2/4)ln(2|cos beta|)} | 2^(n^2/4) (contagem) | log10(|b_n|/sela)')
    for th in (2 * mp.pi / 3 + mp.mpf('0.02'), mp.mpf('2.5'), mp.mpf('2.9'), mp.pi):
        cache = {0: mp.mpf(1)}
        for m in range(1, 81): cache[m] = a_n(m, th)
        for n in (10, 20, 40, 80):
            b = b_n(n, th, cache); cb = abs(mp.cos(th / 2))
            sela = mp.exp((n * n / 4) * mp.log(2 * cb)) if cb > 0 else mp.mpf(0)
            r = mp.log10(abs(b) / sela) if sela > 0 else mp.inf
            print(f' {float(th):.3f} | {n:2d} | {mp.nstr(abs(cache[n]), 5)} | {mp.nstr(abs(b), 5)} | {mp.nstr(sela, 5)} | {mp.nstr(mp.mpf(2) ** (n * n / 4), 5)} | {mp.nstr(r, 5)}')
    print('\n(D) Em theta = pi: a_n = -1 para todo n >= 1 e b_n = 2 - 2^n (exatos).')
    print('    conferencia: ' + ', '.join(f'n={n}: a {mp.nstr(mp.re(a_n(n, mp.pi)), 3)}, b {mp.nstr(mp.re(b_n(n, mp.pi, {m: (a_n(m, mp.pi) if m else mp.mpf(1)) for m in range(n + 1)})), 6)}' for n in (5, 12, 30)))

if __name__ == '__main__':
    main(sys.argv[1])

def onde(n=80):
    """Quais termos dominam a soma exata: a = numero de minimais (a = n: anticadeia; a perto de n: ordem esparsa)."""
    print(f'\nTermos da soma exata (n = {n}): a = numero de elementos minimais; a camada de cima tem n - a elementos.')
    for th in (mp.mpf('2.114'), mp.mpf('2.5'), mp.mpf('2.9')):
        y = 1 + mp.exp(-1j * th); T = [mp.binomial(n, a) * (y ** a - 1) ** (n - a) for a in range(n + 1)]
        tot = abs(mp.fsum(T)); amax = max(range(n + 1), key=lambda a: abs(T[a]))
        topo = sorted(range(n + 1), key=lambda a: -abs(T[a]))[:3]
        print(f'  theta {float(th):.3f}: |soma| {mp.nstr(tot, 4)}; maior termo em a = {amax} (cima com {n - amax} elementos), '
              f'|termo| {mp.nstr(abs(T[amax]), 4)}; tres maiores: a = {topo}; termos com a <= n/2: soma dos modulos {mp.nstr(mp.fsum(abs(T[a]) for a in range(n // 2 + 1)), 4)}')

if __name__ == '__main__' and len(sys.argv) > 2 and sys.argv[2] == 'onde':
    onde()

def separa(ns=(10, 20, 40, 80)):
    """(D) (y^a - 1)^(n-a) = sum_k C(n-a,k) (-1)^(n-a-k) y^(ak): o termo k = n-a (todo elemento de cima livre, grafo bipartido
    qualquer entre camadas fixas, como na contagem C(alpha n^2, .) de Loomis-Carlip) e o resto (inclusao-exclusao que exige
    um elemento abaixo para cada elemento de cima). Compara o termo bipartido em a = n/2 com a sela de Loomis-Carlip."""
    print('\nSeparacao exata: termo "bipartido livre" F = sum_a C(n,a) y^(a(n-a)) e resto = a_n e^{-i theta n} - F')
    for th in (mp.mpf('2.114'), mp.mpf('2.5'), mp.mpf('2.9')):
        y = 1 + mp.exp(-1j * th); beta = th / 2
        for n in ns:
            ex = mp.fsum(mp.binomial(n, a) * (y ** a - 1) ** (n - a) for a in range(n + 1))
            F = mp.fsum(mp.binomial(n, a) * y ** (a * (n - a)) for a in range(n + 1))
            meio = y ** ((n // 2) * (n - n // 2)); sela = mp.exp((n * n / 4) * (-1j * beta + mp.log(2 * mp.cos(beta))))
            print(f'  theta {float(th):.3f} n={n:2d}: |exato| {mp.nstr(abs(ex), 4)}; |F| {mp.nstr(abs(F), 4)}; |resto| {mp.nstr(abs(ex - F), 4)}; '
                  f'termo a=n/2 de F: {mp.nstr(meio, 4)}; sela LC exp[(n^2/4)(-i beta + ln(2 cos beta))]: {mp.nstr(sela, 4)}')

if __name__ == '__main__' and len(sys.argv) > 2 and sys.argv[2] == 'separa':
    separa()
