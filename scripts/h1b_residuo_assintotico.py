"""Exploratorio: de onde vem o crescimento de a_n (soma exata rotulada das ordens de altura <= 2).
a_n e^{-i theta n} = S_n = sum_a C(n,a) (y^a - 1)^(n-a), y = 1 + e^{-i theta}.
Observacao a testar: S_n ~ 2 * T_{k*}, com T_k = C(n,k)(y^k - 1)^(n-k) e k* = argmax_k |1 - y^k|
(o fator 2 viria da simetria de inversao da ordem: k* minimais <-> k* maximais).
Precisao: dps = 0.7 n + 40 (os termos chegam a ~4^n); conferencia: S_n(pi) deve dar (-1) e^{-i pi n} exatamente."""
import mpmath as mp
def S(n, th):
    mp.mp.dps = int(0.7 * n) + 40
    y = 1 + mp.exp(-1j * th)
    t = [mp.binomial(n, a) * (y ** a - 1) ** (n - a) for a in range(n + 1)]
    return mp.fsum(t), t, y
print('Conferencia em theta = pi (a_n = -1):', [mp.nstr(S(n, mp.pi)[0] * mp.exp(1j * mp.pi * n), 6) for n in (40, 160, 320, 640)])
for ths in ('2.114', '2.2', '2.3', '2.4', '2.5', '2.7', '2.9', '3.05'):
    for n in (40, 80, 160, 320, 640):
        ex, t, y = S(n, mp.mpf(ths))
        rho = [abs(1 - y ** k) for k in range(1, 40)]
        k = max(range(39), key=lambda i: rho[i]) + 1
        if n == 40:
            print(f'\ntheta {ths}: |y| = {mp.nstr(abs(y),4)}; k* = {k}; rho_k* = |1-y^k*| = {mp.nstr(rho[k-1],6)}; ln rho_k* = {mp.nstr(mp.log(rho[k-1]),5)}; segundo maior rho = {mp.nstr(sorted(rho)[-2],5)}')
        r = ex / (2 * t[k])
        print(f'  n={n:3d}: |S| {mp.nstr(abs(ex),5)}; (1/n)ln|S| {mp.nstr(mp.log(abs(ex))/n,5)}; S/(2 T_k*) = {mp.nstr(r.real,6)} {mp.nstr(r.imag,3):>10}i')
