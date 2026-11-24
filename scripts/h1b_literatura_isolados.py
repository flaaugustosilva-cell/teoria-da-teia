"""Confere por forca bruta (ordens rotuladas, n <= 5) a identidade:
   F(theta) e^{i theta n} = soma sobre ordens de altura <= 2 de 2^{iso} e^{i theta B},
onde F = sum_a C(n,a) y^{a(n-a)} e o termo 'bipartido livre' (camada de baixo escolhida + qualquer conjunto de relacoes),
e a_n = soma das mesmas ordens com peso 1. Ou seja: a contagem bipartida livre so difere da exata por contar cada ponto
isolado duas vezes (ele pode ser posto em qualquer das camadas)."""
import itertools, cmath, math
def ordens(n):
    pares = [(i, j) for i in range(n) for j in range(n) if i != j]
    for m in range(1 << len(pares)):
        R = {pares[k] for k in range(len(pares)) if m >> k & 1}
        if any((j, i) in R for (i, j) in R): continue
        # altura <= 2: nenhum i<j<k; isso tambem garante transitividade (vacua)
        if any((j, k) in R for (i, j) in R for k in range(n)): continue
        yield R
for th in (math.pi, 2.5, 2.114):
    y = 1 + cmath.exp(-1j * th)
    for n in range(1, 6):
        ex = tw = 0
        for R in ordens(n):
            rel = {i for p in R for i in p}; iso = n - len(rel); B = n - len(R)
            ph = cmath.exp(1j * th * B); ex += ph; tw += 2 ** iso * ph
        F = sum(math.comb(n, a) * y ** (a * (n - a)) for a in range(n + 1)) * cmath.exp(1j * th * n)
        an = sum(math.comb(n, a) * (y ** a - 1) ** (n - a) for a in range(n + 1)) * cmath.exp(1j * th * n)
        print(f'theta {th:.3f} n={n}: exato {ex:.6f} formula a_n {an:.6f} | 2^iso {tw:.6f} formula F {F:.6f} | dif {abs(ex-an)+abs(tw-F):.1e}')
