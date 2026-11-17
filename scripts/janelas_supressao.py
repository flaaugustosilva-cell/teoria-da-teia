"""Soma exata de exp(iS) sobre teias de duas camadas (17/11/2026).
Camadas de m nos cada; acao de ligacoes S = mu*(n - L), L = numero de ligacoes.
Confere por forca bruta (m = 3: 512 teias) a formula |Z| = (2|cos(mu/2)|)^(m*m),
e lista as janelas de supressao em unidades de l_P = raiz(G hbar).
Uso: python janelas_supressao.py"""
import itertools, numpy as np
m = 3; M = m*m
for mu in (0.05, 1.0, 2.5, 3.5, 5.5):
    Z = sum(np.exp(1j*mu*(2*m - sum(b))) for b in itertools.product((0, 1), repeat=M))
    print(f'mu = {mu:4.2f}: |Z| forca bruta = {abs(Z):10.4f}   formula = {(2*abs(np.cos(mu/2)))**M:10.4f}   contagem pura = {2**M}')
c = np.sqrt(2/3); f = np.sqrt(8*np.pi)
print('\nJanelas com |cos(beta)| < 1/2, beta = raiz(2/3)*(l/l_p)^2, l_p^2 = 8 pi G hbar:')
for k in range(4):
    a, b = np.sqrt((np.pi/3 + k*np.pi)/c), np.sqrt((2*np.pi/3 + k*np.pi)/c)
    print(f'  janela {k+1}: l de {a*f:5.2f} a {b*f:5.2f} l_P    alfa de {0.5/(b*f)**2:.5f} a {0.5/(a*f)**2:.5f}')
for nome, l in (('entropia de horizonte', 0.832), ('alfa = 0,005', 10.0), ('alfa = 0,010', 7.07), ('alfa = 0,015', 5.77)):
    beta = c*(l/f)**2; print(f'  {nome:22s} l = {l:5.2f} l_P: 2|cos beta| = {2*abs(np.cos(beta)):.4f}  ({"suprimida" if 2*abs(np.cos(beta)) < 1 else "NAO suprimida"})')
