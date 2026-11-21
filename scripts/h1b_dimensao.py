"""EXPLORATORIO (21/11/2026): as teias que dominam a soma com fases 'parecem' ter que dimensao?
Medida intrinseca: fracao de ordenacao r = (pares comparaveis)/C(n,2); dimensao de Myrheim-Meyer d_MM resolve
f(d) = r, f(d) = Gamma(d+1) Gamma(d/2) / (2 Gamma(3d/2))  (f(2) = 1/2, f(3) ~ 0.2286, f(4) = 0.1).
Acoes (Dowker-Glaser, arXiv:1305.2588), convencao N0 = elos:
  d = 4: B4 = n - N0 + 9 N1 - 16 N2 + 8 N3     d = 2: B2 = n - 2 N0 + 4 N1 - 2 N2
Media complexa de um observavel O: <O>_theta = sum w e^{i theta B} O / sum w e^{i theta B}, w = 1/|Aut|.
Uso: python h1b_dimensao.py PASTA"""
import sys, math, numpy as np
from scipy.special import gammaln
from scipy.optimize import brentq
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from h1b_modelo_rede import contagens

f = lambda d: math.exp(gammaln(d + 1) + gammaln(d / 2) - math.log(2) - gammaln(3 * d / 2))
def dMM(r):
    if r >= 1: return 1.0
    if r <= f(12): return 12.0
    return brentq(lambda d: f(d) - r, 1.0, 12.0)
CORTES = [f(1.5), f(2.5), f(3.5), f(4.5)]         # faixas de dimensao: <1,5 | 1,5-2,5 | 2,5-3,5 | 3,5-4,5 | >4,5
NOMES = ['d<1,5', '1,5-2,5', '2,5-3,5', '3,5-4,5', 'd>4,5']

def faixa(r): return np.digitize(-r, [-c for c in CORTES])

def main(pasta):
    th = np.linspace(0, np.pi, 721)
    print('Valores de referencia: f(2) = %.4f, f(3) = %.4f, f(4) = %.4f; cortes das faixas (r): %s' % (f(2), f(3), f(4), ', '.join(f'{c:.4f}' for c in CORTES)))
    for n in range(6, 11):
        d = np.load(f'{pasta}/h1b_N_n{n}.npz'); w = 1.0 / d['aut'].astype(float)
        P = d['pred'].astype(np.int64); N = contagens(P, n)
        pc = np.array([bin(x).count('1') for x in range(1 << n)]); r = pc[P].sum(1) / math.comb(n, 2)
        B = {4: n + N @ np.array([-1, 9, -16, 8]), 2: n + N @ np.array([-2, 4, -2, 0])}
        assert np.array_equal(B[4], d['B'])
        fx = faixa(r)
        for pop, m in (('todas as ordens', np.ones(len(w), bool)), ('oficial (altura >= 3)', d['h'] >= 3)):
            ww, rr, ff = w[m], r[m], fx[m]
            r0 = (ww * rr).sum() / ww.sum()
            print(f'\n[n={n}, {pop}] sem fases: <r>_0 = {r0:.3f} (d_MM {dMM(r0):.2f}); peso por faixa: '
                  + ', '.join(f'{NOMES[k]} {ww[ff == k].sum()/ww.sum():.3f}' for k in range(5)))
            for dd in (4, 2):
                b = B[dd][m]; v, inv = np.unique(b, return_inverse=True)
                Wb = np.bincount(inv, weights=ww); Rb = np.bincount(inv, weights=ww * rr)
                E = np.exp(1j * np.outer(th, v)); Z = E @ Wb; ZR = E @ Rb; rm = ZR / Z
                jan = th >= 2 * np.pi / 3
                # particao de Z(pi) por faixa de dimensao: participacao Re(Z_k conj Z)/|Z|^2
                part = []
                for k in range(5):
                    Wk = np.bincount(inv, weights=ww * (ff == k), minlength=len(v)); Zk = np.exp(1j * np.pi * v) @ Wk
                    part.append((Zk * np.conj(Z[-1])).real / abs(Z[-1]) ** 2)
                ini = th <= 0.5
                print(f'   acao d={dd}: Re<r> no centro (pi) = {rm[-1].real:+.3f} (Im {rm[-1].imag:+.3f}); '
                      f'na janela [2pi/3, pi]: Re<r> de {rm[jan].real.min():+.3f} a {rm[jan].real.max():+.3f}; '
                      f'|Z(pi)|/W = {abs(Z[-1])/ww.sum():.1e}')
                print(f'      participacao em Z(pi) por faixa: ' + ', '.join(f'{NOMES[k]} {part[k]:+.2f}' for k in range(5)))
                # theta em (0, pi] onde Re<r> fica mais perto do valor da dimensao da propria acao
                alvo = f(dd); ok = (th > 0.05)
                kbest = np.argmin(np.abs(rm[ok].real - alvo) + 10 * np.abs(rm[ok].imag)); tb = th[ok][kbest]
                print(f'      theta em que <r> fica mais perto de f({dd}) = {alvo:.3f} (com Im pequeno): theta = {tb:.3f}, <r> = {rm[ok][kbest].real:+.3f}{rm[ok][kbest].imag:+.3f}i')

if __name__ == '__main__':
    main(sys.argv[1])
