"""Consolidacao de E (E2) - geracao de dados (dados/h1b/PREREGISTRO_E2.md, commit 5a3427b).
Diamante 3+1, condicionado a altura >= 3, semente 20261124. Guarda N0..N3 e B de cada teia valida.
Uso (de dentro de scripts): python h1b_E2_dados.py 10 20 40 80 160  ->  h1b_E2_n{n}.npz (pula tamanhos ja gravados)"""
import sys, os, numpy as np
from h1_robustez import sorteia
SEMENTE = 20261124; D = 4
M = {10: 1_000_000, 20: 1_000_000, 40: 1_000_000, 80: 200_000, 160: 50_000}

def lote(b, n, rng):
    p = sorteia(b, n, D, rng)
    p = np.take_along_axis(p, np.argsort(p[..., 0], axis=1)[..., None], axis=1)
    dt = p[:, None, :, 0] - p[:, :, None, 0]; dr2 = ((p[:, None, :, 1:] - p[:, :, None, 1:])**2).sum(-1)
    C = (dt > 0) & (dt*dt > dr2)
    Cf = C.astype(np.float32); K = np.rint(Cf @ Cf).astype(np.int32)
    N = np.stack([np.sum(C & (K == m), axis=(1, 2)) for m in range(4)], 1)
    ok = np.any(C & (K > 0), axis=(1, 2))                      # altura >= 3
    return N[ok].astype(np.int32), int(np.sum(~ok))

if __name__ == '__main__':
    for n in map(int, sys.argv[1:]):
        if os.path.exists(f'h1b_E2_n{n}.npz'): print(f'n={n}: ja gravado', flush=True); continue
        rng = np.random.default_rng([SEMENTE, D, n]); tam = max(200, min(20_000, int(2e7 // n**2)))
        partes = []; desc = 0; feitos = 0
        while feitos < M[n]:
            b = min(tam, M[n] - feitos); N, k = lote(b, n, rng); partes.append(N); desc += k; feitos += b
        N = np.concatenate(partes); B = n - N[:, 0] + 9*N[:, 1] - 16*N[:, 2] + 8*N[:, 3]
        np.savez_compressed(f'h1b_E2_n{n}.npz', N=N, B=B, sorteios=M[n], descartadas=desc, lote=tam)
        print(f'n={n}: sorteios {M[n]}, validas {len(B)}, descartadas {desc}, desvio de B {B.std():.2f}', flush=True)
