"""Teste do codigo recebido em 17/11/2026 (soma de historias no diagrama de ligacoes do diamante 1+1).
Mesma regra: psi(no) = soma sobre ligacoes (pred -> no) de psi(pred) * exp(i * m * tau). Origem (0,0), topo (2,0).
Afirmacao a testar: o numero de picos de |psi|^2 no "equador" (|t - 1| < 0,1) vem da topologia e cresce
com a teia, sem parametro ajustado. Se vier do parametro m, cresce com m e nao com N.
Medida de picos sem limiar livre: numero de trocas de sinal de Re(psi) ao longo de x (cada oscilacao = 2 trocas),
em 30 faixas de x. Referencia do continuo: zeros de J0(m * raiz(1 - x^2)) em -1 < x < 1.
Uso: python picos_feynman.py"""
import numpy as np
from scipy.special import jn_zeros

def roda(N, m, rng):
    u, v = rng.random(N), rng.random(N)
    t = np.concatenate([[0.0], u + v, [2.0]]); x = np.concatenate([[0.0], u - v, [0.0]])
    o = np.argsort(t); t, x = t[o], x[o]
    dt = t[None, :] - t[:, None]; C = dt > np.abs(x[None, :] - x[:, None])
    Cf = C.astype(np.float64); L = C & ((Cf @ Cf) == 0)          # ligacoes (reducao transitiva)
    tau = np.sqrt(np.clip(dt**2 - (x[None, :] - x[:, None])**2, 0, None))
    psi = np.zeros(len(t), complex); psi[0] = 1.0
    for j in range(1, len(t)):
        pr = np.where(L[:, j])[0]
        psi[j] = np.sum(psi[pr]*np.exp(1j*m*tau[pr, j]))
    eq = np.abs(t - 1) < 0.1
    xe, pe = x[eq], psi[eq]
    bins = np.linspace(xe.min(), xe.max(), 31); idx = np.digitize(xe, bins) - 1
    re = np.array([np.mean(pe[idx == b].real) for b in range(30) if np.any(idx == b)])
    return int(np.sum(np.sign(re[1:]) != np.sign(re[:-1])))

rng = np.random.default_rng(1)
print('Trocas de sinal de Re(psi) no equador (media de 3 teias)')
print('   N       m = 10    m = 20    m = 40    m = 80')
for N in (400, 800, 1600, 3200):
    lin = [np.mean([roda(N, m, rng) for _ in range(3)]) for m in (10, 20, 40, 80)]
    print(f' {N:5d}   ' + '   '.join(f'{v:6.1f}' for v in lin), flush=True)
print('continuo (zeros de J0, dobrados para os dois lados) ' +
      '   '.join(f'{2*np.sum(jn_zeros(0, 40) < m):6d}' for m in (10, 20, 40, 80)) + '   (com 30 faixas o maximo medivel e 29)')
