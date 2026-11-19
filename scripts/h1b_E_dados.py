"""H1, segunda etapa, entrega E - geracao de dados (pre-registro dados/h1b/PREREGISTRO.md, commit 8b30242).
Diamante 3+1, semente 20261121. Para cada teia sorteada guarda: B (acao 4D de Benincasa-Dowker, eps = 1),
R (pares relacionados), h (altura = maior cadeia), minimais e maximais. Mantem so teias com altura >= 3.
Uso (de dentro de scripts): python h1b_E_dados.py 10 20 40 80     e     python h1b_E_dados.py 160
Saida: h1b_E_n{n}.npz"""
import sys, numpy as np
from h1_robustez import sorteia
SEMENTE = 20261121; D = 4
M = {10: 1_000_000, 20: 1_000_000, 40: 1_000_000, 80: 200_000, 160: 50_000}

def lote(b, n, rng):
    p = sorteia(b, n, D, rng)
    p = np.take_along_axis(p, np.argsort(p[..., 0], axis=1)[..., None], axis=1)   # ordem no tempo
    dt = p[:, None, :, 0] - p[:, :, None, 0]; dr2 = ((p[:, None, :, 1:] - p[:, :, None, 1:])**2).sum(-1)
    C = (dt > 0) & (dt*dt > dr2)
    Cf = C.astype(np.float32); K = np.rint(Cf @ Cf).astype(np.int32)
    N = [np.sum(C & (K == m), axis=(1, 2)) for m in range(4)]
    B = n - N[0] + 9*N[1] - 16*N[2] + 8*N[3]
    L = np.ones((b, n), np.int32)
    for j in range(1, n):
        L[:, j] = 1 + np.max(np.where(C[:, :j, j], L[:, :j], 0), axis=1)
    h = L.max(1); R = C.sum((1, 2))
    mmin = (~C.any(1)).sum(1); mmax = (~C.any(2)).sum(1)
    ok = h >= 3
    return [a[ok].astype(np.int32) for a in (B, R, h, mmin, mmax)], int(np.sum(~ok))

if __name__ == '__main__':
    for n in map(int, sys.argv[1:]):
        rng = np.random.default_rng([SEMENTE, D, n]); tam = max(200, min(20_000, int(2e7 // n**2)))
        partes = []; desc = 0; feitos = 0
        while feitos < M[n]:
            b = min(tam, M[n] - feitos); r, k = lote(b, n, rng); partes.append(r); desc += k; feitos += b
        B, R, h, mmin, mmax = (np.concatenate([q[i] for q in partes]) for i in range(5))
        np.savez_compressed(f'h1b_E_n{n}.npz', B=B, R=R, h=h, mmin=mmin, mmax=mmax, sorteios=M[n], descartadas=desc, lote=tam)
        print(f'n={n}: sorteios {M[n]}, validas {len(B)}, descartadas (altura<=2) {desc}, B media {B.mean():.2f} desvio {B.std():.2f}', flush=True)
