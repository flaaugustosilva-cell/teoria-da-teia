"""H1, segunda etapa, E - analise EXPLORATORIA, feita depois do veredito pre-registrado (E-c). Nao altera o veredito.
(1) Colapso na variavel u = desvio(B)*theta, comparando Q com a previsao gaussiana exp(-u^2).
(2) De onde vem a variancia de B: variancias e covariancias de N0..N3 (B = n - N0 + 9N1 - 16N2 + 8N3).
Usa os mesmos dados (h1b_E_n{n}.npz). Uso: python h1b_E_exploratorio.py"""
import json, math, numpy as np
NS = (10, 20, 40, 80, 160)
TH = (0.01, 0.02, 0.03, 0.045, 0.06, 0.08, 0.10, 0.13, 0.16, 0.20, 0.25, 0.32)
res = json.load(open('h1b_E_resultados.json'))['E3']['tabela']
print('(1) Q medido contra a gaussiana exp(-(desvio*theta)^2), so pontos validos (Q > 4 ep):')
for n in NS:
    B = np.load(f'h1b_E_n{n}.npz')['B'].astype(float); sd = B.std(); linha = []
    for th in TH:
        q, e = res[f'{n}|{th}']
        if q > 4*e: linha.append(f'u={sd*th:4.2f}: {q:.3g}/{math.exp(-(sd*th)**2):.3g}')
    print(f' n={n:3d} (desvio {sd:6.1f}): ' + '  '.join(linha))
print('\n(2) Contribuicao para Var(B): coeficientes (-1, 9, -16, 8) aplicados a N0..N3')
from h1_robustez import sorteia
from h1b_E_dados import D
c = np.array([-1, 9, -16, 8])
for n in (20, 40, 80):
    rng = np.random.default_rng([20261121, 99, n]); p = sorteia(4000, n, D, rng)   # amostra auxiliar, semente derivada
    dt = p[:, None, :, 0] - p[:, :, None, 0]; dr2 = ((p[:, None, :, 1:] - p[:, :, None, 1:])**2).sum(-1)
    C = (dt > 0) & (dt*dt > dr2); Cf = C.astype(np.float32); K = np.rint(Cf @ Cf).astype(int)
    N = np.array([np.sum(C & (K == m), axis=(1, 2)) for m in range(4)]).T.astype(float)
    S = np.cov(N.T); tot = c @ S @ c
    diag = [c[i]**2*S[i, i]/tot for i in range(4)]
    print(f' n={n}: Var(B) = {tot:.0f}; termos diagonais (fracao): N0 {diag[0]:.2f}, N1 {diag[1]:.2f}, N2 {diag[2]:.2f}, N3 {diag[3]:.2f};'
          f' soma das covariancias cruzadas {1 - sum(diag):+.2f}; desvios de N0..N3: ' + ', '.join(f'{math.sqrt(S[i,i]):.1f}' for i in range(4)))
