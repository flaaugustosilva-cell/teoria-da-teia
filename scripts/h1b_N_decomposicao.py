"""EXPLORATORIO (fora de registro), 20/11/2026: decomposicao de Z_boa por altura e por numero de minimais,
n = 5 a 10, na janela theta = 2 beta em [2pi/3, 4pi/3] (4001 pontos). Pergunta: alguma subclasse domina a soma?
Le h1b_N_n{n}.npz (dados/h1b/n9n10 para n = 9, 10; para n = 5 a 8, gerar com h1b_N_classes.py a partir do genposetg).
Uso: python h1b_N_decomposicao.py  ->  relatorio na tela."""
import numpy as np
TH = np.linspace(2*np.pi/3, 4*np.pi/3, 4001)
for n in range(5, 11):
    d = np.load(f'h1b_N_n{n}.npz'); B = d['B'].astype(float); h = d['h']; w = 1.0/d['aut'].astype(float); P = d['pred']
    m = (P == 0).sum(1); boa = h >= 3
    def Z(mask):
        v, inv = np.unique(B[mask], return_inverse=True); W = np.bincount(inv, weights=w[mask]); return np.exp(1j*np.outer(TH, v)) @ W
    Zb = Z(boa); k = int(np.argmin(np.abs(Zb)))
    print(f'\nn={n}: W_boa = {w[boa].sum():.1f}; min |Z_boa| = {abs(Zb[k]):.4f} em theta = {TH[k]:.4f}; mediana de |Z_boa| na janela = {np.median(np.abs(Zb)):.2f}')
    for nome, chave in (('altura', h), ('minimais', m)):
        partes = {v: Z(boa & (chave == v)) for v in sorted(set(chave[boa]))}
        soma_mod = sum(np.abs(z) for z in partes.values()); sobra = np.abs(Zb)/soma_mod
        dom = {v: float(np.median(np.abs(z)/soma_mod)) for v, z in partes.items()}
        print(f'  por {nome}: |Z_boa| / soma dos modulos das partes = mediana {np.median(sobra):.3f}, minimo {sobra.min():.4f}')
        print('    fracao mediana de cada parte: ' + ', '.join(f'{v}: {f:.2f}' for v, f in dom.items() if f > 0.01)
              + ' | no ponto de minimo: ' + ', '.join(f'{v}: {abs(z[k]):.3g}' for v, z in partes.items() if abs(z[k]) > 1e-3*abs(Zb[k]) + 1e-12))
