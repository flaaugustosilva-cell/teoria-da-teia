"""H1, segunda etapa, entrega B - sorteio de comparacao (EMENDA_B.md): diamante 3+1, semente 20261123,
10^7 sorteios por n, condicionado a altura >= 3. Guarda B de cada teia valida, na ordem do sorteio.
Uso (de dentro de scripts): python h1b_B_sorteio.py 5 6 7 8   ->  h1b_B_sorteio_n{n}.npz"""
import sys, numpy as np
from h1_robustez import lote
M = 10_000_000; LOTE = 20_000; SEMENTE = 20261123
for n in map(int, sys.argv[1:]):
    rng = np.random.default_rng([SEMENTE, 4, n]); Bs = []; desc = 0
    for _ in range(M // LOTE):
        B, _, k = lote(LOTE, n, 4, rng, False); Bs.append(B.astype(np.int16)); desc += k
    B = np.concatenate(Bs)
    np.savez_compressed(f'h1b_B_sorteio_n{n}.npz', B=B, sorteios=M, descartadas=desc)
    print(f'n={n}: sorteios {M}, validas {len(B)}, descartadas (altura<=2) {desc}', flush=True)
