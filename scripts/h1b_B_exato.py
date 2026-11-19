"""H1, segunda etapa, entrega B - phi_n exato (pre-registro PREREGISTRO.md + EMENDA_B.md, commit e91345e).
Enumera todas as ordens rotuladas naturalmente com n elementos, valida as contagens (OEIS), calcula B, altura e
e(P) (extensoes lineares), agrupa em classes nao rotuladas, certifica que cada classe de altura >= 3 cabe em 3+1
(coordenadas arredondadas e conferidas em fracoes) e grava tudo em h1b_B_n{n}.npz.
Uso (de dentro de scripts): python h1b_B_exato.py 5 6 7"""
import sys, time, itertools, math, numpy as np
from fractions import Fraction
from scipy.optimize import minimize

NATURAIS = {4: 40, 5: 357, 6: 4824, 7: 96428, 8: 2800472}        # A006455
CLASSES = {4: 16, 5: 63, 6: 318, 7: 2045, 8: 16999}             # A000112
ROTULADAS = {4: 219, 5: 4231, 6: 130023, 7: 6129859, 8: 431723379}  # A001035
DELTA = 0.05; EPS_T = 0.01; RECOMECOS = 200

def enumera(n):
    """Matriz (P, n) de mascaras de antecessores (fechadas transitivamente), ordem natural."""
    P = np.zeros((1, 1), np.int64)
    for k in range(1, n):
        S = np.arange(2**k)
        fechado = np.ones((len(P), 2**k), bool)
        for i in range(k):
            tem = ((S >> i) & 1).astype(bool)[None, :]
            fora = (P[:, i][:, None] & ~S[None, :]) != 0
            fechado &= ~(tem & fora)
        a, s = np.nonzero(fechado)
        P = np.column_stack([P[a], S[s]])
    return P

def relacoes(P, n):
    """C[p, i, j] = i antes de j."""
    return ((P[:, None, :] >> np.arange(n)[None, :, None]) & 1).astype(bool)

def invariantes(P, C, n):
    Cf = C.astype(np.float32); K = np.rint(Cf @ Cf).astype(np.int32)
    N = [np.sum(C & (K == m), axis=(1, 2)) for m in range(4)]
    B = n - N[0] + 9*N[1] - 16*N[2] + 8*N[3]
    L = np.ones((len(P), n), np.int32)
    for j in range(1, n):
        L[:, j] = 1 + np.max(np.where(C[:, :j, j], L[:, :j], 0), axis=1)
    return B, L.max(1)

def extensoes(P, n, lote=100_000):
    """Numero de extensoes lineares por DP sobre subconjuntos (vetorizado)."""
    out = np.empty(len(P), np.int64)
    for a in range(0, len(P), lote):
        Q = P[a:a+lote]; dp = np.zeros((len(Q), 2**n), np.int64); dp[:, 0] = 1
        for S in range(2**n):
            v = dp[:, S]
            if not v.any(): continue
            for k in range(n):
                if (S >> k) & 1: continue
                ok = (Q[:, k] & ~S) == 0
                dp[:, S | (1 << k)] += np.where(ok, v, 0)
        out[a:a+lote] = dp[:, -1]
    return out

def canonica(pred, n):
    """Forma canonica: refinamento de invariantes + permutacoes dentro dos empates; menor codigo."""
    suc = [0]*n
    for j in range(n):
        for i in range(n):
            if (pred[j] >> i) & 1: suc[i] |= 1 << j
    inv = [(bin(pred[i]).count('1'), bin(suc[i]).count('1')) for i in range(n)]
    for _ in range(3):
        inv = [(inv[i], tuple(sorted(inv[j] for j in range(n) if (pred[i] >> j) & 1)),
                tuple(sorted(inv[j] for j in range(n) if (suc[i] >> j) & 1))) for i in range(n)]
        mapa = {v: r for r, v in enumerate(sorted(set(inv)))}; inv = [mapa[v] for v in inv]
    grupos = [sorted(i for i in range(n) if inv[i] == r) for r in sorted(set(inv))]
    melhor = None
    for perms in itertools.product(*[itertools.permutations(g) for g in grupos]):
        ordem = [x for p in perms for x in p]; pos = {e: k for k, e in enumerate(ordem)}
        cod = tuple(sorted((pos[i], pos[j]) for j in range(n) for i in range(n) if (pred[j] >> i) & 1))
        cod = (tuple(sorted(inv)), cod)
        if melhor is None or cod < melhor: melhor = cod
    return melhor

def certifica(C, rng):
    """Procura coordenadas em 3+1; devolve as coordenadas certificadas em fracoes ou None."""
    n = C.shape[0]; I, J = np.triu_indices(n, 1)
    rel = C[I, J]; inv = C[J, I]   # inv nunca deve ocorrer em ordem natural
    if inv.any(): raise ValueError('rotulacao nao natural')
    def f(z):
        X = z.reshape(n, 4); D = X[J] - X[I]; dt = D[:, 0]; a = dt*dt - (D[:, 1:]**2).sum(1)
        r1 = np.where(rel, np.maximum(DELTA - a, 0), 0); r2 = np.where(rel, np.maximum(EPS_T - dt, 0), 0)
        r3 = np.where(~rel, np.maximum(DELTA + a, 0), 0)
        L = (r1**2).sum() + (r2**2).sum() + (r3**2).sum()
        da = -2*r1 + 2*r3; ddt = -2*r2
        gD = np.empty_like(D); gD[:, 0] = da*2*dt + ddt; gD[:, 1:] = -da[:, None]*2*D[:, 1:]
        G = np.zeros_like(X); np.add.at(G, J, gD); np.add.at(G, I, -gD)
        return L, G.ravel()
    for tent in range(RECOMECOS):
        X0 = np.column_stack([np.sort(rng.uniform(0, n, n)), rng.normal(0, 0.7*n/2, (n, 3))])
        r = minimize(f, X0.ravel(), jac=True, method='L-BFGS-B', options=dict(maxiter=2000))
        if r.fun > 1e-14: continue
        X = [[Fraction(round(float(v), 6)).limit_denominator(10**6) for v in linha] for linha in r.x.reshape(n, 4)]
        ok = True
        for i in range(n):
            for j in range(n):
                if i == j: continue
                dt = X[j][0] - X[i][0]; a = dt*dt - sum((X[j][k] - X[i][k])**2 for k in (1, 2, 3))
                if C[i, j] and not (dt > 0 and a > 0): ok = False
                if not C[i, j] and not C[j, i] and not (a < 0): ok = False
        if ok: return X, tent + 1
    return None, RECOMECOS

if __name__ == '__main__':
    for n in map(int, sys.argv[1:]):
        t0 = time.time(); P = enumera(n); C = relacoes(P, n)
        assert len(P) == NATURAIS[n], f'contagem de ordens naturais falhou: {len(P)} != {NATURAIS[n]}'
        B, h = invariantes(P, C, n); e = extensoes(P, n)
        val, cnt = np.unique(e, return_counts=True)
        soma = sum(int(c)*Fraction(math.factorial(n), int(v)) for v, c in zip(val, cnt))
        assert soma == ROTULADAS[n], f'identidade n!/e(P) falhou: {soma} != {ROTULADAS[n]}'
        t1 = time.time(); chaves = {}; classe = np.empty(len(P), np.int64)
        for p in range(len(P)):
            k = canonica([int(v) for v in P[p]], n); classe[p] = chaves.setdefault(k, len(chaves))
        assert len(chaves) == CLASSES[n], f'contagem de classes falhou: {len(chaves)} != {CLASSES[n]}'
        t2 = time.time(); rng = np.random.default_rng([20261123, 777, n])
        rep = {}; [rep.setdefault(c, p) for p, c in enumerate(classe)]
        cert = np.zeros(len(chaves), bool); tent = np.zeros(len(chaves), np.int64); coords = {}
        for c, p in rep.items():
            if h[p] < 3: continue
            X, t = certifica(C[p], rng); tent[c] = t
            if X is not None: cert[c] = True; coords[c] = X
        h3 = np.array([h[rep[c]] >= 3 for c in range(len(chaves))])
        t3 = time.time()
        np.savez_compressed(f'h1b_B_n{n}.npz', pred=P, B=B, h=h, e=e, classe=classe, certificada=cert, tentativas=tent,
                            coords=np.array([[float(v) for linha in coords[c] for v in linha] if c in coords else [np.nan]*(4*n) for c in range(len(chaves))]))
        print(f'n={n}: naturais {len(P)} (ok), rotuladas {soma} (ok), classes {len(chaves)} (ok); classes de altura >= 3: {h3.sum()}, '
              f'certificadas {cert.sum()}, nao certificadas {h3.sum() - cert.sum()}; tentativas medias {tent[h3].mean():.2f}, max {tent[h3].max()}; '
              f'tempos: enumeracao {t1-t0:.1f}s, classes {t2-t1:.1f}s, certificados {t3-t2:.1f}s', flush=True)
