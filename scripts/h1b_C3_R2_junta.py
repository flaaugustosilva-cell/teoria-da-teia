"""Rota R2 do PREREGISTRO_C3.md: valida cada parte contra a parte auxiliar publicada e, com as 20, compara Prim_11 com R1.
Uso: python h1b_C3_R2_junta.py PASTA_R2 PASTA_N11AUX"""
import sys, os, numpy as np

R1 = -77098086120
if __name__ == '__main__':
    pr2, paux = sys.argv[1], sys.argv[2]
    tot = {0: 0, 1: 0, 2: 0}; feitas = 0; ok = True; classes = 0
    for x in range(20):
        f = f'{pr2}/h1b_C3_R2_n11_parte{x}.npz'
        if not os.path.exists(f): continue
        d = np.load(f); s = [int(v) for v in d['soma']]
        a = np.load(f'{paux}/h1b_N11_n11_parte{x}.npz')
        Taux = sum(int(p) * (1 if b % 2 == 0 else -1) for (b, h3, c), p in zip(a['chaves'], a['peso']))
        bate = (sum(s) == Taux) and (int(d['total_classes']) == int(a['total_classes']))
        ok &= bate; feitas += 1; classes += int(d['total_classes'])
        for k in (0, 1, 2): tot[k] += s[k]
        print(f'parte {x}: classes {int(d["total_classes"])}, soma com sinal {sum(s):+d} vs auxiliar {Taux:+d} -> {"confere" if bate else "DIFERE"}')
    print(f'{feitas}/20 partes; todas conferem com as partes auxiliares: {ok}')
    if feitas == 20:
        print(f'classes = {classes} (A000112(11) = 46749427)')
        print(f'R2: paralelo {tot[0]:+d}; serie {tot[1]:+d}; raiz prima {tot[2]:+d}')
        print(f'R1: raiz prima {R1:+d} -> R1 e R2 {"CONCORDAM" if tot[2] == R1 else "DISCORDAM"}')
        print(f'R2 tambem confere as partes paralela e serie da recursao (R1): {tot[0] == 34819420745 and tot[1] == 1787428412}')
