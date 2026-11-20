"""EXPLORATORIO (fora de registro), 20/11/2026: estrutura fina de W_b (paridade, vizinhanca, Fourier).
Linha OFICIAL: n = 5 a 10 (altura >= 3; para n <= 10 todas cabem em 3+1, certificado). Le h1b_N_n{n}.npz.
Linha AUXILIAR: n = 11, todas as ordens de altura >= 3 ("nao ruins"). Le h1b_N11_n11_parte{x}.npz.
As duas linhas sao reportadas separadas; a regra de selecao de cada uma vem indicada.
Uso: python h1b_estrutura_fina.py PASTA_N9N10 PASTA_N11  ->  relatorio na tela."""
import sys, math, numpy as np
from collections import defaultdict

def espectro_oficial(pasta, n):
    d = np.load(f'{pasta}/h1b_N_n{n}.npz'); boa = d['h'] >= 3; P = d['pred'][boa]
    v, inv = np.unique(d['B'][boa], return_inverse=True); w = 1.0/d['aut'][boa].astype(float)
    W = np.bincount(inv, weights=w)
    con = np.zeros(len(P), bool)                         # conexidade do grafo de comparabilidade
    for k, p in enumerate(P):
        adj = [0]*n
        for j in range(n):
            m = int(p[j])
            for i in range(n):
                if (m >> i) & 1: adj[i] |= 1 << j; adj[j] |= 1 << i
        vis = 1; fr = 1
        while fr:
            nv = 0
            for i in range(n):
                if (fr >> i) & 1: nv |= adj[i]
            fr = nv & ~vis; vis |= nv
        con[k] = vis == (1 << n) - 1
    Wc = np.bincount(inv, weights=w*con, minlength=len(v)); return v, W, Wc

def espectro_aux(pasta, n=11):
    Wd = defaultdict(int); Wcd = defaultdict(int); fat = math.factorial(n)
    for x in range(20):
        d = np.load(f'{pasta}/h1b_N11_n{n}_parte{x}.npz')
        for (b, h3, c), p in zip(d['chaves'], d['peso']):
            if h3: Wd[int(b)] += int(p); Wcd[int(b)] += int(p) if c else 0
    v = np.array(sorted(Wd)); return v, np.array([Wd[b] for b in v], float)/fat, np.array([Wcd[b] for b in v], float)/fat

def analisa(n, v, W, Wc, rotulo):
    Wt = W.sum(); p = W/Wt; mu = (p*v).sum(); sd = math.sqrt((p*(v - mu)**2).sum())
    b0, b1 = int(v.min()), int(v.max()); bb = np.arange(b0 - 60, b1 + 61); Wf = np.zeros(len(bb)); Wf[v - b0 + 60] = W
    # envelope: suavizacao gaussiana de largura sd/4 (fixada antes de olhar os residuos)
    s = sd/4; ker = np.exp(-0.5*(np.arange(-60, 61)/s)**2); ker /= ker.sum()
    G = np.convolve(Wf, ker, mode='same'); r = Wf - G
    ac = [float(np.sum(r[:-k]*r[k:])/np.sum(r*r)) for k in (1, 2, 3, 4)]
    th = np.linspace(0, np.pi, 3601)
    Z = np.abs(np.exp(1j*np.outer(th, bb)) @ Wf); Zg = np.abs(np.exp(1j*np.outer(th, bb)) @ G); Zr = np.abs(np.exp(1j*np.outer(th, bb)) @ r)
    jan = th >= 2*np.pi/3; kpk = int(np.argmax(Zr*(th > 0.5)))
    D = W[v % 2 == 0].sum() - W[v % 2 == 1].sum(); Dc = Wc[v % 2 == 0].sum() - Wc[v % 2 == 1].sum()
    print(f'\n[{rotulo}] n={n}: W = {Wt:.6g}, desvio de B = {sd:.2f}')
    print(f'  PARIDADE: W_par - W_impar = {D:+.6g} ({D/Wt:+.2e} de W); so conexas: {Dc:+.6g}; desconexas: {D-Dc:+.6g}')
    print(f'  VIZINHANCA: residuo r = W - G (envelope de largura desvio/4): soma|r|/W = {np.abs(r).sum()/Wt:.3f}; '
          f'autocorrelacao de r nos passos 1..4 = ' + ', '.join(f'{a:+.2f}' for a in ac))
    print(f'  FOURIER (|.|/W): theta = ' + '  '.join(f'{t:.2f}: Z {Z[i]/Wt:.1e} | G {Zg[i]/Wt:.1e} | r {Zr[i]/Wt:.1e}'
                                                  for t, i in ((0.5, 573), (1.0, 1146), (2.094, 2400), (2.618, 3000), (3.1416, 3600))))
    print(f'  na janela: max |Z_G|/|Z| = {np.max(Zg[jan]/Z[jan]):.1e} (envelope desprezivel); pico de |r^| fora de theta < 0,5 em theta = {th[kpk]:.3f}')

if __name__ == '__main__':
    p910, p11 = sys.argv[1], sys.argv[2]
    for n in range(5, 11): analisa(n, *espectro_oficial(p910, n), 'OFICIAL: altura >= 3, todas cabem em 3+1')
    analisa(11, *espectro_aux(p11), 'AUXILIAR: altura >= 3, todas as ordens (nao e a definicao oficial)')
