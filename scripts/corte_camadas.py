"""Regra "cadeia x camadas" (17/11/2026): em cada regiao guarda-se M = K * N/H modos de cada sinal,
N/H = nos por camada (cadeias lado a lado), H = maior cadeia. K e calibrado UMA vez em 1+1 para
coincidir com a regra da cadeia (M = H), isto e K = H^2/N medido em 1+1, e usado sem ajuste em 2+1.
Em 1+1 esta regra e a da cadeia sao a mesma; em 2+1 a da cadeia guarda ~N^(1/3) e esta ~N^(2/3).
Uso: python corte_camadas.py"""
import numpy as np
from math import pi
from ssee import sorteia, green
from corte_cadeia import altura, mantem

def entropia(N, d, a, K, rng):
    p = sorteia(N, d, rng); A = green(p, d); A = A - A.T
    lam, V = np.linalg.eigh(1j*A)
    dentro = np.abs(p[:, 0]) + np.sqrt((p[:, 1:]**2).sum(1)) < a/2
    NU = int(dentro.sum()); HO, HU = altura(p, d), altura(p[dentro], d)
    MO = min(N//2, int(round(K*N/HO))); MU = min(NU//2, int(round(K*NU/HU)))
    k = mantem(lam, MO); pos = k[lam[k] > 0]
    W = (V[:, pos]*lam[pos]) @ V[:, pos].conj().T; Dk = (V[:, k]*lam[k]) @ V[:, k].conj().T
    Wu = W[np.ix_(dentro, dentro)]; Du = Dk[np.ix_(dentro, dentro)]
    l2, V2 = np.linalg.eigh(Du); k2 = mantem(l2, MU); k2 = k2[np.abs(l2[k2]) > 1e-9*np.abs(l2).max()]
    mu = np.linalg.eigvals((V2[:, k2].conj().T @ Wu @ V2[:, k2]) / l2[k2][:, None]).real
    mu = mu[np.abs(mu) > 1e-12]
    return float(np.sum(mu*np.log(np.abs(mu)))), MO, MU, NU, HO

if __name__ == '__main__':
    # calibracao de K em 1+1: K = H^2/N
    Ks = []
    for N in (500, 1000, 2000):
        for s in range(3):
            p = sorteia(N, 2, np.random.default_rng(900*N+s)); Ks.append(altura(p, 2)**2/N)
    K = float(np.mean(Ks)); print(f'K calibrado em 1+1 = {K:.2f}  (assintotico: 4)')
    print('--- 1+1 (deve repetir a regra da cadeia: inclinacao ~0,25) ---')
    Ns = (500, 1000, 2000); S = []
    for N in Ns:
        r = [entropia(N, 2, 0.5, K, np.random.default_rng(100*N+s)) for s in range(3)]
        S.append(np.mean([x[0] for x in r])); print(f' N = {N}: S = {S[-1]:.3f}  modos guardados O/U = {np.mean([x[1] for x in r]):.0f}/{np.mean([x[2] for x in r]):.0f}', flush=True)
    print(f' inclinacao contra ln N: {np.polyfit(np.log(Ns), S, 1)[0]:.3f}')
    print('--- 2+1 ---')
    a = 2**(-5/3); a3 = 0.218853; V = pi/12; Ns = (1000, 2000, 4000); S = []
    for N, reps in ((1000, 3), (2000, 3), (4000, 2)):
        r = [entropia(N, 3, a, K, np.random.default_rng(7*N+s)) for s in range(reps)]
        S.append(np.mean([x[0] for x in r])); mol = a3*(N/V)**(1/3)*pi*a
        print(f' N = {N}: S = {S[-1]:.3f}  modos O/U = {np.mean([x[1] for x in r]):.0f}/{np.mean([x[2] for x in r]):.0f} '
              f'(U tem {np.mean([x[3] for x in r]):.0f} nos)  nats por molecula = {S[-1]/mol:.3f}', flush=True)
    if min(S) > 0: print(f' S cresce como N^{np.polyfit(np.log(Ns), np.log(S), 1)[0]:.2f}  (lei de area: 0,33; volume: 1)')
