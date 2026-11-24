"""EXPLORATORIO (24/11/2026): o excesso de coerencia da faixa ~3D vem das ordens de altura <= 2?
Identidade (D): R = N0+N1+N2+N3+R4 (pares comparaveis)  =>  B = n - R + X,  X = 10 N1 - 15 N2 + 9 N3 + R4.
altura <= 2  <=>  N1 = N2 = N3 = R4 = 0  =>  X = 0 (a reciproca falha: X = 0 tambem por coincidencia aritmetica).
Para a faixa 2,5-3,5 (e as outras), separa altura <= 2 e altura >= 3: peso, coerencia, piso analitico, razao.
Uso: python h1b_mecanismo_altura.py PASTA_N9N10 PASTA_D11 n [n ...]"""
import sys, math, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_dimensao import faixa, NOMES
from h1b_decoerencia import TH_JANELA as TH
from h1b_mecanismo_coerencia import carrega, rice_mediana

def main(p910, p11, ns):
    for n in ns:
        B, L, R, h, N = carrega(n, p910, p11); C2 = math.comb(n, 2); Lf = L.astype(float)
        Ni = N.astype(np.int64); X = 10 * Ni[:, 1] - 15 * Ni[:, 2] + 9 * Ni[:, 3] + (R - Ni.sum(1))
        assert np.array_equal(B, n - R + X), 'identidade B = n - R + X falhou'
        so_cob = (Ni[:, 1:].sum(1) == 0) & (R == Ni[:, 0])
        assert np.array_equal(so_cob, h <= 2), "altura <= 2 <=> N1=N2=N3=R4=0 falhou"
        assert np.all(X[h <= 2] == 0)
        fx0 = Lf[(X == 0) & (h >= 3)].sum() / Lf[X == 0].sum()
        b0 = int(B.min()); nb = int(B.max()) - b0 + 1; E = np.exp(1j * np.outer(TH, np.arange(nb) + b0))
        hpop = np.bincount(B - b0, weights=Lf, minlength=nb); Zpop = E @ hpop; W = hpop.sum(); S2 = (Lf ** 2).sum()
        rng = np.random.default_rng(0); g = faixa(R / C2)
        print(f'\n== n = {n}: identidade B = n - R + X confere; altura <= 2 <=> N1=N2=N3=R4=0 confere (=> X = 0); peso de X = 0 que vem de altura >= 3: {fx0:.3f} ==')
        for k in (0, 1, 2):
            linha = []
            for rot, m in (('toda a faixa', g == k), ('altura <= 2', (g == k) & (h <= 2)), ('altura >= 3', (g == k) & (h >= 3))):
                if not m.any(): linha.append(f'{rot}: vazio'); continue
                hk = np.bincount(B[m] - b0, weights=Lf[m], minlength=nb); q = hk.sum() / W
                c = float(np.median(np.abs(E @ hk))) / hk.sum()
                piso = float(np.median(rice_mediana(q * np.abs(Zpop), q * (1 - q) * S2, rng))) / (q * W)
                linha.append(f'{rot}: peso {q:.4f}, coerencia {c:.3e}, razao {c/piso:.2f}')
            print(f'  {NOMES[k]:8s}| ' + ' | '.join(linha), flush=True)
        print('  Concentracao de X dentro de cada fatia R (peso no valor modal; numero de valores com 90% do peso; desvio de X):')
        for r in range(C2 + 1):
            m = R == r
            if Lf[m].sum() / W < 2e-3: continue
            x0 = X[m].min(); hx = np.bincount(X[m] - x0, weights=Lf[m]); hx /= hx.sum(); sv = np.sort(hx)[::-1]
            k90 = int(np.searchsorted(np.cumsum(sv), 0.9)) + 1; ar = np.arange(len(hx)); mx = (hx * ar).sum()
            print(f'     R={r:2d} ({NOMES[g[m][0]]}): modal {sv[0]:.3f} (X = {x0 + int(hx.argmax()):+d}); {k90:3d} valores; desvio {math.sqrt((hx * ar ** 2).sum() - mx ** 2):5.1f}', flush=True)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], [int(x) for x in sys.argv[3:]])
