"""Confere as pecas da prova do Teorema 2 (conjectura C-R) em valores NOVOS de theta.
(1) Formula dupla: S_n = sum_{b,t>=0, b+t<=n} n!/(b! t! r!) (-1)^r y^(bt), r = n-b-t.
(2) Linha b fixa somada em t = T_b; coluna t fixa somada em b = T_t (simetria).
(3) Decomposicao exata: S_n = 2 sum_{k<=K} T_k - D_K + R_K, D_K = bloco b,t<=K, R_K = bloco b,t>K.
(4) Cota: |R_K| <= (1 + 2 |y|^((K+1)/2))^n.
(5) Razao S_n / (2 T_k*)."""
import mpmath as mp
def calc(n, th, K):
    mp.mp.dps = int(0.8 * n) + 50
    y = 1 + mp.exp(-1j * th)
    T = [mp.binomial(n, k) * (y ** k - 1) ** (n - k) for k in range(n + 1)]
    S = mp.fsum(T)
    f = mp.factorial
    M = lambda b, t: f(n) / (f(b) * f(t) * f(n - b - t)) * (-1) ** (n - b - t) * y ** (b * t)
    dupla = D = R = 0
    for b in range(n + 1):
        for t in range(n - b + 1):
            m = M(b, t); dupla += m
            if b <= K and t <= K: D += m
            if b > K and t > K: R += m
    linha2 = mp.fsum(M(2, t) for t in range(n - 1))
    dec = 2 * mp.fsum(T[:K + 1]) - D + R
    return y, T, S, dupla, linha2, D, R, dec
for ths in ('2.25', '2.6', '2.8', '3.3', '3.9'):
    th = mp.mpf(ths)
    y = 1 + mp.exp(-1j * th); rho = [abs(1 - y ** k) for k in range(0, 60)]
    ks = max(range(1, 60), key=lambda k: rho[k]); rs = rho[ks]
    K = next(K for K in range(ks, 200) if 1 + 2 * abs(y) ** ((K + 1) / 2) < rs)
    print(f'\ntheta {ths}: |y| {mp.nstr(abs(y),5)}; k* {ks}; rho* {mp.nstr(rs,6)}; 2o maior {mp.nstr(sorted(rho)[-2],6)}; K = {K}; base da cota {mp.nstr(1+2*abs(y)**((K+1)/2),6)}')
    for n in (30, 60, 120, 240):
        y, T, S, dupla, l2, D, R, dec = calc(n, th, K)
        e1 = abs(dupla - S) / abs(S); e2 = abs(l2 - T[2]) / abs(T[2]); e3 = abs(dec - S) / abs(S)
        cota = (1 + 2 * abs(y) ** ((K + 1) / 2)) ** n
        r = S / (2 * T[ks])
        print(f'  n={n:3d}: (1) {mp.nstr(e1,2)} (2) {mp.nstr(e2,2)} (3) {mp.nstr(e3,2)} | (4) |R_K| {mp.nstr(abs(R),4)} <= {mp.nstr(cota,4)}: {abs(R) <= cota} | |D_K| {mp.nstr(abs(D),4)} | (5) S/(2T_k*) = {mp.nstr(r.real,8)} {mp.nstr(r.imag,3)}i')
