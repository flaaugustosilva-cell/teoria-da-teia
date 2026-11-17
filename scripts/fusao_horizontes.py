"""Reflexao 11 (b): fronteiras que se fundem. 2+1, espaco plano, densidade 1 (grao l = 1).
Horizonte H = fronteira do passado de S, S = dois discos de raio R0 no tempo T, centros a distancia D.
Na fatia t0 o corte de H e a uniao de dois circulos de raio R = R0 + T - t0: separados (R < D/2) ou fundidos.
Conta moleculas de Barton (p no passado de S, q fora, p -> q, ambos abaixo da fatia, q unico no futuro de p
abaixo da fatia) e compara com a3 * perimetro e com a soma dos dois circulos isolados.
Aviso: este H nao e um horizonte de buraco negro; o teste e se a contagem acompanha a geometria na fusao.
Uso: python fusao_horizontes.py"""
import numpy as np
from math import pi, acos
a3 = 0.218853; D = 16.0; delta = 3.0

def perimetro_uniao(R):
    if R <= D/2: return 2*2*pi*R
    th = acos(D/(2*R)); return 4*R*(pi - th)

def conta(R, rng, so_um=False):
    cs = [np.array([-D/2, 0.0])] if so_um else [np.array([-D/2, 0.0]), np.array([D/2, 0.0])]
    caixa = np.array([[-D/2 - R - 2*delta, D/2 + R + 2*delta], [-R - 2*delta, R + 2*delta]])
    vol = delta*np.prod(caixa[:, 1] - caixa[:, 0]); n = rng.poisson(vol)
    t = -delta*rng.random(n); x = caixa[0, 0] + (caixa[0, 1]-caixa[0, 0])*rng.random(n)
    y = caixa[1, 0] + (caixa[1, 1]-caixa[1, 0])*rng.random(n)
    dist = np.min([np.hypot(x-c[0], y-c[1]) for c in cs], 0)
    perto = np.abs(dist - R) < 2*delta + 1
    t, x, y, dist = t[perto], x[perto], y[perto], dist[perto]
    passado = dist <= R - t        # raio do corte cresce para o passado (t <= 0, fatia em t = 0)
    dt = t[None, :] - t[:, None]; C = (dt > 0) & (dt*dt > (x[None, :]-x[:, None])**2 + (y[None, :]-y[:, None])**2)
    um = C.sum(1) == 1; idx = np.where(um & passado)[0]
    q = C[idx].argmax(1); return int(np.sum(~passado[q]))

rng = np.random.default_rng(5)
print(f'D = {D}. Separados se R < {D/2}. Teoria: moleculas = a3 * perimetro (a3 = {a3})')
print('   R   perimetro  2 circulos  | moleculas (uniao)  moleculas (2 x um circulo) | uniao/perimetro')
for R in (5.0, 7.0, 8.5, 10.0, 13.0, 18.0):
    m = [conta(R, rng) for _ in range(12)]; s = [conta(R, rng, True) for _ in range(12)]
    mu, eu = np.mean(m), np.std(m)/np.sqrt(len(m)); ms = 2*np.mean(s)
    P = perimetro_uniao(R)
    print(f' {R:5.1f}  {P:8.1f}  {4*pi*R:8.1f}   | {mu:7.1f} +- {eu:.1f}       {ms:7.1f}                   | {mu/P:.4f}', flush=True)
