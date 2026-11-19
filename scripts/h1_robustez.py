"""Teste numerico de H1 (pre-registrado em 19/11/2026, ~13:45). Nao mudar parametros.
Mede a distribuicao de B (acao 4D de Benincasa-Dowker, eps = 1) em teias sorteadas em diamantes
de 1+1, 2+1 e 3+1, com n fixo. Guarda o histograma de B (e a soma dos pesos 1/|Aut| por valor de B),
de onde Gamma = |media de exp(i theta B)| sai exata para qualquer x.
Uso (de dentro de scripts): python h1_robustez.py d semente [peso]
   ex.: python h1_robustez.py 4 20261120 peso ; python h1_robustez.py 4 7777 ; python h1_robustez.py 2 20261120
Saida: h1_hist_d{d}_s{semente}.npz"""
import sys, numpy as np
NS = (6, 8, 10, 12, 14, 16, 20, 24, 28, 32); M = 1_000_000; LOTE = 20_000

def sorteia(b, n, d, rng):
    """b teias de n pontos uniformes no diamante |t| + r <= 1 com d - 1 dimensoes espaciais."""
    acc = {2: 0.5, 3: 0.26, 4: 0.13}[d]; cap = int(np.ceil(1.6*n/acc)) + 40
    while True:
        p = rng.uniform(-1, 1, (b, cap, d))
        ok = np.abs(p[..., 0]) + np.sqrt((p[..., 1:]**2).sum(-1)) <= 1
        if np.all(ok.sum(1) >= n): break
        cap *= 2                                   # raro: aumenta e sorteia o lote de novo
    idx = np.argsort(~ok, axis=1, kind='stable')[:, :n]
    return np.take_along_axis(p, idx[..., None], axis=1)

def lote(b, n, d, rng, peso):
    p = sorteia(b, n, d, rng)
    dt = p[:, None, :, 0] - p[:, :, None, 0]; dr2 = ((p[:, None, :, 1:] - p[:, :, None, 1:])**2).sum(-1)
    C = (dt > 0) & (dt*dt > dr2)
    Cf = C.astype(np.float32); K = np.rint(Cf @ Cf).astype(np.int32)
    N = [np.sum(C & (K == m), axis=(1, 2)) for m in range(4)]
    B = n - N[0] + 9*N[1] - 16*N[2] + 8*N[3]
    alt3 = np.any(C & (K > 0), axis=(1, 2))
    lnaut = np.zeros(b)
    if peso:   # cota inferior de ln|Aut|: classes de elementos com mesmo passado e mesmo futuro
        r1 = rng.random(n); r2 = rng.random(n)
        h = np.round(Cf.astype(np.float64) @ r1 + np.swapaxes(Cf, 1, 2).astype(np.float64) @ r2, 9)
        h.sort(axis=1); ini = np.ones_like(h, bool); ini[:, 1:] = h[:, 1:] != h[:, :-1]
        ar = np.broadcast_to(np.arange(n), h.shape); ult = np.maximum.accumulate(np.where(ini, ar, 0), axis=1)
        lnaut = np.log(ar - ult + 1).sum(1)
    return B[alt3], lnaut[alt3], int(np.sum(~alt3))

if __name__ == '__main__':
    d = int(sys.argv[1]); sem = int(sys.argv[2]); peso = len(sys.argv) > 3 and sys.argv[3] == 'peso'
    saida = {}
    for n in NS:
        rng = np.random.default_rng([sem, d, n]); Bs = []; La = []; desc = 0
        for _ in range(M // LOTE):
            B, la, k = lote(LOTE, n, d, rng, peso); Bs.append(B); La.append(la); desc += k
        B = np.concatenate(Bs); la = np.concatenate(La)
        vals, inv = np.unique(B, return_inverse=True)
        saida[f'n{n}_B'] = vals; saida[f'n{n}_cont'] = np.bincount(inv)
        if peso:
            saida[f'n{n}_peso'] = np.bincount(inv, weights=np.exp(-la)); saida[f'n{n}_peso2'] = np.bincount(inv, weights=np.exp(-2*la))
            saida[f'n{n}_lnaut_media'] = la.mean()
        saida[f'n{n}_descartadas'] = desc
        print(f'd={d} s={sem} n={n:2d}: validas {len(B)}, descartadas (altura<=2) {desc}, B media {B.mean():.2f} desvio {B.std():.2f}'
              + (f', ln|Aut| medio {la.mean():.2f}' if peso else ''), flush=True)
    np.savez_compressed(f'h1_hist_d{d}_s{sem}.npz', **saida)
