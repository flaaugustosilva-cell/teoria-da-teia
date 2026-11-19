"""Validacao pre-registrada do E1 (antes da rodada principal)."""
import itertools, numpy as np, mpmath as mp
from e1_comum import contagens, B_de, beta_de, lnZ_ruim

# (i) forca bruta: todas as ordens rotuladas de altura <= 2 (sem cadeia de 3), n = 4 e 5
for n in (4, 5):
    pares = [(i, j) for i in range(n) for j in range(n) if i != j]
    for x in (5.0, 7.0, 9.0):
        mu = 2*beta_de(x); Z = 0j; cont = 0
        for bits in itertools.product((0, 1), repeat=len(pares)):
            R = np.zeros((n, n), bool)
            for b, (i, j) in zip(bits, pares):
                if b: R[i, j] = True
            if np.any(R & R.T): continue                                    # antissimetria
            if np.any((R.astype(int) @ R.astype(int)) > 0): continue         # sem cadeia de 3
            cont += 1; L = int(R.sum()); Z += np.exp(1j*mu*(n - L))
        print(f'(i) n={n} x={x}: ordens = {cont}, ln|Z| forca bruta = {np.log(abs(Z)):.10f}, formula = {lnZ_ruim(n, x):.10f}')

# (ii) acao implementada em teias de duas camadas: B = n - L
rng = np.random.default_rng(1)
for _ in range(5):
    a, b = 7, 9; n = a + b; C = np.zeros((n, n), bool)
    C[:a, a:] = rng.random((a, b)) < 0.5
    N, h3 = contagens(C)
    print(f'(ii) B = {B_de(n, N)}, n - L = {n - C.sum()}, altura>=3: {h3}')

# (iii) cadeia de 5
n = 5; C = np.triu(np.ones((n, n), bool), 1); N, h3 = contagens(C)
print(f'(iii) cadeia de 5: N0..N3 = {N}, B = {B_de(n, N)} (esperado [4,3,2,1] e 4), altura>=3: {h3}')
